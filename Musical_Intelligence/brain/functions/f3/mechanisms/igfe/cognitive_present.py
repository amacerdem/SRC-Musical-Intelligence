"""IGFE P-Layer -- Cognitive Present (3D).

Three present-processing dimensions for gamma synchronization and dose effects:

  P0: gamma_synchronization   -- Gamma-band phase synchronization [0, 1]
  P1: dose_accumulation       -- Accumulated dose-response signal [0, 1]
  P2: memory_access           -- Gamma-mediated memory access strength [0, 1]

H3 consumed:
    (25, 0, 0, 2)   coupling 25ms L2              -- fast binding
    (25, 1, 0, 2)   coupling 50ms L2              -- fast binding
    (10, 0, 0, 2)   flux 25ms L2                  -- gamma-range onset (reused)
    (25, 16, 14, 2) coupling periodicity 1s L2    -- sustained binding
    (25, 3, 14, 2)  coupling periodicity 100ms L2 -- binding rhythm

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/igfe/IGFE-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_COUPLING_25MS = (25, 0, 0, 2)          # coupling value 25ms L2
_COUPLING_50MS = (25, 1, 0, 2)          # coupling value 50ms L2
_FLUX_25MS = (10, 0, 0, 2)             # spectral flux 25ms L2
_COUPLING_PERIOD_1S = (25, 16, 14, 2)   # coupling periodicity 1s L2
_COUPLING_PERIOD_100MS = (25, 3, 14, 2) # coupling periodicity 100ms L2


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing from H3 features + E outputs.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(E0, E1, E2, E3)`` each ``(B, T)``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    _e0, e1, _e2, e3 = e

    coupling_25ms = h3_features[_COUPLING_25MS]
    coupling_50ms = h3_features[_COUPLING_50MS]
    flux_25ms = h3_features[_FLUX_25MS]
    coupling_period_1s = h3_features[_COUPLING_PERIOD_1S]
    coupling_period_100ms = h3_features[_COUPLING_PERIOD_100MS]

    # P0: Gamma synchronization -- cross-band coupling at gamma timescale
    # Baltus 2018: EEG phase-locking at IGF predicts enhancement magnitude
    p0 = torch.sigmoid(
        0.40 * coupling_25ms + 0.30 * coupling_50ms
        + 0.30 * flux_25ms
    )

    # P1: Dose accumulation -- sustained gamma binding over time
    # Rufener 2016: dose-dependent accumulation during 20-min tACS
    p1 = torch.sigmoid(
        0.50 * e3 + 0.50 * coupling_period_1s
    )

    # P2: Memory access -- gamma-mediated hippocampal access
    # Rufener 2016: memory improvement via gamma-hippocampal coupling
    p2 = torch.sigmoid(
        0.40 * e1 + 0.30 * coupling_period_100ms
        + 0.30 * coupling_period_1s
    )

    return p0, p1, p2
