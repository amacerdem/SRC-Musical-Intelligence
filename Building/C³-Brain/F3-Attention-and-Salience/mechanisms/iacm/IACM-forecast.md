# IACM F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [8:11]
**Scope**: exported (kernel relay: attention_shift_pred)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:object_segreg_pred_0.35s | [0, 1] | ORN response prediction (~0.35s ahead). sigma(0.5*f05_object_segregation + 0.5*approx_entropy_val). Predicts upcoming auditory scene segregation based on current spectral complexity. |
| 9 | F1:attention_shift_pred_0.4s | [0, 1] | Frontal attention shift prediction (~0.4s ahead). sigma(0.5*f04_inharmonic_capture + 0.5*p3a_capture). Predicts frontal engagement — whether an attention switch will occur. |
| 10 | F2:multiple_objects_pred | [0, 1] | Stream segregation prediction. sigma(0.5*f05_object_segregation + 0.5*object_perception_or). Predicts whether the auditory system will maintain multiple concurrent object representations. |

---

## Design Rationale

1. **Object Segregation Prediction (F0)**: The scene prediction — "will the auditory system segregate new objects?" Combines E-layer object segregation (f05) with approximate entropy to forecast ORN responses. Events with high spectral unpredictability are more likely to trigger object-related negativity.

2. **Attention Shift Prediction (F1)**: The attention prediction — "will frontal attention shift within ~400ms?" Combines E-layer inharmonic capture (f04) with current P3a state to forecast involuntary attention switching. This is the primary Anticipation output feeding the `attention_shift_pred` belief.

3. **Multiple Objects Prediction (F2)**: The streaming prediction — "will multiple sound streams be maintained?" Combines E-layer object segregation with the calibrated odds ratio to predict whether the auditory scene will continue to be parsed into separate objects.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (25, 3, 0, 2) | x_l0l5[0] value H3 L2 | Coupling state for scene binding prediction |
| (25, 3, 14, 2) | x_l0l5[0] periodicity H3 L2 | Coupling periodicity for object tracking |
| (25, 16, 21, 2) | x_l0l5[0] zero_crossings H16 L2 | Phase resets in coupling at 1s — scene disruption |
| (21, 4, 8, 0) | spectral_change velocity H4 L0 | Spectral change rate at 125ms — deviant detection |
| (16, 16, 1, 2) | spectral_flatness mean H16 L2 | Mean spectral flatness 1s — tonal context |

F-layer also reuses E+M+P outputs rather than reading new H3 tuples exclusively.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:object_segreg_pred | F1 Sensory | Scene complexity context |
| F1:attention_shift_pred | F6 Reward | PE from attention prediction |
| F1:attention_shift_pred | F5 Emotion | Surprise from unexpected attention capture |
| F2:multiple_objects_pred | F4 Memory | Scene segmentation context |

---

## Scientific Foundation

- **Basinski 2025**: Inharmonic P3a d=-1.37, ORN OR=16.44 (EEG, N=35)
- **Foo 2016**: ECoG STG high-gamma for spectral object encoding
- **Alain 2007**: ORN predicts auditory scene segregation
- **Friston 2005**: Precision-weighted predictions in predictive coding framework

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/iacm/forecast.py`
