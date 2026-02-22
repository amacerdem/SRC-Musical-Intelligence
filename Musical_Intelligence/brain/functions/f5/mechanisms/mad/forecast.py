"""MAD F-Layer -- Forecast (2D).

Forward predictions for musical anhedonia disconnection:
  F0: recovery_potential   — Potential for anhedonia recovery [0, 1]
  F1: anhedonia_prob        — Probability of musical anhedonia [0, 1]

F0 forecasts recovery potential based on current connectivity state and
reward dynamics. Recovery from musical anhedonia has been observed in
some cases where white matter plasticity allows reconnection of STG-NAcc
pathways. Higher existing connectivity (D0) and some residual music reward
(D1) suggest better recovery prospects.

F1 forecasts the probability that the current listener exhibits musical
anhedonia. This is the primary diagnostic output routed to the F10 clinical
meta-layer. Integrates anhedonia (E0), dissociation (E1), impaired reward
(P0), sound specificity (A1), and BMRQ estimate (A0) into a single
probability estimate.

H3 demands consumed (1 tuple):
  (4, 11, 2, 0)  sensory_pleasantness std H11 L0  -- reward variability

Martinez-Molina et al. 2016: Prevalence ~3-5% with stable trait-like
pattern, some partial recovery with exposure (fMRI, N=45).
Mas-Herrero et al. 2018: Neural correlates predict BMRQ classification
accuracy >90% (fMRI, N=40).

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/mad/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_PLEAS_STD_H11 = (4, 11, 2, 0)       # sensory_pleasantness std H11 L0


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: recovery potential and anhedonia probability.

    F0 (recovery_potential) forecasts potential for recovery from musical
    anhedonia. Existing connectivity (D0) + residual music reward (D1) +
    reward variability suggest white matter plasticity potential. Higher
    values = better recovery prospect.

    F1 (anhedonia_prob) forecasts probability of musical anhedonia. Primary
    diagnostic output for F10 clinical meta-layer. Integrates all upstream
    signals into a single probability estimate.

    Martinez-Molina et al. 2016: ~3-5% prevalence, trait-like (N=45).
    Mas-Herrero et al. 2018: >90% classification accuracy (N=40).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(D0, D1, D2, A0, A1)`` from temporal integration layer.
        p: ``(P0, P1)`` from cognitive present layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)``
    """
    e0, e1 = e
    d0, d1, _d2, a0, a1 = m
    p0, p1 = p

    # -- H3 features --
    pleas_std = h3_features[_PLEAS_STD_H11]   # (B, T)

    # -- Derived signals --
    # Residual reward dynamics: some variability suggests partial function
    residual_reward = pleas_std.clamp(0.0, 1.0)

    # -- F0: Recovery Potential --
    # Potential for anhedonia recovery via white matter plasticity.
    # Higher existing connectivity (D0) + residual music reward (D1) +
    # reward variability suggest reconnection potential.
    # Preserved auditory (P1) confirms the substrate for recovery exists.
    f0 = torch.sigmoid(
        0.35 * d0 * residual_reward.clamp(min=0.1)
        + 0.35 * d1 * p1.clamp(min=0.1)
        + 0.30 * (1.0 - e0) * a0
    )

    # -- F1: Anhedonia Probability --
    # Diagnostic probability of musical anhedonia. Integrates:
    # - E0 (anhedonia strength), E1 (dissociation index)
    # - P0 (impaired reward), A1 (sound specificity)
    # - Inverted A0 (low BMRQ = high probability)
    # Mas-Herrero et al. 2018: >90% classification accuracy.
    f1 = torch.sigmoid(
        0.30 * e0 * a1
        + 0.30 * p0 * e1
        + 0.20 * (1.0 - a0.clamp(0.0, 1.0))
        + 0.20 * (1.0 - d0.clamp(0.0, 1.0)) * (1.0 - residual_reward)
    )

    return f0, f1
