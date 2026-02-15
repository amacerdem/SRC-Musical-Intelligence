"""Region: Superior Olivary Complex (SOC)

First binaural processing stage; computes interaural time and level
differences for spatial hearing and auditory scene analysis.

MNI Coordinates: (6, -34, -24)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 4 citations
Key References: Grothe 2010
"""
from ._region import Region

SOC = Region(
    index=24,
    name="Superior Olivary Complex",
    abbreviation="SOC",
    hemisphere="bilateral",
    mni_coords=(6, -34, -24),
    brodmann_area=None,
    group="brainstem",
)
