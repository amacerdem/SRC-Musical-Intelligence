"""Frozen dataclasses for the MI contracts layer.

Re-exports all immutable value types used throughout Musical Intelligence.
"""
from __future__ import annotations

from .brain_output import BrainOutput, PsiState
from .brain_region import BrainRegion
from .citation import Citation
from .demand_spec import H3DemandSpec
from .feature_spec import R3FeatureSpec
from .layer_spec import LayerSpec
from .model_metadata import ModelMetadata
from .neuro_link import NeuroLink
from .pathway_spec import CrossUnitPathway
from .region_link import RegionLink
from .semantic_output import SemanticGroupOutput

__all__ = [
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
]
