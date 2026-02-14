"""StateHead -- Produces the 1366D MI-space output from expert outputs.

Concatenates and refines all 4 expert outputs into the final
1366D MI-space state vector. This is the primary output head.
"""
from __future__ import annotations

from typing import List

import torch
import torch.nn as nn
from torch import Tensor

from ..mi_space_layout import MI_SPACE_DIM


class StateHead(nn.Module):
    """MI-space state head: expert outputs → 1366D.

    Takes the concatenated 4-expert output (128+128+1006+104 = 1366D),
    applies a refinement MLP + LayerNorm, and produces the final
    MI-space state.

    Parameters
    ----------
    mi_space_dim : int
        Total MI-space dimension (default 1366).
    hidden_dim : int
        Hidden dimension for refinement MLP (default 2048).
    """

    def __init__(
        self,
        mi_space_dim: int = MI_SPACE_DIM,
        hidden_dim: int = 2048,
    ) -> None:
        super().__init__()
        self.mi_space_dim = mi_space_dim

        self.refine = nn.Sequential(
            nn.Linear(mi_space_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, mi_space_dim),
            nn.LayerNorm(mi_space_dim),
        )

    def forward(self, expert_outputs: List[Tensor]) -> Tensor:
        """Combine expert outputs into 1366D MI-space.

        Parameters
        ----------
        expert_outputs : list of Tensor
            [cochlea (B,T,128), r3 (B,T,128), c3 (B,T,1006), l3 (B,T,104)]

        Returns
        -------
        Tensor
            ``(B, T, 1366)`` MI-space state.
        """
        concat = torch.cat(expert_outputs, dim=-1)  # (B, T, 1366)
        return concat + self.refine(concat)  # Residual refinement
