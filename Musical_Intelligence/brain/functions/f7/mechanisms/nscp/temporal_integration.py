"""NSCP M-Layer -- Temporal Integration (3D).

Temporal integration of ISC signals for commercial prediction:
  M0: isc_magnitude       -- Raw ISC magnitude estimate [0, 1]
  M1: sync_consistency    -- Synchrony consistency over time [0, 1]
  M2: popularity_estimate -- Normalized popularity prediction [0, 1]

ISC magnitude (M0) is a direct passthrough of f22 (neural synchrony)
into the mathematical layer. Preserves the raw ISC estimate for
downstream consumers. Leeuwis 2021: ISC computed across 64 EEG channels
with strongest effects at frontocentral and temporal electrodes.

Sync consistency (M1) measures temporal stability of ISC. Combines
coherence periodicity with binding periodicity at 1s. Leeuwis 2021:
early ISC (R^2=0.404) vs late ISC (R^2=0.393) both predict streams,
indicating temporal stability of the ISC signal.

Popularity estimate (M2) is a direct passthrough of f23 (commercial
prediction). Provides continuous [0,1] popularity proxy mapping
neural synchrony to commercial success. Berns 2010: NAcc activity
predicted future song sales.

H3 demands consumed (3):
  (25, 16, 14, 2) coherence periodicity 1s L2     -- sync consistency
  (33, 16, 14, 2) binding periodicity 1s L2        -- sync consistency
  (33, 8, 14, 2)  binding periodicity 500ms L2     -- temporal integration

R3 inputs: x_l0l5[25:33], x_l4l5[33:41]

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/nscp/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_COHERENCE_PERIOD_1S = (25, 16, 14, 2)   # x_l0l5 periodicity H16 L2
_BINDING_PERIOD_1S = (33, 16, 14, 2)     # x_l4l5 periodicity H16 L2
_BINDING_PERIOD_500MS = (33, 8, 14, 2)   # x_l4l5 periodicity H8 L2


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute M-layer: 3D temporal integration of ISC signals.

    M0 (isc_magnitude): Direct passthrough of f22 (neural synchrony).
    Preserves the raw ISC estimate. Identity mapping from E to M
    ensures no information loss.
    Leeuwis 2021: ISC strongest at frontocentral and temporal electrodes.

    M1 (sync_consistency): Temporal stability of ISC from coherence
    periodicity + binding periodicity at 1s. High consistency means
    the ISC signal is sustained rather than transient.
    Leeuwis 2021: ISC stability (R^2 drop of only 0.011).

    M2 (popularity_estimate): Direct passthrough of f23 (commercial
    prediction). Normalized popularity proxy for integration with
    other C3 functions.
    Berns 2010: neural activity in NAcc predicted future song sales.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e_outputs: ``(E0, E1, E2)`` from extraction layer.
        upstream_outputs: ``{"ASAP": (B, T, 11), "DDSMI": (B, T, 11)}``.

    Returns:
        ``(M0, M1, M2)`` each ``(B, T)``.
    """
    e0, e1, e2 = e_outputs

    # -- H3 features --
    coherence_period = h3_features[_COHERENCE_PERIOD_1S]      # (B, T)
    binding_period = h3_features[_BINDING_PERIOD_1S]           # (B, T)
    _binding_500ms = h3_features[_BINDING_PERIOD_500MS]        # (B, T)

    # -- M0: ISC Magnitude --
    # Direct passthrough of f22 neural synchrony
    # Leeuwis 2021: ISC across 64 EEG channels
    m0 = e0

    # -- M1: Sync Consistency --
    # sigma(0.5 * coherence_period_1s + 0.5 * binding_period_1s)
    # Leeuwis 2021: early ISC R^2=0.404 vs late R^2=0.393 (stable)
    m1 = torch.sigmoid(
        0.50 * coherence_period
        + 0.50 * binding_period
    )

    # -- M2: Popularity Estimate --
    # Direct passthrough of f23 commercial prediction
    # Berns 2010: NAcc activity predicts future sales
    m2 = e1

    return (m0, m1, m2)
