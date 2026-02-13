"""H3 pipeline sub-package.

Provides the execution engine and warm-up analysis utilities for the
H3 temporal morphology layer.

Classes
-------
H3Executor
    Seven-phase execution loop that computes demanded temporal morph
    features from an R3 spectral tensor and a pre-built demand tree.
WarmUpHandler
    Stateless utility for analysing warm-up zones at sequence boundaries,
    where attention windows are truncated and morph output is less reliable.
"""

from __future__ import annotations

from .executor import H3Executor
from .warmup import WarmUpHandler

__all__ = [
    "H3Executor",
    "WarmUpHandler",
]
