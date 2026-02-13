"""H3 attention sub-package.

Provides the exponential decay attention kernel and three temporal law
window selectors used by the H3 temporal morphology layer.

Classes
-------
AttentionKernel
    Generates unnormalized exponential decay weights for a temporal window.
MemoryWindow
    L0 (Memory) -- causal, past-only window selection.
PredictionWindow
    L1 (Prediction) -- anticipatory, future-only window selection.
IntegrationWindow
    L2 (Integration) -- bidirectional, symmetric window selection.
"""

from __future__ import annotations

from .integration import IntegrationWindow
from .kernel import AttentionKernel
from .memory import MemoryWindow
from .prediction import PredictionWindow

__all__ = [
    "AttentionKernel",
    "MemoryWindow",
    "PredictionWindow",
    "IntegrationWindow",
]
