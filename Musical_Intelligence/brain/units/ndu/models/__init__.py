"""Model implementations for the NDU cognitive unit.

9 models, 94D total output.
"""
from __future__ import annotations

from .mpg import MPG  # alpha, 12D
from .sdd import SDD  # alpha, 11D
from .ednr import EDNR  # alpha, 12D
from .dsp import DSP  # beta, 10D
from .cdmr import CDMR  # beta, 10D
from .slee import SLEE  # beta, 10D
from .sddp import SDDP  # gamma, 10D
from .oni import ONI  # gamma, 10D
from .ect import ECT  # gamma, 9D

MODEL_CLASSES: list = [
    MPG,
    SDD,
    EDNR,
    DSP,
    CDMR,
    SLEE,
    SDDP,
    ONI,
    ECT,
]
