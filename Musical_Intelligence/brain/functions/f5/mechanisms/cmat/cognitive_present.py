"""CMAT P-Layer -- Cognitive Present (2D).

Present-processing multi-sensory salience and auditory valence contribution:
  P0: multi_sens_salien  -- Multi-sensory salience of current frame [0, 1]
  P1: aud_valence_contr  -- Auditory contribution to cross-modal valence [0, 1]

Multi-sensory salience (P0) captures the degree to which the current
acoustic frame would stand out across multiple sensory channels. Driven
by binding strength (S2), cross-modal transfer potential (E0), and
binding precision from H3 entropy. High salience = strong, congruent
cross-modal event that would capture attention in multimodal context.

Auditory valence contribution (P1) estimates how much the auditory
modality contributes to the overall cross-modal valence. When supramodal
valence (S0) is strong and binding is coherent, auditory features
dominate the cross-modal affective percept. Spence 2011: auditory pitch
drives visual brightness percepts.

H3 demands consumed (1 new):
  (22, 16, 20, 2) distribution_entropy entropy H16 L2 -- binding precision

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/cmat/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_ENTROPY_ENT_H16 = (22, 16, 20, 2)  # distribution_entropy entropy H16 L2

# -- R3 feature indices -------------------------------------------------------
_SPECTRAL_FLUX = 21


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: multi-sensory salience and auditory valence contribution.

    P0 (multi_sens_salien): Multi-sensory salience from cross-modal
    binding (S2) * transfer potential (E0), modulated by binding
    precision (low entropy = high precision). High when acoustic event
    would be salient across multiple sensory channels.
    Spence 2011: congruent cross-modal events capture attention.

    P1 (aud_valence_contr): Auditory modality's contribution to
    overall cross-modal valence. Supramodal valence (S0) weighted by
    temporal binding coherence (T0) and spectral flux (event change).
    When stable and coherent, auditory features strongly drive
    cross-modal affect.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e: ``(E0,)`` from extraction layer.
        m: ``(S0, S1, S2, T0, T1)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    (e0,) = e
    s0, _s1, s2, t0, _t1 = m

    # -- H3 features --
    entropy_ent = h3_features[_ENTROPY_ENT_H16]           # (B, T)

    # -- R3 features --
    spectral_flux = r3_features[..., _SPECTRAL_FLUX]      # (B, T)

    # -- Binding precision --
    # Low entropy = high precision in cross-modal binding
    binding_precision = 1.0 - entropy_ent                  # (B, T)

    # -- P0: Multi-Sensory Salience --
    # Product of cross-modal binding * transfer potential, gated by
    # binding precision. An acoustic event is multi-sensorially salient
    # when it has strong cross-modal correspondences AND those
    # correspondences are precise (low entropy).
    # Spence 2011: congruent correspondences enhance perceptual salience
    p0 = torch.sigmoid(
        0.35 * s2 * e0
        + 0.30 * binding_precision
        + 0.20 * spectral_flux
        + 0.15 * t0
    )

    # -- P1: Auditory Valence Contribution --
    # How much the auditory channel drives cross-modal affect.
    # When supramodal valence is strong AND binding is temporally
    # coherent, auditory features dominate cross-modal percept.
    # Spence 2011: auditory pitch drives visual brightness percepts
    p1 = torch.sigmoid(
        0.40 * s0 * t0
        + 0.30 * e0
        + 0.30 * binding_precision
    )

    return p0, p1
