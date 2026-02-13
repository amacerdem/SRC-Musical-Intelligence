"""R3 Feature Registry sub-package.

Exports:
    R3FeatureRegistry   -- Mutable builder that collects spectral groups.
    R3FeatureMap        -- Frozen read-only snapshot produced by freeze().
    R3GroupInfo         -- Per-group metadata (name, dim, start, end, features).
    auto_discover_groups -- Scan ear/r3/groups/ for BaseSpectralGroup subclasses.
"""
from __future__ import annotations

from .auto_discovery import auto_discover_groups
from .feature_map import R3FeatureMap, R3GroupInfo
from .feature_registry import R3FeatureRegistry

__all__ = [
    "R3FeatureRegistry",
    "R3FeatureMap",
    "R3GroupInfo",
    "auto_discover_groups",
]
