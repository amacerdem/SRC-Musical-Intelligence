"""
Endogenous Opioids (mu-opioid) -- Hedonic "liking" and consummatory pleasure.

The mu-opioid system mediates the hedonic "liking" response -- the raw
pleasurable sensation experienced at the moment of musical consummation.
This is dissociable from dopaminergic "wanting" (Berridge 2003):

    DA "wanting":  Motivational drive, anticipation, prediction error.
    Opioid "liking":  Hedonic impact, conscious pleasure, "felt goodness".

Hedonic hotspots are small (< 1 cm^3) subregions within the NAcc shell
and ventral pallidum where mu-opioid receptor stimulation amplifies
hedonic reactions.  Outside these hotspots, opioid signalling modulates
but does not generate pleasure (Berridge & Kringelbach 2015).

Key papers:
    - Berridge 2003: Wanting vs liking dissociation
    - Berridge & Kringelbach 2015: Hedonic hotspot circuitry
    - Nummenmaa et al. 2025: Music-evoked opioid release (PET)
    - Pecina & Berridge 2005: NAcc shell hotspot mapping
    - Smith & Berridge 2007: Ventral pallidum hedonic hotspot
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


# =====================================================================
# OPIOID REGION DEFINITIONS
# =====================================================================

@dataclass(frozen=True)
class OpioidRegionSpec:
    """Specification of an opioid-relevant brain region.

    Attributes:
        region_key:     Key used in NeurochemicalState.write/read.
        full_name:      Anatomical name.
        role:           Functional role of mu-opioid in this region.
        is_hotspot:     True if this region contains a hedonic hotspot.
        hotspot_volume: Approximate hotspot volume in mm^3 (0 if not a hotspot).
        citation:       Primary supporting citation.
    """

    region_key: str
    full_name: str
    role: str
    is_hotspot: bool
    hotspot_volume: float
    citation: str


OPIOID_REGIONS: Tuple[OpioidRegionSpec, ...] = (
    OpioidRegionSpec(
        region_key="nacc_shell",
        full_name="Nucleus Accumbens Shell",
        role=(
            "Primary hedonic hotspot; mu-opioid stimulation here "
            "amplifies consummatory pleasure reactions. Rostrodorsal "
            "medial shell is the most reliable site for hedonic "
            "enhancement in both rodent and human studies"
        ),
        is_hotspot=True,
        hotspot_volume=8.0,  # mm^3, Pecina & Berridge 2005
        citation="Pecina & Berridge 2005; Nummenmaa 2025",
    ),
    OpioidRegionSpec(
        region_key="vp",
        full_name="Ventral Pallidum",
        role=(
            "Second hedonic hotspot in the pleasure circuit; the VP "
            "posterior region amplifies hedonic 'liking' reactions and "
            "is functionally linked to NAcc shell opioid output"
        ),
        is_hotspot=True,
        hotspot_volume=6.0,  # mm^3, Smith & Berridge 2007
        citation="Smith & Berridge 2007",
    ),
    OpioidRegionSpec(
        region_key="parabrachial",
        full_name="Parabrachial Nucleus",
        role=(
            "Brainstem hedonic hotspot; opioid signalling here "
            "modulates basic sensory pleasure including taste and "
            "potentially auditory hedonic responses. Projects to "
            "NAcc shell and VP to coordinate hedonic evaluation"
        ),
        is_hotspot=True,
        hotspot_volume=3.0,  # mm^3, estimated from Berridge & Kringelbach 2015
        citation="Berridge & Kringelbach 2015",
    ),
)
"""All opioid-relevant regions in the hedonic circuit."""


# =====================================================================
# HEDONIC HOTSPOT DEFINITIONS
# =====================================================================

@dataclass(frozen=True)
class HedonicHotspot:
    """A circumscribed brain region where mu-opioid stimulation
    amplifies hedonic "liking" reactions.

    Hotspots are remarkably small -- typically < 10 mm^3 in rodents
    (scaled to ~25 mm^3 in humans).  They form a distributed network:
    NAcc shell -> VP -> parabrachial, where each hotspot can amplify
    liking independently but their interaction produces maximal hedonic
    impact (Berridge & Kringelbach 2015).

    Attributes:
        name:          Hotspot identifier.
        region_key:    Matching OPIOID_REGIONS region_key.
        mni_centroid:  Approximate MNI152 centroid (x, y, z) in humans.
        receptor:      Dominant receptor subtype (mu, delta, kappa).
        effect:        Direction of hedonic effect when stimulated.
        mechanism:     Brief description of the molecular mechanism.
        citation:      Primary citation.
    """

    name: str
    region_key: str
    mni_centroid: Tuple[int, int, int]
    receptor: str
    effect: str
    mechanism: str
    citation: str


HEDONIC_HOTSPOTS: Tuple[HedonicHotspot, ...] = (
    HedonicHotspot(
        name="NAcc medial shell hotspot",
        region_key="nacc_shell",
        mni_centroid=(8, 14, -6),
        receptor="mu",
        effect="amplifies hedonic liking",
        mechanism=(
            "mu-opioid agonist (DAMGO) in rostrodorsal medial shell "
            "doubles hedonic 'liking' reactions without changing 'wanting'; "
            "blocked by naloxone (Pecina & Berridge 2005)"
        ),
        citation="Pecina & Berridge 2005",
    ),
    HedonicHotspot(
        name="Ventral pallidum posterior hotspot",
        region_key="vp",
        mni_centroid=(-2, 0, -6),
        receptor="mu",
        effect="amplifies hedonic liking",
        mechanism=(
            "mu-opioid stimulation in posterior VP enhances hedonic "
            "reactions; lesions here produce anhedonia -- the only "
            "brain site where lesion abolishes both liking and wanting "
            "(Smith & Berridge 2007)"
        ),
        citation="Smith & Berridge 2007",
    ),
    HedonicHotspot(
        name="Parabrachial nucleus hotspot",
        region_key="parabrachial",
        mni_centroid=(4, -32, -28),
        receptor="mu",
        effect="modulates sensory hedonic tone",
        mechanism=(
            "Opioid signalling in parabrachial nucleus modulates "
            "basic sensory pleasure; projects to NAcc shell to "
            "coordinate evaluation across modalities "
            "(Berridge & Kringelbach 2015)"
        ),
        citation="Berridge & Kringelbach 2015",
    ),
)
"""Known hedonic hotspots in the mu-opioid pleasure circuit."""


__all__ = [
    "OpioidRegionSpec",
    "OPIOID_REGIONS",
    "HedonicHotspot",
    "HEDONIC_HOTSPOTS",
]
