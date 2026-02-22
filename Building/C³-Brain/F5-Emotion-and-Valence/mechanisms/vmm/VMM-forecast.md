# VMM Forecast — Valence Predictions (2D)

**Layer**: Forecast (F)
**Indices**: [12:14]
**Scope**: internal
**Activation**: tanh (valence_forecast) / sigmoid (mode_shift_proximity)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 12 | F0:valence_forecast | [-1, 1] | Predicted valence 2-4s ahead. f12 = tanh(0.60 * consonance_trend_H20 + 0.40 * mode_trajectory_H22). Positive slope = approaching happy resolution. Negative slope = moving toward minor/sad. Based on harmonic trajectory (forward trend at 5s) + mode change direction (forward trend at 15s). |
| 13 | F1:mode_shift_proximity | [0, 1] | Expected key/mode change proximity. f13 = sigma(0.50 * (1 - mode_stability_H22) + 0.30 * consonance_var_H19 + 0.20 * abs(valence_velocity_H20)). High when mode unstable + harmonic variance + rapid valence change. Modulation detection for valence anticipation. |

---

## Design Rationale

1. **Valence Forecast (F0)**: Predicts valence direction 2-4s ahead using two forward-looking H3 features. Consonance trend at H20 (5s, M18 trend, L0 forward law) captures the slope of consonance evolution — rising consonance predicts positive valence shift, falling consonance predicts negative shift. Mode trajectory at H22 (15s, M18 trend, L0 forward law) captures section-level tonal direction. Weighted 60/40 in favor of consonance trend because it is more immediately responsive than mode trajectory.

2. **Mode Shift Proximity (F1)**: Anticipates upcoming key changes or modulations. Three indicators converge: mode instability (1 - stability at section level), consonance variance (harmonic ambiguity at phrase level), and absolute valence velocity (rapid change in any direction). When all three are elevated, a key change is likely imminent. This feeds back into SRP: modulations create prediction errors that drive wanting (anticipation of new tonal environment).

---

## Prediction Horizon Justification

```
WHY 2-4s PREDICTION WINDOW FOR VALENCE:

Mode perception requires phrase-level context (2-8s).
Therefore valence predictions need at least 2s lookahead
to be useful — shorter predictions would not capture
meaningful harmonic transitions.

Compare:
  SRP forecast:   2-8s ahead   (reward events)
  AAC forecast:   1-2s ahead   (ANS response latency)
  VMM forecast:   2-4s ahead   (harmonic transitions)

The 2-4s window maps to:
  ~4-8 chords at 120 BPM (common phrase progression)
  ~2-3 harmonic rhythm events at 60 BPM (slow passages)
  Minimum for detecting modulation onset
```

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:valence_forecast | SRP reward | Anticipated valence -> wanting modulation |
| F0:valence_forecast | Precision engine | pi_pred for valence beliefs |
| F1:mode_shift_proximity | SRP tension | Approaching modulation -> tension buildup |
| F1:mode_shift_proximity | F3 Attention | Key change anticipation -> salience boost |
| F1:mode_shift_proximity | F2 Prediction | Harmonic prediction confidence adjustment |

---

## Cross-Model Interactions

| VMM F-Layer | Interacts With | Nature of Interaction |
|------------|---------------|----------------------|
| valence_forecast | SRP.wanting | Mode changes create prediction errors -> reward |
| valence_forecast | AAC.scr_pred_1s | Valence shifts -> ANS preparation |
| mode_shift_proximity | SRP.tension | Unstable mode -> uncertainty -> tension |
| mode_shift_proximity | SRP.prediction_error | Modulation = harmonic surprise -> RPE |

---

## H3 Dependencies (Forecast)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 20, 18, 0) | sensory_pleasantness trend H20 L0 | consonance_trend — forward consonance slope at 5s |
| (14, 22, 18, 0) | tonalness trend H22 L0 | mode_trajectory — forward mode direction at 15s |
| (14, 22, 19, 2) | tonalness stability H22 L2 | mode_stability — tonal center stability at 15s |
| (4, 19, 2, 2) | sensory_pleasantness std H19 L2 | consonance_var — harmonic ambiguity at 3s |
| (4, 20, 8, 0) | sensory_pleasantness velocity H20 L0 | valence_velocity — rate of valence change at 5s |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [4] | sensory_pleasantness | F0: consonance trend direction, F1: variance |
| [14] | tonalness | F0: mode trajectory, F1: mode stability |

---

## Scientific Foundation

- **Krumhansl & Kessler 1982**: Probe-tone profiles — tonal center requires phrase-level context for reliable classification
- **Lerdahl 2001**: Tonal pitch space — section-level context required for modulation detection
- **Huron 2006**: ITPRA Imagination response — anticipatory valence at seconds-to-minutes timescale (Sweet Anticipation, MIT Press)
- **Sachs 2025**: Context modulates neural event boundaries — preceding emotion affects temporal processing of valence transitions (fMRI + HMM, N=39)
- **Koelsch 2019**: Predictive processes in music — harmonic predictions update across phrase boundaries
- **Carraturo 2025**: Major=positive, minor=negative direction robust across k=70 studies; cultural modulation of strength not direction

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/vmm/forecast.py`
