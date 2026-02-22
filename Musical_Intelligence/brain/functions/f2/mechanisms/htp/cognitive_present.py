"""HTP P-Layer — Cognitive Present (3D).

Present-processing prediction match at each hierarchy level:
  P0: sensory_match        (low-level prediction match in A1)
  P1: pitch_prediction     (mid-level pitch prediction in belt cortex)
  P2: abstract_prediction  (high-level abstract prediction in STG/hippocampus)

H3 demands consumed:
  amplitude:       (7,3,0,2)
  onset_strength:  (11,0,0,2)
  sharpness:       (13,3,0,2)
  spectral_auto:   (17,3,0,2) reused
  tonal_stability: (60,8,0,0) reused

R3 direct reads:
  tristimulus[18:21] — mean for abstract prediction

See Docs/C3/Models/PCU-a1-HTP/HTP.md §6.1 Layer P.
Norman-Haignere et al. 2022: hierarchical integration 50-400ms in auditory cortex.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_TRISTIMULUS_START = 18
_TRISTIMULUS_END = 21

# -- H3 keys consumed ---------------------------------------------------------
_AMPLITUDE_H3_VAL = (7, 3, 0, 2)
_ONSET_H0_VAL = (11, 0, 0, 2)
_SHARPNESS_H3_VAL = (13, 3, 0, 2)
_SPECTRAL_AUTO_H3_VAL = (17, 3, 0, 2)
_TONAL_STAB_H8_VAL = (60, 8, 0, 0)


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: present-processing prediction match.

    Each dimension measures how well the current input matches predictions
    at that hierarchy level. Post-stimulus, high-level representations
    are "silenced" (explained away) while low-level persist as PE.

    Forseth et al. 2020: dual prediction mechanisms in early auditory cortex
    (timing via low-freq phase in HG, content via high-gamma in PT).

    Args:
        r3_features: ``(B, T, 97)`` raw R3.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        m: ``(M0, M1, M2)`` from temporal integration layer.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``
    """
    m0, m1, m2 = m

    trist_mean = r3_features[..., _TRISTIMULUS_START:_TRISTIMULUS_END].mean(
        dim=-1
    )

    amplitude_h3 = h3_features[_AMPLITUDE_H3_VAL]
    onset_h0 = h3_features[_ONSET_H0_VAL]
    sharpness_h3 = h3_features[_SHARPNESS_H3_VAL]
    spectral_auto_h3 = h3_features[_SPECTRAL_AUTO_H3_VAL]
    tonal_stab_h8 = h3_features[_TONAL_STAB_H8_VAL]

    # -- P0: Sensory Match --
    # Low-level prediction match: onset detection + amplitude context
    # gated by M2 latency strength. Persists post-stimulus (PE signal).
    p0 = torch.sigmoid(
        0.40 * m2 + 0.30 * amplitude_h3 + 0.30 * onset_h0
    )

    # -- P1: Pitch Prediction --
    # Mid-level pitch template match: brightness + spectral coupling
    # gated by M1 latency strength. Planum temporale high-gamma.
    p1 = torch.sigmoid(
        0.40 * m1 + 0.30 * sharpness_h3 + 0.30 * spectral_auto_h3
    )

    # -- P2: Abstract Prediction --
    # High-level abstract pattern match: tonal stability + harmonic balance
    # gated by M0 latency. Silenced post-stimulus when prediction is correct.
    # Bonetti et al. 2024: hippocampus/cingulate feedforward for sequence.
    p2 = torch.sigmoid(
        0.40 * m0 + 0.30 * tonal_stab_h8 + 0.30 * trist_mean
    )

    return p0, p1, p2
