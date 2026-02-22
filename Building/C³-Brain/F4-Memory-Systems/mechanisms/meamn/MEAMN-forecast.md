# MEAMN F-Layer — Forecast (4D)

**Layer**: Future Predictions (F)
**Indices**: [8:12]
**Scope**: exported (kernel relay: mem_vividness_fc, emo_response_fc, self_ref_fc)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:mem_vividness_fc | [0, 1] | Memory vividness prediction (2-5s ahead). Hippocampal activation trajectory — predicts whether an autobiographical memory will become more or less vivid. Based on H20 (5s) consolidation window. Janata 2009: imagery vividness strong vs weak autobiographical (t(9)=5.784). |
| 9 | F1:emo_response_fc | [0, 1] | Emotional response prediction (1-3s ahead). Amygdala engagement trajectory — predicts the upcoming emotional intensity of the memory experience. Based on H16 (1s) encoding window. Janata 2009: emotional evocation strong vs weak (t(9)=3.442, p<0.008). |
| 10 | F2:self_ref_fc | [0, 1] | Self-referential prediction (5-10s ahead). mPFC activation trajectory — predicts whether the listener will enter self-referential processing mode. Based on H24 (36s) long-term window. Janata 2009: mPFC self-referential processing. |
| 11 | F3:(reserved) | [0, 1] | Future expansion. Currently outputs zeros. Reserved for potential integration of age-at-encoding factor (reminiscence bump, Janata et al. 2007). |

---

## Design Rationale

1. **Memory Vividness Prediction (F0)**: The temporal prediction of memory recall quality. Uses the hippocampal retrieval trajectory over the 5s consolidation window (H20) to forecast whether the listener's autobiographical memory will sharpen or fade. High values predict vivid, detailed recall is approaching.

2. **Emotional Response Prediction (F1)**: Forecasts the upcoming emotional intensity of the memory experience. Uses the amygdala engagement trajectory over the 1s encoding window (H16) to predict emotional coloring of upcoming memory retrieval. Feeds the reward system for PE estimation.

3. **Self-Referential Prediction (F2)**: Predicts entry into mPFC-mediated self-referential processing — the "this is about me" experience. Uses the long-term window (H24, 36s) to track whether the listener is building toward a deep autobiographical connection with the music.

4. **Reserved (F3)**: Placeholder for future integration of the reminiscence bump effect (ages 10-30 showing strongest music-evoked recall) or other developmental memory factors.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (7, 20, 4, 0) | amplitude max H20 L0 | Peak energy over 5s — vividness trajectory |
| (10, 24, 3, 0) | loudness std H24 L0 | Arousal variability over 36s — self-referential buildup |
| (22, 24, 19, 0) | entropy stability H24 L0 | Pattern stability over 36s — familiarity trajectory |

F-layer primarily reuses E+M+P outputs rather than reading new H3 tuples directly.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:mem_vividness_fc | F6 Reward | PE from memory vividness prediction |
| F1:emo_response_fc | F5 Emotion | Emotional trajectory forecasting |
| F2:self_ref_fc | Precision engine | pi_pred estimation for self-referential processing |
| F3:(reserved) | — | Future expansion |

---

## Scientific Foundation

- **Janata 2009**: Imagery vividness strong vs weak autobiographical (t(9)=5.784, p<0.0003); emotional evocation (t(9)=3.442, p<0.008); mPFC self-referential processing (fMRI 3T, N=13)
- **Janata et al. 2007**: Reminiscence bump ages 10-30; 30%+ MEAM trigger rate (behavioral, N~300)
- **Tulving 2002**: Episodic memory requires coherent feature binding (review)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/meamn/forecast.py`
