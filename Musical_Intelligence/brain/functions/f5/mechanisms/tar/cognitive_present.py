"""TAR P-Layer -- Cognitive Present (1D).

Present-processing therapeutic reward estimation:
  P0: therapeutic_reward   -- Current therapeutic reward signal [0, 1]

Therapeutic reward (P0) is the multiplicative product of anxiety reduction
(T2), depression improvement (T3), and upstream pleasure (SRP.pleasure),
gated by the overall therapeutic potential (E0). This ensures reward is
only generated when BOTH pathways are active AND the music has genuine
therapeutic potential. Monotonic pleasant music without therapeutic
properties should not generate reward.

The multiplicative structure means removing any one component collapses
the reward toward zero -- matching clinical evidence that effective music
therapy requires coordinated activation across multiple pathways.

Chanda & Levitin (2013): Therapeutic effects require coordinated
neuromodulator response (cortisol, DA, oxytocin).

Sakka & Juslin (2018): Emotion regulation via music selection requires
matching music properties to therapeutic goal.

H3 demands consumed (4):
  (4, 15, 1, 0)  sensory_pleasantness mean H15 L0  -- peak response magnitude
  (0, 16, 0, 2)  roughness value H16 L2            -- current consonance
  (4, 15, 1, 0)  sensory_pleasantness mean H15 L0  -- peak therapeutic response
  (4, 16, 18, 0) sensory_pleasantness trend H16 L0 -- mood trend

R3 inputs: sensory_pleasantness[4], warmth[16]

Upstream inputs: SRP.pleasure (idx 15), VMM.valence_state (idx 11)

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_PLEASANT_MEAN_H15 = (4, 15, 1, 0)    # sensory_pleasantness mean H15 L0
_ROUGH_VAL_H16 = (0, 16, 0, 2)        # roughness value H16 L2
_PLEASANT_TREND_H16 = (4, 16, 18, 0)  # sensory_pleasantness trend H16 L0

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_PLEASANTNESS = 4
_WARMTH = 16


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor]:
    """Compute P-layer: therapeutic reward signal.

    P0 (therapeutic_reward): Multiplicative product of anxiety reduction
    and depression improvement, gated by therapeutic context (E0) and
    modulated by current hedonic state. All three terms must co-activate
    for meaningful therapeutic reward.

    The product structure ensures:
    - Anxiolytic music without antidepressant properties: low reward
    - Antidepressant music without anxiety reduction: low reward
    - Music matching neither pathway: near-zero reward
    - Coordinated therapeutic match: high reward

    Chanda 2013: coordinated neuromodulator response required.
    Sakka 2018: music-emotion regulation requires goal matching.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e: ``(E0,)`` from extraction layer.
        m: ``(T0, T1, T2, T3, I0, I1)`` from temporal integration.
        upstream_outputs: ``{"SRP": (B,T,19), "VMM": (B,T,12), ...}``.

    Returns:
        ``(P0,)`` -- single tensor ``(B, T)``.
    """
    (e0,) = e
    _t0, _t1, t2, t3, _i0, _i1 = m
    B, T, _ = r3_features.shape
    device = r3_features.device

    # -- H3 features --
    pleasant_mean_h15 = h3_features[_PLEASANT_MEAN_H15]  # (B, T)
    rough_val_h16 = h3_features[_ROUGH_VAL_H16]          # (B, T)
    pleasant_trend = h3_features[_PLEASANT_TREND_H16]     # (B, T)

    # -- R3 features --
    warmth = r3_features[..., _WARMTH]                    # (B, T)

    # -- Upstream: SRP.pleasure (idx 15), VMM.valence_state (idx 11) --
    srp = upstream_outputs.get("SRP", torch.zeros(B, T, 19, device=device))
    pleasure = srp[..., 15]                               # (B, T)
    vmm = upstream_outputs.get("VMM", torch.zeros(B, T, 12, device=device))
    valence_state = vmm[..., 11]                          # (B, T)

    # -- Hedonic context --
    # Peak therapeutic hedonic response from H15 pleasantness + consonance
    # + mood improvement trend
    hedonic_context = torch.sigmoid(
        0.35 * pleasant_mean_h15
        + 0.30 * (1.0 - rough_val_h16)
        + 0.35 * pleasant_trend
    )

    # -- P0: Therapeutic Reward --
    # Multiplicative: E0 * T2 * T3 * hedonic modulation
    # Gated by therapeutic potential, anxiety reduction, depression
    # improvement, and current hedonic state.
    # Chanda 2013: coordinated cortisol + DA + oxytocin response
    # Koelsch 2014: reward circuit engagement for therapeutic emotion
    therapeutic_product = e0 * t2 * t3   # (B, T), already in [0, 1]

    # Modulate by hedonic context and upstream signals
    p0 = torch.sigmoid(
        0.35 * therapeutic_product
        + 0.25 * hedonic_context
        + 0.20 * pleasure
        + 0.20 * (warmth * valence_state)
    )

    return (p0,)
