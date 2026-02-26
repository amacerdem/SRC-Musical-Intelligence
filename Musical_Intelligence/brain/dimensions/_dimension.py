"""Shared Dimension dataclass for hierarchical belief aggregation.

Three layers form a binary tree:
    Psychology (6D)  → experiential terms, free tier
    Cognition  (12D) → music cognition terms, basic tier
    Neuroscience (24D) → neuroscience terms, premium tier

Each node at the leaf (24D) maps to a subset of the 131 C³ beliefs.
Parent nodes aggregate their children by mean.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Dimension:
    """A node in the hierarchical dimension tree.

    Attributes:
        index:          Position within its layer's tensor (0-5, 0-11, or 0-23).
        key:            Machine-readable identifier (e.g., ``"discovery"``).
        name:           English display name.
        name_tr:        Turkish display name (populated for all layers).
        layer:          ``"psychology"``, ``"cognition"``, or ``"neuroscience"``.
        parent_key:     Key of parent Dimension (``None`` for 6D roots).
        belief_indices: Tuple of C³ belief indices (0-130) that aggregate into
                        this node.  For 6D and 12D, this is the union of all
                        descendant leaf beliefs.
    """

    index: int
    key: str
    name: str
    name_tr: str
    layer: str
    parent_key: Optional[str]
    belief_indices: Tuple[int, ...]
