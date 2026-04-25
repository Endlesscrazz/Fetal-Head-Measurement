"""Config-driven segmentation trainer."""

from __future__ import annotations

import csv
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader

from src.data.dataset import HC18Dataset
from src.models import build_model, count_parameters
from src.training.losses import build_loss
from src.training.optim import build_optimizer


@dataclass(frozen=True)
class TrainArtifacts:
    run_dir: Path
    best_checkpoint: Path
    metrics_csv: Path
    config_json: Path


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def select_device(preferred: str = "auto", *, use_mps: bool = False) -> torch.device:
    if use_mps:
        if not torch.backends.mps.is_built():
            raise RuntimeError("MPS was requested, but this PyTorch build does not include MPS support")
        if not torch.backends.mps.is_available():
            raise RuntimeError(
                "MPS was requested, but PyTorch reports it is unavailable. "
                "Run outside the sandbox or check macOS/Metal availability."
            )
        return torch.device("mps")

    if preferred == "auto":
        if torch.cuda.is_available():
            return torch.device("cuda")
        if torch.backends.mps.is_available():
            return torch.device("mps")
        return torch.device("cpu")
    return torch.device(preferred)


def dice_score_from_logits(logits: torch.Tensor, targets: torch.Tensor, threshold: float = 0.5) -> float:
    probs = torch.sigmoid(logits)
    preds = (probs >= threshold).float()
    targets = targets.float()
    dims = tuple(range(1, preds.ndim))
    intersection = (preds * targets).sum(dim=dims)
    denominator = preds.sum(dim=dims) + targets.sum(dim=dims)
    dice = (2 * intersection + 1.0) / (denominator + 1.0)
    return float(dice.mean().detach().cpu())


def _make_loader(config: dict, split_name: str, *, shuffle: bool) -> DataLoader:
    dataset_config = config["dataset"]
    split_file = Path(config["splits"]["dir"]) / f"{split_name}.csv"
    dataset = HC18Dataset(
        dataset_config["root"],
        split_file=split_file,
        subset=dataset_config.get("subset", "training"),
        image_size=tuple(dataset_config["image_size"]),
        target_type=dataset_config.get("target_type", "filled"),
        band_width=int(dataset_config.get("band_width", 3)),
    )

    smoke_limit = int(config.get("smoke", {}).get(f"{split_name}_samples", 0))
    if smoke_limit > 0:
        dataset.records = dataset.records[:smoke_limit]

    return DataLoader(
        dataset,
        batch_size=int(config["training"]["batch_size"]),
        shuffle=shuffle,
        num_workers=int(config["training"].get("num_workers", 0)),
        pin_memory=bool(config["training"].get("pin_memory", False)),
        collate_fn=collate_segmentation_batch,
    )


def collate_segmentation_batch(batch: list[dict[str, Any]]) -> dict[str, Any]:
    """Collate tensors while preserving per-sample metadata as lists."""

    return {
        "image": torch.stack([sample["image"] for sample in batch], dim=0),
        "mask": torch.stack([sample["mask"] for sample in batch], dim=0),
        "spacing": torch.stack([sample["spacing"] for sample in batch], dim=0),
        "sample_id": [sample["sample_id"] for sample in batch],
        "image_path": [sample["image_path"] for sample in batch],
        "annotation": [sample["annotation"] for sample in batch],
    }


def _write_metrics_header(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["epoch", "train_loss", "val_loss", "val_dice"])
        writer.writeheader()


def _append_metrics(path: Path, row: dict[str, Any]) -> None:
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["epoch", "train_loss", "val_loss", "val_dice"])
        writer.writerow(row)


def _run_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
    optimizer: torch.optim.Optimizer | None,
) -> tuple[float, float]:
    is_train = optimizer is not None
    model.train(is_train)
    losses: list[float] = []
    dices: list[float] = []

    for batch in loader:
        images = batch["image"].to(device)
        masks = batch["mask"].to(device)

        with torch.set_grad_enabled(is_train):
            logits = model(images)
            loss = criterion(logits, masks)

        if is_train:
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()

        losses.append(float(loss.detach().cpu()))
        dices.append(dice_score_from_logits(logits, masks))

    return float(np.mean(losses)), float(np.mean(dices))


def train_from_config(config: dict) -> TrainArtifacts:
    seed = int(config["training"].get("seed", 42))
    set_seed(seed)
    device = select_device(
        config["training"].get("device", "auto"),
        use_mps=bool(config["training"].get("mps", False)),
    )

    run_id = str(config["run"]["id"])
    run_dir = Path(config["run"].get("output_dir", "outputs/runs")) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    model = build_model(**config["model"]).to(device)
    criterion = build_loss(**config["loss"]).to(device)
    optimizer = build_optimizer(model, config["optimizer"])
    train_loader = _make_loader(config, "train", shuffle=True)
    val_loader = _make_loader(config, "val", shuffle=False)

    config_json = run_dir / "config.json"
    with config_json.open("w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2)

    metrics_csv = run_dir / "metrics.csv"
    _write_metrics_header(metrics_csv)

    best_checkpoint = run_dir / "best_model.pt"
    best_val_dice = -1.0
    epochs = int(config["training"]["epochs"])
    print(f"Model parameters: {count_parameters(model):,}")
    print(f"Device: {device}")

    for epoch in range(1, epochs + 1):
        train_loss, _ = _run_epoch(model, train_loader, criterion, device, optimizer)
        with torch.no_grad():
            val_loss, val_dice = _run_epoch(model, val_loader, criterion, device, optimizer=None)

        row = {
            "epoch": epoch,
            "train_loss": f"{train_loss:.6f}",
            "val_loss": f"{val_loss:.6f}",
            "val_dice": f"{val_dice:.6f}",
        }
        _append_metrics(metrics_csv, row)
        print(
            f"epoch={epoch} train_loss={train_loss:.4f} "
            f"val_loss={val_loss:.4f} val_dice={val_dice:.4f}"
        )

        if val_dice > best_val_dice:
            best_val_dice = val_dice
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "model_config": config["model"],
                    "epoch": epoch,
                    "val_dice": val_dice,
                    "seed": seed,
                    "run_id": run_id,
                },
                best_checkpoint,
            )

    return TrainArtifacts(
        run_dir=run_dir,
        best_checkpoint=best_checkpoint,
        metrics_csv=metrics_csv,
        config_json=config_json,
    )
