"""PNH P-Layer — Cognitive Present (3D).

Three present-processing dimensions for ratio encoding, conflict, and preference:

  P0: ratio_encoding         — Current ratio encoding state [0, 1]
  P1: conflict_monitoring    — Current IFG/ACC conflict activation [0, 1]
  P2: consonance_preference  — Consonance-preference binding [0, 1]

H3 consumed:
    (4, 18, 19, 0)  sensory_pleasantness stability H18 L0  — consonance stability (2s)
    (14, 10, 0, 2)  tonalness value H10 L2                 — ratio purity (400ms)
    (17, 10, 14, 2) spectral_autocorrelation period H10 L2 — harmonic regularity (400ms)

R3 consumed:
    [0]  roughness  — sensory dissonance for preference binding

See Building/C3-Brain/F4-Memory-Systems/mechanisms/pnh/PNH-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_PLEASANT_STAB_2S = (4, 18, 19, 0)
_TONALNESS_VAL_400MS = (14, 10, 0, 2)
_SPECAUTOCORR_PERIOD_400MS = (17, 10, 14, 2)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    h_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing from H3/R3 + H/M outputs.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h_outputs: ``(H0, H1, H2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    _h0, h1, _h2 = h_outputs
    m0, m1 = m_outputs

    # -- R3 slices -------------------------------------------------------------
    roughness = r3_features[..., _ROUGHNESS]  # (B, T)

    # -- H3 lookups ------------------------------------------------------------
    pleasant_stab = h3_features[_PLEASANT_STAB_2S]           # (B, T)
    tonalness_val = h3_features[_TONALNESS_VAL_400MS]        # (B, T)
    specautocorr_period = h3_features[_SPECAUTOCORR_PERIOD_400MS]  # (B, T)

    # -- P0: Ratio encoding — current state of Pythagorean hierarchy -----------
    # Tabas et al. 2019: consonant dyads produce earlier/larger POR in alHG
    # harmony = harmonic context summarizing current key/chord stability
    harmony = 0.50 * tonalness_val + 0.50 * specautocorr_period
    p0 = torch.sigmoid(harmony)

    # -- P1: Conflict monitoring — IFG/ACC conflict signal ---------------------
    # Kim et al. 2021: R-IFG to L-IFG connectivity for syntactic irregularity
    # pred_error proxy from H1 conflict and M1 neural activation
    pred_error = h1 * m1
    p1 = torch.sigmoid(pred_error)

    # -- P2: Consonance preference — structural expectation x consonance -------
    # Sarasso et al. 2019: aesthetic appreciation enhances attention (eta_p^2=0.685)
    # struct_expect proxy: consonance stability over phrase
    struct_expect = pleasant_stab
    p2 = torch.sigmoid(struct_expect * (1.0 - roughness))

    return p0, p1, p2
