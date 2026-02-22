# NEMAC F-Layer — Forecast (2D)

**Layer**: Future Predictions (F)
**Indices**: [9:11]
**Scope**: exported (kernel relay: wellbeing_pred, vividness_pred)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 9 | F0:wellbeing_pred | [0, 1] | Well-being improvement prediction (5-30s ahead). wellbeing_pred = sigma(nostalgia_intensity * 0.7). Forecasts the trajectory of mood improvement based on current nostalgia intensity and the dose-response relationship (beta ~ 0.7). Sakakibara 2025: N-BMI loop enhances well-being through nostalgia engagement (EEG, N=33). |
| 10 | F1:vividness_pred | [0, 1] | Memory vividness prediction (2-5s ahead). vividness_pred = sigma(hippocampus + 0.3 * buildup_tracking_mean). Hippocampal activation trajectory predicts whether autobiographical memory clarity will increase or decrease. Uses buildup tracking H3 to detect approaching peak nostalgia moments. Janata 2009: imagery vividness strong vs weak autobiographical (t(9)=5.784, p<0.0003). |

---

## Design Rationale

1. **Well-being Prediction (F0)**: Forecasts the mood improvement trajectory based on current nostalgia intensity. The 0.7 coefficient reflects the estimated nostalgia-to-wellbeing transfer rate — strong nostalgia predicts strong mood improvement within a 5-30s window. This prediction enables the kernel to anticipate therapeutic benefit and modulate attention/salience accordingly.

2. **Vividness Prediction (F1)**: Forecasts whether autobiographical memory recall will become more vivid. Uses hippocampal activation (current memory retrieval strength) plus a buildup tracking signal from H3 to detect approaching peak nostalgic moments. When buildup is high, the prediction anticipates a "nostalgia breakthrough" — a moment of suddenly vivid autobiographical recall.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:wellbeing_pred | F6 Reward | PE from well-being prediction |
| F0:wellbeing_pred | F5 Emotion | Anticipated emotional trajectory |
| F1:vividness_pred | F4 Memory | Memory vividness trajectory forecasting |
| F1:vividness_pred | Precision engine | pi_pred estimation for memory prediction |

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 20, 1, 0) | loudness mean H20 L0 | Arousal trajectory over 5s for wellbeing prediction |
| (3, 20, 1, 2) | stumpf_fusion mean H20 L2 | Binding trajectory for vividness prediction |
| (22, 20, 19, 0) | entropy stability H20 L0 | Pattern stability for familiarity trajectory |

F-layer primarily reuses E+M+W+P outputs rather than reading new H3 tuples directly.

---

## Scientific Foundation

- **Sakakibara 2025**: N-BMI loop: nostalgia → well-being enhancement validated experimentally; memory vividness enhanced by nostalgia engagement (EEG + behavioral, N=33, eta_p^2=0.541)
- **Janata 2009**: Imagery vividness strong vs weak autobiographical (fMRI 3T, N=13, t(9)=5.784, p<0.0003)
- **Barrett et al. 2010**: Nostalgia-wellbeing link modulated by personality traits (behavioral, N=226)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/nemac/forecast.py`
