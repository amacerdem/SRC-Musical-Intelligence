"""R3 spectral feature extraction — 97-D dense spectral vector.

Provides the R3Extractor which auto-discovers 9 spectral groups (A-K,
excluding dissolved E and I), executes them in a 2-stage DAG, normalizes
outputs, and produces a dense (B, T, 97) feature tensor with all values
in [0, 1].

Quick start
-----------
::

    from Musical_Intelligence.ear.r3 import R3Extractor

    extractor = R3Extractor()
    r3_output = extractor.extract(mel)       # mel: (B, 128, T)
    features = r3_output.features            # (B, T, 97) in [0, 1]
    names = r3_output.feature_names          # tuple of 97 strings

Classes
-------
R3Extractor
    Orchestrates all 9 spectral groups into a 97-D feature vector.
R3Output
    Frozen dataclass wrapping the (B, T, 97) tensor and metadata.
"""

from __future__ import annotations

from .extractor import R3Extractor, R3Output

__all__ = [
    "R3Extractor",
    "R3Output",
]
