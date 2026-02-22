"""ICEM F-Layer — Forecast (2D).

Forward predictions for emotional response:
  F0: arousal_change_1_3s    (SCR response prediction ~1.3s ahead)
  F1: valence_shift_2_5s     (subjective feeling prediction ~2.5s ahead)

H3 demands consumed:
  onset_strength:     (11,8,1,0)
  pitch_salience:     (39,16,1,2)
  tonal_stability:    (60,16,1,0) reused
  key_clarity:        (51,8,1,0)

See Docs/C3/Models/PCU-a3-ICEM/ICEM.md §6.1 Layer F.
Salimpoor 2011: dopamine release during anticipation (caudate) and
consummation (NAc) of peak emotion to music.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ONSET_H8_MEAN = (11, 8, 1, 0)
_PITCH_SAL_H16_MEAN = (39, 16, 1, 2)
_TONAL_STAB_H16_MEAN = (60, 16, 1, 0)
_KEY_CLARITY_H8_MEAN = (51, 8, 1, 0)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: forward emotional response predictions.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)``
    """
    _e0, e1, e2, _e3 = e

    onset_mean_500ms = h3_features[_ONSET_H8_MEAN]
    pitch_sal_mean_1s = h3_features[_PITCH_SAL_H16_MEAN]
    tonal_stab_mean_1s = h3_features[_TONAL_STAB_H16_MEAN]
    key_clarity_mean_500ms = h3_features[_KEY_CLARITY_H8_MEAN]

    # -- F0: Arousal Change (~1.3s) --
    # Predicted SCR/arousal response. Current arousal state +
    # onset context (sustained events) + pitch salience context.
    # Salimpoor 2011: anticipatory dopamine release in caudate.
    f0 = torch.sigmoid(
        0.50 * e1 + 0.30 * onset_mean_500ms + 0.20 * pitch_sal_mean_1s
    )

    # -- F1: Valence Shift (~2.5s) --
    # Predicted subjective feeling change. Current valence state +
    # tonal stability (harmonic context) + key clarity (tonal grounding).
    # Gold 2019: pleasure depends on joint uncertainty and surprise.
    f1 = torch.sigmoid(
        0.40 * e2 + 0.30 * tonal_stab_mean_1s + 0.30 * key_clarity_mean_500ms
    )

    return f0, f1
