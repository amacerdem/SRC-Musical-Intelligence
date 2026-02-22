# DAP F-Layer — Forecast (2D)

**Layer**: Future Predictions (F)
**Indices**: [8:10]
**Scope**: exported (kernel relay: adult_hedonic_pred, preference_stab)
**Activation**: clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 8 | F0:adult_hedonic_pred | [0, 1] | Predicted adult hedonic capacity. adult_hedonic = clamp(0.6 * exposure + 0.4 * response, 0, 1). Long-range forecast of the listener's ceiling for musical pleasure based on developmental exposure history (60% weight) and genetic/constitutional baseline (40% weight). Trainor 2012: early musical training predicts enhanced adult processing. |
| 9 | F1:preference_stab | [0, 1] | Preference stability index. preference_stability = maturation. High when past the critical period — mature listeners have stable, crystallized musical preferences. Low during development — preferences are still forming and malleable. Trehub 2003: preference patterns emerge progressively during development. |

---

## Design Rationale

1. **Adult Hedonic Prediction (F0)**: Forecasts the listener's ceiling for musical pleasure. The 0.6/0.4 weighting reflects the estimated environment/genetics split for hedonic capacity development — early musical enrichment contributes ~60% while genetic/constitutional factors contribute ~40%. This is a trait-level prediction that changes slowly over developmental timescales.

2. **Preference Stability (F1)**: Predicts how stable the listener's musical preferences currently are. Directly mapped from neural maturation — mature circuits produce stable preferences, while developing circuits allow preference change. High stability predicts low sensitivity to novel music exposure; low stability predicts high openness to new musical experiences.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:adult_hedonic_pred | F6 Reward | Ceiling estimate for reward magnitude |
| F0:adult_hedonic_pred | F5 Emotion | Developmental modulation of affective ceiling |
| F1:preference_stab | F4 Memory | Stability of musical preference memory traces |
| F1:preference_stab | Precision engine | pi_pred for preference prediction |

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 16, 18, 0) | sensory_pleasantness trend H16 L0 | Hedonic trajectory — maturation direction |
| (22, 16, 19, 0) | entropy stability H16 L0 | Pattern stability — preference crystallization |

F-layer primarily reuses D+P outputs rather than reading new H3 tuples directly.

---

## Scientific Foundation

- **Trainor & Unrau 2012**: Early musical training predicts enhanced adult auditory processing and hedonic capacity (review, Springer Handbook)
- **Trehub 2003**: Musical preference patterns emerge progressively during development; innate predispositions interact with exposure (review, Nature Neuroscience, 6(7), 669-673)
- **Qiu et al. 2025**: Prenatal musical intervention produces lasting neuroplastic changes — evidence for long-range hedonic prediction (mouse model, Translational Psychiatry)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/dap/forecast.py`
