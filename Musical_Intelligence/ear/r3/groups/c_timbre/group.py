from __future__ import annotations
import torch
from torch import Tensor
from .....contracts.bases.base_spectral_group import BaseSpectralGroup

class TimbreGroup(BaseSpectralGroup):
    GROUP_NAME = "timbre"
    DOMAIN = "spectral"
    OUTPUT_DIM = 9
    INDEX_RANGE = (12, 21)
    STAGE = 1
    DEPENDENCIES = ()

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
        B, N, T = mel.shape
        eps = 1e-8
        mt = mel.transpose(1, 2)  # (B, T, 128)
        total = mt.sum(dim=-1).clamp(min=eps)
        quarter = N // 4
        third = N // 3

        # [12] warmth: low-freq ratio (== stumpf_fusion, known duplicate)
        warmth = mt[:, :, :quarter].sum(dim=-1) / total

        # [13] sharpness: high-freq ratio
        sharpness = mt[:, :, 3*quarter:].sum(dim=-1) / total

        # [14] tonalness: peak / sum
        tonalness = mt.max(dim=-1).values / total

        # [15] clarity: spectral centroid / N
        bins = torch.arange(N, device=mel.device, dtype=mel.dtype)
        centroid = (mt * bins).sum(dim=-1) / total
        clarity = centroid / N

        # [16] spectral_smoothness: 1 - mean(|diff|)/frame_energy
        # Per-frame normalization: smooth spectrum (small diffs relative to
        # energy) scores high; peaked/jagged spectrum scores low.
        spec_diff = torch.diff(mt, dim=-1).abs().mean(dim=-1)   # (B, T)
        frame_energy = mt.mean(dim=-1).clamp(min=eps)            # (B, T)
        smoothness = (1.0 - (spec_diff / frame_energy).clamp(0, 1)).clamp(0, 1)

        # [17] spectral_autocorrelation: lag-1 autocorr (== helmholtz, known dup)
        m1 = mt[:, :, :-1]
        m2 = mt[:, :, 1:]
        m1c = m1 - m1.mean(dim=-1, keepdim=True)
        m2c = m2 - m2.mean(dim=-1, keepdim=True)
        num = (m1c * m2c).sum(dim=-1)
        den = (m1c.pow(2).sum(dim=-1) * m2c.pow(2).sum(dim=-1)).sqrt().clamp(min=eps)
        autocorr = (num / den).clamp(0, 1)

        # [18-20] tristimulus 1/2/3
        t1 = mt[:, :, :third].sum(dim=-1) / total
        t2 = mt[:, :, third:2*third].sum(dim=-1) / total
        t3 = mt[:, :, 2*third:].sum(dim=-1) / total

        return torch.stack([
            warmth, sharpness, tonalness, clarity, smoothness,
            autocorr, t1, t2, t3
        ], dim=-1).clamp(0, 1)

    @property
    def feature_names(self):
        return (
            "warmth", "sharpness", "tonalness", "clarity",
            "spectral_smoothness", "spectral_autocorrelation",
            "tristimulus1", "tristimulus2", "tristimulus3",
        )
