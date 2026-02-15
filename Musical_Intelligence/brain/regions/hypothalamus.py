"""Region: Hypothalamus (hypothalamus)

Autonomic regulation; mediates physiological responses (heart rate, chills,
skin conductance) to emotionally powerful music.

MNI Coordinates: (0, -4, -8)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 9 citations
Key References: Blood & Zatorre 2001
"""
from ._region import Region

hypothalamus = Region(
    index=19,
    name="Hypothalamus",
    abbreviation="hypothalamus",
    hemisphere="bilateral",
    mni_coords=(0, -4, -8),
    brodmann_area=None,
    group="subcortical",
)
