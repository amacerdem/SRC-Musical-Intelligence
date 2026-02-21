# Belief Cycle — Core Formulas

## Bayesian Belief Update

Her belief her frame'de 3 adım:

```
observed  = f(R³, H³, relay_outputs)     # measure
predicted = τ × prev + (1−τ) × baseline  # predict
             + w_trend × H³_M18(trend)
             + w_period × H³_M14(periodicity)
             + w_ctx × Σ(context_weights × beliefs_{t-1})
posterior = (1 − gain) × predicted + gain × observed   # update
```

**Bayesian gain:**
```
gain = π_obs / (π_obs + π_pred + ε)
```
- `π_obs` = observation precision (sensory confidence, from observe())
- `π_pred` = prediction precision (from PE history)
- High `π_obs` → trust observation. High `π_pred` → trust prediction.

**Prediction Error:**
```
PE = observed − predicted
```

## Multi-Scale Prediction (v2.0)

Belief'ler birden fazla temporal horizon'da tahmin yapabilir.

**Scale-matched evidence weighting:**
```
w(h, Δ) = exp(−α |h − Δ|) / Σ exp(−α |h' − Δ|)
```
- `h` = evidence horizon, `Δ` = target horizon
- Peak weight when evidence matches target timescale
- α = 0.3 (default decay): ±3 index → %20, ±8 → %5

**Per-horizon prediction:**
```
pred_h = τ × prev + (1−τ) × baseline + w_trend × Σ(w(h_ev, h_target) × M18(h_ev))
```

**Aggregation (T_char-based):**
```
closest_h = argmin_h |HORIZON_SECONDS[h] − T_char|
agg_weights = scale_matched_weights(closest_h, horizons, α)
posterior = Σ agg_weights[h] × pred_h
```

## Belief Parameters

| Belief | τ (inertia) | baseline | phase | grounding |
|--------|-------------|----------|-------|-----------|
| consonance | 0.3 | 0.5 | 0 | R³ roughness/sethares/tonalness |
| tempo | 0.7 | 0.5 | 0 | R³ tempo_estimate/beat/pulse |
| salience | 0.3 | 0.3 | 1 | H³ velocity (M8) |
| familiarity | 0.85 | 0.0 | 2 | H³ periodicity (M14) |
| reward | 0.8 | 0.0 | 3 | C³ internal (PEs) |

## Phase Dependencies

```
consonance(0), tempo(0)      ← independent, R³ grounded
       ↓
salience(1)                  ← needs PE_prev from above
       ↓
familiarity(2)               ← needs macro H³ (slower)
       ↓
reward(3)                    ← needs all PEs + salience + familiarity
```

Phase ordering resolves circular dependency: beliefs_{t-1} includes
reward from previous frame, so consonance can "use" reward without
actual circularity.

## Observe Formulas

### Consonance (R³)
```
# R³ fallback:
value = 0.30×pleasant + 0.25×stumpf + 0.20×tonalness
        + 0.15×(1−roughness) + 0.10×(1−sethares)

# BCH relay mode:
value = 0.50×consonance_signal + 0.30×template_match + 0.20×hierarchy

# Precision (BCH): 1/(std(3 BCH signals) + 0.1)
# Precision (R³): tonalness × amplitude / (H³_std + ε)
```

### Tempo (R³)
```
# R³ base:
value = 0.35×tempo_estimate + 0.25×beat_strength
        + 0.25×pulse_clarity + 0.15×regularity

# HMCE blend: 0.70×R³ + 0.30×HMCE_context
#   HMCE = 0.40×A1 + 0.35×STG + 0.25×MTG

# PEOM motor: 0.50×period_lock + 0.30×kinematic + 0.20×beat_pred

# Precision: regularity × onset × amplitude / (H³_std + ε)
```

### Salience (H³)
```
energy = 0.6×amplitude + 0.4×onset
h3_change = max(|vel_amp|, |vel_onset|, |vel_flux|)  # beat scale
            × 0.60 + phrase_scale × 0.40

# 4-signal mixing (with relays):
base = 0.25×energy + 0.25×h3_change + 0.15×|PE_prev| + 0.35×relay
value = 0.5×base + 0.5×max(all signals)   # peak preservation

# SNEM attention gate (multiplicative):
value *= 1 + 0.3 × selective_gain

# Precision: (0.5×energy + 0.5×h3_change) × 10, clamped [0.5, 10]
```

### Familiarity (H³)
```
# Implicit (65%): H³ periodicity + stability
period_signal = mean(M14(tonalness, key_clarity, tonal_stability))
stability = mean(1 / (1 + 5×M2(features)))
implicit = 0.50×periodicity + 0.35×stability + 0.15×R³_tonal

# Explicit (35%): MEAMN memory
explicit = 0.60×memory_state + 0.25×emotional_color + 0.15×self_ref

# Combined: (0.65×implicit + 0.35×explicit) × energy_gate
# Energy gate: σ(10 × (energy − 0.1))

# Precision: 1/(std(3 periodicity features) + 0.1) × gate
#            + MEAMN: 0.3×(memory×nostalgia) + 0.2×self_ref + 0.1×vividness
```

### Reward (C³)
```
observe() = zeros   # no sensory observation
# Actual computation via RewardAggregator (see REWARD-FORMULA.md)
```

## Multi-Scale Horizons

### Consonance: 8 horizons, T_char = 525ms
```
H5(46ms)  H7(250ms)  H10(400ms)  H13(600ms)
H18(2s)   H21(8s)    H24(36s)    H28(414s)
```

### Tempo: 6 horizons, T_char = 600ms
```
H5(46ms)  H7(250ms)  H10(400ms)  H13(600ms)
H18(2s)   H21(8s)
```
No ultra horizons — tempo is beat/phrase-level, ultra meaningless for 30s excerpts.
