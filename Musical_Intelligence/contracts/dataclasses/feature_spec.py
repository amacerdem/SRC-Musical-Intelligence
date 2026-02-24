"""R3FeatureSpec — per-feature metadata for the R³ feature vector."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class R3FeatureSpec:
    """Metadata for a single R³ feature dimension.

    Attributes:
        name:        Canonical feature name (e.g. ``"stumpf_fusion"``).
        group:       GROUP_NAME of the owning spectral group.
        index:       Position in the R³ feature vector.
        description: Human-readable description of the feature.
        citation:    Literature reference.
    """

    name: str
    group: str
    index: int
    description: str = ""
    citation: str = ""

    def __repr__(self) -> str:
        return f"R3FeatureSpec({self.name!r}, group={self.group!r}, idx={self.index})"
