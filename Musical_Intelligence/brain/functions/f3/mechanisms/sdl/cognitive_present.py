"""SDL P-Layer -- Cognitive Present (2D).

Present-processing lateralization dynamics with upstream STANM integration:
  P0: dynamic_lateral_p     (present lateralization state, TANH [-1, 1])
  P1: hemispheric_engage    (hemispheric engagement level, sigmoid [0, 1])

Upstream STANM (Encoder, 11D) consumed:
  STANM[6]  = P0:temporal_alloc   -- temporal resource allocation
  STANM[7]  = P1:spectral_alloc   -- spectral resource allocation

H3 demands consumed:
  x_l4l5:  (37,16,1,2)  cross-stream mean 1s -- sustained bilateral
  x_l4l5:  (37,16,17,2) cross-stream peaks 1s -- oscillatory marker (reused)

E/M-layer inputs:
  E0: dynamic_lateral       (lateralization, tanh)
  E2: hemispheric_osc       (oscillatory state, sigmoid)
  M0: lateralization_index  (integrated lateralization, tanh)

CRITICAL: P0 uses torch.tanh, producing values in [-1, 1].

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/sdl/
Poeppel 2003: asymmetric sampling in time.
Zatorre 2002: hemispheric specialization review.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_XSTREAM_H16_MEAN = (37, 16, 1, 2)     # cross-stream mean 1s -- sustained bilateral
_XSTREAM_H16_PEAKS = (37, 16, 17, 2)   # cross-stream peaks 1s -- oscillatory marker

# -- STANM upstream output indices (Encoder, 11D) -----------------------------
_STANM_P0_TEMPORAL_ALLOC = 6   # P0:temporal_alloc
_STANM_P1_SPECTRAL_ALLOC = 7   # P1:spectral_alloc


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: present lateralization state with STANM integration.

    P0 integrates M0 (lateralization index), E0 (dynamic lateral), and
    cross-stream mean at 1s to produce the current lateralization state.
    Uses tanh to maintain [-1, 1] range.

    P1 captures hemispheric engagement by combining E2 (oscillatory state),
    cross-stream peaks (oscillatory markers), and STANM spectral allocation
    (upstream attention resource for spectral processing).

    Falls back to E/M + H3 features if STANM is unavailable.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        upstream_outputs: ``{"STANM": (B, T, 11)}``.

    Returns:
        ``(P0, P1)`` each ``(B, T)``
        P0 in [-1, 1] (tanh); P1 in [0, 1] (sigmoid).
    """
    e0, _e1, e2 = e
    m0, _m1 = m

    cross_stream_mean_1s = h3_features[_XSTREAM_H16_MEAN]
    cross_stream_peaks_1s = h3_features[_XSTREAM_H16_PEAKS]

    # -- Read STANM upstream --
    stanm = upstream_outputs.get("STANM")
    if stanm is not None:
        stanm_spectral_alloc = stanm[..., _STANM_P1_SPECTRAL_ALLOC]  # (B, T)
    else:
        # Fallback: use E2 oscillatory state as proxy for spectral allocation
        stanm_spectral_alloc = e2

    # -- P0: Dynamic Lateral (Present) --
    # Current lateralization state: M0 (integrated lateralization) + E0
    # (dynamic lateral) + sustained bilateral processing (cross-stream mean).
    # Poeppel 2003: lateralization state reflects asymmetric sampling.
    p0 = torch.tanh(
        0.40 * m0
        + 0.30 * e0
        + 0.30 * cross_stream_mean_1s
    )

    # -- P1: Hemispheric Engagement --
    # How strongly both hemispheres are engaged: E2 (oscillatory state)
    # captures oscillatory readiness; cross-stream peaks mark bilateral
    # events; STANM spectral_alloc provides upstream attention context.
    # Zatorre 2002: bilateral engagement for complex stimuli.
    p1 = torch.sigmoid(
        0.40 * e2
        + 0.30 * cross_stream_peaks_1s
        + 0.30 * stanm_spectral_alloc
    )

    return p0, p1
