from __future__ import annotations
import torch
from torch import Tensor
from .....contracts.bases.base_spectral_group import BaseSpectralGroup

class ConsonanceGroup(BaseSpectralGroup):
    GROUP_NAME = "consonance"
    DOMAIN = "psychoacoustic"
    OUTPUT_DIM = 7
    INDEX_RANGE = (0, 7)
    STAGE = 1
    DEPENDENCIES = ()

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
        B, N, T = mel.shape
        eps = 1e-8
        mt = mel.transpose(1, 2)  # (B, T, 128)

        # [0] roughness: sigmoid(mel_high.var / mel.mean - 0.5)
        mel_high = mt[:, :, N*3//4:]  # top 25% bins
        roughness = torch.sigmoid(
            mel_high.var(dim=-1) / mt.mean(dim=-1).clamp(min=eps) - 0.5
        )

        # [1] sethares_dissonance: mean(|diff(mel)|) / max
        diff_mel = mt[:, 1:, :] - mt[:, :-1, :]  # use spectral diff along bins
        # Actually: diff along mel-bin axis within each frame
        spec_diff = torch.diff(mt, dim=-1)  # (B, T, 127) - adjacent bin differences
        sethares = spec_diff.abs().mean(dim=-1)  # (B, T)
        sethares = sethares / sethares.amax(dim=-1, keepdim=True).clamp(min=eps)

        # [2] helmholtz_kang: lag-1 autocorrelation of spectrum
        m1 = mt[:, :, :-1]  # (B, T, 127)
        m2 = mt[:, :, 1:]   # (B, T, 127)
        # Pearson correlation along mel-bin axis
        m1c = m1 - m1.mean(dim=-1, keepdim=True)
        m2c = m2 - m2.mean(dim=-1, keepdim=True)
        num = (m1c * m2c).sum(dim=-1)
        den = (m1c.pow(2).sum(dim=-1) * m2c.pow(2).sum(dim=-1)).sqrt().clamp(min=eps)
        helmholtz = (num / den).clamp(0, 1)  # (B, T)

        # [3] stumpf_fusion: low-freq energy ratio
        quarter = N // 4
        stumpf = mt[:, :, :quarter].sum(dim=-1) / mt.sum(dim=-1).clamp(min=eps)

        # [4] sensory_pleasantness: 0.6*(1-sethares) + 0.4*stumpf
        pleasantness = 0.6 * (1.0 - sethares) + 0.4 * stumpf

        # [5] inharmonicity: 1 - helmholtz
        inharmonicity = 1.0 - helmholtz

        # [6] harmonic_deviation: 0.5*sethares + 0.5*(1-helmholtz)
        harmonic_dev = 0.5 * sethares + 0.5 * (1.0 - helmholtz)

        return torch.stack([
            roughness, sethares, helmholtz, stumpf,
            pleasantness, inharmonicity, harmonic_dev
        ], dim=-1).clamp(0, 1)  # (B, T, 7)

    @property
    def feature_names(self):
        return (
            "roughness", "sethares_dissonance", "helmholtz_kang",
            "stumpf_fusion", "sensory_pleasantness", "inharmonicity",
            "harmonic_deviation",
        )
