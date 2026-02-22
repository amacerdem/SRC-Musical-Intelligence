"""STC P-Layer -- Cognitive Present (2D).

Present-moment interoceptive-motor integration state:
  P0: insula_activity -- Temporal-context interoceptive monitoring level [0, 1]
  P1: vocal_motor     -- Beat-entrainment vocal motor output level [0, 1]

Insula activity synthesizes interoceptive coupling (f28) with
connectivity strength from the M-layer. Represents the instantaneous
engagement of the anterior insula in monitoring vocal and respiratory
states.  Kleber 2013: right AIC (MNI 48, 0, -3; F = 22.08 expertise x
anesthesia interaction).

Vocal motor integrates speech sensorimotor activation (f30) with
voice-body coupling from the M-layer. Captures the current level of
vocal motor engagement during music processing.  Even in passive
listening, the vocal motor system shows subthreshold activation
(Zarate 2010: involuntary pitch correction).

H3 demands consumed: None new (uses E-layer and M-layer outputs).

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/stc/p_layer.md
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
    """Compute P-layer: insula activity and vocal motor output.

    P0 (insula_activity): sigma(0.5 * f28 + 0.5 * connectivity_strength).
    Kleber 2013: right anterior insula is the interoceptive hub;
    disrupting somatosensory feedback differentially modulates AIC
    in singers vs nonsingers.

    P1 (vocal_motor): sigma(0.5 * f30 + 0.5 * voice_body_coupling).
    Zarate 2010: involuntary pitch correction supports automatic
    interoceptive-motor loop.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e_outputs: ``(f28, f29, f30)`` from extraction layer.
        m_outputs: ``(connectivity_strength, respiratory_index,
                      voice_body_coupling)`` from temporal integration.

    Returns:
        ``(insula_activity, vocal_motor)`` each ``(B, T)``.
    """
    f28, _f29, f30 = e_outputs
    connectivity_strength, _respiratory_index, voice_body_coupling = m_outputs

    # -- P0: Insula Activity --
    # sigma(0.5 * f28 + 0.5 * connectivity_strength)
    # Kleber 2013: right AIC is the interoceptive hub
    # Zamorano 2023: insula monitors vocal and respiratory states
    insula_activity = torch.sigmoid(
        0.50 * f28
        + 0.50 * connectivity_strength
    )

    # -- P1: Vocal Motor --
    # sigma(0.5 * f30 + 0.5 * voice_body_coupling)
    # Zarate 2010: involuntary pitch correction (automatic motor loop)
    vocal_motor = torch.sigmoid(
        0.50 * f30
        + 0.50 * voice_body_coupling
    )

    return insula_activity, vocal_motor
