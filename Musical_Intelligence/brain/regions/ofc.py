"""Region: Orbitofrontal Cortex (OFC)

Reward valuation and hedonic judgement; conscious aesthetic value of musical
stimuli.

MNI Coordinates: (28, 34, -16)
Brodmann Area: BA 11
Hemisphere: bilateral
Evidence: 15 citations
Key References: Blood & Zatorre 2001, Salimpoor 2013
"""
from ._region import Region

OFC = Region(
    index=6,
    name="Orbitofrontal Cortex",
    abbreviation="OFC",
    hemisphere="bilateral",
    mni_coords=(28, 34, -16),
    brodmann_area=11,
    group="cortical",
)
