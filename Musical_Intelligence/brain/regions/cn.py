"""Region: Cochlear Nucleus (CN)

First central auditory processing station; parallel spectral and temporal
feature extraction via specialised cell types (AVCN onset cells, PVCN
choppers, DCN spectral notch).

MNI Coordinates: (10, -38, -32)
Brodmann Area: --
Hemisphere: bilateral
Evidence: 5 citations
Key References: Young & Oertel 2004
"""
from ._region import Region

CN = Region(
    index=23,
    name="Cochlear Nucleus",
    abbreviation="CN",
    hemisphere="bilateral",
    mni_coords=(10, -38, -32),
    brodmann_area=None,
    group="brainstem",
)
