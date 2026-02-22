"""STANM E-Layer -- Extraction (3D).

Spectrotemporal attention extraction from H3 multi-scale features:
  E0: temporal_attention    (temporal stream attention strength)
  E1: spectral_attention    (spectral stream attention strength)
  E2: network_topology      (attention network integration state)

H3 demands consumed:
  spectral_flux:    (10,16,14,2) temporal periodicity 1s
  spectral_change:  (21,8,8,0)  tempo velocity 500ms
  tonalness:        (14,3,0,2)  tonalness value 100ms
  tonalness:        (14,16,1,2) tonalness mean 1s
  energy_change:    (22,8,2,0)  energy variability 500ms
  x_l0l5:           (25,3,20,2) coupling entropy 100ms
  spectral_flux:    (10,0,0,2)  flux instant
  spectral_flux:    (10,3,1,2)  flux mean 100ms
  spectral_change:  (21,1,8,0)  spectral velocity 50ms
  spectral_flux:    (10,4,14,2) flux periodicity 125ms
  loudness:         (8,3,0,2)   loudness value 100ms
  loudness:         (8,3,20,2)  loudness entropy 100ms

E-layer derives raw spectrotemporal attention from temporal periodicity,
spectral clarity, and network coupling features at multiple timescales.

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/stanm/
Fritz 2007: STRF reshaping during active attention tasks.
Bidet-Caulet 2007: lateralized spectrotemporal attention in MEG.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_FLUX_H16_PERIOD = (10, 16, 14, 2)       # temporal periodicity 1s
_SPEC_CHANGE_H8_VEL = (21, 8, 8, 0)      # tempo velocity 500ms
_TONAL_H3_VAL = (14, 3, 0, 2)            # tonalness value 100ms
_TONAL_H16_MEAN = (14, 16, 1, 2)         # tonalness mean 1s
_ENERGY_H8_STD = (22, 8, 2, 0)           # energy variability 500ms
_COUPLING_H3_ENT = (25, 3, 20, 2)        # coupling entropy 100ms
_FLUX_H0_VAL = (10, 0, 0, 2)             # flux instant
_FLUX_H3_MEAN = (10, 3, 1, 2)            # flux mean 100ms
_SPEC_CHANGE_H1_VEL = (21, 1, 8, 0)      # spectral velocity 50ms
_FLUX_H4_PERIOD = (10, 4, 14, 2)         # flux periodicity 125ms
_LOUD_H3_VAL = (8, 3, 0, 2)             # loudness value 100ms
_LOUD_H3_ENT = (8, 3, 20, 2)            # loudness entropy 100ms


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: spectrotemporal attention extraction.

    E0 captures temporal attention from flux periodicity (beat-scale temporal
    regularity) and tempo velocity (temporal change rate). Fritz 2007: STRFs
    dynamically enhance temporal modulation features during attention.

    E1 captures spectral attention from tonalness (spectral clarity) and
    loudness (spectral envelope). Bidet-Caulet 2007: MEG gamma enhancement
    for attended spectral features.

    E2 captures network topology from energy variability and coupling
    entropy, reflecting the integration state across distributed attention
    networks. Mesgarani 2012: STG networks selectively represent attended
    spectrotemporal features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``
    """
    # -- H3 features --
    temporal_period_1s = h3_features[_FLUX_H16_PERIOD]
    tempo_velocity_500ms = h3_features[_SPEC_CHANGE_H8_VEL]
    tonalness_mean_1s = h3_features[_TONAL_H16_MEAN]
    tonalness_value_100ms = h3_features[_TONAL_H3_VAL]
    energy_var_500ms = h3_features[_ENERGY_H8_STD]
    coupling_entropy_100ms = h3_features[_COUPLING_H3_ENT]
    flux_instant = h3_features[_FLUX_H0_VAL]
    flux_value_100ms = h3_features[_FLUX_H3_MEAN]
    spectral_velocity_50ms = h3_features[_SPEC_CHANGE_H1_VEL]
    flux_period_125ms = h3_features[_FLUX_H4_PERIOD]
    loudness_value_100ms = h3_features[_LOUD_H3_VAL]
    loudness_entropy_100ms = h3_features[_LOUD_H3_ENT]

    # -- E0: Temporal Attention --
    # Strength of attention to the temporal stream. Temporal periodicity at
    # 1s captures beat-scale regularity; tempo velocity at 500ms captures
    # rate of temporal change; flux value/instant provide fast onset cues.
    # Fritz 2007: STRFs enhance temporal modulation during active listening.
    e0 = torch.sigmoid(
        0.35 * temporal_period_1s
        + 0.30 * tempo_velocity_500ms
        + 0.20 * flux_value_100ms
        + 0.15 * flux_instant
    )

    # -- E1: Spectral Attention --
    # Strength of attention to the spectral stream. Tonalness mean (1s)
    # captures sustained spectral clarity; tonalness value (100ms) captures
    # instantaneous pitch salience; loudness envelope provides spectral
    # energy context; flux periodicity adds rhythmic spectral modulation.
    # Bidet-Caulet 2007: MEG reveals sustained gamma for attended spectra.
    e1 = torch.sigmoid(
        0.35 * tonalness_mean_1s
        + 0.30 * tonalness_value_100ms
        + 0.20 * loudness_value_100ms
        + 0.15 * flux_period_125ms
    )

    # -- E2: Network Topology --
    # Integration state of the attention network. Energy variability
    # captures dynamic range (network engagement); coupling entropy
    # captures cross-band interaction complexity; loudness entropy adds
    # spectral diversity; spectral velocity provides fast change cues.
    # Mesgarani 2012: STG networks show distributed selective representations.
    e2 = torch.sigmoid(
        0.35 * energy_var_500ms
        + 0.30 * coupling_entropy_100ms
        + 0.20 * loudness_entropy_100ms
        + 0.15 * spectral_velocity_50ms
    )

    return e0, e1, e2
