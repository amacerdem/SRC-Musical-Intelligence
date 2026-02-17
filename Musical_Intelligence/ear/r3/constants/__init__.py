from __future__ import annotations

from .domain_map import R3Domain, R3_DOMAIN_MAP
from .feature_names import R3_DIM, R3_FEATURE_NAMES
from .group_boundaries import (
    R3GroupBoundary,
    R3_GROUP_BOUNDARIES,
    R3_CONSONANCE,
    R3_ENERGY,
    R3_TIMBRE,
    R3_CHANGE,
    R3_PITCH_CHROMA,
    R3_RHYTHM_GROOVE,
    R3_HARMONY_TONALITY,
    R3_TIMBRE_EXTENDED,
    R3_MODULATION_PSYCHO,
)
from .quality_tiers import QualityTier, R3_QUALITY_TIERS

__all__ = [
    "R3_DIM",
    "R3_FEATURE_NAMES",
    "R3GroupBoundary",
    "R3_GROUP_BOUNDARIES",
    "R3_CONSONANCE",
    "R3_ENERGY",
    "R3_TIMBRE",
    "R3_CHANGE",
    "R3_PITCH_CHROMA",
    "R3_RHYTHM_GROOVE",
    "R3_HARMONY_TONALITY",
    "R3_TIMBRE_EXTENDED",
    "R3_MODULATION_PSYCHO",
    "QualityTier",
    "R3_QUALITY_TIERS",
    "R3Domain",
    "R3_DOMAIN_MAP",
]
