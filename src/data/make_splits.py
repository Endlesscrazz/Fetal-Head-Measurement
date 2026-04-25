"""Create deterministic train/val/internal-test splits for HC18."""

from __future__ import annotations

import argparse
import random
from collections import defaultdict
from pathlib import Path

import pandas as pd
import yaml

from src.data.dataset import discover_hc18_records, group_id_from_sample_id


def load_config(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def split_groups(
    group_to_filenames: dict[str, list[str]],
    *,
    seed: int,
    train_fraction: float,
    val_fraction: float,
) -> tuple[list[str], list[str], list[str]]:
    """Split grouped filenames deterministically."""

    groups = sorted(group_to_filenames)
    rng = random.Random(seed)
    rng.shuffle(groups)

    n_groups = len(groups)
    n_train = int(round(n_groups * train_fraction))
    n_val = int(round(n_groups * val_fraction))
    n_train = min(n_train, n_groups)
    n_val = min(n_val, max(0, n_groups - n_train))

    train_groups = groups[:n_train]
    val_groups = groups[n_train : n_train + n_val]
    test_groups = groups[n_train + n_val :]

    def flatten(selected: list[str]) -> list[str]:
        filenames: list[str] = []
        for group in selected:
            filenames.extend(group_to_filenames[group])
        return sorted(filenames)

    return flatten(train_groups), flatten(val_groups), flatten(test_groups)


def write_split(path: Path, filenames: list[str]) -> None:
    rows = [
        {
            "filename": filename,
            "sample_id": Path(filename).stem,
            "group_id": group_id_from_sample_id(Path(filename).stem),
        }
        for filename in filenames
    ]
    pd.DataFrame(rows).to_csv(path, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/data.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    dataset_cfg = config["dataset"]
    split_cfg = config["splits"]

    records = discover_hc18_records(
        dataset_cfg["root"],
        subset=dataset_cfg.get("subset", "training"),
    )
    if not records:
        raise SystemExit(
            "No HC18 image files found. Place the dataset under "
            f"{dataset_cfg['root']} before creating splits."
        )

    group_to_filenames: dict[str, list[str]] = defaultdict(list)
    for record in records:
        group_id = (
            group_id_from_sample_id(record.sample_id)
            if split_cfg.get("group_by_exam_prefix", True)
            else record.sample_id
        )
        group_to_filenames[group_id].append(record.image_path.name)

    train, val, test = split_groups(
        group_to_filenames,
        seed=int(split_cfg["seed"]),
        train_fraction=float(split_cfg["train_fraction"]),
        val_fraction=float(split_cfg["val_fraction"]),
    )

    output_dir = Path(split_cfg["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    write_split(output_dir / "train.csv", train)
    write_split(output_dir / "val.csv", val)
    write_split(output_dir / "test.csv", test)

    summary = pd.DataFrame(
        [
            {"split": "train", "n": len(train)},
            {"split": "val", "n": len(val)},
            {"split": "test", "n": len(test)},
        ]
    )
    summary.to_csv(output_dir / "summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
