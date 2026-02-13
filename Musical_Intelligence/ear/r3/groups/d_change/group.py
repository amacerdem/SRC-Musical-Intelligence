from __future__ import annotations
import torch
from torch import Tensor
from .....contracts.bases.base_spectral_group import BaseSpectralGroup

class ChangeGroup(BaseSpectralGroup):
    GROUP_NAME = "change"
    DOMAIN = "temporal"
    OUTPUT_DIM = 4
    INDEX_RANGE = (21, 25)
    STAGE = 1
    DEPENDENCIES = ()

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
        B, N, T = mel.shape
        eps = 1e-8
        mt = mel.transpose(1, 2)  # (B, T, 128)

        # [21] spectral_flux: L2 norm of frame diff, max-norm
        diff = mt[:, 1:, :] - mt[:, :-1, :]
        flux_vals = diff.pow(2).sum(dim=-1).sqrt()  # (B, T-1)
        flux = torch.zeros(B, T, device=mel.device, dtype=mel.dtype)
        flux[:, 1:] = flux_vals
        flux = flux / flux.amax(dim=-1, keepdim=True).clamp(min=eps)

        # Probability distribution for entropy/flatness/concentration
        p = mt.clamp(min=eps)
        p = p / p.sum(dim=-1, keepdim=True)

        # [22] distribution_entropy: Shannon entropy / log(128)
        log_p = torch.log(p)
        entropy = -(p * log_p).sum(dim=-1) / torch.log(torch.tensor(128.0, device=mel.device))

        # [23] distribution_flatness: geometric mean / arithmetic mean (Wiener entropy)
        log_mean = p.log().mean(dim=-1)  # log of geometric mean
        arith_mean = p.mean(dim=-1).clamp(min=eps)
        flatness = log_mean.exp() / arith_mean

        # [24] distribution_concentration: HHI * N, clamped to [0,1]
        # KNOWN BUG: Both uniform and concentrated distributions map to 1.0
        # See Docs/R3/Pipeline/Normalization.md Section 4.2
        # Phase 6 fix: (HHI - 1/N) / (1 - 1/N)
        concentration = (p.pow(2).sum(dim=-1) * N).clamp(0, 1)

        return torch.stack([
            flux, entropy, flatness, concentration
        ], dim=-1).clamp(0, 1)

    @property
    def feature_names(self):
        return (
            "spectral_flux", "distribution_entropy",
            "distribution_flatness", "distribution_concentration",
        )
