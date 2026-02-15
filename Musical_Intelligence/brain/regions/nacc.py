"""Region: Nucleus Accumbens (NAcc)

Consummatory reward hub; integrates dopaminergic and opioidergic signals
for peak musical pleasure (Salimpoor 2011, r=0.84).

MNI Coordinates: (10, 12, -8)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 24 citations
Key References: Salimpoor 2011
"""
from ._region import Region

NAcc = Region(
    index=13,
    name="Nucleus Accumbens",
    abbreviation="NAcc",
    hemisphere="bilateral",
    mni_coords=(10, 12, -8),
    brodmann_area=None,
    group="subcortical",
)
