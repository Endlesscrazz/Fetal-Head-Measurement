"""HC18 dataset parser and target generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

from src.data.augmentations import apply_training_augmentation
from src.data.masks import EllipseAnnotation, annotation_image_to_mask, ellipse_to_mask
from src.data.transforms import normalize_image, resize_image, resize_mask, update_spacing_for_resize


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}
ANNOTATION_TOKENS = ("annotation", "mask", "label")


@dataclass(frozen=True)
class HC18Record:
    """Metadata for one HC18 image."""

    sample_id: str
    image_path: Path
    annotation_path: Path | None
    spacing_mm: tuple[float, float]
    hc_mm: float | None = None
    ellipse: EllipseAnnotation | None = None


def sample_id_from_filename(filename: str) -> str:
    return Path(filename).stem


def group_id_from_sample_id(sample_id: str) -> str:
    return sample_id.split("_", 1)[0]


def is_annotation_file(path: Path) -> bool:
    stem = path.stem.lower()
    return any(token in stem for token in ANNOTATION_TOKENS)


def find_image_files(root: Path) -> list[Path]:
    """Find ultrasound image files, excluding likely annotation/mask images."""

    if not root.exists():
        return []
    paths = [p for p in root.rglob("*") if p.suffix.lower() in IMAGE_SUFFIXES]
    return sorted(p for p in paths if not is_annotation_file(p))


def find_annotation_for_image(image_path: Path) -> Path | None:
    """Find a likely annotation image paired with an ultrasound image."""

    stem = image_path.stem
    candidates = [
        image_path.with_name(f"{stem}_Annotation{image_path.suffix}"),
        image_path.with_name(f"{stem}_annotation{image_path.suffix}"),
        image_path.with_name(f"{stem}_mask{image_path.suffix}"),
        image_path.with_name(f"{stem}_Mask{image_path.suffix}"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _normalize_column_name(name: str) -> str:
    return (
        name.strip()
        .lower()
        .replace("(", "")
        .replace(")", "")
        .replace("/", "_")
        .replace(" ", "_")
        .replace("-", "_")
    )


def _metadata_by_filename(root: Path, subset: str = "training") -> dict[str, dict[str, Any]]:
    csv_paths = sorted(root.rglob("*.csv")) if root.exists() else []
    if subset == "training":
        csv_paths = [path for path in csv_paths if "training" in path.name.lower()]
    elif subset == "test":
        csv_paths = [path for path in csv_paths if "test" in path.name.lower()]

    metadata: dict[str, dict[str, Any]] = {}

    for csv_path in csv_paths:
        frame = pd.read_csv(csv_path)
        original_columns = list(frame.columns)
        frame.columns = [_normalize_column_name(str(c)) for c in frame.columns]

        filename_col = _first_matching_column(frame.columns, ("filename", "file_name", "image"))
        if filename_col is None and original_columns:
            filename_col = frame.columns[0]

        if filename_col is None:
            continue

        for _, row in frame.iterrows():
            filename = str(row[filename_col])
            if not filename or filename.lower() == "nan":
                continue
            metadata[Path(filename).name] = row.to_dict()

    return metadata


def _first_matching_column(columns: list[str] | pd.Index, candidates: tuple[str, ...]) -> str | None:
    for candidate in candidates:
        for column in columns:
            if candidate == column or candidate in column:
                return str(column)
    return None


def _spacing_from_metadata(row: dict[str, Any] | None) -> tuple[float, float]:
    if not row:
        return (1.0, 1.0)

    pixel_col = _first_matching_column(list(row.keys()), ("pixel_size", "pixel_spacing", "spacing"))
    if pixel_col is not None and not pd.isna(row[pixel_col]):
        value = float(row[pixel_col])
        return (value, value)

    sx_col = _first_matching_column(list(row.keys()), ("sx", "spacing_x", "pixel_size_x"))
    sy_col = _first_matching_column(list(row.keys()), ("sy", "spacing_y", "pixel_size_y"))
    if sx_col is not None and sy_col is not None:
        return (float(row[sx_col]), float(row[sy_col]))

    return (1.0, 1.0)


def _hc_from_metadata(row: dict[str, Any] | None) -> float | None:
    if not row:
        return None
    hc_col = _first_matching_column(list(row.keys()), ("head_circumference", "hc_mm", "hc"))
    if hc_col is None or pd.isna(row[hc_col]):
        return None
    return float(row[hc_col])


def _ellipse_from_metadata(row: dict[str, Any] | None) -> EllipseAnnotation | None:
    if not row:
        return None
    keys = list(row.keys())
    cx = _first_matching_column(keys, ("center_x", "cx"))
    cy = _first_matching_column(keys, ("center_y", "cy"))
    a = _first_matching_column(keys, ("semi_axes_a", "semi_axis_a", "axis_a"))
    b = _first_matching_column(keys, ("semi_axes_b", "semi_axis_b", "axis_b"))
    angle = _first_matching_column(keys, ("angle_rad", "angle"))
    required = (cx, cy, a, b)
    if any(key is None or pd.isna(row[key]) for key in required):
        return None
    angle_value = 0.0 if angle is None or pd.isna(row[angle]) else float(row[angle])
    return EllipseAnnotation(
        center_x=float(row[cx]),
        center_y=float(row[cy]),
        semi_axis_a=float(row[a]),
        semi_axis_b=float(row[b]),
        angle_rad=angle_value,
    )


def _subset_search_root(root: Path, subset: str) -> Path:
    if subset == "training" and (root / "training_set").exists():
        return root / "training_set"
    if subset == "test" and (root / "test_set").exists():
        return root / "test_set"
    return root


def discover_hc18_records(root: str | Path, *, subset: str = "training") -> list[HC18Record]:
    """Discover HC18 image records under a raw-data root."""

    root = Path(root)
    metadata = _metadata_by_filename(root, subset=subset)
    search_root = _subset_search_root(root, subset)
    records: list[HC18Record] = []

    for image_path in find_image_files(search_root):
        row = metadata.get(image_path.name)
        records.append(
            HC18Record(
                sample_id=sample_id_from_filename(image_path.name),
                image_path=image_path,
                annotation_path=find_annotation_for_image(image_path),
                spacing_mm=_spacing_from_metadata(row),
                hc_mm=_hc_from_metadata(row),
                ellipse=_ellipse_from_metadata(row),
            )
        )

    return records


class HC18Dataset(Dataset[dict[str, Any]]):
    """PyTorch dataset for HC18 segmentation targets."""

    def __init__(
        self,
        root: str | Path,
        *,
        split_file: str | Path | None = None,
        subset: str = "training",
        image_size: tuple[int, int] | None = None,
        target_type: str = "filled",
        band_width: int = 3,
        augmentation: dict[str, Any] | None = None,
    ) -> None:
        self.root = Path(root)
        self.subset = subset
        self.image_size = image_size
        self.target_type = target_type
        self.band_width = band_width
        self.augmentation = augmentation
        records = discover_hc18_records(self.root, subset=self.subset)

        if split_file is not None:
            split_frame = pd.read_csv(split_file)
            allowed = set(split_frame["filename"].astype(str).map(lambda x: Path(x).name))
            records = [record for record in records if record.image_path.name in allowed]

        self.records = records

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int) -> dict[str, Any]:
        record = self.records[index]
        image = cv2.imread(str(record.image_path), cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise FileNotFoundError(f"Could not read image: {record.image_path}")

        original_size = image.shape[:2]
        mask = self._load_mask(record, original_size)
        spacing_mm = record.spacing_mm

        if self.image_size is not None:
            image = resize_image(image, self.image_size)
            mask = resize_mask(mask, self.image_size)
            spacing_mm = update_spacing_for_resize(spacing_mm, original_size, self.image_size)

        if self.augmentation:
            image, mask = apply_training_augmentation(image, mask, self.augmentation)

        image = normalize_image(image)
        image_tensor = torch.from_numpy(image).float().unsqueeze(0)
        mask_tensor = torch.from_numpy(mask.astype(np.float32)).unsqueeze(0)

        return {
            "image": image_tensor,
            "mask": mask_tensor,
            "spacing": torch.tensor(spacing_mm, dtype=torch.float32),
            "sample_id": record.sample_id,
            "image_path": str(record.image_path),
            "annotation": {
                "annotation_path": str(record.annotation_path) if record.annotation_path else None,
                "hc_mm": record.hc_mm,
                "ellipse": record.ellipse,
                "original_size": original_size,
            },
        }

    def _load_mask(self, record: HC18Record, image_shape: tuple[int, int]) -> np.ndarray:
        if record.annotation_path is not None:
            annotation_image = cv2.imread(str(record.annotation_path), cv2.IMREAD_UNCHANGED)
            if annotation_image is None:
                raise FileNotFoundError(f"Could not read annotation: {record.annotation_path}")
            return annotation_image_to_mask(
                annotation_image,
                target_type=self.target_type,
                band_width=self.band_width,
            )

        if record.ellipse is not None:
            return ellipse_to_mask(
                image_shape,
                record.ellipse,
                target_type=self.target_type,
                band_width=self.band_width,
            )

        raise ValueError(
            "No annotation image or ellipse metadata available for "
            f"{record.image_path.name}"
        )
