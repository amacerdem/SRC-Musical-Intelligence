# BCH F-Layer — Forecast (4D)

**Layer**: F (Forecast/Future)
**Dimensions**: 4D (indices 12–15 of BCH 16D output)
**Input**: E+M+P layer outputs + H³ L0 trends + H³ L1 forward windows
**Character**: Trend extrapolation — NOT pattern-based prediction (that belongs to F2/HTP)

---

## Overview

The F-layer extrapolates current trends into short-term forecasts. These are NOT predictions based on learned musical patterns — they are purely signal-driven trend continuations using H³ L0 (memory) regression slopes and L1 (forward window) means.

**Boundary note**: Pattern-based prediction ("After I-IV-V, I expect I") belongs to F2 (HTP model). BCH's F-layer does sensory extrapolation ("roughness is decreasing, so consonance will likely increase").

---

## F0: Consonance Forecast

**Range**: [0, ~0.94]
**Question answered**: "Based on current trends, will consonance increase or decrease?"

### Formula

```python
F0_consonance_forecast = (
    0.15 * E1_harmonicity                   # f02
  + 0.15 * M0_consonance_memory             # M-layer temporal
  + 0.20 * P0_consonance_signal             # P-layer present
  + 0.10 * coupling                          # consonance×timbre (internal)
  + 0.10 * E3_ffr_behavior                  # f04
  + 0.10 * R3[4]                             # sensory_pleasantness
  + 0.10 * H3[51, H12, M1, L0]             # key clarity memory 525ms
  + 0.10 * H3[60, H6, M1, L0]              # tonal stability memory 200ms
)
```

### Key H³ Forward Tuples (contextual)

The forecast also benefits from L1 forward-window information when available (offline analysis):

| R³ Idx | Feature | H | Morph | Law | Role |
|--------|---------|---|-------|-----|------|
| 0 | roughness | 6 | M1 | L1 | Expected roughness 200ms ahead |
| 2 | helmholtz_kang | 6 | M1 | L1 | Expected consonance 200ms ahead |
| 51 | key_clarity | 6 | M1 | L1 | Expected key clarity 200ms ahead |

### Downstream

**F0 → `consonance_trajectory` Anticipation belief**

This is the sole Anticipation belief owned by BCH. It feeds `harmonic_stability`'s predict() formula as a context signal.

---

## F1: Pitch Forecast

**Range**: [0, ~0.98]
**Question answered**: "Will pitch clarity continue or change?"

### Formula

```python
F1_pitch_forecast = (
    0.20 * E0_nps                            # f01
  + 0.20 * M1_pitch_memory                   # M-layer pitch
  + 0.20 * P2_neural_pitch                   # P-layer pitch
  + 0.15 * H3[0, H6, M14, L2]              # roughness periodicity 200ms
  + 0.15 * H3[39, H6, M0, L2]              # pitch salience at 200ms
  + 0.10 * (1 - H3[38, H0, M0, L2])        # low chroma entropy
)
```

### Key H³ Forward Tuples

| R³ Idx | Feature | H | Morph | Law | Role |
|--------|---------|---|-------|-----|------|
| 39 | pitch_salience | 6 | M1 | L1 | Expected pitch salience 200ms |
| 39 | pitch_salience | 12 | M1 | L1 | Expected pitch salience 525ms |

### Downstream

**F1 does NOT feed a BCH belief.** It feeds **PSCL (SPU-α2)** as a pitch continuation signal. PSCL's `pitch_continuation` Anticipation belief consumes this.

---

## F2: Tonal Forecast

**Range**: [0, 1]
**Question answered**: "Will the tonal context remain stable?"

### Formula

```python
F2_tonal_forecast = (
    0.25 * M2_tonal_memory                   # M-layer tonal
  + 0.25 * P3_tonal_context                  # P-layer tonal
  + 0.15 * H3[51, H12, M1, L0]             # key clarity memory 525ms
  + 0.15 * H3[60, H18, M1, L0]             # tonal stability memory 2s
  + 0.10 * H3[51, H6, M1, L1]              # key clarity forward 200ms
  + 0.10 * H3[60, H6, M1, L1]              # tonal stability forward 200ms
)
```

### Downstream

**F2 does NOT feed a BCH belief directly.** It provides tonal context forecasting for cross-model use (HMCE, HTP).

---

## F3: Interval Forecast

**Range**: [0, 1]
**Question answered**: "What interval characteristics are likely next?"

### Formula

```python
trist_balance = 1.0 - std(R3[18], R3[19], R3[20])

F3_interval_forecast = (
    0.20 * H3[2, H12, M1, L0]              # helmholtz memory 525ms
  + 0.15 * H3[3, H6, M1, L0]              # stumpf memory 200ms
  + 0.15 * (1 - H3[0, H6, M18, L0])       # roughness not increasing (200ms)
  + 0.10 * (1 - H3[5, H3, M18, L0])       # inharmonicity trend stable
  + 0.10 * trist_balance                     # current spectral balance
  + 0.10 * coupling                          # consonance×timbre
  + 0.10 * H3[51, H6, M0, L2]             # key clarity 200ms (context)
  + 0.10 * H3[60, H6, M1, L0]             # tonal stability 200ms (context)
)
```

### Key H³ Forward Tuples

| R³ Idx | Feature | H | Morph | Law | Role |
|--------|---------|---|-------|-----|------|
| 2 | helmholtz_kang | 6 | M1 | L1 | Expected consonance 200ms |
| 2 | helmholtz_kang | 12 | M1 | L1 | Expected consonance 525ms |
| 3 | stumpf_fusion | 6 | M1 | L1 | Expected fusion 200ms |
| 5 | inharmonicity | 6 | M18 | L1 | Inharmonicity trend 200ms ahead |

### Downstream

**F3 does NOT feed a BCH belief.** It provides interval trajectory information for cross-model use (HMCE hierarchical encoding, HTP interval prediction).

---

## Layer Summary

| Idx | Name | Range | → Belief | → External |
|-----|------|-------|----------|------------|
| F0 | consonance_forecast | [0, ~0.94] | `consonance_trajectory` (Anticipation) | — |
| F1 | pitch_forecast | [0, ~0.98] | — | → PSCL (pitch_continuation) |
| F2 | tonal_forecast | [0, 1] | — | → HMCE, HTP (tonal context) |
| F3 | interval_forecast | [0, 1] | — | → HMCE, HTP (interval trajectory) |

**Belief-producing outputs**: F0 only
**Cross-model outputs**: F1, F2, F3

---

## Extrapolation vs Prediction Boundary

| Aspect | BCH F-Layer (Extrapolation) | F2/HTP (Prediction) |
|--------|---------------------------|---------------------|
| Method | H³ trend slopes (M18) + L1 forward means | Learned pattern matching |
| Knowledge | None — pure signal continuation | Musical structure, transition probabilities |
| Example | "Roughness ↓ → consonance ↑" | "I-IV-V → expect I resolution" |
| Horizon | 200ms–525ms (brainstem timescales) | 500ms–25s (cortical timescales) |
| Phase | 0a (relay) | 1 (F2 prediction) |
