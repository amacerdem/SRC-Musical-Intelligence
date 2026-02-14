"""Norepinephrine (NE) -- arousal, attentional gating, and orienting response.

The noradrenergic system originates from the locus coeruleus (LC) and
projects to virtually every cortical and subcortical region.  In musical
cognition, NE mediates arousal regulation, attentional gating, orienting
response to novel/unexpected events, and memory consolidation of
emotionally salient musical events.

Key papers: Aston-Jones & Cohen 2005, Menon & Levitin 2005,
Chanda & Levitin 2013, McGaugh 2004, Sara 2009, Arnsten 2011.
"""
from __future__ import annotations

from .dopamine import Neurochemical


NOREPINEPHRINE = Neurochemical(
    name="Norepinephrine",
    abbreviation="NE",
    primary_pathway="Locus Coeruleus -> widespread cortical/subcortical",
    source_regions=("LC",),
    target_regions=("amygdala", "PFC", "hippocampus", "VTA", "AC"),
    primary_function=(
        "Arousal regulation, attentional gating, orienting response, "
        "memory consolidation of emotionally salient events"
    ),
    musical_role=(
        "Global arousal level setting intensity of musical experience; "
        "selective attention to musically relevant events; orienting to "
        "novel/unexpected musical events (dynamics, harmony, timbre); "
        "enhanced encoding of emotionally powerful musical moments"
    ),
    associated_units=("ASU", "NDU", "ARU", "PCU", "IMU"),
)
