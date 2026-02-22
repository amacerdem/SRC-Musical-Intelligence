"""MAD D+A Layer -- Temporal Integration (5D).

Musical Anhedonia Disconnection integration signals (D+A combined layer):
  D0: stg_nacc_connect      — STG-NAcc functional connectivity estimate [0, 1]
  D1: nacc_music_resp        — NAcc music-specific response [0, 1]
  D2: nacc_general_resp      — NAcc general (non-music) response [0, 1]
  A0: bmrq_estimate          — Barcelona Music Reward Questionnaire proxy [0, 1]
  A1: sound_specificity      — Sound-specificity of anhedonia [0, 1]

D0 estimates the functional connectivity between STG (auditory cortex) and
NAcc (reward nucleus). In musical anhedonia, this tract (uncinate fasciculus)
shows reduced fractional anisotropy (FA deficit d=-5.89, Martinez-Molina 2016).
Low D0 = disconnected pathway. Combines disrupted coupling (x_l4l5) with
reward dynamics from SRP.

D1 captures NAcc responsiveness to musical stimuli specifically. In musical
anhedonia, NAcc activation to music is selectively reduced while general
hedonic processing remains intact.

D2 captures NAcc responsiveness to non-music rewards (food, money). In
musical anhedonia, D2 is preserved (double dissociation). Uses general
arousal and spectral features that track non-music reward processing.

A0 estimates BMRQ score (Barcelona Music Reward Questionnaire). BMRQ is
the validated instrument for identifying musical anhedonia (Mas-Herrero 2013).
Low BMRQ = low music reward sensitivity = anhedonia.

A1 captures whether the anhedonia is sound-specific (90.9% in Martinez-Molina
2016). Musical anhedonics have preserved general hedonic capacity but
selectively impaired music reward. High A1 = sound-specific deficit.

H3 demands consumed (3 tuples):
  (4, 11, 8, 0)  sensory_pleasantness velocity H11 L0 -- reward dynamics 500ms
  (10, 11, 2, 0) loudness std H11 L0                  -- reward variability
  (0, 16, 20, 0) roughness entropy H16 L0             -- affect entropy

R3 features:
  [0] roughness, [2] harmonic_ratio, [4] sensory_pleasantness,
  [12] spectral_centroid, [22] distribution_entropy, [33:41] x_l4l5

Upstream reads:
  SRP relay (19D) -- P2:pleasure (idx 15)
  AAC relay (14D) -- E0:emotional_arousal (idx 0)

Martinez-Molina et al. 2016: White matter FA deficit d=-5.89 in uncinate
fasciculus connecting STG and NAcc (fMRI+DTI, N=45).
Mas-Herrero et al. 2013: BMRQ developed and validated for music reward
sensitivity (N=804, factor analysis).
Loui et al. 2017: 90.9% sound-specific musical anhedonia (N=22, DTI).

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/mad/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_PLEAS_VEL_H11 = (4, 11, 8, 0)       # sensory_pleasantness velocity H11 L0
_LOUD_STD_H11 = (10, 11, 2, 0)       # loudness std H11 L0
_ROUGH_ENT_H16 = (0, 16, 20, 0)      # roughness entropy H16 L0

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_ROUGHNESS = 0
_HARMONIC_RATIO = 2
_SENSORY_PLEASANTNESS = 4
_SPECTRAL_CENTROID = 12
_DISTRIBUTION_ENTROPY = 22
_X_L4L5_START = 33
_X_L4L5_END = 41

# -- Upstream relay indices ---------------------------------------------------
_SRP_PLEASURE = 15          # SRP P2:pleasure (idx 15 in 19D)
_AAC_EMOTIONAL_AROUSAL = 0  # AAC E0:emotional_arousal (idx 0 in 14D)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    """Compute D+A layer: connectivity, NAcc responses, BMRQ, and specificity.

    D0 (stg_nacc_connect) estimates STG-NAcc functional connectivity.
    Disrupted coupling (x_l4l5) combined with reward dynamics. Low D0 =
    disconnected uncinate fasciculus (FA deficit d=-5.89).

    D1 (nacc_music_resp) captures NAcc music-specific response. Low in
    musical anhedonia. Uses pleasure x hedonic dynamics x coupling.

    D2 (nacc_general_resp) captures NAcc general reward response. Preserved
    in musical anhedonia (double dissociation). Uses arousal + spectral
    features that generalize beyond music.

    A0 (bmrq_estimate) estimates BMRQ score. Low = anhedonia. Integrates
    E0 (anhedonia) with reward dynamics and connectivity.

    A1 (sound_specificity) measures whether anhedonia is sound-specific.
    90.9% of musical anhedonics show sound-specific deficit (Loui 2017).
    High = music-specific impairment with preserved general hedonic.

    Martinez-Molina et al. 2016: FA deficit d=-5.89 (fMRI+DTI, N=45).
    Mas-Herrero et al. 2013: BMRQ validated (N=804).
    Loui et al. 2017: 90.9% sound-specific (N=22, DTI).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(E0, E1)`` from extraction layer.
        relay_outputs: ``{"SRP": (B, T, 19), "AAC": (B, T, 14)}``

    Returns:
        ``(D0, D1, D2, A0, A1)`` each ``(B, T)``
    """
    e0, e1 = e

    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    pleas_vel_500ms = h3_features[_PLEAS_VEL_H11]   # (B, T)
    loud_std_500ms = h3_features[_LOUD_STD_H11]      # (B, T)
    rough_entropy = h3_features[_ROUGH_ENT_H16]      # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]               # (B, T)
    harmonic = r3_features[..., _HARMONIC_RATIO]            # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    centroid = r3_features[..., _SPECTRAL_CENTROID]          # (B, T)
    dist_entropy = r3_features[..., _DISTRIBUTION_ENTROPY]  # (B, T)
    x_l4l5 = r3_features[..., _X_L4L5_START:_X_L4L5_END]  # (B, T, 8)
    x_l4l5_mean = x_l4l5.mean(dim=-1)                     # (B, T)

    # -- Upstream relay features (graceful fallback) --
    srp = relay_outputs.get("SRP", torch.zeros(B, T, 19, device=device))
    aac = relay_outputs.get("AAC", torch.zeros(B, T, 14, device=device))
    pleasure = srp[..., _SRP_PLEASURE]                 # (B, T)
    emotional_arousal = aac[..., _AAC_EMOTIONAL_AROUSAL]  # (B, T)

    # -- Derived signals --
    # Coupling strength: x_l4l5 mean captures auditory-reward pathway integrity
    coupling = x_l4l5_mean.clamp(0.0, 1.0)

    # Reward dynamics: hedonic velocity + reward variability
    reward_dynamics = 0.50 * pleas_vel_500ms.abs() + 0.50 * loud_std_500ms

    # -- D0: STG-NAcc Functional Connectivity --
    # Estimates white matter tract integrity. High coupling + active reward
    # dynamics = intact connection. Low coupling + flat dynamics = disconnection.
    # Martinez-Molina et al. 2016: FA deficit d=-5.89 in uncinate fasciculus.
    d0 = torch.sigmoid(
        0.40 * coupling * pleasure.clamp(min=0.1)
        + 0.35 * reward_dynamics * harmonic
        + 0.25 * (1.0 - e0) * pleasantness
    )

    # -- D1: NAcc Music-Specific Response --
    # NAcc activation to music. Low in musical anhedonia.
    # Pleasure x hedonic dynamics x coupling = music reward processing.
    d1 = torch.sigmoid(
        0.40 * pleasure * coupling.clamp(min=0.1)
        + 0.35 * pleas_vel_500ms.abs() * pleasantness
        + 0.25 * (1.0 - e0) * harmonic
    )

    # -- D2: NAcc General Response --
    # NAcc activation to non-music rewards. Preserved in musical anhedonia.
    # Uses general arousal + spectral features (domain-general processing).
    # This creates the double dissociation with D1.
    d2 = torch.sigmoid(
        0.40 * emotional_arousal * centroid.clamp(min=0.1)
        + 0.35 * dist_entropy * rough_entropy
        + 0.25 * roughness * loud_std_500ms
    )

    # -- A0: BMRQ Estimate --
    # Barcelona Music Reward Questionnaire proxy. Low = anhedonia.
    # Integrates E-layer anhedonia with connectivity and reward response.
    # Mas-Herrero et al. 2013: BMRQ factor structure (N=804).
    a0 = torch.sigmoid(
        0.35 * (1.0 - e0) * d0
        + 0.35 * d1 * reward_dynamics
        + 0.30 * pleasure * coupling
    )

    # -- A1: Sound Specificity --
    # Whether anhedonia is sound-specific. High = music-specific impairment.
    # Computed as: music reward impaired (low D1) but general preserved (high D2).
    # Loui et al. 2017: 90.9% sound-specific (N=22, DTI).
    music_impaired = 1.0 - d1.clamp(0.0, 1.0)
    general_preserved = d2.clamp(0.0, 1.0)

    a1 = torch.sigmoid(
        0.40 * music_impaired * general_preserved
        + 0.35 * e1 * (1.0 - coupling)
        + 0.25 * e0 * emotional_arousal.clamp(min=0.1)
    )

    return d0, d1, d2, a0, a1
