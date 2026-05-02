"""Shared app-facing types for the v2 demo."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class DemoSampleEntry:
    """Manifest entry for one saved-output demo sample."""

    sample_id: str
    label: str
    split: str
    category: str
    image_path: Path
    target_mask_path: Path
    raw_mask_path: Path
    cleaned_mask_path: Path
    ellipse_overlay_path: Path
    metadata_path: Path


@dataclass(frozen=True)
class DemoManifest:
    """Parsed saved-output manifest with paths resolved for loading."""

    path: Path
    repo_root: Path
    schema_version: int
    safety_text: str
    samples: tuple[DemoSampleEntry, ...]
    created_from_run_id: str | None = None
    created_from_split: str | None = None

    def sample_ids(self) -> list[str]:
        return [sample.sample_id for sample in self.samples]

    def get_entry(self, sample_id: str) -> DemoSampleEntry:
        for sample in self.samples:
            if sample.sample_id == sample_id:
                return sample
        raise KeyError(f"Unknown demo sample id: {sample_id}")


@dataclass(frozen=True)
class DemoSample:
    """App-facing sample object shared by saved-output and live modes."""

    sample_id: str
    label: str
    split: str
    image: np.ndarray
    target_mask: np.ndarray | None
    raw_mask: np.ndarray
    cleaned_mask: np.ndarray
    ellipse_overlay: np.ndarray
    spacing_x_mm: float
    spacing_y_mm: float
    threshold: float
    hc_pred_mm: float | None
    hc_gt_mm: float | None
    dice: float | None
    iou: float | None
    hd95_mm: float | None
    abs_hc_error_mm: float | None
    ellipse_params: dict[str, float] | None
    contour_hc_mm: float | None
    notes: str | None
    category: str | None = None
    tags: tuple[str, ...] = ()
    reason: str | None = None
    signed_hc_error_mm: float | None = None
