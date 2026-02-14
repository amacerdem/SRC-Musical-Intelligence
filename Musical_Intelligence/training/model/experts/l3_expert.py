"""L3Expert -- E-L3 expert for semantic language prediction (104D).

The L3 expert specialises in MI-space[1262:1366], producing the 104D
semantic interpretation across 8 epistemological levels (alpha-theta).

NOTE: L3 is not yet implemented in the MI Teacher code. This expert
is sized correctly and participates in routing, but its loss weight
starts at 0 during training until L3 ground truth is available.

In the cross-expert DAG, L3 can attend to all other expert outputs.
"""
from __future__ import annotations

from .base_expert import BaseExpert
from ..mi_space_layout import L3_DIM


class L3Expert(BaseExpert):
    """E-L3 expert: backbone hidden → 104D semantic features.

    MI-space range: [1262:1366]
    """

    def __init__(self, d_model: int = 2048, dropout: float = 0.0) -> None:
        super().__init__(
            d_model=d_model,
            output_dim=L3_DIM,
            hidden_mult=4.0,
            dropout=dropout,
        )
