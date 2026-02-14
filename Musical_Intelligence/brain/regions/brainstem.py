"""Brainstem brain regions for the C3 architecture.

Five brainstem regions with MNI152 coordinates derived from published
atlases: Harvard Ascending Arousal Network Atlas (Edlow 2012), Coffey
et al. 2016, Chandrasekaran & Kraus 2010, Thompson & Bhatt 2017,
Blood & Zatorre 2001.

Spatial note: brainstem structures are small and deep; MNI coordinates
carry higher spatial uncertainty (+/- 2-3 mm) than cortical regions.
"""
from __future__ import annotations

from ...contracts.dataclasses import BrainRegion


# ── Ascending Auditory Pathway ───────────────────────────────────────

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

AN = BrainRegion(
    name="Auditory Nerve",
    abbreviation="AN",
    hemisphere="bilateral",
    mni_coords=(8, -26, -24),
    brodmann_area=None,
    function=(
        "Peripheral auditory encoding; phase-locked spike trains carry "
        "spectrotemporal information from cochlea to brainstem "
        "(Heil & Peterson 2015)"
    ),
    evidence_count=6,
)

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

SOC = BrainRegion(
    name="Superior Olivary Complex",
    abbreviation="SOC",
    hemisphere="bilateral",
    mni_coords=(6, -34, -24),
    brodmann_area=None,
    function=(
        "First binaural processing stage; computes interaural time and "
        "level differences for spatial hearing and auditory scene "
        "analysis (Grothe 2010)"
    ),
    evidence_count=4,
)

# ── Parallel Emotional Pathway ───────────────────────────────────────

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

# ── Collection ───────────────────────────────────────────────────────

BRAINSTEM_REGIONS = (
    IC,
    AN,
    CN,
    SOC,
    PAG,
)
"""All 5 brainstem regions."""
