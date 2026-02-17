"""DemandTree -- Sparse routing for H3 demand sets.

Reorganises a flat set of 4-tuples into a horizon-keyed dictionary so that
the H3Extractor can compute attention weights once per horizon and reuse
them across all tuples sharing that horizon.  This is a pure data-structure
utility with no learnable parameters or state.

Source of truth
---------------
- Docs/H3/Contracts/DemandTree.md          build() interface, invariants
- Docs/H3/H3-TEMPORAL-ARCHITECTURE.md      Section 9: demand routing
- Docs/H3/Registry/DemandAddressSpace.md   sparsity analysis
"""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Set, Tuple

# ---------------------------------------------------------------------------
# Range bounds for the 4-tuple address axes
# ---------------------------------------------------------------------------
_R3_IDX_MAX = 96       # 97 R3 features  [0, 96]
_HORIZON_MAX = 31      # 32 horizons       [0, 31]
_MORPH_MAX = 23        # 24 morphs         [0, 23]
_LAW_MAX = 2           # 3 laws            [0, 2]


def _validate_tuple(t: Tuple[int, int, int, int]) -> None:
    """Raise ``ValueError`` if any element in the 4-tuple is out of range."""
    r3_idx, horizon, morph, law = t

    if not (0 <= r3_idx <= _R3_IDX_MAX):
        raise ValueError(
            f"r3_idx must be in [0, {_R3_IDX_MAX}], got {r3_idx} "
            f"in tuple {t}"
        )
    if not (0 <= horizon <= _HORIZON_MAX):
        raise ValueError(
            f"horizon must be in [0, {_HORIZON_MAX}], got {horizon} "
            f"in tuple {t}"
        )
    if not (0 <= morph <= _MORPH_MAX):
        raise ValueError(
            f"morph must be in [0, {_MORPH_MAX}], got {morph} "
            f"in tuple {t}"
        )
    if not (0 <= law <= _LAW_MAX):
        raise ValueError(
            f"law must be in [0, {_LAW_MAX}], got {law} "
            f"in tuple {t}"
        )


class DemandTree:
    """Stateless grouping of H3 demand 4-tuples by horizon index.

    All methods are static -- ``DemandTree`` carries no instance state.

    Transformation::

        Input:  {(r3_idx, horizon, morph, law), ...}
                       |
                       v
        Output: {horizon: {(r3_idx, morph, law), ...}}

    The horizon index is extracted as the dictionary key.  The remaining
    three elements ``(r3_idx, morph, law)`` are stored as a 3-tuple in the
    set for that horizon.
    """

    # ------------------------------------------------------------------
    # build
    # ------------------------------------------------------------------

    @staticmethod
    def build(
        demand: Set[Tuple[int, int, int, int]],
    ) -> Dict[int, Set[Tuple[int, int, int]]]:
        """Group demand 4-tuples by horizon.

        Parameters
        ----------
        demand:
            Set of ``(r3_idx, horizon, morph, law)`` 4-tuples.  Duplicates
            are inherently impossible (set semantics).

        Returns
        -------
        Dict mapping each unique horizon index to the set of
        ``(r3_idx, morph, law)`` 3-tuples demanded at that horizon.

        Raises
        ------
        ValueError
            If any element in any 4-tuple is outside the valid range.

        Invariants
        ----------
        - Every 4-tuple in the input appears exactly once in the output
          (as a 3-tuple under its horizon key).
        - The union of all 3-tuples across all horizon keys reconstructs
          the original demand set (with horizon re-added).
        - ``build(set()) == {}``.
        """
        if not demand:
            return {}

        tree: Dict[int, Set[Tuple[int, int, int]]] = defaultdict(set)

        for t in demand:
            _validate_tuple(t)
            r3_idx, horizon, morph, law = t
            tree[horizon].add((r3_idx, morph, law))

        return dict(tree)

    # ------------------------------------------------------------------
    # summary
    # ------------------------------------------------------------------

    @staticmethod
    def summary(
        demand: Set[Tuple[int, int, int, int]],
    ) -> dict:
        """Return statistics describing the demand set structure.

        Parameters
        ----------
        demand:
            Set of ``(r3_idx, horizon, morph, law)`` 4-tuples.

        Returns
        -------
        dict with keys:
            ``total_tuples``       -- number of unique 4-tuples
            ``unique_horizons``    -- number of distinct horizon indices
            ``per_horizon_counts`` -- ``{horizon_idx: count}`` mapping

        Raises
        ------
        ValueError
            If any element in any 4-tuple is outside the valid range.
        """
        if not demand:
            return {
                "total_tuples": 0,
                "unique_horizons": 0,
                "per_horizon_counts": {},
            }

        tree = DemandTree.build(demand)

        per_horizon_counts = {h: len(rml) for h, rml in sorted(tree.items())}

        return {
            "total_tuples": len(demand),
            "unique_horizons": len(tree),
            "per_horizon_counts": per_horizon_counts,
        }
