"""SRP T+M-Layer -- Temporal Integration (7D).

Seven composite signals integrating N+C-layer with temporal context:

  T0: tension              -- Musical tension accumulation [0, 1]
  T1: prediction_match     -- Prediction-outcome match [0, 1]
  T2: reaction             -- ITPRA reaction response [0, 1]
  T3: appraisal            -- ITPRA appraisal evaluation [0, 1]
  M0: harmonic_tension     -- Harmonic tension dynamics [0, 1]
  M1: dynamic_intensity    -- Energy-based intensity [0, 1]
  M2: peak_detection       -- Peak moment identification [0, 1]

H3 consumed (tuples 14-24):
    (0, 18, 18, 0)   roughness trend H18 L0              -- harmonic tension
    (22, 18, 0, 2)   distribution_entropy value H18 L2   -- uncertainty
    (7, 20, 8, 0)    amplitude velocity H20 L0           -- tension buildup
    (7, 18, 8, 0)    amplitude velocity H18 L0           -- dynamic intensity
    (7, 18, 11, 0)   amplitude acceleration H18 L0       -- buildup
    (4, 18, 8, 0)    sensory_pleasantness vel H18 L0     -- prediction match
    (16, 18, 19, 2)  spectral_smoothness stab H18 L2     -- appraisal
    (11, 16, 14, 2)  onset_strength period H16 L2        -- regularity
    (11, 16, 8, 0)   onset_strength velocity H16 L0      -- reaction
    (10, 16, 11, 0)  onset_strength accel H16 L0         -- reaction jerk
    (11, 18, 4, 2)   onset_strength max H18 L2           -- peak

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 14-24 from demand spec) --------------------------------
_ROUGH_TREND_2S = (0, 18, 18, 0)        # #14: harmonic tension buildup
_ENTROPY_VAL_2S = (22, 18, 0, 2)        # #15: uncertainty context
_AMP_VEL_5S = (7, 20, 8, 0)             # #16: tension accumulation
_AMP_VEL_2S = (7, 18, 8, 0)             # #17: dynamic intensity
_AMP_ACCEL_2S = (7, 18, 11, 0)          # #18: energy acceleration
_PLEAS_VEL_2S = (4, 18, 8, 0)           # #19: prediction match
_SMOOTH_STAB_2S = (16, 18, 19, 2)       # #20: spectral stability
_ONSET_PERIOD_1S = (11, 16, 14, 2)      # #21: onset regularity
_ONSET_VEL_1S = (11, 16, 8, 0)          # #22: onset velocity
_FLUX_ACCEL_1S = (10, 16, 11, 0)        # #23: spectral flux jerk
_ONSET_MAX_2S = (11, 18, 4, 2)          # #24: peak onset phrase


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor]:
    """T+M-layer: 7D temporal integration from N+C-layer + H3.

    Mathematical formulation:
        tension = f(harmonic_trend, entropy, energy_buildup)
        prediction_match = f(consonance_velocity, da_nacc, appraisal)
        reaction = f(onset_velocity, flux_jerk, surprise)
        appraisal = f(spectral_stability, prediction_match, opioid)
        harmonic_tension = f(roughness_trend, dissonance_dynamics)
        dynamic_intensity = f(energy_velocity, acceleration)
        peak_detection = f(onset_max, energy_peak, consummatory_burst)

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(N0, N1, N2, C0, C1, C2)`` each ``(B, T)``.

    Returns:
        ``(T0, T1, T2, T3, M0, M1, M2)`` each ``(B, T)``.
    """
    n0, n1, n2, c0, c1, c2 = e_outputs

    rough_trend_2s = h3_features[_ROUGH_TREND_2S]
    entropy_val_2s = h3_features[_ENTROPY_VAL_2S]
    amp_vel_5s = h3_features[_AMP_VEL_5S]
    amp_vel_2s = h3_features[_AMP_VEL_2S]
    amp_accel_2s = h3_features[_AMP_ACCEL_2S]
    pleas_vel_2s = h3_features[_PLEAS_VEL_2S]
    smooth_stab_2s = h3_features[_SMOOTH_STAB_2S]
    onset_period_1s = h3_features[_ONSET_PERIOD_1S]
    onset_vel_1s = h3_features[_ONSET_VEL_1S]
    flux_accel_1s = h3_features[_FLUX_ACCEL_1S]
    onset_max_2s = h3_features[_ONSET_MAX_2S]

    # T0: Tension -- accumulation from harmonic + dynamic + uncertainty
    # Huron 2006 ITPRA: tension phase builds anticipatory reward
    # tension = sigma(0.35*roughness_trend + 0.35*energy_buildup + 0.30*uncertainty)
    t0 = torch.sigmoid(
        0.35 * rough_trend_2s * n0
        + 0.35 * amp_vel_5s * c0
        + 0.30 * entropy_val_2s
    )

    # T1: Prediction match -- consonance velocity confirms/violates expectation
    # Zatorre & Salimpoor 2013: DA release scales with prediction accuracy
    # match = sigma(consonance_velocity * nacc_burst * coupling)
    t1 = torch.sigmoid(
        0.35 * pleas_vel_2s * n1
        + 0.35 * (1.0 - c2) * c1
        + 0.30 * onset_period_1s
    )

    # T2: Reaction -- ITPRA fast-response to salient events
    # Huron 2006: reaction is autonomic + startle + orienting
    # reaction = sigma(onset_velocity * flux_jerk * surprise)
    t2 = torch.sigmoid(
        0.35 * onset_vel_1s * c2
        + 0.35 * flux_accel_1s
        + 0.30 * amp_accel_2s
    )

    # T3: Appraisal -- ITPRA cognitive evaluation of reward context
    # Huron 2006: appraisal evaluates whether outcome was positive
    # appraisal = sigma(spectral_stability * opioid * prediction_match)
    t3 = torch.sigmoid(
        0.35 * smooth_stab_2s * n2
        + 0.35 * pleas_vel_2s * n1
        + 0.30 * onset_period_1s * c1
    )

    # M0: Harmonic tension -- roughness trajectory dynamics
    # Blood & Zatorre 2001: dissonance-to-consonance resolution activates NAcc
    m0 = torch.sigmoid(
        0.40 * rough_trend_2s
        + 0.30 * entropy_val_2s * c2
        + 0.30 * amp_vel_5s * n0
    )

    # M1: Dynamic intensity -- energy velocity and acceleration
    # Salimpoor 2011: caudate DA ramp tracks energy dynamics
    m1 = torch.sigmoid(
        0.40 * amp_vel_2s * c0
        + 0.30 * amp_accel_2s
        + 0.30 * amp_vel_5s
    )

    # M2: Peak detection -- onset max + energy peak + consummatory burst
    # Salimpoor 2011: NAcc DA bursts at peak (r=0.84)
    m2 = torch.sigmoid(
        0.40 * onset_max_2s * n1
        + 0.30 * amp_vel_2s * amp_accel_2s
        + 0.30 * onset_vel_1s * c1
    )

    return t0, t1, t2, t3, m0, m1, m2
