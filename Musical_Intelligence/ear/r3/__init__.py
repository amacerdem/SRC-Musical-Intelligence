"""R3 spectral feature extraction — 128-D dense spectral vector.

Provides the R3Extractor which auto-discovers 11 spectral groups (A-K),
executes them in a 3-stage DAG, normalizes outputs, and produces a dense
(B, T, 128) feature tensor with all values in [0, 1].

Quick start
-----------
::

    from Musical_Intelligence.ear.r3 import R3Extractor

    extractor = R3Extractor()
    r3_output = extractor.extract(mel)       # mel: (B, 128, T)
    features = r3_output.features            # (B, T, 128) in [0, 1]
    names = r3_output.feature_names          # tuple of 128 strings

Classes
-------
R3Extractor
    Orchestrates all 11 spectral groups into a 128-D feature vector.
R3Output
    Frozen dataclass wrapping the (B, T, 128) tensor and metadata.
"""

from __future__ import annotations

from .extractor import R3Extractor, R3Output

__all__ = [
    "R3Extractor",
    "R3Output",
]
