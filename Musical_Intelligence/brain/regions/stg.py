"""Region: Superior Temporal Gyrus (STG)

Auditory association cortex; melody, harmony, timbre through spectrotemporal
pattern recognition.

MNI Coordinates: (58, -22, 4)
Brodmann Area: BA 22
Hemisphere: bilateral
Evidence: 38 citations
Key References: Griffiths & Warren 2002, Alluri 2012
"""
from ._region import Region

STG = Region(
    index=1,
    name="Superior Temporal Gyrus",
    abbreviation="STG",
    hemisphere="bilateral",
    mni_coords=(58, -22, 4),
    brodmann_area=22,
    group="cortical",
)
