"""DDSMI M-Layer -- Temporal Integration (3D).

Dyadic Dance Social Motor Integration temporal integration signals:
  M0: mTRF_social    -- Social coordination mTRF weight [0, 1]
  M1: mTRF_auditory  -- Auditory tracking mTRF weight [0, 1]
  M2: mTRF_balance   -- Social/auditory resource balance [0, 1]

M0 directly inherits from f13 (social_coordination). The social coordination
feature IS the mTRF social weight -- both measure how strongly the neural
system tracks the partner during dance interaction.

M1 directly inherits from f14 (music_tracking). The music tracking feature IS
the mTRF auditory weight -- both measure how strongly the neural system tracks
the musical stimulus.

M2 computes the relative allocation of processing resources between social and
auditory streams. Combines f13 (social strength) with inverted f14 (1 - music
strength). When both social tracking is strong and music tracking is weak (the
visual-contact condition in Bigand 2025), the balance shifts toward social
processing. This captures the core resource competition finding: visual contact
reallocates processing from auditory to social streams.

H3 demands consumed: 0 new tuples (all computation from E-layer features).

Bigand et al. 2025: visual contact x music interaction F(1,57)=50.10, p<.001.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/ddsmi/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_temporal_integration(
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute M-layer: mTRF weights and resource balance.

    M0 (mTRF_social) directly inherits from f13 (social coordination).
    The social coordination feature IS the mTRF social weight -- both
    measure partner tracking strength during dance interaction.

    M1 (mTRF_auditory) directly inherits from f14 (music tracking).
    The music tracking feature IS the mTRF auditory weight -- both
    measure auditory stimulus tracking strength.

    M2 (mTRF_balance) computes relative processing resource allocation.
    sigma(0.5 * f13 + 0.5 * (1 - f14)). Values above 0.5 indicate
    social-dominant processing (visual contact condition), values below
    0.5 indicate music-dominant processing.
    Bigand 2025: visual contact x music interaction F(1,57)=50.10.

    Args:
        e: ``(E0, E1, E2)`` from extraction layer -- f13, f14, f15.

    Returns:
        ``(M0, M1, M2)`` each ``(B, T)``
    """
    f13, f14, _f15 = e

    # -- M0: mTRF Social --
    # Social coordination mTRF weight = f13.
    # Bigand 2025: social mTRF is the dominant process with visual contact.
    m0 = f13

    # -- M1: mTRF Auditory --
    # Auditory tracking mTRF weight = f14.
    # Bigand 2025: music mTRF with music presence F(1,57)=30.22.
    m1 = f14

    # -- M2: mTRF Balance --
    # Social/auditory resource balance. Combines social strength with
    # inverted music strength: when social is high and music is low,
    # balance > 0.5 (social-dominant). This captures the visual contact
    # resource reallocation from auditory to social processing.
    # Bigand 2025: visual contact x music F(1,57)=50.10, p<.001.
    m2 = torch.sigmoid(
        0.50 * f13 + 0.50 * (1.0 - f14)
    )

    return m0, m1, m2
