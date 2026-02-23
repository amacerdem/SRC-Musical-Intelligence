# MPFS — Cognitive Present

**Model**: Musical Prodigy Flow State
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: P — Cognitive Present
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 5 | absorption_depth | Complete absorption / DMN suppression. Cross-feature integration coherence — how merged all processing streams currently are. High = all processing is unified (auditory, motor, structural), consistent with flow's "complete absorption" characteristic. Dai 2025: musicians show more frontal-reward PL state 11 (p=.001); non-musicians more DMN. Formula: σ(0.40 × integration_mean + 0.30 × x_coupling_autocorr + 0.30 × motor_coupling). |
| 6 | entrainment_fluency | Motor entrainment smoothness. Aggregated motor quality from beat-level and meter-level smoothness. Represents how effortlessly the motor system synchronizes with the musical pulse. High = effortless motor synchronization characteristic of flow. Maps to SMA (Chabin 2020: F(2,15)=27.3, p<1e-7) and basal ganglia automaticity. |
| 7 | structural_certainty | Structural knowledge level from temporal context hierarchy. Weighted mean across short (H8), medium (H14), and long (H20) context levels. High = the performer knows exactly where in the piece they are. Maps to the auditory cortex → frontal temporal hierarchy. Criscuolo 2022 ALE meta-analysis (k=84): musicians show higher auditory and sensorimotor activation. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 20 | M1 (mean) | L0 | Long-term coupling strength |
| 1 | 25 | 20 | M22 (autocorr) | L0 | Cross-feature self-similarity |
| 2 | 33 | 20 | M1 (mean) | L0 | Motor-perceptual coupling |
| 3 | 33 | 20 | M19 (stability) | L0 | Coupling stability |
| 4 | 41 | 20 | M1 (mean) | L0 | Cross-modal integration |
| 5 | 41 | 20 | M19 (stability) | L0 | Integration stability |

---

## Computation

The P-layer computes the real-time state of three flow-relevant signals:

1. **Absorption depth** (idx 5): How unified all processing streams are right now. Computed from cross-feature integration mean, coupling autocorrelation, and motor-perceptual coupling at H20. When all streams are coherent and self-similar, DMN suppression and complete absorption emerge.

2. **Entrainment fluency** (idx 6): Motor synchronization quality aggregated from beat and meter smoothness signals. Represents the "effortless control" characteristic of flow. When motor entrainment is smooth and regular, the performer doesn't need to consciously attend to timing.

3. **Structural certainty** (idx 7): Weighted context mastery across three hierarchical levels — motif (H8), phrase (H14), and structure (H20). High structural certainty means clear goals (knowing where in the piece you are), one of Csikszentmihalyi's flow characteristics.

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_motor_automaticity | Automaticity for fluency |
| E-layer | f02_context_mastery | Mastery for certainty |
| M-layer | challenge_skill_balance | Balance context for absorption |
| R³ [25] | x_l0l5 | Long-term coupling and self-similarity |
| R³ [33] | x_l4l5 | Motor-perceptual coupling and stability |
| R³ [41] | x_l5l7 | Cross-modal integration and stability |
| H³ | 6 tuples (see above) | Long-term features at H20 (5000ms) |
