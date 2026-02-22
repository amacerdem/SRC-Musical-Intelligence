"""IUCP P-Layer -- Cognitive Present (1D).

Present-time complexity preference signal:
  P0: current_preference_state -- Real-time liking level [0, 1]

P0 collapses the 4D extraction space into a single real-time preference
signal. It combines the two independent inverted-U curves (IC liking and
entropy liking) with equal weighting.

The balanced 0.5/0.5 combination reflects Gold 2019's finding that both IC
and entropy independently predict liking with comparable effect sizes:
IC R2 = 26.3% vs entropy R2 = 19.1% (Study 1), converging in Study 2
(41.6% vs 34.9%). High output indicates the music is in the listener's
"sweet spot" of optimal complexity; low output indicates either boredom
(too simple) or aversion (too complex).

H3 demands consumed: None new -- reuses E-layer outputs (f01, f02).

Gold et al. 2019: liking jointly predicted by IC + entropy (fMRI, N=43+27).
Gold et al. 2023b: VS reward signal tracks average liking, F(1,22) = 4.83,
p = 0.039.

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/iucp/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_cognitive_present(
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor]:
    """Compute P-layer: real-time complexity preference state.

    P0 (current_preference_state) integrates IC liking (E0) and entropy
    liking (E1) into a unified preference signal. Equal weighting reflects
    comparable effect sizes from Gold 2019 (IC R2 ~26-42%, entropy R2
    ~19-35%). High values = music is in the listener's optimal complexity
    zone.

    Gold et al. 2019: both IC and entropy independently predict liking.
    Gold et al. 2023b: VS reward signal tracks this combined preference.

    Args:
        e: ``(E0, E1, E2, E3)`` from extraction layer.

    Returns:
        ``(P0,)`` each ``(B, T)``
    """
    e0, e1, _e2, _e3 = e

    # -- P0: Current Preference State --
    # sigma(0.5 * f01 + 0.5 * f02)
    # Equal weighting: IC and entropy contribute comparably to liking.
    # Gold 2019: IC R2=26.3% vs entropy R2=19.1% (Study 1), converging
    # in Study 2 (41.6% vs 34.9%).
    p0 = torch.sigmoid(
        0.50 * e0
        + 0.50 * e1
    )

    return (p0,)
