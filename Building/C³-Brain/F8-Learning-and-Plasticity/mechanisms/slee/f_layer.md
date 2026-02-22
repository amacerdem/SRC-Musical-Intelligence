# SLEE — Forecast

**Model**: Statistical Learning Expertise Enhancement
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: β
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 10 | next_probability | Decision preparation prediction. Predicts the probability of the next auditory event based on the learned statistical model and detection accuracy. next_probability = σ(0.50 * f01 + 0.50 * f02). Reflects the predictive coding output: given the current statistical model (f01) and detection sensitivity (f02), what is the expected probability of the next event conforming to learned regularities. |
| 11 | regularity_continuation | Model updating prediction. Predicts whether the current statistical regularity will persist, combining the statistical model with accumulated exposure. regularity_continuation = σ(0.50 * f01 + 0.50 * exposure_model). Bridwell 2017: pattern-specific cortical entrainment predicts continuation of statistical structure. |
| 12 | detection_predict | Behavioral output prediction. Predicts the detection performance for upcoming irregularities based on current pattern segmentation, expertise state, and cross-modal binding strength. Paraskevopoulos 2022: musicians predict irregularities with higher accuracy, suggesting that the statistical learning system generates forward predictions about detection likelihood. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 7 | 3 | M0 (value) | L2 (bidi) | Amplitude at 100ms for detection context |
| 1 | 8 | 8 | M5 (range) | L0 (fwd) | Loudness range 500ms for prediction scaling |
| 2 | 33 | 3 | M0 (value) | L2 (bidi) | Pattern coupling 100ms for continuation estimate |
| 3 | 41 | 3 | M2 (std) | L2 (bidi) | Binding variability 100ms for prediction uncertainty |

---

## Computation

The F-layer generates three forward predictions based on the learned statistical model, reflecting the system's expectations about upcoming auditory events and its own future detection performance.

1. **next_probability**: Combines the statistical model (f01) and detection accuracy (f02) with equal weighting to predict the probability of the next event matching learned regularities. This implements the top-down prediction component of the predictive coding hierarchy (Carbajal & Malmierca 2018).

2. **regularity_continuation**: Combines the statistical model (f01) with the exposure model (M-layer) to predict whether the current regularity structure will persist. Longer exposure and stronger models yield higher continuation predictions, consistent with cortical entrainment buildup (Bridwell 2017).

3. **detection_predict**: Predicts upcoming detection performance by integrating pattern segmentation state (P-layer), expertise state (M-layer), and current binding dynamics. This is the most speculative prediction, anticipating future behavioral performance based on the current cognitive configuration.

H³ demands at this layer provide amplitude context (for attention-based prediction scaling), loudness range (for dynamic range prediction), pattern coupling (for continuation assessment), and binding variability (for prediction uncertainty estimation).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f01 | Statistical model | Core input to probability and continuation predictions |
| E-layer f02 | Detection accuracy | Base for next event prediction |
| M-layer exposure_model | Accumulated exposure | Context for regularity continuation |
| M-layer expertise_state | Expertise consolidation | Expertise level for detection prediction |
| P-layer pattern_segmentation | Boundary state | Current segmentation for prediction context |
| P-layer cross_modal_binding | Binding strength | Multisensory context for detection prediction |
| H³ (4 tuples) | Multi-scale temporal morphology | Amplitude, loudness range, coupling, and binding dynamics |
