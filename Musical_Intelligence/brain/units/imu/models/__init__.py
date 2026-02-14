"""Model implementations for the IMU cognitive unit.

15 models, 159D total output.
"""
from __future__ import annotations

from .meamn import MEAMN  # alpha, 14D
from .pnh import PNH  # alpha, 12D
from .mmp import MMP  # alpha, 11D
from .rasn import RASN  # beta, 10D
from .pmim import PMIM  # beta, 11D
from .oii import OII  # beta, 10D
from .hcmc import HCMC  # beta, 10D
from .riri import RIRI  # beta, 10D
from .mspba import MSPBA  # beta, 11D
from .vriap import VRIAP  # beta, 10D
from .tprd import TPRD  # beta, 11D
from .cmapcc import CMAPCC  # beta, 10D
from .dmms import DMMS  # gamma, 10D
from .cssl import CSSL  # gamma, 10D
from .cdem import CDEM  # gamma, 9D

MODEL_CLASSES: list = [
    MEAMN,
    PNH,
    MMP,
    RASN,
    PMIM,
    OII,
    HCMC,
    RIRI,
    MSPBA,
    VRIAP,
    TPRD,
    CMAPCC,
    DMMS,
    CSSL,
    CDEM,
]
