"""NEMAC P-Layer -- Cognitive Present (2D).

Present-time nostalgia-evoked memory-affect circuit signals:
  P0: nostalgia_correl     — Nostalgia correlation strength [0, 1]
  P1: memory_reward_lnk    — Memory-reward link strength [0, 1]

P0 captures the real-time correlation between nostalgic content and emotional
response. This is the present-moment reading of how strongly the musical
stimulus is evoking nostalgia -- the convergence of memory retrieval (M1),
self-referential processing (M0), and acoustic warmth. High P0 indicates
the listener is actively experiencing nostalgia. STG melodic template
recognition provides the acoustic familiarity signal that triggers the
nostalgia correlation (Sakakibara 2025).

P1 captures the link between memory retrieval and reward activation. When
hippocampal retrieval (M1) co-activates with ventral striatum reward
(SRP.pleasure), the memory-reward link is strong. This link mediates
the therapeutic effect: nostalgic memories that activate reward circuitry
produce wellbeing enhancement. Cheung 2019: pleasure peaks at moderate
surprise within familiar context -- the nostalgia sweet spot.

H3 demands consumed (3 tuples -- shared with other layers):
  (22, 20, 1, 0)  entropy mean H20 L0             -- complexity 5s
  (10, 20, 1, 0)  loudness mean H20 L0            -- arousal 5s
  (14, 20, 1, 0)  tonalness mean H20 L0           -- tonal stability 5s

R3 features:
  [4] sensory_pleasantness, [14] tonalness, [22] distribution_entropy

Janata 2009: mPFC tracks tonal movement (fMRI, N=13).
Cheung et al. 2019: surprise x uncertainty -> pleasure (N=39).
Sakakibara 2025: acoustic similarity triggers nostalgia (N=33).

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/nemac/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ENTROPY_MEAN_H20 = (22, 20, 1, 0)    # entropy mean H20 L0
_LOUD_MEAN_H20 = (10, 20, 1, 0)       # loudness mean H20 L0
_TONAL_MEAN_H20 = (14, 20, 1, 0)      # tonalness mean H20 L0

# -- R3 feature indices -------------------------------------------------------
_SENSORY_PLEASANTNESS = 4
_TONALNESS = 14
_ENTROPY = 22


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: nostalgia correlation and memory-reward link.

    P0 (nostalgia_correl) captures real-time nostalgia-emotion correlation.
    Convergence of memory retrieval (M1), self-referential (M0), and
    acoustic familiarity (tonalness). STG melodic template recognition
    provides acoustic familiarity. Sakakibara 2025: acoustic similarity
    triggers nostalgia (EEG, N=33, eta_p^2=0.636).

    P1 (memory_reward_lnk) captures memory-reward link strength. Hippocampal
    retrieval (M1) co-activating with chills (E0) + nostalgia intensity (W0).
    Mediates therapeutic effect: nostalgic memories activating reward produce
    wellbeing. Cheung 2019: pleasure at moderate surprise in familiar context.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(M0, M1, M2, W0, W1)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    e0, e1 = e
    m0, m1, m2, w0, _w1 = m

    # -- H3 features --
    entropy_mean = h3_features[_ENTROPY_MEAN_H20]    # (B, T)
    loud_mean = h3_features[_LOUD_MEAN_H20]          # (B, T)
    tonal_mean = h3_features[_TONAL_MEAN_H20]        # (B, T)

    # -- R3 features --
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    tonalness = r3_features[..., _TONALNESS]                # (B, T)

    # -- Derived signals --
    familiarity_5s = (1.0 - entropy_mean) * tonal_mean  # familiar + tonal = nostalgic

    # -- P0: Nostalgia Correlation --
    # Real-time nostalgia-emotion correlation: how strongly the current
    # musical stimulus evokes nostalgia. Convergence of memory retrieval,
    # self-referential processing, and acoustic familiarity.
    # Sakakibara 2025: acoustic similarity triggers nostalgia.
    # Janata 2009: mPFC parametrically tracks tonal space.
    p0 = torch.sigmoid(
        0.30 * m0 * m1.clamp(min=0.1)
        + 0.30 * e1 * familiarity_5s
        + 0.25 * tonalness * tonal_mean
        + 0.15 * pleasantness
    )

    # -- P1: Memory-Reward Link --
    # Connection between hippocampal retrieval and reward activation.
    # When memory vividness (M2) + nostalgia intensity (W0) converge
    # with chills (E0), the memory-reward link is active.
    # Cheung 2019: pleasure at moderate surprise in familiar context.
    p1 = torch.sigmoid(
        0.35 * m2 * w0.clamp(min=0.1)
        + 0.30 * e0 * loud_mean
        + 0.20 * m1 * pleasantness
        + 0.15 * familiarity_5s
    )

    return p0, p1
