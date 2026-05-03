"""Reusable single-sample inference utilities for the v2 live demo."""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

import numpy as np
import torch

from src.data.dataset import HC18Dataset
from src.evaluation.metrics import absolute_error, dice_score, hd95, iou_score, signed_error
from src.inference.predict import load_config, load_model_from_checkpoint
from src.utils.geometry import mask_contour_length_mm, mask_to_measurement, threshold_probability


class LiveInputSource(Protocol):
    """Minimal sample source contract for local HC18 or future curated bundles."""

    def sample_ids(self) -> list[str]:
        """Return sample ids available for live inference."""

    def get_sample(self, sample_id: str) -> dict[str, Any]:
        """Return one dataset-style sample by id."""


@dataclass(frozen=True)
class LiveInferenceResult:
    """Live inference output before an API layer chooses URL or data-URL assets."""

    sample: dict[str, Any]
    assets: dict[str, np.ndarray]
    probability: np.ndarray
    raw_mask: np.ndarray
    cleaned_mask: np.ndarray
    runtime_ms: float
    threshold: float
    run_id: str
    split: str

    def to_response_payload(self, assets: dict[str, str]) -> dict[str, Any]:
        """Return the planned FastAPI response shape with caller-provided asset URLs."""

        return {
            "mode": "live",
            "runtime_ms": self.runtime_ms,
            "sample": self.sample,
            "assets": assets,
        }


class LocalHC18InputSource:
    """Load curated samples from the local HC18 dataset and split CSV."""

    def __init__(self, dataset: HC18Dataset) -> None:
        self._samples = {str(sample["sample_id"]): sample for sample in dataset}

    @classmethod
    def from_config(cls, config: dict[str, Any], split: str) -> "LocalHC18InputSource":
        dataset_config = config["dataset"]
        dataset = HC18Dataset(
            dataset_config["root"],
            split_file=Path(config["splits"]["dir"]) / f"{split}.csv",
            subset=dataset_config.get("subset", "training"),
            image_size=tuple(dataset_config["image_size"]),
            target_type=dataset_config.get("target_type", "filled"),
            band_width=int(dataset_config.get("band_width", 3)),
        )
        return cls(dataset)

    def sample_ids(self) -> list[str]:
        return sorted(self._samples)

    def get_sample(self, sample_id: str) -> dict[str, Any]:
        try:
            return self._samples[sample_id]
        except KeyError as exc:
            raise KeyError(f"{sample_id} is not present in the live input source") from exc


class LiveInferenceRunner:
    """Run deterministic curated-sample inference with a model loaded once."""

    def __init__(
        self,
        *,
        model: torch.nn.Module,
        device: torch.device,
        input_source: LiveInputSource,
        curated_samples: dict[str, dict[str, Any]],
        run_id: str,
        split: str,
    ) -> None:
        self.model = model
        self.device = device
        self.input_source = input_source
        self.curated_samples = curated_samples
        self.run_id = run_id
        self.split = split

    def sample_ids(self) -> list[str]:
        source_ids = set(self.input_source.sample_ids())
        return [sample_id for sample_id in self.curated_samples if sample_id in source_ids]

    def run(self, sample_id: str, *, threshold: float = 0.5, timeout_s: float = 30.0) -> LiveInferenceResult:
        if sample_id not in self.curated_samples:
            raise KeyError(f"{sample_id} is not in the curated sample list")
        sample = self.input_source.get_sample(sample_id)
        return infer_sample(
            sample=sample,
            model=self.model,
            device=self.device,
            curated_sample=self.curated_samples[sample_id],
            run_id=self.run_id,
            split=self.split,
            threshold=threshold,
            timeout_s=timeout_s,
        )


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def tensor_to_uint8_image(image_tensor: torch.Tensor) -> np.ndarray:
    image = image_tensor.squeeze(0).detach().cpu().numpy()
    image = image - image.min()
    denom = image.max()
    if denom > 1e-6:
        image = image / denom
    return (image * 255).astype(np.uint8)


def probability_to_uint8(probability: np.ndarray) -> np.ndarray:
    return np.clip(np.rint(probability * 255.0), 0, 255).astype(np.uint8)


def run_probability_inference(model: torch.nn.Module, image_tensor: torch.Tensor, device: torch.device) -> np.ndarray:
    image = image_tensor.unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(image)
        probability = torch.sigmoid(logits).squeeze().detach().cpu().numpy()
    return probability.astype(np.float32)


def category_for_frontend(category: str) -> str:
    if category in {"strong", "typical", "failure"}:
        return category
    if category in {"high_error", "edge"}:
        return "failure"
    if category in {"cleanup_ellipse", "cleanup", "ellipse"}:
        return "typical"
    return "typical"


def summary_from_curated(curated_sample: dict[str, Any]) -> str:
    reason = str(curated_sample.get("reason", "")).strip()
    if reason:
        return reason
    return str(curated_sample.get("label", curated_sample.get("id", "")))


def load_curated_samples(path: str | Path, sample_ids: list[str] | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    curated = load_json(path)
    samples = list(curated.get("samples", []))
    if sample_ids:
        by_id = {str(sample["id"]): sample for sample in samples}
        samples = [
            by_id.get(
                sample_id,
                {
                    "id": sample_id,
                    "label": sample_id,
                    "category": "custom",
                    "tags": ["custom"],
                    "reason": "Selected through --sample-id override.",
                },
            )
            for sample_id in sample_ids
        ]
    if not samples:
        raise ValueError("No curated samples found")
    return curated, samples


def curated_samples_by_id(path: str | Path) -> dict[str, dict[str, Any]]:
    _, samples = load_curated_samples(path)
    return {str(sample["id"]): sample for sample in samples}


def build_dataset_by_sample(config: dict[str, Any], split: str) -> dict[str, dict[str, Any]]:
    return {sample_id: sample for sample_id, sample in LocalHC18InputSource.from_config(config, split)._samples.items()}


def create_local_runner(
    *,
    config_path: str | Path,
    checkpoint_path: str | Path,
    curated_path: str | Path,
    split: str = "test",
    device: str | torch.device = "cpu",
) -> LiveInferenceRunner:
    device_obj = torch.device(device)
    config = load_config(config_path)
    model, checkpoint = load_model_from_checkpoint(checkpoint_path, device_obj)
    run_id = str(checkpoint.get("run_id", config["run"]["id"]))
    return LiveInferenceRunner(
        model=model,
        device=device_obj,
        input_source=LocalHC18InputSource.from_config(config, split),
        curated_samples=curated_samples_by_id(curated_path),
        run_id=run_id,
        split=split,
    )


def run_live_inference(
    sample_id: str,
    *,
    checkpoint_path: str | Path,
    config_path: str | Path,
    curated_path: str | Path = "docs/v2_demo/curated-samples.json",
    split: str = "test",
    threshold: float = 0.5,
    device: str | torch.device = "cpu",
    timeout_s: float = 30.0,
) -> LiveInferenceResult:
    runner = create_local_runner(
        config_path=config_path,
        checkpoint_path=checkpoint_path,
        curated_path=curated_path,
        split=split,
        device=device,
    )
    return runner.run(sample_id, threshold=threshold, timeout_s=timeout_s)


def infer_sample(
    *,
    sample: dict[str, Any],
    model: torch.nn.Module,
    device: torch.device,
    curated_sample: dict[str, Any],
    run_id: str,
    split: str,
    threshold: float = 0.5,
    timeout_s: float = 30.0,
) -> LiveInferenceResult:
    if not 0.0 < float(threshold) < 1.0:
        raise ValueError("threshold must be between 0.0 and 1.0")

    started = time.perf_counter()
    sample_id = str(sample["sample_id"])
    image_uint8 = tensor_to_uint8_image(sample["image"])
    target_mask = (sample["mask"].squeeze(0).detach().cpu().numpy() > 0).astype(np.uint8)
    probability = run_probability_inference(model, sample["image"], device)
    if probability.shape != image_uint8.shape:
        raise ValueError(f"{sample_id}: probability shape {probability.shape} does not match image shape {image_uint8.shape}")

    raw_mask = threshold_probability(probability, threshold=float(threshold))
    spacing = tuple(float(value) for value in sample["spacing"].tolist())
    measurement = mask_to_measurement(raw_mask, spacing)
    cleaned_mask = measurement["cleaned_mask"]
    if cleaned_mask.shape != probability.shape:
        raise ValueError(f"{sample_id}: cleaned mask shape {cleaned_mask.shape} does not match probability shape {probability.shape}")
    if not np.any(cleaned_mask):
        raise ValueError(f"{sample_id}: cleaned mask is empty; cannot compute confidence")

    contour_hc_mm = mask_contour_length_mm(cleaned_mask, spacing, keep_largest_component=True)
    confidence = float(probability[cleaned_mask > 0].mean())
    ellipse = measurement["ellipse"]
    pred_hc = float(measurement["hc_mm"])
    target_hc = _target_hc(sample)
    hc_error = absolute_error(pred_hc, target_hc) if target_hc is not None else math.nan
    signed_hc_error = signed_error(pred_hc, target_hc) if target_hc is not None else math.nan
    runtime_ms = (time.perf_counter() - started) * 1000.0
    if runtime_ms > timeout_s * 1000.0:
        raise TimeoutError(f"{sample_id}: inference exceeded {timeout_s:.1f}s")

    metrics_payload = {
        "dice": float(dice_score(cleaned_mask, target_mask)),
        "iou": float(iou_score(cleaned_mask, target_mask)),
        "hd95_mm": float(hd95(cleaned_mask, target_mask, spacing)),
        "hcErr": float(hc_error),
        "predHC": pred_hc,
        "targetHC": float(target_hc) if target_hc is not None else math.nan,
    }
    pred_ellipse = {
        "cx": float(ellipse.center_x),
        "cy": float(ellipse.center_y),
        "rx": float(ellipse.semi_axis_a),
        "ry": float(ellipse.semi_axis_b),
        "rot": float(math.radians(ellipse.angle_deg)),
    }
    resolution = {"w": int(image_uint8.shape[1]), "h": int(image_uint8.shape[0])}
    frontend_category = category_for_frontend(str(curated_sample.get("category", "")))

    frontend_sample = {
        "id": sample_id,
        "label": str(curated_sample.get("label", sample_id)),
        "cat": frontend_category,
        "split": split,
        "summary": summary_from_curated(curated_sample),
        "metrics": metrics_payload,
        "predEllipse": pred_ellipse,
        "contourHC": float(contour_hc_mm),
        "confidence": confidence,
        "spacingXMm": spacing[0],
        "spacingYMm": spacing[1],
        "resolution": resolution,
        "notes": "Generated live from checkpoint.",
    }
    assets = {
        "ultrasound": image_uint8,
        "target": target_mask,
        "prob": probability_to_uint8(probability),
        "pred": cleaned_mask,
    }

    # Extra fields mirror exporter metadata and are useful for tests/API tracing.
    frontend_sample["live"] = {
        "run_id": run_id,
        "threshold": float(threshold),
        "runtime_ms": runtime_ms,
        "signed_hc_error_mm": float(signed_hc_error),
        "source_category": str(curated_sample.get("category", "")),
    }
    return LiveInferenceResult(
        sample=frontend_sample,
        assets=assets,
        probability=probability,
        raw_mask=raw_mask,
        cleaned_mask=cleaned_mask,
        runtime_ms=runtime_ms,
        threshold=float(threshold),
        run_id=run_id,
        split=split,
    )


def _target_hc(sample: dict[str, Any]) -> float | None:
    value = sample.get("annotation", {}).get("hc_mm")
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return float(value)
