"""Compare HC measurement post-processing variants for saved predictions."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics import absolute_error, rmse, signed_error
from src.utils.geometry import (
    ellipse_circumference_mm,
    extract_largest_contour,
    fit_ellipse_to_contour,
    mask_contour_length_mm,
)


def read_binary_mask(path: str | Path) -> np.ndarray:
    mask = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise FileNotFoundError(f"Could not read mask: {path}")
    return (mask > 0).astype(np.uint8)


def safe_measure(name: str, func) -> dict[str, object]:
    try:
        return {"variant": name, "success": True, "failure_reason": "", "pred_hc_mm": float(func())}
    except ValueError as exc:
        return {"variant": name, "success": False, "failure_reason": str(exc), "pred_hc_mm": math.nan}


def measure_variants(prediction: pd.Series) -> list[dict[str, object]]:
    spacing = (float(prediction["spacing_x_mm"]), float(prediction["spacing_y_mm"]))
    raw_mask = read_binary_mask(prediction["raw_mask_path"])
    cleaned_mask = read_binary_mask(prediction["cleaned_mask_path"])

    return [
        safe_measure(
            "raw_contour_all_components",
            lambda: mask_contour_length_mm(raw_mask, spacing, keep_largest_component=False),
        ),
        safe_measure(
            "raw_largest_contour_ellipse",
            lambda: ellipse_circumference_mm(
                fit_ellipse_to_contour(extract_largest_contour(raw_mask)),
                spacing,
            ),
        ),
        safe_measure(
            "cleaned_contour",
            lambda: mask_contour_length_mm(cleaned_mask, spacing, keep_largest_component=True),
        ),
        safe_measure(
            "cleaned_ellipse",
            lambda: float(prediction["hc_mm"]),
        ),
    ]


def build_postprocess_ablation(run_id: str, split: str, runs_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    predictions_path = runs_dir / run_id / "predictions" / split / "predictions.csv"
    predictions = pd.read_csv(predictions_path)

    rows: list[dict[str, object]] = []
    for _, prediction in predictions.iterrows():
        target_hc = float(prediction["target_hc_mm"])
        for measured in measure_variants(prediction):
            pred_hc = float(measured["pred_hc_mm"])
            signed = signed_error(pred_hc, target_hc) if measured["success"] else math.nan
            rows.append(
                {
                    "run_id": run_id,
                    "split": split,
                    "sample_id": prediction["sample_id"],
                    "variant": measured["variant"],
                    "success": measured["success"],
                    "target_hc_mm": target_hc,
                    "pred_hc_mm": pred_hc,
                    "signed_hc_error_mm": signed,
                    "abs_hc_error_mm": absolute_error(pred_hc, target_hc) if measured["success"] else math.nan,
                    "failure_reason": measured["failure_reason"],
                }
            )

    per_sample = pd.DataFrame(rows)
    aggregate_rows = []
    for variant, group in per_sample.groupby("variant", sort=False):
        finite_signed = group["signed_hc_error_mm"].replace([np.inf, -np.inf], np.nan).dropna()
        finite_abs = group["abs_hc_error_mm"].replace([np.inf, -np.inf], np.nan).dropna()
        aggregate_rows.append(
            {
                "run_id": run_id,
                "split": split,
                "variant": variant,
                "n_samples": len(group),
                "success_rate": float(group["success"].mean()) if len(group) else math.nan,
                "mean_signed_hc_error_mm": float(finite_signed.mean()) if len(finite_signed) else math.nan,
                "mae_hc_mm": float(finite_abs.mean()) if len(finite_abs) else math.nan,
                "rmse_hc_mm": rmse(finite_signed.to_numpy(dtype=float)),
            }
        )

    aggregate = pd.DataFrame(aggregate_rows)
    return per_sample, aggregate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--split", required=True)
    parser.add_argument("--runs-dir", default="outputs/runs")
    args = parser.parse_args()

    runs_dir = Path(args.runs_dir)
    per_sample, aggregate = build_postprocess_ablation(args.run_id, args.split, runs_dir)

    eval_dir = runs_dir / args.run_id / "evaluation" / args.split
    eval_dir.mkdir(parents=True, exist_ok=True)
    per_sample_path = eval_dir / "postprocess_ablation_per_sample.csv"
    aggregate_path = eval_dir / "postprocess_ablation_aggregate.csv"
    per_sample.to_csv(per_sample_path, index=False)
    aggregate.to_csv(aggregate_path, index=False)

    table_dir = Path("outputs/tables")
    table_dir.mkdir(parents=True, exist_ok=True)
    aggregate.to_csv(table_dir / f"{args.run_id}_{args.split}_postprocess_ablation.csv", index=False)

    print(aggregate.to_string(index=False))
    print(f"Saved per-sample post-processing ablation to {per_sample_path}")
    print(f"Saved aggregate post-processing ablation to {aggregate_path}")


if __name__ == "__main__":
    main()
