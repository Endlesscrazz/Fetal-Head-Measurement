import math

import numpy as np
import pytest

from src.data.masks import EllipseAnnotation, ellipse_to_mask
from src.utils.geometry import (
    ellipse_circumference_mm,
    ellipse_circumference_pixels,
    fit_ellipse_from_mask,
    largest_connected_component,
    mask_to_measurement,
    threshold_probability,
)


def test_threshold_probability_returns_binary_mask():
    probability = np.array([[0.2, 0.7], [0.5, 0.1]], dtype=np.float32)

    mask = threshold_probability(probability, threshold=0.5)

    assert mask.dtype == np.uint8
    assert mask.tolist() == [[0, 1], [1, 0]]


def test_largest_connected_component_removes_small_region():
    mask = np.zeros((16, 16), dtype=np.uint8)
    mask[1:3, 1:3] = 1
    mask[8:14, 8:14] = 1

    cleaned = largest_connected_component(mask)

    assert cleaned.sum() == 36


def test_fit_ellipse_from_mask_recovers_reasonable_axes():
    mask = ellipse_to_mask(
        (128, 128),
        EllipseAnnotation(center_x=64, center_y=60, semi_axis_a=30, semi_axis_b=18),
    )

    ellipse = fit_ellipse_from_mask(mask)

    assert ellipse.center_x == pytest.approx(64, abs=2)
    assert ellipse.center_y == pytest.approx(60, abs=2)
    assert ellipse.semi_axis_a == pytest.approx(30, abs=3)
    assert ellipse.semi_axis_b == pytest.approx(18, abs=3)


def test_circumference_mm_matches_pixel_formula_for_isotropic_spacing():
    mask = ellipse_to_mask(
        (128, 128),
        EllipseAnnotation(center_x=64, center_y=64, semi_axis_a=24, semi_axis_b=12),
    )
    ellipse = fit_ellipse_from_mask(mask)

    pixels = ellipse_circumference_pixels(ellipse)
    mm = ellipse_circumference_mm(ellipse, (0.5, 0.5))

    assert mm == pytest.approx(pixels * 0.5, rel=0.02)


def test_mask_to_measurement_fails_on_empty_mask():
    with pytest.raises(ValueError):
        mask_to_measurement(np.zeros((32, 32), dtype=np.uint8), (1.0, 1.0))
