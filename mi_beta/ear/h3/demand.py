"""DemandTree: sparse routing of H3 demands by horizon."""

from __future__ import annotations

from typing import Dict, Set, Tuple


class DemandTree:
    """Groups H3 demands by horizon for efficient batch computation."""

    @staticmethod
    def build(
        demand: Set[Tuple[int, int, int, int]]
    ) -> Dict[int, Set[Tuple[int, int, int]]]:
        """Group 4-tuples by horizon: {h: {(r3_idx, m, l), ...}}."""
        tree: Dict[int, Set[Tuple[int, int, int]]] = {}
        for r3_idx, h, m, l in demand:
            if h not in tree:
                tree[h] = set()
            tree[h].add((r3_idx, m, l))
        return tree

    @staticmethod
    def summary(demand: Set[Tuple[int, int, int, int]]) -> str:
        """Human-readable summary of H3 demand."""
        if not demand:
            return "Empty demand (0 tuples)"
        tree = DemandTree.build(demand)
        lines = [f"H3 Demand: {len(demand)} tuples across {len(tree)} horizons"]
        for h in sorted(tree.keys()):
            lines.append(f"  H{h}: {len(tree[h])} triples")
        return "\n".join(lines)
