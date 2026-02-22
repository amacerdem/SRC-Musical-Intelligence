# IGFE F-Layer — Forecast (2D)

**Layer**: Future Predictions (F)
**Indices**: [7:9]
**Scope**: exported (kernel relay)
**Activation**: sigmoid
**Model**: PCU-γ1 (Individual Gamma Frequency Enhancement, 9D, γ-tier 50-70%)
**Note**: IGFE has NO M-layer. F-layer follows P-layer directly (indices 7-8).

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:memory_enhancement_post | [0, 1] | Post-stimulation word recall prediction. f07 = sigma(0.5*f02 + 0.5*f04). Combines memory enhancement (E1) with dose response (E3). Yokota 2025: word recall improved after IGF-matched stimulation. |
| 8 | F1:executive_improve_post | [0, 1] | Post-stimulation IES reduction prediction. f08 = sigma(0.5*f03 + 0.5*f04). Combines executive enhancement (E2) with dose response (E3). Yokota 2025: IES reduced (faster + more accurate) after gamma stimulation. |

---

## Design Rationale

1. **Memory Enhancement Post (F0)**: Predicts post-stimulation verbal memory improvement. The key insight from Yokota 2025 is that enhancement persists after stimulation ends — this is a forward prediction of how much memory benefit the listener will retain. Equal weighting of memory signal (f02) and dose (f04) reflects that both the quality of IGF match and the duration of exposure contribute equally to lasting benefit.

2. **Executive Improvement Post (F1)**: Predicts post-stimulation executive function improvement (measured as IES reduction = faster responses with fewer errors). Same dose-dependent structure as F0 but uses the executive enhancement signal (f03) instead of memory. This captures the distinct timescale of executive vs memory benefit — executive benefits may emerge sooner but also decay faster.

---

## Mathematical Formulation

```
Enhancement Model:
  Enhancement(f) = Match(f, IGF) * Dose(t) * Intensity

  where:
    Match(f, IGF) = exp(-(f - IGF)^2 / (2 * sigma^2))
    sigma = 5 Hz (Gaussian tuning width)
    IGF in [30, 80] Hz (individual gamma frequency range)
    tau_dose = 300s (dose accumulation time constant)

Memory Prediction:
  F0 = sigma(0.5 * f02_memory + 0.5 * f04_dose)

Executive Prediction:
  F1 = sigma(0.5 * f03_executive + 0.5 * f04_dose)
```

---

## H3 Dependencies (F-Layer)

F-layer is primarily computational from E-layer outputs. Key indirect dependencies:

| E-Layer Source | Feature | Purpose |
|---------------|---------|---------|
| E1 (f02) | memory_enhancement | F0: memory benefit signal |
| E2 (f03) | executive_enhancement | F1: executive benefit signal |
| E3 (f04) | dose_response | F0+F1: dose accumulation |

Additional H3 tuples consumed by the P-layer (gamma synchronization) provide context:
| Tuple | Feature | Purpose |
|-------|---------|---------|
| (5, 3, 1, 2) | periodicity mean H3 L2 | Gamma periodicity stability — prediction confidence |
| (5, 16, 1, 0) | periodicity mean H16 L0 | Sustained gamma — long-term benefit |
| (14, 3, 0, 2) | tonalness value H3 L2 | Tonal context — gamma clarity |
| (14, 16, 1, 0) | tonalness mean H16 L0 | Sustained tonal context |
| (7, 3, 0, 2) | amplitude value H3 L2 | Intensity context at 100ms |

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:memory_enhancement_post | F4 Memory | Predicted memory retrieval benefit |
| F0:memory_enhancement_post | F6 Reward | PE from predicted vs actual recall enhancement |
| F1:executive_improve_post | F3 Attention | Executive attention benefit prediction |
| F1:executive_improve_post | Precision engine | pi_pred for executive function beliefs |

---

## Scientific Foundation

- **Yokota et al. 2025**: IGF-matched stimulation improves word recall AND IES (N=29, within-subjects crossover)
- **Bolland et al. 2025**: Systematic review (k=62) — dose-response relationship confirmed across modalities
- **Dobri et al. 2023**: GABA concentration predicts individual gamma frequency (R²=0.31) — neurochemical basis for individual differences
- **Leeuwis et al. 2021**: Individual gamma frequency predicts cognitive benefit magnitude (R²adj=0.40)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/igfe/forecast.py` (pending)
