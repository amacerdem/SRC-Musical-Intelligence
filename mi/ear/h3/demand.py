"""
DemandTree — Sparse computation routing for H³.

Organizes (r3_idx, horizon, morph, law) demands into a tree structure
so H³ only computes what the MusicalBrain actually needs.
"""

from __future__ import annotations

from typing import Dict, Set, Tuple


class DemandTree:
    """Organizes H³ demands by horizon for efficient computation."""

    @staticmethod
    def build(
        demand: Set[Tuple[int, int, int, int]],
    ) -> Dict[int, Set[Tuple[int, int, int]]]:
        """Build a demand tree: horizon → {(r3_idx, morph, law), ...}.

        Args:
            demand: set of (r3_idx, horizon, morph, law) 4-tuples

        Returns:
            Dict mapping horizon index to set of (r3_idx, morph, law) triples
        """
        tree: Dict[int, Set[Tuple[int, int, int]]] = {}
        for r3_idx, h, m, l in demand:
            if h not in tree:
                tree[h] = set()
            tree[h].add((r3_idx, m, l))
        return tree

    @staticmethod
    def summary(demand: Set[Tuple[int, int, int, int]]) -> str:
        """Human-readable summary of demand."""
        tree = DemandTree.build(demand)
        lines = [f"H³ Demand: {len(demand)} tuples across {len(tree)} horizons"]
        for h in sorted(tree.keys()):
            triples = tree[h]
            lines.append(f"  H{h}: {len(triples)} (r3, morph, law) triples")
        return "\n".join(lines)
