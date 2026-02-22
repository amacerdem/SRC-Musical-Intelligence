"""EDNR P-Layer -- Cognitive Present (2D).

Two present-moment network organisation states:

  current_compartm   -- Real-time network compartmentalization level [0, 1]
  network_isolation   -- Boundary maintenance between functional networks [0, 1]

H3 consumed (tuples 12-13 from demand spec):
    (16, 3, 0, 2)    spectral_flatness value H3 L2     -- flatness at 100ms
    (16, 16, 2, 2)   spectral_flatness std H16 L2      -- flatness variability 1s

P-layer outputs capture the moment-by-moment expertise-dependent processing
state. current_compartm normalizes the E-layer ratio (f03) to [0,1] via
clamping to [0,3] and dividing by 3, then combines with within-connectivity.
network_isolation captures boundary maintenance between functional networks.

Paraskevopoulos 2022: PTE-based multilink analysis reveals real-time network
    interaction patterns in musicians.
Moller et al. 2021: musicians show only local CT correlations while NM show
    distributed V1-HG correlations; FA cluster p<0.001 (left IFOF) -- BCG
    associated with FA in NM only (musicians p=0.64).

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/ednr/p_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 12-13 from demand spec) --------------------------------
_FLATNESS_VAL_100MS = (16, 3, 0, 2)      # #12: flatness at 100ms
_FLATNESS_STD_1S = (16, 16, 2, 2)        # #13: flatness variability 1s

# -- R3 indices ----------------------------------------------------------------
_SPECTRAL_FLATNESS = 16


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present-moment network state.

    Computes the real-time cognitive state of expertise-dependent network
    organisation:
        current_compartm: normalised compartmentalisation ratio combined
            with within-network coupling mean.
        network_isolation: boundary maintenance between functional networks
            based on flatness dynamics and network architecture.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.
        m_outputs: ``(network_architecture, compartmentalization_idx)``
            each ``(B, T)``.

    Returns:
        ``(current_compartm, network_isolation)`` each ``(B, T)``.
    """
    _f01, _f02, f03, _f04 = e_outputs
    network_architecture, _compartmentalization_idx = m_outputs

    flatness_val_100ms = h3_features[_FLATNESS_VAL_100MS]
    flatness_std_1s = h3_features[_FLATNESS_STD_1S]

    # -- H3 features for within-network mean (reused from E-layer) --
    # We use the within_mean_1s H3 tuple from the E-layer demand.
    # Key: (25, 16, 1, 2)
    within_mean_1s = h3_features[(25, 16, 1, 2)]

    # current_compartm: real-time compartmentalisation readout
    # Paraskevopoulos 2022: PTE-based multilink analysis reveals real-time
    # network interaction patterns in musicians.
    # sigma(0.50 * f03.clamp(0,3)/3.0 + 0.50 * within_mean_1s)
    f03_norm = f03.clamp(0.0, 3.0) / 3.0
    current_compartm = torch.sigmoid(
        0.50 * f03_norm
        + 0.50 * within_mean_1s
    )

    # network_isolation: boundary maintenance between networks
    # Moller et al. 2021: musicians show only local CT correlations while NM
    # show distributed V1-HG correlations; FA cluster p<0.001 (left IFOF).
    # sigma(0.35 * flatness_val_100ms + 0.30 * flatness_std_1s
    #        + 0.35 * network_architecture)
    network_isolation = torch.sigmoid(
        0.35 * flatness_val_100ms
        + 0.30 * flatness_std_1s
        + 0.35 * network_architecture
    )

    return current_compartm, network_isolation
