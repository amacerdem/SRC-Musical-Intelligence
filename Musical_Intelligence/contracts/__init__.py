"""MI Contracts — interfaces and value types for Musical Intelligence.

Re-exports all 8 frozen dataclasses and 5 abstract base classes that define
the contract layer for the entire system.
"""
from __future__ import annotations

from .bases import (
    BaseCognitiveUnit,
    BaseMechanism,
    BaseModel,
    BaseSemanticGroup,
    BaseSpectralGroup,
)
from .dataclasses import (
    BrainRegion,
    Citation,
    CrossUnitPathway,
    H3DemandSpec,
    LayerSpec,
    ModelMetadata,
    R3FeatureSpec,
    SemanticGroupOutput,
)

__all__ = [
    # Dataclasses (8)
    "BrainRegion",
    "Citation",
    "CrossUnitPathway",
    "H3DemandSpec",
    "LayerSpec",
    "ModelMetadata",
    "R3FeatureSpec",
    "SemanticGroupOutput",
    # ABCs (5)
    "BaseCognitiveUnit",
    "BaseMechanism",
    "BaseModel",
    "BaseSemanticGroup",
    "BaseSpectralGroup",
]
