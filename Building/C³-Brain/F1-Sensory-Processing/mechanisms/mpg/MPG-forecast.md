# MPG F-Layer — Forecast (1D)

**Layer**: Forecast (F)
**Indices**: [9:10]
**Scope**: external
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|------------------|
| 9 | F0:phrase_boundary_pred | [0, 1] | Phrase boundary prediction. σ(0.30×pitch_trend + 0.25×(1−onset_periodicity) + 0.25×P1 + 0.20×(1−beat_periodicity)) |

---

## Design Rationale

Phrase boundaries are predicted when:
1. **Pitch contour direction changes** — pitch_height trend shifts
2. **Onset periodicity breaks** — regular note timing disrupted
3. **Rhythmic structure shifts** — beat_strength periodicity changes
4. **Contour activity is high** — anterior processing indicates melodic complexity

The inverted periodicity terms (1−periodicity) ensure that boundary predictions
fire when regularity BREAKS, not when it holds.

---

## H³ Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (37, 4, 18, 2) | pitch_height trend ~125ms | Contour direction change |
| (11, 16, 14, 2) | onset periodicity ~1s | Rhythmic regularity (inverted) |
| (42, 3, 14, 2) | beat_strength periodicity | Metric structure (inverted) |

---

## Relay Consumption

```
MPG Relay Wrapper (kernel)
└── phrase_boundary_pred (F0, idx 9) → STU (phrase segmentation)
```

---

## Scientific Foundation

- **Cheung 2019**: AC uncertainty×surprise interaction for harmonic sequences (fMRI, n=40)
- **Samiee 2022**: Delta coherence tracks pitch change (MEG+EEG, n=16)

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/mpg/forecast.py`
