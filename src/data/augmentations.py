"""Training-only image/mask augmentation helpers."""

from __future__ import annotations

import numpy as np


def apply_training_augmentation(
    image: np.ndarray,
    mask: np.ndarray,
    config: dict,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply paired spatial augmentation and image-only intensity augmentation."""

    augmented_image = image.copy()
    augmented_mask = mask.copy()

    hflip_prob = float(config.get("hflip_prob", 0.0))
    if hflip_prob > 0 and np.random.random() < hflip_prob:
        augmented_image = np.ascontiguousarray(np.fliplr(augmented_image))
        augmented_mask = np.ascontiguousarray(np.fliplr(augmented_mask))

    scale_range = config.get("intensity_scale_range")
    if scale_range is not None:
        scale_min, scale_max = float(scale_range[0]), float(scale_range[1])
        scale = np.random.uniform(scale_min, scale_max)
        augmented_image = augmented_image.astype(np.float32) * scale

    shift_range = config.get("intensity_shift_range")
    if shift_range is not None:
        shift_min, shift_max = float(shift_range[0]), float(shift_range[1])
        shift = np.random.uniform(shift_min, shift_max)
        augmented_image = augmented_image.astype(np.float32) + shift

    noise_std = float(config.get("gaussian_noise_std", 0.0))
    if noise_std > 0:
        noise = np.random.normal(loc=0.0, scale=noise_std, size=augmented_image.shape)
        augmented_image = augmented_image.astype(np.float32) + noise.astype(np.float32)

    augmented_image = np.clip(augmented_image, 0, 255).astype(image.dtype)
    return augmented_image, augmented_mask.astype(mask.dtype)
