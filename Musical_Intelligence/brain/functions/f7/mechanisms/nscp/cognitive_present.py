"""NSCP P-Layer -- Cognitive Present (2D).

Instantaneous state of neural synchrony and motor groove:
  P0: coherence_level -- Beat-entrainment cross-layer coherence [0, 1]
  P1: groove_response -- Beat-entrainment motor response level [0, 1]

Coherence level (P0) tracks the instantaneous state of neural coherence
across spectral feature layers, serving as a real-time ISC proxy. Uses
the shortest H3 horizons (25ms, 50ms, 100ms) of the cross-layer coupling
signal (x_l0l5). Leeuwis 2021: ISC strongest at frontocentral and temporal
electrodes during beat-driven passages. Hasson 2004: ISC content-driven
and reliable at moment-to-moment timescales.

Groove response (P1) tracks the current motor engagement state reflecting
population-level rhythmic entrainment. Combines short-timescale onset
tracking with loudness entropy for dynamic modulation. Spiech 2022: pupil
drift rate indexes groove perception moment-by-moment. Sarasso 2019:
consonance enhances motor inhibition engagement in real time.

H3 demands consumed (6):
  (10, 0, 0, 2) onset value 25ms L2            -- groove present state
  (10, 3, 0, 2) onset value 100ms L2           -- groove present state
  (25, 0, 0, 2) coherence value 25ms L2        -- coherence present state
  (25, 3, 0, 2) coherence value 100ms L2       -- coherence present state
  (10, 1, 1, 2) mean onset 50ms L2             -- groove smoothing
  (25, 1, 1, 2) mean coherence 50ms L2         -- coherence smoothing

R3 inputs: spectral_flux[10], x_l0l5[25:33]

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/nscp/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_ONSET_VAL_25MS = (10, 0, 0, 2)       # spectral_flux value H0 L2
_ONSET_VAL_100MS = (10, 3, 0, 2)      # spectral_flux value H3 L2
_COHERENCE_VAL_25MS = (25, 0, 0, 2)   # x_l0l5 value H0 L2
_COHERENCE_VAL_100MS = (25, 3, 0, 2)  # x_l0l5 value H3 L2
_ONSET_MEAN_50MS = (10, 1, 1, 2)      # spectral_flux mean H1 L2
_COHERENCE_MEAN_50MS = (25, 1, 1, 2)  # x_l0l5 mean H1 L2


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: instantaneous coherence and groove.

    P0 (coherence_level): Real-time cross-layer coherence state from
    shortest H3 horizons (25ms instantaneous, 50ms mean, 100ms value)
    of the x_l0l5 signal. Captures moment-to-moment ISC fluctuations.
    Leeuwis 2021: ISC strongest at frontocentral/temporal electrodes.
    Hasson 2004: ISC reliable at moment-to-moment timescales.

    P1 (groove_response): Instantaneous motor entrainment level from
    short-timescale onset tracking (25ms, 50ms, 100ms). The
    population-level groove response -- shared motor engagement.
    Spiech 2022: pupil drift rate indexes groove (F(1,29)=10.515).
    Sarasso 2019: consonance enhances motor inhibition (eta^2=0.685).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e_outputs: ``(E0, E1, E2)`` from extraction layer.
        m_outputs: ``(M0, M1, M2)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    # -- H3 features --
    coherence_25ms = h3_features[_COHERENCE_VAL_25MS]      # (B, T)
    coherence_100ms = h3_features[_COHERENCE_VAL_100MS]    # (B, T)
    coherence_mean = h3_features[_COHERENCE_MEAN_50MS]     # (B, T)
    onset_25ms = h3_features[_ONSET_VAL_25MS]              # (B, T)
    onset_100ms = h3_features[_ONSET_VAL_100MS]            # (B, T)
    onset_mean = h3_features[_ONSET_MEAN_50MS]             # (B, T)

    # -- P0: Coherence Level --
    # sigma(0.35 * coherence_25ms + 0.35 * coherence_mean_50ms
    #       + 0.30 * coherence_100ms)
    # Uses shortest H3 horizons (25ms-100ms) to ground cognitive present
    # Leeuwis 2021: ISC content-driven at frontocentral electrodes
    # Hasson 2004: ISC reliable at moment-to-moment timescales
    p0 = torch.sigmoid(
        0.35 * coherence_25ms
        + 0.35 * coherence_mean
        + 0.30 * coherence_100ms
    )

    # -- P1: Groove Response --
    # sigma(0.35 * onset_25ms + 0.35 * onset_mean_50ms
    #       + 0.30 * onset_100ms)
    # Short-timescale onset tracking for beat-by-beat rhythmic engagement
    # Spiech 2022: pupil drift rate indexes groove perception
    # Sarasso 2019: consonance enhances motor inhibition engagement
    p1 = torch.sigmoid(
        0.35 * onset_25ms
        + 0.35 * onset_mean
        + 0.30 * onset_100ms
    )

    return (p0, p1)
