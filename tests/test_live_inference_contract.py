from __future__ import annotations

import math
from pathlib import Path

import cv2
import numpy as np
import pytest
import torch

from src.inference.live import infer_sample, run_live_inference
from src.utils.geometry import mask_to_measurement


class StaticLogitModel(torch.nn.Module):
    def __init__(self, probability: np.ndarray) -> None:
        super().__init__()
        clipped = np.clip(probability, 1e-4, 1 - 1e-4)
        logits = np.log(clipped / (1.0 - clipped)).astype(np.float32)
        self.register_buffer("logits", torch.from_numpy(logits).unsqueeze(0).unsqueeze(0))

    def forward(self, image: torch.Tensor) -> torch.Tensor:
        return self.logits.expand(image.shape[0], -1, -1, -1)


def _synthetic_sample() -> tuple[dict, np.ndarray]:
    height, width = 64, 96
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.ellipse(mask, (48, 32), (24, 14), 12, 0, 360, 1, thickness=-1)
    image = np.linspace(0, 1, height * width, dtype=np.float32).reshape(height, width)
    target_hc = mask_to_measurement(mask, (0.2, 0.2))["hc_mm"]
    sample = {
        "sample_id": "SYN_HC",
        "image": torch.from_numpy(image).unsqueeze(0),
        "mask": torch.from_numpy(mask.astype(np.float32)).unsqueeze(0),
        "spacing": torch.tensor((0.2, 0.2), dtype=torch.float32),
        "annotation": {"hc_mm": target_hc},
    }
    probability = np.where(mask > 0, 0.9, 0.1).astype(np.float32)
    return sample, probability


def test_infer_sample_returns_frontend_contract_and_assets() -> None:
    sample, probability = _synthetic_sample()
    result = infer_sample(
        sample=sample,
        model=StaticLogitModel(probability),
        device=torch.device("cpu"),
        curated_sample={
            "id": "SYN_HC",
            "label": "Synthetic sample",
            "category": "strong",
            "reason": "Contract fixture.",
        },
        run_id="synthetic_run",
        split="test",
        threshold=0.5,
    )

    frontend_sample = result.sample
    assert frontend_sample["id"] == "SYN_HC"
    assert frontend_sample["cat"] == "strong"
    assert frontend_sample["split"] == "test"
    assert set(frontend_sample["metrics"]) == {"dice", "iou", "hd95_mm", "hcErr", "predHC", "targetHC"}
    assert set(frontend_sample["predEllipse"]) == {"cx", "cy", "rx", "ry", "rot"}
    assert 0.0 <= frontend_sample["predEllipse"]["rot"] <= math.pi
    assert frontend_sample["contourHC"] > 0
    assert 0.0 <= frontend_sample["confidence"] <= 1.0
    assert frontend_sample["resolution"] == {"w": 96, "h": 64}
    assert frontend_sample["live"]["run_id"] == "synthetic_run"

    assert result.probability.shape == (64, 96)
    assert result.raw_mask.shape == (64, 96)
    assert result.cleaned_mask.shape == (64, 96)
    assert result.assets["ultrasound"].shape == (64, 96)
    assert result.assets["target"].shape == (64, 96)
    assert result.assets["prob"].shape == (64, 96)
    assert result.assets["pred"].shape == (64, 96)
    assert result.assets["prob"].dtype == np.uint8
    assert result.assets["pred"].dtype == np.uint8


def test_infer_sample_rejects_invalid_threshold() -> None:
    sample, probability = _synthetic_sample()
    with pytest.raises(ValueError, match="threshold"):
        infer_sample(
            sample=sample,
            model=StaticLogitModel(probability),
            device=torch.device("cpu"),
            curated_sample={"id": "SYN_HC", "category": "strong"},
            run_id="synthetic_run",
            split="test",
            threshold=1.0,
        )


def test_run_live_inference_on_one_curated_sample_when_local_artifacts_exist() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    checkpoint_path = repo_root / "outputs/runs/attention_unet_local_baseline/best_model.pt"
    config_path = repo_root / "outputs/runs/attention_unet_local_baseline/config.json"
    curated_path = repo_root / "docs/v2_demo/curated-samples.json"
    raw_data = repo_root / "data/raw/HC18/training_set"
    if not checkpoint_path.exists() or not config_path.exists() or not raw_data.exists():
        pytest.skip("Local HC18 data/checkpoint are required for the curated live smoke test")

    result = run_live_inference(
        "296_HC",
        checkpoint_path=checkpoint_path,
        config_path=config_path,
        curated_path=curated_path,
        split="test",
        threshold=0.5,
        device="cpu",
        timeout_s=30.0,
    )

    assert result.sample["id"] == "296_HC"
    assert result.sample["metrics"]["predHC"] > 0
    assert result.sample["metrics"]["targetHC"] > 0
    assert result.assets["prob"].shape == result.assets["ultrasound"].shape
    assert result.assets["pred"].shape == result.assets["ultrasound"].shape
