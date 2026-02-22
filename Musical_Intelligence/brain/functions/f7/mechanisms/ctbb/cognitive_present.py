"""CTBB P-Layer -- Cognitive Present (2D).

Present-moment cerebellar motor timing state:
  P0: timing_precision  -- Temporal-context cerebellar timing precision [0, 1]
  P1: motor_stability   -- Beat-entrainment motor output stability [0, 1]

Timing precision (P0) represents the current precision of the cerebellar
timing circuit at the cognitive present, integrating E-layer cerebellar
timing (f25) with M-layer timing enhancement dynamics. Higher values
indicate more precise motor timing, consistent with reduced timing
variability after cerebellar iTBS. Ivry 1988: lateral cerebellum
dissociation for timing vs execution.

Motor stability (P1) captures the stability of motor output in the current
cognitive window, combining sway reduction with cerebellar-M1 coupling
strength. Higher values indicate more stable motor performance. Sansare
2025: Bonferroni POST1-6 all p < .05.

H3 demands consumed: None new (uses E-layer and M-layer outputs).

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/ctbb/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: timing precision and motor stability.

    P0 (timing_precision): Integrates cerebellar timing (f25) with
    timing enhancement dynamics from M-layer. Represents instantaneous
    precision of the cerebellar timing module.
    Ivry 1988: lateral cerebellum as timing controller.

    P1 (motor_stability): Integrates sway reduction and cerebellar-M1
    coupling from M-layer into a single stability index. Maps to how
    stably the motor system maintains beat entrainment.
    Sansare 2025: improved balance POST1-6.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e_outputs: ``(E0, E1, E2)`` from extraction layer.
        m_outputs: ``(M0, M1, M2)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    e0, _e1, _e2 = e_outputs   # f25, f26, f27
    m0, m1, m2 = m_outputs     # timing_enhancement, sway_reduction, coupling

    # -- P0: Timing Precision --
    # Synthesises cerebellar timing (f25) with timing enhancement (M0)
    # Ivry 1988: lateral cerebellum timing dissociation
    # In music listening: precision of cerebellar rhythmic tracking
    p0 = torch.sigmoid(
        0.50 * e0
        + 0.50 * m0
    )

    # -- P1: Motor Stability --
    # Integrates sway reduction (M1) and cerebellar-M1 coupling (M2)
    # Sansare 2025: behavioural balance improvement
    # In music: stability of motor entrainment to beat
    p1 = torch.sigmoid(
        0.50 * m1
        + 0.50 * m2
    )

    return p0, p1
