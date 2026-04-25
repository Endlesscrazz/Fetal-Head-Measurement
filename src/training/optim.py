"""Optimizer and scheduler builders."""

from __future__ import annotations

from torch import nn
from torch.optim import Adam, AdamW, Optimizer, SGD


def build_optimizer(model: nn.Module, config: dict) -> Optimizer:
    """Build optimizer from config."""

    name = config.get("name", "adamw").lower()
    lr = float(config.get("lr", 1e-3))
    weight_decay = float(config.get("weight_decay", 0.0))

    if name == "adam":
        return Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    if name == "adamw":
        return AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    if name == "sgd":
        momentum = float(config.get("momentum", 0.9))
        return SGD(model.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay)
    raise ValueError(f"Unknown optimizer: {name}")
