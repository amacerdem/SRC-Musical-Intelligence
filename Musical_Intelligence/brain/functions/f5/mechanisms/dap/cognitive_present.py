"""DAP P-Layer -- Cognitive Present (3D).

Present-moment affective processing shaped by developmental plasticity:
  P0: current_affect       -- Current affective response strength [0, 1]
  P1: familiarity_warmth   -- Familiarity-driven warmth/comfort [0, 1]
  P2: learning_rate        -- Current affective learning rate [0, 1]

Current affect (P0) captures the real-time emotional response to music,
modulated by developmental sensitivity (E0) and MEAMN memory state.
Music that resonates with early-formed templates produces stronger
affective responses. Koelsch 2014: music-evoked emotions via
auditory cortex -> amygdala -> hippocampus pathway.

Familiarity warmth (P1) estimates the comfort/warmth arising from
recognition of developmentally familiar musical patterns. High when
exposure history (D2) and critical period alignment (D0) converge with
low roughness (consonant, familiar sound). Pereira et al. 2011:
Familiar music activates hippocampus and mPFC.

Learning rate (P2) estimates the current capacity for new affective
associations. High when plasticity coefficient (D1) is elevated and
neural maturation (D3) supports new learning. Declines as maturation
saturates. Trainor 2005: declining plasticity after critical period.

H3 demands consumed: None new (uses E-layer and D-layer outputs).

R3 inputs: roughness[0], sensory_pleasantness[4], entropy[22]

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/dap/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0
_PLEASANTNESS = 4
_ENTROPY = 22

# -- MEAMN upstream index ------------------------------------------------------
_MEAMN_MEMORY_STATE_IDX = 5  # P0:memory_state in MEAMN 12D output


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: current affect, familiarity warmth, learning rate.

    P0 (current_affect): Real-time emotional response weighted by
    developmental sensitivity and hedonic signal. Stronger when
    music matches early-formed templates.
    Koelsch 2014: auditory cortex -> amygdala -> hippocampus.

    P1 (familiarity_warmth): Comfort from recognising developmentally
    familiar patterns. Product of exposure history (D2) and critical
    period (D0) with consonance weighting.
    Pereira et al. 2011: familiar music -> hippocampus + mPFC.

    P2 (learning_rate): Current capacity for new affective learning.
    Plasticity coefficient (D1) gated by neural maturation (D3).
    Trainor 2005: declining plasticity post-critical period.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e_outputs: ``(E0,)`` from extraction layer.
        m_outputs: ``(D0, D1, D2, D3)`` from temporal integration layer.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    (e0,) = e_outputs
    d0, d1, d2, d3 = m_outputs

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]           # (B, T)
    pleasantness = r3_features[..., _PLEASANTNESS]     # (B, T)
    entropy = r3_features[..., _ENTROPY]               # (B, T)

    # -- P0: Current Affect --
    # sigma(0.30*e0 + 0.30*pleasant + 0.20*(1-rough) + 0.20*(1-entropy))
    # Koelsch 2014: music-evoked emotion via auditory-limbic pathway
    # Developmental sensitivity (E0) amplifies response to familiar timbres
    p0 = torch.sigmoid(
        0.30 * e0
        + 0.30 * pleasantness
        + 0.20 * (1.0 - roughness)
        + 0.20 * (1.0 - entropy)
    )

    # -- P1: Familiarity Warmth --
    # sigma(0.35*d2 + 0.35*d0 + 0.30*(1-rough))
    # Pereira et al. 2011: familiar music activates hippocampus + mPFC
    # Exposure history (D2) x critical period (D0) = recognition warmth
    p1 = torch.sigmoid(
        0.35 * d2
        + 0.35 * d0
        + 0.30 * (1.0 - roughness)
    )

    # -- P2: Learning Rate --
    # sigma(0.40*d1 + 0.30*d3 + 0.30*(1-d2))
    # Trainor 2005: plasticity declines after critical period
    # High plasticity (D1) + maturation (D3) - exposure saturation (1-D2)
    p2 = torch.sigmoid(
        0.40 * d1
        + 0.30 * d3
        + 0.30 * (1.0 - d2)
    )

    return p0, p1, p2
