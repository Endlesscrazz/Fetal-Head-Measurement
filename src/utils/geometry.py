"""Deterministic mask-to-ellipse geometry utilities."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import cos, pi, radians, sin, sqrt

import cv2
import numpy as np


@dataclass(frozen=True)
class FittedEllipse:
    """Ellipse fitted in pixel coordinates.

    OpenCV reports full axis lengths. This project stores semi-axis lengths so
    circumference formulas and report text stay unambiguous.
    """

    center_x: float
    center_y: float
    semi_axis_a: float
    semi_axis_b: float
    angle_deg: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def threshold_probability(probability: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """Threshold a probability map into a binary uint8 mask."""

    return (probability >= threshold).astype(np.uint8)


def largest_connected_component(mask: np.ndarray) -> np.ndarray:
    """Keep only the largest foreground connected component."""

    binary = (mask > 0).astype(np.uint8)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
    if num_labels <= 1:
        return binary

    foreground_labels = range(1, num_labels)
    largest_label = max(foreground_labels, key=lambda label: stats[label, cv2.CC_STAT_AREA])
    return (labels == largest_label).astype(np.uint8)


def extract_largest_contour(mask: np.ndarray) -> np.ndarray:
    """Extract the largest external contour as an `[N, 2]` array."""

    binary = (mask > 0).astype(np.uint8)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        raise ValueError("Cannot extract contour from an empty mask")

    contour = max(contours, key=cv2.contourArea)
    points = contour.reshape(-1, 2).astype(np.float32)
    if len(points) < 5:
        raise ValueError("At least 5 contour points are required to fit an ellipse")
    return points


def fit_ellipse_to_contour(contour_points: np.ndarray) -> FittedEllipse:
    """Fit an ellipse to contour points with OpenCV."""

    if len(contour_points) < 5:
        raise ValueError("At least 5 contour points are required to fit an ellipse")

    (center_x, center_y), (axis_1, axis_2), angle_deg = cv2.fitEllipse(
        contour_points.reshape(-1, 1, 2).astype(np.float32)
    )
    semi_a = float(max(axis_1, axis_2) / 2.0)
    semi_b = float(min(axis_1, axis_2) / 2.0)
    if semi_a <= 0 or semi_b <= 0:
        raise ValueError("Fitted ellipse axes must be positive")
    return FittedEllipse(
        center_x=float(center_x),
        center_y=float(center_y),
        semi_axis_a=semi_a,
        semi_axis_b=semi_b,
        angle_deg=float(angle_deg),
    )


def fit_ellipse_from_mask(mask: np.ndarray) -> FittedEllipse:
    """Fit an ellipse to the largest connected component of a mask."""

    cleaned = largest_connected_component(mask)
    contour = extract_largest_contour(cleaned)
    return fit_ellipse_to_contour(contour)


def ellipse_circumference_pixels(ellipse: FittedEllipse) -> float:
    """Approximate ellipse circumference in pixels with Ramanujan's formula."""

    a = ellipse.semi_axis_a
    b = ellipse.semi_axis_b
    return float(pi * (3 * (a + b) - sqrt((3 * a + b) * (a + 3 * b))))


def ellipse_points(ellipse: FittedEllipse, num_points: int = 720) -> np.ndarray:
    """Sample points on the fitted ellipse in pixel coordinates."""

    theta = np.linspace(0, 2 * pi, num_points, endpoint=False)
    angle = radians(ellipse.angle_deg)
    cos_angle = cos(angle)
    sin_angle = sin(angle)
    x = ellipse.semi_axis_a * np.cos(theta)
    y = ellipse.semi_axis_b * np.sin(theta)
    rotated_x = ellipse.center_x + x * cos_angle - y * sin_angle
    rotated_y = ellipse.center_y + x * sin_angle + y * cos_angle
    return np.stack([rotated_x, rotated_y], axis=1).astype(np.float32)


def polyline_length(points: np.ndarray) -> float:
    """Compute closed-polyline length."""

    if len(points) < 2:
        return 0.0
    closed = np.vstack([points, points[0]])
    deltas = np.diff(closed, axis=0)
    return float(np.linalg.norm(deltas, axis=1).sum())


def ellipse_circumference_mm(
    ellipse: FittedEllipse,
    spacing_mm: tuple[float, float],
    *,
    num_points: int = 720,
) -> float:
    """Compute ellipse circumference after scaling sampled points to mm."""

    sx, sy = spacing_mm
    points = ellipse_points(ellipse, num_points=num_points)
    points_mm = points.copy()
    points_mm[:, 0] *= float(sx)
    points_mm[:, 1] *= float(sy)
    return polyline_length(points_mm)


def mask_to_measurement(
    mask: np.ndarray,
    spacing_mm: tuple[float, float],
) -> dict[str, object]:
    """Convert a binary mask into cleaned mask, ellipse, and HC measurements."""

    cleaned = largest_connected_component(mask)
    ellipse = fit_ellipse_from_mask(cleaned)
    return {
        "cleaned_mask": cleaned,
        "ellipse": ellipse,
        "hc_pixels": ellipse_circumference_pixels(ellipse),
        "hc_mm": ellipse_circumference_mm(ellipse, spacing_mm),
    }
