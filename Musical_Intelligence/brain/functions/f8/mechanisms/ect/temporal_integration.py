"""ECT M-Layer -- Temporal Integration (3D).

Three temporal dynamics of the compartmentalization process:

  training_history  -- Specialization accumulation over time [0, 1]
  network_state     -- Recent network architecture state [0, 1]
  task_memory       -- Demand-driven network shaping [0, 1]

training_history uses the pattern binding trend over 1s as a proxy for how
specialization has developed. Increasing trend indicates deepening
compartmentalization; stable or decreasing trend indicates plateau or
broadening.
Leipold et al. 2021 (N = 153): robust effects of musicianship on
interhemispheric and intrahemispheric connectivity independent of absolute
pitch, confirming graded expertise effects.

network_state computes the efficiency delta as the difference between
within-network efficiency (f01) and between-network reduction (f02).
Paraskevopoulos et al. 2022: musicians show a distinct network topology
with more within-network and fewer between-network connections.

task_memory tracks the processing demand entropy through EMA of amplitude
entropy at 500ms. High demand entropy suggests varied task demands that
may counteract compartmentalization.
Olszewska et al. 2021: training-induced brain reorganization involves
dynamic reconfiguration of neural connections.

H3 demands consumed (2):
  (33, 16, 18, 0) x_l4l5 trend H16 L0     -- pattern binding trend 1s
  (7, 8, 20, 2)   amplitude entropy H8 L2  -- demand entropy 500ms

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/ect/m_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed (2 tuples, M-layer) -------------------------------
_BINDING_TREND_1S = (33, 16, 18, 0)       # pattern binding trend 1s (L0 fwd)
_DEMAND_ENT_500MS = (7, 8, 20, 2)         # demand entropy 500ms (L2 bidi)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    ednr: Tensor,
    cdmr: Tensor,
    slee: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute M-layer: 3D temporal integration features.

    training_history: Uses the binding trend over 1s (H3 tuple:
    x_l4l5[0], H16, M18, L0) as a proxy for specialization accumulation.
    The forward-only law (L0) ensures causal tracking.
    sigma(0.50 * binding_trend_1s + 0.25 * ednr_compartm + 0.25 * slee_expertise).
    Leipold et al. 2021: graded expertise effects (N = 153).

    network_state: Combines within-efficiency (f01) with inverted
    between-reduction (1 - f02) through equal weighting.
    sigma(0.50 * f01 + 0.50 * (1 - f02)).
    Paraskevopoulos 2022: distinct network topology.

    task_memory: Tracks the demand entropy at 500ms (H3 tuple:
    amplitude, H8, M20, L2) as a measure of task demand variability.
    sigma(0.50 * demand_entropy_500ms + 0.25 * cdmr_mean + 0.25 * slee_mean).
    Olszewska et al. 2021: dynamic reconfiguration.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.
        ednr: ``(B, T, 10)`` upstream EDNR output.
        cdmr: ``(B, T, 11)`` upstream CDMR output.
        slee: ``(B, T, 13)`` upstream SLEE output.

    Returns:
        ``(training_history, network_state, task_memory)`` each ``(B, T)``.
    """
    f01, f02, _f03, _f04 = e_outputs

    # -- H3 features -----------------------------------------------------------
    binding_trend_1s = h3_features[_BINDING_TREND_1S]    # (B, T)
    demand_ent_500ms = h3_features[_DEMAND_ENT_500MS]    # (B, T)

    # -- Upstream context signals ----------------------------------------------
    # EDNR compartmentalization is dim 2 (f03 in EDNR E-layer)
    ednr_compartm = ednr[..., 2]               # (B, T)
    # SLEE expertise_advantage is dim 3 (f04 in SLEE E-layer)
    slee_expertise = slee[..., 3]              # (B, T)
    cdmr_mean = cdmr.mean(dim=-1)              # (B, T)
    slee_mean = slee.mean(dim=-1)              # (B, T)

    # -- training_history: Specialization accumulation -------------------------
    # sigma(0.50 * binding_trend_1s + 0.25 * ednr_compartm + 0.25 * slee_expertise)
    # Leipold et al. 2021: robust musicianship effects on interhemispheric
    # and intrahemispheric connectivity (N = 153).
    training_history = torch.sigmoid(
        0.50 * binding_trend_1s
        + 0.25 * ednr_compartm
        + 0.25 * slee_expertise
    )

    # -- network_state: Recent network architecture ----------------------------
    # sigma(0.50 * f01 + 0.50 * (1 - f02))
    # Paraskevopoulos 2022: musicians show a distinct network topology with
    # more within-network and fewer between-network connections.
    network_state = torch.sigmoid(
        0.50 * f01
        + 0.50 * (1.0 - f02)
    )

    # -- task_memory: Demand-driven network shaping ----------------------------
    # sigma(0.50 * demand_entropy_500ms + 0.25 * cdmr_mean + 0.25 * slee_mean)
    # Olszewska et al. 2021: training-induced brain reorganization involves
    # dynamic reconfiguration of neural connections.
    task_memory = torch.sigmoid(
        0.50 * demand_ent_500ms
        + 0.25 * cdmr_mean
        + 0.25 * slee_mean
    )

    return training_history, network_state, task_memory
