"""Neurochemicals package — 4 modulatory channels.

.. deprecated::
    This module is deprecated and will be removed in a future version.
    The neurochemical accumulation is handled internally by the executor.
    No new code should import from this package.

Each neurochemical is defined in its own file with channel metadata,
reference values, and interaction descriptions. The ``manager`` module
provides the accumulation logic.
"""
import warnings as _warnings
_warnings.warn(
    "Musical_Intelligence.brain.neurochemicals is deprecated. "
    "Do not add new imports from this package.",
    DeprecationWarning,
    stacklevel=2,
)
from Musical_Intelligence.contracts.dataclasses import (
    DA,
    NE,
    NUM_CHANNELS,
    OPI,
    _5HT,
)

from .manager import BASELINE, accumulate_neuro, init_neuro

__all__ = [
    "DA", "NE", "OPI", "_5HT", "NUM_CHANNELS",
    "BASELINE", "init_neuro", "accumulate_neuro",
]
