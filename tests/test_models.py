import torch

from src.models import build_model, count_parameters
from src.models.unet import UNet


def test_unet_forward_shape_matches_target_shape():
    model = UNet(in_channels=1, out_channels=1, base_channels=8)
    x = torch.randn(2, 1, 64, 96)

    with torch.no_grad():
        logits = model(x)

    assert logits.shape == (2, 1, 64, 96)


def test_unet_handles_odd_input_size():
    model = UNet(in_channels=1, out_channels=1, base_channels=8)
    x = torch.randn(1, 1, 65, 97)

    with torch.no_grad():
        logits = model(x)

    assert logits.shape == (1, 1, 65, 97)


def test_model_registry_builds_unet():
    model = build_model("unet", in_channels=1, out_channels=1, base_channels=8)

    assert isinstance(model, UNet)
    assert count_parameters(model) > 0
