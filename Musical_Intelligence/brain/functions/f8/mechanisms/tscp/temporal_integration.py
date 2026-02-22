"""TSCP M-Layer -- Temporal Integration (1D).

Timbre-Specific Cortical Plasticity mathematical model output:
  enhancement_function (idx 3) -- Enhancement selectivity function [0, 1]

The enhancement function is the multiplicative product of trained timbre
response (f01) and timbre specificity (f02). This ensures that enhancement
is high only when BOTH conditions are met: (a) the stimulus strongly
activates the trained instrument template, AND (b) the response is selective
for that specific timbre. This mirrors the double dissociation found by
Pantev et al. 2001 -- violinists show enhanced responses to violin tones
but not trumpet tones, and vice versa. The multiplicative gating prevents
general auditory enhancement from registering as timbre-specific plasticity.

Computed as: E(t) = f01 * f02

H3 demands consumed: 0 tuples (operates entirely on E-layer outputs).

Dependencies:
  E-layer f01 (trained_timbre_response)
  E-layer f02 (timbre_specificity)

Pantev et al. 2001: trained instrument >> other instrument >> pure tone
hierarchy (MEG, N=16, double dissociation F(1,15)=28.55).

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/tscp/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    ednr: Tensor,
) -> Tuple[Tensor]:
    """Compute M-layer: enhancement selectivity function.

    enhancement_function = f01 * f02 -- multiplicative gating ensures high
    output only when both trained timbre response AND timbre specificity are
    present. This implements the double dissociation from Pantev et al. 2001:
    violinists show enhanced N1m for violin but not trumpet tones.

    The product naturally stays in [0, 1] since both f01 and f02 are sigmoid
    outputs in [0, 1]. No additional normalization is needed.

    Pantev et al. 2001: trained instrument >> other >> pure tone hierarchy.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e_outputs: ``(f01, f02, f03)`` from extraction layer.
        ednr: ``(B, T, 10)`` from upstream EDNR relay.

    Returns:
        ``(enhancement_function,)`` -- ``(B, T)``
    """
    f01, f02, _f03 = e_outputs

    # -- Enhancement function: multiplicative gate --
    # E(t) = f01 * f02
    # High only when both trained response AND specificity are present.
    # Pantev 2001: double dissociation F(1,15)=28.55, p=.00008
    enhancement_function = f01 * f02  # (B, T), already in [0, 1]

    return (enhancement_function,)
