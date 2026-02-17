"""R3FeatureSpec -- Per-feature metadata for R3 spectral feature registration.

Registration record for a single R3 spectral feature. Names the feature,
places it in a group, assigns its index, and records the scientific basis.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class R3FeatureSpec:
    """Registration of a single R3 spectral feature.

    Attributes:
        name:        Canonical name (e.g. ``"stumpf_fusion"``, ``"loudness"``).
        group:       Parent spectral group (e.g. ``"consonance"``, ``"energy"``).
        index:       Position in the R3 feature vector. Valid range is
                     ``[0, 96]`` (97 features, v2).
        description: One-line description of what this feature measures.
        citation:    Primary citation (e.g. ``"Stumpf 1898"``).
        unit:        Physical unit if applicable (e.g. ``"dB"``, ``"Hz"``).
                     Empty string for dimensionless quantities.
    """

    name: str
    group: str
    index: int
    description: str
    citation: str
    unit: str = ""

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        if not (0 <= self.index < 128):
            raise ValueError(
                f"R3FeatureSpec {self.name!r}: index must be in [0, 127], "
                f"got {self.index}"
            )

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        u = f" ({self.unit})" if self.unit else ""
        return (
            f"R3FeatureSpec(idx={self.index}, "
            f"{self.name!r}{u}, "
            f"group={self.group!r}, "
            f"cite={self.citation!r})"
        )
