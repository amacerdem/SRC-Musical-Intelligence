"""CrossUnitPathway -- Directed data dependency between cognitive units.

Declares a data dependency from a source model in one cognitive unit to a
target model in another (or the same) unit. Used by the pipeline for
topological sorting of unit execution order and by auditors for tracing
data flows to scientific citations.

This dataclass does NOT carry data -- it describes the contract that a
source model promises to fulfill and a target model depends on.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CrossUnitPathway:
    """A directed data dependency between models in cognitive units.

    Attributes:
        pathway_id:   Unique identifier (e.g.
                      ``"ARU_SRP__SPU_STAI__arousal"``).
        name:         Human-readable pathway name.
        source_unit:  Source cognitive unit name (e.g. ``"ARU"``).
        source_model: Source model name within that unit (e.g. ``"SRP"``).
        source_dims:  Dimension names provided by the source (e.g.
                      ``("arousal", "prediction_error")``).
        target_unit:  Target cognitive unit name (e.g. ``"SPU"``).
        target_model: Target model name within that unit (e.g. ``"STAI"``).
        correlation:  Expected correlation strength from literature (e.g.
                      ``"r=0.71"``). Empty string if theoretical.
        citation:     Scientific citation justifying this pathway.
    """

    pathway_id: str
    name: str
    source_unit: str
    source_model: str
    source_dims: tuple[str, ...]
    target_unit: str
    target_model: str
    correlation: str
    citation: str

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def is_intra_unit(self) -> bool:
        """``True`` if source and target are in the same cognitive unit."""
        return self.source_unit == self.target_unit

    @property
    def is_inter_unit(self) -> bool:
        """``True`` if source and target are in different cognitive units."""
        return self.source_unit != self.target_unit

    @property
    def edge(self) -> tuple[str, str]:
        """``(source_unit, target_unit)`` for dependency graph construction."""
        return (self.source_unit, self.target_unit)
