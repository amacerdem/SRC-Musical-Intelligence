"""Model implementations for the SPU cognitive unit.

9 models, 99D total output.
"""
from __future__ import annotations

from .bch import BCH  # alpha, 12D
from .pscl import PSCL  # alpha, 12D
from .pccr import PCCR  # alpha, 11D
from .stai import STAI  # beta, 12D
from .tscp import TSCP  # beta, 10D
from .miaa import MIAA  # beta, 11D
from .sdnps import SDNPS  # gamma, 10D
from .esme import ESME  # gamma, 11D
from .sded import SDED  # gamma, 10D

MODEL_CLASSES: list = [
    BCH,
    PSCL,
    PCCR,
    STAI,
    TSCP,
    MIAA,
    SDNPS,
    ESME,
    SDED,
]
