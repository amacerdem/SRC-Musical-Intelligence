"""ASAP E-Layer -- Extraction (3D).

Action Simulation for Auditory Prediction extraction signals:
  f10: beat_prediction     -- Temporal "when" prediction via motor simulation [0, 1]
  f11: motor_simulation    -- Continuous action simulation strength [0, 1]
  f12: dorsal_stream       -- Parietal dorsal auditory-motor pathway activity [0, 1]

f10 captures temporal "when" prediction: the motor system predicts beat timing
rather than content, relying on beat periodicity at 1s (spectral_flux R3[10])
and onset periodicity at 1s (onset_strength R3[11]). Patel & Iversen 2014:
ASAP hypothesis -- beat perception requires continuous motor-auditory
interaction via dorsal pathway.

f11 captures continuous action simulation strength at fast timescales. Onset
value at 100ms (immediate onset detection) combined with motor-auditory
coupling at 100ms (current coupling state). Ross & Balasubramaniam 2022:
motor simulation generates temporal predictions; TMS to parietal/premotor
impairs beat but not interval timing.

f12 models the parietal dorsal auditory-motor pathway. Dorsal periodicity at
1s (sustained activity), dorsal velocity at 100ms (responsiveness), and the
INTERACTION of f10 * f11 (beat prediction gated by simulation strength).
Ross et al. 2018: cTBS to posterior parietal cortex impairs beat-based but
NOT interval timing (double dissociation).

H3 demands consumed (6 tuples):
  (10, 3, 0, 0)   spectral_flux value H3 L0        -- Onset at 100ms
  (10, 16, 14, 0)  spectral_flux periodicity H16 L0 -- Beat periodicity 1s
  (11, 16, 14, 0)  onset_strength periodicity H16 L0 -- Onset periodicity 1s
  (25, 3, 0, 0)   x_l0l5[0] value H3 L0            -- Coupling 100ms
  (33, 3, 8, 0)   x_l4l5[0] velocity H3 L0         -- Dorsal velocity 100ms
  (33, 16, 14, 0)  x_l4l5[0] periodicity H16 L0    -- Dorsal periodicity 1s

R3 features:
  [10] spectral_flux, [11] onset_strength

Upstream reads:
  PEOM relay (11D), MSR (11D) -- used for context but E-layer is H3-driven

Patel & Iversen 2014: ASAP hypothesis -- beat perception is motor simulation.
Ross et al. 2018: cTBS to parietal cortex -- double dissociation.
Ross & Balasubramaniam 2022: bidirectional motor-auditory coupling.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/asap/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ONSET_VAL_H3 = (10, 3, 0, 0)           # spectral_flux value H3 L0 (100ms)
_BEAT_PERIOD_H16 = (10, 16, 14, 0)      # spectral_flux periodicity H16 L0 (1s)
_ONSET_PERIOD_H16 = (11, 16, 14, 0)     # onset_strength periodicity H16 L0 (1s)
_COUPLING_VAL_H3 = (25, 3, 0, 0)        # x_l0l5[0] value H3 L0 (100ms)
_DORSAL_VEL_H3 = (33, 3, 8, 0)          # x_l4l5[0] velocity H3 L0 (100ms)
_DORSAL_PERIOD_H16 = (33, 16, 14, 0)    # x_l4l5[0] periodicity H16 L0 (1s)

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_SPECTRAL_FLUX = 10
_ONSET_STRENGTH = 11


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: beat prediction, motor simulation, dorsal stream.

    f10 (beat_prediction) is the temporal "when" prediction signal. Beat
    periodicity at 1s (rhythmic regularity) and onset periodicity at 1s
    (onset regularity) combine through sigmoid. The motor system predicts
    "when" not "what." Patel & Iversen 2014: ASAP hypothesis.

    f11 (motor_simulation) captures continuous action simulation at fast
    timescales. Onset value at 100ms (immediate detection) combined with
    motor-auditory coupling at 100ms (coupling state). Ross &
    Balasubramaniam 2022: motor simulation generates temporal predictions.

    f12 (dorsal_stream) models the parietal dorsal auditory-motor pathway.
    Dorsal periodicity at 1s, dorsal velocity at 100ms, and the INTERACTION
    of f10 * f11 (beat prediction gated by simulation). Ross et al. 2018:
    cTBS to posterior parietal cortex impairs beat timing.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        relay_outputs: ``{"PEOM": (B, T, 11), "MSR": (B, T, 11)}``

    Returns:
        ``(f10, f11, f12)`` each ``(B, T)``
    """
    # -- H3 features --
    onset_val = h3_features[_ONSET_VAL_H3]            # (B, T)
    beat_period = h3_features[_BEAT_PERIOD_H16]        # (B, T)
    onset_period = h3_features[_ONSET_PERIOD_H16]      # (B, T)
    coupling_val = h3_features[_COUPLING_VAL_H3]       # (B, T)
    dorsal_vel = h3_features[_DORSAL_VEL_H3]           # (B, T)
    dorsal_period = h3_features[_DORSAL_PERIOD_H16]    # (B, T)

    # -- R3 features (anchoring) --
    spectral_flux = r3_features[..., _SPECTRAL_FLUX]   # (B, T)
    onset_str = r3_features[..., _ONSET_STRENGTH]      # (B, T)

    # -- f10: Beat Prediction ("when") --
    # Motor system predicts beat timing via spectral_flux periodicity at 1s
    # (beat regularity) and onset_strength periodicity at 1s (onset
    # regularity). Patel & Iversen 2014: ASAP hypothesis.
    # f10 = sigma(0.40 * beat_periodicity_1s + 0.35 * onset_periodicity_1s)
    f10 = torch.sigmoid(
        0.40 * beat_period * spectral_flux.clamp(min=0.1)
        + 0.35 * onset_period * onset_str.clamp(min=0.1)
    )

    # -- f11: Motor Simulation --
    # Continuous action simulation at fast timescales. Onset at 100ms
    # (immediate onset detection) + coupling at 100ms (current coupling).
    # Ross & Balasubramaniam 2022: motor simulation generates predictions.
    # f11 = sigma(0.40 * onset_100ms + 0.35 * coupling_100ms)
    f11 = torch.sigmoid(
        0.40 * onset_val * onset_str.clamp(min=0.1)
        + 0.35 * coupling_val
    )

    # -- f12: Dorsal Stream --
    # Parietal dorsal auditory-motor pathway. Integrates dorsal periodicity
    # at 1s, dorsal velocity at 100ms, and the INTERACTION of f10 * f11.
    # The interaction term captures bidirectional coupling: motor prediction
    # (f11) modulates beat prediction (f10) through the dorsal pathway.
    # Ross et al. 2018: cTBS to posterior parietal cortex impairs beat timing.
    # f12 = sigma(0.35 * dorsal_period_1s + 0.35 * dorsal_vel_100ms
    #             + 0.30 * f10 * f11)
    f12 = torch.sigmoid(
        0.35 * dorsal_period
        + 0.35 * dorsal_vel
        + 0.30 * f10 * f11
    )

    return f10, f11, f12
