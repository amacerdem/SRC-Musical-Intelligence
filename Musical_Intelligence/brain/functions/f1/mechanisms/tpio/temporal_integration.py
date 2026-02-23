"""TPIO M-Layer -- Temporal Integration (1D).

Single composite overlap index integrating perception and imagery
substrates over time:

  M0: overlap_index -- Sustained perception-imagery overlap strength

No additional H3/R3 dependencies -- uses E-layer outputs.

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/tpio/TPIO-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (none consumed directly -- uses E-layer) -----------------------


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor]:
    """M-layer: 1D temporal integration from E-layer.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.

    Returns:
        ``(M0,)`` single-element tuple, ``(B, T)``.
    """
    f01, f02, f03, f04 = e_outputs

    # M0: Overlap Index
    # Integrates overlap (dominant) with perception + imagery substrates.
    # Halpern 2004: overlap strength modulates imagery fidelity.
    m0 = torch.sigmoid(
        0.40 * f03
        + 0.25 * f01
        + 0.20 * f02
        + 0.15 * f04
    )

    return (m0,)
