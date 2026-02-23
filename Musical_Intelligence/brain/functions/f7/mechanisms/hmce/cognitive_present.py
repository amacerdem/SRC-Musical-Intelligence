"""HMCE P-Layer -- Cognitive Present (3D).

Three present-processing dimensions for encoding state:

  P0: a1_stg_encoding  -- Current A1-STG encoding strength
  P1: context_predict   -- Contextual predictability
  P2: phrase_expect     -- Phrase-level expectation signal

H3 consumed:
    (7, 3, 0, 0)    amplitude value H3     -- instantaneous dynamic level
    (11, 3, 0, 0)   onset_strength value H3 -- current event salience
    (17, 8, 14, 0)  spectral_autocorr period H8 -- tonal regularity at theta
    (60, 3, 0, 0)   x_l0l2l5 value H3     -- instantaneous context

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/hmce/HMCE-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_AMPLITUDE_H3 = (7, 3, 0, 0)
_ONSET_H3 = (11, 3, 0, 0)
_SPECTRAL_AUTO_PERIOD_H8 = (17, 8, 14, 0)
_HIER_VALUE_H3 = (60, 3, 0, 0)


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing from H3 + E/M outputs.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03)`` each ``(B, T)``.
        m_outputs: ``(M0, M1, M2)`` each ``(B, T)``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    f01, f02, f03 = e_outputs
    m0, m1, m2 = m_outputs

    B, T = r3_features.shape[:2]
    device = r3_features.device
    zero = torch.zeros(B, T, device=device)

    # H3 features
    amplitude_h3 = h3_features.get(_AMPLITUDE_H3, zero)
    onset_h3 = h3_features.get(_ONSET_H3, zero)
    spectral_auto_period_h8 = h3_features.get(_SPECTRAL_AUTO_PERIOD_H8, zero)
    hier_value_h3 = h3_features.get(_HIER_VALUE_H3, zero)

    # P0: A1-STG Encoding -- current encoding strength
    # Koelsch 2009: A1-STG cascade encodes local events
    p0 = torch.sigmoid(
        0.25 * f01
        + 0.25 * onset_h3
        + 0.25 * amplitude_h3
        + 0.25 * hier_value_h3
    )

    # P1: Context Predict -- contextual predictability
    # Pearce 2018: information content reflects contextual prediction
    p1 = torch.sigmoid(
        0.30 * m1
        + 0.25 * spectral_auto_period_h8
        + 0.25 * f02
        + 0.20 * m0
    )

    # P2: Phrase Expect -- phrase-level expectation signal
    # Koelsch 2009: phrase boundaries generate specific ERP responses
    p2 = torch.sigmoid(
        0.30 * f03
        + 0.25 * m2
        + 0.25 * m1
        + 0.20 * f02
    )

    return p0, p1, p2
