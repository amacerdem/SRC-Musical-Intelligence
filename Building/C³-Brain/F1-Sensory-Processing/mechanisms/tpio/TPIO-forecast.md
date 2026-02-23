# TPIO F-Layer — Forecast (3D)

**Layer**: F (Forecast)
**Dimensions**: 3D (indices 7–9 of TPIO 10D output)
**Input**: H³ tuples + E-layer + P-layer features
**Character**: Future predictions — imagery stability, timbre expectation, overlap maintenance

---

## Overview

The F-layer generates predictions about the continuation of timbre perception-imagery processing. Three outputs forecast imagery maintenance stability, expected timbre continuation, and predicted overlap persistence. All sigmoid-bounded to [0, 1] with coefficient sums ≤ 1.0.

---

## F0: Imagery Stability Prediction (imagery_stability_pred)

**Range**: [0, 1]
**Brain region**: pSTG → memory circuits (imagery maintenance)
**Question answered**: "Will the current timbre imagery be maintained in the next window?"

### Formula

```python
trist1_autocorr = H3[(18, 20, 22, 0)]  # tristimulus1 autocorrelation at H20
imagery_stability_pred = σ(0.60 * trist1_autocorr + 0.40 * f02_imagery_substrate)
# coefficients: 0.60 + 0.40 = 1.0 ✓
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Purpose |
|--------|---------|---|-------|-----|---------|
| 18 | tristimulus1 | 20 | M22 (autocorr) | L0 | F0 self-similarity at section |

### Logic

High F0 autocorrelation at section level (5000ms) means the fundamental frequency pattern is self-similar → the instrument identity is stable → imagery can be maintained. Combined with current imagery substrate strength, this predicts whether the internal timbre representation will persist. When F0 pattern is irregular (low autocorr) or imagery is weak → imagery likely to decay.

---

## F1: Timbre Expectation (timbre_expectation)

**Range**: [0, 1]
**Brain region**: pSTG (predictive timbre processing)
**Question answered**: "What timbre continuation is expected in the next window?"

### Formula

```python
warmth_phrase = H3[(12, 14, 1, 0)]     # warmth mean at H14
tonalness_std = H3[(14, 14, 3, 0)]     # tonalness std at H14
timbre_expectation = σ(0.50 * warmth_phrase + 0.50 * (1.0 - tonalness_std))
# coefficients: 0.50 + 0.50 = 1.0 ✓
```

### H³ Tuples Consumed

Uses tuples already consumed in E-layer and P-layer (no unique new tuples).

### Logic

Combines phrase-level warmth mean and tonal stability (inverted std):
1. **Warmth trajectory** (0.50): Stable warmth → timbre continuation expected
2. **Tonal consistency** (0.50): Low variability → reliable timbre prediction

When both are high, the system confidently predicts timbre continuation. When either is unstable → instrument change or timbral evolution expected.

---

## F2: Overlap Prediction (overlap_pred)

**Range**: [0, 1]
**Brain region**: pSTG shared substrate (predictive maintenance)
**Question answered**: "Will the perception-imagery overlap be maintained?"

### Formula

```python
amplitude_trend = H3[(7, 20, 18, 0)]   # amplitude trend at H20
overlap_pred = σ(0.50 * f03_perc_imag_overlap + 0.50 * amplitude_trend)
# coefficients: 0.50 + 0.50 = 1.0 ✓
```

### H³ Tuples Consumed

Uses tuples already consumed in E-layer (no unique new tuples).

### Logic

Combines current overlap strength (E2) with long-range amplitude trend:
1. **Current overlap** (0.50): Strong overlap now → likely to persist
2. **Amplitude trend** (0.50): Rising intensity → engagement maintained → overlap persists. Declining intensity → disengagement → overlap may decay.

This prediction is particularly relevant for the "gap" paradigm (Kraemer 2005) — during silences, overlap depends on whether the intensity context predicts resumption.

---

## Layer Summary

| Idx | Name | Range | Key Inputs | Downstream |
|-----|------|-------|------------|------------|
| F0 | imagery_stability_pred | [0, 1] | H³ trist1 autocorr at H20 + E1 | → beliefs imagery prediction |
| F1 | timbre_expectation | [0, 1] | H³ warmth+tonalness at H14 | → ETAM timbre context |
| F2 | overlap_pred | [0, 1] | E2 + H³ amplitude trend at H20 | → ARU affective response |

**Total F-layer unique H³ tuples**: 0 (all reused from E-layer and P-layer)

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f02_imagery_substrate | Imagery quality for stability prediction |
| E-layer | f03_perc_imag_overlap | Current overlap for persistence prediction |
| P-layer | (indirect) | Stability features shared |
| H³ | 0 unique tuples | All reused from E/P layers |
