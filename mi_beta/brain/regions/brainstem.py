"""
Brainstem brain regions relevant to musical cognition.

MNI152 coordinates are taken from published atlases and studies:
    - Harvard Ascending Arousal Network Atlas (Edlow 2012)
    - Coffey et al. 2016 (frequency-following response in IC)
    - Chandrasekaran & Kraus 2010 (auditory brainstem encoding)
    - Thompson & Bhatt 2017 (brainstem auditory pathway atlas)
    - Goldstein 1983 (PAG and emotional vocalisation)
    - Blood & Zatorre 2001 (PAG activation during chills)

Brainstem structures are small and deep; MNI coordinates carry
higher spatial uncertainty (+/- 2-3 mm) than cortical regions.
"""

from __future__ import annotations

from mi_beta.contracts import BrainRegion

# =====================================================================
# INFERIOR COLLICULUS (IC)
# =====================================================================
# Midbrain auditory processing hub.  Obligatory relay for all ascending
# auditory information.  Generates the frequency-following response
# (FFR) which faithfully encodes the fundamental frequency and
# harmonics of musical sounds.  Critical for subcortical pitch
# encoding (Coffey et al. 2016, Chandrasekaran & Kraus 2010).
# MNI from Thompson & Bhatt 2017 brainstem atlas.

IC = BrainRegion(
    name="Inferior Colliculus",
    abbreviation="IC",
    hemisphere="bilateral",
    mni_coords=(0, -34, -8),
    brodmann_area=None,
    function=(
        "Midbrain auditory relay; generates frequency-following response "
        "(FFR) for subcortical pitch encoding of musical sounds "
        "(Coffey 2016, Chandrasekaran & Kraus 2010)"
    ),
    evidence_count=12,
)

# =====================================================================
# AUDITORY NERVE (AN)
# =====================================================================
# Cranial nerve VIII.  Carries phase-locked spike trains from cochlear
# hair cells to the cochlear nucleus.  The very first neural encoding
# of acoustic information preserving fine temporal structure up to
# ~4 kHz (Heil & Peterson 2015).
# MNI approximate: internal auditory meatus at petrous bone.

AN = BrainRegion(
    name="Auditory Nerve",
    abbreviation="AN",
    hemisphere="bilateral",
    mni_coords=(8, -26, -24),
    brodmann_area=None,
    function=(
        "Peripheral auditory encoding; phase-locked spike trains "
        "carry spectrotemporal information from cochlea to brainstem "
        "(Heil & Peterson 2015)"
    ),
    evidence_count=6,
)

# =====================================================================
# COCHLEAR NUCLEUS (CN)
# =====================================================================
# First central auditory relay.  Contains three subdivisions (AVCN,
# PVCN, DCN) that begin parallel processing of spectral and temporal
# features.  Onset cells for transient detection, chopper cells for
# periodicity encoding (Young & Oertel 2004).
# MNI from Thompson & Bhatt 2017 brainstem atlas.

CN = BrainRegion(
    name="Cochlear Nucleus",
    abbreviation="CN",
    hemisphere="bilateral",
    mni_coords=(10, -38, -32),
    brodmann_area=None,
    function=(
        "First central auditory processing station; parallel spectral "
        "and temporal feature extraction via specialised cell types "
        "(Young & Oertel 2004)"
    ),
    evidence_count=5,
)

# =====================================================================
# SUPERIOR OLIVARY COMPLEX (SOC)
# =====================================================================
# First site of binaural convergence.  Computes interaural time
# differences (ITD) and interaural level differences (ILD) for
# spatial hearing and auditory scene analysis.  Medial superior
# olive (MSO) for ITD, lateral superior olive (LSO) for ILD.
# MNI from Thompson & Bhatt 2017 brainstem atlas.

SOC = BrainRegion(
    name="Superior Olivary Complex",
    abbreviation="SOC",
    hemisphere="bilateral",
    mni_coords=(6, -34, -24),
    brodmann_area=None,
    function=(
        "First binaural processing stage; computes interaural time "
        "and level differences for spatial hearing and auditory "
        "scene analysis (Grothe 2010)"
    ),
    evidence_count=4,
)

# =====================================================================
# PERIAQUEDUCTAL GRAY (PAG)
# =====================================================================
# Midbrain structure surrounding the cerebral aqueduct.  Critical
# for autonomic regulation of emotional responses: mediates chills,
# piloerection, and respiratory changes during musical peaks.
# Also involved in emotional vocalisation and pain modulation.
# MNI from Blood & Zatorre 2001 PET peak during musical chills.

PAG = BrainRegion(
    name="Periaqueductal Gray",
    abbreviation="PAG",
    hemisphere="bilateral",
    mni_coords=(0, -30, -10),
    brodmann_area=None,
    function=(
        "Autonomic and emotional regulation; mediates chills, "
        "piloerection, and respiratory changes during peak musical "
        "moments (Blood & Zatorre 2001, Goldstein 1983)"
    ),
    evidence_count=8,
)

# =====================================================================
# CONVENIENCE TUPLE
# =====================================================================

ALL_BRAINSTEM: tuple[BrainRegion, ...] = (
    IC,
    AN,
    CN,
    SOC,
    PAG,
)
"""All brainstem regions in ascending pathway order."""

__all__ = [
    "IC",
    "AN",
    "CN",
    "SOC",
    "PAG",
    "ALL_BRAINSTEM",
]
