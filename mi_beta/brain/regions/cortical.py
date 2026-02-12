"""
Cortical brain regions relevant to musical cognition.

MNI152 coordinates are taken from published meta-analyses and atlases:
    - Brodmann area assignments from Talairach & Tournoux 1988
    - Zatorre et al. 2002 (auditory cortex specialization)
    - Koelsch 2011, 2014 (music syntax & emotion)
    - Grahn & Rowe 2009, 2013 (motor timing)
    - Janata 2009 (tonality-tracking in mPFC)
    - Levitin & Menon 2003 (musical structure)
    - Tillmann et al. 2003 (harmonic priming)
    - Alluri et al. 2012 (timbral feature mapping)
    - Patterson et al. 2002 (pitch centre in HG)
    - Sammler et al. 2013 (music syntax in IFG)

All coordinates represent bilateral centroids with the hemisphere noted.
Where a structure is strongly lateralised, the dominant hemisphere is given.
Evidence counts reflect the number of C3 meta-analysis studies citing each
region in a music cognition context.
"""

from __future__ import annotations

from mi_beta.contracts import BrainRegion

# =====================================================================
# PRIMARY AUDITORY CORTEX / HESCHL'S GYRUS (A1 / HG)
# =====================================================================
# Tonotopic frequency mapping.  First cortical processing stage for
# all auditory input.  Contains both core (A1) and belt regions.
# Bilateral but shows rightward lateralisation for spectral processing
# and leftward for temporal resolution (Zatorre et al. 2002).
# MNI from Patterson et al. 2002 pitch center.

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

# =====================================================================
# SUPERIOR TEMPORAL GYRUS (STG)
# =====================================================================
# Auditory association cortex.  Processes complex spectrotemporal
# patterns including melody, harmony, and timbre.  Posterior STG is
# critical for pitch pattern recognition (Griffiths & Warren 2002).
# MNI from Alluri et al. 2012 meta-analytic peak for timbral features.

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

# =====================================================================
# SUPERIOR TEMPORAL SULCUS (STS)
# =====================================================================
# Higher-order integration of auditory streams.  Sensitive to voice
# and music processing distinctions, multimodal binding with visual
# information, and social/communicative aspects of music.
# MNI from Belin et al. 2000 voice-selective temporal cortex.

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

# =====================================================================
# INFERIOR FRONTAL GYRUS (IFG) -- Broca's Area
# =====================================================================
# Music syntactic processing.  BA44/45 (pars opercularis/triangularis)
# processes hierarchical structure in both language and music.
# ERAN (early right anterior negativity) generator.  Left IFG for
# linguistic syntax, right IFG for musical syntax (Koelsch 2011).
# MNI from Sammler et al. 2013 music syntax violation peak.

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

# =====================================================================
# DORSOLATERAL PREFRONTAL CORTEX (dlPFC)
# =====================================================================
# Working memory maintenance and executive control.  Holds tonal
# context in working memory, enables comparison of current events
# with expected patterns.  Left dlPFC for verbal, right for spatial
# and tonal working memory (Zatorre et al. 1994).
# MNI from Owen et al. 2005 WM meta-analysis peak.

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

# =====================================================================
# VENTROMEDIAL PREFRONTAL CORTEX (vmPFC)
# =====================================================================
# Value computation and emotional regulation.  Integrates reward signals
# from NAcc/OFC with contextual evaluation.  Tracks tonality and
# musical autobiography (Janata 2009, Blood & Zatorre 2001).
# MNI from Janata 2009 tonality-tracking peak.

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

# =====================================================================
# ORBITOFRONTAL CORTEX (OFC)
# =====================================================================
# Reward valuation and hedonic judgement.  Computes the hedonic value
# of musical stimuli, mediating "conscious liking" versus raw reward
# signal.  Connected to NAcc, amygdala, and vmPFC.
# MNI from Blood & Zatorre 2001 PET peak during musical chills.

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

# =====================================================================
# ANTERIOR CINGULATE CORTEX (ACC)
# =====================================================================
# Conflict monitoring and error detection.  Responds to harmonic
# violations, unexpected rhythmic events, and prediction error.
# Part of the salience network with anterior insula (Menon 2015).
# MNI from Shenhav et al. 2013 meta-analysis of ACC function.

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

# =====================================================================
# SUPPLEMENTARY MOTOR AREA (SMA)
# =====================================================================
# Internal timing and motor sequence planning.  Critical for rhythm
# perception even without overt movement.  Encodes beat-level
# temporal structure and metric hierarchy (Grahn & Rowe 2009, 2013).
# MNI from Grahn & Rowe 2009 fMRI peak.

SMA = BrainRegion(
    name="Supplementary Motor Area",
    abbreviation="SMA",
    hemisphere="bilateral",
    mni_coords=(2, -2, 56),
    brodmann_area=6,
    function=(
        "Internal timing and motor planning; encodes beat-level "
        "metric structure even during passive listening "
        "(Grahn & Rowe 2009, 2013, d=0.67)"
    ),
    evidence_count=21,
)

# =====================================================================
# PREMOTOR CORTEX (PMC)
# =====================================================================
# Motor planning and auditory-motor coupling.  Ventral PMC connects
# auditory cortex to motor cortex for rhythm entrainment and
# sensorimotor synchronisation (Chen et al. 2008).
# MNI from Chen et al. 2008 auditory-motor coupling peak.

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

# =====================================================================
# ANGULAR GYRUS
# =====================================================================
# Cross-modal integration and semantic processing.  Part of the
# temporo-parietal junction (TPJ).  Integrates auditory, visual,
# and somatosensory information; contributes to music-evoked
# autobiographical memories (Koelsch 2014, Seghier 2013).
# MNI from Seghier 2013 meta-analysis of angular gyrus function.

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

# =====================================================================
# TEMPORAL POLE
# =====================================================================
# Semantic memory and conceptual processing.  Anterior temporal lobe
# stores abstract musical knowledge, genre schemas, and semantic
# associations evoked by familiar music (Patterson et al. 2007).
# MNI from Patterson et al. 2007 semantic dementia study.

TEMPORAL_POLE = BrainRegion(
    name="Temporal Pole",
    abbreviation="TP",
    hemisphere="bilateral",
    mni_coords=(42, 12, -32),
    brodmann_area=38,
    function=(
        "Semantic memory hub; stores abstract musical knowledge, "
        "genre schemas, and conceptual associations "
        "(Patterson 2007, Peretz & Coltheart 2003)"
    ),
    evidence_count=7,
)

# =====================================================================
# CONVENIENCE TUPLE
# =====================================================================

ALL_CORTICAL: tuple[BrainRegion, ...] = (
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
"""All cortical regions in canonical order."""

__all__ = [
    "A1_HG",
    "STG",
    "STS",
    "IFG",
    "DLPFC",
    "VMPFC",
    "OFC",
    "ACC",
    "SMA",
    "PMC",
    "ANGULAR_GYRUS",
    "TEMPORAL_POLE",
    "ALL_CORTICAL",
]
