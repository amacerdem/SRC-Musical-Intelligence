"""SRP P-Layer -- Cognitive Present (3D).

Three present-processing dimensions for striatal reward state:

  P0: wanting     -- Anticipatory reward (caudate DA ramp) [0, 1]
  P1: liking      -- Consummatory reward (NAcc DA burst) [0, 1]
  P2: pleasure    -- Hedonic impact (opioid + DA integration) [0, 1]

H3 consumed (tuple 25):
    (4, 18, 18, 0)  sensory_pleasantness trend H18 L0  -- resolution signal

R3 consumed:
    [0]      roughness               -- consonance proxy (inverse)
    [4]      sensory_pleasantness    -- direct hedonic signal
    [7]      amplitude               -- energy for wanting magnitude
    [25:33]  x_l0l5                  -- STG-NAcc coupling

P-layer outputs are the primary relay exports:
    wanting   -> F3 Attention salience, F6 Reward wanting
    liking    -> F6 Reward hedonic contribution
    pleasure  -> F6 Reward 1.5*surprise + 0.8*resolution

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuple 25 from demand spec) ------------------------------------
_PLEAS_TREND_2S = (4, 18, 18, 0)    # #25: consonance trend -> resolution

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_AMPLITUDE = 7
_X_L0L5_START = 25
_X_L0L5_END = 33


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing from H3/R3 + N+C/T+M outputs.

    P-layer outputs are the primary relay exports:
        wanting   -> salience mixer (F3 Attention), reward (F6)
        liking    -> reward hedonic contribution
        pleasure  -> reward signal (1.5*surprise + 0.8*resolution)

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(N0, N1, N2, C0, C1, C2)`` each ``(B, T)``.
        m_outputs: ``(T0, T1, T2, T3, M0, M1, M2)`` each ``(B, T)``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    n0, n1, n2, c0, c1, c2 = e_outputs
    t0, t1, t2, t3, m0, m1, m2 = m_outputs

    pleas_trend_2s = h3_features[_PLEAS_TREND_2S]

    # R3 features
    roughness = r3_features[..., _ROUGHNESS]                # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    amplitude = r3_features[..., _AMPLITUDE]                # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)

    # Derived
    consonance = 1.0 - roughness
    coupling = x_l0l5.mean(dim=-1)  # (B, T)

    # P0: Wanting -- anticipatory reward (caudate DA ramp)
    # Salimpoor 2011: caudate DA ramps 9-15s before peak (r=0.71)
    # wanting = f(caudate_da, tension, dynamic_intensity, anticipation)
    p0 = torch.sigmoid(
        0.30 * n0 + 0.25 * t0 + 0.25 * m1
        + 0.20 * amplitude * c0
    )

    # P1: Liking -- consummatory reward (NAcc DA burst)
    # Salimpoor 2011: NAcc DA bursts at peak moments (r=0.84)
    # liking = f(nacc_da, peak_detection, prediction_match, coupling)
    p1 = torch.sigmoid(
        0.30 * n1 + 0.25 * m2 + 0.25 * t1
        + 0.20 * coupling * consonance
    )

    # P2: Pleasure -- hedonic impact (opioid + DA integration)
    # Mallik 2017: mu-opioid mediates hedonic pleasure
    # Blood & Zatorre 2001: consonance resolution activates reward
    # pleasure = f(opioid, liking, appraisal, resolution_trend)
    p2 = torch.sigmoid(
        0.30 * n2 + 0.25 * t3 * pleasantness
        + 0.25 * pleas_trend_2s * consonance
        + 0.20 * c1 * n1
    )

    return p0, p1, p2
