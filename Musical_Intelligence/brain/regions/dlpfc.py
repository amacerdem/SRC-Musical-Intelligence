"""Region: Dorsolateral Prefrontal Cortex (dlPFC)

Working memory and executive control; maintains tonal context for expectation.

MNI Coordinates: (42, 32, 30)
Brodmann Area: BA 46
Hemisphere: bilateral
Evidence: 13 citations
Key References: Zatorre 1994, Owen 2005
"""
from ._region import Region

dlPFC = Region(
    index=4,
    name="Dorsolateral Prefrontal Cortex",
    abbreviation="dlPFC",
    hemisphere="bilateral",
    mni_coords=(42, 32, 30),
    brodmann_area=46,
    group="cortical",
)
