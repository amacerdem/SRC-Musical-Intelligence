# TMRM — Cognitive Present

**Model**: Tempo Memory Reproduction Method
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 5 | sensory_state | Sensory pathway activation (SMA + auditory cortex). Aggregated beat induction signal from beat peak loudness and flux periodicity. Represents the real-time quality of the sensory reproduction pathway. High when auditory feedback is clear and periodic — enabling the adjusting method. Maps to SMA internal tempo representation (Grahn & Brett 2007: SMA Z=5.03) and auditory cortex feedback loop (Ross & Balasubramaniam 2022). |
| 6 | motor_state | Motor pathway activation (cerebellum + premotor cortex). Aggregated motor entrainment from amplitude max and energy velocity at H11 (500ms). Represents the real-time quality of the motor reproduction pathway (tapping). Maps to cerebellar timing circuit (Okada 2022: 3 neuron types, PI t=3.36) and premotor motor planning. Formula: σ(0.50 × amp_max × energy_velocity). |

---

## H³ Demands

No additional unique H³ demands beyond E/M layers. The P-layer reuses tuples from E and M layers.

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No unique H³ demands; reuses E/M layer tuples |

---

## Computation

The P-layer computes the real-time state of both reproduction pathways:

1. **Sensory state** (idx 5): Current sensory pathway activation from beat induction quality. Represents how well the SMA + auditory cortex loop can support tempo matching via the adjusting method. Higher when beats are loud, periodic, and the internal template is clear.

2. **Motor state** (idx 6): Current motor pathway activation from amplitude and energy dynamics. Represents the cerebellum + premotor system's readiness for motor reproduction via tapping. Computed from peak amplitude × energy velocity at H11, reflecting the motor-only pathway without sensory feedback.

Both outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_adjusting_advantage | Sensory signal quality for pathway state |
| E-layer | f02_optimal_tempo | Tempo proximity for state calibration |
| M-layer | method_dissociation | Pathway dominance context |
| H³ (shared) | Reuses E/M tuples | Current-state features |
