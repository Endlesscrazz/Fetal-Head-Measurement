"""Segmentation model registry."""

from __future__ import annotations

from torch import nn

from src.models.unet import UNet, count_parameters


MODEL_REGISTRY = {
    "unet": UNet,
}


def build_model(name: str, **kwargs) -> nn.Module:
    """Build a segmentation model by registry name."""

    key = name.lower()
    if key not in MODEL_REGISTRY:
        available = ", ".join(sorted(MODEL_REGISTRY))
        raise ValueError(f"Unknown model '{name}'. Available models: {available}")
    return MODEL_REGISTRY[key](**kwargs)


__all__ = ["MODEL_REGISTRY", "UNet", "build_model", "count_parameters"]
