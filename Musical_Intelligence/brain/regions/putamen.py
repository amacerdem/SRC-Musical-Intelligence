"""Region: Putamen (putamen)

Beat-based motor timing; entrainment to regular rhythmic structures via
basal ganglia-cortical loops (Grahn & Rowe 2009, d=0.67).

MNI Coordinates: (26, 4, 2)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 16 citations
Key References: Grahn & Rowe 2009
"""
from ._region import Region

putamen = Region(
    index=17,
    name="Putamen",
    abbreviation="putamen",
    hemisphere="bilateral",
    mni_coords=(26, 4, 2),
    brodmann_area=None,
    group="subcortical",
)
