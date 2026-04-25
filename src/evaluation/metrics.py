"""Segmentation and measurement metrics."""

from __future__ import annotations

import math

import cv2
import numpy as np
from scipy.spatial.distance import cdist


def dice_score(pred_mask: np.ndarray, target_mask: np.ndarray, smooth: float = 1.0) -> float:
    pred = (pred_mask > 0).astype(np.uint8)
    target = (target_mask > 0).astype(np.uint8)
    intersection = float((pred * target).sum())
    denominator = float(pred.sum() + target.sum())
    return (2 * intersection + smooth) / (denominator + smooth)


def iou_score(pred_mask: np.ndarray, target_mask: np.ndarray, smooth: float = 1.0) -> float:
    pred = (pred_mask > 0).astype(np.uint8)
    target = (target_mask > 0).astype(np.uint8)
    intersection = float((pred * target).sum())
    union = float(((pred + target) > 0).sum())
    return (intersection + smooth) / (union + smooth)


def surface_points(mask: np.ndarray) -> np.ndarray:
    binary = (mask > 0).astype(np.uint8)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return np.empty((0, 2), dtype=np.float32)
    return np.vstack([contour.reshape(-1, 2) for contour in contours]).astype(np.float32)


def hd95(pred_mask: np.ndarray, target_mask: np.ndarray, spacing_mm: tuple[float, float] = (1.0, 1.0)) -> float:
    """Compute symmetric 95th percentile Hausdorff distance in mm."""

    pred_points = surface_points(pred_mask)
    target_points = surface_points(target_mask)
    if len(pred_points) == 0 and len(target_points) == 0:
        return 0.0
    if len(pred_points) == 0 or len(target_points) == 0:
        return math.inf

    sx, sy = spacing_mm
    pred_mm = pred_points.copy()
    target_mm = target_points.copy()
    pred_mm[:, 0] *= sx
    pred_mm[:, 1] *= sy
    target_mm[:, 0] *= sx
    target_mm[:, 1] *= sy

    distances = cdist(pred_mm, target_mm)
    pred_to_target = distances.min(axis=1)
    target_to_pred = distances.min(axis=0)
    return float(np.percentile(np.concatenate([pred_to_target, target_to_pred]), 95))


def signed_error(prediction: float, target: float) -> float:
    return float(prediction - target)


def absolute_error(prediction: float, target: float) -> float:
    return abs(signed_error(prediction, target))


def rmse(errors: np.ndarray) -> float:
    finite = errors[np.isfinite(errors)]
    if len(finite) == 0:
        return math.nan
    return float(np.sqrt(np.mean(finite**2)))
