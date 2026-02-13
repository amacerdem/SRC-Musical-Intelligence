"""Citation and ModelMetadata: evidence provenance for cognitive models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Citation:
    author: str                  # "Bidelman"
    year: int                    # 2009
    finding: str                 # one-line summary
    effect_size: str = ""        # "r=0.84", "d=0.67", etc.

    @property
    def short_ref(self) -> str:
        return f"{self.author} {self.year}"


@dataclass(frozen=True)
class ModelMetadata:
    citations: Tuple[Citation, ...]
    evidence_tier: str           # "alpha" / "beta" / "gamma"
    confidence_range: Tuple[float, float]  # (low, high) in [0, 1]
    falsification_criteria: Tuple[str, ...]
    version: str = "1.0.0"
    paper_count: Optional[int] = None

    @property
    def effective_paper_count(self) -> int:
        if self.paper_count is not None:
            return self.paper_count
        return len(self.citations)

    @property
    def is_mechanistic(self) -> bool:
        return self.evidence_tier == "alpha"
