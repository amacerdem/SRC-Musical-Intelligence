"""Cortical brain regions for the C3 architecture.

Twelve cortical regions with MNI152 coordinates derived from published
meta-analyses: Zatorre 2002, Koelsch 2011/2014, Grahn & Rowe 2009/2013,
Janata 2009, Levitin & Menon 2003, Alluri 2012, Patterson 2002,
Sammler 2013.
"""
from __future__ import annotations

from ...contracts.dataclasses import BrainRegion


# ── Auditory Processing Chain ────────────────────────────────────────

A1_HG = BrainRegion(
    name="Primary Auditory Cortex (Heschl's Gyrus)",
    abbreviation="A1/HG",
    hemisphere="bilateral",
    mni_coords=(48, -18, 8),
    brodmann_area=41,
    function=(
        "Tonotopic frequency analysis; first cortical stage of spectral "
        "decomposition with rightward lateralisation for pitch, leftward "
        "for temporal fine structure (Zatorre 2002, Patterson 2002)"
    ),
    evidence_count=42,
)

STG = BrainRegion(
    name="Superior Temporal Gyrus",
    abbreviation="STG",
    hemisphere="bilateral",
    mni_coords=(58, -22, 4),
    brodmann_area=22,
    function=(
        "Auditory association cortex; processes melody, harmony, and "
        "timbre through spectrotemporal pattern recognition "
        "(Griffiths & Warren 2002, Alluri 2012)"
    ),
    evidence_count=38,
)

STS = BrainRegion(
    name="Superior Temporal Sulcus",
    abbreviation="STS",
    hemisphere="bilateral",
    mni_coords=(54, -32, 4),
    brodmann_area=21,
    function=(
        "Multimodal stream integration; voice/music discrimination, "
        "audiovisual binding, and communicative intent processing "
        "(Belin 2000, Peretz & Coltheart 2003)"
    ),
    evidence_count=15,
)

# ── Frontal Executive / Syntax ───────────────────────────────────────

IFG = BrainRegion(
    name="Inferior Frontal Gyrus (Broca's Area)",
    abbreviation="IFG",
    hemisphere="R",
    mni_coords=(48, 18, 8),
    brodmann_area=44,
    function=(
        "Musical syntax processing; generates ERAN for unexpected "
        "harmonic events, hierarchical sequence parsing "
        "(Koelsch 2011, Sammler 2013)"
    ),
    evidence_count=27,
)

DLPFC = BrainRegion(
    name="Dorsolateral Prefrontal Cortex",
    abbreviation="dlPFC",
    hemisphere="bilateral",
    mni_coords=(42, 32, 30),
    brodmann_area=46,
    function=(
        "Working memory and executive control; maintains tonal context "
        "for expectation comparison and planning "
        "(Zatorre 1994, Owen 2005)"
    ),
    evidence_count=13,
)

# ── Reward / Valuation ───────────────────────────────────────────────

VMPFC = BrainRegion(
    name="Ventromedial Prefrontal Cortex",
    abbreviation="vmPFC",
    hemisphere="bilateral",
    mni_coords=(2, 46, -10),
    brodmann_area=10,
    function=(
        "Subjective value computation; integrates reward with contextual "
        "evaluation, tracks tonality and musical autobiography "
        "(Janata 2009, Blood & Zatorre 2001)"
    ),
    evidence_count=17,
)

OFC = BrainRegion(
    name="Orbitofrontal Cortex",
    abbreviation="OFC",
    hemisphere="bilateral",
    mni_coords=(28, 34, -16),
    brodmann_area=11,
    function=(
        "Reward valuation and hedonic judgement; computes the conscious "
        "aesthetic value of musical stimuli "
        "(Blood & Zatorre 2001, Salimpoor 2013)"
    ),
    evidence_count=15,
)

# ── Monitoring / Integration ─────────────────────────────────────────

ACC = BrainRegion(
    name="Anterior Cingulate Cortex",
    abbreviation="ACC",
    hemisphere="bilateral",
    mni_coords=(2, 30, 28),
    brodmann_area=32,
    function=(
        "Conflict monitoring and prediction error signalling; detects "
        "harmonic violations and unexpected musical events "
        "(Koelsch 2014, Menon 2015)"
    ),
    evidence_count=12,
)

# ── Motor / Timing ───────────────────────────────────────────────────

SMA = BrainRegion(
    name="Supplementary Motor Area",
    abbreviation="SMA",
    hemisphere="bilateral",
    mni_coords=(2, -2, 56),
    brodmann_area=6,
    function=(
        "Internal timing and motor planning; encodes beat-level metric "
        "structure even during passive listening "
        "(Grahn & Rowe 2009, 2013, d=0.67)"
    ),
    evidence_count=21,
)

PMC = BrainRegion(
    name="Premotor Cortex",
    abbreviation="PMC",
    hemisphere="bilateral",
    mni_coords=(46, 0, 48),
    brodmann_area=6,
    function=(
        "Auditory-motor coupling and motor planning; mediates rhythm "
        "entrainment and sensorimotor synchronisation "
        "(Chen 2008, Zatorre 2007)"
    ),
    evidence_count=14,
)

# ── Cross-modal / Semantic ───────────────────────────────────────────

ANGULAR_GYRUS = BrainRegion(
    name="Angular Gyrus",
    abbreviation="AG",
    hemisphere="bilateral",
    mni_coords=(48, -60, 30),
    brodmann_area=39,
    function=(
        "Cross-modal integration; binds auditory, visual, and "
        "somatosensory streams for holistic musical experience "
        "(Seghier 2013, Koelsch 2014)"
    ),
    evidence_count=8,
)

TEMPORAL_POLE = BrainRegion(
    name="Temporal Pole",
    abbreviation="TP",
    hemisphere="bilateral",
    mni_coords=(42, 12, -32),
    brodmann_area=38,
    function=(
        "Semantic memory hub; stores abstract musical knowledge, genre "
        "schemas, and conceptual associations "
        "(Patterson 2007, Peretz & Coltheart 2003)"
    ),
    evidence_count=7,
)

# ── Collection ───────────────────────────────────────────────────────

CORTICAL_REGIONS = (
    A1_HG,
    STG,
    STS,
    IFG,
    DLPFC,
    VMPFC,
    OFC,
    ACC,
    SMA,
    PMC,
    ANGULAR_GYRUS,
    TEMPORAL_POLE,
)
"""All 12 cortical regions."""
