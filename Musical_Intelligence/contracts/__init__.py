"""MI Contracts — interfaces and value types for Musical Intelligence.

Re-exports frozen dataclasses and abstract base classes that define
the contract layer for the entire system.
"""
from __future__ import annotations

from .bases import (
    Associator,
    BaseModel,
    BaseSemanticGroup,
    BaseSpectralGroup,
    Encoder,
    Hub,
    Integrator,
    Nucleus,
    Relay,
)
from .dataclasses import (
    BrainOutput,
    BrainRegion,
    Citation,
    CrossUnitPathway,
    H3DemandSpec,
    LayerSpec,
    ModelMetadata,
    NeuroLink,
    PsiState,
    R3FeatureSpec,
    RegionLink,
    SemanticGroupOutput,
)

__all__ = [
    # Dataclasses
    "BrainOutput",
    "BrainRegion",
    "Citation",
    "CrossUnitPathway",
    "H3DemandSpec",
    "LayerSpec",
    "ModelMetadata",
    "NeuroLink",
    "PsiState",
    "R3FeatureSpec",
    "RegionLink",
    "SemanticGroupOutput",
    # ABCs
    "BaseModel",
    "BaseSemanticGroup",
    "BaseSpectralGroup",
    # Nucleus hierarchy
    "Associator",
    "Encoder",
    "Hub",
    "Integrator",
    "Nucleus",
    "Relay",
]
