# PSH P-Layer — Cognitive Present (3D)

**Layer**: Cognitive Present (P)
**Indices**: [4:7]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 4 | P0:prediction_state | [0, 1] | Current pre-stimulus prediction strength. Represents how strongly the system is generating predictions at all levels before the next stimulus arrives. High = active predictive processing. Maps to IFG → STG top-down prediction pathway. |
| 5 | P1:sensory_persistence | [0, 1] | Current low-level sensory persistence state. Real-time tracking of how much low-level representation persists post-stimulus. Always active regardless of prediction accuracy. Maps to A1/HG persistent activity (de Vries 2023: V1/A1 persistence at ~110ms). |
| 6 | P2:error_persistence | [0, 1] | Current PE persistence in primary cortex. Real-time tracking of how much the error signal persists at low levels (0-500ms post-stimulus). Persists for error monitoring regardless of prediction accuracy. Maps to auditory cortex MMN generator (Fong 2020, Tervaniemi 2022). |

---

## Design Rationale

1. **Prediction State (P0)**: Pre-stimulus prediction activation from high-level coupling. Represents the system's current predictive "load" — how actively it is generating expectations before the next event.

2. **Sensory Persistence (P1)**: Low-level representation persistence from E1. This signal ALWAYS persists post-stimulus, reflecting the fundamental asymmetry between hierarchical levels in the PSH model.

3. **Error Persistence (P2)**: PE signal persistence from PE magnitude and variability. Error signals persist at low levels for ongoing monitoring, consistent with the MMN literature.

---

## H³ Demands

No additional unique H³ demands. Reuses E-layer tuples.

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No unique H³ demands; reuses E-layer tuples |

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | E0:high_level_silencing | High-level state for prediction tracking |
| E-layer | E1:low_level_persistence | Low-level persistence |
| E-layer | E2:silencing_efficiency | Current silencing quality |
| H³ (shared) | Reuses E-layer tuples | Current-state features |
