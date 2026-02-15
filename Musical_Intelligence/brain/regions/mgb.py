"""Region: Thalamus (Medial Geniculate Body) (MGB)

Primary auditory relay; gates ascending spectrotemporal information to
cortex with attentional modulation.

MNI Coordinates: (14, -24, -2)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 11 citations
Key References: Suga 2008, Winer 2005
"""
from ._region import Region

MGB = Region(
    index=18,
    name="Thalamus (Medial Geniculate Body)",
    abbreviation="MGB",
    hemisphere="bilateral",
    mni_coords=(14, -24, -2),
    brodmann_area=None,
    group="subcortical",
)
