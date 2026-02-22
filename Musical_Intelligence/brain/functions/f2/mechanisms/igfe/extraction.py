"""IGFE E-Layer -- Extraction (2D).

Individual gamma frequency match and memory enhancement proxy:
  E0: igf_match          (how well stimulus frequency matches IGF)
  E1: memory_enhancement (enhancement proxy from stimulus properties)

R3 direct reads:
  periodicity:   [5]  -- frequency structure / gamma proxy
  amplitude:     [7]  -- stimulus intensity
  onset_strength:[11] -- temporal modulation rate
  tonalness:     [14] -- harmonic structure / IGF match

Extraction is R3-only: the E-layer derives raw gamma entrainment
features from spectral properties before temporal integration.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/igfe/
Galambos 1981: 40 Hz ASSR maximal at fronto-central sites.
Herrmann 2016: individual variation in peak gamma frequency.
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_PERIODICITY = 5          # frequency structure / gamma proxy
_AMPLITUDE = 7            # stimulus intensity
_ONSET_STRENGTH = 11      # temporal modulation rate
_TONALNESS = 14           # harmonic structure / IGF match


def compute_extraction(
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor]:
    """Compute E-layer: gamma frequency match and enhancement proxy.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.

    Returns:
        ``(E0, E1)`` each ``(B, T)``
    """
    periodicity = r3_features[..., _PERIODICITY]
    amplitude = r3_features[..., _AMPLITUDE]
    onset_strength = r3_features[..., _ONSET_STRENGTH]
    tonalness = r3_features[..., _TONALNESS]

    # -- E0: IGF Match --
    # How well the stimulus frequency structure aligns with the individual
    # gamma frequency. Periodicity captures frequency regularity (gamma
    # proxy), tonalness captures harmonic structure matching.
    # Galambos 1981: 40 Hz ASSR is maximal when stimulus matches neural gamma.
    # Herrmann 2016: peak gamma varies 30-80 Hz across individuals.
    e0 = torch.sigmoid(0.55 * periodicity + 0.45 * tonalness)

    # -- E1: Memory Enhancement Proxy --
    # Stimulus properties that predict cognitive enhancement: amplitude
    # (sufficient intensity for entrainment) and onset modulation rate
    # (temporal structure for gamma-band driving).
    # Bolland 2025: stimulus intensity and modulation rate predict effect size.
    e1 = torch.sigmoid(0.50 * amplitude + 0.50 * onset_strength)

    return e0, e1
