"""Frozen dataclasses for the MI contracts layer.

Re-exports all 8 immutable value types used throughout Musical Intelligence.
"""
from __future__ import annotations

from .brain_region import BrainRegion
from .citation import Citation
from .demand_spec import H3DemandSpec
from .feature_spec import R3FeatureSpec
from .layer_spec import LayerSpec
from .model_metadata import ModelMetadata
from .pathway_spec import CrossUnitPathway
from .semantic_output import SemanticGroupOutput

__all__ = [
    "BrainRegion",
    "Citation",
    "CrossUnitPathway",
    "H3DemandSpec",
    "LayerSpec",
    "ModelMetadata",
    "R3FeatureSpec",
    "SemanticGroupOutput",
]
