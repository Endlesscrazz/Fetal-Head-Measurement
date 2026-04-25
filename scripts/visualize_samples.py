#!/usr/bin/env python3
"""Save image/mask overlay sanity checks for HC18 samples."""

from __future__ import annotations

import argparse
import os
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("XDG_CACHE_HOME", str(PROJECT_ROOT / ".cache"))
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
import yaml

from src.data.dataset import HC18Dataset


def load_config(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/data.yaml")
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    config = load_config(args.config)
    dataset_cfg = config["dataset"]
    viz_cfg = config["visualization"]
    split_file = Path(viz_cfg["split_file"])

    dataset = HC18Dataset(
        dataset_cfg["root"],
        split_file=split_file if split_file.exists() else None,
        subset=dataset_cfg.get("subset", "training"),
        image_size=tuple(dataset_cfg["image_size"]),
        target_type=dataset_cfg.get("target_type", "filled"),
        band_width=int(dataset_cfg.get("band_width", 3)),
    )
    if len(dataset) == 0:
        raise SystemExit(
            "No samples available for visualization. Place HC18 data under "
            f"{dataset_cfg['root']} and create splits first."
        )

    rng = random.Random(args.seed)
    indices = list(range(len(dataset)))
    rng.shuffle(indices)
    selected = indices[: min(args.n, len(indices))]

    output_dir = Path(viz_cfg["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    for index in selected:
        sample = dataset[index]
        image = sample["image"].squeeze(0)
        mask = sample["mask"].squeeze(0)
        image = (image - image.min()) / torch.clamp(image.max() - image.min(), min=1e-6)

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.imshow(image.numpy(), cmap="gray")
        ax.imshow(mask.numpy(), cmap="Reds", alpha=0.35)
        ax.set_title(sample["sample_id"])
        ax.axis("off")
        fig.tight_layout()
        fig.savefig(output_dir / f"{sample['sample_id']}_overlay.png", dpi=150)
        plt.close(fig)

    print(f"Saved {len(selected)} overlays to {output_dir}")


if __name__ == "__main__":
    main()
