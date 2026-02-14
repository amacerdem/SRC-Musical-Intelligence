"""Model implementations for the ASU cognitive unit.

9 models, 94D total output.
"""
from __future__ import annotations

from .snem import SNEM  # alpha, 12D
from .iacm import IACM  # alpha, 11D
from .csg import CSG  # alpha, 12D
from .barm import BARM  # beta, 10D
from .stanm import STANM  # beta, 10D
from .aacm import AACM  # beta, 10D
from .pwsm import PWSM  # gamma, 10D
from .dgtp import DGTP  # gamma, 10D
from .sdl import SDL  # gamma, 9D

MODEL_CLASSES: list = [
    SNEM,
    IACM,
    CSG,
    BARM,
    STANM,
    AACM,
    PWSM,
    DGTP,
    SDL,
]
