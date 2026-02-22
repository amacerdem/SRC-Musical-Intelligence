"""MEAMN P-Layer -- Cognitive Present (3D).

Three present-processing dimensions for memory retrieval state:

  P0: memory_state      -- Current memory retrieval activation [0, 1]
  P1: emotional_color   -- Affective tag strength on current memory [0, 1]
  P2: nostalgia_link    -- Nostalgia-familiarity warmth signal [0, 1]

H3 consumed:
    (14, 16, 0, 2)  tonalness value H16 L2         -- melodic recognition state
    (14, 20, 1, 0)  tonalness mean H20 L0          -- tonal stability over 5s
    (3, 24, 1, 0)   stumpf_fusion mean H24 L0      -- long-term binding context

R3 consumed:
    [4]      sensory_pleasantness  -- valence quality
    [25:33]  x_l0l5               -- memory binding (reused for P0)
    [41:49]  x_l5l7               -- nostalgia warmth (reused for P2)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/meamn/MEAMN-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_TONAL_VAL_1S = (14, 16, 0, 2)
_TONAL_MEAN_5S = (14, 20, 1, 0)
_STUMPF_MEAN_36S = (3, 24, 1, 0)

# -- R3 indices ----------------------------------------------------------------
_SENSORY_PLEASANTNESS = 4
_X_L5L7_START = 41
_X_L5L7_END = 49


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing from H3/R3 + E/M outputs.

    P-layer outputs are the primary relay exports:
        memory_state     -> familiarity computation
        emotional_color  -> reward: emotion component of hedonic signal
        nostalgia_link   -> familiarity + reward: nostalgia-enhanced binding

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    e0, e1, e2 = e_outputs
    m0, m1 = m_outputs

    tonal_val_1s = h3_features[_TONAL_VAL_1S]
    tonal_mean_5s = h3_features[_TONAL_MEAN_5S]
    stumpf_mean_36s = h3_features[_STUMPF_MEAN_36S]

    # R3 features
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)

    # P0: Memory state -- aggregated retrieval activation
    # Janata 2009: dorsal MPFC parametrically tracks autobiographical salience
    # Retrieval_dynamics aggregation from E-layer + M-layer
    p0 = torch.sigmoid(
        0.35 * e0 + 0.30 * m0 + 0.20 * tonal_val_1s
        + 0.15 * stumpf_mean_36s
    )

    # P1: Emotional coloring -- arousal * (1-roughness)
    # Sakakibara 2025: nostalgia enhances memory vividness (eta_p^2=0.541)
    # arousal * valence -> e2 captures emotional memory coloring, modulated
    # by tonal stability as recognition support
    p1 = torch.sigmoid(
        0.40 * e2 + 0.30 * pleasantness + 0.30 * tonal_mean_5s
    )

    # P2: Nostalgia link -- familiarity * x_l5l7.mean
    # Sakakibara 2025: acoustic similarity triggers nostalgia (Cohen's r=0.878 older)
    # familiarity from M1 (recall probability) x consonance-timbre interaction
    nostalgia_warmth = x_l5l7.mean(dim=-1)
    p2 = torch.sigmoid(
        0.40 * e1 + 0.35 * m1 * nostalgia_warmth
        + 0.25 * stumpf_mean_36s
    )

    return p0, p1, p2
