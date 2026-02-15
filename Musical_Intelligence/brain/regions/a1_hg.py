"""Region: Primary Auditory Cortex (Heschl's Gyrus) (A1_HG)

Tonotopic frequency analysis; first cortical stage of spectral decomposition
with rightward lateralisation for pitch, leftward for temporal fine structure.

MNI Coordinates: (48, -18, 8)
Brodmann Area: BA 41
Hemisphere: bilateral
Evidence: 42 citations
Key References: Zatorre 2002, Patterson 2002
"""
from ._region import Region

A1_HG = Region(
    index=0,
    name="Primary Auditory Cortex (Heschl's Gyrus)",
    abbreviation="A1_HG",
    hemisphere="bilateral",
    mni_coords=(48, -18, 8),
    brodmann_area=41,
    group="cortical",
)
