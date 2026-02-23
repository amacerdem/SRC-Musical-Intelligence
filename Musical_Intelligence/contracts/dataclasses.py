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


# -- Neurochemical channel constants ------------------------------------------
DA = 0        # Dopamine
NE = 1        # Norepinephrine
OPI = 2       # Opioid
_5HT = 3      # Serotonin
NUM_CHANNELS = 4


class NeuroLink:
    """Link between a mechanism dimension and a neuromodulator.

    Attributes:
        dim_name:  Name of the output dimension that drives the link.
        modulator: Neuromodulator name (e.g. "DA", "NE", "OPI", "5HT").
        weight:    Coupling strength (0-1).
        citation:  Literature reference.
        channel:   Integer index into the (B, T, 4) neuro tensor.
        effect:    One of ``"produce"``, ``"amplify"``, ``"inhibit"``.
    """

    __slots__ = ("dim_name", "modulator", "weight", "citation", "channel", "effect")

    _MODULATOR_TO_CHANNEL = {"DA": DA, "NE": NE, "OPI": OPI, "5HT": _5HT}

    def __init__(self, *args, **kwargs) -> None:
        """Accept both calling conventions:

        4-arg:  NeuroLink(dim_name, modulator, weight, citation)
        5-arg:  NeuroLink(dim_name, channel, effect, weight, citation)
        """
        if len(args) == 5 and isinstance(args[1], int):
            # 5-arg: (dim_name, channel, effect, weight, citation)
            self.dim_name = args[0]
            self.channel = args[1]
            self.effect = args[2]
            self.weight = args[3]
            self.citation = args[4]
            _ch_to_mod = {v: k for k, v in self._MODULATOR_TO_CHANNEL.items()}
            self.modulator = _ch_to_mod.get(self.channel, f"CH{self.channel}")
        elif len(args) >= 4:
            # 4-arg: (dim_name, modulator, weight, citation)
            self.dim_name = args[0]
            self.modulator = args[1]
            self.weight = args[2]
            self.citation = args[3]
            self.channel = kwargs.get("channel") or self._MODULATOR_TO_CHANNEL.get(str(self.modulator), 0)
            self.effect = kwargs.get("effect", "produce")
        else:
            # Kwargs-only or partial
            self.dim_name = kwargs.get("dim_name", args[0] if args else "")
            self.modulator = kwargs.get("modulator", args[1] if len(args) > 1 else "")
            self.weight = kwargs.get("weight", args[2] if len(args) > 2 else 0.0)
            self.citation = kwargs.get("citation", args[3] if len(args) > 3 else "")
            self.channel = kwargs.get("channel") or self._MODULATOR_TO_CHANNEL.get(str(self.modulator), 0)
            self.effect = kwargs.get("effect", "produce")

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


class CrossUnitPathway:
    """Cross-unit pathway connecting models in different functional units."""

    __slots__ = (
        "pathway_id", "name", "source_unit", "source_model",
        "source_dims", "target_unit", "target_model",
        "correlation", "citation",
    )

    def __init__(
        self,
        pathway_id: str,
        name: str,
        source_unit: str,
        source_model: str,
        source_dims: Tuple[str, ...],
        target_unit: str,
        target_model: str,
        correlation: str,
        citation: str,
    ) -> None:
        self.pathway_id = pathway_id
        self.name = name
        self.source_unit = source_unit
        self.source_model = source_model
        self.source_dims = source_dims
        self.target_unit = target_unit
        self.target_model = target_model
        self.correlation = correlation
        self.citation = citation

    def __repr__(self) -> str:
        return (
            f"CrossUnitPathway({self.source_unit}.{self.source_model} "
            f"-> {self.target_unit}.{self.target_model})"
        )


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
