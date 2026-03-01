"""Shared Dimension dataclass for the 3-tier falsifiability system.

Three independent tiers (NOT hierarchically derived):
    Psychology   (6D)  — gut-level, zero training to validate, free tier
    Cognition    (12D) — informed listener, some music knowledge, basic tier
    Neuroscience (24D) — expert, requires neuroscience knowledge, premium tier

Each dimension is independently computed from (beliefs, ram, neuro).
Computation models live in ``dimensions/models/``.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Dimension:
    """A dimension in the 3-tier falsifiability system.

    Attributes:
        index:          Position within its layer's tensor (0-5, 0-11, or 0-23).
        key:            Machine-readable identifier (e.g., ``"energy"``).
        name:           English display name.
        name_tr:        Turkish display name.
        layer:          ``"psychology"``, ``"cognition"``, or ``"neuroscience"``.
        parent_key:     Organizational grouping key (for display, NOT computation).
        description:    Falsification test — the question a listener asks to
                        validate this dimension.
        agreement:      Expected inter-rater agreement level among the tier's
                        target audience (``"very_high"``, ``"high"``, ``"medium"``).
        belief_indices: Tuple of C³ belief indices (0-130) used by this dimension's
                        computation model.  For reference/display only — actual
                        computation is in ``models/``.
    """

    index: int
    key: str
    name: str
    name_tr: str
    layer: str
    parent_key: Optional[str] = None
    description: str = ""
    agreement: str = ""
    belief_indices: Tuple[int, ...] = ()
