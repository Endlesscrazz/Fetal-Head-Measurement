from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np

from demo.adapters.saved_output import load_manifest, load_sample, load_samples


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_gray(path: Path, value: int = 64) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = np.full((4, 5), value, dtype=np.uint8)
    cv2.imwrite(str(path), image)


def _write_mask(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mask = np.zeros((4, 5), dtype=np.uint8)
    mask[1:3, 2:4] = 255
    cv2.imwrite(str(path), mask)


def _write_overlay(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = np.zeros((4, 5, 3), dtype=np.uint8)
    image[:, :, 2] = 255
    cv2.imwrite(str(path), image)


def _make_bundle(tmp_path: Path) -> Path:
    sample_dir = tmp_path / "outputs" / "demo_samples" / "001_HC"
    _write_gray(sample_dir / "image.png")
    _write_mask(sample_dir / "target_mask.png")
    _write_mask(sample_dir / "raw_mask.png")
    _write_mask(sample_dir / "cleaned_mask.png")
    _write_overlay(sample_dir / "ellipse_overlay.png")
    _write_json(
        sample_dir / "metadata.json",
        {
            "sample_id": "001_HC",
            "run_id": "attention_unet_local_baseline",
            "split": "test",
            "category": "strong",
            "label": "Strong fixture",
            "tags": ["strong"],
            "reason": "Fixture sample.",
            "threshold": 0.5,
            "spacing_x_mm": 0.1,
            "spacing_y_mm": 0.2,
            "hc_pred_mm": 100.0,
            "hc_gt_mm": 101.0,
            "dice": 0.95,
            "iou": 0.9,
            "hd95_mm": 1.2,
            "abs_hc_error_mm": 1.0,
            "signed_hc_error_mm": -1.0,
            "ellipse_params": {
                "center_x": 10.0,
                "center_y": 12.0,
                "semi_axis_a": 5.0,
                "semi_axis_b": 4.0,
                "angle_deg": 20.0,
            },
            "contour_hc_mm": 110.0,
            "notes": "Fixture notes.",
        },
    )
    manifest_path = tmp_path / "outputs" / "demo_samples" / "manifest.json"
    _write_json(
        manifest_path,
        {
            "schema_version": 1,
            "created_from_run_id": "attention_unet_local_baseline",
            "created_from_split": "test",
            "safety_text": "Educational demo only. Not for clinical use.",
            "samples": [
                {
                    "id": "001_HC",
                    "label": "Strong fixture",
                    "split": "test",
                    "category": "strong",
                    "image_path": str(sample_dir / "image.png"),
                    "target_mask_path": str(sample_dir / "target_mask.png"),
                    "raw_mask_path": str(sample_dir / "raw_mask.png"),
                    "cleaned_mask_path": str(sample_dir / "cleaned_mask.png"),
                    "ellipse_overlay_path": str(sample_dir / "ellipse_overlay.png"),
                    "metadata_path": str(sample_dir / "metadata.json"),
                }
            ],
        },
    )
    return manifest_path


def test_load_manifest_reads_entries_without_loading_arrays(tmp_path: Path) -> None:
    manifest = load_manifest(_make_bundle(tmp_path))

    assert manifest.safety_text == "Educational demo only. Not for clinical use."
    assert manifest.sample_ids() == ["001_HC"]
    assert manifest.get_entry("001_HC").label == "Strong fixture"


def test_load_sample_returns_demo_sample_with_binary_masks_and_rgb_overlay(tmp_path: Path) -> None:
    manifest = load_manifest(_make_bundle(tmp_path))
    sample = load_sample(manifest, "001_HC")

    assert sample.sample_id == "001_HC"
    assert sample.label == "Strong fixture"
    assert sample.image.shape == (4, 5)
    assert sample.target_mask is not None
    assert set(np.unique(sample.target_mask)) == {0, 1}
    assert set(np.unique(sample.raw_mask)) == {0, 1}
    assert set(np.unique(sample.cleaned_mask)) == {0, 1}
    assert sample.ellipse_overlay.shape == (4, 5, 3)
    assert sample.ellipse_overlay[0, 0].tolist() == [255, 0, 0]
    assert sample.spacing_x_mm == 0.1
    assert sample.spacing_y_mm == 0.2
    assert sample.hc_pred_mm == 100.0
    assert sample.contour_hc_mm == 110.0
    assert sample.ellipse_params == {
        "center_x": 10.0,
        "center_y": 12.0,
        "semi_axis_a": 5.0,
        "semi_axis_b": 4.0,
        "angle_deg": 20.0,
    }


def test_load_samples_loads_all_manifest_entries(tmp_path: Path) -> None:
    manifest = load_manifest(_make_bundle(tmp_path))

    assert [sample.sample_id for sample in load_samples(manifest)] == ["001_HC"]
