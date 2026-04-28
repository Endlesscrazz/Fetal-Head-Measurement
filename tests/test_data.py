from pathlib import Path

import cv2
import numpy as np

from src.data.augmentations import apply_training_augmentation
from src.data.dataset import HC18Dataset, discover_hc18_records
from src.data.masks import EllipseAnnotation, annotation_image_to_mask, ellipse_to_mask
from src.data.transforms import update_spacing_for_resize


def test_ellipse_to_mask_has_foreground():
    mask = ellipse_to_mask(
        (64, 64),
        EllipseAnnotation(center_x=32, center_y=30, semi_axis_a=12, semi_axis_b=8),
    )

    assert mask.shape == (64, 64)
    assert mask.dtype == np.uint8
    assert mask.sum() > 0


def test_update_spacing_for_resize():
    sx, sy = update_spacing_for_resize((0.5, 0.25), (100, 200), (50, 100))

    assert sx == 1.0
    assert sy == 0.5


def test_annotation_image_to_mask_fills_contour():
    boundary = ellipse_to_mask(
        (64, 64),
        EllipseAnnotation(center_x=32, center_y=32, semi_axis_a=15, semi_axis_b=10),
        target_type="boundary",
    )

    filled = annotation_image_to_mask(boundary * 255, target_type="filled")

    assert filled.sum() > boundary.sum()


def test_hc18_dataset_reads_synthetic_annotation(tmp_path: Path):
    training_dir = tmp_path / "training_set"
    training_dir.mkdir()
    image_path = training_dir / "001_HC.png"
    annotation_path = training_dir / "001_HC_Annotation.png"
    csv_path = tmp_path / "training_set_pixel_size_and_HC.csv"

    image = np.full((64, 64), 100, dtype=np.uint8)
    annotation = ellipse_to_mask(
        (64, 64),
        EllipseAnnotation(center_x=32, center_y=32, semi_axis_a=15, semi_axis_b=10),
    )
    cv2.imwrite(str(image_path), image)
    cv2.imwrite(str(annotation_path), annotation * 255)
    csv_path.write_text(
        "filename,pixel size(mm),head circumference (mm)\n"
        "001_HC.png,0.5,120.0\n",
        encoding="utf-8",
    )

    records = discover_hc18_records(tmp_path, subset="training")
    assert len(records) == 1
    assert records[0].annotation_path == annotation_path
    assert records[0].spacing_mm == (0.5, 0.5)

    dataset = HC18Dataset(tmp_path, image_size=(32, 32))
    sample = dataset[0]

    assert sample["image"].shape == (1, 32, 32)
    assert sample["mask"].shape == (1, 32, 32)
    assert sample["mask"].sum() > 0
    assert tuple(sample["spacing"].tolist()) == (1.0, 1.0)
    assert sample["sample_id"] == "001_HC"


def test_training_augmentation_flips_image_and_mask_together():
    image = np.arange(6, dtype=np.uint8).reshape(2, 3)
    mask = np.array([[0, 1, 1], [1, 0, 0]], dtype=np.uint8)

    augmented_image, augmented_mask = apply_training_augmentation(
        image,
        mask,
        {"hflip_prob": 1.0},
    )

    np.testing.assert_array_equal(augmented_image, np.fliplr(image))
    np.testing.assert_array_equal(augmented_mask, np.fliplr(mask))
