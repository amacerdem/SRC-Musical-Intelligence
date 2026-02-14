"""Model implementations for the ARU cognitive unit.

10 models, 120D total output.
"""
from __future__ import annotations

from .srp import SRP  # alpha, 19D
from .aac import AAC  # alpha, 14D
from .vmm import VMM  # alpha, 12D
from .pupf import PUPF  # beta, 12D
from .clam import CLAM  # beta, 11D
from .mad import MAD  # beta, 11D
from .nemac import NEMAC  # beta, 11D
from .dap import DAP  # gamma, 10D
from .cmat import CMAT  # gamma, 10D
from .tar import TAR  # gamma, 10D

MODEL_CLASSES: list = [
    SRP,
    AAC,
    VMM,
    PUPF,
    CLAM,
    MAD,
    NEMAC,
    DAP,
    CMAT,
    TAR,
]
