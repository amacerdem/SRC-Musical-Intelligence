"""H3DemandSpec -- Temporal Demand Specification.

Each cognitive model declares which H3 features it needs via a set of
``H3DemandSpec`` instances. Every spec maps to one scalar time series:
a specific R3 feature, observed through a specific temporal horizon,
summarised by a specific morphological statistic, and viewed under a
specific causal law.

The canonical 4-tuple address is ``(r3_idx, horizon, morph, law)``.

Temporal law semantics:

    0  Memory       -- recent past via exponential decay
    1  Prediction   -- expected future from learned patterns
    2  Integration  -- combined memory + prediction (convolution)
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class H3DemandSpec:
    """Typed declaration of a single H3 temporal demand (4-tuple address).

    Attributes:
        r3_idx:        Index into the R3 feature vector.
        r3_name:       Human-readable name of the R3 feature.
        horizon:       Horizon index (0-31).
        horizon_label: Human-readable horizon label (e.g. ``"2s phrase"``).
        morph:         Morph index (0-23).
        morph_name:    Human-readable morph name (e.g. ``"velocity"``).
        law:           Temporal law index (0=memory, 1=prediction,
                       2=integration).
        law_name:      Human-readable law name (e.g. ``"memory"``).
        purpose:       One-line description of WHY this demand exists.
        citation:      Short-form citation justifying the demand.
    """

    # H3 Address (the 4-tuple)
    r3_idx: int
    r3_name: str
    horizon: int
    horizon_label: str
    morph: int
    morph_name: str
    law: int
    law_name: str

    # Justification
    purpose: str
    citation: str

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def as_tuple(self) -> tuple[int, int, int, int]:
        """Return the canonical ``(r3_idx, horizon, morph, law)`` 4-tuple.

        This is the key used by ``H3Output.features`` and ``DemandTree``.
        """
        return (self.r3_idx, self.horizon, self.morph, self.law)
