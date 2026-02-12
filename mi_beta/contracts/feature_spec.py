"""
R3FeatureSpec -- Registration record for a single R3 spectral feature.

R3 computes 49 spectral features per frame from the mel spectrogram, organised
into 5 groups (A-E: consonance, energy, timbre, change, interactions).  Each
feature occupies a fixed index in the 49-D R3 vector.

R3FeatureSpec is the registration dataclass: it names the feature, places it
in a group, assigns its index, and records the scientific basis.  Spectral
group implementations (BaseSpectralGroup subclasses) use these specs to
declare what they produce.

Models that read R3 features directly (e.g. da_nacc reads r3[3] stumpf_fusion)
can reference the spec by index or name for documentation and validation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class R3FeatureSpec:
    """Registration of a single R3 spectral feature.

    Attributes:
        name:        Canonical name (e.g. "stumpf_fusion", "loudness").
        group:       Parent spectral group (e.g. "consonance", "energy").
        index:       Position in the 49-D R3 vector (0-48).
        description: One-line description of what this feature measures.
        citation:    Primary citation (e.g. "Stumpf 1898", "Plomp & Levelt 1965").
        unit:        Physical unit if applicable (e.g. "dB", "Hz", "").
                     Empty string for dimensionless quantities.
    """

    name: str
    group: str
    index: int
    description: str
    citation: str
    unit: str = ""

    def __post_init__(self) -> None:
        if not (0 <= self.index < 49):
            raise ValueError(
                f"R3FeatureSpec {self.name!r}: index must be in [0, 48], "
                f"got {self.index}"
            )

    def __repr__(self) -> str:
        u = f" ({self.unit})" if self.unit else ""
        return (
            f"R3FeatureSpec(idx={self.index}, "
            f"{self.name!r}{u}, "
            f"group={self.group!r}, "
            f"cite={self.citation!r})"
        )
