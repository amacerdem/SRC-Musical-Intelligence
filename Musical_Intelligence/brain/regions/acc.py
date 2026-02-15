"""Region: Anterior Cingulate Cortex (ACC)

Conflict monitoring and prediction error signalling; harmonic violation
detection.

MNI Coordinates: (2, 30, 28)
Brodmann Area: BA 32
Hemisphere: bilateral
Evidence: 12 citations
Key References: Koelsch 2014, Menon 2015
"""
from ._region import Region

ACC = Region(
    index=7,
    name="Anterior Cingulate Cortex",
    abbreviation="ACC",
    hemisphere="bilateral",
    mni_coords=(2, 30, 28),
    brodmann_area=32,
    group="cortical",
)
