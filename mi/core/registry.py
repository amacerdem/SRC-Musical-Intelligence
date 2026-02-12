"""
MI Component Registry — Computes H³ demand from the MusicalBrain.

DemandAggregator computes the set of 4-tuple demands that H³ must extract.
"""

from __future__ import annotations

from typing import List, Set, Tuple


class DemandAggregator:
    """Computes the H³ demand set from the MusicalBrain.

    Demand format: 4-tuple (r3_idx, h, m, l) — per-R³ feature tracking.
    """

    @staticmethod
    def from_brain(brain) -> Set[Tuple[int, int, int, int]]:
        """Compute the H³ demand set from a MusicalBrain instance.

        Args:
            brain: MusicalBrain (or any object with .h3_demand property)

        Returns:
            Set of (r3_idx, horizon, morph, law) 4-tuples
        """
        return set(brain.h3_demand)

    @staticmethod
    def horizons_needed(demand: Set[Tuple[int, int, int, int]]) -> Set[int]:
        """Which horizons appear in the demand set."""
        return {h for _, h, _, _ in demand}
