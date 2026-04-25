"""Training entrypoint."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from src.training.trainer import train_from_config


def load_config(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    artifacts = train_from_config(load_config(args.config))
    print(f"Run directory: {artifacts.run_dir}")
    print(f"Best checkpoint: {artifacts.best_checkpoint}")
    print(f"Metrics: {artifacts.metrics_csv}")


if __name__ == "__main__":
    main()
