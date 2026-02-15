"""Region: Hippocampus (hippocampus)

Musical memory encoding and retrieval; familiarity detection, episodic
associations, statistical learning of musical structure.

MNI Coordinates: (28, -22, -12)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 22 citations
Key References: Janata 2009, Watanabe 2008
"""
from ._region import Region

hippocampus = Region(
    index=16,
    name="Hippocampus",
    abbreviation="hippocampus",
    hemisphere="bilateral",
    mni_coords=(28, -22, -12),
    brodmann_area=None,
    group="subcortical",
)
