# ETAM F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [8:11]
**Scope**: exported (kernel relay)
**Activation**: sigmoid
**Model**: ETAM (STU-B4, Entrainment Tempo & Attention Modulation, 11D, beta-tier 70-90%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:tracking_prediction | [0, 1] | sigma(0.5*f01 + 0.3*groove_trend + 0.2*entrainment_index). Predicted tracking quality at next bar boundary. Early window (E0) provides the onset basis, groove trend extrapolates temporal dynamics, entrainment index (M1) anchors the prediction. Doelling & Poeppel 2015: entrainment predicts future tracking. |
| 9 | F1:attention_sustain | [0, 1] | sigma(0.40*attention_gain + 0.30*loud_mean_beat + 0.30*loud_trend_long). Predicted attention sustainability over upcoming bars. Combines current attention gain (M0) with loudness trajectory — sustained loudness supports sustained attention. Aparicio-Terres 2025: tempo modulates attention sustainability. |
| 10 | F2:segregation_predict | [0, 1] | sigma(0.4*f03 + 0.3*f04 + 0.3*stream_entropy). Predicted segregation depth at next structural boundary. Late window (E2) and instrument asymmetry (E3) extrapolate whether stream organization will become more or less complex. Basinski 2025: ORN dynamics anticipate segregation changes. |

---

## Design Rationale

1. **Tracking Prediction (F0)**: Forecasts how well the listener will track the attended stream at the next bar boundary. The early window (E0, weight 0.5) is the strongest predictor because current onset tracking quality is the best indicator of future tracking. Groove trend (0.3) captures whether tracking is improving or degrading, and entrainment index (M1, 0.2) provides the rhythmic context.

2. **Attention Sustain (F1)**: Predicts whether attention can be maintained over the next few bars. Current attention gain (M0, 0.40) is the baseline. Loudness mean at beat level (0.30) and long-term loudness trend (0.30) capture whether the acoustic environment supports sustained attention — fading dynamics predict attention dropout, while crescendo predicts sustained engagement.

3. **Segregation Predict (F2)**: Anticipates changes in stream complexity. Uses the same features as stream_separation (P1) but oriented toward prediction: if late-window entropy is increasing and instrument asymmetry is high, segregation demands are likely to increase (e.g., a new voice entering). This helps the system prepare processing resources for upcoming complexity changes.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (33, 16, 18, 0) | x_l4l5 trend H16 L0 | F0: groove trend for tracking prediction |
| (8, 14, 1, 0) | loudness mean H14 L0 | F1: loudness at beat scale for sustain prediction |
| (8, 20, 18, 0) | loudness trend H20 L0 | F1: long-term loudness trajectory for sustain |

F2 reuses E2 (late_window) and E3 (instrument_asymmetry) outputs — no new H3 tuples.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:tracking_prediction | F2 Prediction | Expected tracking quality for prediction confidence |
| F0:tracking_prediction | F6 Reward | Tracking quality PE drives learning signals |
| F1:attention_sustain | F5 Emotion | Sustained attention predicts emotional engagement |
| F1:attention_sustain | Precision engine | pi_pred estimation for attention-related beliefs |
| F2:segregation_predict | F4 Memory | Texture boundary anticipation for episodic segmentation |
| F2:segregation_predict | F1 Sensory | Predicted complexity adjusts sensory gain |

---

## H3 Tuple Summary (Full ETAM Model, 20 tuples)

```
E-layer (11 tuples):
  (7,6,0,2), (7,6,4,2), (8,6,0,0), (11,6,0,0)      — E0 early window
  (10,11,0,0), (21,8,1,0), (22,11,8,0)                — E1 middle window
  (25,16,0,2), (41,14,1,0), (41,14,13,0)              — E2 late window
  (24,14,3,0)                                           — E3 instrument asymmetry

M-layer (2 tuples):
  (22,11,14,2), (25,16,14,2)                           — M1 entrainment index

P-layer (1 tuple):
  (33,16,0,2)                                           — P1 stream separation

F-layer (3 tuples):
  (33,16,18,0)                                          — F0 tracking prediction
  (8,14,1,0), (8,20,18,0)                              — F1 attention sustain

Additional E-layer tuples used in F-layer formulas:
  (10,11,17,0)                                          — flux periodicity for groove
  (21,8,3,0)                                            — spectral_change std
  (24,8,0,0)                                            — timbre_change value

Total: 20 unique H3 tuples
```

---

## Scientific Foundation

- **Doelling & Poeppel 2015**: Entrainment predicts future tracking quality in musicians (MEG)
- **Aparicio-Terres et al. 2025**: Tempo modulates attention sustainability — slow tempi allow longer sustained attention
- **Pesnot Lerousseau et al. 2021**: High-gamma activity forecasts attention deployment (iEEG)
- **Hausfeld et al. 2021**: Three delay windows show predictive temporal structure (d=0.60-0.68, fMRI, N=14)
- **Basinski et al. 2025**: ORN dynamics anticipate stream reorganization events (EEG)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/etam/forecast.py`
