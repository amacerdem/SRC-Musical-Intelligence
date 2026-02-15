"""Region: Caudate Nucleus (caudate)

Anticipatory reward; dopamine release peaks 10-15s before consummatory
pleasure reflecting prediction-based 'wanting' (Salimpoor 2011, r=0.71).

MNI Coordinates: (12, 10, 10)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 19 citations
Key References: Salimpoor 2011, Zatorre & Salimpoor 2013
"""
from ._region import Region

caudate = Region(
    index=14,
    name="Caudate Nucleus",
    abbreviation="caudate",
    hemisphere="bilateral",
    mni_coords=(12, 10, 10),
    brodmann_area=None,
    group="subcortical",
)
