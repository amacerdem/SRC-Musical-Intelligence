"""Region: Superior Temporal Sulcus (STS)

Multimodal stream integration; voice/music discrimination, audiovisual binding.

MNI Coordinates: (54, -32, 4)
Brodmann Area: BA 21
Hemisphere: bilateral
Evidence: 15 citations
Key References: Belin 2000, Peretz & Coltheart 2003
"""
from ._region import Region

STS = Region(
    index=2,
    name="Superior Temporal Sulcus",
    abbreviation="STS",
    hemisphere="bilateral",
    mni_coords=(54, -32, 4),
    brodmann_area=21,
    group="cortical",
)
