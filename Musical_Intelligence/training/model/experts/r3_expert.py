"""R3Expert -- E-R3 expert for spectral feature prediction (128D).

The R3 expert specialises in MI-space[128:256], producing the 128D
spectral feature vector across 11 groups (A-K): consonance, energy,
timbre, change, interactions, pitch/chroma, rhythm, harmony,
information, extended timbre, modulation.

In the cross-expert DAG, R3 can attend to Cochlea output.
"""
from __future__ import annotations

from .base_expert import BaseExpert
from ..mi_space_layout import R3_DIM


class R3Expert(BaseExpert):
    """E-R3 expert: backbone hidden → 128D spectral features.

    MI-space range: [128:256]
    """

    def __init__(self, d_model: int = 2048, dropout: float = 0.0) -> None:
        super().__init__(
            d_model=d_model,
            output_dim=R3_DIM,
            hidden_mult=4.0,
            dropout=dropout,
        )
