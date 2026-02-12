"""
MI-Beta Pipeline -- Orchestration layer for the full audio -> MI-space pipeline.

Components:
    BrainOrchestrator  -- Sequences brain computation across mechanisms,
                          units, and pathways.
    MIBetaPipeline     -- Full audio -> MI-space orchestrator combining
                          ear (cochlea, R3, H3) and brain.
"""

from __future__ import annotations

from .brain_runner import BrainOrchestrator
from .mi_beta import MIBetaPipeline

__all__ = [
    "BrainOrchestrator",
    "MIBetaPipeline",
]
