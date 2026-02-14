"""Endogenous Opioids (mu-opioid) -- hedonic "liking" and consummatory pleasure.

The mu-opioid system mediates the hedonic "liking" response -- the raw
pleasurable sensation at the moment of musical consummation, dissociable
from dopaminergic "wanting" (Berridge 2003).

Hedonic hotspots: NAcc medial shell, ventral pallidum posterior,
parabrachial nucleus.

Key papers: Berridge 2003, Berridge & Kringelbach 2015, Nummenmaa 2025,
Pecina & Berridge 2005, Smith & Berridge 2007.
"""
from __future__ import annotations

from .dopamine import Neurochemical


OPIOID = Neurochemical(
    name="Endogenous Opioid",
    abbreviation="EO",
    primary_pathway="NAcc shell -> Ventral Pallidum -> OFC/vmPFC",
    source_regions=("NAcc", "VP", "parabrachial"),
    target_regions=("NAcc", "VP", "OFC", "vmPFC"),
    primary_function=(
        "Hedonic impact, consummatory pleasure, 'liking' reactions"
    ),
    musical_role=(
        "Peak musical pleasure at consummatory moment, chills/frisson "
        "hedonic component, aesthetic enjoyment via hedonic hotspot network"
    ),
    associated_units=("ARU", "RPU", "PCU"),
)
