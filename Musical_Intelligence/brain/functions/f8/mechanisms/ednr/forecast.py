"""EDNR F-Layer -- Forecast (2D).

Expertise-dependent network reorganization forward predictions:

  optimal_config_pred    -- Network topology prediction [0, 1]
  processing_efficiency  -- Task performance prediction [0, 1]

H3 consumed (tuples 14-15 from demand spec):
    (8, 3, 0, 2)    loudness value H3 L2               -- loudness at 100ms
    (8, 16, 20, 2)  loudness entropy H16 L2            -- loudness entropy 1s

optimal_config_pred forecasts the optimal network configuration for upcoming
auditory processing based on within-connectivity (f01) and expertise
signature (f04). Uses an 8-second XTI window reflecting the slow dynamics
of network reconfiguration.

processing_efficiency predicts how efficiently the auditory system will
process upcoming input given current compartmentalisation and stimulus
complexity (loudness entropy).

Dependencies:
    E-layer f01 (within_connectivity)
    E-layer f04 (expertise_signature)
    P-layer current_compartm
    R3[8] loudness (stimulus complexity proxy)
    H3 loudness tuples (complexity dynamics)

Papadaki et al. 2023: aspiring professionals show greater auditory network
    strength (Cohen's d=0.70) and global efficiency (d=0.70) that correlates
    with behavioral performance (rho=0.36, r=0.35).

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/ednr/f_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_LOUD_VAL_100MS = (8, 3, 0, 2)           # #14: loudness at 100ms
_LOUD_ENTROPY_1S = (8, 16, 20, 2)        # #15: loudness entropy 1s

# -- R3 feature indices -------------------------------------------------------
_LOUDNESS = 8


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """F-layer: 2D predictions for network configuration and efficiency.

    optimal_config_pred forecasts the optimal network topology for upcoming
    auditory input. Combines within-connectivity (f01) with expertise
    signature (f04) to predict converging toward a more compartmentalized,
    expert-like configuration. XTI window ~8s.

    processing_efficiency predicts how efficiently the auditory system will
    process upcoming input given current network state. Based on Papadaki
    et al. 2023: aspiring professionals show greater auditory network
    strength (Cohen's d=0.70) correlating with behavioural performance.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03, f04)`` from extraction layer.
        m_outputs: ``(network_architecture, compartmentalization_idx)``
            from temporal integration layer.
        p_outputs: ``(current_compartm, network_isolation)`` from P-layer.

    Returns:
        ``(optimal_config_pred, processing_efficiency)`` each ``(B, T)``.
    """
    f01, _f02, _f03, f04 = e_outputs
    current_compartm, _network_isolation = p_outputs

    # -- H3 features --
    loud_entropy_1s = h3_features[_LOUD_ENTROPY_1S]

    # optimal_config_pred: predict optimal network configuration
    # Combines within-connectivity and expertise signature. XTI ~8s.
    # sigma(0.50 * f01 + 0.50 * f04)
    optimal_config_pred = torch.sigmoid(
        0.50 * f01
        + 0.50 * f04
    )

    # processing_efficiency: predict task performance at 0.5-1s horizon
    # Papadaki et al. 2023: network strength -> interval recognition (rho=0.36)
    # and BGS (r=0.35). Loudness entropy at 1s gauges stimulus complexity.
    # sigma(0.40 * current_compartm + 0.30 * f04 + 0.30 * loud_entropy_1s)
    processing_efficiency = torch.sigmoid(
        0.40 * current_compartm
        + 0.30 * f04
        + 0.30 * loud_entropy_1s
    )

    return optimal_config_pred, processing_efficiency
