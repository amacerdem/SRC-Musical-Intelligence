# HMCE — Cognitive Present

**Model**: Hierarchical Musical Context Encoding
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: P — Cognitive Present
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | a1_stg_encoding | Current auditory cortex encoding state. Measures real-time neural encoding strength at primary and secondary auditory cortex. High values = strong stimulus representation in spectrotemporal domain. Maps to A1/HG + STG. Forseth 2020: high-gamma activation in HG within 110ms of stimulus. |
| 7 | context_predict | Current context-based prediction state. Measures the strength of top-down prediction from accumulated context. High values = confident structural predictions. Maps to IFG→STG top-down pathway. Rimmele 2021: IFG chunks phrases for prediction. |
| 8 | phrase_expect | Current phrase expectation level. Measures whether the system expects a phrase boundary or continuation based on accumulated context. High values = phrase boundary expected. Maps to ACC evaluation of structural transitions. Bonetti 2024: cingulate assumes top position at final tone. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 7 | 3 | M0 (value) | L0 | Amplitude at 100ms — current encoding strength |
| 1 | 11 | 3 | M0 (value) | L0 | Onset strength at 100ms — event detection |
| 2 | 17 | 8 | M14 (periodicity) | L0 | Spectral autocorrelation periodicity 500ms — prediction confidence |
| 3 | 60 | 3 | M0 (value) | L0 | Tonal stability at 100ms — current harmonic state |

---

## Computation

The P-layer computes the real-time state of the hierarchical context encoding system:

1. **A1/STG encoding** (idx 6): Current bottom-up encoding strength from amplitude + onset. Higher when stimulus is strong and well-defined. Maps to Forseth 2020's high-gamma in HG (110ms latency).

2. **Context prediction** (idx 7): Top-down prediction strength from accumulated context. Combines context_depth (M-layer) with spectral autocorrelation periodicity — stable periodicity means confident predictions. Maps to the IFG→STG feedback loop.

3. **Phrase expectation** (idx 8): Phrase boundary detection from transition dynamics (M-layer) + tonal stability. When tonal stability drops sharply while transition dynamics are high, a phrase boundary is expected. Maps to ACC structural evaluation.

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01-f03 | Context levels for prediction generation |
| M-layer | context_depth, transition_dynamics | Integrated context for phrase detection |
| R³ [7] | amplitude | Current stimulus strength |
| R³ [11] | onset_strength | Event detection |
| H³ | 4 tuples (see above) | Current-state features |
