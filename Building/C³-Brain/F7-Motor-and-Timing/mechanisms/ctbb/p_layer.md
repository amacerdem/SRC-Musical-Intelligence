# CTBB — Cognitive Present

**Model**: Cerebellar Theta-Burst Balance
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | timing_precision | Temporal-context cerebellar timing precision. Represents the current precision of the cerebellar timing circuit at the cognitive present, integrating the E-layer cerebellar timing with the M-layer temporal dynamics. Higher values indicate more precise motor timing, consistent with reduced timing variability observed after cerebellar iTBS (Ivry 1988: lateral cerebellum dissociation for timing vs execution). |
| 7 | motor_stability | Beat-entrainment motor output stability. Captures the stability of motor output in the current cognitive window, combining sway reduction with cerebellar-M1 coupling strength. Higher values indicate more stable motor performance, reflecting the postural improvement observed by Sansare 2025 (Bonferroni POST1-6 all p < .05). |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | P-layer uses no additional H3 tuples beyond E and M layers |

---

## Computation

The P-layer computes the cognitive present state of cerebellar motor timing by integrating E-layer and M-layer outputs into two summary dimensions that capture the "now" of cerebellar motor performance.

1. **timing_precision**: Synthesizes the cerebellar timing signal (f25) with timing enhancement dynamics from the M-layer. This represents the instantaneous precision of the cerebellar timing module, corresponding to the lateral cerebellum's role as a timing controller (Ivry 1988). In the context of music listening, this tracks how precisely the cerebellar circuit is tracking the rhythmic structure at the current moment.

2. **motor_stability**: Integrates sway reduction and cerebellar-M1 coupling from the M-layer to produce a single stability index. This corresponds to the behavioral outcome of cerebellar iTBS -- improved balance and motor steadiness (Sansare 2025). For music, this maps to how stably the motor system maintains entrainment to the beat.

The P-layer consumes no additional H3 tuples, relying entirely on the E-layer and M-layer computations to construct the cognitive present representation.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f25 | Cerebellar timing | Core timing signal for precision computation |
| M-layer timing_enhancement | Temporal timing dynamics | Temporal context for timing precision |
| M-layer sway_reduction | Postural sway dynamics | Stability input for motor_stability |
| M-layer cerebellar_m1_coupling | Pathway strength | Coupling input for motor_stability |
