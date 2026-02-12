"""
Subcortical brain regions relevant to musical cognition.

MNI152 coordinates are taken from published meta-analyses and atlases:
    - Harvard-Oxford Subcortical Structural Atlas (Desikan 2006)
    - Neurosynth meta-analytic peaks (Yarkoni 2011)
    - Salimpoor et al. 2011, 2013 (reward circuitry)
    - Koelsch 2014 (music-evoked emotion model)
    - Zatorre & Salimpoor 2013 (pleasure and prediction)
    - Blood & Zatorre 2001 (chills and autonomic)
    - Grahn & Rowe 2009 (putamen and timing)
    - Trost et al. 2012 (amygdala and emotion)
    - Watanabe et al. 2008 (thalamic relay)

All coordinates represent bilateral centroids unless hemisphere is specified.
Evidence counts reflect the number of C3 meta-analysis studies citing each
region in a music cognition context.
"""

from __future__ import annotations

from mi_beta.contracts import BrainRegion

# =====================================================================
# VENTRAL TEGMENTAL AREA (VTA)
# =====================================================================
# Primary dopaminergic cell body.  Projects to NAcc (mesolimbic) and
# PFC (mesocortical).  Activated by unexpected musical events that
# generate reward prediction error (Salimpoor 2011, Ferreri 2019).
# MNI from Murty et al. 2014 meta-analysis of VTA/SN activations.

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

# =====================================================================
# NUCLEUS ACCUMBENS (NAcc)
# =====================================================================
# Core target of mesolimbic DA.  Consummatory pleasure ("liking") site.
# PET [11C]raclopride shows DA release during peak pleasure moments
# (Salimpoor 2011, r=0.84).  Also receives opioidergic hedonic signals.
# MNI from Harvard-Oxford atlas centroid.

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

# =====================================================================
# CAUDATE NUCLEUS
# =====================================================================
# Anticipatory reward.  DA release in caudate peaks 10-15s BEFORE the
# pleasure peak in NAcc (Salimpoor 2011).  Encodes expected future
# reward value based on learned musical expectations.
# MNI from Salimpoor 2011 PET peak coordinates.

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

# =====================================================================
# AMYGDALA
# =====================================================================
# Emotional valence tagging and arousal modulation.  Responds to
# dissonance, minor mode, and fear-relevant timbres.  Bidirectional
# connection with NAcc and OFC for value computation.
# MNI from Trost et al. 2012 meta-analysis of music-evoked emotion.

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

# =====================================================================
# HIPPOCAMPUS
# =====================================================================
# Memory encoding and retrieval.  Critical for musical familiarity,
# recognition memory, and episodic associations triggered by music.
# Activated during exposure to familiar melodies and during encoding
# of novel musical patterns (Watanabe et al. 2008, Janata 2009).
# MNI from Harvard-Oxford atlas, posterior hippocampal centroid.

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

# =====================================================================
# PUTAMEN
# =====================================================================
# Motor timing and beat-based entrainment.  Part of the dorsal
# striatum circuit with SMA and PMC.  Preferentially activated by
# regular beat structures (Grahn & Rowe 2009, 2013).
# MNI from Grahn & Rowe 2009 fMRI peak.

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

# =====================================================================
# THALAMUS (MEDIAL GENICULATE BODY)
# =====================================================================
# Primary auditory relay nucleus.  All ascending auditory information
# passes through MGB before reaching auditory cortex.  Modulated by
# top-down attention and arousal state (Suga 2008).
# MNI from Harvard-Oxford atlas, MGB centroid.

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

# =====================================================================
# HYPOTHALAMUS
# =====================================================================
# Autonomic regulation hub.  Music-evoked chills, heart rate changes,
# and skin conductance responses are mediated partly through
# hypothalamic-brainstem autonomic pathways (Blood & Zatorre 2001).
# MNI from Harvard-Oxford atlas centroid.

HYPOTHALAMUS = BrainRegion(
    name="Hypothalamus",
    abbreviation="hypothalamus",
    hemisphere="bilateral",
    mni_coords=(0, -4, -8),
    brodmann_area=None,
    function=(
        "Autonomic regulation; mediates physiological responses "
        "(heart rate, chills, skin conductance) to emotionally "
        "powerful music (Blood & Zatorre 2001)"
    ),
    evidence_count=9,
)

# =====================================================================
# INSULA
# =====================================================================
# Interoceptive awareness and emotional feeling states.  The anterior
# insula integrates bodily signals with emotional context, generating
# conscious "felt" experience of music (Craig 2009, Koelsch 2014).
# MNI from Kurth et al. 2010 meta-analysis of insular function.

INSULA = BrainRegion(
    name="Insula",
    abbreviation="insula",
    hemisphere="bilateral",
    mni_coords=(36, 16, 0),
    brodmann_area=None,
    function=(
        "Interoceptive awareness; integrates bodily arousal signals "
        "with emotional context for conscious musical feeling states "
        "(Craig 2009, Koelsch 2014)"
    ),
    evidence_count=14,
)

# =====================================================================
# CONVENIENCE TUPLE
# =====================================================================

ALL_SUBCORTICAL: tuple[BrainRegion, ...] = (
    VTA,
    NACC,
    CAUDATE,
    AMYGDALA,
    HIPPOCAMPUS,
    PUTAMEN,
    THALAMUS_MGB,
    HYPOTHALAMUS,
    INSULA,
)
"""All subcortical regions in canonical order."""

__all__ = [
    "VTA",
    "NACC",
    "CAUDATE",
    "AMYGDALA",
    "HIPPOCAMPUS",
    "PUTAMEN",
    "THALAMUS_MGB",
    "HYPOTHALAMUS",
    "INSULA",
    "ALL_SUBCORTICAL",
]
