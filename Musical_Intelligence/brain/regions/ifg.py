"""Region: Inferior Frontal Gyrus (Broca's Area) (IFG)

Musical syntax processing; ERAN for unexpected harmonic events, hierarchical
sequence parsing.

MNI Coordinates: (48, 18, 8)
Brodmann Area: BA 44
Hemisphere: R
Evidence: 27 citations
Key References: Koelsch 2011, Sammler 2013
"""
from ._region import Region

IFG = Region(
    index=3,
    name="Inferior Frontal Gyrus (Broca's Area)",
    abbreviation="IFG",
    hemisphere="R",
    mni_coords=(48, 18, 8),
    brodmann_area=44,
    group="cortical",
)
