"""Region: Ventral Tegmental Area (VTA)

Dopaminergic source nucleus; generates reward prediction error signals
during unexpected harmonic progressions and timbral changes.

MNI Coordinates: (0, -16, -8)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 18 citations
Key References: Schultz 1997, Ferreri 2019
"""
from ._region import Region

VTA = Region(
    index=12,
    name="Ventral Tegmental Area",
    abbreviation="VTA",
    hemisphere="bilateral",
    mni_coords=(0, -16, -8),
    brodmann_area=None,
    group="subcortical",
)
