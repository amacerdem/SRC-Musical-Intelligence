"""RASN P-Layer -- Cognitive Present (3D).

Present-time rhythmic auditory stimulation neuroplasticity signals:
  P0: entrainment_state          — Current neural oscillation lock [0, 1]
  P1: temporal_precision         — Beat tracking accuracy [0, 1]
  P2: motor_facilitation_level   — Movement readiness state [0, 1]

P0 captures the real-time phase-locking state between neural oscillations
and the auditory beat. This is the instantaneous reading of how well the
brain has locked onto the rhythmic stimulus. Derived from beat_induction
aggregation -- the present-moment neural entrainment level that drives all
downstream plasticity.

P1 measures how accurately the brain tracks the beat. Derived from meter
extraction crossed with periodicity. High temporal precision indicates
clean cerebellar-SMA coordination where beat predictions closely match
actual onsets. Distinct from entrainment (which measures lock strength) --
precision measures lock quality.

P2 captures the current state of motor pathway readiness driven by rhythmic
stimulation. Reflects the moment-by-moment activation of premotor cortex
and cerebellum. Rhythmic auditory stimulation facilitates movement even
without explicit motor tasks (covert motor simulation).

H3 demands consumed (4 tuples -- shared keys with E-layer):
  (5, 6, 0, 2)    periodicity_strength value H6 L2   -- rhythmic regularity
  (5, 11, 14, 0)  periodicity_strength period H11 L0 -- entrainment stability
  (10, 16, 14, 0) spectral_flux periodicity H16 L0   -- beat regularity 1s
  (7, 16, 1, 0)   amplitude mean H16 L0              -- average energy 1s

R3 features:
  [5] periodicity_strength, [10] spectral_flux, [11] onset_strength,
  [25:33] x_l0l5

Upstream reads:
  SNEM relay (12D) -- entrainment context

Noboa et al. 2025: SS-EPs at beat-related frequencies (1.25 Hz, EEG N=30).
Ding et al. 2025: all 12 rates (1-12 Hz) entrain neural oscillations
(ITPC eta-sq=0.14, EPS eta-sq=0.32, N=37).
Ross & Balasubramaniam 2022: covert motor simulation for beat perception.
Harrison et al. 2025: external/internal cues activate sensorimotor cortex.

See Building/C3-Brain/F4-Memory-Systems/mechanisms/rasn/RASN-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_PERIOD_VAL_H6 = (5, 6, 0, 2)          # periodicity_strength value H6 L2
_PERIOD_PERIOD_H11 = (5, 11, 14, 0)    # periodicity_strength period H11 L0
_FLUX_PERIOD_H16 = (10, 16, 14, 0)     # spectral_flux periodicity H16 L0
_AMP_MEAN_H16 = (7, 16, 1, 0)          # amplitude mean H16 L0

# -- R3 feature indices -------------------------------------------------------
_PERIODICITY = 5
_SPECTRAL_FLUX = 10
_ONSET_STRENGTH = 11
_X_L0L5_START = 25
_X_L0L5_END = 33

# -- Upstream relay indices ---------------------------------------------------
_SNEM_ENTRAINMENT = 7     # SNEM P1:entrainment_strength
_SNEM_BEAT_SALIENCE = 3   # SNEM M0:ssep_enhancement
_SNEM_ENHANCEMENT = 5     # SNEM M2:beat_salience -> idx 5


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: present-time entrainment, precision, and motor state.

    P0 (entrainment_state) captures real-time SMA phase-locking. Combines
    beat_induction from H3 periodicity, E0 (entrainment strength), and
    SNEM context. This is the instantaneous entrainment reading.

    P1 (temporal_precision) measures beat tracking accuracy. Meter
    extraction (flux periodicity at bar level) crossed with periodicity
    provides precision. Cerebellar error correction produces precise
    temporal alignment.

    P2 (motor_facilitation_level) captures movement readiness. Motor
    facilitation (E1), motor recovery potential (M1), and SNEM entrainment
    context drive motor pathway activation.

    Noboa et al. 2025: SS-EPs at beat-related frequencies (1.25 Hz).
    Ding et al. 2025: all 12 rates entrain neural oscillations (N=37).
    Ross & Balasubramaniam 2022: covert motor simulation.
    Harrison et al. 2025: sensorimotor cortex activation (N=55 fMRI).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        relay_outputs: ``{"SNEM": (B, T, 12)}``

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``
    """
    e0, e1, _e2 = e
    m0, m1 = m

    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    period_val = h3_features[_PERIOD_VAL_H6]           # (B, T)
    period_period = h3_features[_PERIOD_PERIOD_H11]    # (B, T)
    flux_period_1s = h3_features[_FLUX_PERIOD_H16]     # (B, T)
    amp_mean_1s = h3_features[_AMP_MEAN_H16]           # (B, T)

    # -- R3 features --
    periodicity = r3_features[..., _PERIODICITY]       # (B, T)
    flux = r3_features[..., _SPECTRAL_FLUX]            # (B, T)
    onset = r3_features[..., _ONSET_STRENGTH]          # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    x_l0l5_mean = x_l0l5.mean(dim=-1)                 # (B, T)

    # -- Upstream relay features (graceful fallback) --
    snem = relay_outputs.get("SNEM", torch.zeros(B, T, 12, device=device))
    snem_entrainment = snem[..., _SNEM_ENTRAINMENT]    # (B, T)
    snem_beat_sal = snem[..., _SNEM_BEAT_SALIENCE]     # (B, T)

    # -- Derived signals --
    # Beat induction aggregation: periodicity-driven entrainment state
    beat_induction = (
        0.35 * period_val * x_l0l5_mean
        + 0.35 * flux_period_1s
        + 0.30 * snem_beat_sal
    )

    # Meter extraction: bar-level periodic structure
    meter_extraction = 0.50 * flux_period_1s + 0.50 * period_period

    # -- P0: Entrainment State --
    # Real-time phase-locking state between neural oscillations and beat.
    # Beat induction + E0 (entrainment strength) + SNEM context.
    # Noboa et al. 2025: SS-EPs at beat-related frequencies (1.25 Hz).
    p0 = torch.sigmoid(
        0.35 * beat_induction
        + 0.35 * e0
        + 0.30 * snem_entrainment
    )

    # -- P1: Temporal Precision --
    # Beat tracking accuracy: meter extraction x periodicity.
    # Cerebellar-SMA coordination produces precise temporal alignment.
    # Ding et al. 2025: ITPC eta-sq=0.14, EPS eta-sq=0.32 (N=37).
    p1 = torch.sigmoid(
        0.40 * meter_extraction * periodicity.clamp(min=0.1)
        + 0.30 * onset * flux
        + 0.30 * period_period
    )

    # -- P2: Motor Facilitation Level --
    # Movement readiness from rhythmic stimulation. E1 (motor facilitation)
    # + M1 (motor recovery) + sustained energy context.
    # Harrison et al. 2025: sensorimotor cortex activation (FWE-corrected).
    # Ross & Balasubramaniam 2022: covert motor simulation.
    p2 = torch.sigmoid(
        0.40 * e1 * m1.clamp(min=0.1)
        + 0.30 * amp_mean_1s * snem_entrainment
        + 0.30 * m0
    )

    return p0, p1, p2
