# AAC Forecast — Predictive ANS Signals (2D)

**Layer**: Forecast (F)
**Indices**: [12:14]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 12 | F0:scr_pred_1s | [0, 1] | Predicted SCR 1s ahead. f12 = sigma(future_energy_H20 - current_energy_H9). Rising energy anticipation gap: if future peak energy (H20 5s horizon, forward law) exceeds current energy, SCR will increase. Boucsein 2012: SCR onset 1-3.5s, so 1s prediction allows preparatory sympathetic priming. |
| 13 | F1:hr_pred_2s | [0, 1] | Predicted HR deceleration 2s ahead. f13 = sigma(-(future_energy_H22 - current_energy_H9)). INVERTED: rising energy predicts HR will DROP (vagal brake). Uses H22 (15s) forward law for longer-horizon section-level prediction. Rickard 2004: HR deceleration onset 0.5-2s after emotional peak. |

---

## Design Rationale

1. **SCR Prediction (F0)**: Anticipates skin conductance increase 1s ahead based on the energy anticipation gap. The gap is computed as: future peak energy at 5s horizon (H20, M4, L1 forward law) minus current peak energy at 350ms (H9, M4, L2). When future energy exceeds current energy (crescendo approaching), SCR will rise. The 1s prediction window matches SCR onset latency (Boucsein 2012: 1-3.5s), allowing the brain to prepare sympathetic efferent commands.

2. **HR Prediction (F1)**: Anticipates heart rate deceleration 2s ahead. INVERTED logic: when future energy exceeds current (approaching climax), HR is predicted to DROP due to the vagal brake mechanism. Uses the longer H22 (15s) horizon because HR deceleration is a sustained response (2-5s duration) reflecting section-level dynamics rather than beat-level events. The 2s prediction window accounts for both the cardiac response lag and the vagal brake onset.

---

## Anticipation Gap Model

```
ENERGY ANTICIPATION GAP:

  gap_scr = H3(H20, M4, L1) - H3(H9, M4, L2)
            ^^^^^^^^^^^^^^     ^^^^^^^^^^^^^^^
            future max energy  current max energy
            at 5s horizon      at 350ms
            forward law        integration law

  gap_hr  = -(H3(H22, M4, L1) - H3(H9, M4, L2))
             ^^^^^^^^^^^^^^^^    ^^^^^^^^^^^^^^^
             future max energy   current max energy
             at 15s horizon      at 350ms
             forward law         integration law
             INVERTED: rising energy -> HR DROP

If gap > 0: energy is BUILDING → SCR will rise, HR will drop
If gap < 0: energy is FALLING → SCR will drop, HR will return
If gap = 0: energy is STABLE → no ANS change predicted
```

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:scr_pred_1s | Precision engine | pi_pred for autonomic predictions |
| F0:scr_pred_1s | SRP forecast | Anticipatory reward signal validation |
| F1:hr_pred_2s | F7 Motor | Cardiac preparation for breath-holding (Etzel 2006) |
| F1:hr_pred_2s | Precision engine | pi_pred for cardiac response |

---

## Overlap with SRP Direct Reads

| Tuple | AAC Uses | SRP Uses | Dedup? |
|-------|----------|----------|--------|
| (7, 20, 4, 1) | future_energy_H20 | anticipation_gap | YES |
| (7, 22, 4, 1) | future_energy_H22 | anticipation_gap | YES |
| (7, 9, 4, 2) | current_energy_H9 | — | No (AAC only) |

The DemandAggregator automatically deduplicates overlapping tuples via set union.

---

## H3 Dependencies (Forecast)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (7, 20, 4, 1) | amplitude max H20 L1 | future_energy_H20 — 5s ahead peak energy (forward law) |
| (7, 22, 4, 1) | amplitude max H22 L1 | future_energy_H22 — 15s ahead peak energy (forward law) |
| (7, 9, 4, 2) | amplitude max H9 L2 | current_energy_H9 — current 350ms peak energy |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [7] | amplitude | F0+F1: energy anticipation gap (future vs current) |

---

## Scientific Foundation

- **Boucsein 2012**: SCR onset 1-3.5s, definitive electrodermal timing reference (Electrodermal Activity, 2nd ed.)
- **Rickard 2004**: Biphasic HR pattern — brief acceleration then sustained deceleration at emotional peaks (Musicae Scientiae)
- **Salimpoor 2011**: Caudate DA ramp 15-30s before peak, ANS composite correlated d=0.71 (PET, N=8)
- **Laeng 2016**: Pupil dilation onset 200-500ms BEFORE subjective report — ANS preparation precedes awareness (N=24, r=0.56)
- **Mori & Zatorre 2024**: Pre-listening auditory-reward connectivity predicts chills duration (fMRI + LASSO, N=49, r=0.53)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/aac/forecast.py`
