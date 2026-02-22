"""PWUP F-Layer -- Forecast (3D).

Forward predictions for precision dynamics:
  F0: precision_adjustment     (predicted change in precision at next time step)
  F1: context_uncertainty      (predicted contextual uncertainty ~500ms ahead)
  F2: response_attenuation     (predicted degree of PE suppression)

H3 demands consumed:
  tonal_stability:  (41,16,20,0)  entropy at 1s memory
  onset_strength:   (10,3,14,2)   periodicity at 100ms integration
  periodicity:      (5,16,14,2)   periodicity at 1s integration

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/pwup/
Vuust et al. 2022: precision expectations adjust over time in music perception.
Friston 2005: precision is updated via gradient descent on free energy.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_TONAL_STAB_H16_ENT = (41, 16, 20, 0)       # tonal_stability entropy at 1s memory
_ONSET_H3_PERIOD = (10, 3, 14, 2)            # onset_strength periodicity at 100ms
_PERIODICITY_H16_PERIOD = (5, 16, 14, 2)     # periodicity at 1s periodicity integration


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for precision dynamics.

    F0 predicts how precision will adjust based on current precision
    state (E-layer) and long-range structural entropy. High structural
    entropy predicts precision will decrease.

    F1 predicts contextual uncertainty ~500ms ahead using tonal stability
    entropy and periodicity trends. High entropy = high predicted uncertainty.

    F2 predicts the degree of PE suppression at the next time step,
    based on current precision weights (P-layer) and rhythmic regularity.

    Vuust et al. 2022: music perception involves continuous updating of
    precision estimates at multiple hierarchical levels.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    e0, e1 = e
    p0, p1, p2 = p

    # -- H3 features --
    tonal_stab_ent_1s = h3_features[_TONAL_STAB_H16_ENT]
    onset_period_100ms = h3_features[_ONSET_H3_PERIOD]
    periodicity_1s = h3_features[_PERIODICITY_H16_PERIOD]

    # -- F0: Precision Adjustment --
    # Predicted change in precision: current precision (E0, E1) modulated
    # by structural entropy. High entropy signals that precision should
    # decrease at the next step (uncertainty increasing).
    # Friston 2005: precision updated via gradient descent on free energy.
    f0 = torch.sigmoid(
        0.35 * e0
        + 0.30 * e1
        + 0.35 * (1.0 - tonal_stab_ent_1s)
    )

    # -- F1: Context Uncertainty --
    # Predicted contextual uncertainty ~500ms ahead. High tonal entropy
    # + low periodicity = high predicted uncertainty. Inverse of F0.
    # Vuust 2022: uncertainty expectations adjust with musical context.
    f1 = torch.sigmoid(
        0.40 * tonal_stab_ent_1s
        + 0.35 * (1.0 - periodicity_1s)
        + 0.25 * (1.0 - onset_period_100ms)
    )

    # -- F2: Response Attenuation --
    # Predicted degree of PE suppression at the next time step.
    # Based on current precision weights: high P0/P1 predict continued
    # attenuation; high P2 (currently passing errors) predicts less
    # attenuation. Sedley 2016: precision modulates PE propagation.
    f2 = torch.sigmoid(
        0.35 * p0
        + 0.35 * p1
        + 0.30 * (1.0 - p2)
    )

    return f0, f1, f2
