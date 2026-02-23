# PTGMP — Cognitive Present

**Model**: Piano Training Grey Matter Plasticity
**Unit**: STU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 5 | motor_coordination | Current cerebellar motor state. σ(0.30 × flux_val + 0.30 × onset_val + 0.20 × flux_mean + 0.20 × spec_chg_mean). Short-context aggregation at H8 (300ms) reflecting real-time keystroke timing precision and motor coordination demand. High when note onsets are frequent and spectrally complex. |
| 6 | audio_motor_binding | Current DLPFC audio-motor integration state. σ(0.30 × energy_mean_H14 + 0.25 × loudness_mean_H14 + 0.25 × pitch_mean_H14 + 0.20 × amp_trend_H14). Medium-context aggregation at H14 (700ms) reflecting phrase-level motor-sequence planning and audio-motor coordination demand. |

---

## H³ Demands

No unique H³ tuples — P-layer reuses E-layer tuples:

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | 10 | 8 | M0 (value) | L0 | Flux current (from E-layer) |
| — | 10 | 8 | M1 (mean) | L0 | Flux mean (from E-layer) |
| — | 11 | 8 | M0 (value) | L0 | Onset current (from E-layer) |
| — | 21 | 8 | M1 (mean) | L0 | Spectral change mean (from E-layer) |
| — | 22 | 14 | M1 (mean) | L0 | Energy mean (from E-layer) |
| — | 8 | 14 | M1 (mean) | L0 | Loudness mean (from M-layer) |
| — | 23 | 14 | M1 (mean) | L0 | Pitch mean (from E-layer) |
| — | 7 | 14 | M18 (trend) | L0 | Amplitude trend (from E-layer) |

---

## Computation

The P-layer represents the present-tense motor and audio-motor state:

1. **Motor coordination** (idx 5): Real-time cerebellar demand from four short-context features at H8. Spectral flux (onset detection), onset strength (keystroke precision), mean flux (information rate), and spectral change (motor dynamics). Coefficient sum: 0.30 + 0.30 + 0.20 + 0.20 = 1.0.

2. **Audio-motor binding** (idx 6): Real-time DLPFC demand from four phrase-context features at H14. Energy dynamics, loudness level, pitch dynamics, and intensity trajectory combine to represent the audio-motor planning load. This is the executive planning counterpart to cerebellar coordination. Coefficient sum: 0.30 + 0.25 + 0.25 + 0.20 = 1.0.

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| H³ (reused) | Short-context tuples at H8 | Motor coordination features |
| H³ (reused) | Phrase-context tuples at H14 | Audio-motor binding features |
