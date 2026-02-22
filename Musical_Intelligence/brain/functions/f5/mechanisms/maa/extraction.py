"""MAA E-Layer -- Extraction (4D).

Complexity tolerance, familiarity, framing, and appreciation composite:
  E0: complexity_tolerance    -- Goldilocks surface (inverted-U) [0, 1]
  E1: familiarity_index       -- Mere exposure / repetition benefit [0, 1]
  E2: framing_effect          -- Cognitive framing (artistic vs popular) [0, 1]
  E3: appreciation_composite  -- Multiplicative gate: E0 * E1 * E2 [0, 1]

Complexity tolerance (E0) implements the Goldilocks surface: intermediate
complexity (neither too simple nor too chaotic) maximises pleasure. Uses
consonance entropy and coupling entropy as complexity signals, with the
PUPF.goldilocks_zone (idx 6) providing the optimal-complexity reference.
Cheung 2019: NAcc BOLD correlates with subjective pleasure (beta=0.242).

Familiarity index (E1) models mere exposure: repeated listening increases
liking of initially disliked atonal music. Uses coupling trend (trajectory
toward familiar) and mean periodicity/tonalness as familiarity anchors.
VMM.mode_signal (idx 1) provides emotional-mode context.
Gold 2019: 8 repetitions shift preference by d=0.42.

Framing effect (E2) captures cognitive reappraisal: artistic framing
increases appreciation of complex music. Uses immediate consonance and
dissonance percepts weighted by the appreciation pathway (x_l5l7).
Huang 2016: PCC/mPFC/arMFC activation for artistic framing.

Appreciation composite (E3) is multiplicative: all three pathways must
co-activate. If complexity is too extreme, or familiarity is absent, or
framing is negative, appreciation collapses toward zero.

H3 demands consumed (8):
  (4, 16, 20, 0)  sensory_pleasantness entropy H16 L0 -- consonance entropy
  (41, 16, 20, 0) x_l5l7[0] entropy H16 L0            -- coupling entropy
  (41, 16, 18, 0) x_l5l7[0] trend H16 L0              -- coupling trend
  (5, 16, 1, 0)   periodicity mean H16 L0              -- key clarity
  (14, 16, 1, 0)  tonalness mean H16 L0                -- atonality level
  (21, 8, 1, 0)   spectral_change mean H8 L0           -- structural complexity
  (4, 3, 0, 2)    sensory_pleasantness value H3 L2     -- consonance 100ms
  (0, 3, 0, 2)    roughness value H3 L2                -- dissonance 100ms

R3 inputs: roughness[0], sensory_pleasantness[4], periodicity[5],
           tonalness[14], spectral_change[21], x_l5l7[41:49]

Upstream: PUPF[6] (goldilocks_zone), VMM[1] (mode_signal)

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_PLEASANT_ENT_H16 = (4, 16, 20, 0)     # sensory_pleasantness entropy H16 L0
_COUPLING_ENT_H16 = (41, 16, 20, 0)    # x_l5l7[0] entropy H16 L0
_COUPLING_TREND_H16 = (41, 16, 18, 0)  # x_l5l7[0] trend H16 L0
_PERIOD_MEAN_H16 = (5, 16, 1, 0)       # periodicity mean H16 L0
_TONAL_MEAN_H16 = (14, 16, 1, 0)       # tonalness mean H16 L0
_SCHANGE_MEAN_H8 = (21, 8, 1, 0)       # spectral_change mean H8 L0
_PLEASANT_VAL_H3 = (4, 3, 0, 2)        # sensory_pleasantness value H3 L2
_ROUGH_VAL_H3 = (0, 3, 0, 2)           # roughness value H3 L2

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0
_PLEASANTNESS = 4
_PERIODICITY = 5
_TONALNESS = 14
_SPECTRAL_CHANGE = 21
_X_L5L7_START = 41
_X_L5L7_END = 49

# -- Upstream indices ----------------------------------------------------------
_PUPF_GOLDILOCKS = 6    # PUPF.goldilocks_zone (G1)
_VMM_MODE_SIGNAL = 1    # VMM.mode_signal (V1)


def _goldilocks_surface(
    complexity: Tensor,
    reference: Tensor,
) -> Tensor:
    """Inverted-U Goldilocks surface: peak at intermediate complexity.

    Maps complexity to appreciation via Gaussian centred on the reference
    (optimal complexity point from PUPF.goldilocks_zone). Too simple or
    too chaotic both reduce the output.

    Cheung 2019: intermediate uncertainty maximises pleasure.

    Args:
        complexity: (B, T) current complexity estimate [0, 1].
        reference: (B, T) optimal complexity point from PUPF.

    Returns:
        (B, T) in [0, 1] via Gaussian shape.
    """
    # Gaussian centred on reference, width sigma=0.30
    diff = complexity - reference
    return torch.exp(-0.5 * (diff / 0.30) ** 2)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: 4D complexity/familiarity/framing/appreciation.

    E0 (complexity_tolerance): Goldilocks surface -- intermediate
    complexity maximises appreciation. Consonance entropy + coupling
    entropy + structural complexity form the complexity estimate;
    PUPF.goldilocks_zone provides the optimal reference.
    Cheung 2019: NAcc beta=0.242 for uncertainty-pleasure link.

    E1 (familiarity_index): Mere exposure pathway -- coupling trend
    (trajectory toward familiar) and periodicity/tonalness anchors
    weighted by VMM.mode_signal for emotional-mode context.
    Gold 2019: d=0.42 shift after 8 repetitions.

    E2 (framing_effect): Cognitive framing -- immediate consonance
    and dissonance percepts modulated by x_l5l7 appreciation pathway.
    Huang 2016: PCC/mPFC/arMFC activation for artistic framing.

    E3 (appreciation_composite): Multiplicative gate: E0 * E1 * E2.
    All pathways must co-activate for appreciation to emerge.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        upstream_outputs: ``{"PUPF": (B, T, 12), "VMM": (B, T, 12)}``.

    Returns:
        ``(E0, E1, E2, E3)`` each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    pleasant_ent = h3_features[_PLEASANT_ENT_H16]          # (B, T)
    coupling_ent = h3_features[_COUPLING_ENT_H16]          # (B, T)
    coupling_trend = h3_features[_COUPLING_TREND_H16]      # (B, T)
    period_mean = h3_features[_PERIOD_MEAN_H16]            # (B, T)
    tonal_mean = h3_features[_TONAL_MEAN_H16]              # (B, T)
    schange_mean = h3_features[_SCHANGE_MEAN_H8]           # (B, T)
    pleasant_val = h3_features[_PLEASANT_VAL_H3]           # (B, T)
    rough_val = h3_features[_ROUGH_VAL_H3]                 # (B, T)

    # -- R3 features --
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)

    # -- Upstream features --
    pupf = upstream_outputs.get("PUPF", torch.zeros(B, T, 12, device=device))
    vmm = upstream_outputs.get("VMM", torch.zeros(B, T, 12, device=device))
    goldilocks_ref = pupf[..., _PUPF_GOLDILOCKS]           # (B, T)
    mode_signal = vmm[..., _VMM_MODE_SIGNAL]               # (B, T)

    # -- E0: Complexity Tolerance (Goldilocks surface) --
    # Complexity = mean of consonance entropy, coupling entropy, spectral change
    # All in [0, 1] range after sigmoid; Goldilocks surface peaks at reference
    # Cheung 2019: intermediate uncertainty maximises pleasure (NAcc beta=0.242)
    complexity = torch.sigmoid(
        0.35 * pleasant_ent
        + 0.35 * coupling_ent
        + 0.30 * schange_mean
    )
    e0 = _goldilocks_surface(complexity, torch.sigmoid(goldilocks_ref))

    # -- E1: Familiarity Index (mere exposure) --
    # sigma(0.30*coupling_trend + 0.25*periodicity + 0.25*tonalness + 0.20*mode)
    # Coupling trend rising = becoming more familiar; periodicity and tonalness
    # anchor familiarity; VMM mode_signal provides emotional context.
    # Gold 2019: 8 repetitions shift preference d=0.42 for atonal excerpts
    e1 = torch.sigmoid(
        0.30 * coupling_trend
        + 0.25 * period_mean
        + 0.25 * tonal_mean
        + 0.20 * mode_signal
    )

    # -- E2: Framing Effect (cognitive reappraisal) --
    # sigma(0.35*consonance*x_l5l7.mean + 0.35*(1-roughness) + 0.30*x_l5l7.mean)
    # Consonance weighted by appreciation pathway; low roughness enables framing;
    # sustained appreciation pathway provides cognitive context.
    # Huang 2016: PCC/mPFC/arMFC for artistic framing (fMRI, N=21)
    x_l5l7_mean = x_l5l7.mean(dim=-1)                     # (B, T)
    e2 = torch.sigmoid(
        0.35 * pleasant_val * x_l5l7_mean
        + 0.35 * (1.0 - rough_val)
        + 0.30 * x_l5l7_mean
    )

    # -- E3: Appreciation Composite (multiplicative gate) --
    # Product of tolerance, familiarity, and framing: all three must co-activate.
    # Cheung 2019 + Gold 2019 + Huang 2016: appreciation requires complexity
    # tolerance AND familiarity AND cognitive framing.
    e3 = (e0 * e1 * e2).clamp(0.0, 1.0)

    return e0, e1, e2, e3
