# RIRI F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [7:10]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:recovery_trajectory | [0, 1] | Recovery trajectory prediction. sigma(0.40 * connectivity_trend + 0.30 * stability + 0.30 * integration_synergy). Predicts the direction of functional recovery based on connectivity trends and entrainment stability. Blasi 2025: structural neuroplasticity from music/dance rehab across sessions. |
| 8 | F1:connectivity_pred | [0, 1] | Functional connectivity restoration prediction. sigma(0.50 * connectivity_mean + 0.50 * connectivity_period). Predicts upcoming connectivity state based on current level and periodicity. Blasi 2025: enhanced FC within language and motor networks post-intervention. |
| 9 | F2:consolidation_pred | [0, 1] | Motor memory consolidation prediction. sigma(0.40 * connectivity_mean + 0.30 * temporal_coherence + 0.30 * encoding). Predicts session-to-session motor learning consolidation. Fang et al. 2017: music therapy preserves encoding in neurodegeneration. |

---

## Design Rationale

1. **Recovery Trajectory (F0)**: The macro-level prediction -- "is rehabilitation moving in the right direction?" Uses x_l5l7 connectivity trend (H16, regression slope) combined with entrainment stability and integration synergy. High values indicate positive recovery trajectory across rehabilitation sessions.

2. **Connectivity Prediction (F1)**: Predicts the near-future state of functional connectivity restoration. Based on current connectivity level and its periodicity (regularity of connectivity fluctuations). Stable, periodic connectivity signals predict continued restoration.

3. **Consolidation Prediction (F2)**: Predicts whether motor memories from the current session will consolidate across sessions. Combines connectivity coupling, temporal coherence, and encoding state. This is the hippocampal contribution to RIRI -- session-to-session learning depends on hippocampal-cortical consolidation.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (41, 16, 18, 0) | x_l5l7[0] trend H16 L0 | Connectivity trajectory for recovery forecast |
| (41, 16, 14, 2) | x_l5l7[0] periodicity H16 L2 | Connectivity regularity for prediction |
| (41, 16, 1, 0) | x_l5l7[0] mean H16 L0 | Current connectivity level |
| (25, 16, 19, 0) | x_l0l5[0] stability H16 L0 | Entrainment stability for recovery |

F-layer combines long-horizon H3 tuples with M-layer integration synergy for trajectory prediction.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:recovery_trajectory | F8 Learning | Recovery direction for adaptive difficulty |
| F1:connectivity_pred | F4 Memory | Connectivity state for session planning |
| F2:consolidation_pred | F6 Reward | Session success prediction |
| F2:consolidation_pred | Precision engine | pi_pred for rehabilitation beliefs |

---

## Scientific Foundation

- **Blasi et al. 2025**: Structural + functional neuroplasticity from music/dance rehab (20 RCTs, N=718)
- **Fang et al. 2017**: Music therapy preserves encoding in neurodegeneration (review, AD patients)
- **Jiao 2025**: 40 Hz gamma entrainment supports memory and neural integrity (review)
- **Provias et al. 2025**: Familiar music activates reward + memory circuits in chronic stroke (protocol)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/riri/forecast.py`
