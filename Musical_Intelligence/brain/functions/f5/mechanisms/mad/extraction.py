"""MAD E-Layer -- Extraction (2D).

Musical Anhedonia Disconnection extraction signals:
  E0: anhedonia           — STG-NAcc disconnection index [0, 1]
  E1: dissociation_idx    — Reward-perception dissociation [0, 1]

E0 captures the degree to which the auditory-reward pathway is disrupted.
Operationalised as: intact auditory processing (sensory_pleasantness,
harmonic_ratio) combined with absent reward-system response (SRP.pleasure).
High E0 = high anhedonia: strong sensory processing but no reward coupling.
The uncinate fasciculus FA deficit (d=-5.89, Martinez-Molina et al. 2016)
disrupts white matter connectivity between STG and NAcc.

E1 captures the dissociation between preserved sensory perception and
absent emotional response. Uses the double dissociation principle:
tonalness and spectral features are intact, but reward dynamics
(SRP pleasure, AAC arousal) fail to engage. High E1 = clear dissociation
between perception and reward.

H3 demands consumed (3 tuples):
  (4, 16, 0, 0)  sensory_pleasantness value H16 L0     -- 1s hedonic (absent reward)
  (4, 6, 8, 0)   sensory_pleasantness velocity H6 L0   -- hedonic change rate (flat)
  (10, 16, 20, 0) loudness entropy H16 L0              -- 1s affect entropy (low)

R3 features:
  [0] roughness, [2] harmonic_ratio, [4] sensory_pleasantness,
  [10] loudness, [14] tonalness, [33:41] x_l4l5

Upstream reads:
  SRP relay (19D) -- P2:pleasure (idx 15)
  AAC relay (14D) -- E0:emotional_arousal (idx 0)

Martinez-Molina et al. 2016: STG-NAcc functional disconnection in
specific musical anhedonia (fMRI, N=45, d=-5.89 FA deficit).
Mas-Herrero et al. 2014: BMRQ identifies musical anhedonia prevalence
3-5% (N=500, Barcelona).

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/mad/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_PLEAS_VAL_H16 = (4, 16, 0, 0)       # sensory_pleasantness value H16 L0
_PLEAS_VEL_H6 = (4, 6, 8, 0)         # sensory_pleasantness velocity H6 L0
_LOUD_ENT_H16 = (10, 16, 20, 0)      # loudness entropy H16 L0

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_ROUGHNESS = 0
_HARMONIC_RATIO = 2
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 10
_TONALNESS = 14
_X_L4L5_START = 33
_X_L4L5_END = 41

# -- Upstream relay indices ---------------------------------------------------
_SRP_PLEASURE = 15          # SRP P2:pleasure (idx 15 in 19D)
_AAC_EMOTIONAL_AROUSAL = 0  # AAC E0:emotional_arousal (idx 0 in 14D)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute E-layer: anhedonia and dissociation extraction signals.

    E0 (anhedonia) captures STG-NAcc disconnection. Intact sensory processing
    (sensory pleasantness, harmonic ratio) combined with absent reward response
    (SRP pleasure). High E0 = strong auditory signal with no reward coupling,
    the hallmark of musical anhedonia.

    E1 (dissociation_idx) captures the double dissociation between preserved
    auditory perception and absent emotional engagement. Uses tonalness and
    spectral features (preserved) vs reward dynamics (absent).

    Martinez-Molina et al. 2016: STG-NAcc white matter disconnection
    (d=-5.89 FA deficit, fMRI N=45).
    Mas-Herrero et al. 2014: BMRQ prevalence 3-5% (N=500).

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
    pleas_val_1s = h3_features[_PLEAS_VAL_H16]      # (B, T)
    pleas_vel = h3_features[_PLEAS_VEL_H6]          # (B, T)
    loud_entropy = h3_features[_LOUD_ENT_H16]       # (B, T)

    # -- R3 features --
    harmonic = r3_features[..., _HARMONIC_RATIO]          # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    tonalness = r3_features[..., _TONALNESS]              # (B, T)
    x_l4l5 = r3_features[..., _X_L4L5_START:_X_L4L5_END]  # (B, T, 8)
    x_l4l5_mean = x_l4l5.mean(dim=-1)                    # (B, T)

    # -- Upstream relay features (graceful fallback) --
    srp = relay_outputs.get("SRP", torch.zeros(B, T, 19, device=device))
    aac = relay_outputs.get("AAC", torch.zeros(B, T, 14, device=device))
    pleasure = srp[..., _SRP_PLEASURE]                # (B, T)
    emotional_arousal = aac[..., _AAC_EMOTIONAL_AROUSAL]  # (B, T)

    # -- Derived signals --
    # Intact auditory: sensory pleasantness + harmonic ratio (preserved in anhedonia)
    intact_auditory = 0.50 * pleasantness + 0.50 * harmonic

    # Reward absence: inverted pleasure + flat hedonic velocity
    # In anhedonia, pleasure is low and hedonic velocity is flat (near zero)
    reward_absence = 1.0 - pleasure.clamp(0.0, 1.0)

    # Hedonic flatness: low velocity = no reward dynamics
    hedonic_flatness = 1.0 - pleas_vel.abs().clamp(0.0, 1.0)

    # -- E0: Anhedonia --
    # STG-NAcc disconnection: intact sensory processing x absent reward coupling.
    # High when auditory features are present but reward system does not respond.
    # Martinez-Molina et al. 2016: d=-5.89 FA deficit.
    e0 = torch.sigmoid(
        0.35 * intact_auditory * reward_absence
        + 0.35 * hedonic_flatness * pleas_val_1s.clamp(min=0.1)
        + 0.30 * (1.0 - x_l4l5_mean) * (1.0 - emotional_arousal.clamp(0.0, 1.0))
    )

    # -- E1: Dissociation Index --
    # Double dissociation: preserved perception vs absent emotion.
    # Tonalness and loudness entropy intact, but reward dynamics absent.
    # Mas-Herrero et al. 2014: BMRQ identifies dissociation.
    e1 = torch.sigmoid(
        0.35 * tonalness * reward_absence
        + 0.35 * (1.0 - loud_entropy.clamp(0.0, 1.0)) * hedonic_flatness
        + 0.30 * intact_auditory * (1.0 - pleasure.clamp(0.0, 1.0))
    )

    return e0, e1
