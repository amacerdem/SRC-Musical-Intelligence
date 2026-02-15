"""Registry — collects all 26 brain regions into lookup structures.

This is the single source of truth for region identity, coordinates,
and RAM tensor position ``(B, T, 26)``.

Source: Docs/C³/Regions/{Cortical,Subcortical,Brainstem}.md
"""
from __future__ import annotations

from typing import Dict, Tuple

from ._region import Region

# --- CORTICAL (12 regions, indices 0-11) ---
from .a1_hg import A1_HG
from .stg import STG
from .sts import STS
from .ifg import IFG
from .dlpfc import dlPFC
from .vmpfc import vmPFC
from .ofc import OFC
from .acc import ACC
from .sma import SMA
from .pmc import PMC
from .ag import AG
from .tp import TP

# --- SUBCORTICAL (9 regions, indices 12-20) ---
from .vta import VTA
from .nacc import NAcc
from .caudate import caudate
from .amygdala import amygdala
from .hippocampus import hippocampus
from .putamen import putamen
from .mgb import MGB
from .hypothalamus import hypothalamus
from .insula import insula

# --- BRAINSTEM (5 regions, indices 21-25) ---
from .ic import IC
from .an import AN
from .cn import CN
from .soc import SOC
from .pag import PAG

# ======================================================================
# Ordered tuple — canonical order by index
# ======================================================================

ALL_REGIONS: Tuple[Region, ...] = (
    # Cortical (0-11)
    A1_HG, STG, STS, IFG, dlPFC, vmPFC, OFC, ACC, SMA, PMC, AG, TP,
    # Subcortical (12-20)
    VTA, NAcc, caudate, amygdala, hippocampus, putamen, MGB, hypothalamus, insula,
    # Brainstem (21-25)
    IC, AN, CN, SOC, PAG,
)

# ======================================================================
# Lookup dicts
# ======================================================================

REGION_REGISTRY: Dict[str, Region] = {r.abbreviation: r for r in ALL_REGIONS}
REGION_BY_INDEX: Dict[int, Region] = {r.index: r for r in ALL_REGIONS}

NUM_REGIONS: int = len(ALL_REGIONS)
assert NUM_REGIONS == 26, f"Expected 26 regions, got {NUM_REGIONS}"


def region_index(abbreviation: str) -> int:
    """Return the RAM tensor index for a region abbreviation.

    Raises:
        KeyError: If the abbreviation is not in the registry.
    """
    return REGION_REGISTRY[abbreviation].index
