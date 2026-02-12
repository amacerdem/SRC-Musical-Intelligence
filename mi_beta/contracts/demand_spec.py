"""
H3DemandSpec -- Typed declaration of a single H3 temporal demand.

Each cognitive model declares EXACTLY which H3 features it needs via a set of
H3DemandSpec instances.  Every spec maps to one scalar time series: a specific
R3 feature, observed through a specific temporal horizon, summarised by a
specific morphological statistic, and viewed under a specific causal law.

The 4-tuple (r3_idx, horizon, morph, law) is the canonical address in H3 space.
The remaining fields (names, purpose, citation) are metadata for auditability --
every demand must justify its existence with a scientific citation.

See also:
    mi.core.constants  -- MORPH_NAMES, LAW_NAMES, HORIZON_MS
    mi.ear.h3          -- DemandTree, HorizonEngine, MorphEngine
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class H3DemandSpec:
    """A single H3 temporal demand declared by a cognitive model.

    Attributes:
        r3_idx:        Index into the 49-D R3 feature vector (0-48).
        r3_name:       Human-readable name of the R3 feature (e.g. "stumpf_fusion").
        horizon:       Horizon index (0-31).  Maps to HORIZON_MS[horizon].
        horizon_label: Human-readable horizon label (e.g. "2s phrase").
        morph:         Morph index (0-23).  Maps to MORPH_NAMES[morph].
        morph_name:    Human-readable morph name (e.g. "value", "velocity").
        law:           Temporal law index (0-2): 0=memory, 1=prediction, 2=integration.
        law_name:      Human-readable law name (e.g. "memory", "prediction").
        purpose:       One-line description of WHY this demand exists in the model.
        citation:      Short-form citation justifying the demand (e.g. "Salimpoor 2011").
    """

    # ---- H3 address (the 4-tuple) ------------------------------------
    r3_idx: int
    r3_name: str
    horizon: int
    horizon_label: str
    morph: int
    morph_name: str
    law: int
    law_name: str

    # ---- Justification -----------------------------------------------
    purpose: str
    citation: str

    # ---- Helpers ------------------------------------------------------

    def as_tuple(self) -> Tuple[int, int, int, int]:
        """Return the canonical (r3_idx, horizon, morph, law) 4-tuple.

        This is the key used by H3Output.features and DemandTree.
        """
        return (self.r3_idx, self.horizon, self.morph, self.law)

    def __repr__(self) -> str:
        return (
            f"H3DemandSpec("
            f"r3={self.r3_idx}:{self.r3_name}, "
            f"H{self.horizon}:{self.horizon_label}, "
            f"M{self.morph}:{self.morph_name}, "
            f"L{self.law}:{self.law_name}, "
            f"cite={self.citation!r})"
        )
