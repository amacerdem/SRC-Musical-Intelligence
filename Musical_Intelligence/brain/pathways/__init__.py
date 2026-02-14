"""Pathway routing -- 5 cross-unit data dependencies.

3 inter-unit pathways routed by PathwayRunner (P1, P3, P5).
2 intra-unit pathways handled within STU (P2, P4).
"""
from __future__ import annotations

from .definitions import (
    ALL_PATHWAYS,
    INTER_UNIT_PATHWAYS,
    INTRA_UNIT_PATHWAYS,
    P1_SPU_ARU,
    P2_STU_INTERNAL,
    P3_IMU_ARU,
    P4_STU_INTERNAL,
    P5_STU_ARU,
)
from .runner import PathwayRunner

__all__ = [
    "PathwayRunner",
    "ALL_PATHWAYS",
    "INTER_UNIT_PATHWAYS",
    "INTRA_UNIT_PATHWAYS",
    "P1_SPU_ARU",
    "P2_STU_INTERNAL",
    "P3_IMU_ARU",
    "P4_STU_INTERNAL",
    "P5_STU_ARU",
]
