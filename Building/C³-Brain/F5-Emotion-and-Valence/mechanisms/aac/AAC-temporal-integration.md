# AAC Temporal Integration — Integration Composites (2D)

**Layer**: Temporal Integration (I)
**Indices**: [7:9]
**Scope**: exported (kernel relay: chills_intensity)
**Activation**: clamp [0, 1] / tanh (ans_composite)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | I0:chills_intensity | [0, 1] | CI = 0.35*SCR + 0.40*(1-HR) + 0.25*RespR. Salimpoor 2011 weights reconstructed from correlation data. Peaks at chill moments. HR INVERTED because HR DECREASES at peaks (vagal brake). Not sigmoid-wrapped — inputs already [0,1]. |
| 8 | I1:ans_composite | [-1, 1] | Standardized multi-modal ANS score. f08 = tanh(mean(z_score(scr), z_score(hr), z_score(respr), z_score(bvp), z_score(temp))). +1 = maximal sympathetic arousal. Complementary to CI — equal-weight PCA-like approach. |

---

## Design Rationale

1. **Chills Intensity (I0)**: The signature physiological marker of peak musical emotion. Combines the three most reliable ANS markers with weights derived from meta-analytic effect sizes: HR has the highest weight (0.40) because the vagal brake is the strongest and most consistent marker (d=1.0-1.5, Fancourt 2020). SCR is second (0.35, d=0.85) as the purely sympathetic channel. RespR is third (0.25, d=0.45) as the arousal-driven respiratory component. The paradoxical co-activation (SCR up + HR down simultaneously) places chills in Berntson's co-activation quadrant. Peng 2022 definitively proved cardiac-level co-activation (PEP shortened + RSA increased).

2. **ANS Composite (I1)**: A complementary integration using z-scored equal-weight averaging of all five ANS channels. This captures the overall autonomic state without privileging any single marker. Positive values indicate net sympathetic activation; negative values indicate parasympathetic dominance. Useful for tracking tonic arousal level across the piece, while CI is tuned for phasic peak detection.

---

## Mathematical Formulation

```
Chills Intensity (Salimpoor 2011 reconstruction):
  CI = w1 * SCR + w2 * (1 - HR) + w3 * RespR
  w1 = 0.35 (SCR weight — purely sympathetic, d=0.85)
  w2 = 0.40 (HR weight — inverted vagal brake, d=1.0-1.5)
  w3 = 0.25 (RespR weight — arousal-driven, d=0.45)

  Note: HR is INVERTED (1-HR) because HR DECREASES at peaks.
  CI in [0, 1] when inputs are normalized.

ANS Composite (equal-weight standardized):
  ans_composite = tanh(mean(z(SCR), z(HR), z(RespR), z(BVP), z(Temp)))
  z(x) = (x - mu_running) / (sigma_running + epsilon)
```

---

## The Co-Activation Paradox

```
BERNTSON AUTONOMIC SPACE (1991):

                    Sympathetic HIGH
                         |
         RECIPROCAL      |      CO-ACTIVATION
         (classical)     |      <<<< CHILLS >>>>
                         |
  Parasympathetic  ------+------  Parasympathetic
  LOW                    |         HIGH
                         |
         CO-INHIBITION   |      RECIPROCAL
                         |      (inverse)
                         |
                    Sympathetic LOW

At chills: SCR up (sympathetic) AND HR down (parasympathetic)
         = CO-ACTIVATION quadrant

Peng 2022 proof: PEP shortened (sympathetic cardiac)
                + RSA increased (parasympathetic cardiac)
                = CARDIAC-LEVEL co-activation (not just peripheral)
```

---

## H3 Dependencies (Temporal Integration)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| — | — | I-layer computes from A-layer outputs (no direct H3 reads) |

I-layer is a pure mathematical combination of the five autonomic markers computed in the A-layer. All H3 dependencies flow through the E+A extraction layer.

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| — | — | I-layer reads from E+A layer outputs only |

---

## Scientific Foundation

- **Salimpoor 2011**: Chills intensity correlates with ANS composite (d=0.71), DA release in NAcc and caudate (PET, N=8)
- **Fancourt 2020**: Meta-pooled effect sizes: SCR d=0.85, HR d=0.8-1.5, RespR d=0.45 (meta-analysis, k=26)
- **Peng 2022**: PEP shortened d=-0.45 + RSA increased d=+0.38 simultaneously = definitive cardiac co-activation (impedance cardiography)
- **Berntson 1991**: 2D autonomic space model — co-activation, co-inhibition, and reciprocal modes (Psychophysiology)
- **de Fleurian & Pearce 2021**: 55-90% prevalence of musical chills, piloerection in ~50% of episodes (systematic review, k=116)
- **Mori & Iwanaga 2017**: Two chill subtypes — "cold chill" (goosebumps, SCR up) vs "warm thrill" (tears, HR down) (N=43)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/aac/temporal_integration.py`
