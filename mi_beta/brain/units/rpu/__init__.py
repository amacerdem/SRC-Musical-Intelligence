"""
RPU -- Reward Processing Unit.

Re-exports the unit definition and all model classes for convenient access:

    from mi_beta.brain.units.rpu import RPUUnit
    from mi_beta.brain.units.rpu import DAED, MORMR, RPEM  # individual models
"""

from ._unit import RPUUnit
from .models import (
    ALL_RPU_MODELS,
    DAED,
    IOTMS,
    IUCP,
    LDAC,
    MCCN,
    MEAMR,
    MORMR,
    RPEM,
    SSPS,
)

__all__ = [
    "RPUUnit",
    # Alpha
    "DAED",
    "MORMR",
    "RPEM",
    # Beta
    "IUCP",
    "MCCN",
    "MEAMR",
    # Gamma
    "LDAC",
    "IOTMS",
    "SSPS",
    # Registry
    "ALL_RPU_MODELS",
]
