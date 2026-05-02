"""Export curated v2 saved-output demo artifacts."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pandas as pd
import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.validate_demo_manifest import REQUIRED_SAFETY_TEXT, validate_manifest
from src.data.dataset import HC18Dataset
from src.inference.predict import load_model_from_checkpoint
from src.inference.predict import save_mask
from src.utils.geometry import mask_contour_length_mm


DEFAULT_CURATED_PATH = Path("docs/v2_demo/curated-samples.json")
DEFAULT_OUTPUT_DIR = Path("outputs/demo_samples")


def _load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def _to_builtin(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _to_builtin(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_to_builtin(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


def _read_binary_mask(path: str | Path) -> np.ndarray:
    mask = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise FileNotFoundError(f"Could not read mask: {path}")
    return (mask > 0).astype(np.uint8)


def _tensor_to_uint8_image(image_tensor) -> np.ndarray:
    image = image_tensor.squeeze(0).detach().cpu().numpy()
    image = image - image.min()
    denom = image.max()
    if denom > 1e-6:
        image = image / denom
    return (image * 255).astype(np.uint8)


def _probability_to_uint8(probability: np.ndarray) -> np.ndarray:
    return np.clip(np.rint(probability * 255.0), 0, 255).astype(np.uint8)


def _run_probability_inference(model: torch.nn.Module, image_tensor: torch.Tensor, device: torch.device) -> np.ndarray:
    image = image_tensor.unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(image)
        probability = torch.sigmoid(logits).squeeze().detach().cpu().numpy()
    return probability.astype(np.float32)


def _category_for_frontend(category: str) -> str:
    if category in {"strong", "typical", "failure"}:
        return category
    if category in {"high_error", "edge"}:
        return "failure"
    if category in {"cleanup_ellipse", "cleanup", "ellipse"}:
        return "typical"
    return "typical"


def _summary_from_curated(curated_sample: dict[str, Any]) -> str:
    reason = str(curated_sample.get("reason", "")).strip()
    if reason:
        return reason
    return str(curated_sample.get("label", curated_sample.get("id", "")))


def _load_curated_samples(path: Path, sample_ids: list[str] | None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    curated = _load_json(path)
    samples = list(curated.get("samples", []))
    if sample_ids:
        by_id = {str(sample["id"]): sample for sample in samples}
        selected = []
        for sample_id in sample_ids:
            selected.append(
                by_id.get(
                    sample_id,
                    {
                        "id": sample_id,
                        "label": sample_id,
                        "category": "custom",
                        "tags": ["custom"],
                        "reason": "Selected through --sample-id override.",
                    },
                )
            )
        samples = selected
    if not samples:
        raise ValueError("No curated samples found")
    return curated, samples


def _build_dataset_by_sample(config: dict[str, Any], split: str) -> dict[str, dict[str, Any]]:
    dataset_config = config["dataset"]
    dataset = HC18Dataset(
        dataset_config["root"],
        split_file=Path(config["splits"]["dir"]) / f"{split}.csv",
        subset=dataset_config.get("subset", "training"),
        image_size=tuple(dataset_config["image_size"]),
        target_type=dataset_config.get("target_type", "filled"),
        band_width=int(dataset_config.get("band_width", 3)),
    )
    return {str(sample["sample_id"]): sample for sample in dataset}


def _require_raw_data(config: dict[str, Any]) -> None:
    dataset_root = PROJECT_ROOT / str(config["dataset"]["root"])
    training_set = dataset_root / "training_set"
    if not training_set.exists():
        raise FileNotFoundError(
            "V2 demo export requires local raw HC18 training data at "
            f"{training_set}. After export, the saved-output app does not need raw data."
        )


def _copy_required_file(source: str | Path, destination: Path) -> None:
    source = PROJECT_ROOT / source if not Path(source).is_absolute() else Path(source)
    if not source.exists():
        raise FileNotFoundError(f"Missing source artifact: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def export_demo_artifacts(
    *,
    run_id: str,
    split: str,
    curated_path: str | Path = DEFAULT_CURATED_PATH,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    sample_ids: list[str] | None = None,
) -> dict[str, Any]:
    curated_path = Path(curated_path)
    output_dir = PROJECT_ROOT / output_dir
    run_dir = PROJECT_ROOT / "outputs" / "runs" / run_id
    config_path = run_dir / "config.json"
    predictions_path = run_dir / "predictions" / split / "predictions.csv"
    metrics_path = run_dir / "evaluation" / split / "per_sample_metrics.csv"
    checkpoint_path = run_dir / "best_model.pt"

    config = _load_json(config_path)
    _require_raw_data(config)
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Missing checkpoint required for prob.png export: {checkpoint_path}")

    curated, curated_samples = _load_curated_samples(curated_path, sample_ids)
    dataset_by_sample = _build_dataset_by_sample(config, split)
    predictions = pd.read_csv(predictions_path).set_index("sample_id")
    metrics = pd.read_csv(metrics_path).set_index("sample_id")
    device = torch.device("cpu")
    model, _ = load_model_from_checkpoint(checkpoint_path, device)

    manifest_samples: list[dict[str, Any]] = []
    for curated_sample in curated_samples:
        sample_id = str(curated_sample["id"])
        if sample_id not in dataset_by_sample:
            raise KeyError(f"{sample_id} is not present in split {split}")
        if sample_id not in predictions.index:
            raise KeyError(f"{sample_id} is missing from {predictions_path}")
        if sample_id not in metrics.index:
            raise KeyError(f"{sample_id} is missing from {metrics_path}")

        sample = dataset_by_sample[sample_id]
        prediction = predictions.loc[sample_id]
        metric = metrics.loc[sample_id]
        sample_dir = output_dir / sample_id

        ultrasound_path = sample_dir / "ultrasound.png"
        target_path = sample_dir / "target.png"
        pred_path = sample_dir / "pred.png"
        prob_path = sample_dir / "prob.png"
        metadata_path = sample_dir / "metadata.json"

        image_uint8 = _tensor_to_uint8_image(sample["image"])
        ultrasound_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(ultrasound_path), image_uint8)
        save_mask(target_path, sample["mask"].squeeze(0).detach().cpu().numpy())
        _copy_required_file(prediction["cleaned_mask_path"], pred_path)

        probability = _run_probability_inference(model, sample["image"], device)
        if probability.shape != image_uint8.shape:
            raise ValueError(
                f"{sample_id}: probability shape {probability.shape} does not match image shape {image_uint8.shape}"
            )
        cv2.imwrite(str(prob_path), _probability_to_uint8(probability))

        spacing = (float(prediction["spacing_x_mm"]), float(prediction["spacing_y_mm"]))
        cleaned_mask = _read_binary_mask(pred_path)
        if cleaned_mask.shape != probability.shape:
            raise ValueError(
                f"{sample_id}: mask shape {cleaned_mask.shape} does not match probability shape {probability.shape}"
            )
        contour_hc_mm = mask_contour_length_mm(cleaned_mask, spacing, keep_largest_component=True)
        if np.any(cleaned_mask):
            confidence = float(probability[cleaned_mask > 0].mean())
        else:
            raise ValueError(f"{sample_id}: cleaned mask is empty; cannot compute confidence")

        angle_deg = float(prediction["ellipse_angle_deg"])
        pred_ellipse = {
            "cx": float(prediction["ellipse_center_x"]),
            "cy": float(prediction["ellipse_center_y"]),
            "rx": float(prediction["ellipse_semi_axis_a"]),
            "ry": float(prediction["ellipse_semi_axis_b"]),
            "rot": float(math.radians(angle_deg)),
        }
        frontend_category = _category_for_frontend(str(curated_sample.get("category", "")))
        metrics_payload = {
            "dice": float(metric["dice"]),
            "iou": float(metric["iou"]),
            "hd95_mm": float(metric["hd95_mm"]),
            "hcErr": float(metric["abs_hc_error_mm"]),
            "predHC": float(metric["pred_hc_mm"]),
            "targetHC": float(metric["target_hc_mm"]),
        }
        resolution = {"w": int(image_uint8.shape[1]), "h": int(image_uint8.shape[0])}

        metadata = {
            "sample_id": sample_id,
            "run_id": run_id,
            "split": split,
            "cat": frontend_category,
            "source_category": str(curated_sample.get("category", "")),
            "label": str(curated_sample.get("label", sample_id)),
            "summary": _summary_from_curated(curated_sample),
            "tags": list(curated_sample.get("tags", [])),
            "reason": str(curated_sample.get("reason", "")),
            "threshold": float(prediction["threshold"]),
            "spacing_x_mm": spacing[0],
            "spacing_y_mm": spacing[1],
            "spacingXMm": spacing[0],
            "spacingYMm": spacing[1],
            "hc_pred_mm": float(metric["pred_hc_mm"]),
            "hc_gt_mm": float(metric["target_hc_mm"]),
            "metrics": metrics_payload,
            **metrics_payload,
            "signed_hc_error_mm": float(metric["signed_hc_error_mm"]),
            "ellipse_params": {
                "center_x": pred_ellipse["cx"],
                "center_y": pred_ellipse["cy"],
                "semi_axis_a": pred_ellipse["rx"],
                "semi_axis_b": pred_ellipse["ry"],
                "angle_deg": angle_deg,
            },
            "predEllipse": pred_ellipse,
            "contourHC": float(contour_hc_mm),
            "confidence": confidence,
            "resolution": resolution,
            "artifacts": {
                "ultrasound": ultrasound_path.name,
                "target": target_path.name,
                "pred": pred_path.name,
                "prob": prob_path.name,
            },
            "notes": str(curated_sample.get("reason", "")),
        }
        _write_json(metadata_path, {key: _to_builtin(value) for key, value in metadata.items()})

        manifest_samples.append(
            {
                "id": sample_id,
                "label": str(curated_sample.get("label", sample_id)),
                "cat": frontend_category,
                "split": split,
                "summary": _summary_from_curated(curated_sample),
                "metrics": metrics_payload,
                "predEllipse": pred_ellipse,
                "contourHC": float(contour_hc_mm),
                "confidence": confidence,
                "spacingXMm": spacing[0],
                "spacingYMm": spacing[1],
                "resolution": resolution,
                "notes": str(curated_sample.get("reason", "")),
            }
        )

    manifest = {
        "schema_version": 2,
        "created_from_run_id": run_id,
        "created_from_split": split,
        "curated_samples_path": str(curated_path),
        "source_metrics_path": curated.get("source_metrics_path", str(metrics_path.relative_to(PROJECT_ROOT))),
        "source_predictions_path": curated.get("source_predictions_path", str(predictions_path.relative_to(PROJECT_ROOT))),
        "safety_text": REQUIRED_SAFETY_TEXT,
        "samples": manifest_samples,
    }
    _write_json(output_dir / "manifest.json", manifest)

    errors = validate_manifest(manifest, repo_root=PROJECT_ROOT, artifact_root=output_dir)
    if errors:
        raise ValueError("Exported manifest failed validation:\n" + "\n".join(errors))

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default="attention_unet_local_baseline")
    parser.add_argument("--split", default="test")
    parser.add_argument("--curated", default=str(DEFAULT_CURATED_PATH))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--sample-id", action="append", dest="sample_ids", default=None)
    args = parser.parse_args()

    manifest = export_demo_artifacts(
        run_id=args.run_id,
        split=args.split,
        curated_path=args.curated,
        output_dir=args.output_dir,
        sample_ids=args.sample_ids,
    )
    print(f"Exported {len(manifest['samples'])} demo samples to {args.output_dir}")
    print(f"Manifest: {Path(args.output_dir) / 'manifest.json'}")


if __name__ == "__main__":
    main()
