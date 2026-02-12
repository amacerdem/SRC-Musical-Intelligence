"""
STU -- Sensorimotor Timing Unit.

Re-exports the unit definition and all model classes for convenient access:

    from mi_beta.brain.units.stu import STUUnit
    from mi_beta.brain.units.stu import HMCE, AMSC, MDNS  # individual models
"""

from ._unit import STUUnit
from .models import (
    ALL_STU_MODELS,
    AMSC,
    AMSS,
    EDTA,
    ETAM,
    HGSIC,
    HMCE,
    MDNS,
    MPFS,
    MTNE,
    NEWMD,
    OMS,
    PTGMP,
    TMRM,
    TPIO,
)

__all__ = [
    "STUUnit",
    # Alpha
    "HMCE",
    "AMSC",
    "MDNS",
    # Beta
    "AMSS",
    "TPIO",
    "EDTA",
    "ETAM",
    "HGSIC",
    "OMS",
    # Gamma
    "TMRM",
    "NEWMD",
    "MTNE",
    "PTGMP",
    "MPFS",
    # Registry
    "ALL_STU_MODELS",
]
