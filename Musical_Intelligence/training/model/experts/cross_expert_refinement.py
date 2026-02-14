"""CrossExpertRefinement -- Causal DAG-masked cross-expert attention.

After individual expert outputs are computed, this module refines
them via cross-attention with a causal DAG mask that mirrors the
MI Teacher pipeline's information flow:

    E-Cochlea → E-R3 → E-C3 → E-L3

Attention mask::

             Cochlea  R3     C3     L3
    Cochlea [  1      0      0      0  ]   Cochlea is independent
    R3      [  1      1      0      0  ]   R3 sees Cochlea
    C3      [  1      1      1      0  ]   C3 sees Cochlea + R3
    L3      [  1      1      1      1  ]   L3 sees everything

This ensures experts respect the causal ordering of the teacher pipeline.
"""
from __future__ import annotations

from typing import List

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor

from ..mi_space_layout import C3_DIM, COCHLEA_DIM, L3_DIM, R3_DIM


# Expert output dimensions in MI-space order
EXPERT_DIMS = [COCHLEA_DIM, R3_DIM, C3_DIM, L3_DIM]  # [128, 128, 1006, 104]
N_EXPERTS = len(EXPERT_DIMS)


class CrossExpertRefinement(nn.Module):
    """Cross-expert refinement with causal DAG mask.

    Each expert output is projected to a shared dimension, refined
    via masked multi-head attention, then projected back to its
    original dimension.

    Parameters
    ----------
    d_expert_shared : int
        Shared hidden dimension for cross-expert attention (default 512).
    n_heads : int
        Number of attention heads (default 8).
    dropout : float
        Attention dropout (default 0.0).
    """

    def __init__(
        self,
        d_expert_shared: int = 512,
        n_heads: int = 8,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        self.d_shared = d_expert_shared
        self.n_heads = n_heads

        # Project each expert to shared dim
        self.proj_in = nn.ModuleList([
            nn.Linear(dim, d_expert_shared, bias=False)
            for dim in EXPERT_DIMS
        ])

        # Project back from shared dim
        self.proj_out = nn.ModuleList([
            nn.Linear(d_expert_shared, dim, bias=False)
            for dim in EXPERT_DIMS
        ])

        # Multi-head attention
        self.attn = nn.MultiheadAttention(
            embed_dim=d_expert_shared,
            num_heads=n_heads,
            dropout=dropout,
            batch_first=True,
        )

        self.norm = nn.LayerNorm(d_expert_shared)

        # Build the causal DAG mask (4×4)
        self.register_buffer(
            "dag_mask",
            self._build_dag_mask(),
            persistent=False,
        )

    @staticmethod
    def _build_dag_mask() -> Tensor:
        """Build the 4×4 causal DAG attention mask.

        Returns (4, 4) bool mask where True = MASKED (cannot attend).
        Follows PyTorch convention: True values are masked out.
        """
        # Cochlea→R3→C3→L3 (lower triangular = allowed)
        mask = torch.ones(N_EXPERTS, N_EXPERTS, dtype=torch.bool)
        for i in range(N_EXPERTS):
            for j in range(i + 1):
                mask[i, j] = False  # Can attend to self and predecessors
        return mask

    def forward(self, expert_outputs: List[Tensor]) -> List[Tensor]:
        """Refine expert outputs via cross-expert attention.

        Parameters
        ----------
        expert_outputs : list of Tensor
            4 tensors: [cochlea (B,T,128), r3 (B,T,128),
                        c3 (B,T,1006), l3 (B,T,104)].

        Returns
        -------
        list of Tensor
            Refined expert outputs with same shapes.
        """
        B, T = expert_outputs[0].shape[:2]

        # Project to shared dimension
        projected = [
            proj(out) for proj, out in zip(self.proj_in, expert_outputs)
        ]  # List of (B, T, d_shared)

        # Stack experts as sequence: (B, T, 4, d_shared) -> (B*T, 4, d_shared)
        stacked = torch.stack(projected, dim=2)
        stacked = stacked.view(B * T, N_EXPERTS, self.d_shared)

        # Cross-expert attention with DAG mask
        normed = self.norm(stacked)
        refined, _ = self.attn(
            normed, normed, normed,
            attn_mask=self.dag_mask,
        )
        stacked = stacked + refined  # Residual

        # Reshape back: (B*T, 4, d_shared) -> (B, T, 4, d_shared)
        stacked = stacked.view(B, T, N_EXPERTS, self.d_shared)

        # Project back to expert-specific dimensions
        outputs = []
        for i, proj_out in enumerate(self.proj_out):
            expert_refined = proj_out(stacked[:, :, i])  # (B, T, expert_dim)
            # Residual from original expert output
            outputs.append(expert_refined + expert_outputs[i])

        return outputs
