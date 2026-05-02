"""Validate the saved-output v2 demo sample manifest."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SAFETY_TEXT = "Educational demo only. Not for clinical use."
REQUIRED_SAMPLE_FIELDS = {
    "id",
    "label",
    "cat",
    "split",
    "summary",
    "metrics",
    "predEllipse",
    "contourHC",
    "confidence",
    "spacingXMm",
    "spacingYMm",
    "resolution",
}
REQUIRED_ARTIFACT_FILES = {
    "ultrasound.png",
    "target.png",
    "pred.png",
    "prob.png",
    "metadata.json",
}
REQUIRED_METRICS_FIELDS = {
    "dice",
    "iou",
    "hd95_mm",
    "hcErr",
    "predHC",
    "targetHC",
}
REQUIRED_ELLIPSE_FIELDS = {
    "cx",
    "cy",
    "rx",
    "ry",
    "rot",
}
REQUIRED_RESOLUTION_FIELDS = {"w", "h"}
NUMERIC_SAMPLE_FIELDS = {"contourHC", "confidence", "spacingXMm", "spacingYMm"}
VALID_CATEGORIES = {"strong", "typical", "failure"}


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _sample_dir(artifact_root: Path, sample_id: str) -> Path:
    return artifact_root / sample_id


def _validate_numeric_object(
    *,
    errors: list[str],
    prefix: str,
    value: Any,
    required_fields: set[str],
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{prefix} must be an object")
        return
    missing = sorted(required_fields - set(value))
    if missing:
        errors.append(f"{prefix} missing fields: {', '.join(missing)}")
    for field in sorted(required_fields & set(value)):
        if not _is_number(value[field]):
            errors.append(f"{prefix}.{field} must be a finite number")


def validate_manifest(
    manifest: dict[str, Any],
    *,
    repo_root: str | Path = PROJECT_ROOT,
    artifact_root: str | Path | None = None,
) -> list[str]:
    """Return a list of validation errors for a demo manifest."""

    repo_root = Path(repo_root)
    artifact_root = Path(artifact_root) if artifact_root is not None else repo_root / "outputs" / "demo_samples"
    errors: list[str] = []

    if manifest.get("schema_version") != 2:
        errors.append("schema_version must be 2")
    if manifest.get("safety_text") != REQUIRED_SAFETY_TEXT:
        errors.append(f"safety_text must be {REQUIRED_SAFETY_TEXT!r}")

    samples = manifest.get("samples")
    if not isinstance(samples, list) or not samples:
        errors.append("samples must be a non-empty list")
        return errors

    categories = set()
    for index, sample in enumerate(samples):
        prefix = f"samples[{index}]"
        if not isinstance(sample, dict):
            errors.append(f"{prefix} must be an object")
            continue

        missing = sorted(REQUIRED_SAMPLE_FIELDS - set(sample))
        if missing:
            errors.append(f"{prefix} missing fields: {', '.join(missing)}")
            continue

        sample_id = str(sample["id"])
        category = str(sample["cat"])
        categories.add(category)
        if category not in VALID_CATEGORIES:
            errors.append(f"{sample_id}: cat must be one of {sorted(VALID_CATEGORIES)}")

        sample_dir = _sample_dir(artifact_root, sample_id)
        for filename in sorted(REQUIRED_ARTIFACT_FILES):
            path = sample_dir / filename
            if not path.exists():
                errors.append(f"{sample_id}: missing required artifact {path}")

        for field in sorted(NUMERIC_SAMPLE_FIELDS):
            if not _is_number(sample[field]):
                errors.append(f"{sample_id}: {field} must be a finite number")
        if _is_number(sample["confidence"]) and not (0.0 <= float(sample["confidence"]) <= 1.0):
            errors.append(f"{sample_id}: confidence must be between 0 and 1")

        _validate_numeric_object(
            errors=errors,
            prefix=f"{sample_id}: metrics",
            value=sample.get("metrics"),
            required_fields=REQUIRED_METRICS_FIELDS,
        )
        _validate_numeric_object(
            errors=errors,
            prefix=f"{sample_id}: predEllipse",
            value=sample.get("predEllipse"),
            required_fields=REQUIRED_ELLIPSE_FIELDS,
        )
        _validate_numeric_object(
            errors=errors,
            prefix=f"{sample_id}: resolution",
            value=sample.get("resolution"),
            required_fields=REQUIRED_RESOLUTION_FIELDS,
        )
        resolution = sample.get("resolution")
        if isinstance(resolution, dict):
            for field in sorted(REQUIRED_RESOLUTION_FIELDS & set(resolution)):
                if _is_number(resolution[field]) and int(resolution[field]) <= 0:
                    errors.append(f"{sample_id}: resolution.{field} must be positive")

        metadata_path = sample_dir / "metadata.json"
        if not metadata_path.exists():
            continue

        try:
            metadata = load_json(metadata_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{sample_id}: metadata is invalid JSON: {exc}")
            continue

        if str(metadata.get("sample_id")) != sample_id:
            errors.append(f"{sample_id}: metadata sample_id mismatch: {metadata.get('sample_id')}")
        if str(metadata.get("split")) != str(sample["split"]):
            errors.append(f"{sample_id}: metadata split mismatch: {metadata.get('split')}")
        for field in ["cat", "contourHC", "confidence", "spacingXMm", "spacingYMm"]:
            if metadata.get(field) != sample.get(field):
                errors.append(f"{sample_id}: metadata {field} does not match manifest")

    if "strong" not in categories:
        errors.append("manifest must include at least one strong sample")
    if "failure" not in categories:
        errors.append("manifest must include at least one failure sample")

    return errors


def validate_manifest_file(path: str | Path, *, repo_root: str | Path = PROJECT_ROOT) -> list[str]:
    path = Path(path)
    return validate_manifest(load_json(path), repo_root=repo_root, artifact_root=path.parent)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default="outputs/demo_samples/manifest.json")
    args = parser.parse_args()

    errors = validate_manifest_file(args.manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

    print(f"Validated demo manifest: {args.manifest}")


if __name__ == "__main__":
    main()
