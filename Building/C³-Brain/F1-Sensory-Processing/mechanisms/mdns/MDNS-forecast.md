# MDNS F-Layer — Forecast (3D)

**Layer**: F (Forecast)
**Dimensions**: 3D (indices 9–11 of MDNS 12D output)
**Input**: H³ tuples + E-layer + P-layer features
**Character**: Future predictions — next note, phrase completion, imagery generation

---

## Overview

The F-layer generates predictions about upcoming melodic events. Three outputs forecast the next note (TRF-based continuation), phrase completion likelihood (entropy-driven closure), and internal imagery generation strength (perception-imagery code activation). All sigmoid-bounded to [0, 1] with coefficient sums ≤ 1.0.

---

## F0: Next Note Prediction (next_note)

**Range**: [0, 1]
**Brain region**: STG → premotor (predictive coding)
**Question answered**: "What is the predicted next note in the melody?"

### Formula

```python
pitch_vel = H3[(23, 8, 8, 0)]    # pitch_change velocity at H8
pitch_std = H3[(23, 8, 3, 0)]    # pitch_change std at H8
next_note = σ(0.50 * f02_pitch_decoding + 0.30 * pitch_vel + 0.20 * pitch_std)
# coefficients: 0.50 + 0.30 + 0.20 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 23 | pitch_change | 8 | M8 (velocity) | L0 | Pitch trajectory |
| 23 | pitch_change | 8 | M3 (std) | L0 | Pitch variability |

### Logic

Combines current pitch decoding quality (E1), pitch trajectory (velocity), and pitch variability (std) at the motif scale. High decoding + clear trajectory + low variability → confident next-note prediction. High variability + flat trajectory → uncertain prediction.

---

## F1: Phrase Completion (phrase_completion)

**Range**: [0, 1]
**Brain region**: Frontal → STG (phrase closure anticipation)
**Question answered**: "How likely is the current phrase to complete soon?"

### Formula

```python
phrase_entropy = H3[(25, 14, 13, 0)]   # x_l0l5 entropy at H14
phrase_trend = H3[(33, 14, 18, 0)]     # x_l4l5 trend at H14
phrase_completion = σ(0.50 * phrase_entropy + 0.50 * phrase_trend)
# coefficients: 0.50 + 0.50 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 25 | x_l0l5[0] | 14 | M13 (entropy) | L0 | Phrase unpredictability |
| 33 | x_l4l5[0] | 14 | M18 (trend) | L0 | Dynamics coupling direction |

### Logic

Entropy-driven closure anticipation at the phrase level (700ms). Low entropy + declining dynamics trend → phrase approaching cadence → high completion prediction. High entropy + rising trend → phrase continuing → low completion.

---

## F2: Imagery Generation (imagery_generation)

**Range**: [0, 1]
**Brain region**: Secondary AC → PAC (internal representation activation)
**Question answered**: "How strongly is the internal melodic imagery being generated?"

### Formula

```python
phrase_mean = H3[(25, 14, 1, 0)]      # x_l0l5 mean at H14
dyn_mean = H3[(33, 14, 1, 0)]         # x_l4l5 mean at H14
pitch_mean = H3[(23, 14, 1, 0)]       # pitch_change mean at H14
imagery_generation = σ(0.40 * f03_percept_imag
                      + 0.30 * phrase_mean
                      + 0.30 * (dyn_mean + pitch_mean) / 2)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 25 | x_l0l5[0] | 14 | M1 (mean) | L0 | Phrase-level TRF average |
| 33 | x_l4l5[0] | 14 | M1 (mean) | L0 | Phrase dynamics coupling |
| 23 | pitch_change | 14 | M1 (mean) | L0 | Phrase-level pitch dynamics |

### Logic

Combines perception-imagery overlap strength (E2), phrase-level TRF average, and a blend of dynamics and pitch context. When the shared neural code is active AND phrase-level context is rich, strong imagery generation is predicted. Maps to Kraemer 2005: PAC activation during instrumental imagery gaps.

---

## Layer Summary

| Idx | Name | Range | Key H³ Scales | Downstream |
|-----|------|-------|---------------|------------|
| F0 | next_note | [0, 1] | H8 (300ms) velocity+std | → beliefs prediction |
| F1 | phrase_completion | [0, 1] | H14 (700ms) entropy+trend | → beliefs phrase closure |
| F2 | imagery_generation | [0, 1] | H14 (700ms) means | → IMU.MEAMN memory retrieval |

**Total F-layer H³ tuples**: 5 unique (some shared with P-layer)

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f02_pitch_decoding | Pitch quality for next-note prediction |
| E-layer | f03_percept_imag | Imagery overlap for generation forecast |
| P-layer | phrase_position (indirect) | Entropy context reuse |
| H³ | 5 tuples (see above) | Phrase-level features at H8 and H14 |
