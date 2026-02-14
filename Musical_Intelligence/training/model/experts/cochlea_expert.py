"""CochleaExpert -- E-Cochlea expert for mel spectrogram generation (128D).

The Cochlea expert specialises in MI-space[0:128], producing the mel
spectrogram representation that Vocos renders into audio waveform.

This expert is independent (no cross-expert dependencies).
"""
from __future__ import annotations

from .base_expert import BaseExpert
from ..mi_space_layout import COCHLEA_DIM


class CochleaExpert(BaseExpert):
    """E-Cochlea expert: backbone hidden → 128D mel features.

    MI-space range: [0:128]
    """

    def __init__(self, d_model: int = 2048, dropout: float = 0.0) -> None:
        super().__init__(
            d_model=d_model,
            output_dim=COCHLEA_DIM,
            hidden_mult=4.0,
            dropout=dropout,
        )
