"""
SPU -- Spectral Processing Unit.

Re-exports the unit definition and all model classes for convenient access:

    from mi_beta.brain.units.spu import SPUUnit
    from mi_beta.brain.units.spu import BCH, PSCL, PCCR  # individual models
"""

from ._unit import SPUUnit
from .models import (
    ALL_SPU_MODELS,
    BCH,
    ESME,
    MIAA,
    PCCR,
    PSCL,
    SDED,
    SDNPS,
    STAI,
    TSCP,
)

__all__ = [
    "SPUUnit",
    # Alpha
    "BCH",
    "PSCL",
    "PCCR",
    # Beta
    "STAI",
    "TSCP",
    "MIAA",
    # Gamma
    "SDNPS",
    "ESME",
    "SDED",
    # Registry
    "ALL_SPU_MODELS",
]
