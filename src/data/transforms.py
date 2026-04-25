"""Geometry-safe preprocessing helpers."""

from __future__ import annotations

import cv2
import numpy as np


def normalize_image(image: np.ndarray) -> np.ndarray:
    """Normalize a grayscale image to zero mean and unit variance."""

    image = image.astype(np.float32)
    nonzero = image[image > 0]
    values = nonzero if nonzero.size else image.reshape(-1)
    mean = float(values.mean())
    std = float(values.std())
    if std < 1e-6:
        std = 1.0
    return (image - mean) / std


def resize_image(image: np.ndarray, output_size: tuple[int, int]) -> np.ndarray:
    """Resize an image to `(height, width)` with bilinear interpolation."""

    height, width = output_size
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)


def resize_mask(mask: np.ndarray, output_size: tuple[int, int]) -> np.ndarray:
    """Resize a binary mask to `(height, width)` with nearest interpolation."""

    height, width = output_size
    resized = cv2.resize(mask.astype(np.uint8), (width, height), interpolation=cv2.INTER_NEAREST)
    return (resized > 0).astype(np.uint8)


def update_spacing_for_resize(
    spacing_mm: tuple[float, float],
    original_size: tuple[int, int],
    output_size: tuple[int, int],
) -> tuple[float, float]:
    """Update `(sx, sy)` spacing after resizing from `(H, W)` to `(H2, W2)`."""

    sx, sy = spacing_mm
    original_h, original_w = original_size
    output_h, output_w = output_size
    return sx * (original_w / output_w), sy * (original_h / output_h)
