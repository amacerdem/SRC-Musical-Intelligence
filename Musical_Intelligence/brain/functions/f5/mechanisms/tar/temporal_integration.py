"""TAR T+I-Layer -- Temporal Integration (6D).

Temporal dynamics for therapeutic modulation and adaptive recommendation:
  T0: arousal_mod_tgt       -- Target arousal modulation level [0, 1]
  T1: valence_mod_tgt       -- Target valence modulation level [0, 1]
  T2: anxiety_reduction     -- Anxiolytic pathway strength [0, 1]
  T3: depression_improv     -- Antidepressant pathway strength [0, 1]
  I0: rec_tempo_norm        -- Recommended tempo (normalized 0=slow, 1=fast) [0, 1]
  I1: rec_consonance        -- Recommended consonance level [0, 1]

Arousal modulation target (T0) tracks the optimal arousal direction from
current state: low arousal music when anxious (high E0), moderate arousal
when depressed. Bernardi 2006: tempo drives cardiovascular response.

Valence modulation target (T1) tracks optimal valence from VMM state:
positive valence needed when valence is low (depression), neutral when
already positive. Juslin 2013: evaluative conditioning pathway.

Anxiety reduction (T2) models the anxiolytic pathway: slow tempo + high
consonance + soft dynamics -> amygdala downregulation + PNS activation.
Koelsch 2014: consonant music reduces amygdala activation.

Depression improvement (T3) models the antidepressant pathway: positive
valence + moderate energy + reward -> striatal DA upregulation.
Chanda 2013: music modulates DA in NAcc.

Recommended tempo (I0) and consonance (I1) provide adaptive targets for
music selection/generation. Lower tempo for anxiety, higher consonance
for both conditions.

H3 demands consumed (8):
  (4, 6, 8, 0)   sensory_pleasantness velocity H6 L0  -- affect velocity
  (4, 16, 2, 0)  sensory_pleasantness std H16 L0      -- mood stability
  (0, 12, 18, 0) roughness trend H12 L0               -- dissonance trajectory
  (0, 15, 18, 0) roughness trend H15 L0               -- sustained dissonance
  (8, 12, 8, 0)  velocity_A velocity H12 L0           -- tempo buildup
  (8, 12, 18, 0) velocity_A trend H12 L0              -- tempo trend
  (10, 6, 0, 2)  loudness value H6 L2                 -- current arousal
  (4, 11, 1, 0)  sensory_pleasantness mean H11 L0     -- cognitive-projection

R3 inputs: roughness[0], sensory_pleasantness[4], velocity_A[8],
           onset_strength[11], warmth[16], spectral_flux[21]

Upstream inputs: VMM.valence_state (idx 11), CLAM.modulation_success (idx 10),
                 SRP.pleasure (idx 15)

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_PLEASANT_VEL_H6 = (4, 6, 8, 0)       # sensory_pleasantness velocity H6 L0
_PLEASANT_STD_H16 = (4, 16, 2, 0)     # sensory_pleasantness std H16 L0
_ROUGH_TREND_H12 = (0, 12, 18, 0)     # roughness trend H12 L0
_ROUGH_TREND_H15 = (0, 15, 18, 0)     # roughness trend H15 L0
_VELOA_VEL_H12 = (8, 12, 8, 0)        # velocity_A velocity H12 L0
_VELOA_TREND_H12 = (8, 12, 18, 0)     # velocity_A trend H12 L0
_LOUD_VAL_H6 = (10, 6, 0, 2)          # loudness value H6 L2
_PLEASANT_MEAN_H11 = (4, 11, 1, 0)    # sensory_pleasantness mean H11 L0

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0
_PLEASANTNESS = 4
_VELOCITY_A = 8
_ONSET = 11
_WARMTH = 16
_SPECTRAL_FLUX = 21


def _anxiolytic_signal(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tensor:
    """Anxiolytic pathway signal: consonance + low arousal + slow tempo.

    Returns (B, T) anxiolytic strength in [0, 1] via sigmoid.
    """
    rough_trend_h12 = h3_features[_ROUGH_TREND_H12]    # (B, T)
    rough_trend_h15 = h3_features[_ROUGH_TREND_H15]    # (B, T)
    loud_val = h3_features[_LOUD_VAL_H6]                # (B, T)
    warmth = r3_features[..., _WARMTH]                  # (B, T)

    # Low roughness trend (consonance improving) + low arousal + warmth
    return torch.sigmoid(
        0.35 * (1.0 - 0.50 * rough_trend_h12 - 0.50 * rough_trend_h15)
        + 0.35 * (1.0 - loud_val)
        + 0.30 * warmth
    )


def _antidepressant_signal(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    pleasure: Tensor,
) -> Tensor:
    """Antidepressant pathway signal: positive valence + moderate energy + DA.

    Returns (B, T) antidepressant strength in [0, 1] via sigmoid.
    """
    pleasant_vel = h3_features[_PLEASANT_VEL_H6]        # (B, T)
    pleasant_mean = h3_features[_PLEASANT_MEAN_H11]      # (B, T)
    onset = r3_features[..., _ONSET]                    # (B, T)

    # Rising pleasantness + sustained hedonic tone + moderate rhythmic
    # engagement + reward (SRP.pleasure)
    return torch.sigmoid(
        0.30 * pleasant_vel
        + 0.25 * pleasant_mean
        + 0.20 * onset
        + 0.25 * pleasure
    )


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor]:
    """Compute T+I-layer: 6D therapeutic modulation and recommendation.

    T0 (arousal_mod_tgt): Target arousal modulation. When therapeutic
    potential (E0) is high and current arousal is high, target low arousal
    (anxiolytic); when E0 is high but arousal is low, target moderate
    arousal (antidepressant). Bernardi 2006: tempo-cardiovascular link.

    T1 (valence_mod_tgt): Target valence modulation from VMM state.
    When current valence is low, target positive valence direction.
    Juslin 2013: evaluative conditioning for valence shift.

    T2 (anxiety_reduction): Anxiolytic pathway -- slow tempo + consonance
    + soft dynamics -> amygdala downregulation. Koelsch 2014: consonant
    music engagement reduces amygdala threat response.

    T3 (depression_improv): Antidepressant pathway -- positive valence +
    moderate energy + reward -> striatal DA. Chanda 2013: DA modulation.

    I0 (rec_tempo_norm): Adaptive tempo recommendation. Lower tempo for
    high anxiety (high anxiolytic need), moderate for depression.

    I1 (rec_consonance): Adaptive consonance recommendation. High
    consonance for both conditions, slightly higher for anxiety.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e: ``(E0,)`` from extraction layer.
        upstream_outputs: ``{"VMM": (B,T,12), "SRP": (B,T,19),
                            "CLAM": (B,T,11), ...}``.

    Returns:
        ``(T0, T1, T2, T3, I0, I1)`` each ``(B, T)``.
    """
    (e0,) = e
    B, T, _ = r3_features.shape
    device = r3_features.device

    # -- H3 features --
    pleasant_std = h3_features[_PLEASANT_STD_H16]        # (B, T)
    veloa_vel_h12 = h3_features[_VELOA_VEL_H12]          # (B, T)
    veloa_trend_h12 = h3_features[_VELOA_TREND_H12]      # (B, T)
    loud_val = h3_features[_LOUD_VAL_H6]                  # (B, T)

    # -- Upstream: VMM.valence_state (C1, idx 11), SRP.pleasure (P2, idx 15),
    #              CLAM.modulation_success (F1, idx 10) --
    vmm = upstream_outputs.get("VMM", torch.zeros(B, T, 12, device=device))
    valence_state = vmm[..., 11]                          # (B, T)
    srp = upstream_outputs.get("SRP", torch.zeros(B, T, 19, device=device))
    pleasure = srp[..., 15]                               # (B, T)
    clam = upstream_outputs.get("CLAM", torch.zeros(B, T, 11, device=device))
    mod_success = clam[..., 10]                           # (B, T)

    # -- Pathway signals --
    anxiolytic = _anxiolytic_signal(h3_features, r3_features)
    antidepressant = _antidepressant_signal(
        h3_features, r3_features, pleasure,
    )

    # -- T0: Arousal Modulation Target --
    # When therapeutic (E0 high): modulate arousal down (anxiolytic) or
    # to moderate (antidepressant). Uses inverse loudness weighted by E0.
    # Bernardi 2006: slow tempo reduces HR, BP, sympathetic activation
    t0 = torch.sigmoid(
        0.40 * e0 * (1.0 - loud_val)
        + 0.30 * anxiolytic
        + 0.30 * (1.0 - pleasant_std)  # mood stability
    )

    # -- T1: Valence Modulation Target --
    # When valence is low (need improvement), target positive direction.
    # sigma(0.40*E0*(1-valence) + 0.30*mod_success + 0.30*antidepressant)
    # Juslin 2013: evaluative conditioning shifts valence
    t1 = torch.sigmoid(
        0.40 * e0 * (1.0 - valence_state)
        + 0.30 * mod_success
        + 0.30 * antidepressant
    )

    # -- T2: Anxiety Reduction --
    # sigma(0.40*anxiolytic*E0 + 0.30*(1-veloa_vel) + 0.30*(1-rough_trend))
    # Product of anxiolytic signal and therapeutic context: slow, consonant,
    # soft music with high therapeutic potential.
    # Koelsch 2014: amygdala downregulation via consonant music
    t2 = torch.sigmoid(
        0.40 * anxiolytic * e0
        + 0.30 * (1.0 - veloa_vel_h12.abs().clamp(0.0, 1.0))
        + 0.30 * mod_success
    )

    # -- T3: Depression Improvement --
    # sigma(0.40*antidepressant*E0 + 0.30*pleasure + 0.30*valence_state)
    # Antidepressant pathway gated by therapeutic context: positive valence
    # music with reward activation drives DA upregulation.
    # Chanda 2013: music modulates DA, serotonin in NAcc
    t3 = torch.sigmoid(
        0.40 * antidepressant * e0
        + 0.30 * pleasure
        + 0.30 * valence_state
    )

    # -- I0: Recommended Tempo (normalized) --
    # Lower when anxiolytic need is high (slow tempo for anxiety);
    # moderate when antidepressant need dominates. Uses tempo trend to
    # track current direction and adjust recommendation.
    # 0 = recommend slow, 1 = recommend fast
    # Bernardi 2006: slow tempo (<80 BPM) for relaxation
    i0 = torch.sigmoid(
        0.35 * (1.0 - anxiolytic)               # low anxiolytic -> faster OK
        + 0.35 * veloa_trend_h12                  # current tempo trajectory
        + 0.30 * antidepressant                   # moderate energy for depression
    )

    # -- I1: Recommended Consonance --
    # High consonance for both conditions; slightly higher for anxiety.
    # Uses dissonance trajectory to track improvement.
    # Koelsch 2014: consonance essential for therapeutic emotion circuits
    rough_trend_h12 = h3_features[_ROUGH_TREND_H12]      # (B, T)
    i1 = torch.sigmoid(
        0.40 * anxiolytic                         # high consonance for anxiety
        + 0.30 * (1.0 - rough_trend_h12)          # improving consonance
        + 0.30 * e0                               # therapeutic context
    )

    return t0, t1, t2, t3, i0, i1
