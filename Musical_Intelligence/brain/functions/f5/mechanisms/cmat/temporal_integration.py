"""CMAT S+T Layer -- Temporal Integration (5D).

Supramodal representations and temporal binding dynamics:
  S0: supramodal_valence   -- Valence that generalizes across modalities [0, 1]
  S1: supramodal_arousal   -- Arousal that generalizes across modalities [0, 1]
  S2: cross_modal_bind     -- Binding strength between modalities [0, 1]
  T0: binding_temporal     -- Temporal coherence of cross-modal binding [0, 1]
  T1: congruence_streng    -- Congruence strength of modal correspondences [0, 1]

Supramodal valence (S0) captures the amodal affective valence that
transfers across sensory channels. Derived from VMM.valence_state
integrated with pleasantness trajectory. Spence 2011: pitch-brightness
systematic correspondence implies shared valence representation.

Supramodal arousal (S1) captures the amodal arousal level driven by
tempo/loudness dynamics. AAC.emotional_arousal provides direct arousal
context. Collier & Hubbard 2001: tempo-arousal r=0.68 (N=60).

Cross-modal binding (S2) estimates how tightly auditory features bind
to estimated visual/tactile correspondences. High binding when
pitch-brightness AND mode-warmth are both congruent.

Binding temporal (T0) tracks temporal coherence of the cross-modal
binding over 500ms integration window. Stable binding = reliable
cross-modal transfer.

Congruence strength (T1) measures how well the current stimulus
features align with expected cross-modal correspondences (high pitch
+ bright, low pitch + dark, etc.).

H3 demands consumed (3):
  (4, 6, 8, 0)  sensory_pleasantness velocity H6 L0  -- affect velocity
  (4, 11, 1, 0) sensory_pleasantness mean H11 L0     -- integration state
  (4, 11, 2, 0) sensory_pleasantness std H11 L0      -- integration variability

R3 inputs: roughness[0], sensory_pleasantness[4], loudness[10],
           brightness[15], warmth[16], x_l0l5[25:33]

Upstream: VMM.valence_state (idx 11 of 12D), AAC.emotional_arousal (idx 0 of 14D)

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/cmat/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_PLEAS_VEL_H6 = (4, 6, 8, 0)       # sensory_pleasantness velocity H6 L0
_PLEAS_MEAN_H11 = (4, 11, 1, 0)    # sensory_pleasantness mean H11 L0
_PLEAS_STD_H11 = (4, 11, 2, 0)     # sensory_pleasantness std H11 L0

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0
_PLEASANTNESS = 4
_LOUDNESS = 10
_BRIGHTNESS = 15
_WARMTH = 16
_X_L0L5_START = 25
_X_L0L5_END = 33

# -- Upstream dimension indices ------------------------------------------------
_VMM_VALENCE_STATE = 11  # VMM output idx 11 = valence_state (of 12D)
_AAC_EMOTIONAL_AROUSAL = 0  # AAC output idx 0 = emotional_arousal (of 14D)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    """Compute S+T layer: 5D supramodal representation and temporal binding.

    S0 (supramodal_valence): Amodal valence from VMM valence context
    integrated with H3 pleasantness trajectory. Represents valence that
    would transfer to visual brightness/warmth.
    Spence 2011: systematic cross-modal valence correspondences.

    S1 (supramodal_arousal): Amodal arousal from AAC arousal context
    and loudness dynamics. Represents arousal that maps to tempo-visual
    motion correspondences.
    Collier & Hubbard 2001: tempo-arousal r=0.68 (N=60).

    S2 (cross_modal_bind): Binding strength from convergence of
    pitch-brightness and mode-warmth pathways. High when both are
    congruent.
    Spence 2011: congruent cross-modal pairs facilitate processing.

    T0 (binding_temporal): Temporal coherence of binding from affect
    velocity (H3) modulated by integration state. Stable binding =
    reliable transfer.

    T1 (congruence_streng): Alignment between acoustic features and
    expected cross-modal correspondences. Low pleasantness-std =
    stable mapping = high congruence.
    Palmer et al. 2013: emotion mediates music-color associations.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e: ``(E0,)`` from extraction layer.
        upstream_outputs: ``{"VMM": (B, T, 12), "AAC": (B, T, 14)}``.

    Returns:
        ``(S0, S1, S2, T0, T1)`` each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    (e0,) = e

    # -- H3 features --
    pleas_vel = h3_features[_PLEAS_VEL_H6]              # (B, T)
    pleas_mean = h3_features[_PLEAS_MEAN_H11]            # (B, T)
    pleas_std = h3_features[_PLEAS_STD_H11]              # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]              # (B, T)
    brightness = r3_features[..., _BRIGHTNESS]            # (B, T)
    warmth = r3_features[..., _WARMTH]                    # (B, T)
    loudness = r3_features[..., _LOUDNESS]                # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)

    # -- Upstream reads --
    vmm = upstream_outputs.get("VMM", torch.zeros(B, T, 12, device=device))
    aac = upstream_outputs.get("AAC", torch.zeros(B, T, 14, device=device))
    valence_state = vmm[..., _VMM_VALENCE_STATE]          # (B, T)
    emotional_arousal = aac[..., _AAC_EMOTIONAL_AROUSAL]   # (B, T)

    # -- Derived signals --
    consonance = 1.0 - roughness                          # (B, T)
    binding_substrate = x_l0l5.mean(dim=-1)               # (B, T)

    # -- S0: Supramodal Valence --
    # Amodal valence representation that transfers across modalities.
    # Weighted by VMM valence context and H3 pleasantness integration.
    # Spence 2011: pitch-brightness mapping implies shared valence space
    s0 = torch.sigmoid(
        0.35 * valence_state
        + 0.30 * pleas_mean
        + 0.20 * consonance
        + 0.15 * warmth
    )

    # -- S1: Supramodal Arousal --
    # Amodal arousal from AAC arousal + loudness dynamics.
    # Collier & Hubbard 2001: tempo-arousal r=0.68
    s1 = torch.sigmoid(
        0.35 * emotional_arousal
        + 0.30 * loudness
        + 0.20 * pleas_vel.abs()
        + 0.15 * e0
    )

    # -- S2: Cross-Modal Binding --
    # Convergence of pitch-brightness and mode-warmth pathways.
    # High when brightness correlates with consonance AND warmth
    # correlates with valence (congruent mappings).
    # Spence 2011: congruent pairs facilitate processing
    pitch_bright = brightness * consonance                 # (B, T)
    mode_warm = warmth * valence_state                     # (B, T)
    s2 = torch.sigmoid(
        0.35 * pitch_bright
        + 0.35 * mode_warm
        + 0.30 * binding_substrate
    )

    # -- T0: Binding Temporal --
    # Temporal coherence: stable affect velocity + stable integration
    # state = reliable cross-modal transfer. Fast changes reduce
    # binding coherence.
    t0 = torch.sigmoid(
        0.40 * pleas_mean
        + 0.30 * (1.0 - pleas_vel.abs())
        + 0.30 * binding_substrate
    )

    # -- T1: Congruence Strength --
    # How well stimulus aligns with expected correspondences.
    # Low variability (std) = stable mapping = high congruence.
    # Palmer et al. 2013: emotion mediates music-color association
    t1 = torch.sigmoid(
        0.35 * s0
        + 0.35 * (1.0 - pleas_std)
        + 0.30 * e0
    )

    return s0, s1, s2, t0, t1
