"""R3 pipeline sub-package.

Provides the execution engine, normalization, and warm-up analysis for the
R3 spectral feature extraction pipeline.

Classes
-------
DependencyDAG
    Three-stage execution DAG encoding inter-group dependencies.
StageExecutor
    Executes spectral groups in DAG-ordered stages.
FeatureNormalizer
    Per-group normalization ensuring all features are in [0, 1].
WarmupManager
    Tracks warm-up zones for features that require temporal context.
"""

from __future__ import annotations

from .dag import DependencyDAG
from .normalization import FeatureNormalizer
from .stage_executor import StageExecutor
from .warmup import WarmupManager

__all__ = [
    "DependencyDAG",
    "FeatureNormalizer",
    "StageExecutor",
    "WarmupManager",
]
