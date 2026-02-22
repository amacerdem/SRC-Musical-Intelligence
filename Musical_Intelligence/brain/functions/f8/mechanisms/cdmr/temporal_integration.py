"""CDMR M-Layer -- Temporal Integration (2D).

Context-Dependent Mismatch Response temporal integration outputs:
  melodic_expectation  -- Pattern expectation state [0, 1]
  deviance_history     -- Recent deviance memory [0, 1]

melodic_expectation maintains a running estimate of the melodic context
richness that modulates mismatch sensitivity. In predictive coding terms,
this represents the precision of melodic predictions -- richer contexts
produce more precise expectations and therefore stronger mismatch responses
to violations. Temporal smoothing of context modulation (f02) over a 2.5s
melodic context window. Uses spectral trend at 125ms (theta timescale)
aligned with the MMN latency window.

deviance_history maintains a running estimate of recent deviance levels via
exponential moving average of mismatch amplitude (f01) with tau=0.4s decay.
This memory trace adapts mismatch sensitivity -- if recent deviance is high,
the threshold for strong mismatch response increases (habituation). If
recent deviance is low, sensitivity increases (oddball enhancement). Uses
mean deviance at 1s for baseline calibration.

H3 demands consumed (4 tuples):
  (10, 16, 1, 2)  spectral_flux mean H16 L2       -- mean deviance over 1s
  (23, 4, 2, 2)   pitch_change std H4 L2          -- pitch variability 125ms
  (21, 3, 0, 2)   spectral_change value H3 L2     -- spectral deviance 100ms
  (21, 4, 18, 0)  spectral_change trend H4 L0     -- spectral trend 125ms

Dependencies:
  E-layer f01 (mismatch_amplitude) -- input to deviance history EMA
  E-layer f02 (context_modulation) -- input to melodic expectation EMA
  R3 [21] spectral_change, R3 [23] pitch_change
  EDNR relay (upstream)

Tervaniemi 2022: genre-specific MMN modulation by expertise.
Koelsch: ERAN (150-250ms) reflects long-term music-syntactic regularities.
Fong 2020: MMN as prediction error signal under predictive coding framework.

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/cdmr/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_FLUX_MEAN_H16 = (10, 16, 1, 2)       # mean deviance over 1s
_PITCH_STD_H4 = (23, 4, 2, 2)         # pitch variability at 125ms
_SPECTRAL_VAL_H3 = (21, 3, 0, 2)      # spectral deviance at 100ms
_SPECTRAL_TREND_H4 = (21, 4, 18, 0)   # spectral trend at 125ms


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    ednr: Tensor,
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: melodic expectation and deviance history.

    melodic_expectation (idx 4) temporally smooths context modulation (f02)
    over a 2.5s context window. Uses pitch variability at 125ms and
    spectral trend at 125ms for context quality estimation.
    Tervaniemi 2022: genre-specific MMN modulation by expertise.
    Koelsch: ERAN (150-250ms) reflects long-term music-syntactic regularities.

    deviance_history (idx 5) exponentially averages mismatch amplitude (f01)
    with tau=0.4s decay. Uses mean deviance at 1s for baseline calibration
    and spectral deviance at 100ms for cross-feature validation.
    Fong 2020: MMN as prediction error under predictive coding framework.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e_outputs: ``(f01, f02, f03, f04)`` from extraction layer.
        ednr: ``(B, T, 10)`` upstream EDNR relay output.

    Returns:
        ``(melodic_expectation, deviance_history)`` each ``(B, T)``
    """
    f01, f02, _f03, _f04 = e_outputs

    # -- H3 features --
    mean_deviance_1s = h3_features[_FLUX_MEAN_H16]        # (B, T)
    pitch_variability = h3_features[_PITCH_STD_H4]         # (B, T)
    spectral_deviance = h3_features[_SPECTRAL_VAL_H3]      # (B, T)
    spectral_trend = h3_features[_SPECTRAL_TREND_H4]       # (B, T)

    # -- melodic_expectation --
    # Temporal smoothing of context modulation (f02) over RTI_WINDOW=2.5s.
    # Pitch variability at 125ms and spectral trend at 125ms provide
    # context quality for the expectation signal.
    # Tervaniemi 2022: genre-specific MMN modulation by expertise.
    # Koelsch: ERAN (150-250ms) reflects long-term syntactic regularities.
    melodic_expectation = torch.sigmoid(
        0.35 * f02
        + 0.30 * pitch_variability
        + 0.25 * spectral_trend
    )

    # -- deviance_history --
    # EMA of mismatch amplitude with tau=0.4s decay. Mean deviance at 1s
    # provides baseline calibration; spectral deviance at 100ms provides
    # cross-feature validation of the deviance memory trace.
    # Fong 2020: MMN as prediction error — deviance history forms the
    # prediction baseline.
    deviance_history = torch.sigmoid(
        0.35 * f01
        + 0.30 * mean_deviance_1s
        + 0.25 * spectral_deviance
    )

    return melodic_expectation, deviance_history
