"""Brain layer — mechanisms, units, circuits, pathways, regions, neurochemicals.

The brain layer implements the C3 cognitive architecture:
- 10 mechanisms (30D each, computed once per forward pass)
- 9 cognitive units (96 models total, 1006D output)
- 5 pathways (3 inter-unit, 2 intra-unit)
- 5-phase orchestrated execution

Quick start::

    from Musical_Intelligence.brain import BrainOrchestrator

    brain = BrainOrchestrator()
    output = brain.forward(h3_features, r3_features)
    # output.tensor: (B, T, 1006)
"""
from __future__ import annotations

from .orchestrator import BrainOrchestrator, BrainOutput

__all__ = [
    "BrainOrchestrator",
    "BrainOutput",
]
