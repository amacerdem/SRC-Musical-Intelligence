"""Region: Supplementary Motor Area (SMA)

Internal timing and motor planning; beat-level metric structure during passive
listening.

MNI Coordinates: (2, -2, 56)
Brodmann Area: BA 6
Hemisphere: bilateral
Evidence: 21 citations
Key References: Grahn & Rowe 2009, 2013
"""
from ._region import Region

SMA = Region(
    index=8,
    name="Supplementary Motor Area",
    abbreviation="SMA",
    hemisphere="bilateral",
    mni_coords=(2, -2, 56),
    brodmann_area=6,
    group="cortical",
)
