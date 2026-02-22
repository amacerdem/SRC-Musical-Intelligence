# SDED F-Layer — Forecast (3D)

**Layer**: Forecast (F)
**Indices**: [7:10]
**Scope**: external
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:dissonance_detection_pred | [0, 1] | Predicted dissonance detection. sigma(0.60*E0 + 0.40*helmholtz_mean). Next-frame roughness expectation from current detection + consonance context. |
| 8 | F1:behavioral_accuracy_pred | [0, 1] | Predicted behavioral accuracy. sigma(0.50*E0 + 0.50*E1). Combined detection signals predict behavioral readout. |
| 9 | F2:training_effect_pred | [0, 1] | Training effect prediction. sigma(0.70*E1 + 0.30*M0). Neural (M0) stays constant, behavioral (E1) improves with training. |

---

## Design Rationale

Three forward predictions for dissonance processing:

1. **Dissonance Detection (F0)**: Current early detection (E0, 0.60) predicts next-frame dissonance. Helmholtz mean (0.40) provides consonance context — high consonance context suggests the dissonance may resolve.

2. **Behavioral Accuracy (F1)**: Combines early detection and MMN signals equally. Predicts how accurately the listener will behaviorally discriminate the next dissonance event.

3. **Training Effect (F2)**: Models the neural-behavioral dissociation at the prediction level. MMN signal (E1, 0.70) dominates because training primarily enhances behavioral readout. Detection function (M0, 0.30) provides the neural constant.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (2, 3, 1, 2) | helmholtz mean H3 L2 | Consonance context for prediction (reused) |

---

## Belief Consumption

```
SDED beliefs
└── spectral_complexity (Appraisal) — uses M0, P0, P1 (not F-layer)
```

---

## Scientific Foundation

- **Crespo-Bojorque 2018**: Training effect — late MMN ONLY in musicians
- **Bidelman 2013**: Brainstem hierarchy is constant (innate), behavioral varies

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/sded/forecast.py`
