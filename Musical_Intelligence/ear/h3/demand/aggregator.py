"""Demand aggregation -- collect, deduplicate, and analyse H3 demands.

Provides two public functions:

- ``aggregate_demands``  -- collect H3DemandSpec instances from an iterable
  of model objects, deduplicate into a set of 4-tuples, and build a
  ``DemandTree`` grouped by horizon.
- ``demand_statistics``  -- compute summary statistics (per-horizon counts,
  per-band counts, sparsity vs 294,912 theoretical space) for a raw
  demand set.

Source of truth
---------------
- Docs/H3/H3-TEMPORAL-ARCHITECTURE.md      Section 9: aggregation pipeline
- Docs/H3/Registry/DemandAddressSpace.md   sparsity analysis
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Dict, Iterable, Set, Tuple

from ..constants.horizons import BAND_ASSIGNMENTS
from .demand_tree import DemandTree

# ---------------------------------------------------------------------------
# Theoretical address space  (128 * 32 * 24 * 3)
# ---------------------------------------------------------------------------
_THEORETICAL_SPACE = 294_912


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def aggregate_demands(
    models: Iterable[Any],
) -> Dict[int, Set[Tuple[int, int, int]]]:
    """Collect all H3 demands from *models*, deduplicate, and group by horizon.

    Each model is expected to expose an ``h3_demand`` property that returns a
    tuple (or iterable) of ``H3DemandSpec`` instances.  The canonical 4-tuple
    ``(r3_idx, horizon, morph, law)`` is extracted via ``spec.as_tuple()``
    for every spec across all models, deduplicated into a set, and finally
    organised into a ``DemandTree`` (horizon-keyed dictionary).

    Expected aggregate volume: ~8,600 unique tuples from 96 models.

    Parameters
    ----------
    models:
        Iterable of objects with an ``h3_demand`` property returning
        ``Tuple[H3DemandSpec, ...]``.

    Returns
    -------
    Dict mapping each unique horizon index to the set of
    ``(r3_idx, morph, law)`` 3-tuples demanded at that horizon --
    the output of ``DemandTree.build()``.
    """
    demand_set: Set[Tuple[int, int, int, int]] = set()

    for model in models:
        for spec in model.h3_demand:
            demand_set.add(spec.as_tuple())

    return DemandTree.build(demand_set)


def demand_statistics(
    demand_set: Set[Tuple[int, int, int, int]],
) -> dict:
    """Compute summary statistics for a raw demand set.

    Parameters
    ----------
    demand_set:
        Set of ``(r3_idx, horizon, morph, law)`` 4-tuples.

    Returns
    -------
    dict with keys:
        ``total_unique``        -- number of unique 4-tuples
        ``per_horizon_counts``  -- ``{horizon_idx: count}``
        ``per_band_counts``     -- ``{'micro': n, 'meso': n, ...}``
        ``sparsity_percent``    -- percentage of the 294,912 theoretical
                                   space that is **unoccupied**

    Raises
    ------
    ValueError
        Propagated from ``DemandTree.build()`` if any tuple is out of range.
    """
    if not demand_set:
        return {
            "total_unique": 0,
            "per_horizon_counts": {},
            "per_band_counts": {},
            "sparsity_percent": 100.0,
        }

    # Build tree to validate and group by horizon
    tree = DemandTree.build(demand_set)

    # Per-horizon counts
    per_horizon_counts: Dict[int, int] = {
        h: len(rml) for h, rml in sorted(tree.items())
    }

    # Per-band counts (aggregate horizon counts into band buckets)
    band_counter: Counter[str] = Counter()
    for h, count in per_horizon_counts.items():
        band_counter[BAND_ASSIGNMENTS[h]] += count

    per_band_counts: Dict[str, int] = {
        band: band_counter.get(band, 0)
        for band in ("micro", "meso", "macro", "ultra")
    }

    # Sparsity: percentage of theoretical space NOT occupied
    total_unique = len(demand_set)
    occupancy = total_unique / _THEORETICAL_SPACE
    sparsity_percent = round((1.0 - occupancy) * 100.0, 2)

    return {
        "total_unique": total_unique,
        "per_horizon_counts": per_horizon_counts,
        "per_band_counts": per_band_counts,
        "sparsity_percent": sparsity_percent,
    }
