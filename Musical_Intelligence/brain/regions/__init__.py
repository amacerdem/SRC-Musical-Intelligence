"""Brain regions package — 26 canonical regions with MNI152 coordinates.

Each region is defined in its own file under this package.
The ``registry`` module collects them into lookup structures.
"""
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
