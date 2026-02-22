# SRP Forecast — Predictive Signals (3D)

**Layer**: Forecast (F)
**Indices**: [16:19]
**Scope**: exported (kernel relay: reward_forecast, chills_proximity, resolution_expect)
**Activation**: clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 16 | F0:reward_forecast | [0, 1] | Expected reward in 2-8s ahead. f16 = sigma(0.40 * da_caudate_ramp + 0.30 * harmonic_tension + 0.30 * dynamic_intensity). Based on current buildup trajectory + harmonic tension state. Huron 2006: Imagination (I) response at longer timescales. |
| 17 | F1:chills_proximity | [0, 1] | Estimated proximity to chills event. f17 = sigma(0.35 * peak_detection + 0.30 * da_caudate + 0.20 * dynamic_intensity + 0.15 * refractory_gate). Respects inter-chill refractory period ~10-30s (Grewe 2009). Mori & Zatorre 2024: pre-listening connectivity predicts chills. |
| 18 | F2:resolution_expect | [0, 1] | Expected harmonic resolution in 0.5-2s. f18 = sigma(0.50 * harmonic_tension + 0.30 * (1 - mode_stability) + 0.20 * consonance_trajectory). High when dominant-to-tonic resolution anticipated. Koelsch 2019: predictive processes and the peculiar case of music. |

---

## Design Rationale

1. **Reward Forecast (F0)**: The Imagination (I) component of Huron's ITPRA — the longer-timescale anticipation of future reward. Integrates the current caudate DA ramp (how far along the anticipation cycle), harmonic tension (unresolved tension implies upcoming resolution = reward), and dynamic intensity (crescendo = approaching climax). This is the "something good is coming" signal that creates sustained engagement over 2-8s timescales.

2. **Chills Proximity (F1)**: A composite proximity estimate for the next potential chills/frisson event. Combines peak trigger detection (are Sloboda features present?), caudate ramp state (is the anticipation cycle mature?), and dynamic intensity (is energy building?). Gated by a refractory function: after a chills event, proximity drops and cannot exceed threshold for ~10-30s (Grewe 2009). This reflects not neural exhaustion but the time needed to build new predictions.

3. **Resolution Expectation (F2)**: Predicts when harmonic tension will resolve. High when the current harmonic state implies imminent resolution — a sustained dominant chord, chromatic approach, or unstable mode position that typically resolves to tonic within 0.5-2s. Feeds back into the wanting/anticipation system: high resolution expectation amplifies the wanting ramp because the reward is "almost here."

---

## Refractory Period Model

```
CHILLS REFRACTORY (Grewe 2009):

After a chills event at t_chill:
  refractory_gate(t) = 1 - exp(-(t - t_chill) / tau_refrac)
  where tau_refrac ~ 10-30s (behavioral, not neural)

  t < t_chill + 10s: gate < 0.65 → chills_proximity suppressed
  t > t_chill + 30s: gate > 0.95 → full recovery

This is NOT neural exhaustion — prediction models need time
to rebuild new expectations after a peak event.

Average chills frequency: ~3.7 per 2-3 min excerpt (Salimpoor 2011)
```

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:reward_forecast | F6 Reward | Forward reward signal for learning |
| F0:reward_forecast | F3 Attention | Salience amplification for expected reward |
| F1:chills_proximity | AAC (sibling model) | ANS preparation for chills |
| F1:chills_proximity | F7 Motor | Motor preparation (breath-holding, Etzel 2006) |
| F2:resolution_expect | F2 Prediction | Harmonic resolution prediction validation |
| F2:resolution_expect | Precision engine | pi_pred estimation for harmonic domain |

---

## H3 Dependencies (Forecast)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (7, 22, 4, 1) | amplitude max H22 L1 | Future peak energy at 15s — reward forecast |
| (0, 20, 18, 0) | roughness trend H20 L0 | Dissonance trajectory at 5s — resolution direction |
| (4, 20, 18, 0) | sensory_pleasantness trend H20 L0 | Consonance trend at 5s — resolution approach |
| (7, 20, 8, 1) | amplitude velocity H20 L1 | Forward energy velocity — chills proximity |
| (0, 18, 19, 2) | roughness stability H18 L2 | Harmonic stability at phrase — resolution expectation |

F-layer also reuses T+M and P-layer outputs (harmonic_tension, dynamic_intensity, da_caudate, peak_detection) rather than making all H3 reads directly.

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | F2: resolution trajectory direction |
| [4] | sensory_pleasantness | F2: consonance trend for resolution |
| [7] | amplitude | F0: future energy for reward forecast |

---

## Scientific Foundation

- **Huron 2006**: Imagination (I) response — anticipatory reward at seconds-to-minutes timescale (Sweet Anticipation, MIT Press)
- **Grewe 2009**: Inter-chill refractory ~10-30s, ~3.7 chills per excerpt (psychophysiology, N=38)
- **Salimpoor 2011**: Caudate DA ramp 15-30s before peak = Salimpoor anticipation window (PET, N=8)
- **Howe 2013**: Quasi-hyperbolic DA ramp scales with proximity x magnitude (in vivo rodent)
- **Mori & Zatorre 2024**: Pre-listening auditory-reward connectivity predicts chills duration, r=0.53 (fMRI + LASSO, N=49)
- **Koelsch 2019**: Predictive processes in music — prediction error drives reward and learning
- **de Fleurian & Pearce 2021**: Chills prevalence 55-90%, crescendo = most common trigger (systematic review, k=116)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/srp/forecast.py`
