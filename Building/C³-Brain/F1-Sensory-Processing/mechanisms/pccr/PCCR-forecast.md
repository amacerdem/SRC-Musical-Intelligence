# PCCR F-Layer — Forecast (3D)

**Layer**: F (Forecast/Future)
**Dimensions**: 3D (indices 8–10 of PCCR 11D output)
**Input**: E+M+P layer outputs + H³ L0 trends + H³ L1 forward windows + upstream PSCL
**Scope**: external (feeds beliefs, downstream models, and other Functions)

---

## Overview

The F-layer extrapolates chroma trends into the near future. Unlike BCH/PSCL F-layers (4D each), PCCR has 3D — capturing the three essential chroma predictions:

1. **F0**: Will the current chroma persist? (continuation)
2. **F1**: Is a chroma change likely? (transition)
3. **F2**: Is the change toward tonal resolution? (direction)

These three together paint a complete picture of chroma trajectory: persistence, change likelihood, and change direction.

---

## Outputs

### F0: Chroma Continuation Signal — [0, 1]

Feeds the Core belief `pitch_identity.predict()` as context signal.

```
F0 = (
    0.30 × (1 − H³[38, H6, M18, L0])    # low PCE trend → stable chroma
  + 0.25 × H³[14, H6, M1, L1]            # expected tonalness ahead
  + 0.25 × H³[39, H6, M1, L1]            # expected pitch_salience ahead
  + 0.20 × M0                             # current chroma stability
)
```

**Interpretation**:
- **High F0** (≈ 0.80): Chroma is stable, tonalness and pitch are expected to persist → strong continuation.
- **Low F0** (≈ 0.20): PCE trend is increasing (more distributed chroma), or tonalness/pitch expected to decrease → chroma change imminent.

**Key**: F0 uses L0 trend (past direction) and L1 forward (expected future) for complementary evidence.

### F1: Chroma Transition Likelihood — [0, 1]

How likely is a chroma class change in the near future?

```
F1 = (
    0.35 × H³[38, H6, M18, L0]           # PCE trend (↑entropy = ↑change)
  + 0.30 × H³[37, H6, M8, L0]            # pitch_height velocity (register movement)
  + 0.20 × (1 − H³[38, H6, M1, L1])      # high expected PCE → change likely
  + 0.15 × H³[38, H6, M0, L2]            # current PCE level (high = unstable)
)
```

**Interpretation**:
- **High F1** (≈ 0.80): Multiple indicators suggest chroma change: entropy rising, pitch register moving, expected high PCE.
- **Low F1** (≈ 0.15): Chroma is stable from all perspectives → no transition expected.

**Note**: F1 is complementary to F0 (continuation ≈ 1 − transition, loosely). They are computed independently so they can diverge when signals conflict.

### F2: Chroma Resolution Direction — [0, 1]

Is the chroma movement trending toward tonal resolution (clarity) or away from it?

```
F2 = (
    0.30 × (1 − H³[38, H6, M1, L1])     # expected lower PCE = toward clarity
  + 0.25 × H³[14, H6, M1, L1]            # expected tonalness increase
  + 0.25 × P0                             # current chroma identity strength
  + 0.20 × H³[37, H6, M1, L1]            # expected pitch_height (register context)
)
```

**Interpretation**:
- **High F2** (≈ 0.80): Chroma is moving toward tonal resolution — PCE decreasing, tonalness increasing, current identity is strong. This is the trajectory from dominant → tonic resolution.
- **Low F2** (≈ 0.20): Chroma is moving away from tonal clarity — dissolving into noise, chromatic motion, or tonal ambiguity.

---

## H³ Tuples Consumed (F-Layer Only)

| # | R³ Idx | Feature | H | Morph | Law | Used In | Purpose |
|---|--------|---------|---|-------|-----|---------|---------|
| 1 | 38 | PCE | 6 | M18 (trend) | L0 | F0, F1 | PCE trend direction |
| 2 | 14 | tonalness | 6 | M1 (mean) | L1 | F0, F2 | Expected tonalness |
| 3 | 39 | pitch_salience | 6 | M1 (mean) | L1 | F0 | Expected pitch salience |
| 4 | 37 | pitch_height | 6 | M8 (velocity) | L0 | F1 | Register movement rate |
| 5 | 38 | PCE | 6 | M1 (mean) | L1 | F1, F2 | Expected PCE |
| 6 | 38 | PCE | 6 | M0 (value) | L2 | F1 | Current PCE level |
| 7 | 37 | pitch_height | 6 | M1 (mean) | L1 | F2 | Expected register |

---

## Extrapolation vs Prediction Boundary

| Property | PCCR F-Layer (F1 Sensory) | F2 Prediction (HTP) |
|----------|---------------------------|----------------------|
| **Scope** | Will chroma persist/change? | Which chroma comes next? |
| **Method** | H³ trend extrapolation | Learned harmonic patterns |
| **Knowledge** | Zero — signal continuation | Musical grammar (key, scale) |
| **Example** | "PCE ↓ → chroma stabilizing" | "V chord → expect resolution to I" |
| **Horizon** | 200ms forward | 500ms–5s forward |

PCCR's F-layer provides **sensory extrapolation** ("chroma trends suggest continuation/change"). It does NOT predict which specific pitch class comes next — that requires F2's learned musical patterns.

---

## Downstream Routing

| Output | → Consumer | How It's Used |
|--------|-----------|---------------|
| F0 | `pitch_identity` predict() | Context signal (w_ctx weight) |
| F0 | Precision engine | Continuation confidence → π_pred |
| F1 | HTP (F2) | Transition likelihood as prediction input |
| F1 | MPG contour tracking | Chroma change supports contour boundary detection |
| F2 | IMU memory binding | Tonal resolution → memory encoding gate |
| F2 | STU temporal structure | Resolution direction informs phrase structure |
