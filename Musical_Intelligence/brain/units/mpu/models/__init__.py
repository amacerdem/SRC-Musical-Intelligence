"""Model implementations for the MPU cognitive unit.

10 models, 104D total output.
"""
from __future__ import annotations

from .peom import PEOM  # alpha, 12D
from .msr import MSR  # alpha, 12D
from .gssm import GSSM  # alpha, 11D
from .asap import ASAP  # beta, 10D
from .ddsmi import DDSMI  # beta, 10D
from .vrmsme import VRMSME  # beta, 10D
from .spmc import SPMC  # beta, 11D
from .nscp import NSCP  # gamma, 10D
from .ctbb import CTBB  # gamma, 9D
from .stc import STC  # gamma, 9D

MODEL_CLASSES: list = [
    PEOM,
    MSR,
    GSSM,
    ASAP,
    DDSMI,
    VRMSME,
    SPMC,
    NSCP,
    CTBB,
    STC,
]
