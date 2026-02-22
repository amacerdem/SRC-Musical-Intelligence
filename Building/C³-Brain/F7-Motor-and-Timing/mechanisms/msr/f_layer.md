# MSR — Forecast

**Model**: Musician Sensorimotor Reorganization
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: F — Forecast
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 9 | performance_efficiency | Trial-level efficiency prediction. Predicts near-future sensorimotor efficiency based on current PLV/P2 state. Higher values predict more efficient processing on the next trial. Grahn & Brett 2007: musicians show consistent motor-area activation across rhythm types. Alpheis 2025: stable FC patterns in trained musicians. |
| 10 | processing_automaticity | Session-level automaticity. Predicts the degree of automatic (effortless) processing over the session time scale. Higher values indicate more automatized sensorimotor routines. Blasi 2025: structural neuroplasticity (GMV increases in IFG, cerebellum) supports automatic processing. Fujioka 2012: internalized timing in beta oscillations. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 7 | 3 | M0 (value) | L2 (bidi) | Amplitude at 100ms — motor drive for prediction |
| 1 | 7 | 16 | M1 (mean) | L2 (bidi) | Mean amplitude 1s — sustained motor state |
| 2 | 21 | 4 | M8 (velocity) | L2 (bidi) | Tempo velocity at 125ms — rate dynamics for prediction |

---

## Computation

The F-layer generates predictions about future sensorimotor processing efficiency:

1. **Performance efficiency** (idx 9): Predicts trial-level sensorimotor performance from the current PLV/P2 balance and motor dynamics. Combines the efficiency index (M-layer) with amplitude-based motor drive signals. Higher current PLV and stronger P2 suppression predict more efficient processing on upcoming trials. This implements a short-horizon forecast that captures how the dual reorganization translates to moment-to-moment performance advantage.

2. **Processing automaticity** (idx 10): Predicts session-level automaticity — the degree to which auditory-motor processing has become effortless and automatic. Combines the training level estimate (P-layer) with long-term amplitude stability (mean amplitude 1s). Automaticity increases with training level and stable motor engagement. This longer-horizon forecast reflects the structural neuroplasticity documented by Blasi 2025 (GMV increases supporting automatic processing) and the internalized timing of Fujioka 2012 (beta oscillations representing automatized rhythm).

Both outputs are sigmoid-bounded to [0, 1] and represent confidence in future-state predictions.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| M-layer | efficiency_index | Current efficiency feeds performance prediction |
| P-layer | training_level | Training estimate feeds automaticity prediction |
| R³ [7] | amplitude | Motor drive signal for prediction generation |
| R³ [21] | spectral_change | Tempo dynamics for rate-based prediction |
| H³ | 3 tuples (see above) | Amplitude and velocity features for forecast computation |
