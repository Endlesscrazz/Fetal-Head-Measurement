from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_demo_manifest import REQUIRED_SAFETY_TEXT, validate_manifest


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_validate_manifest_accepts_minimal_bundle(tmp_path: Path) -> None:
    sample_dir = tmp_path / "outputs" / "demo_samples" / "001_HC"
    for filename in [
        "ultrasound.png",
        "target.png",
        "pred.png",
        "prob.png",
    ]:
        (sample_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        (sample_dir / filename).write_bytes(b"placeholder")

    metadata_path = sample_dir / "metadata.json"
    _write_json(
        metadata_path,
        {
            "sample_id": "001_HC",
            "run_id": "attention_unet_local_baseline",
            "split": "test",
            "cat": "strong",
            "threshold": 0.5,
            "spacing_x_mm": 0.1,
            "spacing_y_mm": 0.1,
            "spacingXMm": 0.1,
            "spacingYMm": 0.1,
            "metrics": {
                "dice": 0.95,
                "iou": 0.9,
                "hd95_mm": 1.2,
                "hcErr": 1.0,
                "predHC": 100.0,
                "targetHC": 101.0,
            },
            "predEllipse": {
                "cx": 10.0,
                "cy": 12.0,
                "rx": 5.0,
                "ry": 4.0,
                "rot": 0.35,
            },
            "contourHC": 110.0,
            "confidence": 0.91,
            "notes": "Synthetic validation fixture.",
        },
    )
    failure_dir = tmp_path / "outputs" / "demo_samples" / "002_HC"
    for filename in [
        "ultrasound.png",
        "target.png",
        "pred.png",
        "prob.png",
    ]:
        (failure_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        (failure_dir / filename).write_bytes(b"placeholder")
    _write_json(
        failure_dir / "metadata.json",
        {
            "sample_id": "002_HC",
            "run_id": "attention_unet_local_baseline",
            "split": "test",
            "cat": "failure",
            "threshold": 0.5,
            "spacing_x_mm": 0.1,
            "spacing_y_mm": 0.1,
            "spacingXMm": 0.1,
            "spacingYMm": 0.1,
            "metrics": {
                "dice": 0.85,
                "iou": 0.75,
                "hd95_mm": 5.2,
                "hcErr": 8.0,
                "predHC": 108.0,
                "targetHC": 100.0,
            },
            "predEllipse": {"cx": 10.0, "cy": 12.0, "rx": 5.0, "ry": 4.0, "rot": 0.35},
            "contourHC": 110.0,
            "confidence": 0.91,
            "notes": "Synthetic validation fixture.",
        },
    )
    manifest = {
        "schema_version": 2,
        "safety_text": REQUIRED_SAFETY_TEXT,
        "samples": [
            {
                "id": "001_HC",
                "label": "Strong synthetic",
                "split": "test",
                "cat": "strong",
                "summary": "Synthetic success.",
                "metrics": {
                    "dice": 0.95,
                    "iou": 0.9,
                    "hd95_mm": 1.2,
                    "hcErr": 1.0,
                    "predHC": 100.0,
                    "targetHC": 101.0,
                },
                "predEllipse": {
                    "cx": 10.0,
                    "cy": 12.0,
                    "rx": 5.0,
                    "ry": 4.0,
                    "rot": 0.35,
                },
                "contourHC": 110.0,
                "confidence": 0.91,
                "spacingXMm": 0.1,
                "spacingYMm": 0.1,
                "resolution": {"w": 384, "h": 256},
            },
            {
                "id": "002_HC",
                "label": "Failure synthetic",
                "split": "test",
                "cat": "failure",
                "summary": "Synthetic failure.",
                "metrics": {
                    "dice": 0.85,
                    "iou": 0.75,
                    "hd95_mm": 5.2,
                    "hcErr": 8.0,
                    "predHC": 108.0,
                    "targetHC": 100.0,
                },
                "predEllipse": {
                    "cx": 10.0,
                    "cy": 12.0,
                    "rx": 5.0,
                    "ry": 4.0,
                    "rot": 0.35,
                },
                "contourHC": 110.0,
                "confidence": 0.91,
                "spacingXMm": 0.1,
                "spacingYMm": 0.1,
                "resolution": {"w": 384, "h": 256},
            },
        ],
    }

    assert validate_manifest(manifest, repo_root=tmp_path) == []


def test_validate_manifest_reports_missing_contour_hc(tmp_path: Path) -> None:
    sample_dir = tmp_path / "outputs" / "demo_samples" / "001_HC"
    for filename in [
        "ultrasound.png",
        "target.png",
        "pred.png",
        "prob.png",
    ]:
        (sample_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        (sample_dir / filename).write_bytes(b"placeholder")

    metadata_path = sample_dir / "metadata.json"
    _write_json(
        metadata_path,
        {
            "sample_id": "001_HC",
            "run_id": "attention_unet_local_baseline",
            "split": "test",
            "cat": "strong",
            "threshold": 0.5,
            "spacing_x_mm": 0.1,
            "spacing_y_mm": 0.1,
            "spacingXMm": 0.1,
            "spacingYMm": 0.1,
            "metrics": {
                "dice": 0.95,
                "iou": 0.9,
                "hd95_mm": 1.2,
                "hcErr": 1.0,
                "predHC": 100.0,
                "targetHC": 101.0,
            },
            "predEllipse": {"cx": 10.0, "cy": 12.0, "rx": 5.0, "ry": 4.0, "rot": 0.35},
            "contourHC": 110.0,
            "confidence": 0.91,
            "notes": "Synthetic validation fixture.",
        },
    )
    manifest = {
        "schema_version": 2,
        "safety_text": REQUIRED_SAFETY_TEXT,
        "samples": [
            {
                "id": "001_HC",
                "label": "Strong synthetic",
                "split": "test",
                "cat": "strong",
                "summary": "Synthetic success.",
                "metrics": {
                    "dice": 0.95,
                    "iou": 0.9,
                    "hd95_mm": 1.2,
                    "hcErr": 1.0,
                    "predHC": 100.0,
                    "targetHC": 101.0,
                },
                "predEllipse": {"cx": 10.0, "cy": 12.0, "rx": 5.0, "ry": 4.0, "rot": 0.35},
                "confidence": 0.91,
                "spacingXMm": 0.1,
                "spacingYMm": 0.1,
                "resolution": {"w": 384, "h": 256},
            },
            {
                "id": "001_HC",
                "label": "Failure synthetic",
                "split": "test",
                "cat": "failure",
                "summary": "Synthetic failure.",
                "metrics": {
                    "dice": 0.85,
                    "iou": 0.75,
                    "hd95_mm": 5.2,
                    "hcErr": 8.0,
                    "predHC": 108.0,
                    "targetHC": 100.0,
                },
                "predEllipse": {"cx": 10.0, "cy": 12.0, "rx": 5.0, "ry": 4.0, "rot": 0.35},
                "contourHC": 110.0,
                "confidence": 0.91,
                "spacingXMm": 0.1,
                "spacingYMm": 0.1,
                "resolution": {"w": 384, "h": 256},
            },
        ],
    }

    errors = validate_manifest(manifest, repo_root=tmp_path)

    assert any("contourHC" in error for error in errors)
