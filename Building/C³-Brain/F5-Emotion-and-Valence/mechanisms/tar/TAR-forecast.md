# TAR F-Layer — Forecast (2D)

**Layer**: Future Predictions (F)
**Indices**: [8:10]
**Scope**: exported (kernel relay: mood_improv_pred, stress_reduc_pred)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:mood_improv_pred | [0, 1] | Predicted mood improvement (10-30 min ahead). mood_pred = sigma(0.4 * therapeutic_reward + 0.3 * valence_mod + 0.3 * depression_improvement). Based on dose-response model trajectory: Effect(t) = E_max * (1 - exp(-t / tau_onset)) * exp(-max(0, t - t_peak) / tau_decay), where tau_onset ~ 10 min, t_peak ~ 30 min. Kheirkhah 2025: music therapy for depression, d = 0.88. |
| 9 | F1:stress_reduc_pred | [0, 1] | Predicted stress/cortisol reduction (5-15 min ahead). stress_pred = sigma(0.4 * anxiety_reduction + 0.3 * predictability + 0.3 * warmth). Based on autonomic pathway activation and the relaxation response — cortisol reduction follows PNS activation with a 5-15 min delay. Thoma 2013: music reduces cortisol via autonomic stress pathway (RCT, N=60). |

---

## Design Rationale

1. **Mood Improvement Prediction (F0)**: Forecasts the trajectory of mood improvement over the 10-30 minute therapeutic window. Uses the present-moment therapeutic reward (is the music working now?), valence modulation target (does the music have antidepressant properties?), and depression improvement signal (condition-specific efficacy). The dose-response model predicts that effects build during the first 10 minutes, peak around 30 minutes, and then gradually decay. This prediction enables adaptive therapeutic dose management.

2. **Stress Reduction Prediction (F1)**: Forecasts cortisol reduction over the 5-15 minute autonomic response window. Uses anxiety reduction potential (primary anxiolytic signal), predictability (familiar, predictable music reduces the uncertainty that drives stress), and warmth (timbral comfort signal). Cortisol reduction is mediated by the parasympathetic pathway, which has a shorter time constant than mood improvement — hence the 5-15 min prediction window vs 10-30 min for mood.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:mood_improv_pred | F6 Reward | PE from therapeutic mood prediction |
| F0:mood_improv_pred | F5 Emotion | Anticipated emotional trajectory |
| F1:stress_reduc_pred | F3 Attention | Predicted relaxation for attention allocation |
| F1:stress_reduc_pred | Precision engine | pi_pred estimation for stress trajectory |

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 15, 1, 0) | sensory_pleasantness mean H15 L0 | Peak response for mood trajectory |
| (4, 16, 18, 0) | sensory_pleasantness trend H16 L0 | Mood trend for improvement prediction |
| (0, 15, 18, 0) | roughness trend H15 L0 | Consonance trajectory for stress prediction |
| (10, 16, 1, 0) | loudness mean H16 L0 | Sustained arousal context |
| (8, 15, 8, 0) | velocity_A velocity H15 L0 | Tempo dynamics at peak scale |
| (7, 7, 8, 0) | amplitude velocity H7 L0 | Energy change for breakthrough detection |

F-layer also reuses T+I+P outputs for integrated predictions.

---

## Scientific Foundation

- **Kheirkhah et al. 2025**: Music + ketamine + mindfulness for treatment-resistant depression — dose-response evidence for mood improvement trajectory (RCT, d=0.88, Journal of Affective Disorders)
- **Thoma et al. 2013**: Music reduces cortisol via autonomic stress pathway — 5-15 min onset for physiological stress reduction (RCT, N=60, PLOS ONE, 8(8), e70156)
- **Bradt & Dileo 2014**: Music interventions show consistent anxiety reduction across 26 RCTs, supporting stress prediction validity (meta-analysis, d ~ 0.5-0.8, Cochrane Database)
- **Fu et al. 2025**: Music therapy modulates synaptic plasticity, oxidative stress, and inflammation — mechanistic basis for mood improvement prediction (mouse model, Translational Psychiatry, 15, 143)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/tar/forecast.py`
