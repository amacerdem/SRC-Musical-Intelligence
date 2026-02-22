"""SPH E-Layer — Extraction (4D).

Oscillatory and hierarchical feature extraction for sequence recognition:
  E0: gamma_match             (gamma power match — memorised sequence)
  E1: alpha_beta_error        (alpha-beta prediction error — varied sequence)
  E2: hierarchy_position      (network hierarchy state — cingulate position)
  E3: feedforward_feedback    (directional information flow balance)

H3 demands consumed:
  sensory_pleasantness: (4,3,0,2), (4,16,1,0)
  onset_strength:       (11,0,0,2), (11,3,14,2)
  spectral_auto:        (17,3,0,2), (17,16,1,0)
  spectral_flux:        (21,3,0,2), (21,3,2,2)
  chroma_C:             (25,3,0,2)
  tonal_stability:      (60,3,0,2), (60,16,1,0), (60,16,13,0)

See Docs/C3/Models/PCU-a2-SPH/SPH.md §7.2 formulas.
Bonetti 2024: gamma>alpha-beta for memorised, alpha-beta>gamma for varied.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_CONSONANCE_H3_VAL = (4, 3, 0, 2)
_CONSONANCE_H16_MEAN = (4, 16, 1, 0)
_ONSET_H0_VAL = (11, 0, 0, 2)
_ONSET_H3_PERIOD = (11, 3, 14, 2)
_SPECTRAL_AUTO_H3_VAL = (17, 3, 0, 2)
_SPECTRAL_AUTO_H16_MEAN = (17, 16, 1, 0)
_SPECTRAL_FLUX_H3_VAL = (21, 3, 0, 2)
_SPECTRAL_FLUX_H3_STD = (21, 3, 2, 2)
_CHROMA_H3_VAL = (25, 3, 0, 2)
_TONAL_STAB_H3_VAL = (60, 3, 0, 2)
_TONAL_STAB_H16_MEAN = (60, 16, 1, 0)
_TONAL_STAB_H16_ENTROPY = (60, 16, 13, 0)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: oscillatory and hierarchical features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``

    Returns:
        ``(E0, E1, E2, E3)`` each ``(B, T)``
    """
    consonance_100ms = h3_features[_CONSONANCE_H3_VAL]
    consonance_mean_1s = h3_features[_CONSONANCE_H16_MEAN]
    onset_25ms = h3_features[_ONSET_H0_VAL]
    onset_period_100ms = h3_features[_ONSET_H3_PERIOD]
    spectral_auto_100ms = h3_features[_SPECTRAL_AUTO_H3_VAL]
    spectral_auto_mean_1s = h3_features[_SPECTRAL_AUTO_H16_MEAN]
    spectral_flux_100ms = h3_features[_SPECTRAL_FLUX_H3_VAL]
    spectral_flux_std_100ms = h3_features[_SPECTRAL_FLUX_H3_STD]
    chroma_100ms = h3_features[_CHROMA_H3_VAL]
    tonal_stab_100ms = h3_features[_TONAL_STAB_H3_VAL]
    tonal_stab_mean_1s = h3_features[_TONAL_STAB_H16_MEAN]
    tonal_stab_entropy_1s = h3_features[_TONAL_STAB_H16_ENTROPY]

    # -- E0: Gamma Match --
    # Gamma power activation for memorised sequences. Memory confirmation
    # through consonance (harmonic match) + spectral coupling (feedforward)
    # + chroma content (tonal identity).
    # Bonetti 2024: gamma > alpha-beta for memorised sequences.
    e0 = torch.sigmoid(
        0.35 * consonance_100ms
        + 0.30 * spectral_auto_100ms
        + 0.20 * consonance_mean_1s
        + 0.15 * chroma_100ms
    )

    # -- E1: Alpha-Beta Error --
    # Prediction error activation for varied sequences. Spectral deviation
    # + onset detection + change variability + periodicity (rhythmic context).
    # Bonetti 2024: alpha-beta > gamma for varied sequences.
    e1 = torch.sigmoid(
        0.35 * spectral_flux_100ms
        + 0.25 * onset_25ms
        + 0.20 * spectral_flux_std_100ms
        + 0.20 * onset_period_100ms
    )

    # -- E2: Hierarchy Position --
    # Network hierarchy state. High values indicate cingulate at top of
    # hierarchy (final tone of sequence). Tonal stability across two
    # timescales tracks structural predictability.
    # Golesorkhi 2021: core-periphery hierarchy η²=0.86.
    e2 = torch.sigmoid(
        0.50 * tonal_stab_100ms + 0.50 * tonal_stab_mean_1s
    )

    # -- E3: Feedforward-Feedback Balance --
    # >0.5 = feedforward dominant (Heschl→hippocampus), <0.5 = feedback.
    # Spectral coupling mean (low-level integration) vs tonal entropy
    # (high-level uncertainty).
    # Bonetti 2024: feedforward Heschl→Hippocampus→Cingulate, feedback reverse.
    e3 = torch.sigmoid(
        0.50 * spectral_auto_mean_1s - 0.50 * tonal_stab_entropy_1s
    )

    return e0, e1, e2, e3
