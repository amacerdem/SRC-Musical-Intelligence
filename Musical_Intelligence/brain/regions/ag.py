"""Region: Angular Gyrus (AG)

Cross-modal integration; binds auditory, visual, somatosensory for holistic
musical experience.

MNI Coordinates: (48, -60, 30)
Brodmann Area: BA 39
Hemisphere: bilateral
Evidence: 8 citations
Key References: Seghier 2013, Koelsch 2014
"""
from ._region import Region

AG = Region(
    index=10,
    name="Angular Gyrus",
    abbreviation="AG",
    hemisphere="bilateral",
    mni_coords=(48, -60, 30),
    brodmann_area=39,
    group="cortical",
)
