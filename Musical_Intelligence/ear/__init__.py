"""Ear layer — signal processing (R3 spectral + H3 temporal).

The ear layer transforms raw audio (as mel spectrograms) into the
perceptual feature representations consumed by the brain layer:

- **R3**: Dense 97-D spectral feature vector at every time step.
- **H3**: Sparse temporal morphology features computed on demand.

Quick start
-----------
::

    from Musical_Intelligence.ear import R3Extractor, H3Extractor

    r3 = R3Extractor()
    r3_out = r3.extract(mel)            # mel: (B, 128, T)

    h3 = H3Extractor()
    h3_out = h3.extract(r3_out.features, demand_set)

Re-exports
----------
From ``ear.r3``: R3Extractor, R3Output
From ``ear.h3``: H3Extractor, H3Output
"""

from __future__ import annotations

from .h3 import H3Extractor, H3Output
from .r3 import R3Extractor, R3Output

__all__ = [
    "R3Extractor",
    "R3Output",
    "H3Extractor",
    "H3Output",
]
