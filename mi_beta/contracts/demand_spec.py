"""H3DemandSpec: temporal demand specification for cognitive models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class H3DemandSpec:
    r3_idx: int                  # [0-48]
    r3_name: str                 # human-readable R3 feature name
    horizon: int                 # [0-31]
    horizon_label: str           # e.g., "200ms beat"
    morph: int                   # [0-23]
    morph_name: str              # e.g., "velocity"
    law: int                     # [0-2]
    law_name: str                # "memory" / "prediction" / "integration"
    purpose: str                 # WHY this demand exists
    citation: str                # justifying paper

    def as_tuple(self) -> Tuple[int, int, int, int]:
        return (self.r3_idx, self.horizon, self.morph, self.law)
