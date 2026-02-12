"""
DemandAggregator -- Union all H3 demands from registered models.

Given a ModelRegistry, the DemandAggregator computes which H3 4-tuples
the ear/H3 subsystem must extract.  This drives selective computation:
H3 only calculates the temporal features that at least one active model
actually reads, rather than the full 2304D cartesian product.

Usage::

    from mi_beta.core.registry import ModelRegistry
    from mi_beta.core.demand_aggregator import DemandAggregator

    registry = ModelRegistry()
    registry.scan()

    demand = DemandAggregator.from_registry(registry)
    horizons = DemandAggregator.horizons_needed(demand)
    summary = DemandAggregator.demand_summary(registry)
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from .constants import HORIZON_MS, MORPH_NAMES, LAW_NAMES


class DemandAggregator:
    """Static utility for computing and analysing H3 demand sets.

    All methods are static -- no state is held.  The registry itself
    is the single source of truth for which models are active.
    """

    @staticmethod
    def from_registry(registry: "ModelRegistry") -> Set[Tuple[int, int, int, int]]:
        """Compute the union of all H3 demands from active models.

        This delegates to ``registry.get_total_demand()`` for the actual
        union computation, providing a convenient entry point that matches
        the mi/ DemandAggregator API shape.

        Args:
            registry: A scanned ModelRegistry instance.

        Returns:
            Set of (r3_idx, horizon, morph, law) 4-tuples.
        """
        return registry.get_total_demand()

    @staticmethod
    def horizons_needed(
        demand: Set[Tuple[int, int, int, int]],
    ) -> Set[int]:
        """Extract the set of horizon indices that appear in the demand.

        This tells the H3 engine which horizon buffers to maintain.
        Horizons not in this set can be skipped entirely.

        Args:
            demand: Set of (r3_idx, horizon, morph, law) 4-tuples.

        Returns:
            Set of horizon indices (0-31).
        """
        return {h for _, h, _, _ in demand}

    @staticmethod
    def r3_features_needed(
        demand: Set[Tuple[int, int, int, int]],
    ) -> Set[int]:
        """Extract the set of R3 feature indices that appear in the demand.

        Args:
            demand: Set of (r3_idx, horizon, morph, law) 4-tuples.

        Returns:
            Set of R3 feature indices (0-48).
        """
        return {r for r, _, _, _ in demand}

    @staticmethod
    def morphs_needed(
        demand: Set[Tuple[int, int, int, int]],
    ) -> Set[int]:
        """Extract the set of morph indices that appear in the demand.

        Args:
            demand: Set of (r3_idx, horizon, morph, law) 4-tuples.

        Returns:
            Set of morph indices (0-23).
        """
        return {m for _, _, m, _ in demand}

    @staticmethod
    def laws_needed(
        demand: Set[Tuple[int, int, int, int]],
    ) -> Set[int]:
        """Extract the set of law indices that appear in the demand.

        Args:
            demand: Set of (r3_idx, horizon, morph, law) 4-tuples.

        Returns:
            Set of law indices (0-2).
        """
        return {l for _, _, _, l in demand}

    @staticmethod
    def demand_by_horizon(
        demand: Set[Tuple[int, int, int, int]],
    ) -> Dict[int, List[Tuple[int, int, int, int]]]:
        """Group demand tuples by horizon index.

        Useful for the H3 engine to process demands in horizon order.

        Args:
            demand: Set of 4-tuples.

        Returns:
            Dict mapping horizon index to sorted list of tuples at that horizon.
        """
        by_h: Dict[int, List[Tuple[int, int, int, int]]] = {}
        for tup in demand:
            by_h.setdefault(tup[1], []).append(tup)
        for lst in by_h.values():
            lst.sort()
        return dict(sorted(by_h.items()))

    @staticmethod
    def demand_by_r3(
        demand: Set[Tuple[int, int, int, int]],
    ) -> Dict[int, List[Tuple[int, int, int, int]]]:
        """Group demand tuples by R3 feature index.

        Args:
            demand: Set of 4-tuples.

        Returns:
            Dict mapping R3 index to sorted list of tuples for that feature.
        """
        by_r: Dict[int, List[Tuple[int, int, int, int]]] = {}
        for tup in demand:
            by_r.setdefault(tup[0], []).append(tup)
        for lst in by_r.values():
            lst.sort()
        return dict(sorted(by_r.items()))

    @staticmethod
    def demand_summary(registry: "ModelRegistry") -> Dict[str, int]:
        """Summarise demand count per active model.

        Args:
            registry: A scanned ModelRegistry instance.

        Returns:
            Dict mapping model_name -> number of H3 4-tuples it demands.
            Sorted by model name.
        """
        summary: Dict[str, int] = {}
        for entry in registry.active_model_entries():
            demand = registry.get_model_demand(entry.name)
            summary[entry.name] = len(demand)
        return dict(sorted(summary.items()))

    @staticmethod
    def demand_report(
        demand: Set[Tuple[int, int, int, int]],
    ) -> str:
        """Generate a human-readable report of the demand set.

        Args:
            demand: Set of 4-tuples.

        Returns:
            Multi-line string describing each demand entry.
        """
        lines = [
            f"H3 Demand Report: {len(demand)} unique 4-tuples",
            f"  Horizons: {sorted(DemandAggregator.horizons_needed(demand))}",
            f"  R3 features: {sorted(DemandAggregator.r3_features_needed(demand))}",
            f"  Morphs: {sorted(DemandAggregator.morphs_needed(demand))}",
            f"  Laws: {sorted(DemandAggregator.laws_needed(demand))}",
            "",
        ]

        by_horizon = DemandAggregator.demand_by_horizon(demand)
        for h_idx, tuples in by_horizon.items():
            h_ms = HORIZON_MS[h_idx] if h_idx < len(HORIZON_MS) else "?"
            lines.append(f"  H{h_idx} ({h_ms}ms) -- {len(tuples)} demands:")
            for r3, h, m, l in tuples:
                m_name = MORPH_NAMES[m] if m < len(MORPH_NAMES) else f"M{m}"
                l_name = LAW_NAMES[l] if l < len(LAW_NAMES) else f"L{l}"
                lines.append(f"    R3[{r3}] M{m}:{m_name} L{l}:{l_name}")

        return "\n".join(lines)
