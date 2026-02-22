"""MEAMR P-Layer -- Cognitive Present (1D).

Present-time autobiographical memory activation signal:
  P0: memory_activation_state -- Current autobio memory activation level [0, 1]

Integrates familiarity (E0) and autobiographical salience (E1) into a single
memory activation signal. Balanced 0.5/0.5 combination ensures music must be
both familiar AND autobiographically salient for strong memory activation --
either alone produces only moderate activation. This mirrors the dMPFC
response pattern where activation requires both familiarity and
autobiographical relevance (Janata 2009).

The memory activation signal has a long sustain (tau_decay = 10.0s) reflecting
the extended nature of autobiographical memory retrieval, which unfolds over
seconds.

H3 demands consumed: None new -- reuses E-layer outputs (f01, f02).
  The P-layer doc lists 3 tuples that are already in the E-layer demand set:
    (4, 16, 18, 2)   pleasantness trend 1s -- via f01
    (12, 16, 1, 2)   mean warmth 1s -- via f01
    (41, 16, 18, 2)  memory-structure trend 1s -- via f02
  These are consumed via E-layer outputs, not directly.

Janata 2009: dMPFC activation proportional to autobiographical salience
(P < 0.001, FDR P < 0.025, fMRI, N = 13).
Salimpoor 2011: DA release during familiar music (PET, N = 8, r = 0.71).

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/meamr/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_cognitive_present(
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor]:
    """Compute P-layer: 1D memory activation state.

    P0 (memory_activation_state): Collapses E-layer into a single real-time
    memory activation signal. Equal weighting of familiarity (E0) and
    autobiographical salience (E1) ensures both must be present for strong
    activation.

    sigma(0.5 * f02 + 0.5 * f01)

    Janata 2009: dMPFC requires both familiarity and autobiographical
    relevance (FDR P < 0.025, fMRI, N = 13).
    Salimpoor 2011: DA release during familiar music (r = 0.71, PET, N = 8).

    Args:
        e: ``(E0, E1, E2, E3)`` from extraction layer, each ``(B, T)``.

    Returns:
        ``(P0,)`` each ``(B, T)``.
    """
    e0, e1, _e2, _e3 = e

    # -- P0: Memory Activation State --
    # sigma(0.5 * f02 + 0.5 * f01)
    # Janata 2009: dMPFC requires familiarity + autobio for full activation
    p0 = torch.sigmoid(
        0.50 * e1
        + 0.50 * e0
    )

    return (p0,)
