"""C3Expert -- E-C3 expert for cognitive model prediction (1006D).

The C3 expert is the largest, specialising in MI-space[256:1262].
It produces outputs for all 96 cognitive models across 9 units.

In the cross-expert DAG, C3 can attend to Cochlea and R3 outputs.
"""
from __future__ import annotations

from .base_expert import BaseExpert
from ..mi_space_layout import C3_DIM


class C3Expert(BaseExpert):
    """E-C3 expert: backbone hidden → 1006D cognitive model outputs.

    MI-space range: [256:1262]
    """

    def __init__(self, d_model: int = 2048, dropout: float = 0.0) -> None:
        super().__init__(
            d_model=d_model,
            output_dim=C3_DIM,
            hidden_mult=4.0,
            dropout=dropout,
        )
