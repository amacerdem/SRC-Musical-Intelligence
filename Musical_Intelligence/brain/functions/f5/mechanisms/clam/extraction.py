"""CLAM E-Layer -- Extraction (2D).

Closed-Loop Affective Modulation extraction signals:
  E0: affective_mod           — BCI affective modulation strength [0, 1]
  E1: loop_coherence          — Feedback loop coherence [0, 1]

E0 captures the degree to which the closed-loop BCI system is actively
modulating the listener's affective state. Combines frontal EEG gamma
power (proxied by spectral energy dynamics) with the current pleasure
signal from SRP and arousal from AAC. When EEG-decoded affect diverges
from the target, modulation strength increases. The FC6 electrode site
provides the primary gamma-band signal for affect decoding.

E1 measures the coherence (stability) of the feedback loop itself. A
coherent loop has low entropy in arousal dynamics, consistent feedback
signal rate, and stable SRP pleasure. When the loop breaks down
(participant disengagement, artifact), coherence drops. This gates all
downstream computations.

H3 demands consumed (2 tuples):
  (10, 16, 20, 0) loudness entropy H16 L0        -- 1s entropy of arousal
  (10, 7, 8, 0)   loudness velocity H7 L0        -- instantaneous arousal change

R3 features:
  [0] roughness, [4] sensory_pleasantness, [10] loudness, [11] onset_strength,
  [21] spectral_flux, [25:33] x_l0l5

Upstream reads:
  SRP relay (19D) -- pleasure signal (P2:pleasure at index 15)
  AAC relay (14D) -- emotional arousal (E0:emotional_arousal at index 0)

Ehrlich et al. 2019: BCI closed-loop, N=5, arousal r=0.74, valence r=0.52.
Daly et al. 2019: Affective BCI, frontal EEG gamma for affect decode.

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_LOUD_ENTROPY_H16 = (10, 16, 20, 0)   # loudness entropy H16 L0
_LOUD_VEL_H7 = (10, 7, 8, 0)          # loudness velocity H7 L0

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 10
_ONSET_STRENGTH = 11
_SPECTRAL_FLUX = 21
_X_L0L5_START = 25
_X_L0L5_END = 33

# -- Upstream relay indices ---------------------------------------------------
_SRP_PLEASURE = 15        # SRP P2:pleasure (hybrid, idx 15)
_AAC_EMOTIONAL_AROUSAL = 0  # AAC E0:emotional_arousal (internal, idx 0)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute E-layer: BCI affective modulation extraction signals.

    E0 (affective_mod) captures the active modulation strength of the
    closed-loop BCI system. Frontal gamma power (proxied by spectral
    energy dynamics), SRP pleasure, and AAC arousal combine to estimate
    how strongly the loop is driving affective change. Higher values
    indicate the BCI is actively steering affect.

    E1 (loop_coherence) measures feedback loop stability. Low arousal
    entropy + consistent spectral flux + stable pleasure signal = coherent
    loop. When the loop degrades (disengagement, artifact), coherence
    drops and gates downstream processing.

    Ehrlich et al. 2019: BCI closed-loop affective modulation (N=5,
    arousal tracking r=0.74, valence tracking r=0.52).
    Daly et al. 2019: Frontal EEG gamma for affect classification.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        relay_outputs: ``{"SRP": (B, T, 19), "AAC": (B, T, 14)}``

    Returns:
        ``(E0, E1)`` each ``(B, T)``
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    loud_entropy = h3_features[_LOUD_ENTROPY_H16]   # (B, T)
    loud_vel = h3_features[_LOUD_VEL_H7]            # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]                   # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]     # (B, T)
    loudness = r3_features[..., _LOUDNESS]                     # (B, T)
    onset = r3_features[..., _ONSET_STRENGTH]                  # (B, T)
    flux = r3_features[..., _SPECTRAL_FLUX]                    # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]     # (B, T, 8)
    x_l0l5_mean = x_l0l5.mean(dim=-1)                         # (B, T)

    # -- Upstream relay features (graceful fallback) --
    srp = relay_outputs.get("SRP", torch.zeros(B, T, 19, device=device))
    aac = relay_outputs.get("AAC", torch.zeros(B, T, 14, device=device))
    pleasure = srp[..., _SRP_PLEASURE]              # (B, T)
    arousal = aac[..., _AAC_EMOTIONAL_AROUSAL]       # (B, T)

    # -- Derived signals --
    # Affect divergence: how much the current state deviates (drives modulation)
    affect_divergence = loud_vel.abs() * 0.50 + (1.0 - pleasantness) * roughness * 0.50

    # Loop signal quality: spectral flux consistency x onset density
    signal_quality = 0.50 * flux * onset.clamp(min=0.1) + 0.50 * x_l0l5_mean

    # -- E0: Affective Modulation Strength --
    # Active modulation from BCI loop. Combines affect divergence (drives
    # loop activity), arousal from AAC, and pleasure from SRP. Stronger
    # when the loop detects that the current affective state diverges
    # from the target.
    # Ehrlich 2019: arousal tracking r=0.74 via EEG-driven music adaptation.
    e0 = torch.sigmoid(
        0.35 * affect_divergence * arousal.clamp(min=0.1)
        + 0.35 * loudness * pleasure.clamp(min=0.1)
        + 0.30 * loud_vel.abs() * x_l0l5_mean
    )

    # -- E1: Loop Coherence --
    # Stability of the feedback loop. Low entropy in arousal (stable state)
    # + consistent signal quality + pleasure stability = coherent loop.
    # Ehrlich 2019: 3/5 participants maintained coherent loops.
    # Inverted entropy: high entropy = low coherence.
    arousal_stability = 1.0 - loud_entropy.clamp(0.0, 1.0)

    e1 = torch.sigmoid(
        0.35 * arousal_stability * signal_quality
        + 0.35 * pleasure * pleasantness
        + 0.30 * (1.0 - affect_divergence.clamp(0.0, 1.0))
    )

    return e0, e1
