# HMCE — Forecast

**Model**: Hierarchical Musical Context Encoding
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: F — Forecast
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 9 | phrase_boundary_pred | Predicted phrase boundary within next 1-2s. Combines phrase_expect (P-layer) with spectral flux trend and key clarity entropy. High values = system predicts an upcoming structural boundary (cadence, section end, key change). Maps to medial cingulate hierarchical top position. Bonetti 2024: cingulate assumes top at sequence recognition. |
| 10 | structure_pred | Structural continuation prediction 2-5s ahead. Predicts whether the current tonal-rhythmic framework will continue or change. Uses long context (f03) + tonal stability trend. Maps to hippocampal sequence completion signal. Fernandez-Rubio 2022: hippocampus + cingulate tonal recognition (N=71). |

---

## H³ Demands

No additional unique H³ demands beyond E/M/P layers. The F-layer reuses:
- tonal_stability trend 1s from (60, 16, M18, L0)
- key_clarity entropy 1s from (51, 16, M13, L0)

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No unique H³ demands; reuses E/M/P layer tuples |

---

## Computation

The F-layer generates predictions about upcoming structural events:

1. **Phrase boundary prediction** (idx 9): Combines phrase_expect (P-layer) with transition dynamics (M-layer) and tonal stability trend at 1s. When context is deep and transition is rising, a phrase boundary is predicted. Formula: σ(0.5 × phrase_expect + 0.3 × transition_dynamics + 0.2 × (1 − tonal_stability_trend)).

2. **Structure prediction** (idx 10): Extrapolates whether the current structural framework persists. Uses long context (f03) and tonal stability trends at 1s. High f03 + stable trend = continuation predicted. Low f03 or falling trend = structural change predicted. Formula: σ(0.5 × f03 + 0.5 × tonal_stability_trend).

Both outputs are sigmoid-bounded to [0, 1] and represent confidence in future structural states.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f03_long_context | Long-range structure for extrapolation |
| M-layer | transition_dynamics | Rate of structural change for boundary detection |
| P-layer | phrase_expect | Current phrase expectation level |
| H³ (shared) | tonal_stability_trend_1s, key_clarity_entropy_1s | Structural signals for prediction |
