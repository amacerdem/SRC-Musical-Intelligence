# MIAA F-Layer — Forecast (3D)

**Layer**: Forecast (F)
**Indices**: [8:11]
**Scope**: external
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|------------------|
| 8 | F0:melody_continuation_pred | [0, 1] | Predicted imagery content for next phrase. σ(0.50×E0 + 0.30×P0 + 0.20×P1). |
| 9 | F1:ac_activation_pred | [0, 1] | Predicted AC activation during upcoming gap. σ(0.60×E1 + 0.40×E0). Familiarity drives sustained AC in silence. |
| 10 | F2:recognition_pred | [0, 1] | Predicted familiar-match probability at gap resolution. σ(0.50×E1 + 0.30×spectral_auto_mean + 0.20×tonalness_mean). |

---

## Design Rationale

Three forward predictions for imagery:

1. **Melody Continuation (F0)**: Will the imagery continue? Combines current imagery activation (E0), template retrieval (P0), and continuation prediction (P1). High values = imagery stream will persist.

2. **AC Activation (F1)**: Will auditory cortex remain active during the upcoming silent gap? Dominated by familiarity (E1, 0.60) — familiar music sustains AC activation longer. Base imagery (E0, 0.40) provides the activation floor.

3. **Recognition (F2)**: Will the listener recognize the next sound as matching the imagined template? Familiarity (E1) is primary, cross-band coherence (spectral_auto_mean at 300ms) indicates template stability, tonal quality (tonalness_mean) adds clarity. This is the prediction consumed by the imagery_recognition belief.

---

## H³ Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (17, 8, 1, 0) | spectral_auto mean H8 L0 | Cross-band coherence for recognition |
| (14, 5, 1, 0) | tonalness mean H5 L0 | Tonal quality context (reused) |

---

## Belief Consumption

```
MIAA beliefs
└── imagery_recognition (Anticipation) ← F2:recognition_pred (idx 10)
```

---

## Scientific Foundation

- **Kraemer 2005**: AC active during silent gaps in familiar music
- **Halpern 2004**: Familiar music produces more vivid imagery
- **Di Liberto 2021**: Imagery pitch decoding comparable to perception

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/miaa/forecast.py`
