"""Serotonin (5-HT) -- mood regulation and emotional valence modulation.

The serotonergic system originates from the raphe nuclei and projects widely.
In musical cognition, 5-HT modulates emotional valence, social bonding during
group music-making, and anxiety reduction.  Operates primarily as a slow
neuromodulator (seconds to minutes) rather than encoding discrete events.

Key papers: Koelsch 2014, Chanda & Levitin 2013, Tarr et al. 2014,
Kreutz et al. 2012, Ferreri 2019.
"""
from __future__ import annotations

from .dopamine import Neurochemical


SEROTONIN = Neurochemical(
    name="Serotonin",
    abbreviation="5-HT",
    primary_pathway="Dorsal Raphe -> Amygdala, PFC (widespread)",
    source_regions=("raphe",),
    target_regions=("amygdala", "PFC", "NAcc", "VTA"),
    primary_function=(
        "Emotional valence modulation, mood regulation, social bonding, "
        "anxiety reduction"
    ),
    musical_role=(
        "Background mood state colouring emotional interpretation of music; "
        "positive valence bias (high 5-HT), social bonding in group "
        "music-making, anxiety reduction via calming music"
    ),
    associated_units=("ARU", "RPU", "PCU"),
)
