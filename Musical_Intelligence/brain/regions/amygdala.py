"""Region: Amygdala (amygdala)

Emotional valence tagging; responds to dissonance, tension, and affective
salience in musical stimuli (Koelsch 2014).

MNI Coordinates: (24, -4, -18)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 31 citations
Key References: Koelsch 2014, Trost 2012
"""
from ._region import Region

amygdala = Region(
    index=15,
    name="Amygdala",
    abbreviation="amygdala",
    hemisphere="bilateral",
    mni_coords=(24, -4, -18),
    brodmann_area=None,
    group="subcortical",
)
