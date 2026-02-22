"""STC M-Layer -- Temporal Integration (3D).

Temporal integration of interoceptive-motor extraction features:
  M0: connectivity_strength -- Insula-sensorimotor connectivity over time [0, 1]
  M1: respiratory_index     -- Respiratory control quality index [0, 1]
  M2: voice_body_coupling   -- Voice-body integration index [0, 1]

Connectivity strength integrates interoceptive coupling (f28) with
the raw interoceptive periodicity signal at 1s.
connectivity_strength = sigma(0.5 * f28 + 0.5 * interoceptive_period_1s).
Zamorano 2023: accumulated singing training predicts enhanced resting-state
connectivity between insula and speech/respiratory sensorimotor areas.

Respiratory index directly propagates f29 (respiratory integration).
The M-layer treats it as already temporally integrated by the E-layer's
combination of slow periodicity (1s) and fast entropy (100ms).

Voice-body coupling averages interoceptive coupling (f28) with speech
sensorimotor activation (f30).
voice_body_coupling = sigma(0.5 * f28 + 0.5 * f30).
Kleber 2013: right AIC connectivity with M1, S1, auditory cortex.

H3 demands consumed (1 new):
  (7, 8, 1, 2) amplitude mean H8 L2 -- Mean vocal intensity 500ms

R3 inputs: amplitude[7]

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/stc/m_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_INTERO_PER_H16 = (33, 16, 14, 2)    # x_l4l5 periodicity H16 L2 (shared E)
_AMP_MEAN_H8 = (7, 8, 1, 2)          # amplitude mean H8 L2 (new M-layer)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute M-layer: 3D temporal integration of singing connectivity.

    M0 (connectivity_strength): sigma(0.5 * f28 + 0.5 * interoceptive_period_1s).
    Zamorano 2023: training predicts enhanced resting-state connectivity.

    M1 (respiratory_index): Directly propagates f29.
    Zarate 2008: ACC + pSTS + anterior insula.

    M2 (voice_body_coupling): sigma(0.5 * f28 + 0.5 * f30).
    Kleber 2013: right AIC to M1/S1/auditory connectivity.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e_outputs: ``(f28, f29, f30)`` from extraction layer.
        upstream_outputs: ``{"MSR": (B, T, 11), "SPMC": (B, T, 11)}``.

    Returns:
        ``(connectivity_strength, respiratory_index, voice_body_coupling)``
        each ``(B, T)``.
    """
    f28, f29, f30 = e_outputs

    # -- H3 features (shared with E-layer) --
    intero_per_1s = h3_features[_INTERO_PER_H16]    # (B, T)

    # -- M0: Connectivity Strength --
    # sigma(0.5 * f28 + 0.5 * interoceptive_period_1s)
    # Zamorano 2023: singing training -> insula-sensorimotor connectivity
    connectivity_strength = torch.sigmoid(
        0.50 * f28
        + 0.50 * intero_per_1s
    )

    # -- M1: Respiratory Index --
    # Direct propagation of f29 (already temporally integrated)
    # Zarate 2008: ACC + pSTS + anterior insula network
    respiratory_index = f29

    # -- M2: Voice-Body Coupling --
    # sigma(0.5 * f28 + 0.5 * f30)
    # Kleber 2013: right AIC -> M1, S1, auditory cortex
    voice_body_coupling = torch.sigmoid(
        0.50 * f28
        + 0.50 * f30
    )

    return connectivity_strength, respiratory_index, voice_body_coupling
