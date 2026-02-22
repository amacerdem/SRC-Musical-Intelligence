# PNH M-Layer — Temporal Integration (2D)

**Layer**: Mathematical (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid (M0) / clamp (M1)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:ratio_complexity | [0, 1] | Normalized log2(n*d) proxy. sigma((roughness + inharm + 0.5*harm_dev + 0.5*harm_dev_h14)/3). Multi-feature ratio complexity combining current and progression-level harmonic deviation. |
| 4 | M1:neural_activation | [0, 1] | Predicted BOLD signal. (H0*H1).clamp(0,1). Ratio encoding * conflict = IFG/ACC activation. Bidelman & Krishnan 2009: r>=0.81 brain-behavior correlation. |

---

## Design Rationale

Two computed quantities from harmonic encoding:

1. **Ratio Complexity (M0)**: Combines roughness, inharmonicity, and harmonic deviation (current R3 + progression-level H14) as a multi-dimensional proxy for Pythagorean log2(n*d). Harrison & Pearce 2020: consonance = interference + harmonicity + familiarity. The 0.50 weights on harmonic deviation (current + trend) prevent over-weighting template mismatch.

2. **Neural Activation (M1)**: Product of ratio encoding (H0) and conflict response (H1) predicts the BOLD signal observed by Bidelman & Krishnan. Simple intervals produce low H0 and H1, yielding low M1. Complex intervals produce high H0 and H1, yielding high M1. Clamp rather than sigmoid preserves product dynamics.

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (6, 14, 0, 0) | harmonic_deviation value H14 L0 | Template mismatch at progression level |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 0 | roughness | Sensory dissonance component |
| 5 | inharmonicity | Ratio complexity component |
| 6 | harmonic_deviation | Template mismatch (current) |

---

## Range Analysis

- M0 = sigmoid(~[0, 1]) → ~[0.50, 0.73]
- M1 = sigmoid × sigmoid → [0, 1], typically [0.25, 0.50]

---

## Scientific Foundation

- **Bidelman & Krishnan 2009**: r>=0.81 brain-behavior correlation for ratio complexity
- **Harrison & Pearce 2020**: Consonance = interference + harmonicity + familiarity (3-factor model)
- **Tabas 2019**: POR latency: consonant < dissonant by up to 36ms

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/pnh/temporal_integration.py`
