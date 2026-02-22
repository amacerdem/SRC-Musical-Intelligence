"""RASN E-Layer -- Extraction (3D).

Rhythmic Auditory Stimulation Neuroplasticity extraction signals:
  E0: entrainment_strength      — SMA + auditory cortex phase-locking [0, 1]
  E1: motor_facilitation        — Premotor cortex + cerebellum activation [0, 1]
  E2: neuroplasticity_index     — Hippocampus + corticospinal connectivity [0, 1]

E0 captures how strongly neural oscillations lock to the beat frequency. Uses
motor-auditory coupling (x_l0l5) combined with beat induction signals and
spectral flux/onset. Rhythmic entrainment is the primary driver of RAS-based
neuroplasticity. SMA phase-locking to regular beats provides the temporal
scaffold for memory binding.

E1 captures the degree of motor pathway activation from auditory stimulation.
Uses sensorimotor integration features (x_l4l5) combined with energy envelope
(amplitude, loudness) and encoding/binding quality (stumpf fusion). Motor
facilitation reflects premotor cortex and cerebellar engagement for beat-driven
movement.

E2 measures the neuroplastic potential of current rhythmic stimulation. Uses an
inverted-U complexity function reflecting that moderate complexity produces
optimal plasticity demand. Combined with binding stability (stumpf fusion) and
engagement (sensory pleasantness).

H3 demands consumed (12 tuples):
  (10, 6, 0, 2)   spectral_flux value H6 L2        -- current beat onset 200ms
  (10, 11, 4, 0)  spectral_flux max H11 L0         -- peak onset 500ms
  (11, 6, 0, 2)   onset_strength value H6 L2       -- current onset sharpness
  (11, 11, 14, 0) onset_strength periodicity H11 L0 -- beat regularity 500ms
  (7, 6, 0, 2)    amplitude value H6 L2            -- current beat energy 200ms
  (7, 11, 8, 0)   amplitude velocity H11 L0        -- energy dynamics 500ms
  (7, 16, 1, 0)   amplitude mean H16 L0            -- average energy 1s
  (8, 6, 0, 2)    loudness value H6 L2             -- current accent strength
  (8, 11, 17, 0)  loudness peaks H11 L0            -- beat count per 500ms
  (8, 16, 1, 0)   loudness mean H16 L0             -- average loudness 1s
  (5, 6, 0, 2)    periodicity_strength value H6 L2 -- current rhythmic regularity
  (5, 11, 14, 0)  periodicity_strength period H11 L0 -- entrainment stability

R3 features:
  [7] amplitude, [8] loudness, [10] spectral_flux, [11] onset_strength,
  [5] periodicity_strength, [25:33] x_l0l5, [33:41] x_l4l5,
  [3] stumpf_fusion, [4] sensory_pleasantness, [23] entropy

Upstream reads:
  SNEM relay (12D) -- entrainment context
  beat-entrainment (F3 cross-circuit) -- beat-locked signals

Grahn & Brett 2007: SMA + putamen for beat-inducing rhythms (Z=5.67).
Harrison et al. 2025: sensorimotor cortex activation (FWE-corrected, N=55).
Blasi et al. 2025: structural neuroplasticity from rhythm (20 RCTs, N=718).

See Building/C3-Brain/F4-Memory-Systems/mechanisms/rasn/RASN-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_FLUX_VAL_H6 = (10, 6, 0, 2)         # spectral_flux value H6 L2
_FLUX_MAX_H11 = (10, 11, 4, 0)       # spectral_flux max H11 L0
_ONSET_VAL_H6 = (11, 6, 0, 2)        # onset_strength value H6 L2
_ONSET_PERIOD_H11 = (11, 11, 14, 0)  # onset_strength periodicity H11 L0
_AMP_VAL_H6 = (7, 6, 0, 2)           # amplitude value H6 L2
_AMP_VEL_H11 = (7, 11, 8, 0)         # amplitude velocity H11 L0
_AMP_MEAN_H16 = (7, 16, 1, 0)        # amplitude mean H16 L0
_LOUD_VAL_H6 = (8, 6, 0, 2)          # loudness value H6 L2
_LOUD_PEAKS_H11 = (8, 11, 17, 0)     # loudness peaks H11 L0
_LOUD_MEAN_H16 = (8, 16, 1, 0)       # loudness mean H16 L0
_PERIOD_VAL_H6 = (5, 6, 0, 2)        # periodicity_strength value H6 L2
_PERIOD_PERIOD_H11 = (5, 11, 14, 0)  # periodicity_strength periodicity H11 L0

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_AMPLITUDE = 7
_LOUDNESS = 8
_SPECTRAL_FLUX = 10
_ONSET_STRENGTH = 11
_PERIODICITY = 5
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_ENTROPY = 23
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L4L5_START = 33
_X_L4L5_END = 41

# -- Upstream relay indices ---------------------------------------------------
_SNEM_ENTRAINMENT = 7       # SNEM P1:entrainment_strength (hybrid, idx 7)
_SNEM_BEAT_ENTRAINMENT = 0  # SNEM E0:beat_entrainment (internal, idx 0)
_SNEM_METER = 1             # SNEM E1:meter_entrainment (internal, idx 1)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: rhythmic entrainment extraction signals.

    E0 (entrainment_strength) captures SMA + auditory cortex phase-locking
    to beat frequency. Motor-auditory coupling (x_l0l5) combined with beat
    induction signals and spectral flux/onset drives entrainment.

    E1 (motor_facilitation) captures premotor cortex + cerebellum activation
    from auditory stimulation. Sensorimotor integration (x_l4l5) combined
    with energy envelope and encoding quality.

    E2 (neuroplasticity_index) measures neuroplastic potential using an
    inverted-U complexity function (moderate complexity = optimal plasticity).
    Combined with binding stability and engagement.

    Grahn & Brett 2007: SMA + putamen respond to beat-inducing rhythms
    (fMRI N=27, Z=5.67, FDR p<.05).
    Harrison et al. 2025: external/internal cues activate sensorimotor cortex
    (fMRI N=55, FWE-corrected).
    Blasi et al. 2025: structural neuroplasticity from rhythm interventions
    (20 RCTs, N=718).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        relay_outputs: ``{"SNEM": (B, T, 12)}``

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    flux_val = h3_features[_FLUX_VAL_H6]            # (B, T)
    flux_max = h3_features[_FLUX_MAX_H11]            # (B, T)
    onset_val = h3_features[_ONSET_VAL_H6]           # (B, T)
    onset_period = h3_features[_ONSET_PERIOD_H11]    # (B, T)
    amp_val = h3_features[_AMP_VAL_H6]               # (B, T)
    amp_vel = h3_features[_AMP_VEL_H11]              # (B, T)
    amp_mean = h3_features[_AMP_MEAN_H16]            # (B, T)
    loud_val = h3_features[_LOUD_VAL_H6]             # (B, T)
    loud_peaks = h3_features[_LOUD_PEAKS_H11]        # (B, T)
    loud_mean = h3_features[_LOUD_MEAN_H16]          # (B, T)
    period_val = h3_features[_PERIOD_VAL_H6]         # (B, T)
    period_period = h3_features[_PERIOD_PERIOD_H11]  # (B, T)

    # -- R3 features --
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    x_l4l5 = r3_features[..., _X_L4L5_START:_X_L4L5_END]  # (B, T, 8)
    stumpf = r3_features[..., _STUMPF_FUSION]                # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]   # (B, T)
    entropy = r3_features[..., _ENTROPY]                     # (B, T)

    # -- Upstream relay features (graceful fallback) --
    snem = relay_outputs.get("SNEM", torch.zeros(B, T, 12, device=device))
    beat_ent = snem[..., _SNEM_BEAT_ENTRAINMENT]    # (B, T) beat entrainment
    meter_ent = snem[..., _SNEM_METER]              # (B, T) meter entrainment
    entrainment = snem[..., _SNEM_ENTRAINMENT]       # (B, T) entrainment strength

    # -- Derived signals --
    x_l0l5_mean = x_l0l5.mean(dim=-1)   # (B, T)
    x_l4l5_mean = x_l4l5.mean(dim=-1)   # (B, T)

    # Beat induction: flux/onset at beat level combined with periodicity
    beat_induction = 0.35 * flux_val * onset_val + 0.35 * flux_max + 0.30 * period_val

    # Motor engagement: sensorimotor coupling + energy dynamics
    motor_engagement = 0.40 * x_l4l5_mean + 0.30 * amp_vel + 0.30 * loud_peaks

    # Encoding quality: SNEM entrainment + meter structure
    encoding = 0.50 * entrainment + 0.50 * meter_ent

    # -- E0: Entrainment Strength --
    # SMA + auditory cortex phase-locking to beat frequency.
    # Motor-auditory coupling (x_l0l5) x beat induction x SNEM context.
    # Nozaradan 2012: SS-EPs at beat frequency. Grahn & Brett 2007: SMA Z=5.67.
    e0 = torch.sigmoid(
        0.35 * x_l0l5_mean * beat_ent.clamp(min=0.1)
        + 0.35 * flux_val * onset_val * meter_ent.clamp(min=0.1)
        + 0.30 * period_val * encoding.clamp(min=0.1)
    )

    # -- E1: Motor Facilitation --
    # Premotor cortex + cerebellum activation from auditory stimulation.
    # Sensorimotor integration (x_l4l5) x motor engagement x encoding.
    # Harrison et al. 2025: both external and internal cues activate
    # sensorimotor cortex (FWE-corrected, N=55).
    e1 = torch.sigmoid(
        0.40 * x_l4l5_mean * motor_engagement.clamp(min=0.1)
        + 0.30 * amp_val * loud_val
        + 0.30 * encoding * stumpf
    )

    # -- E2: Neuroplasticity Index --
    # Hippocampus + corticospinal connectivity. Inverted-U complexity
    # function: moderate complexity produces optimal plasticity demand.
    # Blasi et al. 2025: structural neuroplasticity from rhythm interventions
    # (20 RCTs, N=718).
    entropy_optimal = 1.0 - (entropy - 0.5).abs() * 2.0  # inverted-U [0, 1]

    e2 = torch.sigmoid(
        0.35 * entropy_optimal * entrainment
        + 0.35 * period_period * onset_period
        + 0.30 * stumpf * pleasantness
    )

    return e0, e1, e2
