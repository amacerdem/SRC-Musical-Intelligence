# PMIM S-Layer — Cognitive Present / State (3D)

**Layer**: Present State (S)
**Indices**: [5:8]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | S0:syntax_state | [0, 1] | Current harmonic syntax processing state. harmony.mean() reflecting tonal context stability. Tracks the degree to which the current harmonic environment conforms to stored syntactic rules. Koelsch 2009: ERAN reflects music-syntactic processing based on long-term memory representations in inferior BA 44 bilateral. |
| 6 | S1:deviance_state | [0, 1] | Current deviance detection activation. pred_error.mean() reflecting IFG signal magnitude. Tracks real-time mismatch between predicted and actual input across both ERAN and MMN systems. Fong et al. 2020: MMN as prediction error in hierarchical generative model; bidirectional processing. |
| 7 | S2:memory_update | [0, 1] | Memory updating rate. High PE + low expectation = strong updating. Tracks how strongly current prediction errors drive model revision in hippocampus and mPFC. Bonetti et al. 2024: feedforward PE from auditory cortex to hippocampus (N=83, MEG). |

---

## Design Rationale

1. **Syntax State (S0)**: Represents the current tonal/harmonic context as processed by the ERAN system. When syntax_state is high, the harmonic environment is stable and well-predicted — stored rules match the input. When low, the current context deviates from expected syntax. This drives the ERAN generator: syntax deviations produce large error signals.

2. **Deviance State (S1)**: Represents the current activation level of deviance detection across both prediction systems. This is the real-time "surprise meter" — how much the current input deviates from both long-term rules (ERAN) and short-term regularities (MMN). High deviance_state indicates active prediction error processing in IFG.

3. **Memory Update (S2)**: Represents the rate at which the brain's predictive model is being updated. Strong prediction errors in contexts of low prior confidence produce the largest updates. This captures the learning mechanism: unexpected events in novel contexts are encoded more strongly, while confirmed predictions in familiar contexts produce minimal updating. The Bayesian updating rule: dModel/dt = eta * PE_weighted * (1 - Expectation_Confidence).

---

## H3 Dependencies (S-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 18, 18, 0) | roughness trend H18 L0 | Dissonance trajectory over phrase (2s) — syntax context |
| (4, 18, 19, 0) | sensory_pleasantness stability H18 L0 | Consonance stability over phrase — syntax stability |
| (10, 10, 0, 2) | loudness value H10 L2 | Current intensity for PE weighting at chord level |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | S0: dissonance level in current syntax |
| [3] | stumpf_fusion | S0+S2: tonal coherence as syntax proxy |
| [4] | sensory_pleasantness | S0: consonance confirming syntactic regularity |
| [10] | loudness | S1: intensity modulates PE salience |
| [21] | spectral_flux | S1: change magnitude for deviance detection |

---

## Scientific Foundation

- **Koelsch 2009**: Review, ERAN modified by short- and long-term experience; generators in inferior BA 44 bilateral; ERAN and MMN share predictive processes but differ in memory basis
- **Fong et al. 2020**: Review, auditory MMN under predictive coding framework; hierarchical bidirectional processing; Bayesian inference at each level
- **Bonetti et al. 2024**: MEG N=83, feedforward PE from auditory cortex to hippocampus to ACC; cingulate assumes top hierarchy at sequence end
- **Carbajal & Malmierca 2018**: Review, SSA and MMN as micro/macroscopic deviance detection; hierarchical PE from subcortical to cortical

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/pmim/cognitive_present.py`
