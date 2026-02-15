"""Region: Temporal Pole (TP)

Semantic memory hub; abstract musical knowledge, genre schemas, conceptual
associations.

MNI Coordinates: (42, 12, -32)
Brodmann Area: BA 38
Hemisphere: bilateral
Evidence: 7 citations
Key References: Patterson 2007, Peretz & Coltheart 2003
"""
from ._region import Region

TP = Region(
    index=11,
    name="Temporal Pole",
    abbreviation="TP",
    hemisphere="bilateral",
    mni_coords=(42, 12, -32),
    brodmann_area=38,
    group="cortical",
)
