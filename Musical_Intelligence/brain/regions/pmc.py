"""Region: Premotor Cortex (PMC)

Auditory-motor coupling; rhythm entrainment and sensorimotor synchronisation.

MNI Coordinates: (46, 0, 48)
Brodmann Area: BA 6
Hemisphere: bilateral
Evidence: 14 citations
Key References: Chen 2008, Zatorre 2007
"""
from ._region import Region

PMC = Region(
    index=9,
    name="Premotor Cortex",
    abbreviation="PMC",
    hemisphere="bilateral",
    mni_coords=(46, 0, 48),
    brodmann_area=6,
    group="cortical",
)
