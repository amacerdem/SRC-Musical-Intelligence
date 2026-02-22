"""BARM E-Layer -- Extraction (3D).

Brainstem response modulation signals from H3 periodicity features:
  E0: regularization_tendency  (tendency to impose regular temporal structure)
  E1: beat_alignment           (alignment of neural response to beat structure)
  E2: sync_benefit             (synchronization benefit from sensorimotor coupling)

Brainstem responses are enhanced when stimuli have regular temporal structure
(Skoe & Kraus 2010). E0 captures regularity detection, E1 captures beat-locked
neural firing, and E2 captures the benefit of active sensorimotor engagement.

H3 demands consumed:
  spectral_change:  (21,8,14,0)  periodicity at 500ms memory
  spectral_flux:    (10,16,14,2) periodicity at 1s integration
  onset_strength:   (11,16,14,2) periodicity at 1s integration
  x_l0l5:           (25,16,14,2) periodicity at 1s integration
  energy_change:    (22,8,8,0)   velocity at 500ms memory
  x_l0l5:           (25,8,0,2)   value at 500ms integration

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/barm/
Skoe & Kraus 2010: ABR enhancement at beat-aligned time points.
Tierney & Kraus 2013: beat synchronization predicts brainstem consistency.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_SPEC_CHANGE_H8_PERIOD = (21, 8, 14, 0)     # spectral_change periodicity 500ms memory
_FLUX_H16_PERIOD = (10, 16, 14, 2)          # spectral_flux periodicity 1s integration
_ONSET_H16_PERIOD = (11, 16, 14, 2)         # onset_strength periodicity 1s integration
_COUPLING_H16_PERIOD = (25, 16, 14, 2)      # x_l0l5 periodicity 1s integration
_ENERGY_H8_VEL = (22, 8, 8, 0)             # energy_change velocity 500ms memory
_COUPLING_H8_VAL = (25, 8, 0, 2)           # x_l0l5 value 500ms integration


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: brainstem response modulation extraction signals.

    E0 (regularization_tendency) reflects the tendency to impose regular
    temporal structure. Low spectral change periodicity (high irregularity)
    is inverted to capture the brain's drive to regularize. Beat periodicity
    and coupling periodicity provide rhythmic anchoring context.

    E1 (beat_alignment) captures how well neural responses align with beat
    structure. Beat periodicity (onset regularity) is the dominant cue,
    supplemented by onset periodicity and coupling periodicity.

    E2 (sync_benefit) captures the synchronization advantage from active
    sensorimotor coupling. Coupling periodicity + coupling value + energy
    dynamics indicate engaged motor-auditory interaction.

    Skoe & Kraus 2010: ABR latency at beat-aligned points shows d=1.2
    enhancement in musicians.
    Tierney & Kraus 2013: Beat synchronization ability (r=0.65) predicts
    brainstem response consistency.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``
    """
    # -- H3 features --
    spec_change_period = h3_features[_SPEC_CHANGE_H8_PERIOD]   # (B, T)
    beat_period = h3_features[_FLUX_H16_PERIOD]                 # (B, T)
    onset_period = h3_features[_ONSET_H16_PERIOD]               # (B, T)
    coupling_period = h3_features[_COUPLING_H16_PERIOD]         # (B, T)
    energy_vel = h3_features[_ENERGY_H8_VEL]                    # (B, T)
    coupling_val = h3_features[_COUPLING_H8_VAL]                # (B, T)

    # -- E0: Regularization Tendency --
    # Brainstem imposes regularity even on irregular stimuli (Skoe 2010).
    # Low spectral change periodicity = irregular signal -> brain regularizes.
    # Beat and coupling periodicity provide rhythmic scaffolding.
    e0 = torch.sigmoid(
        0.35 * (1.0 - spec_change_period)
        + 0.35 * beat_period
        + 0.30 * coupling_period
    )

    # -- E1: Beat Alignment --
    # Neural firing aligns to beat structure. Onset periodicity reflects
    # event regularity; coupling periodicity reflects metric structure.
    # Tierney 2013: stronger beat synchronizers have more consistent ABR.
    e1 = torch.sigmoid(
        0.40 * beat_period
        + 0.30 * onset_period
        + 0.30 * coupling_period
    )

    # -- E2: Sync Benefit --
    # Active sensorimotor coupling enhances brainstem responses.
    # Coupling periodicity + instantaneous coupling value + energy dynamics.
    # Musacchia 2007: cross-domain transfer of musical training to ABR.
    e2 = torch.sigmoid(
        0.35 * coupling_period
        + 0.35 * coupling_val
        + 0.30 * energy_vel
    )

    return e0, e1, e2
