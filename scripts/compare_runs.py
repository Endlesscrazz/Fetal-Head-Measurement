"""Create a comparison table from saved run evaluation summaries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def load_run_config(run_id: str, runs_dir: Path) -> dict:
    config_path = runs_dir / run_id / "config.json"
    with config_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_label(config: dict) -> str:
    model = config["model"]["name"]
    loss = config["loss"]["name"]
    augmentation = config.get("augmentation", {})
    aug_label = "+aug" if augmentation.get("enabled", False) else "no_aug"
    return f"{model}_{loss}_{aug_label}"


def load_summary(run_id: str, split: str, runs_dir: Path) -> dict:
    summary_path = runs_dir / run_id / "evaluation" / split / "aggregate_metrics.csv"
    frame = pd.read_csv(summary_path)
    if len(frame) != 1:
        raise ValueError(f"Expected one row in {summary_path}, found {len(frame)}")
    return frame.iloc[0].to_dict()


def build_comparison(run_ids: list[str], splits: list[str], runs_dir: Path) -> pd.DataFrame:
    rows: list[dict] = []
    for run_id in run_ids:
        config = load_run_config(run_id, runs_dir)
        for split in splits:
            summary = load_summary(run_id, split, runs_dir)
            rows.append(
                {
                    "run_id": run_id,
                    "label": run_label(config),
                    "split": split,
                    "model": config["model"]["name"],
                    "loss": config["loss"]["name"],
                    "augmentation": bool(config.get("augmentation", {}).get("enabled", False)),
                    "image_size": "x".join(str(v) for v in config["dataset"]["image_size"]),
                    "base_channels": config["model"]["base_channels"],
                    "epochs": config["training"]["epochs"],
                    "split_id": config["splits"].get("split_id", ""),
                    "mean_dice": summary["mean_dice"],
                    "mean_iou": summary["mean_iou"],
                    "mean_hd95_mm": summary["mean_hd95_mm"],
                    "mean_signed_hc_error_mm": summary["mean_signed_hc_error_mm"],
                    "mae_hc_mm": summary["mae_hc_mm"],
                    "rmse_hc_mm": summary["rmse_hc_mm"],
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", nargs="+", required=True)
    parser.add_argument("--splits", nargs="+", default=["val", "test"])
    parser.add_argument("--runs-dir", default="outputs/runs")
    parser.add_argument("--output", default="outputs/tables/local_ablation_summary.csv")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    comparison = build_comparison(args.runs, args.splits, Path(args.runs_dir))
    comparison.to_csv(output_path, index=False)
    print(comparison.to_string(index=False))
    print(f"Saved comparison table to {output_path}")


if __name__ == "__main__":
    main()
