"""Build local v1 report tables and figures from saved run artifacts."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("XDG_CACHE_HOME", str(PROJECT_ROOT / ".cache"))
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


DISPLAY_NAMES = {
    "unet_local_baseline": "U-Net + BCE/Dice",
    "attention_unet_local_baseline": "Attention U-Net + BCE/Dice",
    "attention_unet_dice_loss": "Attention U-Net + Dice",
    "attention_unet_aug": "Attention U-Net + BCE/Dice + Aug",
    "raw_contour_all_components": "Raw contour",
    "raw_largest_contour_ellipse": "Raw ellipse",
    "cleaned_contour": "Cleaned contour",
    "cleaned_ellipse": "Cleaned ellipse",
}


def _format_metric(value: float, decimals: int = 3) -> str:
    return f"{float(value):.{decimals}f}"


def _write_markdown_table(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text_frame = frame.copy()
    text_frame = text_frame.map(lambda value: f"{value:.4f}" if isinstance(value, float) else str(value))
    headers = list(text_frame.columns)
    rows = text_frame.values.tolist()
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _bar_plot(
    frame: pd.DataFrame,
    *,
    x_col: str,
    y_col: str,
    title: str,
    ylabel: str,
    path: Path,
    color: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(frame[x_col], frame[y_col], color=color)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", labelrotation=20)
    for label in ax.get_xticklabels():
        label.set_ha("right")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _load_local_summary(tables_dir: Path) -> pd.DataFrame:
    path = tables_dir / "local_ablation_summary.csv"
    frame = pd.read_csv(path)
    frame["display_name"] = frame["run_id"].map(DISPLAY_NAMES).fillna(frame["run_id"])
    return frame


def _load_postprocess_summary(tables_dir: Path) -> pd.DataFrame:
    path = tables_dir / "local_postprocess_ablation_summary.csv"
    frame = pd.read_csv(path)
    frame["display_name"] = frame["variant"].map(DISPLAY_NAMES).fillna(frame["variant"])
    return frame


def build_report_artifacts(tables_dir: Path, report_dir: Path) -> None:
    report_tables = report_dir / "tables"
    report_figures = report_dir / "figures"
    report_tables.mkdir(parents=True, exist_ok=True)
    report_figures.mkdir(parents=True, exist_ok=True)

    local_summary = _load_local_summary(tables_dir)
    postprocess_summary = _load_postprocess_summary(tables_dir)

    test_results = local_summary[local_summary["split"] == "test"].copy()
    test_results = test_results.sort_values(["mae_hc_mm", "rmse_hc_mm"], ascending=[True, True])
    main_columns = [
        "display_name",
        "run_id",
        "model",
        "loss",
        "augmentation",
        "image_size",
        "base_channels",
        "epochs",
        "split_id",
        "mean_dice",
        "mean_iou",
        "mean_hd95_mm",
        "mae_hc_mm",
        "rmse_hc_mm",
    ]
    main_results = test_results[main_columns].rename(columns={"display_name": "experiment"})
    main_results.to_csv(report_tables / "main_test_results.csv", index=False)

    ablation_results = local_summary[
        local_summary["run_id"].isin(
            [
                "attention_unet_local_baseline",
                "attention_unet_dice_loss",
                "attention_unet_aug",
            ]
        )
    ].copy()
    ablation_results = ablation_results[ablation_results["split"] == "test"]
    ablation_results = ablation_results.sort_values("mae_hc_mm")
    ablation_results = ablation_results[main_columns].rename(columns={"display_name": "experiment"})
    ablation_results.to_csv(report_tables / "attention_unet_ablation_test_results.csv", index=False)

    postprocess_test = postprocess_summary[postprocess_summary["split"] == "test"].copy()
    postprocess_test = postprocess_test.sort_values("mae_hc_mm")
    postprocess_test = postprocess_test[
        [
            "display_name",
            "variant",
            "n_samples",
            "success_rate",
            "mean_signed_hc_error_mm",
            "mae_hc_mm",
            "rmse_hc_mm",
        ]
    ].rename(columns={"display_name": "postprocess_variant"})
    postprocess_test.to_csv(report_tables / "postprocess_test_results.csv", index=False)

    _write_markdown_table(main_results, report_tables / "main_test_results.md")
    _write_markdown_table(ablation_results, report_tables / "attention_unet_ablation_test_results.md")
    _write_markdown_table(postprocess_test, report_tables / "postprocess_test_results.md")

    _bar_plot(
        main_results,
        x_col="experiment",
        y_col="mae_hc_mm",
        title="Internal-Test HC MAE by Local Experiment",
        ylabel="HC MAE (mm)",
        path=report_figures / "main_test_hc_mae.png",
        color="#4c78a8",
    )
    _bar_plot(
        main_results,
        x_col="experiment",
        y_col="mean_dice",
        title="Internal-Test Dice by Local Experiment",
        ylabel="Mean Dice",
        path=report_figures / "main_test_dice.png",
        color="#59a14f",
    )
    _bar_plot(
        postprocess_test,
        x_col="postprocess_variant",
        y_col="mae_hc_mm",
        title="Internal-Test HC MAE by Post-Processing Variant",
        ylabel="HC MAE (mm)",
        path=report_figures / "postprocess_test_hc_mae.png",
        color="#e15759",
    )

    best = main_results.iloc[0]
    setup = {
        "split_id": best["split_id"],
        "image_size": best["image_size"],
        "base_channels": best["base_channels"],
        "epochs": best["epochs"],
    }

    summary = f"""# Local V1 Report Results Summary

These artifacts summarize the local reduced-resource v1 experiments for the
HC18 fetal head circumference project.

## Local Setup

- Split id: `{setup["split_id"]}`
- Train/val/internal-test counts: 698 / 152 / 149
- Image size: `{setup["image_size"]}`
- Base channels: `{setup["base_channels"]}`
- Epochs per reported local run: `{setup["epochs"]}`
- Compute: MacBook MPS
- Final HC measurement method: cleaned largest component + ellipse fitting

The local setup uses the full labeled HC18 training split partition but reduced
image resolution and model width. This should be disclosed in the course report.

## Best Local Model

Best internal-test model by HC MAE:

- Experiment: {best["experiment"]}
- Run id: `{best["run_id"]}`
- Dice: {_format_metric(best["mean_dice"], 4)}
- IoU: {_format_metric(best["mean_iou"], 4)}
- HD95: {_format_metric(best["mean_hd95_mm"], 2)} mm
- HC MAE: {_format_metric(best["mae_hc_mm"], 2)} mm
- HC RMSE: {_format_metric(best["rmse_hc_mm"], 2)} mm

## Report Tables

- `report/tables/main_test_results.csv`
- `report/tables/attention_unet_ablation_test_results.csv`
- `report/tables/postprocess_test_results.csv`

## Report Figures

- `report/figures/main_test_hc_mae.png`
- `report/figures/main_test_dice.png`
- `report/figures/postprocess_test_hc_mae.png`

## Suggested Interpretation

Attention U-Net with BCE+Dice gave the best local v1 result. Dice-only loss and
the simple augmentation recipe did not improve internal-test HC error. Direct
contour-length measurement substantially overestimated HC, while ellipse fitting
reduced HC error and supports the segmentation-to-geometry design.
"""
    (report_dir / "report-results-summary.md").write_text(summary, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tables-dir", default="outputs/tables")
    parser.add_argument("--report-dir", default="report")
    args = parser.parse_args()

    build_report_artifacts(Path(args.tables_dir), Path(args.report_dir))
    print(f"Saved report artifacts under {args.report_dir}")


if __name__ == "__main__":
    main()
