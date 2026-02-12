"""
CrossUnitPathway -- Declaration of a data dependency between cognitive units.

In the mi_beta architecture, cognitive units (ARU, SPU, STU, IMU, etc.) are
NOT fully independent.  Some models within one unit read outputs from models
in another unit.  For example:

    ARU's autonomic model reads SPU's arousal signal.
    IMU's familiarity model reads ARU's prediction error.

These cross-unit dependencies must be declared explicitly so that:
    1. The pipeline can topologically sort unit execution order.
    2. The demand aggregator knows which units must run first.
    3. Auditors can trace every data flow to a scientific citation.

CrossUnitPathway is the declaration record.  It does NOT carry data -- it
describes the contract that a source model promises to fulfill and a target
model depends on.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CrossUnitPathway:
    """Declaration of a directed data dependency between two models in
    different (or the same) cognitive units.

    Attributes:
        pathway_id:   Unique identifier (e.g. "ARU_SRP__SPU_STAI__arousal").
        name:         Human-readable pathway name (e.g. "Arousal -> Spectral Gating").
        source_unit:  Source cognitive unit name (e.g. "ARU").
        source_model: Source model name within that unit (e.g. "SRP").
        source_dims:  Tuple of dimension names or indices provided by the source.
                      E.g. ("arousal", "prediction_error") or (0, 1).
        target_unit:  Target cognitive unit name (e.g. "SPU").
        target_model: Target model name within that unit (e.g. "STAI").
        correlation:  Expected correlation strength from literature.
                      E.g. "r=0.71" or "d=0.53".  Empty string if theoretical.
        citation:     Scientific citation justifying this pathway.
    """

    pathway_id: str
    name: str
    source_unit: str
    source_model: str
    source_dims: Tuple[str, ...]
    target_unit: str
    target_model: str
    correlation: str
    citation: str

    @property
    def is_intra_unit(self) -> bool:
        """True if source and target are in the same cognitive unit."""
        return self.source_unit == self.target_unit

    @property
    def is_inter_unit(self) -> bool:
        """True if source and target are in different cognitive units."""
        return self.source_unit != self.target_unit

    @property
    def edge(self) -> Tuple[str, str]:
        """Return (source_unit, target_unit) for dependency graph construction."""
        return (self.source_unit, self.target_unit)

    def __repr__(self) -> str:
        dims = ", ".join(self.source_dims) if self.source_dims else "all"
        return (
            f"CrossUnitPathway("
            f"{self.source_unit}.{self.source_model}[{dims}] "
            f"-> {self.target_unit}.{self.target_model}, "
            f"{self.correlation}, {self.citation!r})"
        )
