"""MAD P-Layer -- Cognitive Present (2D).

Present-time musical anhedonia disconnection signals:
  P0: impaired_reward      — Current music reward impairment state [0, 1]
  P1: preserved_auditory   — Current auditory processing preservation [0, 1]

P0 captures the real-time state of music reward impairment. This is the
moment-by-moment reading of how much the reward system fails to engage
with the current musical input. Integrates E0 (anhedonia), D0 (connectivity),
and D1 (music-specific NAcc response) with instantaneous hedonic and
arousal signals.

P1 captures the real-time state of preserved auditory processing. In musical
anhedonia, auditory cortex (STG) functions normally -- sound perception,
tonalness, spectral analysis all remain intact. High P1 confirms that the
deficit is not perceptual but connective (STG-NAcc disconnection). This
is the hallmark double dissociation: P0 high (impaired reward) + P1 high
(preserved perception).

H3 demands consumed (2 tuples):
  (10, 6, 0, 0)  loudness value H6 L0               -- instant arousal
  (4, 6, 0, 0)   sensory_pleasantness value H6 L0   -- instant hedonic

R3 features:
  [4] sensory_pleasantness, [11] onset_strength, [12] spectral_centroid,
  [14] tonalness, [21] spectral_flux

Loui et al. 2017: Musical anhedonia is perceptually intact (N=22, DTI).
Martinez-Molina et al. 2016: STG activation preserved in anhedonia (fMRI, N=45).

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/mad/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_LOUD_VAL_H6 = (10, 6, 0, 0)         # loudness value H6 L0
_PLEAS_VAL_H6 = (4, 6, 0, 0)         # sensory_pleasantness value H6 L0

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_SENSORY_PLEASANTNESS = 4
_ONSET_STRENGTH = 11
_SPECTRAL_CENTROID = 12
_TONALNESS = 14
_SPECTRAL_FLUX = 21


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: present-time reward impairment and auditory preservation.

    P0 (impaired_reward) captures real-time music reward impairment. Integrates
    E0 (anhedonia), D0 (connectivity), and D1 (music-specific NAcc response)
    with instantaneous hedonic signal. High P0 = reward system not responding
    to current musical input.

    P1 (preserved_auditory) captures real-time auditory processing preservation.
    Tonalness + onset_strength + spectral features remain intact. This confirms
    the deficit is connective (STG-NAcc disconnection), not perceptual.

    Loui et al. 2017: musical anhedonia is perceptually intact (N=22, DTI).
    Martinez-Molina et al. 2016: STG activation preserved (fMRI, N=45).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(D0, D1, D2, A0, A1)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    e0, e1 = e
    d0, d1, _d2, _a0, a1 = m

    # -- H3 features --
    loud_instant = h3_features[_LOUD_VAL_H6]      # (B, T)
    pleas_instant = h3_features[_PLEAS_VAL_H6]    # (B, T)

    # -- R3 features --
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    onset = r3_features[..., _ONSET_STRENGTH]               # (B, T)
    centroid = r3_features[..., _SPECTRAL_CENTROID]          # (B, T)
    tonalness = r3_features[..., _TONALNESS]                # (B, T)
    spectral_flux = r3_features[..., _SPECTRAL_FLUX]        # (B, T)

    # -- P0: Impaired Reward --
    # Real-time music reward impairment state. E0 (anhedonia) + low connectivity
    # (1 - D0) + low music NAcc (1 - D1) + instant hedonic context.
    # High P0 = reward system fails to engage with current music.
    # Martinez-Molina et al. 2016: NAcc response absent to music (d=-5.89).
    reward_impairment = (
        0.50 * (1.0 - d1.clamp(0.0, 1.0))
        + 0.50 * (1.0 - d0.clamp(0.0, 1.0))
    )

    p0 = torch.sigmoid(
        0.35 * e0 * reward_impairment
        + 0.35 * a1 * (1.0 - pleas_instant.clamp(0.0, 1.0))
        + 0.30 * e1 * (1.0 - loud_instant.clamp(0.0, 1.0))
    )

    # -- P1: Preserved Auditory --
    # Real-time auditory processing preservation. Tonalness, onset, and
    # spectral features are intact even in musical anhedonia.
    # Loui et al. 2017: perception fully intact (N=22).
    auditory_quality = (
        0.35 * tonalness
        + 0.30 * onset
        + 0.35 * centroid
    )

    p1 = torch.sigmoid(
        0.40 * auditory_quality * pleasantness.clamp(min=0.1)
        + 0.30 * spectral_flux * loud_instant
        + 0.30 * pleas_instant * tonalness
    )

    return p0, p1
