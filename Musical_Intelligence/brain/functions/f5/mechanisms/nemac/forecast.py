"""NEMAC F-Layer -- Forecast (2D).

Forward predictions for the nostalgia-evoked memory-affect circuit:
  F0: wellbeing_pred      — Wellbeing trajectory prediction [0, 1]
  F1: vividness_pred      — Memory vividness prediction [0, 1]

F0 forecasts the wellbeing trajectory based on current nostalgia state.
When nostalgia intensity (W0) and wellbeing enhancement (W1) are high
and the binding trajectory is stable, the model predicts continued
wellbeing improvement. Barrett 2010: nostalgia increases self-continuity
and meaning in life (6 studies, N=670+). Uses the 5s binding trajectory
to assess whether the nostalgic context is being sustained.

F1 forecasts memory vividness trajectory. When hippocampal activation (M1)
and current vividness (M2) are high, the model predicts continued vivid
memory retrieval. Tonal stability (tonalness mean at 5s) indicates the
musical context will continue supporting memory retrieval.

H3 demands consumed (2 tuples -- shared with other layers + 1 F-specific):
  (14, 20, 1, 0)  tonalness mean H20 L0           -- tonal stability 5s
  (3, 20, 1, 2)   stumpf_fusion mean H20 L2       -- binding trajectory

R3 features: None (F-layer uses only upstream layer outputs + H3)

Upstream layers:
  E-layer: (E0:chills, E1:nostalgia)
  M+W-layer: (M0:mpfc_activation, M1:hippocampus_activ, M2:memory_vividness,
              W0:nostalgia_intens, W1:wellbeing_enhance)
  P-layer: (P0:nostalgia_correl, P1:memory_reward_lnk)

Barrett et al. 2010: nostalgia increases wellbeing (6 studies, N=670+).
Janata 2009: mPFC tracks tonal movement for autobiographical salience.
Sakakibara 2025: self-selected music sustains nostalgia (d=0.88).

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/nemac/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_TONAL_MEAN_H20 = (14, 20, 1, 0)      # tonalness mean H20 L0
_STUMPF_MEAN_H20 = (3, 20, 1, 2)      # stumpf_fusion mean H20 L2


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: wellbeing and vividness trajectory predictions.

    F0 (wellbeing_pred) forecasts wellbeing trajectory. Nostalgia intensity
    (W0) + wellbeing enhancement (W1) + binding trajectory (stumpf 5s)
    predict sustained wellbeing. Barrett 2010: nostalgia increases social
    connectedness and meaning in life (6 studies, N=670+).

    F1 (vividness_pred) forecasts memory vividness trajectory. Hippocampal
    activation (M1) + current vividness (M2) + tonal stability (tonalness
    5s) predict continued vivid retrieval. Stable tonal context sustains
    the retrieval cue.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(M0, M1, M2, W0, W1)`` from temporal integration layer.
        p: ``(P0, P1)`` from cognitive present layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)``
    """
    _e0, e1 = e
    m0, m1, m2, w0, w1 = m
    p0, p1 = p

    # -- H3 features --
    tonal_mean = h3_features[_TONAL_MEAN_H20]      # (B, T)
    binding_5s = h3_features[_STUMPF_MEAN_H20]     # (B, T)

    # -- F0: Wellbeing Prediction --
    # Forecasts sustained wellbeing from nostalgia. When nostalgia intensity
    # (W0) and wellbeing enhancement (W1) are high with stable binding,
    # the wellbeing trajectory is predicted to continue.
    # Barrett 2010: nostalgia -> self-continuity + meaning (N=670+).
    f0 = torch.sigmoid(
        0.35 * w0 * w1.clamp(min=0.1)
        + 0.30 * p0 * binding_5s
        + 0.20 * m0 * e1
        + 0.15 * p1
    )

    # -- F1: Vividness Prediction --
    # Forecasts memory vividness trajectory. Hippocampal retrieval (M1)
    # + current vividness (M2) + tonal stability predict continued
    # vivid autobiographical retrieval.
    # Janata 2009: mPFC tracks tonal space (t=5.784).
    f1 = torch.sigmoid(
        0.35 * m1 * m2.clamp(min=0.1)
        + 0.30 * tonal_mean * p0
        + 0.20 * binding_5s * e1
        + 0.15 * w0
    )

    return f0, f1
