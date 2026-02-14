"""Subcortical brain regions for the C3 architecture.

Nine subcortical regions with MNI152 coordinates derived from published
atlases and studies: Harvard-Oxford Atlas (Desikan 2006), Neurosynth
(Yarkoni 2011), Salimpoor 2011/2013, Koelsch 2014, Blood & Zatorre 2001,
Grahn & Rowe 2009, Trost 2012.
"""
from __future__ import annotations

from ...contracts.dataclasses import BrainRegion


# ── Mesolimbic Reward Circuit ────────────────────────────────────────

VTA = BrainRegion(
    name="Ventral Tegmental Area",
    abbreviation="VTA",
    hemisphere="bilateral",
    mni_coords=(0, -16, -8),
    brodmann_area=None,
    function=(
        "Dopaminergic source nucleus; generates reward prediction error "
        "signals during unexpected harmonic progressions and timbral changes"
    ),
    evidence_count=18,
)

NACC = BrainRegion(
    name="Nucleus Accumbens",
    abbreviation="NAcc",
    hemisphere="bilateral",
    mni_coords=(10, 12, -8),
    brodmann_area=None,
    function=(
        "Consummatory reward hub; integrates dopaminergic and opioidergic "
        "signals for peak musical pleasure (Salimpoor 2011, r=0.84)"
    ),
    evidence_count=24,
)

CAUDATE = BrainRegion(
    name="Caudate Nucleus",
    abbreviation="caudate",
    hemisphere="bilateral",
    mni_coords=(12, 10, 10),
    brodmann_area=None,
    function=(
        "Anticipatory reward; dopamine release peaks 10-15s before "
        "consummatory pleasure reflecting prediction-based 'wanting' "
        "(Salimpoor 2011, r=0.71)"
    ),
    evidence_count=19,
)

# ── Emotional Processing ─────────────────────────────────────────────

AMYGDALA = BrainRegion(
    name="Amygdala",
    abbreviation="amygdala",
    hemisphere="bilateral",
    mni_coords=(24, -4, -18),
    brodmann_area=None,
    function=(
        "Emotional valence tagging; responds to dissonance, tension, "
        "and affective salience in musical stimuli (Koelsch 2014)"
    ),
    evidence_count=31,
)

INSULA = BrainRegion(
    name="Insula",
    abbreviation="insula",
    hemisphere="bilateral",
    mni_coords=(36, 16, 0),
    brodmann_area=None,
    function=(
        "Interoceptive awareness; integrates bodily arousal signals with "
        "emotional context for conscious musical feeling states "
        "(Craig 2009, Koelsch 2014)"
    ),
    evidence_count=14,
)

HYPOTHALAMUS = BrainRegion(
    name="Hypothalamus",
    abbreviation="hypothalamus",
    hemisphere="bilateral",
    mni_coords=(0, -4, -8),
    brodmann_area=None,
    function=(
        "Autonomic regulation; mediates physiological responses (heart "
        "rate, chills, skin conductance) to emotionally powerful music "
        "(Blood & Zatorre 2001)"
    ),
    evidence_count=9,
)

# ── Memory ───────────────────────────────────────────────────────────

HIPPOCAMPUS = BrainRegion(
    name="Hippocampus",
    abbreviation="hippocampus",
    hemisphere="bilateral",
    mni_coords=(28, -22, -12),
    brodmann_area=None,
    function=(
        "Musical memory encoding and retrieval; familiarity detection, "
        "episodic associations, and statistical learning of musical "
        "structure (Janata 2009, Watanabe 2008)"
    ),
    evidence_count=22,
)

# ── Sensory Relay / Timing ───────────────────────────────────────────

THALAMUS_MGB = BrainRegion(
    name="Thalamus (Medial Geniculate Body)",
    abbreviation="MGB",
    hemisphere="bilateral",
    mni_coords=(14, -24, -2),
    brodmann_area=None,
    function=(
        "Primary auditory relay; gates ascending spectrotemporal "
        "information to cortex with attentional modulation "
        "(Suga 2008, Winer 2005)"
    ),
    evidence_count=11,
)

PUTAMEN = BrainRegion(
    name="Putamen",
    abbreviation="putamen",
    hemisphere="bilateral",
    mni_coords=(26, 4, 2),
    brodmann_area=None,
    function=(
        "Beat-based motor timing; entrainment to regular rhythmic "
        "structures via basal ganglia-cortical loops "
        "(Grahn & Rowe 2009, d=0.67)"
    ),
    evidence_count=16,
)

# ── Collection ───────────────────────────────────────────────────────

SUBCORTICAL_REGIONS = (
    VTA,
    NACC,
    CAUDATE,
    AMYGDALA,
    INSULA,
    HYPOTHALAMUS,
    HIPPOCAMPUS,
    THALAMUS_MGB,
    PUTAMEN,
)
"""All 9 subcortical regions."""
