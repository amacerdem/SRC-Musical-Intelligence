"""Model implementations for the STU cognitive unit.

14 models, 148D total output.
"""
from __future__ import annotations

from .hmce import HMCE  # alpha, 14D
from .amsc import AMSC  # alpha, 12D
from .mdns import MDNS  # alpha, 11D
from .amss import AMSS  # beta, 10D
from .tpio import TPIO  # beta, 10D
from .edta import EDTA  # beta, 11D
from .etam import ETAM  # beta, 10D
from .hgsic import HGSIC  # beta, 12D
from .oms import OMS  # beta, 10D
from .tmrm import TMRM  # gamma, 10D
from .newmd import NEWMD  # gamma, 10D
from .mtne import MTNE  # gamma, 10D
from .ptgmp import PTGMP  # gamma, 9D
from .mpfs import MPFS  # gamma, 9D

MODEL_CLASSES: list = [
    HMCE,
    AMSC,
    MDNS,
    AMSS,
    TPIO,
    EDTA,
    ETAM,
    HGSIC,
    OMS,
    TMRM,
    NEWMD,
    MTNE,
    PTGMP,
    MPFS,
]
