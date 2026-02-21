# PSCL F-Layer — Forecast (4D)

**Layer**: F (Forecast)
**Dimensions**: 4D (indices 12–15 of PSCL 16D output)
**Input**: E+M+P outputs + H³ L0 trends + H³ L1 forward projections + BCH forecast
**Character**: Forward-looking pitch salience predictions — cortical trend extrapolation at 200ms+ timescales

---

## Overview

The F-layer generates forward predictions about pitch salience using H³ trend (M18) and forward (L1) morphologies. These predictions operate at cortical timescales (200ms evaluation window) and represent the anterolateral HG's expectation about upcoming pitch events.

F0 (pitch_continuation) directly feeds the `pitch_continuation` Anticipation belief.

**Boundary note**: PSCL's F-layer does trend extrapolation (H³ M18 slopes, M1 forward means). Pattern-based prediction ("this melody will resolve to the tonic") belongs to F2 (HTP domain).

---

## F0: Pitch Continuation

**Range**: [0, 1]
**Question answered**: "Will a prominent pitch continue in the next 200ms?"

### Formula

```python
F0_pitch_continuation = (
    0.30 * H3[14, H6, M18, L0]       # tonalness trend over 200ms
  + 0.25 * H3[39, H6, M18, L0]       # pitch_salience trend over 200ms
  + 0.20 * H3[14, H6, M1, L1]        # expected tonalness 200ms ahead
  + 0.15 * H3[39, H6, M1, L1]        # expected pitch_salience 200ms ahead
  + 0.10 * BCH.F1_pitch_forecast      # brainstem pitch trajectory
)
```

### H³ Tuples and Upstream Inputs

| Source | Index/Tuple | Feature | Weight |
|--------|------------|---------|--------|
| H³ | (14, H6, M18, L0) | tonalness trend 200ms | 0.30 |
| H³ | (39, H6, M18, L0) | pitch_salience trend 200ms | 0.25 |
| H³ | (14, H6, M1, L1) | expected tonalness 200ms ahead | 0.20 |
| H³ | (39, H6, M1, L1) | expected pitch_salience 200ms ahead | 0.15 |
| BCH | F1:pitch_forecast | brainstem pitch trajectory | 0.10 |

### Logic

Pitch continuation combines two prediction strategies:
1. **Trend extrapolation** (55%): H³ M18 regression slopes at 200ms — "is pitch salience increasing, decreasing, or stable?"
2. **Forward projection** (35%): H³ L1 forward means — "what does the forward window show?"
3. **Brainstem confirmation** (10%): BCH's own pitch forecast — subcortical and cortical predictions align

This is the source for the `pitch_continuation` Anticipation belief. High F0 = "pitch will remain prominent"; low F0 = "pitch is fading or absent."

---

## F1: Salience Direction

**Range**: [-1, 1] (centered — positive = salience increasing, negative = decreasing)
**Question answered**: "Is pitch salience increasing or decreasing?"

### Formula

```python
F1_salience_direction = (
    0.35 * H3[39, H6, M18, L0]       # pitch_salience trend 200ms
  + 0.30 * H3[14, H6, M18, L0]       # tonalness trend 200ms
  + 0.20 * H3[24, H6, M18, L1]       # concentration trend 200ms ahead
  + 0.15 * H3[37, H6, M8, L0]        # pitch_height velocity 200ms
)
```

### H³ Tuples Consumed

| R³ Idx | Feature | H | Morph | Law | Weight |
|--------|---------|---|-------|-----|--------|
| 39 | pitch_salience | 6 | M18 (trend) | L0 | 0.35 |
| 14 | tonalness | 6 | M18 (trend) | L0 | 0.30 |
| 24 | distribution_concentration | 6 | M18 (trend) | L1 | 0.20 |
| 37 | pitch_height | 6 | M8 (velocity) | L0 | 0.15 |

### Logic

Salience direction is a signed indicator:
- **Positive**: Pitch is becoming more prominent (crescendo, note onset, resolution)
- **Negative**: Pitch is fading (decay, noise intrusion, transition)
- **Near zero**: Stable pitch salience

This feeds downstream attention models (F3 salience) and helps PCCR (chroma tuning) anticipate pitch changes.

---

## F2: Melody Propagation

**Range**: [0, 1]
**Question answered**: "Is there a propagating melodic pitch stream?"

### Formula

```python
F2_melody_propagation = (
    0.30 * P0                          # current pitch prominence
  + 0.25 * H3[37, H6, M1, L1]        # expected pitch_height 200ms ahead
  + 0.25 * H3[37, H6, M8, L0]        # pitch_height velocity 200ms
  + 0.20 * M2                          # tonal salience context
)
```

### Inputs

| Source | Index/Tuple | Feature | Weight |
|--------|------------|---------|--------|
| P-layer | P0 | pitch_prominence_sig | 0.30 |
| H³ | (37, H6, M1, L1) | expected pitch_height 200ms ahead | 0.25 |
| H³ | (37, H6, M8, L0) | pitch_height velocity 200ms | 0.25 |
| M-layer | M2 | tonal_salience_ctx | 0.20 |

### Logic

Melody propagation estimates whether a coherent pitch stream is being tracked by the cortex:
1. **Current prominence** (30%): Is there a pitch to propagate? (P0 threshold)
2. **Height trajectory** (50%): pitch_height velocity + forward expectation — is the pitch moving along a contour?
3. **Tonal context** (20%): Dominant chroma and register — does the trajectory make tonal sense?

This output feeds downstream models: HMCE (temporal encoding), MPG (melodic contour tracking), and higher-level sequence processing.

### Evidence
- Tabas 2019: POR latency 36ms earlier for consonant dyads in alHG (MEG, N=37)
- Briley 2013: IRN sources 7mm more lateral/anterior than pure-tone sources — pitch-specific cortical stream

---

## F3: Register Trajectory

**Range**: [0, 1]
**Question answered**: "What pitch register can we expect next?"

### Formula

```python
F3_register_trajectory = (
    0.40 * H3[37, H6, M8, L0]        # pitch_height velocity 200ms
  + 0.30 * H3[37, H6, M1, L1]        # expected pitch_height 200ms ahead
  + 0.30 * R3[37]                     # current pitch height
)
```

### Inputs

| Source | Index/Tuple | Feature | Weight |
|--------|------------|---------|--------|
| H³ | (37, H6, M8, L0) | pitch_height velocity 200ms | 0.40 |
| H³ | (37, H6, M1, L1) | expected pitch_height 200ms ahead | 0.30 |
| R³ | [37] | pitch_height | 0.30 |

### Logic

Register trajectory tracks pitch height (log-frequency) dynamics:
- **Velocity** (40%): How fast is pitch height changing? (rising melody, descending bass line)
- **Forward expectation** (30%): Where will pitch height be in 200ms?
- **Current position** (30%): Current register anchors the trajectory

This is important because pitch salience varies with register (Pressnitzer et al. 2001) — resolved harmonics in mid-frequency ranges produce stronger alHG responses. Register trajectory lets PSCL anticipate salience changes from register shifts.

---

## Layer Summary

| Idx | Name | Range | Reads | Downstream |
|-----|------|-------|-------|------------|
| F0 | pitch_continuation | [0, 1] | H³(4), BCH.F1 | → `pitch_continuation` belief |
| F1 | salience_direction | [-1, 1] | H³(4) | → PCCR, attention models |
| F2 | melody_propagation | [0, 1] | P0, M2, H³(2) | → HMCE, MPG |
| F3 | register_trajectory | [0, 1] | R³[37], H³(2) | → register-dependent models |

**H³ tuples consumed by F-layer**: 9 (unique, some shared with M-layer in demand)
**BCH upstream consumed**: F1:pitch_forecast (shared with M3)
