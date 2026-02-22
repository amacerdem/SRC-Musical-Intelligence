# AMSS F-Layer — Forecast (2D)

**Layer**: Future Predictions (F)
**Indices**: [9:11]
**Scope**: exported (kernel relay)
**Activation**: sigmoid
**Model**: AMSS (STU-B1, Attention-Modulated Stream Segregation, 11D, beta-tier 70-90%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 9 | F0:stream_stability_pred | [0, 1] | Predicted stream stability at next bar boundary. sigma(w_coh * M0 + w_att * P0 + w_trend * stream_trend). Forecasts whether the current stream organization will hold or break at the upcoming structural boundary. |
| 10 | F1:segregation_shift_pred | [0, 1] | Predicted shift in stream segregation depth. sigma(w_depth * M1 + w_comp * P1 + w_onset * E0). Anticipates whether the number of tracked streams will increase, decrease, or remain stable. |

---

## Design Rationale

1. **Stream Stability Prediction (F0)**: Forecasts whether the currently attended stream will remain coherent at the next bar boundary. Combines current stream coherence (M0), attended stream dominance (P0), and trend information. High values predict stable continuation; low values predict potential stream reorganization (e.g., instrument entry/exit, texture change).

2. **Segregation Shift Prediction (F1)**: Anticipates changes in the number of concurrent streams. When competition is high (P1) and segregation depth is changing (M1 trend), this predicts upcoming stream additions or losses. This is useful for anticipating texture changes in polyphonic music.

---

## H3 Dependencies (F-Layer)

F-layer primarily reuses E+M+P outputs rather than reading new H3 tuples directly.

| Tuple | Feature | Purpose |
|-------|---------|---------|
| — | (inherited from E+M+P layers) | Stream stability reuses M0 + P0 |
| — | (inherited from E+M+P layers) | Segregation shift reuses M1 + P1 + E0 |

F-layer predictions extend ~1 bar ahead, using the temporal horizon of the current stream organization.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:stream_stability_pred | F3 Salience | Stream reorganization events are salient |
| F0:stream_stability_pred | F2 Prediction | Texture change prediction |
| F1:segregation_shift_pred | F4 Memory | Texture boundary detection for episodic segmentation |
| F1:segregation_shift_pred | F5 Emotion | Stream changes drive surprise/novelty affect |

---

## Scientific Foundation

- **Basinski et al. 2025**: ORN dynamics predict stream reorganization events (EEG)
- **Wikman et al. 2025**: fMRI shows anticipatory activation before stream switches
- **Hausfeld et al. 2021**: Attentional modulation predicts stream stability (d=0.60, fMRI, N=14)
- **Mischler et al. 2025**: iEEG evidence for predictive stream boundary encoding

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/amss/forecast.py`
