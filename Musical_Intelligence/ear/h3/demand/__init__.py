"""H3 demand sub-package -- demand routing, horizon lookup, and aggregation.

Re-exports the public API for H3 demand management:

- ``DemandTree``         -- stateless grouping of 4-tuples by horizon
- ``EventHorizon``       -- lightweight horizon-index-to-attributes wrapper
- ``aggregate_demands``  -- collect demands from models and build a DemandTree
- ``demand_statistics``  -- sparsity and distribution statistics for a demand set
"""
from __future__ import annotations

from .aggregator import aggregate_demands, demand_statistics
from .demand_tree import DemandTree
from .event_horizon import EventHorizon

__all__ = [
    "DemandTree",
    "EventHorizon",
    "aggregate_demands",
    "demand_statistics",
]
