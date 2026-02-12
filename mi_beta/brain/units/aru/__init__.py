"""
ARU -- Affective Resonance Unit.

Re-exports the unit definition and all model classes for convenient access:

    from mi_beta.brain.units.aru import ARUUnit
    from mi_beta.brain.units.aru import SRP, AAC, VMM  # individual models
"""

from ._unit import ARUUnit
from .models import (
    AAC,
    ALL_ARU_MODELS,
    CLAM,
    CMAT,
    DAP,
    MAD,
    NEMAC,
    PUPF,
    SRP,
    TAR,
    VMM,
)

__all__ = [
    "ARUUnit",
    # Alpha
    "SRP",
    "AAC",
    "VMM",
    # Beta
    "PUPF",
    "CLAM",
    "MAD",
    "NEMAC",
    # Gamma
    "DAP",
    "CMAT",
    "TAR",
    # Registry
    "ALL_ARU_MODELS",
]
