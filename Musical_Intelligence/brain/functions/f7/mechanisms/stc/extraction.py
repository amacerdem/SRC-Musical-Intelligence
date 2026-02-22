"""STC E-Layer -- Extraction (3D).

Interoceptive-motor integration features for singing training connectivity:
  E0: f28_interoceptive_coupling  -- Insula-sensorimotor connectivity [0, 1]
  E1: f29_respiratory_integration -- Respiratory motor control quality [0, 1]
  E2: f30_speech_sensorimotor     -- Speech motor area activation [0, 1]

Interoceptive coupling (f28) captures how strongly the interoceptive
monitoring system (insula) is coupled with sensorimotor areas, estimated
from interoceptive periodicity at 1s.  f28 = sigma(0.40 * interoceptive_
period_1s).  Zamorano 2023: singing training predicts enhanced insula
co-activation with sensorimotor areas.

Respiratory integration (f29) combines respiratory periodicity at 1s with
breath entropy at 100ms.  f29 = sigma(0.40 * respiratory_period_1s +
0.30 * breath_entropy).  Tsunada 2024: dual vocal suppression supports
separate interoceptive and motor pathways.

Speech sensorimotor (f30) estimates speech motor area engagement from
vocal warmth at 100ms.  f30 = sigma(0.35 * vocal_warmth_100ms).
Kleber 2013: connectivity with M1, S1, auditory cortex; pitch deviation
t(728) = -4.8, p < .001.

H3 demands consumed (11):
  (33, 3, 0, 2)   x_l4l5 value H3 L2       -- Interoceptive signal 100ms
  (33, 3, 2, 2)   x_l4l5 std H3 L2         -- Interoceptive variability 100ms
  (33, 8, 14, 2)  x_l4l5 periodicity H8 L2 -- Interoceptive period 500ms
  (33, 16, 14, 2) x_l4l5 periodicity H16 L2 -- Interoceptive period 1s
  (25, 3, 0, 2)   x_l0l5 value H3 L2       -- Respiratory coupling 100ms
  (25, 8, 14, 2)  x_l0l5 periodicity H8 L2 -- Respiratory period 500ms
  (25, 16, 14, 2) x_l0l5 periodicity H16 L2 -- Respiratory period 1s
  (8, 3, 0, 2)    loudness value H3 L2      -- Breath amplitude 100ms
  (8, 3, 20, 2)   loudness entropy H3 L2    -- Breath entropy 100ms
  (12, 3, 0, 2)   warmth value H3 L2        -- Vocal warmth 100ms
  (15, 3, 0, 2)   tristimulus1 value H3 L2  -- Voice harmonic 100ms

R3 inputs: amplitude[7], loudness[8], warmth[12], tristimulus1[15],
           x_l0l5[25:33], x_l4l5[33:41]

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/stc/e_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_INTERO_VAL_H3 = (33, 3, 0, 2)       # x_l4l5 value H3 L2
_INTERO_STD_H3 = (33, 3, 2, 2)       # x_l4l5 std H3 L2
_INTERO_PER_H8 = (33, 8, 14, 2)      # x_l4l5 periodicity H8 L2
_INTERO_PER_H16 = (33, 16, 14, 2)    # x_l4l5 periodicity H16 L2
_RESP_VAL_H3 = (25, 3, 0, 2)         # x_l0l5 value H3 L2
_RESP_PER_H8 = (25, 8, 14, 2)        # x_l0l5 periodicity H8 L2
_RESP_PER_H16 = (25, 16, 14, 2)      # x_l0l5 periodicity H16 L2
_BREATH_AMP_H3 = (8, 3, 0, 2)        # loudness value H3 L2
_BREATH_ENT_H3 = (8, 3, 20, 2)       # loudness entropy H3 L2
_WARMTH_VAL_H3 = (12, 3, 0, 2)       # warmth value H3 L2
_HARMONIC_VAL_H3 = (15, 3, 0, 2)     # tristimulus1 value H3 L2


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: 3D interoceptive-motor extraction.

    E0 (f28_interoceptive_coupling): Insula-sensorimotor connectivity
    from interoceptive periodicity at 1s.
    Zamorano 2023: singing training predicts enhanced resting-state
    connectivity between insula and speech/respiratory sensorimotor areas.
    Kleber 2013: right AIC dissociates expertise x anesthesia (F = 22.08).

    E1 (f29_respiratory_integration): Respiratory motor control quality
    from respiratory periodicity at 1s and breath entropy at 100ms.
    Zarate 2008: ACC + pSTS + anterior insula network.
    Tsunada 2024: dual vocal suppression (phasic + tonic).

    E2 (f30_speech_sensorimotor): Speech motor area activation from
    vocal warmth at 100ms.
    Kleber 2013: connectivity with M1, S1, auditory cortex.
    Criscuolo 2022: ALE meta-analysis (84 studies, 3005 participants).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        upstream_outputs: ``{"MSR": (B, T, 11), "SPMC": (B, T, 11)}``.

    Returns:
        ``(f28, f29, f30)`` each ``(B, T)``.
    """
    # -- H3 features --
    intero_per_1s = h3_features[_INTERO_PER_H16]    # (B, T)
    resp_per_1s = h3_features[_RESP_PER_H16]         # (B, T)
    breath_ent = h3_features[_BREATH_ENT_H3]          # (B, T)
    warmth_val = h3_features[_WARMTH_VAL_H3]           # (B, T)

    # -- E0: f28 Interoceptive Coupling --
    # sigma(0.40 * interoceptive_period_1s)
    # Zamorano 2023: singing training -> insula-sensorimotor connectivity
    # Kleber 2013: right AIC expertise x anesthesia (F = 22.08)
    f28 = torch.sigmoid(0.40 * intero_per_1s)

    # -- E1: f29 Respiratory Integration --
    # sigma(0.40 * respiratory_period_1s + 0.30 * breath_entropy)
    # Zarate 2008: ACC + pSTS + anterior insula
    # Tsunada 2024: dual vocal suppression (phasic gating + tonic prediction)
    f29 = torch.sigmoid(
        0.40 * resp_per_1s
        + 0.30 * breath_ent
    )

    # -- E2: f30 Speech Sensorimotor --
    # sigma(0.35 * vocal_warmth_100ms)
    # Kleber 2013: M1, S1, auditory cortex connectivity
    # Criscuolo 2022: ALE meta-analysis cortico-subcortical network
    f30 = torch.sigmoid(0.35 * warmth_val)

    return f28, f29, f30
