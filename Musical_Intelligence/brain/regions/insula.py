"""Region: Insula (insula)

Interoceptive awareness; integrates bodily arousal signals with emotional
context for conscious musical feeling states.

MNI Coordinates: (36, 16, 0)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 14 citations
Key References: Craig 2009, Koelsch 2014
"""
from ._region import Region

insula = Region(
    index=20,
    name="Insula",
    abbreviation="insula",
    hemisphere="bilateral",
    mni_coords=(36, 16, 0),
    brodmann_area=None,
    group="subcortical",
)
