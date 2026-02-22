"""ECT F-Layer -- Forecast (3D).

Three forward predictions about the compartmentalization trade-off trajectory:

  transfer_limit       -- Cross-domain performance prediction [0, 1]
  efficiency_opt       -- Within-network speed prediction [0, 1]
  flexibility_recovery -- Network reconfiguration capacity prediction [0, 1]

transfer_limit predicts the degree to which compartmentalization will limit
cross-domain transfer by combining between-reduction (f02) with inverted
flexibility (1 - f04).
Moller et al. 2021: musicians show behavioral cost in BCG
(t(42.3) = 3.06, p = 0.004) -- reduced cross-modal structural connectivity
limits visual cue benefit.

efficiency_opt predicts future processing efficiency within specialized
modules based on current within-binding state and training history.
Papadaki et al. 2023: network strength and global efficiency correlate
with task performance in aspiring professionals.

flexibility_recovery predicts whether the system can recover flexibility
through varied demands, based on flexibility index (f04), task memory demand
entropy, and current network isolation.
Wu-Chung et al. 2025: baseline network flexibility determines whether music
training produces cognitive benefit -- suggesting flexibility can be a
recoverable resource.
Blasi et al. 2025: music/dance rehabilitation produces neuroplasticity in
perception, memory, and motor areas.

H3 demands consumed (2):
  (7, 3, 0, 2)    amplitude value H3 L2      -- task demand 100ms
  (13, 3, 0, 2)   brightness value H3 L2     -- tonal adaptation 100ms

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/ect/f_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed (2 tuples, F-layer) -------------------------------
_TASK_DEMAND_100MS = (7, 3, 0, 2)          # task demand at 100ms
_TONAL_ADAPT_100MS = (13, 3, 0, 2)         # tonal adaptation at 100ms


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
    ednr: Tensor,
    cdmr: Tensor,
    slee: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: 3D forward predictions for compartmentalization.

    transfer_limit: Predicts cross-domain transfer limitations.
    sigma(0.50 * f02 + 0.50 * (1 - f04)).
    High between-reduction + low flexibility -> strong transfer limitation.
    Moller 2021: BCG behavioral cost (t(42.3) = 3.06, p = 0.004).

    efficiency_opt: Predicts within-network processing speed trajectory.
    sigma(0.30 * within_binding + 0.30 * training_history
          + 0.20 * task_demand_100ms + 0.20 * ednr_efficiency).
    Papadaki 2023: network strength correlates with performance.

    flexibility_recovery: Predicts whether flexibility can be recovered.
    sigma(0.25 * f04 + 0.25 * task_memory + 0.20 * (1 - network_isolation)
          + 0.15 * tonal_adapt_100ms + 0.15 * slee_mean).
    Wu-Chung 2025: baseline flexibility determines training benefit.
    Blasi 2025: rehabilitation-induced neuroplasticity.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.
        m_outputs: ``(training_history, network_state, task_memory)``
            each ``(B, T)``.
        p_outputs: ``(within_binding, network_isolation)`` each ``(B, T)``.
        ednr: ``(B, T, 10)`` upstream EDNR output.
        cdmr: ``(B, T, 11)`` upstream CDMR output.
        slee: ``(B, T, 13)`` upstream SLEE output.

    Returns:
        ``(transfer_limit, efficiency_opt, flexibility_recovery)``
        each ``(B, T)``.
    """
    _f01, f02, _f03, f04 = e_outputs
    training_history, _network_state, task_memory = m_outputs
    within_binding, network_isolation = p_outputs

    # -- H3 features -----------------------------------------------------------
    task_demand_100ms = h3_features[_TASK_DEMAND_100MS]    # (B, T)
    tonal_adapt_100ms = h3_features[_TONAL_ADAPT_100MS]    # (B, T)

    # -- Upstream context signals ----------------------------------------------
    # EDNR processing_efficiency is F-layer dim 9 (last dim in EDNR 10D output)
    ednr_efficiency = ednr[..., 9]             # (B, T)
    slee_mean = slee.mean(dim=-1)              # (B, T)

    # -- transfer_limit: Cross-domain performance prediction -------------------
    # sigma(0.50 * f02 + 0.50 * (1 - f04))
    # Moller 2021: musicians show behavioral cost in BCG (t(42.3) = 3.06,
    # p = 0.004). Reduced cross-modal structural connectivity limits visual
    # cue benefit.
    transfer_limit = torch.sigmoid(
        0.50 * f02
        + 0.50 * (1.0 - f04)
    )

    # -- efficiency_opt: Within-network speed prediction -----------------------
    # sigma(0.30 * within_binding + 0.30 * training_history
    #       + 0.20 * task_demand_100ms + 0.20 * ednr_efficiency)
    # Papadaki 2023: network strength and global efficiency correlate with
    # task performance in aspiring professionals.
    efficiency_opt = torch.sigmoid(
        0.30 * within_binding
        + 0.30 * training_history
        + 0.20 * task_demand_100ms
        + 0.20 * ednr_efficiency
    )

    # -- flexibility_recovery: Reconfiguration capacity prediction -------------
    # sigma(0.25 * f04 + 0.25 * task_memory + 0.20 * (1 - network_isolation)
    #       + 0.15 * tonal_adapt_100ms + 0.15 * slee_mean)
    # Wu-Chung 2025: baseline network flexibility determines whether music
    # training produces cognitive benefit.
    # Blasi 2025: music/dance rehabilitation produces neuroplasticity.
    flexibility_recovery = torch.sigmoid(
        0.25 * f04
        + 0.25 * task_memory
        + 0.20 * (1.0 - network_isolation)
        + 0.15 * tonal_adapt_100ms
        + 0.15 * slee_mean
    )

    return transfer_limit, efficiency_opt, flexibility_recovery
