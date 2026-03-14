"""Brain regions package — 26 canonical regions with MNI152 coordinates.

.. deprecated::
    This module is deprecated and will be removed in a future version.
    Region activation is handled internally by the executor.
    No new code should import from this package.

Each region is defined in its own file under this package.
The ``registry`` module collects them into lookup structures.
"""
import warnings as _warnings
_warnings.warn(
    "Musical_Intelligence.brain.regions is deprecated. "
    "Do not add new imports from this package.",
    DeprecationWarning,
    stacklevel=2,
)
from ._region import Region
from .registry import (
    ALL_REGIONS,
    NUM_REGIONS,
    REGION_BY_INDEX,
    REGION_REGISTRY,
    region_index,
)

__all__ = [
    "Region",
    "ALL_REGIONS",
    "NUM_REGIONS",
    "REGION_BY_INDEX",
    "REGION_REGISTRY",
    "region_index",
]
