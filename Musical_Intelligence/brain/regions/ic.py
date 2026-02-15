"""Region: Inferior Colliculus (IC)

Midbrain auditory relay; generates frequency-following response (FFR) for
subcortical pitch encoding of musical sounds.

MNI Coordinates: (0, -34, -8)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 12 citations
Key References: Coffey 2016, Chandrasekaran & Kraus 2010
"""
from ._region import Region

IC = Region(
    index=21,
    name="Inferior Colliculus",
    abbreviation="IC",
    hemisphere="bilateral",
    mni_coords=(0, -34, -8),
    brodmann_area=None,
    group="brainstem",
)
