#!/usr/bin/env python3
"""Run a tiny local training smoke test."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.training.train import load_config
from src.training.trainer import train_from_config


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/unet_smoke.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    artifacts = train_from_config(config)
    print(f"Smoke run completed: {artifacts.run_dir}")


if __name__ == "__main__":
    main()
