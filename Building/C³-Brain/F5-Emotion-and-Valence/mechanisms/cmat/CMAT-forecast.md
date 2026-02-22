# CMAT F-Layer — Forecast (2D)

**Layer**: Future Predictions (F)
**Indices**: [8:10]
**Scope**: exported (kernel relay: coherence_pred, generalization_pr)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:coherence_pred | [0, 1] | Predicted emotional coherence (1-2s ahead). coherence_pred = sigma(0.4 * binding_temporal + 0.3 * congruence + 0.3 * (1.0 - integration_var)). Forecasts whether the unified multi-sensory percept will stabilize. High binding precision + high congruence + low variability = coherent emotional experience approaching. Spence 2011: congruent cross-modal stimuli produce more stable percepts. |
| 9 | F1:generalization_pr | [0, 1] | Cross-modal generalization potential (2-3s ahead). generalization = f13 * binding_temporal * congruence. Triple product forecasts the transfer potential — how strongly the current affective experience will generalize across modalities. High when all three factors (cross-modal quality, temporal precision, and congruence) are simultaneously elevated. Tsuji 2025: habituation transfers across modalities in infants. |

---

## Design Rationale

1. **Coherence Prediction (F0)**: Forecasts whether the unified emotional experience will become more coherent. Uses a weighted combination of binding temporal precision (how well-timed the cross-modal integration is), congruence strength (how well the modalities agree emotionally), and integration stability (inverse of variability). This prediction enables the kernel to anticipate stable affective states and modulate attention accordingly.

2. **Generalization Prediction (F1)**: Forecasts the cross-modal transfer potential. Uses the triple product of cross-modal transfer strength (from E-layer), binding precision (from T-layer), and congruence (from T-layer). The multiplicative gate ensures that generalization requires all three conditions — transfer quality, temporal precision, and affective agreement — to be simultaneously high. This is relevant for therapeutic design (CMAT informs TAR about multi-modal intervention effectiveness).

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:coherence_pred | F3 Attention | Predicted perceptual stability for attention allocation |
| F0:coherence_pred | Precision engine | pi_pred estimation for multi-sensory coherence |
| F1:generalization_pr | F5 Emotion | Cross-modal generalization forecast |
| F1:generalization_pr | TAR | Multi-modal therapeutic intervention effectiveness |

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 11, 2, 0) | sensory_pleasantness std H11 L0 | Integration variability for coherence prediction |
| (22, 16, 19, 0) | entropy stability H16 L0 | Pattern stability for generalization trajectory |

F-layer primarily reuses E+S+T+P outputs rather than reading new H3 tuples directly.

---

## Scientific Foundation

- **Spence 2011**: Congruent cross-modal stimuli produce more stable and coherent unified percepts (tutorial review, Attention, Perception, & Psychophysics, 73(4), 971-995)
- **Tsuji & Cristia 2025**: Habituation transfers across modalities — demonstrated in infant speech and music perception; evidence for cross-modal generalization mechanism (behavioral)
- **Molholm et al. 2002**: Temporal binding window constrains cross-modal coherence — events outside +/-100ms fail to bind (ERP, N=10, Cognitive Brain Research)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/cmat/forecast.py`
