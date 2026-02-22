"""MSPBA F-Layer -- Forecast (3D).

Forward predictions for harmonic resolution, mERAN trajectory, and
syntactic repair:

  F0: resolution_fc       -- Harmonic resolution prediction (0.5-2s) [0, 1]
  F1: eran_trajectory_fc  -- mERAN trajectory prediction (200-700ms) [0, 1]
  F2: syntax_repair_fc    -- Syntactic repair prediction (1-3s) [0, 1]

F0 predicts whether harmonic resolution (return to tonic) will occur
in the near future. Uses structural expectation trajectory at phrase
level (H18, 2s). Wohrle et al. 2024: N1m at resolution chord reflects
preceding dominant chord dissonance (MEG, N=30, eta-p2=0.101).

F1 predicts the magnitude of the next mERAN response based on current
context depth and dissonance trends (H14, 700ms). As more chords
accumulate, the predicted mERAN for future violations grows larger.
Maess et al. 2001: 2:1 position ratio.

F2 predicts whether Broca's area will integrate the violation (repair)
or reset the syntactic structure. Uses roughness and entropy trends.
Koelsch review: ERAN reflects long-term memory based syntactic processing.

H3 consumed:
    (0, 18, 18, 0)  roughness trend H18 L0               -- dissonance trajectory
    (22, 18, 18, 0) entropy trend H18 L0                  -- complexity trajectory
    (4, 18, 19, 0)  sensory_pleasantness stability H18 L0 -- consonance stability
    (1, 14, 8, 0)   sethares_dissonance velocity H14 L0   -- dissonance change rate

Cross-function downstream:
    F0 -> F6 Reward (resolution -> pleasure), F5 Emotion (satisfaction)
    F1 -> F3 Attention (anticipated violation), precision engine (pi_pred)
    F2 -> F2 Prediction (parse repair vs reset)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/mspba/MSPBA-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_TREND_H18 = (0, 18, 18, 0)      # roughness trend H18 L0
_ENTROPY_TREND_H18 = (22, 18, 18, 0)       # entropy trend H18 L0
_PLEASANT_STAB_H18 = (4, 18, 19, 0)        # sensory_pleasantness stability H18 L0
_SETHARES_VEL_H14 = (1, 14, 8, 0)          # sethares_dissonance velocity H14 L0


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    s_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from S/M/P outputs + long-horizon H3 trends.

    F0 (resolution_fc) predicts harmonic resolution from structural
    expectation trajectory (consonance stability H18) and current
    violation state (P1). After a violation, the resolution signal
    indicates when syntactic tension will be resolved.
    Wohrle et al. 2024: N1m at resolution chord (MEG, N=30).

    F1 (eran_trajectory_fc) predicts next mERAN magnitude from context
    depth (P0) and dissonance velocity (sethares H14). As more chords
    accumulate, larger mERAN is predicted for any future violation.
    Maess et al. 2001: 2:1 position ratio.

    F2 (syntax_repair_fc) predicts parse repair vs reset from roughness
    trend and entropy trend at phrase level. Persistent violations
    trigger parse reset rather than local repair.
    Koelsch: ERAN reflects LTM-based syntactic processing.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        s_outputs: ``(S0, S1, S2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1, M2)`` each ``(B, T)``.
        p_outputs: ``(P0, P1)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    _s0, _s1, s2 = s_outputs
    m0, _m1, _m2 = m_outputs
    p0, p1 = p_outputs

    # -- H3 features (phrase-level, H18 = 2s; progression-level, H14 = 700ms) ---
    roughness_trend = h3_features[_ROUGHNESS_TREND_H18]      # (B, T)
    entropy_trend = h3_features[_ENTROPY_TREND_H18]          # (B, T)
    pleasant_stab = h3_features[_PLEASANT_STAB_H18]          # (B, T)
    sethares_vel = h3_features[_SETHARES_VEL_H14]            # (B, T)

    # -- F0: Resolution Forecast (0.5-2s ahead) ---------------------------------
    # Predicts return to tonic after violation. High consonance stability
    # + declining violation state = resolution approaching.
    # Wohrle et al. 2024: N1m at resolution reflects preceding dissonance
    f0 = torch.sigmoid(
        0.40 * pleasant_stab
        + 0.30 * (1.0 - p1)
        + 0.30 * (1.0 - roughness_trend)
    )

    # -- F1: ERAN Trajectory Forecast (200-700ms ahead) --------------------------
    # Predicts upcoming violation strength from context depth (P0) and
    # dissonance velocity. Deeper context = larger predicted mERAN.
    # Maess et al. 2001: 2:1 position ratio -- context accumulation
    f1 = torch.sigmoid(
        0.40 * p0
        + 0.30 * m0
        + 0.30 * sethares_vel
    )

    # -- F2: Syntax Repair Forecast (1-3s ahead) --------------------------------
    # Predicts whether Broca's area can integrate the violation (repair)
    # or must reset. Low roughness/entropy trends + active processing (S2)
    # = successful repair; persistent trends = parse reset.
    # Koelsch: ERAN reflects long-term memory based syntactic processing
    f2 = torch.sigmoid(
        0.35 * s2
        + 0.35 * (1.0 - entropy_trend)
        + 0.30 * (1.0 - roughness_trend)
    )

    return f0, f1, f2
