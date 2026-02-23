"""Neurochemicals package — 4 modulatory channels.

Each neurochemical is defined in its own file with channel metadata,
reference values, and interaction descriptions. The ``manager`` module
provides the accumulation logic.
"""
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
