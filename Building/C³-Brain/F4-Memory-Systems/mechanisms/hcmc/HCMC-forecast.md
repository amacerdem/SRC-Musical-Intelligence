# HCMC F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [8:11]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:consolidation_fc | [0, 1] | Consolidation prediction (5-36s ahead). Hippocampal replay trajectory -- predicts whether current trace will successfully consolidate into cortical storage. Based on stumpf_fusion stability at H24 and entropy stability at H24. Buzsaki 2015: sharp-wave ripples forecast consolidation outcome. |
| 9 | F1:retrieval_fc | [0, 1] | Retrieval probability prediction (1-5s ahead). Pattern completion trajectory -- predicts likelihood that current musical context will trigger recognition/recall. Based on harmonicity autocorrelation at H20 and tonalness repetition. Biau et al. 2025: theta reinstatement during retrieval. |
| 10 | F2:pattern_compl_fc | [0, 1] | Pattern completion prediction (0.5-2s ahead). Hippocampal cue-to-cortical reconstruction forecast -- predicts whether partial melodic input will trigger full pattern completion. Based on stumpf_fusion mean at H16 and x_l0l5 binding strength. Rolls 2013: CA3 pattern completion. |

---

## Design Rationale

1. **Consolidation Forecast (F0)**: Predicts whether the hippocampal trace currently being formed will successfully transfer to cortical long-term storage. Uses long-horizon (H24, 36s) stability features. High consolidation forecast occurs when patterns are stable and coherent over extended time windows.

2. **Retrieval Forecast (F1)**: Predicts the probability that a retrieval event will occur in the near future (1-5s). Based on autocorrelation features that detect repetition -- when musical patterns repeat, hippocampal pattern completion is triggered. Feeds the Anticipation belief system.

3. **Pattern Completion Forecast (F2)**: The shortest-horizon prediction -- will the next 0.5-2s of music trigger hippocampal pattern completion? This is the "I know what comes next" signal. High values indicate the listener has a strong template and the incoming signal matches it.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 24, 19, 0) | stumpf_fusion stability H24 L0 | Long-term binding stability for consolidation forecast |
| (22, 24, 19, 0) | entropy stability H24 L0 | Pattern stability over 36s for consolidation forecast |
| (5, 24, 22, 0) | harmonicity autocorrelation H24 L0 | Harmonic repetition for retrieval forecast |
| (14, 20, 22, 0) | tonalness autocorrelation H20 L0 | Tonal repetition for retrieval forecast |
| (3, 16, 1, 2) | stumpf_fusion mean H16 L2 | Binding coherence for pattern completion |

F-layer primarily reuses E+M outputs and long-horizon H3 tuples for trajectory prediction.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:consolidation_fc | F8 Learning | Consolidation trajectory for learning rate |
| F1:retrieval_fc | F6 Reward | Familiarity-based reward prediction |
| F1:retrieval_fc | F5 Emotion | Nostalgia/recognition emotion |
| F2:pattern_compl_fc | F2 Prediction | Pattern completion feeds prediction engine |
| F2:pattern_compl_fc | Precision engine | pi_pred estimation for memory-related beliefs |

---

## Scientific Foundation

- **Buzsaki 2015**: Sharp-wave ripples drive hippocampal-cortical transfer and forecast consolidation outcome (review)
- **Rolls 2013**: CA3 autoassociative network supports pattern completion from partial cues (computational)
- **Biau et al. 2025**: Theta reinstatement during memory recall (MEG, N=23)
- **Cheung et al. 2019**: Hippocampal encoding of uncertainty predicts future memory (fMRI, N=79)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/hcmc/forecast.py`
