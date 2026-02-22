"""SDL E-Layer -- Extraction (3D).

Salience-dependent lateralization extraction from H3 multi-scale features:
  E0: dynamic_lateral      (dynamic lateralization index, TANH [-1, 1])
  E1: local_clustering     (local network clustering coefficient, sigmoid [0, 1])
  E2: hemispheric_osc      (hemispheric oscillatory state, sigmoid [0, 1])

H3 demands consumed:
  spectral_centroid: (15,3,0,2)   centroid value 100ms -- spectral focus
  spectral_flux:     (10,3,0,2)   flux value 100ms -- temporal focus
  x_l0l5:            (25,17,8,0)  coupling velocity 1250ms -- hemispheric shift
  x_l4l5:            (37,3,20,2)  cross-stream entropy 100ms -- bilateral load
  loudness:          (8,16,20,2)  loudness entropy 1s -- salience demand
  spectral_centroid: (15,3,2,2)   centroid std 100ms -- spectral spread
  x_l4l5:            (37,16,17,2) cross-stream peaks 1s -- oscillatory marker
  spectral_flux:     (10,4,17,2)  flux peaks 125ms -- event detection

CRITICAL: E0 uses torch.tanh for lateralization ([-1, 1]).
  Positive = spectral-dominant (right hemisphere bias)
  Negative = temporal-dominant (left hemisphere bias)

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/sdl/
Poeppel 2003: asymmetric sampling in time.
Zatorre 2002: hemispheric specialization for spectral vs temporal.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_CENTROID_H3_VAL = (15, 3, 0, 2)       # centroid value 100ms -- spectral focus
_FLUX_H3_VAL = (10, 3, 0, 2)           # flux value 100ms -- temporal focus
_COUPLING_H17_VEL = (25, 17, 8, 0)     # coupling velocity 1250ms -- hemispheric shift
_XSTREAM_H3_ENT = (37, 3, 20, 2)       # cross-stream entropy 100ms -- bilateral load
_LOUD_H16_ENT = (8, 16, 20, 2)         # loudness entropy 1s -- salience demand
_CENTROID_H3_STD = (15, 3, 2, 2)       # centroid std 100ms -- spectral spread
_XSTREAM_H16_PEAKS = (37, 16, 17, 2)   # cross-stream peaks 1s -- oscillatory marker
_FLUX_H4_PEAKS = (10, 4, 17, 2)        # flux peaks 125ms -- event detection


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: salience-dependent lateralization extraction.

    E0 captures dynamic lateralization as the balance between spectral focus
    (centroid, right-biased) and temporal focus (flux, left-biased), modulated
    by cross-band coupling velocity (hemispheric shift dynamics) and
    cross-stream entropy (bilateral processing load). Uses tanh to produce
    a lateralization index in [-1, 1].

    E1 captures local network clustering from loudness entropy (salience
    demand), cross-stream entropy (bilateral load), and centroid spread
    (spectral variability within local ensembles).

    E2 captures hemispheric oscillatory state from coupling velocity
    (hemispheric shift), cross-stream peaks (oscillatory markers), and
    flux peaks (event detection at theta timescale).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``
        E0 in [-1, 1] (tanh); E1, E2 in [0, 1] (sigmoid).
    """
    # -- H3 features --
    centroid_100ms = h3_features[_CENTROID_H3_VAL]
    flux_100ms = h3_features[_FLUX_H3_VAL]
    coupling_velocity_1250ms = h3_features[_COUPLING_H17_VEL]
    cross_stream_entropy_100ms = h3_features[_XSTREAM_H3_ENT]
    loudness_entropy_1s = h3_features[_LOUD_H16_ENT]
    centroid_std_100ms = h3_features[_CENTROID_H3_STD]
    cross_stream_peaks_1s = h3_features[_XSTREAM_H16_PEAKS]
    flux_peaks_125ms = h3_features[_FLUX_H4_PEAKS]

    # -- E0: Dynamic Lateral --
    # Lateralization index: spectral focus (centroid) vs temporal focus (flux).
    # Positive centroid -> right hemisphere (spectral detail); negative flux
    # -> left hemisphere (temporal detail). Coupling velocity adds hemispheric
    # shift dynamics; cross-stream entropy adds bilateral load.
    # Poeppel 2003: asymmetric temporal windows across hemispheres.
    e0 = torch.tanh(
        0.35 * centroid_100ms
        - 0.30 * flux_100ms
        + 0.20 * coupling_velocity_1250ms
        + 0.15 * cross_stream_entropy_100ms
    )

    # -- E1: Local Clustering --
    # Local network clustering coefficient: loudness entropy captures salience
    # demand driving network engagement; cross-stream entropy captures
    # bilateral processing load; centroid std captures spectral spread within
    # local ensembles. High clustering = tightly coupled lateralized networks.
    # Zatorre 2002: hemispheric specialization review.
    e1 = torch.sigmoid(
        0.35 * loudness_entropy_1s
        + 0.35 * cross_stream_entropy_100ms
        + 0.30 * centroid_std_100ms
    )

    # -- E2: Hemispheric Oscillatory State --
    # Oscillatory dynamics of hemispheric processing: coupling velocity tracks
    # shifts between hemispheres; cross-stream peaks mark oscillatory events;
    # flux peaks detect temporal events at theta timescale.
    # Poeppel 2003: gamma (left) vs theta (right) oscillatory asymmetry.
    e2 = torch.sigmoid(
        0.35 * coupling_velocity_1250ms
        + 0.30 * cross_stream_peaks_1s
        + 0.35 * flux_peaks_125ms
    )

    return e0, e1, e2
