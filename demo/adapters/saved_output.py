"""Saved-output adapter for v2 demo artifacts."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from demo.types import DemoManifest, DemoSample, DemoSampleEntry


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _resolve_path(repo_root: Path, path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return repo_root / path


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _load_grayscale(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return image.astype(np.uint8)


def _load_binary_mask(path: Path) -> np.ndarray:
    return (_load_grayscale(path) > 0).astype(np.uint8)


def _load_rgb(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Could not read RGB image: {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.uint8)


def load_manifest(path: str | Path = "outputs/demo_samples/manifest.json") -> DemoManifest:
    """Load a saved-output manifest without loading sample image arrays."""

    manifest_path = _resolve_path(PROJECT_ROOT, str(path))
    payload = _load_json(manifest_path)
    samples = []
    for sample in payload.get("samples", []):
        samples.append(
            DemoSampleEntry(
                sample_id=str(sample["id"]),
                label=str(sample["label"]),
                split=str(sample["split"]),
                category=str(sample["category"]),
                image_path=_resolve_path(PROJECT_ROOT, str(sample["image_path"])),
                target_mask_path=_resolve_path(PROJECT_ROOT, str(sample["target_mask_path"])),
                raw_mask_path=_resolve_path(PROJECT_ROOT, str(sample["raw_mask_path"])),
                cleaned_mask_path=_resolve_path(PROJECT_ROOT, str(sample["cleaned_mask_path"])),
                ellipse_overlay_path=_resolve_path(PROJECT_ROOT, str(sample["ellipse_overlay_path"])),
                metadata_path=_resolve_path(PROJECT_ROOT, str(sample["metadata_path"])),
            )
        )

    return DemoManifest(
        path=manifest_path,
        repo_root=PROJECT_ROOT,
        schema_version=int(payload.get("schema_version", 0)),
        safety_text=str(payload.get("safety_text", "")),
        samples=tuple(samples),
        created_from_run_id=payload.get("created_from_run_id"),
        created_from_split=payload.get("created_from_split"),
    )


def load_sample(manifest: DemoManifest, sample_id: str) -> DemoSample:
    """Load one saved-output sample into the app-facing `DemoSample` contract."""

    entry = manifest.get_entry(sample_id)
    metadata = _load_json(entry.metadata_path)
    ellipse_params = metadata.get("ellipse_params")
    if isinstance(ellipse_params, dict):
        ellipse_params = {
            str(key): float(value)
            for key, value in ellipse_params.items()
            if _optional_float(value) is not None
        }
    else:
        ellipse_params = None

    return DemoSample(
        sample_id=entry.sample_id,
        label=str(metadata.get("label", entry.label)),
        split=str(metadata.get("split", entry.split)),
        category=str(metadata.get("category", entry.category)),
        tags=tuple(str(tag) for tag in metadata.get("tags", [])),
        reason=metadata.get("reason"),
        image=_load_grayscale(entry.image_path),
        target_mask=_load_binary_mask(entry.target_mask_path) if entry.target_mask_path.exists() else None,
        raw_mask=_load_binary_mask(entry.raw_mask_path),
        cleaned_mask=_load_binary_mask(entry.cleaned_mask_path),
        ellipse_overlay=_load_rgb(entry.ellipse_overlay_path),
        spacing_x_mm=float(metadata["spacing_x_mm"]),
        spacing_y_mm=float(metadata["spacing_y_mm"]),
        threshold=float(metadata["threshold"]),
        hc_pred_mm=_optional_float(metadata.get("hc_pred_mm")),
        hc_gt_mm=_optional_float(metadata.get("hc_gt_mm")),
        dice=_optional_float(metadata.get("dice")),
        iou=_optional_float(metadata.get("iou")),
        hd95_mm=_optional_float(metadata.get("hd95_mm")),
        abs_hc_error_mm=_optional_float(metadata.get("abs_hc_error_mm")),
        signed_hc_error_mm=_optional_float(metadata.get("signed_hc_error_mm")),
        ellipse_params=ellipse_params,
        contour_hc_mm=_optional_float(metadata.get("contour_hc_mm")),
        notes=metadata.get("notes"),
    )


def load_samples(manifest: DemoManifest) -> list[DemoSample]:
    """Load every sample referenced by a manifest."""

    return [load_sample(manifest, sample_id) for sample_id in manifest.sample_ids()]
