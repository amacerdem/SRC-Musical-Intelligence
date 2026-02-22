# CLAM F-Layer — Forecast (2D)

**Layer**: Forecast (F)
**Indices**: [9:11]
**Scope**: exported (kernel relay)
**Activation**: tanh (idx 9), sigmoid (idx 10)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 9 | F0:target_affect_pred | [-1, 1] | Predicted affective state 2-5s ahead. tanh(decoded_affect + 0.5 * error_trend). Based on current decoded state and error convergence trajectory from H12 trend morphs. Ehrlich 2019: loop latency ~1s implies 2-5s forecast horizon for stable control. |
| 10 | F1:modulation_success | [0, 1] | Predicted modulation success 5-10s ahead. sigma(loop_coherence + 0.5 * (1.0 - \|error\|)). Based on loop coherence stability and error convergence rate. Ehrlich 2019: 3/5 modulation success rate implies predictable individual differences. |

---

## Design Rationale

1. **Target Affect Prediction (F0)**: Projects the affective state 2-5 seconds ahead based on the current trajectory. Uses the decoded affect as baseline plus half the error trend — if error is converging (negative trend), the prediction moves toward target; if diverging, it moves away. The 2-5s horizon reflects the practical control timescale: one loop cycle is ~1s, so 2-5 cycles ahead is a reasonable prediction window for clinical monitoring. Enables preemptive parameter adjustments before the loop diverges.

2. **Modulation Success Prediction (F1)**: Forecasts whether the BCI loop will maintain or achieve successful modulation over the next 5-10 seconds. Combines loop coherence (is the causal pathway intact?) with error magnitude (is modulation working?). High coherence + low error = high predicted success. This enables clinical decision-making: if predicted success drops below threshold, the system can alert the therapist or switch strategies. Ehrlich 2019's 60% success rate suggests this predictor should distinguish responders from non-responders early.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 12, 18, 0) | loudness trend H12 L0 | Arousal trajectory for affect prediction |
| (0, 12, 18, 0) | roughness trend H12 L0 | Valence trajectory for affect prediction |
| (21, 16, 18, 0) | spectral_flux trend H16 L0 | Feedback signal trajectory for success prediction |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | F0: valence trajectory basis |
| [10] | loudness | F0: arousal trajectory basis |
| [21] | spectral_flux | F1: feedback signal trend |

---

## Scientific Foundation

- **Ehrlich et al. 2019**: Loop latency ~1000ms; modulation success 3/5 participants (60%) — implies individual difference predictability (EEG-BCI, N=11)
- **Ehrlich et al. 2019**: Closed-loop transfer function H(s) = Kp*G_music*G_brain / (1 + Kp*G_music*G_brain) — convergence dynamics predict success (control theory)
- **Sayal et al. 2025**: Music-based neurofeedback engagement predicts therapeutic outcome — reward-system coupling enables success forecasting (systematic review, N=20+ studies)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/clam/forecast.py`
