# PTGMP — Temporal Integration

**Model**: Piano Training Grey Matter Plasticity
**Unit**: STU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | plasticity_index | Overall structural plasticity signal. Effect-size-weighted sum: (0.34×f01 + 0.34×f02 + 0.27×f03) / (0.34+0.34+0.27). Weighting reflects reported effect sizes from Espinosa 2025 SR: DLPFC d=0.34, cerebellum d=0.34, theta d=0.27. Range [0, 1]. |
| 4 | age_resilience | Late-life plasticity preservation factor. σ(0.50 × loudness_stability_H14 × coupling_stability_H20). Stability of performance intensity and long-range motor coupling. High stability = consistent practice engagement → age-resilient plasticity maintained. Espinosa 2025: older adults show comparable GMV increases to younger trainees. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 8 | 14 | M19 (stability) | L0 | Loudness performance consistency |
| 1 | 25 | 20 | M19 (stability) | L0 | Practice-level motor coupling stability |

---

## Computation

The M-layer integrates E-layer features into two consolidated plasticity metrics:

1. **Plasticity index** (idx 3): Weighted average using study-reported effect sizes as weights. DLPFC and cerebellum contribute equally (d=0.34 each) while frontal theta has slightly lower weight (d=0.27). This produces a single plasticity signal that reflects the relative contribution of each pathway.

2. **Age resilience** (idx 4): Product of loudness stability (performance consistency at H14) and coupling stability (practice-level at H20). When both are high, the system maintains consistent engagement → structural plasticity occurs regardless of age. Sigmoid-bounded with coefficient 0.50.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01, f02, f03 | Three plasticity pathway signals |
| H³ | 2 tuples (see above) | Stability features at H14/H20 |
| R³ [8] | loudness | Performance consistency |
| R³ [25] | x_l0l5[0] | Motor coupling stability |
