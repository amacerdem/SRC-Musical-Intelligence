"""Shared dataclasses for the C3 cognitive architecture."""
from __future__ import annotations

from typing import Sequence, Tuple


class H3DemandSpec:
    """Specification for a single H3 temporal feature demand."""

    __slots__ = (
        "r3_idx", "r3_name", "horizon", "horizon_label",
        "morph", "morph_name", "law", "law_name",
        "purpose", "citation",
    )

    def __init__(
        self,
        r3_idx: int,
        r3_name: str,
        horizon: int,
        horizon_label: str,
        morph: int,
        morph_name: str,
        law: int,
        law_name: str,
        purpose: str,
        citation: str,
    ) -> None:
        self.r3_idx = r3_idx
        self.r3_name = r3_name
        self.horizon = horizon
        self.horizon_label = horizon_label
        self.morph = morph
        self.morph_name = morph_name
        self.law = law
        self.law_name = law_name
        self.purpose = purpose
        self.citation = citation

    def as_tuple(self) -> Tuple[int, int, int, int]:
        """Return the 4-tuple key ``(r3_idx, horizon, morph, law)``."""
        return (self.r3_idx, self.horizon, self.morph, self.law)

    def __repr__(self) -> str:
        return (
            f"H3DemandSpec({self.r3_name}[{self.r3_idx}], "
            f"H{self.horizon}, M{self.morph}, L{self.law})"
        )


class LayerSpec:
    """Specification for a mechanism output layer."""

    __slots__ = ("code", "name", "start", "end", "dims", "scope")

    def __init__(
        self,
        code: str,
        name: str,
        start: int,
        end: int,
        dims: Tuple[str, ...],
        *,
        scope: str = "internal",
    ) -> None:
        self.code = code
        self.name = name
        self.start = start
        self.end = end
        self.dims = dims
        self.scope = scope

    def __repr__(self) -> str:
        return f"LayerSpec({self.code}, {self.name}, [{self.start}:{self.end}])"


class RegionLink:
    """Link between a mechanism dimension and a brain region."""

    __slots__ = ("dim_name", "region", "weight", "citation")

    def __init__(
        self,
        dim_name: str,
        region: str,
        weight: float,
        citation: str,
    ) -> None:
        self.dim_name = dim_name
        self.region = region
        self.weight = weight
        self.citation = citation

    def __repr__(self) -> str:
        return f"RegionLink({self.dim_name} -> {self.region}, w={self.weight})"


class NeuroLink:
    """Link between a mechanism dimension and a neuromodulator."""

    __slots__ = ("dim_name", "modulator", "weight", "citation")

    def __init__(
        self,
        dim_name: str,
        modulator: str,
        weight: float,
        citation: str,
    ) -> None:
        self.dim_name = dim_name
        self.modulator = modulator
        self.weight = weight
        self.citation = citation

    def __repr__(self) -> str:
        return f"NeuroLink({self.dim_name} -> {self.modulator}, w={self.weight})"


class Citation:
    """Literature citation for a mechanism or belief."""

    __slots__ = ("author", "year", "description", "evidence")

    def __init__(
        self,
        author: str,
        year: int,
        description: str,
        evidence: str,
    ) -> None:
        self.author = author
        self.year = year
        self.description = description
        self.evidence = evidence

    def __repr__(self) -> str:
        return f"Citation({self.author} {self.year})"


class ModelMetadata:
    """Metadata for a mechanism model."""

    __slots__ = (
        "citations", "evidence_tier", "confidence_range",
        "falsification_criteria", "version",
    )

    def __init__(
        self,
        citations: Tuple[Citation, ...],
        evidence_tier: str,
        confidence_range: Tuple[float, float],
        falsification_criteria: Sequence[str],
        version: str,
    ) -> None:
        self.citations = citations
        self.evidence_tier = evidence_tier
        self.confidence_range = confidence_range
        self.falsification_criteria = falsification_criteria
        self.version = version

    def __repr__(self) -> str:
        return (
            f"ModelMetadata(tier={self.evidence_tier}, "
            f"v={self.version}, {len(self.citations)} citations)"
        )
