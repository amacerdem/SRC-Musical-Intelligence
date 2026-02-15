"""Region: Periaqueductal Gray (PAG)

Autonomic and emotional regulation; mediates chills, piloerection, and
respiratory changes during peak musical moments. Not part of ascending
auditory pathway.

MNI Coordinates: (0, -30, -10)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 8 citations
Key References: Blood & Zatorre 2001, Goldstein 1983
"""
from ._region import Region

PAG = Region(
    index=25,
    name="Periaqueductal Gray",
    abbreviation="PAG",
    hemisphere="bilateral",
    mni_coords=(0, -30, -10),
    brodmann_area=None,
    group="brainstem",
)
