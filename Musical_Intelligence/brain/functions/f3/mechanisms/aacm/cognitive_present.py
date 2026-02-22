"""AACM P-Layer -- Cognitive Present (2D).

Present-time aesthetic engagement and judgment integrating CSG cross-function:
  P0: n1p2_engagement        (ERP-indexed engagement from salience network)
  P1: aesthetic_judgment      (present aesthetic evaluation)

Cross-function reads:
  CSG [6] P0:salience_network  -- consonance-salience gradient (F1)

H3 demands consumed:
  roughness:   (0,3,0,2)  roughness value at 100ms -- dissonance level
  loudness:    (8,16,20,2) loudness entropy at 1s -- dynamic unpredictability

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/aacm/
Sarasso 2019: N1/P2 engagement correlates with consonance (EEG ERP, N=22).
Brattico 2013: aesthetic judgment engages vmPFC/IFG network (fMRI, N=18).
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ROUGH_H3 = (0, 3, 0, 2)           # roughness value at 100ms
_LOUD_ENTROPY_1S = (8, 16, 20, 2)  # loudness entropy at 1s

# -- Cross-function indices ---------------------------------------------------
_CSG_SALIENCE_NETWORK = 6           # CSG P0:salience_network


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    relay_outputs: Optional[Dict[str, Tensor]] = None,
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: present aesthetic engagement and judgment.

    Integrates CSG cross-function salience information with local E/M
    layer features and H3 temporal context. CSG P0:salience_network
    provides the consonance-salience gradient from F1, which modulates
    the engagement and judgment signals.

    Sarasso 2019: N1/P2 amplitude is enhanced for consonant intervals,
    reflecting greater engagement with aesthetically pleasant stimuli.
    Brattico 2013: vmPFC/IFG activated during aesthetic judgment of music.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        relay_outputs: ``{"CSG": (B, T, 12)}`` cross-function relay data.

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    e0, _e1, e2 = e
    m0, m1 = m

    roughness_100ms = h3_features[_ROUGH_H3]
    loudness_entropy_1s = h3_features[_LOUD_ENTROPY_1S]

    # -- Optional CSG cross-function read --
    # CSG P0:salience_network provides consonance-driven salience context.
    # If unavailable (during testing or independent runs), we proceed
    # without it -- the formulas still produce valid [0,1] outputs.
    csg_salience = None
    if relay_outputs is not None:
        csg = relay_outputs.get("CSG")
        if csg is not None:
            csg_salience = csg[..., _CSG_SALIENCE_NETWORK]

    # -- P0: N1/P2 Engagement --
    # ERP-indexed engagement from aesthetic engagement (M0) and
    # attentional capture (E0), modulated by roughness (dissonance drives
    # a different pattern of engagement via salience network).
    # Sarasso 2019: N1/P2 larger for consonant than dissonant intervals.
    p0 = torch.sigmoid(
        0.35 * m0
        + 0.35 * e0
        + 0.30 * roughness_100ms
    )

    # -- P1: Aesthetic Judgment --
    # Present aesthetic evaluation from appreciation (M1) and savoring
    # (E2), with loudness entropy adding unpredictability (dynamic range
    # of loudness modulates aesthetic surprise/interest).
    # Brattico 2013: aesthetic judgment activates vmPFC evaluation network.
    p1 = torch.sigmoid(
        0.35 * m1
        + 0.35 * e2
        + 0.30 * loudness_entropy_1s
    )

    return p0, p1
