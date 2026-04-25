"""Mask generation utilities for HC18 annotations."""

from __future__ import annotations

from dataclasses import dataclass
from math import degrees

import cv2
import numpy as np


@dataclass(frozen=True)
class EllipseAnnotation:
    """Ellipse annotation in pixel coordinates."""

    center_x: float
    center_y: float
    semi_axis_a: float
    semi_axis_b: float
    angle_rad: float = 0.0


def ellipse_to_mask(
    image_shape: tuple[int, int],
    annotation: EllipseAnnotation,
    *,
    target_type: str = "filled",
    band_width: int = 3,
) -> np.ndarray:
    """Rasterize an ellipse annotation into a binary mask.

    Args:
        image_shape: `(height, width)` of the output mask.
        annotation: Ellipse parameters in pixel coordinates.
        target_type: `filled` or `boundary`.
        band_width: Boundary thickness in pixels for `boundary` targets.

    Returns:
        A `uint8` binary mask with values 0 or 1.
    """

    if target_type not in {"filled", "boundary"}:
        raise ValueError(f"Unsupported target_type: {target_type}")
    if band_width < 1:
        raise ValueError("band_width must be >= 1")

    height, width = image_shape
    mask = np.zeros((height, width), dtype=np.uint8)
    center = (round(annotation.center_x), round(annotation.center_y))
    axes = (round(annotation.semi_axis_a), round(annotation.semi_axis_b))
    if axes[0] <= 0 or axes[1] <= 0:
        raise ValueError(f"Ellipse axes must be positive, got {axes}")

    thickness = -1 if target_type == "filled" else int(band_width)
    cv2.ellipse(
        mask,
        center=center,
        axes=axes,
        angle=degrees(annotation.angle_rad),
        startAngle=0,
        endAngle=360,
        color=1,
        thickness=thickness,
    )
    return mask


def annotation_image_to_mask(
    annotation_image: np.ndarray,
    *,
    target_type: str = "filled",
    band_width: int = 3,
    threshold: int = 0,
) -> np.ndarray:
    """Convert an HC18 annotation image into a binary mask.

    HC18 annotation PNGs encode an ellipse contour. For the default filled-mask
    supervision, fill the contour deterministically. For boundary supervision,
    optionally thicken the contour to `band_width`.
    """

    if target_type not in {"filled", "boundary"}:
        raise ValueError(f"Unsupported target_type: {target_type}")

    if annotation_image.ndim == 3:
        gray = cv2.cvtColor(annotation_image, cv2.COLOR_BGR2GRAY)
    elif annotation_image.ndim == 2:
        gray = annotation_image
    else:
        raise ValueError(f"Unsupported annotation image shape: {annotation_image.shape}")

    boundary = (gray > threshold).astype(np.uint8)
    if target_type == "boundary":
        if band_width <= 1:
            return boundary
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (band_width, band_width))
        return (cv2.dilate(boundary, kernel, iterations=1) > 0).astype(np.uint8)

    contours, _ = cv2.findContours(boundary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled = np.zeros_like(boundary, dtype=np.uint8)
    if contours:
        cv2.drawContours(filled, contours, contourIdx=-1, color=1, thickness=-1)
    return filled
