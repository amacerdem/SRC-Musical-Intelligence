# MPFS — Forecast

**Model**: Musical Prodigy Flow State
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: F — Forecast
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 8 | flow_sustain_predict | Flow sustainability prediction. Will flow continue in the next window? Based on current flow propensity, loudness trend, and groove smoothness at bar level (H16). Positive trend with smooth groove and high current flow predict flow continuation. Salimpoor 2011: caudate anticipation r=0.71. Formula: σ(0.40 × f03 + 0.30 × loudness_trend + 0.30 × groove_smooth). |
| 9 | flow_disrupt_risk | Flow disruption risk. High = challenge may exceed skill in the upcoming window. Based on context entropy, amplitude variability, and short-context spectral change variability. Rising entropy and variability signal that the music is becoming less predictable — threatening the challenge-skill balance point. Formula: σ(0.50 × ctx_entropy + 0.30 × amp_variability + 0.20 × spec_chg_std). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 8 | 11 | M18 (trend) | L0 | Loudness trajectory |
| 1 | 8 | 16 | M15 (smoothness) | L0 | Groove smoothness |

---

## Computation

The F-layer generates predictions about flow state sustainability:

1. **Flow sustain prediction** (idx 8): Extrapolates flow continuation from current flow propensity (f03), loudness trend at H11, and groove smoothness at H16. When flow is currently high, loudness is trending smoothly, and groove is smooth, flow is predicted to continue. Maps to caudate anticipatory dopamine (Salimpoor 2011: r=0.71 with chill anticipation).

2. **Flow disruption risk** (idx 9): Predicts flow breakdown from increasing complexity signals. Context entropy (unpredictability), amplitude variability (motor challenge), and spectral change variability (short-context surprise) all threaten the challenge-skill balance. When these signals rise, flow disruption becomes likely — DLPFC reactivation and DMN resumption are predicted.

All outputs are sigmoid-bounded to [0, 1] with coefficient sums ≤ 1.0.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f03_flow_propensity | Current flow state for sustainability prediction |
| E-layer | f01_motor_automaticity | Automaticity for disruption context |
| M-layer | challenge_skill_balance | Balance state for risk assessment |
| R³ [7] | amplitude | Variability for disruption risk |
| R³ [8] | loudness | Trend and smoothness for sustainability |
| R³ [21] | spectral_change | Short-context variability for disruption |
| R³ [22] | energy_change | Entropy for disruption risk |
| H³ | 2 tuples (see above) + reuses E/M/P tuples | Bar-level features |
