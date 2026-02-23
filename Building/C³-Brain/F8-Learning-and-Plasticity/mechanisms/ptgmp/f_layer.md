# PTGMP — Forecast

**Model**: Piano Training Grey Matter Plasticity
**Unit**: STU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | skill_trajectory | Predicted motor improvement direction. σ(0.60 × x_l5l7_trend_H20 + 0.40 × x_l4l5_mean_H20). Long-range structural coupling trend indicates whether skill is improving, plateauing, or declining. Positive trend = continued skill growth. |
| 8 | timing_improvement | Predicted timing precision improvement. σ(0.50 × x_l4l5_autocorr_H20 + 0.50 × f02_cerebellar_plast). Autocorrelation-based repetition learning — high self-similarity in dynamics coupling indicates systematic practice → timing precision improves. |
| 9 | adaptation_rate | Rate of practice-level adaptation. σ(0.40 × x_l0l5_mean_H20 + 0.30 × x_l5l7_trend_H20 + 0.30 × plasticity_index). Combines long-range motor coupling mean, structural trend, and overall plasticity. High when practice engagement is sustained and plasticity pathways are active. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 20 | M1 (mean) | L0 | Long-term motor coupling mean |
| 1 | 25 | 20 | M19 (stability) | L0 | Practice-level stability |
| 2 | 33 | 20 | M1 (mean) | L0 | Audio-motor integration mean |
| 3 | 33 | 20 | M22 (autocorr) | L0 | Repetition-based learning |
| 4 | 41 | 20 | M1 (mean) | L0 | Structural coupling mean |
| 5 | 41 | 20 | M18 (trend) | L0 | Skill improvement trend |

---

## Computation

The F-layer generates predictions about upcoming motor skill development:

1. **Skill trajectory** (idx 7): Long-range structural coupling trend (x_l5l7 at H20) weighted 60% + dynamics coupling mean weighted 40%. The x_l5l7 trend captures whether the structural coordination pattern is improving over the section timescale (5000ms). Coefficient sum: 0.60 + 0.40 = 1.0.

2. **Timing improvement** (idx 8): Repetition-based learning signal from x_l4l5 autocorrelation (systematic practice patterns) + cerebellar plasticity (E-layer f02). When dynamics coupling shows high self-similarity AND cerebellar plasticity is active → timing precision improvement predicted. Coefficient sum: 0.50 + 0.50 = 1.0.

3. **Adaptation rate** (idx 9): Combines three signals: motor coupling strength (mean), structural trend, and plasticity index (M-layer). Captures the overall rate at which the system adapts to practice demands. Higher when all three pathways are engaged. Coefficient sum: 0.40 + 0.30 + 0.30 = 1.0.

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f02_cerebellar_plast | Timing improvement input |
| M-layer | plasticity_index | Adaptation rate input |
| H³ | 6 tuples (see above) | Long-context features at H20 |
