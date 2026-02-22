"""SPH F-Layer — Forecast (3D).

Forward predictions for sequence recognition:
  F0: next_tone_pred_350ms     (Heschl→Hippocampus retrieval ~350ms)
  F1: sequence_completion_2s   (cingulate hierarchy boundary ~2.5s)
  F2: decision_evaluation      (cingulate top position at final tone)

H3 demands consumed:
  sensory_pleasantness: (4,16,1,0) reused
  spectral_auto:        (17,16,1,0) reused
  chroma_C:             (25,16,1,0)
  pitch_height:         (37,8,8,0)
  tonal_stability:      (60,16,1,0) reused

See Docs/C3/Models/PCU-a2-SPH/SPH.md §6.1 Layer F.
Bonetti 2024: final tone reshapes hierarchy — cingulate assumes top position.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_CONSONANCE_H16_MEAN = (4, 16, 1, 0)
_SPECTRAL_AUTO_H16_MEAN = (17, 16, 1, 0)
_CHROMA_H16_MEAN = (25, 16, 1, 0)
_PITCH_HEIGHT_H8_VEL = (37, 8, 8, 0)
_TONAL_STAB_H16_MEAN = (60, 16, 1, 0)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for sequence recognition.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    e0, _e1, e2, _e3 = e

    consonance_mean_1s = h3_features[_CONSONANCE_H16_MEAN]
    spectral_auto_mean_1s = h3_features[_SPECTRAL_AUTO_H16_MEAN]
    chroma_mean_1s = h3_features[_CHROMA_H16_MEAN]
    pitch_height_vel_500ms = h3_features[_PITCH_HEIGHT_H8_VEL]
    tonal_stab_mean_1s = h3_features[_TONAL_STAB_H16_MEAN]

    # -- F0: Next Tone Prediction (~350ms) --
    # Heschl→Hippocampus memory retrieval. Gamma match pattern +
    # long-range consonance context + pitch height velocity
    # (extrapolated pitch trajectory for next tone).
    f0 = torch.sigmoid(
        0.40 * e0 + 0.30 * consonance_mean_1s + 0.30 * pitch_height_vel_500ms
    )

    # -- F1: Sequence Completion (~2.5s) --
    # Cingulate hierarchy boundary prediction. Long-range tonal stability
    # + spectral coupling + chroma context — together indicate whether
    # the current sequence is approaching completion.
    f1 = torch.sigmoid(
        0.40 * tonal_stab_mean_1s
        + 0.30 * spectral_auto_mean_1s
        + 0.30 * chroma_mean_1s
    )

    # -- F2: Decision Evaluation --
    # Cingulate assumes top position at final tone. Hierarchy position
    # + long-range tonal stability provides evaluation context.
    # Bonetti 2024: cingulate > hippocampus at sequence end.
    f2 = torch.sigmoid(0.50 * e2 + 0.50 * tonal_stab_mean_1s)

    return f0, f1, f2
