"""DGTP E-Layer -- Extraction (3D).

Domain-general temporal processing signals from H3 features:
  E0: music_timing      (beat-based temporal processing for music)
  E1: speech_timing     (envelope-based temporal processing for speech)
  E2: shared_mechanism  (geometric mean proxy for shared variance)

Music timing relies on beat periodicity cues (spectral flux peaks at 1s and
100ms scales, coupling peaks). Speech timing relies on onset velocity and
trajectory at 600ms scale plus coupling stability.

H3 demands consumed:
  spectral_flux:   (10,3,0,2)   value at 100ms integration
  spectral_flux:   (10,3,17,2)  peaks at 100ms integration
  spectral_flux:   (10,16,17,2) peaks at 1s integration
  onset_strength:  (11,13,8,0)  velocity at 600ms memory
  onset_strength:  (11,13,11,0) trend at 600ms memory
  x_l0l5:          (25,3,17,2)  peaks at 100ms integration
  x_l0l5:          (25,16,19,0) stability at 1s memory

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/dgtp/
Grahn 2012: SMA/putamen recruitment for beat processing.
Tierney 2017: shared timing mechanism for music and speech.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_FLUX_H3_VAL = (10, 3, 0, 2)          # spectral_flux value 100ms integration
_FLUX_H3_PEAKS = (10, 3, 17, 2)       # spectral_flux peaks 100ms integration
_FLUX_H16_PEAKS = (10, 16, 17, 2)     # spectral_flux peaks 1s integration
_ONSET_H13_VEL = (11, 13, 8, 0)       # onset_strength velocity 600ms memory
_ONSET_H13_TREND = (11, 13, 11, 0)    # onset_strength trend 600ms memory
_COUPLING_H3_PEAKS = (25, 3, 17, 2)   # x_l0l5 peaks 100ms integration
_COUPLING_H16_STAB = (25, 16, 19, 0)  # x_l0l5 stability 1s memory


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: domain-general temporal extraction signals.

    E0 (music_timing) captures beat-based temporal processing. Beat
    periodicity at 1s scale provides the primary metric structure, flux
    peaks at 100ms give event-level onset salience, and coupling peaks
    at 100ms provide fast sensorimotor cues.

    E1 (speech_timing) captures envelope-based temporal processing for
    speech. Onset velocity at 600ms reflects syllabic rate dynamics,
    onset trend captures speech trajectory, and coupling stability at
    1s provides sustained timing precision.

    E2 (shared_mechanism) captures the geometric mean proxy of E0 and
    E1, representing the degree of overlap between music and speech
    timing mechanisms (Patel 2011 OPERA hypothesis).

    Grahn 2012: beat periodicity drives SMA/putamen activation.
    Tierney 2017: onset velocity predicts speech-in-noise performance.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``
    """
    # -- H3 features --
    flux_peaks_1s = h3_features[_FLUX_H16_PEAKS]           # (B, T)
    coupling_peaks_100ms = h3_features[_COUPLING_H3_PEAKS]  # (B, T)
    flux_value_100ms = h3_features[_FLUX_H3_VAL]            # (B, T)
    onset_velocity_600ms = h3_features[_ONSET_H13_VEL]      # (B, T)
    onset_trend_600ms = h3_features[_ONSET_H13_TREND]        # (B, T)
    coupling_stability_1s = h3_features[_COUPLING_H16_STAB]  # (B, T)

    # -- E0: Music Timing --
    # Beat-based temporal processing from flux peaks (beat periodicity)
    # and coupling peaks (fast metric cue). Grahn 2012: SMA/putamen
    # recruit preferentially for beat-based vs duration-based timing.
    e0 = torch.sigmoid(
        0.40 * flux_peaks_1s
        + 0.30 * coupling_peaks_100ms
        + 0.30 * flux_value_100ms
    )

    # -- E1: Speech Timing --
    # Envelope-based temporal processing from onset velocity and trend
    # at 600ms (syllabic rate) plus coupling stability (sustained timing).
    # Tierney 2017: beat sync predicts speech timing accuracy.
    e1 = torch.sigmoid(
        0.35 * onset_velocity_600ms
        + 0.30 * onset_trend_600ms
        + 0.35 * coupling_stability_1s
    )

    # -- E2: Shared Mechanism --
    # Geometric mean proxy: sqrt(E0 * E1 + eps) captures shared variance
    # between music and speech timing. Patel 2011: OPERA overlap.
    e2 = torch.sigmoid(torch.sqrt(e0 * e1 + 1e-8))

    return e0, e1, e2
