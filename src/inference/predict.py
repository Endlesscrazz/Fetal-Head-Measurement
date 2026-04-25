"""Run segmentation inference and geometry post-processing."""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLBACKEND", "Agg")

import cv2
import numpy as np
import torch
import yaml

from src.data.dataset import HC18Dataset
from src.models import build_model
from src.training.trainer import select_device
from src.utils.geometry import mask_to_measurement, threshold_probability


def load_config(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        suffix = Path(path).suffix.lower()
        if suffix in {".yaml", ".yml"}:
            return yaml.safe_load(handle)
        return json.load(handle)


def load_model_from_checkpoint(checkpoint_path: str | Path, device: torch.device):
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model_config = checkpoint["model_config"]
    model = build_model(**model_config).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model, checkpoint


def tensor_to_uint8_image(image_tensor: torch.Tensor) -> np.ndarray:
    image = image_tensor.squeeze(0).detach().cpu().numpy()
    image = image - image.min()
    denom = image.max()
    if denom > 1e-6:
        image = image / denom
    return (image * 255).astype(np.uint8)


def save_mask(path: Path, mask: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), (mask.astype(np.uint8) * 255))


def save_overlay(path: Path, image: np.ndarray, mask: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    red = np.zeros_like(rgb)
    red[:, :, 2] = 255
    alpha = (mask > 0).astype(np.float32)[:, :, None] * 0.35
    overlay = (rgb * (1 - alpha) + red * alpha).astype(np.uint8)
    cv2.imwrite(str(path), overlay)


def predict_split(
    *,
    config: dict,
    checkpoint_path: str | Path,
    split: str = "val",
    output_dir: str | Path | None = None,
    threshold: float = 0.5,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    device = select_device(
        config["training"].get("device", "auto"),
        use_mps=bool(config["training"].get("mps", False)),
    )
    model, checkpoint = load_model_from_checkpoint(checkpoint_path, device)

    run_id = str(checkpoint.get("run_id", config["run"]["id"]))
    output_root = Path(output_dir or Path(config["run"].get("output_dir", "outputs/runs")) / run_id / "predictions")
    split_output = output_root / split
    mask_dir = split_output / "masks"
    overlay_dir = split_output / "overlays"
    records_path = split_output / "predictions.csv"
    split_output.mkdir(parents=True, exist_ok=True)

    dataset_config = config["dataset"]
    split_file = Path(config["splits"]["dir"]) / f"{split}.csv"
    dataset = HC18Dataset(
        dataset_config["root"],
        split_file=split_file,
        subset=dataset_config.get("subset", "training"),
        image_size=tuple(dataset_config["image_size"]),
        target_type=dataset_config.get("target_type", "filled"),
        band_width=int(dataset_config.get("band_width", 3)),
    )
    if limit is not None:
        dataset.records = dataset.records[:limit]

    records: list[dict[str, Any]] = []
    for sample in dataset:
        image = sample["image"].unsqueeze(0).to(device)
        with torch.no_grad():
            logits = model(image)
            probability = torch.sigmoid(logits).squeeze().detach().cpu().numpy()

        raw_mask = threshold_probability(probability, threshold=threshold)
        spacing = tuple(float(value) for value in sample["spacing"].tolist())
        image_uint8 = tensor_to_uint8_image(sample["image"])

        record: dict[str, Any] = {
            "sample_id": sample["sample_id"],
            "image_path": sample["image_path"],
            "split": split,
            "threshold": threshold,
            "spacing_x_mm": spacing[0],
            "spacing_y_mm": spacing[1],
            "target_hc_mm": sample["annotation"]["hc_mm"],
            "success": True,
            "failure_reason": "",
        }

        raw_mask_path = mask_dir / f"{sample['sample_id']}_raw.png"
        cleaned_mask_path = mask_dir / f"{sample['sample_id']}_cleaned.png"
        overlay_path = overlay_dir / f"{sample['sample_id']}_overlay.png"
        save_mask(raw_mask_path, raw_mask)

        try:
            measurement = mask_to_measurement(raw_mask, spacing)
            cleaned_mask = measurement["cleaned_mask"]
            ellipse = measurement["ellipse"]
            save_mask(cleaned_mask_path, cleaned_mask)
            save_overlay(overlay_path, image_uint8, cleaned_mask)
            record.update(
                {
                    "raw_mask_path": str(raw_mask_path),
                    "cleaned_mask_path": str(cleaned_mask_path),
                    "overlay_path": str(overlay_path),
                    "hc_pixels": measurement["hc_pixels"],
                    "hc_mm": measurement["hc_mm"],
                    **{f"ellipse_{key}": value for key, value in ellipse.to_dict().items()},
                }
            )
        except ValueError as exc:
            record["success"] = False
            record["failure_reason"] = str(exc)
            record.update(
                {
                    "raw_mask_path": str(raw_mask_path),
                    "cleaned_mask_path": "",
                    "overlay_path": "",
                    "hc_pixels": np.nan,
                    "hc_mm": np.nan,
                    "ellipse_center_x": np.nan,
                    "ellipse_center_y": np.nan,
                    "ellipse_semi_axis_a": np.nan,
                    "ellipse_semi_axis_b": np.nan,
                    "ellipse_angle_deg": np.nan,
                }
            )

        records.append(record)

    if records:
        with records_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)

    with (split_output / "predictions.json").open("w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2)

    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--split", default="val")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    records = predict_split(
        config=load_config(args.config),
        checkpoint_path=args.checkpoint,
        split=args.split,
        output_dir=args.output_dir,
        threshold=args.threshold,
        limit=args.limit,
    )
    print(f"Saved predictions for {len(records)} samples")


if __name__ == "__main__":
    main()
