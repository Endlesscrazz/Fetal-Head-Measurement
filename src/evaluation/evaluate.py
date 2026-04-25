"""Evaluate segmentation predictions and HC measurements."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

from src.data.dataset import HC18Dataset
from src.evaluation.metrics import absolute_error, dice_score, hd95, iou_score, rmse, signed_error
from src.inference.predict import load_config, predict_split


def _dataset_by_sample_id(config: dict, split: str, limit: int | None) -> dict[str, dict]:
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
    return {dataset[index]["sample_id"]: dataset[index] for index in range(len(dataset))}


def _read_binary_mask(path: str | Path) -> np.ndarray:
    mask = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise FileNotFoundError(f"Could not read mask: {path}")
    return (mask > 0).astype(np.uint8)


def evaluate_checkpoint(
    *,
    config: dict,
    checkpoint_path: str | Path,
    split: str = "val",
    threshold: float = 0.5,
    limit: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    predictions = predict_split(
        config=config,
        checkpoint_path=checkpoint_path,
        split=split,
        threshold=threshold,
        limit=limit,
    )
    samples = _dataset_by_sample_id(config, split, limit)

    rows: list[dict] = []
    for prediction in predictions:
        sample_id = prediction["sample_id"]
        sample = samples[sample_id]
        target_mask = sample["mask"].squeeze(0).numpy().astype(np.uint8)

        if prediction["success"]:
            pred_mask = _read_binary_mask(prediction["cleaned_mask_path"])
            dice = dice_score(pred_mask, target_mask)
            iou = iou_score(pred_mask, target_mask)
            hausdorff95 = hd95(
                pred_mask,
                target_mask,
                spacing_mm=(float(prediction["spacing_x_mm"]), float(prediction["spacing_y_mm"])),
            )
            target_hc = sample["annotation"]["hc_mm"]
            pred_hc = float(prediction["hc_mm"])
            signed_hc_error = signed_error(pred_hc, float(target_hc)) if target_hc is not None else math.nan
            abs_hc_error = absolute_error(pred_hc, float(target_hc)) if target_hc is not None else math.nan
        else:
            dice = math.nan
            iou = math.nan
            hausdorff95 = math.inf
            target_hc = sample["annotation"]["hc_mm"]
            pred_hc = math.nan
            signed_hc_error = math.nan
            abs_hc_error = math.nan

        rows.append(
            {
                "sample_id": sample_id,
                "split": split,
                "success": prediction["success"],
                "dice": dice,
                "iou": iou,
                "hd95_mm": hausdorff95,
                "target_hc_mm": target_hc,
                "pred_hc_mm": pred_hc,
                "signed_hc_error_mm": signed_hc_error,
                "abs_hc_error_mm": abs_hc_error,
                "overlay_path": prediction.get("overlay_path", ""),
                "failure_reason": prediction.get("failure_reason", ""),
            }
        )

    per_sample = pd.DataFrame(rows)
    finite_abs = per_sample["abs_hc_error_mm"].replace([np.inf, -np.inf], np.nan).dropna()
    finite_signed = per_sample["signed_hc_error_mm"].replace([np.inf, -np.inf], np.nan).dropna()
    aggregate = pd.DataFrame(
        [
            {
                "split": split,
                "n_samples": len(per_sample),
                "success_rate": float(per_sample["success"].mean()) if len(per_sample) else math.nan,
                "mean_dice": float(per_sample["dice"].mean()),
                "mean_iou": float(per_sample["iou"].mean()),
                "mean_hd95_mm": float(
                    per_sample["hd95_mm"].replace([np.inf, -np.inf], np.nan).mean()
                ),
                "mean_signed_hc_error_mm": float(finite_signed.mean()) if len(finite_signed) else math.nan,
                "mae_hc_mm": float(finite_abs.mean()) if len(finite_abs) else math.nan,
                "rmse_hc_mm": rmse(finite_signed.to_numpy(dtype=float)),
            }
        ]
    )

    run_id = str(config["run"]["id"])
    eval_dir = Path(config["run"].get("output_dir", "outputs/runs")) / run_id / "evaluation" / split
    eval_dir.mkdir(parents=True, exist_ok=True)
    per_sample.to_csv(eval_dir / "per_sample_metrics.csv", index=False)
    aggregate.to_csv(eval_dir / "aggregate_metrics.csv", index=False)

    Path("outputs/tables").mkdir(parents=True, exist_ok=True)
    aggregate.to_csv(Path("outputs/tables") / f"{run_id}_{split}_summary.csv", index=False)
    return per_sample, aggregate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--split", default="val")
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    per_sample, aggregate = evaluate_checkpoint(
        config=load_config(args.config),
        checkpoint_path=args.checkpoint,
        split=args.split,
        threshold=args.threshold,
        limit=args.limit,
    )
    print(f"Evaluated {len(per_sample)} samples")
    print(aggregate.to_string(index=False))


if __name__ == "__main__":
    main()
