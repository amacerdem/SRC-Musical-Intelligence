"""Region: Auditory Nerve (AN)

Peripheral auditory encoding; phase-locked spike trains carry spectrotemporal
information from cochlea to brainstem.

MNI Coordinates: (8, -26, -24)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 6 citations
Key References: Heil & Peterson 2015
"""
from ._region import Region

AN = Region(
    index=22,
    name="Auditory Nerve",
    abbreviation="AN",
    hemisphere="bilateral",
    mni_coords=(8, -26, -24),
    brodmann_area=None,
    group="brainstem",
)
