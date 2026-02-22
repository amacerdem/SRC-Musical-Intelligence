"""ESME M-Layer -- Temporal Integration (1D).

Unified MMN-expertise function:
  M0: mmn_expertise_function  -- Geometric mean of expertise and MMN [0, 1]

The M-layer computes a single unified expertise-MMN function that
integrates across all three deviance domains. Unlike mechanisms with
multiple M-layer dimensions, ESME's M-layer focuses on a single
integrated metric: the geometric mean of expertise enhancement (f04)
and the maximum domain-specific MMN response.

The geometric mean is used rather than arithmetic mean because it
captures the interaction: both expertise AND deviance must be present
for the function to be high. A musician with no deviant present
produces low output; a non-musician encountering a deviant also
produces low output.

Yu et al. 2015: MMN as comprehensive indicator of perception of
regularities -- the unified function integrates the domain-specific
gradient into a single expertise metric.

Doelling & Poeppel 2015: enhanced PLV across all tempi in musicians
reflects general expertise mechanism.

H3 demands consumed: 0 tuples (operates entirely on E-layer outputs).

Dependencies:
  E-layer f01 (pitch_mmn)
  E-layer f02 (rhythm_mmn)
  E-layer f03 (timbre_mmn)
  E-layer f04 (expertise_enhancement)

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/esme/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- Epsilon for sqrt stability ------------------------------------------------
_EPS = 1e-8


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    ednr: Tensor,
    tscp: Tensor,
    cdmr: Tensor,
) -> Tuple[Tensor]:
    """Compute M-layer: 1D unified MMN-expertise function.

    mmn_expertise_function: Geometric mean of expertise enhancement (f04)
    and the maximum domain-specific MMN (max of f01, f02, f03).

    mmn_expertise_function = sqrt(f04 * max(f01, f02, f03))

    The geometric mean captures the interaction: both expertise and
    deviance must be present for the function to be high. A musician
    with no deviant present produces low output; a non-musician
    encountering a deviant also produces low output.

    Yu et al. 2015: MMN as comprehensive indicator of regularities.
    Doelling & Poeppel 2015: enhanced PLV across tempi in musicians.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``
            from extraction layer.
        ednr: ``(B, T, 10)`` upstream EDNR output.
        tscp: ``(B, T, 10)`` upstream TSCP output.
        cdmr: ``(B, T, 11)`` upstream CDMR output.

    Returns:
        ``(mmn_expertise_function,)`` each ``(B, T)``.
    """
    f01, f02, f03, f04 = e_outputs

    # -- mmn_expertise_function ------------------------------------------------
    # Geometric mean: sqrt(f04 * max(f01, f02, f03))
    # Both terms are in [0, 1] (sigmoid outputs), so product is in [0, 1]
    # and sqrt maps [0, 1] -> [0, 1].
    max_mmn = torch.max(torch.max(f01, f02), f03)
    mmn_expertise_function = torch.sqrt(f04 * max_mmn + _EPS)

    return (mmn_expertise_function,)
