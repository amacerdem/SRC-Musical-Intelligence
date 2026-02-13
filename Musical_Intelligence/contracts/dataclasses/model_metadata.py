"""ModelMetadata -- Evidence provenance, confidence, and falsification criteria.

Every ``BaseModel`` must declare its scientific grounding via
``ModelMetadata``. This enables systematic evidence auditing: which papers
support which dimensions, what is the overall confidence, and what would
falsify the model.

Evidence tiers:

    alpha   Mechanistic    >90% confidence,  k >= 10 studies
    beta    Correlational  >70% confidence,  5 <= k < 10
    gamma   Exploratory    <70% confidence,  k < 5
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .citation import Citation


_VALID_TIERS = frozenset({"alpha", "beta", "gamma"})


@dataclass(frozen=True)
class ModelMetadata:
    """Evidence provenance and confidence metadata for a cognitive model.

    Attributes:
        citations:              All supporting citations.
        evidence_tier:          ``"alpha"``, ``"beta"``, or ``"gamma"``.
        confidence_range:       ``(low, high)`` bounds as fractions in
                                ``[0, 1]``.
        falsification_criteria: What empirical results would invalidate this
                                model; at least one required (Popper 1959).
        version:                Semantic version string of the model spec.
        paper_count:            Number of unique papers. Auto-computed from
                                citations if not set.
    """

    citations: tuple[Citation, ...]
    evidence_tier: str
    confidence_range: tuple[float, float]
    falsification_criteria: tuple[str, ...]
    version: str = "1.0.0"
    paper_count: Optional[int] = None

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        # 1. evidence_tier must be valid
        if self.evidence_tier not in _VALID_TIERS:
            raise ValueError(
                f"ModelMetadata: evidence_tier must be one of "
                f"{sorted(_VALID_TIERS)}, got {self.evidence_tier!r}"
            )

        # 2. confidence_range must satisfy 0 <= low <= high <= 1
        low, high = self.confidence_range
        if not (0 <= low <= high <= 1):
            raise ValueError(
                f"ModelMetadata: confidence_range must satisfy "
                f"0 <= low <= high <= 1, got ({low}, {high})"
            )

        # 3. falsification_criteria must be non-empty (Popper 1959)
        if len(self.falsification_criteria) == 0:
            raise ValueError(
                "ModelMetadata: falsification_criteria must be non-empty -- "
                "every scientific model must be falsifiable (Popper 1959)"
            )

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def effective_paper_count(self) -> int:
        """Number of unique papers.

        Uses explicit ``paper_count`` if set; otherwise counts unique
        ``(author, year)`` pairs from ``citations``.
        """
        if self.paper_count is not None:
            return self.paper_count
        return len({(c.author, c.year) for c in self.citations})

    @property
    def is_mechanistic(self) -> bool:
        """``True`` if ``evidence_tier == "alpha"``."""
        return self.evidence_tier == "alpha"
