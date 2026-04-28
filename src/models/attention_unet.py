"""Attention U-Net segmentation model."""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F

from src.models.unet import DoubleConv, DownBlock


class AttentionGate(nn.Module):
    """Additive attention gate for filtering encoder skip features."""

    def __init__(self, skip_channels: int, gating_channels: int, inter_channels: int) -> None:
        super().__init__()
        self.skip_projection = nn.Sequential(
            nn.Conv2d(skip_channels, inter_channels, kernel_size=1, bias=False),
            nn.BatchNorm2d(inter_channels),
        )
        self.gating_projection = nn.Sequential(
            nn.Conv2d(gating_channels, inter_channels, kernel_size=1, bias=False),
            nn.BatchNorm2d(inter_channels),
        )
        self.attention = nn.Sequential(
            nn.ReLU(inplace=True),
            nn.Conv2d(inter_channels, 1, kernel_size=1),
            nn.Sigmoid(),
        )

    def forward(self, skip: torch.Tensor, gating: torch.Tensor) -> torch.Tensor:
        gating = F.interpolate(gating, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        coefficients = self.attention(self.skip_projection(skip) + self.gating_projection(gating))
        return skip * coefficients


class AttentionUpBlock(nn.Module):
    """Upsampling block with attention-gated skip concatenation."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.up = nn.ConvTranspose2d(in_channels, out_channels, kernel_size=2, stride=2)
        inter_channels = max(1, skip_channels // 2)
        self.gate = AttentionGate(
            skip_channels=skip_channels,
            gating_channels=out_channels,
            inter_channels=inter_channels,
        )
        self.conv = DoubleConv(out_channels + skip_channels, out_channels)

    def forward(self, x: torch.Tensor, skip: torch.Tensor) -> torch.Tensor:
        x = self.up(x)
        if x.shape[-2:] != skip.shape[-2:]:
            x = F.interpolate(x, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        skip = self.gate(skip, x)
        return self.conv(torch.cat([skip, x], dim=1))


class AttentionUNet(nn.Module):
    """Attention U-Net for binary fetal head segmentation.

    Contract:
        input: `[B, in_channels, H, W]`
        output: `[B, out_channels, H, W]` logits
    """

    def __init__(
        self,
        in_channels: int = 1,
        out_channels: int = 1,
        base_channels: int = 32,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        channels = [base_channels, base_channels * 2, base_channels * 4, base_channels * 8]

        self.encoder1 = DoubleConv(in_channels, channels[0])
        self.encoder2 = DownBlock(channels[0], channels[1])
        self.encoder3 = DownBlock(channels[1], channels[2])
        self.encoder4 = DownBlock(channels[2], channels[3])
        self.bottleneck = DownBlock(channels[3], channels[3] * 2, dropout=dropout)

        self.decoder4 = AttentionUpBlock(channels[3] * 2, channels[3], channels[3])
        self.decoder3 = AttentionUpBlock(channels[3], channels[2], channels[2])
        self.decoder2 = AttentionUpBlock(channels[2], channels[1], channels[1])
        self.decoder1 = AttentionUpBlock(channels[1], channels[0], channels[0])
        self.output_conv = nn.Conv2d(channels[0], out_channels, kernel_size=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        skip1 = self.encoder1(x)
        skip2 = self.encoder2(skip1)
        skip3 = self.encoder3(skip2)
        skip4 = self.encoder4(skip3)
        x = self.bottleneck(skip4)

        x = self.decoder4(x, skip4)
        x = self.decoder3(x, skip3)
        x = self.decoder2(x, skip2)
        x = self.decoder1(x, skip1)
        return self.output_conv(x)
