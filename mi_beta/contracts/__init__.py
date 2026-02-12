"""
MI-Beta Contracts -- Abstract base classes and specification types.

All domain contracts live here so that layers (ear, brain, language)
can depend on contracts without depending on each other.  This is the
foundational dependency -- every other mi_beta module imports from here.

Hierarchy:
    Dataclasses (no dependencies):
        H3DemandSpec, R3FeatureSpec, LayerSpec, CrossUnitPathway,
        BrainRegion, NeurochemicalType, NeurochemicalState,
        ModelMetadata, Citation, SemanticGroupOutput

    ABCs (depend on dataclasses above):
        BaseMechanism   -- model-internal sub-computation
        BaseModel       -- cognitive model (THE central contract)
        BaseCognitiveUnit -- unit grouping related models
        BaseSpectralGroup -- R3 spectral feature group
        BaseSemanticGroup -- L3 semantic interpretation group
"""

from __future__ import annotations

# ── Specification dataclasses ──────────────────────────────────────────
from .brain_region import BrainRegion
from .demand_spec import H3DemandSpec
from .feature_spec import R3FeatureSpec
from .layer_spec import LayerSpec
from .model_metadata import Citation, ModelMetadata
from .neurochemical import NeurochemicalState, NeurochemicalType
from .pathway_spec import CrossUnitPathway

# ── Abstract base classes ──────────────────────────────────────────────
from .base_mechanism import BaseMechanism
from .base_model import BaseModel
from .base_semantic_group import BaseSemanticGroup, SemanticGroupOutput
from .base_spectral_group import BaseSpectralGroup
from .base_unit import BaseCognitiveUnit

__all__ = [
    # Specification dataclasses
    "BrainRegion",
    "Citation",
    "CrossUnitPathway",
    "H3DemandSpec",
    "LayerSpec",
    "ModelMetadata",
    "NeurochemicalState",
    "NeurochemicalType",
    "R3FeatureSpec",
    "SemanticGroupOutput",
    # Abstract base classes
    "BaseMechanism",
    "BaseModel",
    "BaseCognitiveUnit",
    "BaseSemanticGroup",
    "BaseSpectralGroup",
]
