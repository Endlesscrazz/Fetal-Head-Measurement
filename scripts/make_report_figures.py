#!/usr/bin/env python3
"""Create report-ready figures from evaluation artifacts."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("XDG_CACHE_HOME", str(PROJECT_ROOT / ".cache"))
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".matplotlib_cache"))

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def _save_histogram(values, title: str, xlabel: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.hist(values.dropna(), bins=min(12, max(3, len(values.dropna()))), color="#4c78a8")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _save_qualitative_panel(frame: pd.DataFrame, path: Path, max_items: int = 4) -> None:
    available = frame[frame["overlay_path"].astype(str).map(lambda p: Path(p).exists())]
    if available.empty:
        return

    panel = available.sort_values("abs_hc_error_mm", ascending=False).head(max_items)
    fig, axes = plt.subplots(1, len(panel), figsize=(4 * len(panel), 3.5))
    if len(panel) == 1:
        axes = [axes]

    for ax, (_, row) in zip(axes, panel.iterrows()):
        image = cv2.imread(str(row["overlay_path"]), cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ax.imshow(image)
        ax.set_title(f"{row['sample_id']}\nAbs HC err: {row['abs_hc_error_mm']:.1f} mm")
        ax.axis("off")

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--split", default="val")
    parser.add_argument("--metrics", default=None)
    args = parser.parse_args()

    metrics_path = Path(args.metrics or f"outputs/runs/{args.run_id}/evaluation/{args.split}/per_sample_metrics.csv")
    frame = pd.read_csv(metrics_path)

    output_dir = Path("outputs/figures") / args.run_id
    _save_histogram(
        frame["dice"],
        title=f"{args.run_id} {args.split} Dice",
        xlabel="Dice",
        path=output_dir / f"{args.split}_dice_histogram.png",
    )
    _save_histogram(
        frame["abs_hc_error_mm"],
        title=f"{args.run_id} {args.split} HC Error",
        xlabel="Absolute HC error (mm)",
        path=output_dir / f"{args.split}_hc_error_histogram.png",
    )
    _save_qualitative_panel(frame, output_dir / f"{args.split}_qualitative_failures.png")
    print(f"Saved report figures to {output_dir}")


if __name__ == "__main__":
    main()
