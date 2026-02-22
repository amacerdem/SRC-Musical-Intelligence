# MAA F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [7:10]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:appreciation_growth | [0, 1] | Liking increase prediction (2-5s ahead). Predicts whether repeated exposure will increase appreciation. f_growth = sigma(0.5 * f02 + 0.5 * f04). Gold 2019: inverted-U preference shifts toward expected outcomes with repetition (quadratic IC+entropy p<0.05). |
| 8 | F1:pattern_recognition | [0, 1] | Structure perception prediction (1-3s ahead). Predicts whether the listener will discover pattern regularity in upcoming material. f_pattern = sigma(0.5 * f01 + 0.5 * f02). Cheung 2019: low uncertainty + high surprise = high pleasure (saddle-shaped surface, R2=0.476). |
| 9 | F2:aesthetic_development | [0, 1] | Taste evolution prediction (5-10s ahead). Predicts long-term aesthetic development toward appreciating complex music. f_aesthetic = sigma(0.5 * f03 + 0.5 * f04). Sarasso 2021: aesthetic attitude reorients attention to learning; Harding 2025: psilocybin maintains surprise-related pleasure (between-group p<0.05). |

---

## Design Rationale

1. **Appreciation Growth (F0)**: Forecasts the trajectory of liking over the next several seconds. Combines familiarity index (f02) with current appreciation composite (f04) to predict whether the mere exposure effect will strengthen. When familiarity is building and current appreciation is positive, the forecast predicts continued liking increase. Maps to the behavioral finding that liking for complex music grows with repeated exposure, following an inverted-U trajectory.

2. **Pattern Recognition (F1)**: Predicts the likelihood that the listener will discover structural regularity in the upcoming musical material. Combines complexity tolerance (f01) with familiarity (f02), since pattern recognition requires both the capacity to handle complexity and sufficient exposure to detect recurring structures. Maps to the Cheung 2019 finding that pleasure peaks when uncertainty is low (patterns discovered) and surprise is high (novel elements within those patterns).

3. **Aesthetic Development (F2)**: The longest-horizon prediction — forecasts whether the listener's aesthetic sensibility is shifting toward greater appreciation of complexity. Combines framing effect (f03) with appreciation composite (f04), reflecting the idea that sustained aesthetic framing combined with positive appreciation drives taste development. Maps to Sarasso 2021 theory that aesthetic emotions facilitate cognitive adaptation and Harding 2025 evidence that altered states can maintain surprise-related pleasure.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 16, 1, 0) | roughness mean H16 L0 | Mean dissonance trajectory over 1s |
| (4, 16, 1, 0) | sensory_pleasantness mean H16 L0 | Mean consonance trajectory over 1s |

F-layer primarily reuses E-layer and P-layer outputs (f01-f04) rather than reading new H3 tuples directly. The two tuples above provide trajectory context for the prediction horizon.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:appreciation_growth | F6 Reward | PE from liking trajectory prediction |
| F1:pattern_recognition | F2 Prediction | Pattern discovery forecast for precision estimation |
| F2:aesthetic_development | Precision engine | pi_pred for long-horizon aesthetic processing |

---

## Scientific Foundation

- **Gold et al. 2019**: Inverted-U preference shifts with repetition; preferences move toward expected outcomes under uncertainty (behavioral + IDyOM, N=43+27, quadratic IC+entropy p<0.05)
- **Cheung et al. 2019**: Low uncertainty + high surprise = maximal pleasure; saddle-shaped surface (fMRI, N=39+40, R2_marginal=0.476)
- **Sarasso et al. 2021**: Aesthetic emotions help tolerate predictive uncertainty; aesthetic attitude reorients attention to learning (theoretical)
- **Harding et al. 2025**: Psilocybin maintained surprise-related pleasure vs escitalopram reduction; dissociable treatment effects on hedonic processing (fMRI RCT, N=41 MDD, between-group p<0.05)
- **Mas-Herrero et al. 2014**: Musical anhedonia — individual differences in reward sensitivity modulate appreciation trajectory (behavioral + SCR/HR, N=30, R2=0.32)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/maa/forecast.py`
