"""Dopamine (DA) neurochemical system -- mesolimbic reward and anticipatory signalling.

Two distinct DA subsystems operate in parallel during music listening:
- **Anticipatory DA** (caudate): 10-15s before peak pleasure (wanting)
- **Consummatory DA** (NAcc): at the moment of peak pleasure (liking)

Key papers: Salimpoor 2011, Ferreri 2019, Schultz 1997, Berridge 2003.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Neurochemical:
    """A neurochemical system definition.

    Attributes:
        name:              Full neurochemical name (e.g. ``"Dopamine"``).
        abbreviation:      Short label (e.g. ``"DA"``).
        primary_pathway:   Principal neural pathway (e.g.
                           ``"Mesolimbic (VTA -> NAcc)"``).
        source_regions:    Tuple of source region abbreviations.
        target_regions:    Tuple of target region abbreviations.
        primary_function:  Brief functional description.
        musical_role:      Role in music cognition and emotion.
        associated_units:  Tuple of cognitive-unit abbreviations.
    """

    name: str
    abbreviation: str
    primary_pathway: str
    source_regions: Tuple[str, ...]
    target_regions: Tuple[str, ...]
    primary_function: str
    musical_role: str
    associated_units: Tuple[str, ...]


DOPAMINE = Neurochemical(
    name="Dopamine",
    abbreviation="DA",
    primary_pathway="Mesolimbic (VTA -> NAcc)",
    source_regions=("VTA", "SNc"),
    target_regions=("NAcc", "caudate", "putamen", "mPFC"),
    primary_function=(
        "Reward prediction error, motivation, reinforcement learning"
    ),
    musical_role=(
        "Anticipatory pleasure (caudate, wanting), consummatory pleasure "
        "(NAcc, liking), groove reward, chills/frisson"
    ),
    associated_units=("ARU", "RPU"),
)
