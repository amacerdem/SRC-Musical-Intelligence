# CHPI — Forecast

**Model**: Cross-Modal Harmonic Predictive Integration
**Unit**: PCU
**Function**: F12 Cross-Modal Integration
**Tier**: beta
**Layer**: F — Forecast
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | next_chord_prediction | Confidence in upcoming harmonic event. Combines all streams: cross-modal prediction gain, voice-leading parsimony, and harmonic context strength from the P-layer. sigma(0.35 * f01 + 0.35 * f02 + 0.30 * harmonic_context_strength). High values indicate high confidence in predicting the next chord -- the system has strong cross-modal, geometric, and contextual evidence converging. Cheung 2019: harmonic expectation predicts amygdala, hippocampus, and auditory cortex activity. |
| 8 | crossmodal_anticipation | Visual/motor advance prediction signal. Driven by the visual-motor lead feature and sustained cross-modal coupling. sigma(0.50 * f03 + 0.50 * crossmodal_coupling_500ms). Represents the forward-looking benefit of cross-modal information: how far ahead the system can predict based on non-auditory streams. de Vries & Wurm 2023: view-invariant body motion predicted ~500ms ahead (eta_p^2=0.49). Bauer 2020: cross-modal phase resetting mediates sensory anticipation. |
| 9 | harmonic_trajectory | Predicted voice-leading direction. Tracks the expected trajectory of harmonic motion in chord space, combining voice-leading smoothness, tension dynamics, and harmonic change patterns. sigma(0.35 * voiceleading_smoothness + 0.35 * tension_velocity_100ms + 0.30 * harmonic_change_100ms). Tymoczko 2011: voice-leading as directional movement in geometric chord space. Gollin & Rehding 2011: PLR transformations predict efficient chord transition paths. |
| 10 | integration_confidence | Reliability of cross-modal integration. Meta-signal reflecting how much the system should trust its integrated cross-modal prediction. Driven by prediction gain, harmonic context, and inverse of surprise modulation. sigma(0.35 * f01 + 0.35 * harmonic_context_strength + 0.30 * (1 - f04)). High confidence when cross-modal enhancement is strong, tonal context is stable, and surprise modulation is low (predictable environment). Millidge, Seth & Buckley 2022: precision weighting in predictive coding determines integration confidence. |

---

## H3 Demands

The F-layer does not consume H3 tuples directly. All 20 H3 tuples are consumed upstream by the E-layer (14 tuples) and P-layer (6 tuples). The F-layer operates on the computed outputs of the E-layer (f01-f04) and P-layer (harmonic_context_strength, crossmodal_convergence, voiceleading_smoothness).

---

## Computation

The F-layer generates four forward-looking predictions about upcoming harmonic events, leveraging the full cross-modal integration pipeline:

1. **Next chord prediction** (idx 7): The primary predictive output, combining the cross-modal prediction gain (f01), voice-leading parsimony (f02), and harmonic context strength from the P-layer. This represents the system's overall confidence that it can predict the next harmonic event. When all three sources agree -- cross-modal coupling is strong, voice-leading is smooth, and the tonal center is stable -- prediction confidence is high. This signal feeds into other PCU models (HTP hierarchy, PWUP precision) and cross-unit to STU for motor timing.

2. **Crossmodal anticipation** (idx 8): The temporal advance signal capturing how far ahead the system can predict based on non-auditory information. Visual streams (notation reading, hand position observation) provide 200-500ms lead time, while motor streams (fingering patterns) provide 150-300ms lead time -- both substantially ahead of the 50-150ms lead from auditory statistical prediction alone. This signal represents the effective prediction horizon enabled by cross-modal convergence.

3. **Harmonic trajectory** (idx 9): Predicts the direction of harmonic motion in chord space. Combines voice-leading smoothness (current parsimony state), tension velocity (direction of tension change), and harmonic change magnitude (rate of harmonic motion). This geometric prediction allows the system to anticipate not just that a chord change is coming (next_chord_prediction), but where in chord space it is heading. Grounded in Tymoczko's voice-leading geometry and Neo-Riemannian PLR transformations.

4. **Integration confidence** (idx 10): A meta-cognitive signal representing the reliability of the cross-modal integration itself. High when cross-modal gain is strong (multiple streams converging), harmonic context is stable (clear tonal reference), and surprise modulation is low (predictable harmonic environment). Low when streams are misaligned, tonal context is ambiguous, or harmonic surprises are frequent. This signal modulates how much downstream processes (reward, attention) should weight cross-modal harmonic predictions. Maps to the precision-weighting framework of Millidge, Seth & Buckley 2022.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| CHPI E-layer | f01_crossmodal_prediction_gain | Cross-modal enhancement for chord prediction and confidence |
| CHPI E-layer | f02_voiceleading_parsimony | Geometric parsimony for chord prediction |
| CHPI E-layer | f03_visual_motor_lead | Temporal lead for cross-modal anticipation |
| CHPI E-layer | f04_harmonic_surprise_modulation | Inverse surprise for integration confidence |
| CHPI P-layer | harmonic_context_strength | Tonal stability for chord prediction and confidence |
| CHPI P-layer | crossmodal_convergence | Stream alignment for anticipation |
| CHPI P-layer | voiceleading_smoothness | Current parsimony for trajectory prediction |
| H3 (indirect) | via E-layer and P-layer | All temporal dynamics consumed upstream |
