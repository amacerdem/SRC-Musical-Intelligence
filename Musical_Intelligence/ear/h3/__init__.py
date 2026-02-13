"""H3 temporal morphology extraction — sparse demand-driven features.

Provides the H3Extractor which computes temporal morph features on demand,
using attention-weighted windows across multiple event horizons.

Quick start
-----------
::

    from Musical_Intelligence.ear.h3 import H3Extractor

    extractor = H3Extractor()
    h3_output = extractor.extract(r3_tensor, demand_set)
    # h3_output.features: Dict[(r3_idx, horizon, morph, law)] -> (B, T)
    # h3_output.n_tuples: number of computed tuples

Classes
-------
H3Extractor
    Orchestrates sparse temporal morphology extraction via 7-phase pipeline.
H3Output
    Frozen dataclass wrapping the sparse feature dictionary and count.
"""

from __future__ import annotations

from .extractor import H3Extractor, H3Output

__all__ = [
    "H3Extractor",
    "H3Output",
]
