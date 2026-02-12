"""
ModelMetadata / Citation -- Evidence provenance for cognitive models.

Every BaseModel must declare its scientific grounding via ModelMetadata.
This enables systematic evidence auditing: which papers support which
dimensions, what is the overall confidence, and what would falsify the model.

Evidence tiers follow the C3 meta-analysis framework:
    alpha  -- Mechanistic: >90% confidence, k >= 10 studies, pooled d or r.
    beta   -- Correlational: >70% confidence, 5 <= k < 10 studies.
    gamma  -- Exploratory: <70% confidence, k < 5 studies, theoretical.

Citation captures a single empirical finding with its effect size.  This is
NOT a bibliography entry -- it is a specific CLAIM from a specific study
that supports a specific dimension or mechanism in the model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass(frozen=True)
class Citation:
    """A single empirical finding supporting a model dimension or mechanism.

    Attributes:
        author:      First author last name (e.g. "Salimpoor").
        year:        Publication year.
        finding:     One-line summary of the relevant finding.
        effect_size: Reported effect size as a string (e.g. "r=0.84",
                     "d=0.67", "F(2,39)=15.48", "t=5.1").  Empty string
                     if not applicable (theoretical papers).
    """

    author: str
    year: int
    finding: str
    effect_size: str = ""

    @property
    def short_ref(self) -> str:
        """Short-form reference: 'Author YEAR'."""
        return f"{self.author} {self.year}"

    def __repr__(self) -> str:
        es = f", {self.effect_size}" if self.effect_size else ""
        return f"Citation({self.author} {self.year}{es})"


@dataclass(frozen=True)
class ModelMetadata:
    """Evidence provenance and confidence metadata for a cognitive model.

    Attributes:
        citations:             Tuple of all supporting citations.
        evidence_tier:         "alpha", "beta", or "gamma" (see module docstring).
        confidence_range:      (low, high) confidence bounds as fractions in [0, 1].
                               E.g. (0.90, 0.98) for a well-supported alpha model.
        falsification_criteria: Tuple of strings describing what empirical results
                               would invalidate this model.  Every model MUST declare
                               at least one falsification criterion (Popper 1959).
        version:               Semantic version string of the model spec
                               (e.g. "4.0.0").
        paper_count:           Number of unique papers supporting this model.
                               Computed from citations or set explicitly if some
                               citations share the same paper.
    """

    citations: Tuple[Citation, ...]
    evidence_tier: str
    confidence_range: Tuple[float, float]
    falsification_criteria: Tuple[str, ...]
    version: str = "1.0.0"
    paper_count: Optional[int] = None

    def __post_init__(self) -> None:
        valid_tiers = ("alpha", "beta", "gamma")
        if self.evidence_tier not in valid_tiers:
            raise ValueError(
                f"ModelMetadata: evidence_tier must be one of {valid_tiers}, "
                f"got {self.evidence_tier!r}"
            )
        low, high = self.confidence_range
        if not (0.0 <= low <= high <= 1.0):
            raise ValueError(
                f"ModelMetadata: confidence_range must satisfy "
                f"0 <= low <= high <= 1, got ({low}, {high})"
            )
        if not self.falsification_criteria:
            raise ValueError(
                "ModelMetadata: at least one falsification criterion is required. "
                "Every scientific model must be falsifiable."
            )

    @property
    def effective_paper_count(self) -> int:
        """Number of unique papers.  Uses explicit paper_count if set,
        otherwise falls back to counting unique (author, year) pairs."""
        if self.paper_count is not None:
            return self.paper_count
        unique = {(c.author, c.year) for c in self.citations}
        return len(unique)

    @property
    def is_mechanistic(self) -> bool:
        """True if the model has alpha-tier (mechanistic) evidence."""
        return self.evidence_tier == "alpha"

    def __repr__(self) -> str:
        lo, hi = self.confidence_range
        return (
            f"ModelMetadata(tier={self.evidence_tier}, "
            f"confidence=[{lo:.0%}-{hi:.0%}], "
            f"papers={self.effective_paper_count}, "
            f"v{self.version})"
        )
