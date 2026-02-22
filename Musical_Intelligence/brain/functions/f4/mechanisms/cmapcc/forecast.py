"""CMAPCC F-Layer -- Forecast (3D).

Three forward predictions for cross-modal transfer, motor and perceptual
sequence anticipation:

  F0: transfer_pred       -- Cross-modal transfer prediction (2-5s ahead) [0, 1]
  F1: motor_seq_pred      -- Motor sequence prediction (0.5-1s ahead) [0, 1]
  F2: perceptual_seq_pred -- Perceptual sequence prediction (0.5-1s ahead) [0, 1]

H3 consumed:
    (3, 20, 1, 0)   stumpf_fusion mean H20 L0                 -- binding stability 5s
    (5, 20, 19, 0)  periodicity stability H20 L0              -- sequence stability 5s
    (4, 24, 1, 0)   sensory_pleasantness mean H24 L0          -- long-term valence
    (1, 24, 19, 0)  sethares_dissonance stability H24 L0      -- interval stability
    (7, 20, 18, 0)  amplitude trend H20 L0                    -- intensity trajectory 5s
    (7, 6, 8, 0)    amplitude velocity H6 L0                  -- action dynamics at beat
    (10, 6, 0, 2)   onset_strength value H6 L2                -- beat-level onset
    (11, 6, 0, 2)   spectral_flux value H6 L2                 -- spectral change at beat
    (11, 11, 1, 0)  spectral_flux mean H11 L0                 -- mean flux at 500ms
    (0, 20, 18, 0)  roughness trend H20 L0                    -- dissonance trajectory

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cmapcc/CMAPCC-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_5S = (3, 20, 1, 0)
_PERIOD_STAB_5S = (5, 20, 19, 0)
_PLEAS_MEAN_36S = (4, 24, 1, 0)
_SETH_STAB_36S = (1, 24, 19, 0)
_AMP_TREND_5S = (7, 20, 18, 0)
_AMP_VEL_H6 = (7, 6, 8, 0)
_ONSET_VAL_H6 = (10, 6, 0, 2)
_FLUX_VAL_H6 = (11, 6, 0, 2)
_FLUX_MEAN_500MS = (11, 11, 1, 0)
_ROUGH_TREND_5S = (0, 20, 18, 0)


def _predict_future(
    state: Tensor,
    trend: Tensor,
    weight_state: float = 0.60,
    weight_trend: float = 0.40,
) -> Tensor:
    """Simple forward prediction: state + weighted trend.

    Combines a current state estimate with a temporal trajectory
    (trend or velocity) to project a future activation level.

    Args:
        state: ``(B, T)`` current state estimate.
        trend: ``(B, T)`` temporal trajectory (trend, velocity, or stability).
        weight_state: weight for state component.
        weight_trend: weight for trend component.

    Returns:
        ``(B, T)`` predicted future activation (sigmoid-bounded).
    """
    return torch.sigmoid(weight_state * state + weight_trend * trend)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from E/M/P outputs + H3 context + upstreams.

    F0 projects whether cross-modal transfer will occur over 2-5s using
    common_code_strength and H20 consolidation window.

    F1 projects the motor system's next action 0.5-1s ahead using
    motor_entrainment from SNEM and beat-level H6 features.

    F2 projects the auditory system's expectation 0.5-1s ahead using
    encoding_state from MEAMN and bar-level H16 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.
        p_outputs: ``(P0, P1)`` each ``(B, T)``.
        upstream_outputs: ``{"MEAMN": (B, T, D), "SNEM": (B, T, D)}``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    _e0, _e1, _e2 = e_outputs
    m0, _m1 = m_outputs
    p0, p1 = p_outputs

    # -- H3 features --
    stumpf_mean_5s = h3_features[_STUMPF_MEAN_5S]
    period_stab_5s = h3_features[_PERIOD_STAB_5S]
    pleas_mean_36s = h3_features[_PLEAS_MEAN_36S]
    seth_stab_36s = h3_features[_SETH_STAB_36S]
    amp_trend_5s = h3_features[_AMP_TREND_5S]
    amp_vel_h6 = h3_features[_AMP_VEL_H6]
    onset_val_h6 = h3_features[_ONSET_VAL_H6]
    flux_val_h6 = h3_features[_FLUX_VAL_H6]
    flux_mean_500ms = h3_features[_FLUX_MEAN_500MS]
    rough_trend_5s = h3_features[_ROUGH_TREND_5S]

    # -- Upstream reads (graceful degradation) --
    # SNEM: E0:beat_entrainment [0] as motor_entrainment
    snem = upstream_outputs.get("SNEM")
    if snem is not None:
        motor_entrainment = snem[..., 0]  # E0:beat_entrainment -- (B, T)
    else:
        motor_entrainment = torch.zeros_like(m0)

    # MEAMN: P0:memory_state [5] as encoding_state
    meamn = upstream_outputs.get("MEAMN")
    if meamn is not None:
        encoding_state = meamn[..., 5]  # P0:memory_state -- (B, T)
    else:
        encoding_state = torch.zeros_like(m0)

    # -- Consolidation trajectory for transfer prediction --
    consolidation = (
        0.25 * stumpf_mean_5s + 0.25 * period_stab_5s
        + 0.25 * pleas_mean_36s + 0.25 * seth_stab_36s
    )

    # F0: Transfer prediction -- cross-modal transfer over 2-5s
    # Uses common_code_strength (M0) and consolidation trajectory.
    # Paraskevopoulos 2022: musicians show enhanced statistical learning
    # transfer (g=-1.09, MEG+PTE, N=25).
    f0 = _predict_future(m0, consolidation, 0.55, 0.45)

    # -- Motor trajectory for motor prediction --
    motor_traj = (
        0.35 * amp_vel_h6 + 0.35 * onset_val_h6
        + 0.30 * flux_val_h6
    )

    # F1: Motor sequence prediction -- right PMC action prediction (0.5-1s)
    # Uses motor_entrainment from SNEM and beat-level H6 features.
    # Ross & Balasubramaniam 2022: premotor cortex enables beat-level
    # action prediction.
    f1 = _predict_future(motor_entrainment, motor_traj, 0.50, 0.50)

    # -- Perceptual trajectory for perceptual prediction --
    perceptual_traj = (
        0.35 * flux_mean_500ms + 0.35 * rough_trend_5s
        + 0.30 * amp_trend_5s
    )

    # F2: Perceptual sequence prediction -- right PMC auditory (0.5-1s)
    # Uses encoding_state from MEAMN and H16 window features.
    # Di Liberto 2021: shared encoding between perceived and imagined
    # melodies (EEG, N=21).
    f2 = _predict_future(encoding_state, perceptual_traj, 0.50, 0.50)

    return f0, f1, f2
