"""CLAM B+C-Layer -- Temporal Integration (5D).

Closed-Loop Affective Modulation integration signals:
  B0: decoded_affect       — EEG-decoded affective state [0, 1]
  B1: target_affect        — Therapeutic target affect [0, 1]
  B2: affect_error         — Divergence: decoded vs target [0, 1]
  C0: control_output       — Controller drive signal [0, 1]
  C1: music_param_delta    — Music parameter adjustment magnitude [0, 1]

B0 decodes the current affective state from combined arousal (loudness
dynamics) and valence (roughness/pleasantness) signals. This mirrors
the EEG-based affect classification in BCI systems where frontal gamma
power and asymmetry map to arousal-valence space.

B1 estimates the therapeutic target affect. In a real BCI system this
is set by the clinician; here we infer it from hedonic engagement
(SRP pleasure) combined with temporal stability. A stable, pleasant
state represents the default therapeutic target.

B2 is the affect error: the divergence between decoded state (B0) and
target state (B1). This is the core signal that drives the closed-loop
controller -- larger errors demand stronger corrective action.

C0 is the control output: how strongly the system should adjust music
parameters. Proportional to affect error, gated by loop coherence (E1).
When the loop is incoherent, control output is suppressed.

C1 captures the magnitude of music parameter adjustment needed. Combines
control output with brightness uncertainty (spectral centroid entropy)
and feedback signal dynamics.

H3 demands consumed (6 tuples):
  (0, 16, 0, 0)   roughness value H16 L0            -- 1s valence baseline
  (10, 16, 0, 0)  loudness value H16 L0             -- 1s integrated arousal
  (10, 12, 18, 0) loudness trend H12 L0             -- arousal trajectory error
  (0, 12, 18, 0)  roughness trend H12 L0            -- valence trajectory control
  (21, 7, 8, 0)   spectral_flux velocity H7 L0      -- feedback signal rate
  (12, 16, 20, 0) spectral_centroid entropy H16 L0  -- brightness uncertainty

R3 features:
  [0] roughness, [4] sensory_pleasantness, [8] velocity_A, [10] loudness,
  [12] spectral_centroid, [21] spectral_flux

Upstream reads:
  SRP relay (19D) -- pleasure signal (P2:pleasure at index 15)
  AAC relay (14D) -- emotional arousal (E0:emotional_arousal at index 0)

Ehrlich et al. 2019: BCI closed-loop, arousal trajectory control.
Daly et al. 2019: Affect decode from frontal EEG, music-feature mapping.
Miranda 2011: Brain-computer music interface, spectral parameter control.

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ROUGH_VAL_H16 = (0, 16, 0, 0)          # roughness value H16 L0
_LOUD_VAL_H16 = (10, 16, 0, 0)          # loudness value H16 L0
_LOUD_TREND_H12 = (10, 12, 18, 0)       # loudness trend H12 L0
_ROUGH_TREND_H12 = (0, 12, 18, 0)       # roughness trend H12 L0
_FLUX_VEL_H7 = (21, 7, 8, 0)           # spectral_flux velocity H7 L0
_CENTROID_ENTROPY_H16 = (12, 16, 20, 0)  # spectral_centroid entropy H16 L0

# -- R3 feature indices -------------------------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_VELOCITY_A = 8
_LOUDNESS = 10
_SPECTRAL_CENTROID = 12
_SPECTRAL_FLUX = 21

# -- Upstream relay indices ---------------------------------------------------
_SRP_PLEASURE = 15        # SRP P2:pleasure (hybrid, idx 15)
_AAC_EMOTIONAL_AROUSAL = 0  # AAC E0:emotional_arousal (internal, idx 0)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    """Compute B+C-layer: affect decode, target, error, control, and delta.

    B0 (decoded_affect) maps the current arousal-valence state from
    integrated loudness (arousal proxy) and roughness (inverted valence).
    This mirrors EEG-based affect classification.

    B1 (target_affect) infers the therapeutic target from hedonic
    engagement (pleasure) and temporal stability. Stable pleasant
    states = default target.

    B2 (affect_error) is |decoded - target|, the core closed-loop error
    signal. Larger errors drive stronger corrective action.

    C0 (control_output) is proportional to affect error, gated by loop
    coherence (E1). Control is suppressed when the loop is incoherent.

    C1 (music_param_delta) captures the magnitude of music parameter
    adjustment. Combines control with brightness uncertainty and
    feedback rate for parameter-level adaptation.

    Ehrlich et al. 2019: arousal trajectory error drives loop correction.
    Daly et al. 2019: music-feature mapping to affective dimensions.
    Miranda 2011: real-time parameter control via brain-computer interface.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(E0, E1)`` from extraction layer.
        relay_outputs: ``{"SRP": (B, T, 19), "AAC": (B, T, 14)}``

    Returns:
        ``(B0, B1, B2, C0, C1)`` each ``(B, T)``
    """
    e0, e1 = e

    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    rough_val = h3_features[_ROUGH_VAL_H16]             # (B, T)
    loud_val = h3_features[_LOUD_VAL_H16]               # (B, T)
    loud_trend = h3_features[_LOUD_TREND_H12]           # (B, T)
    rough_trend = h3_features[_ROUGH_TREND_H12]         # (B, T)
    flux_vel = h3_features[_FLUX_VEL_H7]               # (B, T)
    centroid_entropy = h3_features[_CENTROID_ENTROPY_H16]  # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]               # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    velocity_a = r3_features[..., _VELOCITY_A]             # (B, T)
    loudness = r3_features[..., _LOUDNESS]                 # (B, T)
    centroid = r3_features[..., _SPECTRAL_CENTROID]        # (B, T)
    flux = r3_features[..., _SPECTRAL_FLUX]                # (B, T)

    # -- Upstream relay features (graceful fallback) --
    srp = relay_outputs.get("SRP", torch.zeros(B, T, 19, device=device))
    aac = relay_outputs.get("AAC", torch.zeros(B, T, 14, device=device))
    pleasure = srp[..., _SRP_PLEASURE]              # (B, T)
    arousal = aac[..., _AAC_EMOTIONAL_AROUSAL]       # (B, T)

    # -- B0: Decoded Affect --
    # Maps current arousal-valence state. Arousal from loudness dynamics,
    # valence from pleasantness (inverted roughness). AAC arousal provides
    # upstream emotional context.
    # Daly et al. 2019: frontal asymmetry + gamma power -> arousal-valence.
    b0 = torch.sigmoid(
        0.35 * loud_val * arousal.clamp(min=0.1)
        + 0.35 * pleasantness * (1.0 - rough_val.clamp(0.0, 1.0))
        + 0.30 * velocity_a * loudness
    )

    # -- B1: Target Affect --
    # Therapeutic target inferred from hedonic engagement + stability.
    # Stable pleasure = default target. Loop coherence (E1) confirms
    # the target is trackable.
    # Ehrlich 2019: target set by clinician, here inferred from engagement.
    b1 = torch.sigmoid(
        0.40 * pleasure * e1.clamp(min=0.1)
        + 0.30 * pleasantness * (1.0 - roughness.clamp(0.0, 1.0))
        + 0.30 * (1.0 - loud_trend.abs().clamp(0.0, 1.0))
    )

    # -- B2: Affect Error --
    # Divergence between decoded and target affect. Core error signal.
    # Larger errors drive stronger corrective action from the controller.
    # Ehrlich 2019: error-driven loop correction, arousal r=0.74.
    raw_error = (b0 - b1).abs()
    trajectory_error = loud_trend.abs() * 0.50 + rough_trend.abs() * 0.50

    b2 = torch.sigmoid(
        0.45 * raw_error
        + 0.30 * trajectory_error
        + 0.25 * e0 * (1.0 - e1.clamp(0.0, 1.0))
    )

    # -- C0: Control Output --
    # Controller drive signal proportional to affect error, gated by
    # loop coherence. When the loop is incoherent (E1 low), control
    # is suppressed to prevent erratic music changes.
    # Miranda 2011: brain-computer music interface parameter control.
    c0 = torch.sigmoid(
        0.40 * b2 * e1.clamp(min=0.1)
        + 0.30 * flux_vel.abs() * e0
        + 0.30 * trajectory_error * e1
    )

    # -- C1: Music Parameter Delta --
    # Magnitude of music parameter adjustment. Combines control output
    # with brightness uncertainty (spectral centroid entropy) for
    # parameter-level adaptation. Higher uncertainty = more conservative.
    # Daly et al. 2019: tempo, mode, loudness mapped to affect dimensions.
    brightness_uncertainty = centroid_entropy.clamp(0.0, 1.0)

    c1 = torch.sigmoid(
        0.35 * c0 * (1.0 - brightness_uncertainty * 0.50)
        + 0.35 * flux_vel.abs() * centroid
        + 0.30 * b2 * flux
    )

    return b0, b1, b2, c0, c1
