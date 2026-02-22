# PNH M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:ratio_complexity | [0, 1] | Normalized log2(n*d) proxy. sigma((roughness + inharmonicity + harmonic_deviation) / 3). Combines three spectral signatures that correlate with Pythagorean ratio complexity. Bidelman & Krishnan 2009: NPS ordering matches log2(n*d); Plomp & Levelt 1965: roughness proportional to ratio complexity. |
| 4 | M1:neural_activation | [0, 1] | Predicted BOLD signal. harmony * ratio_complexity * (1-consonance) * training_level. Estimates the neural activation magnitude across ratio-sensitive ROIs. Sarasso et al. 2019: aesthetic judgment eta_p^2 = 0.685; N1 modulation eta_p^2 = 0.225. |

---

## Design Rationale

1. **Ratio Complexity (M0)**: The core mathematical model. Computes a normalized proxy for log2(n*d) using three R3 features: roughness (critical-band beating), inharmonicity (deviation from harmonic series), and harmonic deviation (partial misalignment). Their average produces a continuous monotonic estimate of Pythagorean ratio complexity without requiring explicit pitch pair detection.

2. **Neural Activation (M1)**: Predicts the BOLD signal magnitude across ratio-sensitive brain regions. Multiplies the harmonic context (current key/chord stability), ratio complexity (how dissonant), inverse consonance (higher activation for dissonance), and training level (expertise modulation). Musicians show stronger activation across 5 ROIs; non-musicians show activation only in R-IFG.

---

## Mathematical Formulation

```
Ratio Complexity:
  Complexity(n:d) = log2(n * d)

R3 Proxy:
  ratio_complexity = sigma((roughness + inharmonicity + harmonic_deviation) / 3)

  Simple ratios -> aligned partials -> low beating -> low roughness
                                    -> low inharmonicity
                                    -> high stumpf_fusion

  Complex ratios -> misaligned partials -> high beating -> high roughness
                                        -> high inharmonicity
                                        -> low stumpf_fusion

Neural Activation:
  BOLD_musician(ratio) = alpha * Complexity(ratio) + epsilon   [5 ROIs]
  BOLD_nonmusician(ratio) = alpha * Complexity(ratio) + epsilon [1 ROI]

  neural_activation = harmony * ratio_complexity * (1-consonance) * training
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 18, 18, 0) | roughness trend H18 L0 | Dissonance trajectory over phrase (2s) |
| (3, 14, 1, 2) | stumpf_fusion mean H14 L2 | Fusion stability over progression (700ms) |
| (4, 10, 0, 2) | sensory_pleasantness value H10 L2 | Current consonance (400ms) |
| (14, 14, 3, 0) | tonalness std H14 L0 | Purity variation over progression (700ms) |
| (6, 14, 0, 0) | harmonic_deviation value H14 L0 | Template mismatch over progression (700ms) |

---

## Scientific Foundation

- **Bidelman & Krishnan 2009**: Brainstem NPS ordering matches Pythagorean hierarchy (brainstem FFR, N=10, r >= 0.81)
- **Plomp & Levelt 1965**: Critical bandwidth theory — roughness proportional to ratio complexity (psychoacoustic)
- **Sarasso et al. 2019**: Consonance drives aesthetic judgment (eta_p^2=0.685) and N1 modulation (eta_p^2=0.225) (EEG+behavioral, N=22)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/pnh/temporal_integration.py`
