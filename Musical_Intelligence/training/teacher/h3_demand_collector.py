"""H3DemandCollector -- Aggregates all H3 demands from 96 cognitive models.

Iterates all 9 cognitive units, collects every model's ``h3_demand`` property,
deduplicates the 4-tuples, and establishes a canonical ordering for conversion
between the sparse H3 dict representation and a dense ``(B, T, N)`` tensor
needed by the H3 auxiliary head.

Usage::

    collector = H3DemandCollector()
    demand_set = collector.demand_set        # Set of ~5210 4-tuples
    index_map  = collector.index_map         # {(r3,h,m,l) -> int}
    n_demands  = collector.n_demands         # ~5210
"""
from __future__ import annotations

from typing import Dict, FrozenSet, List, Set, Tuple

from Musical_Intelligence.brain.orchestrator import BrainOrchestrator


class H3DemandCollector:
    """Collects and canonically orders all H3 demands from all 96 C3 models.

    The canonical ordering is deterministic: 4-tuples are sorted
    lexicographically by ``(r3_idx, horizon, morph, law)`` so the same
    demand set always maps to the same dense tensor indices.

    Attributes:
        demand_set:  Deduplicated set of 4-tuples.
        demand_list: Sorted list of 4-tuples (canonical ordering).
        index_map:   Maps each 4-tuple to its dense index.
        n_demands:   Total number of unique demands.
    """

    def __init__(self) -> None:
        self._demand_set: Set[Tuple[int, int, int, int]] = set()
        self._demand_list: List[Tuple[int, int, int, int]] = []
        self._index_map: Dict[Tuple[int, int, int, int], int] = {}
        self._collect()

    # ------------------------------------------------------------------
    # Collection
    # ------------------------------------------------------------------

    def _collect(self) -> None:
        """Walk all units and models, collect h3_demand tuples."""
        orch = BrainOrchestrator()

        for unit_name in ("SPU", "STU", "IMU", "ASU", "NDU",
                          "MPU", "PCU", "ARU", "RPU"):
            unit = orch._units[unit_name]
            for model in unit.models:
                for spec in model.h3_demand:
                    self._demand_set.add(spec.as_tuple())

        # Sort lexicographically for deterministic ordering
        self._demand_list = sorted(self._demand_set)
        self._index_map = {t: i for i, t in enumerate(self._demand_list)}

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def demand_set(self) -> FrozenSet[Tuple[int, int, int, int]]:
        """Deduplicated set of all demanded 4-tuples."""
        return frozenset(self._demand_set)

    @property
    def demand_list(self) -> List[Tuple[int, int, int, int]]:
        """Canonically sorted list of demanded 4-tuples."""
        return list(self._demand_list)

    @property
    def index_map(self) -> Dict[Tuple[int, int, int, int], int]:
        """Maps each 4-tuple to its index in the dense tensor."""
        return dict(self._index_map)

    @property
    def n_demands(self) -> int:
        """Total number of unique H3 demands."""
        return len(self._demand_list)

    # ------------------------------------------------------------------
    # Per-unit statistics
    # ------------------------------------------------------------------

    def demands_per_unit(self) -> Dict[str, int]:
        """Return count of unique demands contributed by each unit."""
        orch = BrainOrchestrator()
        result: Dict[str, int] = {}

        for unit_name in ("SPU", "STU", "IMU", "ASU", "NDU",
                          "MPU", "PCU", "ARU", "RPU"):
            unit = orch._units[unit_name]
            unit_demands: Set[Tuple[int, int, int, int]] = set()
            for model in unit.models:
                for spec in model.h3_demand:
                    unit_demands.add(spec.as_tuple())
            result[unit_name] = len(unit_demands)

        return result

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"H3DemandCollector(n_demands={self.n_demands})"
