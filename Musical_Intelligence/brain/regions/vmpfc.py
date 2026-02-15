"""Region: Ventromedial Prefrontal Cortex (vmPFC)

Subjective value computation; reward integration, tonality tracking, musical
autobiography.

MNI Coordinates: (2, 46, -10)
Brodmann Area: BA 10
Hemisphere: bilateral
Evidence: 17 citations
Key References: Janata 2009, Blood & Zatorre 2001
"""
from ._region import Region

vmPFC = Region(
    index=5,
    name="Ventromedial Prefrontal Cortex",
    abbreviation="vmPFC",
    hemisphere="bilateral",
    mni_coords=(2, 46, -10),
    brodmann_area=10,
    group="cortical",
)
