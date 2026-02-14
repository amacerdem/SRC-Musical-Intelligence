"""PlanningHead -- Predicts K future frames in MI-space.

The planning head projects the backbone hidden state into K future
MI-space states, enabling the model to plan ~2 seconds ahead.

At inference, if no motor input changes, MI-Core executes the
pre-planned trajectory.
"""
from __future__ import annotations

import torch.nn as nn
from torch import Tensor

from ..mi_space_layout import MI_SPACE_DIM, PLANNING_HORIZON_STEPS


class PlanningHead(nn.Module):
    """Planning head: hidden → K × 1366D future trajectory.

    Parameters
    ----------
    d_model : int
        Backbone hidden dimension (default 2048).
    mi_space_dim : int
        MI-space dimension (default 1366).
    n_steps : int
        Number of future steps to predict (default 8).
    """

    def __init__(
        self,
        d_model: int = 2048,
        mi_space_dim: int = MI_SPACE_DIM,
        n_steps: int = PLANNING_HORIZON_STEPS,
    ) -> None:
        super().__init__()
        self.n_steps = n_steps
        self.mi_space_dim = mi_space_dim

        self.proj = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, d_model),
            nn.GELU(),
            nn.Linear(d_model, n_steps * mi_space_dim),
        )

    def forward(self, hidden: Tensor) -> Tensor:
        """Predict future MI-space trajectory.

        Parameters
        ----------
        hidden : Tensor
            Shape ``(B, T, d_model)`` backbone hidden state.

        Returns
        -------
        Tensor
            Shape ``(B, T, n_steps, mi_space_dim)``.
        """
        B, T, D = hidden.shape
        out = self.proj(hidden)  # (B, T, n_steps * mi_space_dim)
        return out.view(B, T, self.n_steps, self.mi_space_dim)
