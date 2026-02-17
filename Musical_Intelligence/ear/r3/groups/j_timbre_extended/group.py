from __future__ import annotations
import math
import torch
from torch import Tensor
from .....contracts.bases.base_spectral_group import BaseSpectralGroup


def _build_dct_matrix(n_mels: int = 128, n_mfcc: int = 13) -> Tensor:
    """Build DCT-II matrix for MFCC computation (coefficients 1-13)."""
    matrix = torch.zeros(n_mels, n_mfcc)
    for k in range(n_mfcc):
        for n in range(n_mels):
            matrix[n, k] = math.cos(math.pi * (k + 1) * (2 * n + 1) / (2 * n_mels))
    return matrix


# Per-coefficient empirical scaling factors
_MFCC_SCALES = torch.tensor([40, 80, 60, 50, 40, 35, 30, 25, 22, 20, 18, 16, 15], dtype=torch.float32)

# 7 octave sub-bands for spectral contrast (mel bin ranges)
_CONTRAST_BANDS = [(0, 4), (4, 8), (8, 16), (16, 32), (32, 64), (64, 96), (96, 128)]


class TimbreExtendedGroup(BaseSpectralGroup):
    GROUP_NAME = "timbre_extended"
    DOMAIN = "spectral"
    OUTPUT_DIM = 20
    INDEX_RANGE = (63, 83)
    STAGE = 1
    DEPENDENCIES = ()

    def __init__(self):
        super().__init__()
        self._dct_matrix = _build_dct_matrix()  # (128, 13)

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
        B, N, T = mel.shape
        mt = mel.transpose(1, 2)  # (B, T, 128)

        dct = self._dct_matrix.to(mt.device, mt.dtype)
        scales = _MFCC_SCALES.to(mt.device, mt.dtype)

        # [94-106] MFCC 1-13: DCT-II, per-coefficient scaling
        mfcc = torch.matmul(mt, dct)  # (B, T, 13)
        mfcc = (mfcc / scales + 1.0) / 2.0  # normalize to ~[0,1]
        mfcc = mfcc.clamp(0, 1)

        # [107-113] Spectral contrast: 7 octave sub-bands
        contrasts = []
        for lo, hi in _CONTRAST_BANDS:
            band = mt[:, :, lo:hi]  # (B, T, band_width)
            band_sorted = band.sort(dim=-1).values
            bw = band.shape[-1]
            n_edge = max(1, bw // 5)  # top/bottom 20%
            valley = band_sorted[:, :, :n_edge].mean(dim=-1)
            peak = band_sorted[:, :, -n_edge:].mean(dim=-1)
            contrast = (peak - valley) / 10.0
            contrasts.append(contrast.clamp(0, 1))

        contrast_stack = torch.stack(contrasts, dim=-1)  # (B, T, 7)

        return torch.cat([mfcc, contrast_stack], dim=-1).clamp(0, 1)  # (B, T, 20)

    @property
    def feature_names(self):
        mfcc_names = tuple(f"mfcc_{i}" for i in range(1, 14))
        contrast_names = tuple(f"spectral_contrast_{i}" for i in range(1, 8))
        return mfcc_names + contrast_names
