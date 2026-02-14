"""Regularization losses -- Temporal smoothness and expert balance.

- temporal_smooth: Penalises discontinuities in MI-space output
- expert_balance:  MoE load balancing loss (from router)
"""
from __future__ import annotations

from typing import Dict

import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


class RegularizationLoss(nn.Module):
    """Temporal smoothness and expert balance regularisation."""

    def forward(
        self,
        mi_space: Tensor,
        balance_loss: Tensor,
    ) -> Dict[str, Tensor]:
        """Compute regularisation losses.

        Parameters
        ----------
        mi_space : Tensor
            ``(B, T, 1366)`` MI-space output.
        balance_loss : Tensor
            Expert routing balance loss from router.

        Returns
        -------
        dict
            Maps ``temporal_smooth`` and ``expert_balance`` to scalars.
        """
        # Temporal smoothness: L2 norm of frame-to-frame differences
        if mi_space.shape[1] > 1:
            diff = mi_space[:, 1:] - mi_space[:, :-1]
            temporal = (diff ** 2).mean()
        else:
            temporal = mi_space.new_tensor(0.0)

        return {
            "temporal_smooth": temporal,
            "expert_balance": balance_loss,
        }
