"""CompositeLoss -- Aggregates all 14 loss terms with curriculum weights.

Combines encode, decode, cycle, fill, and regularisation losses using
the CurriculumScheduler's epoch-dependent weights.

Total loss:
    L = sum_i(w_i * L_i) for all 14 terms

Reference: MI-VISION Section 12.3, 12.5
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
import torch.nn as nn
from torch import Tensor

from .curriculum import CurriculumScheduler


class MICompositeLoss(nn.Module):
    """Combined loss with 14 terms and curriculum-scheduled weights.

    Usage::

        loss_fn = MICompositeLoss()
        total, breakdown = loss_fn(individual_losses, epoch=100)
    """

    def __init__(self, interpolate: bool = True) -> None:
        super().__init__()
        self.scheduler = CurriculumScheduler(interpolate=interpolate)

    def forward(
        self,
        losses: Dict[str, Tensor],
        epoch: int,
    ) -> Tuple[Tensor, Dict[str, float]]:
        """Aggregate all losses with curriculum weights.

        Parameters
        ----------
        losses : dict
            Maps each loss name to its scalar tensor value.
            Expected keys: encode_mel, encode_r3, encode_h3, encode_c3,
            decode_h3, decode_r3, decode_mel, decode_wav,
            cycle_forward, cycle_inverse, fill_c3, fill_decode,
            temporal_smooth, expert_balance.
        epoch : int
            Current training epoch.

        Returns
        -------
        total_loss : Tensor
            Weighted sum of all losses.
        breakdown : dict
            Maps each loss name to its weighted scalar value (for logging).
        """
        weights = self.scheduler.get_weights(epoch)

        total = torch.tensor(0.0, device=self._get_device(losses))
        breakdown: Dict[str, float] = {}

        for name, weight in weights.items():
            if name in losses and weight > 0:
                weighted = weight * losses[name]
                total = total + weighted
                breakdown[name] = weighted.item()
            else:
                breakdown[name] = 0.0

        breakdown["total"] = total.item()
        breakdown["phase"] = self.scheduler.get_phase(epoch)

        return total, breakdown

    @staticmethod
    def _get_device(losses: Dict[str, Tensor]) -> torch.device:
        """Get device from first available loss tensor."""
        for v in losses.values():
            if isinstance(v, Tensor):
                return v.device
        return torch.device("cpu")
