"""OII P-Layer -- Cognitive Present (3D).

Three explicit features modeling present-time oscillatory states:

  P0: integration_state  -- Current theta/alpha integration level [0, 1]
  P1: segregation_state  -- Current gamma segregation level [0, 1]
  P2: encoding_quality   -- Pattern encoding success (integration result) [0, 1]

H3 consumed:
    (14, 16, 0, 2) tonalness value H16 L2             -- harmonic integration at 1s
    (14, 20, 1, 0) tonalness mean H20 L0              -- tonal stability over 5s
    (4, 16, 0, 2)  sensory_pleasantness value H16 L2  -- encoding reward at 1s
    (4, 20, 18, 0) sensory_pleasantness trend H20 L0  -- pleasantness trajectory 5s
    (0, 16, 0, 2)  roughness value H16 L2             -- gamma-band demand at 1s
    (10, 16, 0, 2) loudness value H16 L2              -- oscillatory drive at 1s
    (10, 20, 1, 0) loudness mean H20 L0               -- average drive over 5s

R3 consumed:
    [0]  roughness             -- P1: gamma-band demand proxy
    [4]  sensory_pleasantness  -- P2: encoding reward signal
    [14] tonalness             -- P0: harmonic integration measure
    [10] loudness              -- P0+P2: oscillatory drive / arousal
    [22] entropy               -- P1: integration demand (high=segregation)

Reads: PMIM, MEAMN, MSPBA via relay_outputs (graceful fallback).

See Building/C3-Brain/F4-Memory-Systems/mechanisms/oii/OII-cognitive-present.md
Biau et al. 2025: theta oscillations track audiovisual integration (MEG N=23).
Dobri et al. 2023: 40-Hz gamma ASSR correlates with hearing abilities (MEG).
Borderie et al. 2024: theta-gamma PAC supports auditory STM (iEEG).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_TONAL_VAL_H16 = (14, 16, 0, 2)         # tonalness value H16 L2
_TONAL_MEAN_H20 = (14, 20, 1, 0)        # tonalness mean H20 L0
_PLEAS_VAL_H16 = (4, 16, 0, 2)          # sensory_pleasantness value H16 L2
_PLEAS_TREND_H20 = (4, 20, 18, 0)       # sensory_pleasantness trend H20 L0
_ROUGH_VAL_H16 = (0, 16, 0, 2)          # roughness value H16 L2
_LOUD_VAL_H16 = (10, 16, 0, 2)          # loudness value H16 L2
_LOUD_MEAN_H20 = (10, 20, 1, 0)         # loudness mean H20 L0

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 10
_TONALNESS = 14
_ENTROPY = 22


def _relay_field(
    relay_outputs: Dict[str, Tensor],
    name: str,
    idx: int,
    shape_ref: Tensor,
) -> Tensor:
    """Gracefully extract a single field from an upstream relay."""
    relay = relay_outputs.get(name)
    if relay is None:
        return torch.zeros_like(shape_ref)
    return relay[..., idx]


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: present-time oscillatory integration states.

    P0 (integration_state) captures the current level of theta/alpha
    binding.  Uses harmonic syntax from upstream synthesis and tonalness
    at H16 (1s working memory window).  When high, the brain is in binding
    mode -- distributed features across frontal-temporal networks are being
    unified into a coherent percept.

    P1 (segregation_state) captures the current level of gamma-band local
    processing.  Uses roughness (unresolved harmonics demanding fine-grained
    spectral analysis) and entropy (complex local structure requiring
    segregated processing).  Excessive gamma synchrony can be detrimental
    (Dobri 2023).

    P2 (encoding_quality) captures how successfully the current input has
    been integrated and bound for memory encoding.  Uses pleasantness at
    H16 (encoding facilitated by pleasant stimuli) and integration-memory
    binding quality.  Maps to hippocampal theta-gamma coupling.

    Biau et al. 2025: MEG N=23, theta oscillations track audiovisual
    integration and replay of speech memories.
    Dobri et al. 2023: MEG, 40-Hz gamma ASSR correlates with hearing
    abilities and left auditory cortex GABA; excessive gamma = detrimental.
    Borderie et al. 2024: iEEG, theta-gamma PAC in hippocampus supports
    auditory STM; PAC strength predicts correct recall.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        relay_outputs: Upstream mechanism outputs (PMIM, MEAMN, MSPBA, etc.).

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    e0, _e1, _e2 = e
    m0, _m1 = m

    # -- H3 features --
    tonal_h16 = h3_features[_TONAL_VAL_H16]           # (B, T)
    tonal_h20 = h3_features[_TONAL_MEAN_H20]          # (B, T)
    pleas_h16 = h3_features[_PLEAS_VAL_H16]           # (B, T)
    pleas_trend_h20 = h3_features[_PLEAS_TREND_H20]   # (B, T)
    rough_h16 = h3_features[_ROUGH_VAL_H16]           # (B, T)
    loud_h16 = h3_features[_LOUD_VAL_H16]             # (B, T)
    loud_h20 = h3_features[_LOUD_MEAN_H20]            # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]           # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    loudness = r3_features[..., _LOUDNESS]             # (B, T)
    tonalness = r3_features[..., _TONALNESS]           # (B, T)
    entropy = r3_features[..., _ENTROPY]               # (B, T)

    # -- Upstream relay signals (graceful fallback) --
    # PMIM synthesis quality for harmonic syntax proxy
    syntax_proxy = _relay_field(relay_outputs, "PMIM", 0, roughness)
    # MEAMN memory state for encoding context
    memory_proxy = _relay_field(relay_outputs, "MEAMN", 0, roughness)

    # -- P0: Integration State --
    # Current theta/alpha integration level.
    # sigma(0.30 * syntax.mean + 0.20 * tonalness_h16).
    # Biau et al. 2025: theta oscillations track integration.
    p0 = torch.sigmoid(
        0.30 * (syntax_proxy + tonalness) / 2.0
        + 0.20 * tonal_h16
    )

    # -- P1: Segregation State --
    # Current gamma segregation level.
    # sigma(0.25 * roughness + 0.25 * entropy).
    # Dobri et al. 2023: gamma ASSR correlates with hearing abilities.
    p1 = torch.sigmoid(
        0.25 * roughness
        + 0.25 * entropy
    )

    # -- P2: Encoding Quality --
    # Pattern encoding success (integration result).
    # sigma(0.25 * pleasantness_h16 + 0.25 * integration_binding).
    # Borderie et al. 2024: theta-gamma PAC supports auditory STM.
    p2 = torch.sigmoid(
        0.25 * pleas_h16
        + 0.25 * (e0 * m0 + memory_proxy) / 2.0
    )

    return p0, p1, p2
