"""DDSMI P-Layer -- Cognitive Present (2D).

Dyadic Dance Social Motor Integration present-state signals:
  P0: partner_sync       -- Current partner synchronization level [0, 1]
  P1: music_entrainment  -- Current music entrainment level [0, 1]

P0 captures the instantaneous quality of interpersonal motor synchronization.
Derived from the interaction of social mTRF weight (M-layer) with the
fast-scale social coupling signals. When social coordination is strong and
the partner's movements are being tracked accurately, partner_sync is high.
This feeds downstream to ARU (social reward) because successful partner
synchronization is inherently rewarding.

P1 captures the instantaneous state of auditory-motor coupling with the music.
Derived from the interaction of auditory mTRF weight (M-layer) with music
coupling signals. Operates somewhat independently of partner_sync -- Bigand
2025 found that self-movement (motor control for the music) is autonomous
from social context (all ps>.224). However, resource competition means that
when partner_sync demands increase (visual contact), music_entrainment may
decrease.

H3 demands consumed: 0 new tuples (all computation from upstream layers).

Wohltjen et al. 2023: beat entrainment predicts social synchrony (d=1.37).
Kohler et al. 2025: self-produced actions in left M1, other-produced in
right PMC.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/ddsmi/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_cognitive_present(
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: current partner sync and music entrainment state.

    P0 (partner_sync) reflects instantaneous interpersonal motor
    synchronization quality. Social mTRF weight (M0) gated by resource
    balance (M2) determines how strongly the motor system is coupled to
    the partner. When social tracking is dominant (M2 > 0.5) and social
    coordination is strong (M0 high), partner_sync peaks.
    Wohltjen 2023: beat entrainment predicts social synchrony (d=1.37).

    P1 (music_entrainment) reflects instantaneous auditory-motor coupling.
    Auditory mTRF weight (M1) combined with music tracking (E1) determines
    coupling strength. Somewhat independent of partner_sync -- self-movement
    tracking is autonomous from social context (Bigand 2025: ps>.224).
    However, resource competition via M2 modulates this.

    Args:
        e: ``(E0, E1, E2)`` from extraction layer -- f13, f14, f15.
        m: ``(M0, M1, M2)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    f13, f14, _f15 = e
    mTRF_social, mTRF_auditory, mTRF_balance = m

    # -- P0: Partner Sync --
    # Real-time partner synchronization from social mTRF weight (M0)
    # gated by resource balance (M2). Social coordination (f13) provides
    # the raw tracking signal. When M2 > 0.5 (social-dominant), the system
    # is allocating more resources to partner tracking.
    # Wohltjen 2023: beat entrainment predicts social synchrony (d=1.37).
    p0 = torch.sigmoid(
        0.40 * mTRF_social * mTRF_balance.clamp(min=0.1)
        + 0.35 * f13 * mTRF_balance.clamp(min=0.1)
        + 0.25 * mTRF_social
    )

    # -- P1: Music Entrainment --
    # Real-time auditory-motor coupling from auditory mTRF weight (M1)
    # combined with music tracking signal (f14). Inverse balance (1-M2)
    # reflects music-dominant processing. Self-movement tracking is
    # autonomous (Bigand 2025: ps>.224), but resource competition means
    # increased social demands reduce music entrainment.
    p1 = torch.sigmoid(
        0.40 * mTRF_auditory * (1.0 - mTRF_balance).clamp(min=0.1)
        + 0.35 * f14 * mTRF_auditory.clamp(min=0.1)
        + 0.25 * mTRF_auditory
    )

    return p0, p1
