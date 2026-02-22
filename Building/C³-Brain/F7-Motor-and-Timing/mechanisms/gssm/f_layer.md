# GSSM — Forecast

**Model**: Gait-Synchronized Stimulation Model
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: F — Forecast
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 9 | cv_pred_30min | CV prediction with 30-minute persistence. Predicts stride variability level persisting after stimulation cessation. σ(0.5 * f08 + 0.5 * coupling_periodicity_1s). Yamashita 2025: stimulation effects persist post-session; Sansare 2025: cerebellar iTBS reduced postural sway for >= 30 min in healthy older adults. |
| 10 | balance_pred | Balance score prediction. Predicts future balance performance from current gait stability. σ(0.5 * f09 + 0.5 * gait_stability). Yamashita 2025: Mini-BESTest improvement d = 1.05 correlated with CV reduction; 15-session protocol showed cumulative benefit with walking speed increase at session 15 vs session 1 (p = 0.002). |

---

## H³ Demands

No additional H³ demands beyond those already consumed by E, M, and P layers. The F-layer reuses:
- coupling_periodicity_1s from (25, 16, 14, 2)

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No unique H³ demands; reuses E/M/P layer tuples |

---

## Computation

The F-layer generates predictions about therapeutic outcomes:

1. **CV prediction 30min** (idx 9): Predicts the persistence of stride variability reduction 30 minutes after stimulation ends. Combines the current CV reduction level (f08) with coupling periodicity at 1s to estimate how well the gait pattern will maintain its improved variability. Sansare 2025 provides the time course evidence: cerebellar iTBS effects persisted for at least 30 minutes. Yamashita 2025 showed cumulative effects across 15 sessions. The 0.5/0.5 weighting reflects equal contribution of current therapeutic state and ongoing coupling strength.

2. **Balance prediction** (idx 10): Predicts future balance performance by combining the current balance improvement (f09) with overall gait stability (M-layer). The CV-balance correlation (r = 0.62, p = 0.012 from Yamashita 2025) justifies using gait stability as a balance predictor. This longer-horizon forecast captures the dose-response relationship where more sessions accumulate greater benefit, and current gait quality predicts future balance outcomes.

Both outputs are sigmoid-bounded to [0, 1] and represent confidence in future therapeutic outcomes.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f08_cv_reduction | Current CV reduction feeds persistence prediction |
| E-layer | f09_balance_improvement | Current balance feeds outcome prediction |
| M-layer | gait_stability | Overall stability feeds balance prediction |
| H³ (shared) | coupling_periodicity_1s | Coupling strength for persistence estimation |
