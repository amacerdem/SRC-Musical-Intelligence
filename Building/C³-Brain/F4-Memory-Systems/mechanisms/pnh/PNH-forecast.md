# PNH F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [8:11]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:dissonance_res_fc | [0, 1] | Dissonance resolution prediction (0.5-2s ahead). Based on struct_expect trajectory over H14 (700ms) window. Predicts whether current dissonance will resolve to consonance. Harrison & Pearce 2020: consonance = interference + harmonicity + cultural familiarity (3-factor model). |
| 9 | F1:pref_judgment_fc | [0, 1] | Preference judgment prediction (1-3s ahead). Consonance-to-pleasure mapping over H18 (2s) window. Predicts the upcoming aesthetic response. Sarasso et al. 2019: consonance drives aesthetic judgment (eta_p^2=0.685); memorization of preferred intervals (d=0.474). |
| 10 | F2:expertise_mod_fc | [0, 1] | Expertise modulation forecast. Training-dependent sensitivity prediction over H14 (700ms) window. Predicts whether musician-specific processing will engage. Schon et al. 2005: musicians N1-P2 (100-200ms) vs non-musicians N2 (200-300ms). |

---

## Design Rationale

1. **Dissonance Resolution Prediction (F0)**: The harmonic prediction of the Pythagorean system. Forecasts whether the current dissonant interval (high ratio complexity) will resolve to a consonant one. Uses the structural expectation trajectory to predict harmonic motion. The tritone resolves to a fifth; the minor second resolves to a unison. This generates prediction error when resolution is violated.

2. **Preference Judgment Prediction (F1)**: Forecasts the upcoming aesthetic evaluation. Uses the consonance-to-pleasure mapping over the phrase-level window (H18, 2s) to predict whether the listener will find the upcoming harmonies pleasant. Sarasso et al. 2019 showed memorization is enhanced for preferred intervals (d=0.474), linking PNH to memory through preference.

3. **Expertise Modulation Forecast (F2)**: Predicts whether the musician-specific expanded cortical representation will engage. Uses the familiarity trajectory to estimate whether the upcoming interval progression will benefit from musical training. In musicians, expertise_mod_fc is higher and engages earlier, reflecting the 100ms timing advantage (Schon et al. 2005).

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (2, 18, 1, 0) | helmholtz_kang mean H18 L0 | Harmonic template over phrase — resolution trajectory |

F-layer primarily reuses H+M+P outputs rather than reading new H3 tuples directly.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:dissonance_res_fc | F6 Reward | PE from harmonic resolution prediction |
| F1:pref_judgment_fc | F5 Emotion | Aesthetic-emotional evaluation |
| F2:expertise_mod_fc | F8 Learning | Training-dependent processing forecast |

---

## Scientific Foundation

- **Harrison & Pearce 2020**: 3-factor consonance model — interference + harmonicity + cultural familiarity (computational model, N=500+ reanalysis)
- **Sarasso et al. 2019**: Consonance-preference-attention link; preferred interval memorization d=0.474 (EEG+behavioral, N=22)
- **Schon et al. 2005**: Musicians N1-P2 (100-200ms) vs non-musicians N2 (200-300ms) for consonance processing (ERP, N=20)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/pnh/forecast.py`
