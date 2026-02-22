"""PUPF F-Layer -- Forecast (2D).

Forward predictions for pleasure-uncertainty:
  F0: next_event_prob     — Probability estimate for next musical event [0, 1]
  F1: pleasure_forecast   — Predicted pleasure for upcoming events [0, 1]

F0 forecasts the probability of the next musical event. Uses entropy
trajectory (distribution_entropy trend at 525ms and 800ms) combined with
surprise trajectory (spectral_flux trend at 525ms) to estimate how likely
the next event is. Low entropy trend + stable surprise = high probability
estimate. This feeds back into the Goldilocks function: if the next event
is highly predicted (high F0), any violation will produce large surprise.

F1 projects the expected pleasure for upcoming events based on current
Goldilocks state. Uses pleasure trajectory (sensory_pleasantness trend at
800ms) combined with current pleasure state (G0) and affective outcome (P1).
If the current H x S interaction is in the Goldilocks zone, pleasure
forecast is high. Rising pleasantness trend amplifies the forecast.

H3 demands consumed (4 tuples -- F-layer specific):
  (22, 12, 18, 0)  distribution_entropy trend H12 L0   -- entropy trajectory
  (21, 12, 18, 0)  spectral_flux trend H12 L0          -- surprise trajectory
  (22, 15, 18, 0)  distribution_entropy trend H15 L0   -- longer entropy trend
  (4, 15, 18, 0)   sensory_pleasantness trend H15 L0   -- hedonic trajectory

R3 features: none beyond what upstream layers provide

Cheung et al. 2019: predictive coding in auditory cortex (fMRI, N=39).
Koelsch 2014: anticipatory pleasure from musical expectations.

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/pupf/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ENTROPY_TREND_H12_F = (22, 12, 18, 0)    # distribution_entropy trend H12 L0
_FLUX_TREND_H12 = (21, 12, 18, 0)         # spectral_flux trend H12 L0
_ENTROPY_TREND_H15 = (22, 15, 18, 0)      # distribution_entropy trend H15 L0
_PLEAS_TREND_H15 = (4, 15, 18, 0)         # sensory_pleasantness trend H15 L0


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: forward predictions for pleasure-uncertainty.

    F0 (next_event_prob) forecasts the probability of the next event.
    Entropy trajectory at 525ms and 800ms combined with surprise trajectory
    at 525ms estimate how predictable the upcoming musical material is.
    Low entropy trend = increasing predictability = higher event probability.
    Feeds back into Goldilocks: high F0 amplifies surprise if violated.

    F1 (pleasure_forecast) projects expected pleasure. Current Goldilocks
    pleasure (G0), affective outcome (P1), and hedonic trajectory
    (pleasantness trend at 800ms) project future pleasure state. If H x S
    is in the Goldilocks zone and pleasure is rising, forecast is high.

    Cheung et al. 2019: predictive coding in auditory cortex -- anticipation
    of surprise modulates amygdala (fMRI, N=39).
    Koelsch 2014: anticipatory pleasure from musical expectations.
    Salimpoor et al. 2011: anticipatory dopamine in caudate nucleus.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(U0, U1, U2, G0, G1)`` from temporal integration layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)``
    """
    _e0, e1 = e
    u0, _u1, u2, g0, g1 = m
    p0, p1, _p2 = p

    # -- H3 features --
    entropy_trend_12 = h3_features[_ENTROPY_TREND_H12_F]  # (B, T)
    flux_trend_12 = h3_features[_FLUX_TREND_H12]          # (B, T)
    entropy_trend_15 = h3_features[_ENTROPY_TREND_H15]    # (B, T)
    pleas_trend_15 = h3_features[_PLEAS_TREND_H15]        # (B, T)

    # -- Derived signals --
    # Multi-scale entropy trajectory: average of 525ms and 800ms
    entropy_trajectory = 0.50 * entropy_trend_12 + 0.50 * entropy_trend_15

    # Predictability: inverse entropy trajectory (falling entropy = rising
    # predictability = higher event probability estimate)
    predictability = 1.0 - entropy_trajectory.abs()

    # -- F0: Next Event Probability --
    # Forecasts how probable the next event is. Predictability (inverse
    # entropy trajectory) + surprise trajectory (flux trend) + current
    # uncertainty (E1 inverted).
    # Cheung 2019: predictive coding in auditory cortex anticipates events.
    f0 = torch.sigmoid(
        0.35 * predictability * (1.0 - e1).clamp(min=0.1)
        + 0.35 * (1.0 - flux_trend_12.abs())
        + 0.30 * u0 * u2.clamp(min=0.1)
    )

    # -- F1: Pleasure Forecast --
    # Projects expected pleasure for upcoming events. Goldilocks pleasure
    # (G0) + affective outcome (P1) + hedonic trajectory (pleasantness
    # trend at 800ms). Rising pleasantness amplifies the forecast.
    # Salimpoor et al. 2011: anticipatory dopamine in caudate tracks this.
    f1 = torch.sigmoid(
        0.35 * g0 * p1.clamp(min=0.1)
        + 0.35 * pleas_trend_15 * g1.clamp(min=0.1)
        + 0.30 * p0 * predictability.clamp(min=0.1)
    )

    return f0, f1
