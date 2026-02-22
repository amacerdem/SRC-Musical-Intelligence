"""EDNR M-Layer -- Temporal Integration (2D).

Two network architecture descriptors derived from E-layer outputs:

  network_architecture       -- Connectivity strength measure [0, 1]
  compartmentalization_idx   -- Musician vs non-musician compartmentalization [0, ~3]

H3 consumed (tuples 8-11 from demand spec):
    (33, 3, 0, 2)    x_l4l5 value H3 L2               -- cross-network coupling 100ms
    (33, 3, 2, 2)    x_l4l5 std H3 L2                 -- cross coupling variability 100ms
    (33, 16, 1, 2)   x_l4l5 mean H16 L2               -- mean cross coupling over 1s
    (33, 16, 20, 2)  x_l4l5 entropy H16 L2            -- cross coupling entropy 1s

The M-layer H3 demands provide multi-scale temporal context for the cross-
network coupling dynamics. The two output dimensions are:

    network_architecture = sigma(0.50 * f01 + 0.50 * f02)
    compartmentalization_idx = f03 (direct pass-through from E-layer ratio)

Leipold et al. 2021: structural subnetwork including bilateral auditory,
    frontal, and parietal regions (pFWE<0.05, n=153).
Cui et al. 2025: 1-year training does NOT change WM -- slow structural
    change constraint.
Paraskevopoulos 2022: 192 vs 106 edges (NM vs M).

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/ednr/m_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 8-11 from demand spec) ---------------------------------
_CROSS_VAL_100MS = (33, 3, 0, 2)         # #8: cross-network coupling 100ms
_CROSS_STD_100MS = (33, 3, 2, 2)         # #9: cross coupling variability 100ms
_CROSS_MEAN_1S = (33, 16, 1, 2)          # #10: mean cross coupling over 1s
_CROSS_ENTROPY_1S = (33, 16, 20, 2)      # #11: cross coupling entropy 1s


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D temporal integration from E-layer outputs.

    Computes two network architecture descriptors:
        network_architecture: balanced combination of within- and between-
            connectivity (f01, f02) summarising overall network topology.
        compartmentalization_idx: carries forward E-layer ratio (f03 =
            f01 / (f02 + eps)). Constrained by the slow structural plasticity
            finding from Cui et al. 2025 (1-year training does not change WM).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.

    Returns:
        ``(network_architecture, compartmentalization_idx)`` each ``(B, T)``.
    """
    f01, f02, f03, _f04 = e_outputs

    # network_architecture: balanced within + between connectivity
    # Leipold et al. 2021: structural subnetwork pFWE<0.05, n=153
    # sigma(0.50 * f01 + 0.50 * f02)
    network_architecture = torch.sigmoid(
        0.50 * f01
        + 0.50 * f02
    )

    # compartmentalization_idx: direct pass-through of E-layer ratio
    # Paraskevopoulos 2022: 192 vs 106 edges (NM vs M)
    # Cui et al. 2025: 1-year training does NOT change WM -- slow structural
    # change. The ratio captures this slow-dynamics compartmentalization.
    compartmentalization_idx = f03

    return network_architecture, compartmentalization_idx
