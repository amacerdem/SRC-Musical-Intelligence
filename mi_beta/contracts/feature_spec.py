"""R3FeatureSpec: spectral feature specification."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class R3FeatureSpec:
    name: str                    # "roughness"
    group: str                   # "consonance"
    index: int                   # global index in R3 vector
    domain: str = ""             # "psychoacoustic", "dsp", "cross_domain"
    description: str = ""
