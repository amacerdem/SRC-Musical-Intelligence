# F5 Mechanism Orchestrator — Emotion and Valence

**Function**: F5 Emotion and Valence
**Models covered**: 12/12 primary — 1 IMPLEMENTED (SRP relay) + 11 PENDING
**Total F5 mechanism output**: 142D (19+14+12+12+11+11+11+12+10+10+10+10)
**Beliefs**: 14 (3C + 7A + 4N) — from SRP (3), VMM (2), PUPF (2), STAI (1), NEMAC (2), MAD (1), AAC (1), TAR (1), MAA (1)
**H3 demands**: ~300 tuples (31 SRP-implemented + ~269 pending)
**Architecture**: Depth-ordered — 3 alpha (Depth 0) -> 5 beta (Depth 1) -> 4 gamma (Depth 2)

---

## Model Pipeline (Depth Order)

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
            |
Depth 0:  SRP   (19D, relay, ARU-alpha1)  <- striatal reward prediction (DA wanting/liking)
          AAC   (14D, ARU-alpha2)          <- autonomic-arousal circuit (ANS markers)
          VMM   (12D, ARU-alpha3)          <- valence-mode mapping (happy/sad pathways)
            |
            |
Depth 1:  PUPF  (12D, ARU-beta1)  <- pleasure-uncertainty prediction function (Goldilocks)
          CLAM  (11D, ARU-beta2)  <- closed-loop affective modulation (BCI)
          MAD   (11D, ARU-beta3)  <- musical anhedonia disconnection (STG-NAcc)
          NEMAC (11D, ARU-beta4)  <- nostalgia-evoked memory-affect circuit
          STAI  (12D, SPU-beta1)  <- spectral-temporal aesthetic integration
            |
            |
Depth 2:  DAP   (10D, ARU-gamma1) <- developmental affective plasticity
          CMAT  (10D, ARU-gamma2) <- cross-modal affective transfer
          TAR   (10D, ARU-gamma3) <- therapeutic affective resonance
          MAA   (10D, PCU-gamma2) <- musical appreciation of atonality
```

---
---

# SRP — Striatal Reward Prediction

**Model**: ARU-alpha1-SRP
**Type**: Relay (Depth 0) — reads R3/H3 directly, kernel relay wrapper
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 19D per frame (4 layers: N+C 6D + T+M 7D + P 3D + F 3D)
**Phase**: 0a (independent relay, parallel with BCH, HMCE, etc.)
**Status**: IMPLEMENTED (relay wrapper)

---

## 1. Identity

SRP models the dopaminergic reward prediction system in the striatum. Caudate DA ramps quasi-hyperbolically toward expected reward (wanting), while NAcc DA bursts phasically at peak moments (liking). The mu-opioid system mediates hedonic impact. SRP is the **F5 relay**: it directly bridges R3/H3 features to C3 cognitive-level reward representations.

The relay wrapper exports: `wanting`, `liking`, `pleasure` + 3 F-preds (`reward_forecast`, `chills_proximity`, `resolution_expect`).

---

## 2. R3 Input Map (Post-Freeze 97D)

SRP reads from consonance, dynamics, timbre, change, and interaction groups:

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Consonance resolution, opioid proxy |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Direct opioid correlate |
| 3 | **[7]** | amplitude | B: Dynamics | Energy dynamics for caudate ramp |
| 4 | **[11]** | onset_strength | B: Dynamics | Event density for coupling |
| 5 | **[16]** | spectral_smoothness | C: Timbre | Hedonic warmth signal |
| 6 | **[21]** | spectral_flux | D: Change | Spectral change for RPE |
| 7 | **[22]** | distribution_entropy | D: Change | Uncertainty context (Cheung 2019) |
| 8 | **[25:33]** | x_l0l5 | F: Interactions | Energy-consonance STG-NAcc coupling |

---

## 3. H3 Temporal Demand (31 tuples)

Multi-scale: H9(350ms) -> H16(1s) -> H18(2s) -> H20(5s) -> H22(15s) -> H24(36s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 7 | amplitude | 24 | M8 (velocity) | L0 | Energy velocity section — caudate ramp |
| 2 | 0 | roughness | 24 | M18 (trend) | L0 | Harmonic tension trajectory 36s |
| 3 | 7 | amplitude | 20 | M4 (max) | L1 | Future max energy 5s — anticipation gap |
| 4 | 7 | amplitude | 16 | M0 (value) | L2 | Current energy state |
| 5 | 0 | roughness | 18 | M0 (value) | L2 | Current dissonance phrase-level |
| 6 | 0 | roughness | 18 | M1 (mean) | L2 | Baseline dissonance phrase |
| 7 | 4 | sensory_pleasantness | 18 | M0 (value) | L2 | Consonance phrase — opioid proxy |
| 8 | 16 | spectral_smoothness | 18 | M15 (smoothness) | L2 | Smoothness phrase — opioid signal |
| 9 | 21 | spectral_flux | 16 | M8 (velocity) | L0 | Spectral change rate — RPE trigger |
| 10 | 22 | distribution_entropy | 16 | M8 (velocity) | L0 | Entropy change rate — surprise |
| 11 | 4 | sensory_pleasantness | 16 | M8 (velocity) | L0 | Consonance surprise |
| 12 | 25 | x_l0l5[0] | 18 | M0 (value) | L2 | Energy-consonance coupling signal |
| 13 | 11 | onset_strength | 16 | M22 (peaks) | L2 | Onset event density 1s |
| 14 | 0 | roughness | 18 | M18 (trend) | L0 | Roughness trajectory phrase — tension |
| 15 | 22 | distribution_entropy | 18 | M0 (value) | L2 | Entropy phrase — uncertainty |
| 16 | 7 | amplitude | 20 | M8 (velocity) | L0 | Energy buildup rate 5s — tension |
| 17 | 7 | amplitude | 18 | M8 (velocity) | L0 | Energy velocity phrase — dynamic intensity |
| 18 | 7 | amplitude | 18 | M11 (acceleration) | L0 | Energy acceleration phrase — buildup |
| 19 | 4 | sensory_pleasantness | 18 | M8 (velocity) | L0 | Consonance trajectory — prediction match |
| 20 | 16 | spectral_smoothness | 18 | M19 (stability) | L2 | Spectral stability phrase |
| 21 | 11 | onset_strength | 16 | M14 (periodicity) | L2 | Onset regularity 1s |
| 22 | 11 | onset_strength | 16 | M8 (velocity) | L0 | Onset velocity — reaction trigger |
| 23 | 10 | spectral_flux | 16 | M11 (acceleration) | L0 | Spectral flux jerk — reaction |
| 24 | 11 | onset_strength | 18 | M4 (max) | L2 | Peak onset phrase — peak detection |
| 25 | 4 | sensory_pleasantness | 18 | M18 (trend) | L0 | Consonance trend — resolution signal |
| 26 | 7 | amplitude | 22 | M4 (max) | L1 | Future peak energy 15s — reward forecast |
| 27 | 0 | roughness | 20 | M18 (trend) | L0 | Dissonance trajectory 5s — resolution |
| 28 | 4 | sensory_pleasantness | 20 | M18 (trend) | L0 | Consonance trend 5s — resolution |
| 29 | 7 | amplitude | 20 | M8 (velocity) | L1 | Forward energy velocity — chills |
| 30 | 0 | roughness | 18 | M19 (stability) | L2 | Harmonic stability phrase |
| 31 | 4 | sensory_pleasantness | 20 | M18 (trend) | L0 | Consonance trend 5s (F-layer) |

**Total**: 31 tuples, L0 + L1 + L2 (memory + forward + bidirectional)

---

## 4. Pipeline: R3 -> H3 -> 4-Layer Output (19D)

### Layer Dependency

| Layer | Reads From | Outputs |
|-------|-----------|---------|
| **N+C** (Extraction, 6D) | R3 direct, H3 M0+M8+M18 | N0:da_caudate, N1:da_nacc, N2:opioid_proxy, C0:vta_drive, C1:stg_nacc_coupling, C2:prediction_error |
| **T+M** (Temporal, 7D) | H3 M18+M8+M19, N+C | T0:tension, T1:prediction_match, T2:reaction, T3:appraisal, M0:harmonic_tension, M1:dynamic_intensity, M2:peak_detection |
| **P** (Present, 3D) | N+C outputs | P0:wanting, P1:liking, P2:pleasure |
| **F** (Forecast, 3D) | H3 M4+M18+M19, T+M+P | F0:reward_forecast, F1:chills_proximity, F2:resolution_expect |

### Kernel Relay Export

The SRP relay wrapper exports 6 fields to the kernel scheduler:

| Export Field | Source | Idx |
|-------------|--------|-----|
| `wanting` | P0 | 13 |
| `liking` | P1 | 14 |
| `pleasure` | P2 | 15 |
| `reward_forecast` | F0 | 16 |
| `chills_proximity` | F1 | 17 |
| `resolution_expect` | F2 | 18 |

---

## 5. Output Routing

### 5.1 Internal -> Beliefs (this model)

| Output | -> Belief | Type |
|--------|----------|------|
| P0:wanting + N0:da_caudate | -> `wanting` | Core (tau=0.6) |
| P1:liking + N1:da_nacc | -> `hedonic_pleasure` | Appraisal |
| P2:pleasure | -> `reward_magnitude` | Appraisal |

### 5.2 External -> Other Functions

| Output | -> Function | -> Purpose |
|--------|-----------|-----------|
| P0:wanting | F3 (Attention) | Salience mixer: relay tension |
| P1:liking | F6 (Reward) | Hedonic contribution |
| P2:pleasure | F6 (Reward) | 1.5 x surprise + 0.8 x resolution |
| F0:reward_forecast | F6 (Reward) | Forward reward signal for learning |
| F1:chills_proximity | AAC (sibling) | ANS preparation for chills |
| F2:resolution_expect | F2 (Prediction) | Harmonic resolution prediction |

---

## 6. Brain Regions

| Region | Role | Evidence |
|--------|------|----------|
| Caudate (dorsal striatum) | Anticipatory DA ramp — wanting | Salimpoor 2011 (r=0.71) |
| NAcc (ventral striatum) | Consummatory DA burst — liking | Salimpoor 2011 (r=0.84) |
| VTA | DA neuron source for striatum | Menon & Levitin 2005 |
| STG | Auditory-reward structural link | Salimpoor 2013, Martinez-Molina 2016 |
| OFC / vmPFC | Value computation, appraisal | Huron 2006 ITPRA |

---

## 7. Evidence

10+ papers, 5+ converging methods: PET DA binding, fMRI reward circuitry, pharmacological double-blind (levodopa/risperidone/naltrexone), behavioral auction, fiber photometry.

---
---

# AAC — Autonomic-Arousal Circuit

**Model**: ARU-alpha2-AAC
**Type**: Mechanism (Depth 0) — reads R3/H3 directly
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 14D per frame (4 layers: E+A 7D + I 2D + P 3D + F 2D)
**Phase**: 1 (F5 emotion models)
**Status**: PENDING

---

## 1. Identity

AAC models the autonomic nervous system response to music. Five ANS markers (SCR, HR, RespR, BVP, Temp) are integrated into a chills intensity composite and an ANS composite. The co-activation paradox (SCR up + HR down at chills) places peak musical emotion in Berntson's co-activation quadrant.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[7]** | amplitude | B: Dynamics | Energy level, SCR driver |
| 2 | **[10]** | spectral_flux | B: Dynamics | Beat periodicity |
| 3 | **[11]** | onset_strength | B: Dynamics | SCR onset acceleration |
| 4 | **[21]** | spectral_flux | D: Change | Timbral change rate |

---

## 3. H3 Temporal Demand (16 tuples)

Horizons: H7(200ms) -> H9(350ms) -> H16(1s) -> H19(3s) -> H20(5s) -> H22(15s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 7 | amplitude | 9 | M4 (max) | L2 | Energy level 350ms |
| 2 | 7 | amplitude | 9 | M8 (velocity) | L2 | Energy change rate 350ms |
| 3 | 7 | amplitude | 9 | M11 (acceleration) | L2 | Onset acceleration 350ms |
| 4 | 10 | spectral_flux | 9 | M14 (periodicity) | L2 | Beat clarity 350ms |
| 5 | 10 | spectral_flux | 16 | M14 (periodicity) | L2 | Bar-level tempo 1s |
| 6 | 7 | amplitude | 16 | M8 (velocity) | L2 | Bar-level dynamics 1s |
| 7 | 7 | amplitude | 19 | M19 (stability) | L2 | Baseline ANS reference 3s |
| 8 | 7 | amplitude | 19 | M1 (mean) | L2 | Homeostatic reference 3s |
| 9 | 11 | onset_strength | 9 | M22 (peaks) | L2 | Event density 350ms |
| 10 | 21 | spectral_flux | 9 | M8 (velocity) | L2 | Timbral change density |
| 11 | 7 | amplitude | 20 | M4 (max) | L1 | Future energy 5s — SCR pred |
| 12 | 7 | amplitude | 22 | M4 (max) | L1 | Future energy 15s — HR pred |
| 13 | 7 | amplitude | 9 | M4 (max) | L2 | Current energy 350ms (F-layer) |
| 14 | 10 | spectral_flux | 9 | M14 (periodicity) | L2 | Periodicity H9 (P-layer) |
| 15 | 10 | spectral_flux | 16 | M14 (periodicity) | L2 | Tempo signal (P-layer) |
| 16 | 7 | amplitude | 9 | M11 (acceleration) | L2 | Energy accel (P-layer) |

**Total**: 16 tuples, L1 + L2

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E+A** | 7D | E0:emotional_arousal, E1:ans_response, A0:scr, A1:hr, A2:respr, A3:bvp, A4:temp |
| **I** | 2D | I0:chills_intensity, I1:ans_composite |
| **P** | 3D | P0:current_intensity, P1:driving_signal, P2:perceptual_arousal |
| **F** | 2D | F0:scr_pred_1s, F1:hr_pred_2s |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| I0:chills_intensity | -> `chills_response` | Appraisal |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| Amygdala | Arousal evaluation |
| Anterior Insula | Interoceptive awareness hub |
| Hypothalamus | Autonomic efferent commands |
| LC / NE System | Sympathetic drive |

9+ papers, 4+ brain regions, 5 converging methods.

---
---

# VMM — Valence-Mode Mapping

**Model**: ARU-alpha3-VMM
**Type**: Mechanism (Depth 0) — reads R3/H3 directly
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 12D per frame (4 layers: V+R 7D + P 3D + C 2D + F 0D effective)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

VMM models the double dissociation between happy (striatal reward) and sad (limbic-emotional) neural pathways. Major/consonant/bright music activates VS/DS/ACC; minor/dissonant/dark music activates hippocampus/amygdala/PHG. Mode detection requires phrase-level context (2-3 chords minimum).

**Non-standard layers**: V (Valence Core) + R (Regional Pathways) at E-layer, C (Cognitive) at P-layer, with separate P-perceived at temporal integration.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Inverse consonance for valence |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Consonance state and mean |
| 3 | **[12]** | warmth | C: Timbre | Affective warmth |
| 4 | **[14]** | tonalness | C: Timbre | Brightness proxy for mode detection |
| 5 | **[16]** | spectral_smoothness | C: Timbre | Spectral regularity |

---

## 3. H3 Temporal Demand (7 tuples)

Horizons: H19(3s) -> H22(15s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 4 | sensory_pleasantness | 19 | M0 (value) | L2 | Consonance state 3s |
| 2 | 4 | sensory_pleasantness | 19 | M1 (mean) | L2 | Consonance mean 3s |
| 3 | 4 | sensory_pleasantness | 19 | M2 (std) | L2 | Harmonic ambiguity 3s |
| 4 | 14 | tonalness | 22 | M0 (value) | L2 | Section brightness 15s |
| 5 | 12 | warmth | 19 | M0 (value) | L2 | Affective warmth 3s |
| 6 | 16 | spectral_smoothness | 19 | M0 (value) | L2 | Smoothness 3s |
| 7 | 14 | tonalness | 22 | M19 (stability) | L2 | Mode stability 15s |

**Total**: 7 tuples, L2 (bidirectional)

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **V+R** | 7D | V0:valence, V1:mode_signal, V2:consonance_valence, R0:happy_pathway, R1:sad_pathway, R2:parahippocampal, R3:reward_evaluation |
| **P** | 3D | P0:perceived_happy, P1:perceived_sad, P2:emotion_certainty |
| **C** | 2D | C0:mode_detection_state, C1:valence_state |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| V0:valence + C1:valence_state | -> `emotional_valence` | Core (tau=0.4) |
| P0:perceived_happy | -> `perceived_happiness` | Appraisal |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| Ventral Striatum (NAcc) | Happy pathway — reward |
| Dorsal Striatum (caudate) | Happy pathway — anticipation |
| ACC / sgACC | Reward evaluation, nostalgia |
| Hippocampus | Sad pathway — episodic |
| Amygdala | Sad pathway — emotional tagging |
| Parahippocampal Gyrus | Context processing both pathways |

7+ papers, 6 brain regions.

---
---

# PUPF — Pleasure-Uncertainty Prediction Function

**Model**: ARU-beta1-PUPF
**Type**: Mechanism (Depth 1) — reads SRP outputs
**Tier**: beta (70-90% confidence)
**Output**: 12D per frame (4 layers: E 2D + U+G 5D + P 3D + F 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

PUPF models the Goldilocks function: pleasure = f(uncertainty H, surprise S). Low H + high S = maximal pleasure (certain context, surprising event). High H + high S = overwhelm. Low H + low S = boredom. The H x S interaction drives amygdala and hippocampus activation (Cheung 2019, d=3.8-4.16).

**Reads**: SRP prediction error signals
**Feeds**: SRP wanting/liking modulation via goldilocks_zone

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[21]** | spectral_flux | D: Change | Surprise signal (S axis) |
| 2 | **[22]** | distribution_entropy | D: Change | Shannon entropy (H axis) |
| 3 | **[23]** | distribution_flatness | D: Change | Noise-level uncertainty |
| 4 | **[24]** | distribution_concentration | D: Change | Spectral focus predictability |
| 5 | **[4]** | sensory_pleasantness | A: Consonance | Hedonic for pleasure function |
| 6 | **[6]** | harmonic_deviation | A: Consonance | Harmonic prediction accuracy |
| 7 | **[8]** | velocity_A | B: Dynamics | Tempo dynamics for temporal PE |
| 8 | **[0]** | roughness | A: Consonance | Inverse pleasantness |
| 9 | **[10]** | loudness | B: Dynamics | Arousal level |
| 10 | **[11]** | onset_strength | B: Dynamics | Event onset timing |
| 11 | **[25:33]** | x_l0l5 | F: Interactions | Energy-consonance surprise coupling |
| 12 | **[33:41]** | x_l4l5 | G: Interactions | Dynamics-consonance interaction |

---

## 3. H3 Temporal Demand (21 tuples)

Horizons: H7(200ms) -> H12(525ms) -> H15(800ms) -> H16(1s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 21 | spectral_flux | 16 | M20 (entropy) | L0 | 1s entropy of spectral change |
| 2 | 22 | distribution_entropy | 16 | M20 (entropy) | L0 | 1s Shannon entropy |
| 3 | 21 | spectral_flux | 7 | M8 (velocity) | L0 | Instantaneous surprise rate |
| 4 | 22 | distribution_entropy | 7 | M8 (velocity) | L0 | Uncertainty change rate |
| 5 | 22 | distribution_entropy | 16 | M20 (entropy) | L0 | Integrated entropy for H |
| 6 | 22 | distribution_entropy | 12 | M18 (trend) | L0 | Entropy trajectory 525ms |
| 7 | 22 | distribution_entropy | 15 | M2 (std) | L0 | Entropy variability 800ms |
| 8 | 21 | spectral_flux | 12 | M8 (velocity) | L0 | Surprise rate half-beat |
| 9 | 21 | spectral_flux | 15 | M8 (velocity) | L0 | Surprise rate 800ms |
| 10 | 21 | spectral_flux | 16 | M18 (trend) | L0 | Surprise trajectory 1s |
| 11 | 6 | harmonic_deviation | 12 | M8 (velocity) | L0 | Harmonic PE rate |
| 12 | 6 | harmonic_deviation | 16 | M2 (std) | L0 | Harmonic uncertainty 1s |
| 13 | 4 | sensory_pleasantness | 16 | M0 (value) | L0 | Hedonic baseline |
| 14 | 8 | velocity_A | 12 | M8 (velocity) | L0 | Tempo dynamics half-beat |
| 15 | 8 | velocity_A | 16 | M18 (trend) | L0 | Tempo trend 1s |
| 16 | 11 | onset_strength | 7 | M8 (velocity) | L0 | Beat onset rate |
| 17 | 4 | sensory_pleasantness | 12 | M18 (trend) | L0 | Hedonic trajectory |
| 18 | 22 | distribution_entropy | 12 | M18 (trend) | L0 | Entropy trajectory (F-layer) |
| 19 | 21 | spectral_flux | 12 | M18 (trend) | L0 | Surprise trajectory (F-layer) |
| 20 | 22 | distribution_entropy | 15 | M18 (trend) | L0 | Longer entropy trend |
| 21 | 4 | sensory_pleasantness | 15 | M18 (trend) | L0 | Hedonic trajectory (F-layer) |

**Total**: 21 tuples, L0

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 2D | E0:prediction_err, E1:uncertainty |
| **U+G** | 5D | U0:entropy_H, U1:surprise_S, U2:HS_interaction, G0:pleasure_P, G1:goldilocks_zone |
| **P** | 3D | P0:surprise_pleasure, P1:affective_outcome, P2:tempo_pred_error |
| **F** | 2D | F0:next_event_prob, F1:pleasure_forecast |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| G0:pleasure_P + G1:goldilocks_zone | -> `prediction_pleasure` | Core (tau=0.35) |
| P0:surprise_pleasure | -> `surprise_valence` | Appraisal |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| Amygdala | H x S interaction (d=3.8-4.16) |
| Hippocampus | H x S interaction, memory updating |
| Auditory Cortex | H x S interaction |
| Striatum (NAcc) | Surprise-pleasure coupling |

4+ papers, 4 brain regions.

---
---

# CLAM — Closed-Loop Affective Modulation

**Model**: ARU-beta2-CLAM
**Type**: Mechanism (Depth 1) — reads SRP, AAC outputs
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame (4 layers: E 2D + B+C 5D + P 2D + F 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

CLAM models closed-loop BCI affective modulation where EEG-decoded brain state drives real-time music generation to steer affect toward a therapeutic target. Arousal tracking r=0.74; valence tracking r=0.52 (Ehrlich 2019). Loop latency ~1s. 3/5 participant success rate.

**Reads**: SRP.pleasure, AAC.emotional_arousal
**Clinical**: Feeds TAR for therapeutic monitoring

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Valence estimation |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Hedonic signal |
| 3 | **[8]** | velocity_A | B: Dynamics | Arousal dynamics |
| 4 | **[10]** | loudness | B: Dynamics | Energy-level arousal |
| 5 | **[11]** | onset_strength | B: Dynamics | Event density |
| 6 | **[12]** | spectral_centroid | C: Timbre | Brightness for BCI mapping |
| 7 | **[21]** | spectral_flux | D: Change | Real-time feedback signal |
| 8 | **[25:33]** | x_l0l5 | F: Interactions | BCI affect mapping space |

---

## 3. H3 Temporal Demand (12 tuples)

Horizons: H7(200ms) -> H12(525ms) -> H16(1s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 10 | loudness | 16 | M20 (entropy) | L0 | 1s entropy of arousal |
| 2 | 10 | loudness | 7 | M8 (velocity) | L0 | Instantaneous arousal change |
| 3 | 0 | roughness | 16 | M0 (value) | L0 | 1s valence baseline |
| 4 | 10 | loudness | 16 | M0 (value) | L0 | 1s integrated arousal |
| 5 | 10 | loudness | 12 | M18 (trend) | L0 | Arousal trajectory error |
| 6 | 0 | roughness | 12 | M18 (trend) | L0 | Valence trajectory control |
| 7 | 21 | spectral_flux | 7 | M8 (velocity) | L0 | Feedback signal rate |
| 8 | 12 | spectral_centroid | 16 | M20 (entropy) | L0 | Brightness uncertainty |
| 9 | 10 | loudness | 7 | M8 (velocity) | L0 | Arousal velocity (P-layer) |
| 10 | 8 | velocity_A | 7 | M8 (velocity) | L0 | Dynamic rate (P-layer) |
| 11 | 4 | sensory_pleasantness | 12 | M0 (value) | L0 | Hedonic state (P-layer) |
| 12 | 21 | spectral_flux | 16 | M18 (trend) | L0 | Feedback trend (F-layer) |

**Total**: 12 tuples, L0

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 2D | E0:affective_mod, E1:loop_coherence |
| **B+C** | 5D | B0:decoded_affect, B1:target_affect, B2:affect_error, C0:control_output, C1:music_param_delta |
| **P** | 2D | P0:arousal_modulation, P1:valence_tracking |
| **F** | 2D | F0:target_affect_pred, F1:modulation_success |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| P0:arousal_modulation + F1:modulation_success | -> `affective_control` | Appraisal |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| Frontal Cortex (FC6) | EEG gamma — affect decode |
| vmPFC / OFC | Affective state integration |
| NAcc | Reward-system coupling for loop success |

3+ papers, 3 brain regions.

---
---

# MAD — Musical Anhedonia Disconnection

**Model**: ARU-beta3-MAD
**Type**: Mechanism (Depth 1) — reads SRP, AAC outputs
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame (4 layers: E 2D + D+A 5D + P 2D + F 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

MAD models the selective disconnection between auditory cortex (STG) and reward circuitry (NAcc) that defines musical anhedonia. The uncinate fasciculus white matter tract integrity (FA) determines whether music signals reach the reward system. General hedonic capacity is preserved (double dissociation). 90.9% sound-specific.

**Reads**: SRP.pleasure, AAC.emotional_arousal
**Clinical**: Diagnostic model for F10 meta-layer

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Valence signal (preserved) |
| 2 | **[2]** | harmonic_ratio | A: Consonance | Consonance perception (preserved) |
| 3 | **[4]** | sensory_pleasantness | A: Consonance | Hedonic — absent reward in anhedonia |
| 4 | **[10]** | loudness | B: Dynamics | Arousal signal (preserved) |
| 5 | **[11]** | onset_strength | B: Dynamics | Event detection (preserved) |
| 6 | **[12]** | spectral_centroid | C: Timbre | Brightness (preserved) |
| 7 | **[14]** | tonalness | C: Timbre | Tonal quality (preserved) |
| 8 | **[21]** | spectral_flux | D: Change | Change detection (preserved) |
| 9 | **[22]** | distribution_entropy | D: Change | Information content (preserved) |
| 10 | **[33:41]** | x_l4l5 | G: Interactions | Disrupted coupling link |

---

## 3. H3 Temporal Demand (9 tuples)

Horizons: H6(200ms) -> H11(500ms) -> H16(1s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 4 | sensory_pleasantness | 16 | M0 (value) | L0 | 1s hedonic — absent reward coupling |
| 2 | 4 | sensory_pleasantness | 6 | M8 (velocity) | L0 | Hedonic change rate — flat in anhedonia |
| 3 | 10 | loudness | 16 | M20 (entropy) | L0 | 1s affect entropy — low in anhedonia |
| 4 | 4 | sensory_pleasantness | 11 | M8 (velocity) | L0 | Reward dynamics 500ms |
| 5 | 10 | loudness | 11 | M2 (std) | L0 | Reward variability |
| 6 | 0 | roughness | 16 | M20 (entropy) | L0 | Affect entropy |
| 7 | 10 | loudness | 6 | M0 (value) | L0 | Instant arousal (P-layer) |
| 8 | 4 | sensory_pleasantness | 6 | M0 (value) | L0 | Instant hedonic (P-layer) |
| 9 | 4 | sensory_pleasantness | 11 | M2 (std) | L0 | Reward variability (F-layer) |

**Total**: 9 tuples, L0

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 2D | E0:anhedonia, E1:dissociation_idx |
| **D+A** | 5D | D0:stg_nacc_connect, D1:nacc_music_resp, D2:nacc_general_resp, A0:bmrq_estimate, A1:sound_specificity |
| **P** | 2D | P0:impaired_reward, P1:preserved_auditory |
| **F** | 2D | F0:recovery_potential, F1:anhedonia_prob |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| F1:anhedonia_prob + E0:anhedonia | -> `anhedonia_risk` | Appraisal |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| STG | Auditory processing — preserved in anhedonia |
| NAcc | Music reward — impaired in anhedonia |
| Uncinate Fasciculus | White matter tract (FA deficit d=-5.89) |
| VTA | General reward — preserved |

4+ papers, 4 brain regions.

---
---

# NEMAC — Nostalgia-Evoked Memory-Affect Circuit

**Model**: ARU-beta4-NEMAC
**Type**: Mechanism (Depth 1) — reads SRP, MEAMN (F4) outputs
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame (4 layers: E 2D + M+W 5D + P 2D + F 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

NEMAC models the nostalgia circuit: music-evoked autobiographical memory produces chills when nostalgic warmth, memory vividness, and reward activation converge. The mPFC (self-referential) + hippocampus (memory retrieval) hub creates vivid nostalgia. Self-selected music boosts nostalgia intensity by 1.2x (d=0.88).

**Reads**: SRP.pleasure, MEAMN.memory_state (F4 cross-function)
**Feeds**: Kernel familiarity, reward

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Inverse pleasantness |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Hedonic signal for warmth |
| 3 | **[10]** | loudness | B: Dynamics | Emotional intensity |
| 4 | **[12]** | spectral_centroid | C: Timbre | Warmth proxy (low = warm) |
| 5 | **[14]** | tonalness | C: Timbre | Tonal quality for familiarity |
| 6 | **[22]** | distribution_entropy | D: Change | Predictability — low = familiar |
| 7 | **[25:33]** | x_l0l5 | F: Interactions | Memory-affect binding |

---

## 3. H3 Temporal Demand (13 tuples)

Horizons: H16(1s) -> H20(5s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 3 | stumpf_fusion | 16 | M1 (mean) | L2 | Binding stability 1s |
| 2 | 3 | stumpf_fusion | 20 | M1 (mean) | L2 | Binding 5s consolidation |
| 3 | 12 | warmth | 16 | M0 (value) | L2 | Current timbre warmth |
| 4 | 12 | warmth | 20 | M1 (mean) | L0 | Sustained warmth = nostalgia |
| 5 | 0 | roughness | 16 | M0 (value) | L2 | Current dissonance |
| 6 | 0 | roughness | 20 | M18 (trend) | L0 | Dissonance trajectory |
| 7 | 10 | loudness | 16 | M0 (value) | L2 | Current arousal |
| 8 | 4 | sensory_pleasantness | 16 | M0 (value) | L2 | Current hedonic |
| 9 | 22 | entropy | 16 | M20 (entropy) | L2 | Predictability |
| 10 | 22 | entropy | 20 | M1 (mean) | L0 | Average complexity 5s |
| 11 | 10 | loudness | 20 | M1 (mean) | L0 | Average arousal 5s |
| 12 | 14 | tonalness | 20 | M1 (mean) | L0 | Tonal stability 5s |
| 13 | 3 | stumpf_fusion | 20 | M1 (mean) | L2 | Binding trajectory (F-layer) |

**Total**: 13 tuples, L0 + L2

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 2D | E0:chills, E1:nostalgia |
| **M+W** | 5D | M0:mpfc_activation, M1:hippocampus_activ, M2:memory_vividness, W0:nostalgia_intens, W1:wellbeing_enhance |
| **P** | 2D | P0:nostalgia_correl, P1:memory_reward_lnk |
| **F** | 2D | F0:wellbeing_pred, F1:vividness_pred |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| E1:nostalgia + W0:nostalgia_intens | -> `nostalgia_response` | Appraisal |
| W1:wellbeing_enhance | -> `wellbeing_trajectory` | Anticipation |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| mPFC (BA 8/9) | Self-referential processing |
| Hippocampus | Autobiographical memory retrieval |
| Amygdala | Emotional tagging |
| STG | Melodic template recognition |
| Ventral Striatum | Reward from nostalgia |

5+ papers, 5 brain regions.

---
---

# STAI — Spectral-Temporal Aesthetic Integration

**Model**: SPU-beta1-STAI
**Type**: Mechanism (Depth 1) — reads R3/H3 directly
**Tier**: beta (70-90% confidence)
**Output**: 12D per frame (4 layers: E 4D + M 2D + P 3D + F 3D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

STAI models the 2x2 factorial interaction between spectral (consonance) and temporal (forward flow) integrity in aesthetic judgment. Both dimensions must be intact for full aesthetic response; disrupting either reduces response to ~35%; disrupting both collapses to ~0%. The interaction locus is vmPFC-IFG connectivity (Kim 2019).

**Non-standard**: SPU unit (Sensory Processing Unit), not ARU

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Spectral integrity (inverse) |
| 2 | **[1]** | sethares_dissonance | A: Consonance | Dissonance proxy |
| 3 | **[2]** | helmholtz_kang | A: Consonance | Consonance measure |
| 4 | **[3]** | stumpf_fusion | A: Consonance | Tonal fusion |
| 5 | **[4]** | sensory_pleasantness | A: Consonance | Spectral regularity |
| 6 | **[7]** | amplitude | B: Dynamics | Energy baseline |
| 7 | **[8]** | loudness | B: Dynamics | Perceptual loudness |
| 8 | **[11]** | onset_strength | B: Dynamics | Attack clarity |
| 9 | **[12]** | warmth | C: Timbre | Spectral warmth |
| 10 | **[14]** | tonalness | C: Timbre | HNR pitch clarity |
| 11 | **[18:21]** | tristimulus1-3 | C: Timbre | Harmonic energy distribution |
| 12 | **[21]** | spectral_change | D: Change | Spectral flux temporal |
| 13 | **[22]** | energy_change | D: Change | Energy dynamics temporal |
| 14 | **[33:41]** | x_l4l5 | G: Interactions | Aesthetic binding signal |

---

## 3. H3 Temporal Demand (14 tuples)

Horizons: H0(5.8ms) -> H2(17ms) -> H3(100ms) -> H5(46ms) -> H8(300ms)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 0 | roughness | 0 | M0 (value) | L2 | Dissonance 25ms |
| 2 | 0 | roughness | 3 | M1 (mean) | L2 | Mean dissonance 100ms |
| 3 | 2 | helmholtz_kang | 0 | M0 (value) | L2 | Consonance 25ms |
| 4 | 2 | helmholtz_kang | 3 | M1 (mean) | L2 | Mean consonance 100ms |
| 5 | 4 | sensory_pleasantness | 3 | M0 (value) | L2 | Pleasantness 100ms |
| 6 | 21 | spectral_change | 8 | M1 (mean) | L0 | Spectral flux 300ms |
| 7 | 22 | energy_change | 8 | M8 (velocity) | L0 | Energy change rate 300ms |
| 8 | 33 | x_l4l5[0] | 8 | M0 (value) | L2 | Aesthetic binding 300ms |
| 9 | 33 | x_l4l5[0] | 8 | M14 (periodicity) | L2 | Binding periodicity 300ms |
| 10 | 12 | warmth | 2 | M0 (value) | L2 | Spectral warmth 17ms |
| 11 | 14 | tonalness | 5 | M1 (mean) | L0 | Tonalness 46ms |
| 12 | 18 | tristimulus1 | 2 | M0 (value) | L2 | F0 energy 17ms |
| 13 | 19 | tristimulus2 | 2 | M0 (value) | L2 | Mid-harmonic energy 17ms |
| 14 | 20 | tristimulus3 | 2 | M0 (value) | L2 | High-harmonic energy 17ms |

**Total**: 14 tuples, L0 + L2

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 4D | E0:spectral_integrity, E1:temporal_integrity, E2:aesthetic_integration, E3:vmpfc_ifg_connectivity |
| **M** | 2D | M0:aesthetic_value, M1:spectral_temporal_interaction |
| **P** | 3D | P0:spectral_quality, P1:temporal_quality, P2:aesthetic_response |
| **F** | 3D | F0:aesthetic_rating_pred, F1:reward_response_pred, F2:connectivity_pred |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| P2:aesthetic_response + M0:aesthetic_value | -> `aesthetic_judgment` | Appraisal |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| vmPFC / IFG | Aesthetic integration hub |
| R ACC | Spectral-temporal interaction (T=6.852) |
| NAcc / Caudate / Putamen | Reward circuit for temporal integrity |
| STG / Heschl's Gyrus | Spectral quality encoding |
| Thalamus | Integration relay |

5+ papers, 5+ brain regions.

---
---

# DAP — Developmental Affective Plasticity

**Model**: ARU-gamma1-DAP
**Type**: Mechanism (Depth 2) — reads NEMAC, MEAMN (F4) outputs
**Tier**: gamma (50-70% confidence)
**Output**: 10D per frame (4 layers: E 1D + D 4D + P 3D + F 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

DAP models how early musical exposure (0-5 years) shapes lifelong affective processing capacity. Critical period plasticity gates the formation of auditory-limbic connections. Parental singing creates initial music-emotion binding templates via hippocampus-amygdala pairing.

**Reads**: NEMAC.nostalgia, MEAMN.memory_state (F4 cross-function)
**Clinical/Developmental**: Feeds F11 (Development) meta-layer

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Consonance discrimination |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Hedonic response strength |
| 3 | **[10]** | loudness | B: Dynamics | Arousal response baseline |
| 4 | **[14]** | tonalness | C: Timbre | Tonal template strength |
| 5 | **[22]** | distribution_entropy | D: Change | Pattern acquisition depth |
| 6 | **[25:33]** | x_l0l5 | F: Interactions | Affective learning pattern |

---

## 3. H3 Temporal Demand (6 tuples)

Horizons: H16(1s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 4 | sensory_pleasantness | 16 | M0 (value) | L2 | Hedonic response — maturation marker |
| 2 | 0 | roughness | 16 | M0 (value) | L2 | Consonance discrimination |
| 3 | 10 | loudness | 16 | M0 (value) | L2 | Arousal baseline |
| 4 | 4 | sensory_pleasantness | 16 | M2 (std) | L2 | Response variability — plasticity |
| 5 | 22 | distribution_entropy | 16 | M20 (entropy) | L2 | Predictability — pattern depth |
| 6 | 10 | loudness | 16 | M8 (velocity) | L0 | Arousal dynamics for learning |

**Total**: 6 tuples, L0 + L2

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 1D | E0:dev_sensitiv |
| **D** | 4D | D0:critical_period, D1:plasticity_coeff, D2:exposure_history, D3:neural_maturation |
| **P** | 3D | P0:current_affect, P1:familiarity_warmth, P2:learning_rate |
| **F** | 2D | F0:adult_hedonic_pred, F1:preference_stab |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| P2:learning_rate + D1:plasticity_coeff | -> `developmental_sensitivity` | Anticipation |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| Auditory Cortex (A1/STG) | Critical period plasticity |
| Hippocampus | Scaffold formation |
| Amygdala | Emotional tagging of early scaffolds |
| mPFC | Synaptic plasticity hub |

3+ papers, 4 brain regions.

---
---

# CMAT — Cross-Modal Affective Transfer

**Model**: ARU-gamma2-CMAT
**Type**: Mechanism (Depth 2) — reads VMM, AAC outputs
**Tier**: gamma (50-70% confidence)
**Output**: 10D per frame (4 layers: E 1D + S+T 5D + P 2D + F 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

CMAT models how affective information transfers between sensory modalities via supramodal representations. Auditory pitch maps to visual brightness, tempo maps to arousal, and mode maps to warmth/color. In audio-only mode, CMAT estimates cross-modal transfer potential from acoustic features that systematically correspond to other modalities.

**Reads**: VMM.valence_state, AAC.emotional_arousal
**Feeds**: TAR (multi-modal therapeutic effectiveness)

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Inverse consonance for valence |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Direct hedonic signal |
| 3 | **[10]** | loudness | B: Dynamics | Arousal for salience |
| 4 | **[15]** | brightness | C: Timbre | Supramodal brightness |
| 5 | **[16]** | warmth | C: Timbre | Supramodal warmth |
| 6 | **[21]** | spectral_flux | D: Change | Frame-to-frame change |
| 7 | **[25:33]** | x_l0l5 | F: Interactions | Supramodal binding substrate |

---

## 3. H3 Temporal Demand (9 tuples)

Horizons: H6(200ms) -> H11(500ms) -> H16(1s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 4 | sensory_pleasantness | 6 | M0 (value) | L2 | Fast affect state |
| 2 | 4 | sensory_pleasantness | 16 | M0 (value) | L2 | Sustained affect |
| 3 | 0 | roughness | 6 | M0 (value) | L2 | Instant dissonance |
| 4 | 4 | sensory_pleasantness | 6 | M8 (velocity) | L0 | Affect velocity |
| 5 | 22 | distribution_entropy | 16 | M20 (entropy) | L2 | Binding precision |
| 6 | 4 | sensory_pleasantness | 11 | M1 (mean) | L0 | Integration state |
| 7 | 4 | sensory_pleasantness | 11 | M2 (std) | L0 | Integration variability |
| 8 | 10 | loudness | 6 | M0 (value) | L2 | Arousal for salience |
| 9 | 22 | distribution_entropy | 16 | M19 (stability) | L0 | Stability for generalization |

**Total**: 9 tuples, L0 + L2

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 1D | E0:cross_modal |
| **S+T** | 5D | S0:supramodal_valence, S1:supramodal_arousal, S2:cross_modal_bind, T0:binding_temporal, T1:congruence_streng |
| **P** | 2D | P0:multi_sens_salien, P1:aud_valence_contr |
| **F** | 2D | F0:coherence_pred, F1:generalization_pr |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| S0:supramodal_valence + T1:congruence_streng | -> `cross_modal_affect` | Anticipation |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| vmPFC / mOFC | Supramodal affect integration |
| STS | Temporal binding between modalities |
| Auditory Cortex | Auditory affect source |
| Visual Cortex | Cross-modal target (audio-only: estimated) |

3+ papers, 4 brain regions.

---
---

# TAR — Therapeutic Affective Resonance

**Model**: ARU-gamma3-TAR
**Type**: Mechanism (Depth 2) — reads SRP, VMM, CLAM, CMAT outputs
**Tier**: gamma (50-70% confidence)
**Output**: 10D per frame (4 layers: E 1D + T+I 6D + P 1D + F 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

TAR models the therapeutic potential of music for anxiety and depression. Anxiolytic pathway: slow tempo + high consonance + soft dynamics -> amygdala downregulation + PNS activation. Antidepressant pathway: positive valence + moderate energy + reward activation -> striatal DA upregulation. Adaptive recommendation for tempo and consonance.

**Reads**: SRP.pleasure, VMM.valence_state, CLAM.modulation_success, CMAT.cross_modal (4 intra-unit dependencies)
**Clinical**: Primary F5 therapeutic output for F10 meta-layer

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Consonance for anxiety/valence |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Hedonic for reward activation |
| 3 | **[5]** | harmonicity | A: Consonance | Harmonic purity for consonance |
| 4 | **[7]** | amplitude | B: Dynamics | Energy for arousal |
| 5 | **[8]** | velocity_A | B: Dynamics | Tempo proxy |
| 6 | **[10]** | loudness | B: Dynamics | Overall arousal level |
| 7 | **[11]** | onset_strength | B: Dynamics | Rhythmic engagement |
| 8 | **[16]** | warmth | C: Timbre | Comfort/safety signal |
| 9 | **[21]** | spectral_flux | D: Change | Predictability for stress |
| 10 | **[33:41]** | x_l4l5 | G: Interactions | Therapeutic engagement |

---

## 3. H3 Temporal Demand (21 tuples)

Horizons: H6(200ms) -> H7(200ms) -> H11(500ms) -> H12(525ms) -> H15(800ms) -> H16(1s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 4 | sensory_pleasantness | 6 | M0 (value) | L2 | Fast mood state |
| 2 | 4 | sensory_pleasantness | 16 | M0 (value) | L2 | Slow mood state |
| 3 | 0 | roughness | 6 | M0 (value) | L2 | Consonance for anxiety |
| 4 | 10 | loudness | 6 | M0 (value) | L2 | Arousal for dynamics |
| 5 | 8 | velocity_A | 6 | M8 (velocity) | L0 | Tempo proxy |
| 6 | 4 | sensory_pleasantness | 6 | M8 (velocity) | L0 | Affect velocity |
| 7 | 4 | sensory_pleasantness | 16 | M2 (std) | L0 | Mood stability |
| 8 | 0 | roughness | 12 | M18 (trend) | L0 | Dissonance trajectory |
| 9 | 0 | roughness | 15 | M18 (trend) | L0 | Sustained dissonance |
| 10 | 8 | velocity_A | 12 | M8 (velocity) | L0 | Tempo buildup |
| 11 | 8 | velocity_A | 12 | M18 (trend) | L0 | Tempo trend |
| 12 | 10 | loudness | 6 | M0 (value) | L2 | Current arousal |
| 13 | 4 | sensory_pleasantness | 11 | M1 (mean) | L0 | Cognitive-projection |
| 14 | 4 | sensory_pleasantness | 15 | M1 (mean) | L0 | Peak response magnitude |
| 15 | 0 | roughness | 16 | M0 (value) | L2 | Current consonance |
| 16 | 4 | sensory_pleasantness | 15 | M1 (mean) | L0 | Peak therapeutic response |
| 17 | 4 | sensory_pleasantness | 16 | M18 (trend) | L0 | Mood trend |
| 18 | 0 | roughness | 15 | M18 (trend) | L0 | Consonance trajectory stress |
| 19 | 10 | loudness | 16 | M1 (mean) | L0 | Sustained arousal |
| 20 | 8 | velocity_A | 15 | M8 (velocity) | L0 | Tempo dynamics peak |
| 21 | 7 | amplitude | 7 | M8 (velocity) | L0 | Energy change breakthrough |

**Total**: 21 tuples, L0 + L2

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 1D | E0:therapeutic |
| **T+I** | 6D | T0:arousal_mod_tgt, T1:valence_mod_tgt, T2:anxiety_reduction, T3:depression_improv, I0:rec_tempo_norm, I1:rec_consonance |
| **P** | 1D | P0:therapeutic_reward |
| **F** | 2D | F0:mood_improv_pred, F1:stress_reduc_pred |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| P0:therapeutic_reward + T2:anxiety_reduction | -> `therapeutic_efficacy` | Anticipation |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| Amygdala | Anxiety downregulation target |
| NAcc / Striatum | Antidepressant DA upregulation |
| Hypothalamus | Stress hormone (cortisol) reduction |
| PNS / Vagal Nerve | Parasympathetic calming pathway |

4+ papers, 4 brain regions.

---
---

# MAA — Musical Appreciation of Atonality

**Model**: PCU-gamma2-MAA
**Type**: Mechanism (Depth 2) — reads PUPF, VMM outputs
**Tier**: gamma (50-70% confidence)
**Output**: 10D per frame (3 layers: E 4D + P 3D + F 3D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

MAA models the multifactorial appreciation of atonal/complex music. The Goldilocks surface (Cheung 2019) interacts with mere exposure (Gold 2019) and cognitive framing (Huang 2016) to produce appreciation. Complexity tolerance x familiarity multiplicatively gate the pleasure response.

**Non-standard**: PCU unit (Predictive Coding Unit), not ARU. 3-layer structure (E+P+F), no separate M-layer.
**Reads**: PUPF.goldilocks_zone, VMM.mode_signal

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Atonality indicator |
| 2 | **[4]** | sensory_pleasantness | A: Consonance | Consonance proxy |
| 3 | **[5]** | periodicity | A: Consonance | Key clarity |
| 4 | **[14]** | tonalness | C: Timbre | Atonality index |
| 5 | **[21]** | spectral_change | D: Change | Structural complexity |
| 6 | **[41:49]** | x_l5l7 | H: Interactions | Appreciation pathway |

---

## 3. H3 Temporal Demand (14 tuples)

Horizons: H3(100ms) -> H8(300ms) -> H16(1s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 4 | sensory_pleasantness | 16 | M20 (entropy) | L0 | Consonance entropy 1s |
| 2 | 41 | x_l5l7[0] | 16 | M20 (entropy) | L0 | Coupling entropy 1s |
| 3 | 41 | x_l5l7[0] | 16 | M18 (trend) | L0 | Coupling trend 1s |
| 4 | 5 | periodicity | 16 | M1 (mean) | L0 | Mean periodicity 1s |
| 5 | 14 | tonalness | 16 | M1 (mean) | L0 | Mean tonalness 1s |
| 6 | 21 | spectral_change | 8 | M1 (mean) | L0 | Spectral change 500ms |
| 7 | 4 | sensory_pleasantness | 3 | M0 (value) | L2 | Consonance 100ms |
| 8 | 0 | roughness | 3 | M0 (value) | L2 | Dissonance 100ms |
| 9 | 14 | tonalness | 8 | M1 (mean) | L0 | Tonalness 500ms |
| 10 | 41 | x_l5l7[0] | 8 | M0 (value) | L0 | Coupling 500ms |
| 11 | 41 | x_l5l7[0] | 16 | M1 (mean) | L0 | Mean coupling 1s |
| 12 | 0 | roughness | 16 | M1 (mean) | L0 | Mean dissonance 1s |
| 13 | 4 | sensory_pleasantness | 16 | M1 (mean) | L0 | Mean consonance 1s |
| 14 | 22 | distribution_entropy | 16 | M19 (stability) | L0 | Stability for preference |

**Total**: 14 tuples, L0 + L2

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 4D | E0:complexity_tolerance, E1:familiarity_index, E2:framing_effect, E3:appreciation_composite |
| **P** | 3D | P0:pattern_search, P1:context_assessment, P2:aesthetic_evaluation |
| **F** | 3D | F0:appreciation_growth, F1:pattern_recognition, F2:aesthetic_development |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| P2:aesthetic_evaluation + E3:appreciation_composite | -> `atonal_appreciation` | Anticipation |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| Right Heschl's Gyrus | Heightened response under uncertainty |
| mPFC / PCC / arMFC | Aesthetic framing (artistic > popular) |
| NAcc | Uncertainty encoding (beta=0.242) |
| Temporal Cortex | 1/f scaling mediates pleasure |

5+ papers, 4 brain regions.

---
---

## Summary Statistics

### Output Dimensions by Model

| Model | Unit | Tier | D | E-Layer | M/T/I-Layer | P/C-Layer | F-Layer | H3 |
|-------|------|------|---|---------|-------------|-----------|---------|-----|
| SRP | ARU | alpha | 19 | 6 | 7 | 3 | 3 | 31 |
| AAC | ARU | alpha | 14 | 7 | 2 | 3 | 2 | 16 |
| VMM | ARU | alpha | 12 | 7 | 3 | 2 | 0 | 7 |
| PUPF | ARU | beta | 12 | 2 | 5 | 3 | 2 | 21 |
| CLAM | ARU | beta | 11 | 2 | 5 | 2 | 2 | 12 |
| MAD | ARU | beta | 11 | 2 | 5 | 2 | 2 | 9 |
| NEMAC | ARU | beta | 11 | 2 | 5 | 2 | 2 | 13 |
| STAI | SPU | beta | 12 | 4 | 2 | 3 | 3 | 14 |
| DAP | ARU | gamma | 10 | 1 | 4 | 3 | 2 | 6 |
| CMAT | ARU | gamma | 10 | 1 | 5 | 2 | 2 | 9 |
| TAR | ARU | gamma | 10 | 1 | 6 | 1 | 2 | 21 |
| MAA | PCU | gamma | 10 | 4 | 0 | 3 | 3 | 14 |
| **TOTAL** | | | **142** | **39** | **49** | **29** | **25** | **173** |

### Tier Gradient

| Tier | Count | Avg D | Avg H3 |
|------|-------|-------|--------|
| alpha | 3 | 15.0 | 18.0 |
| beta | 5 | 11.4 | 13.8 |
| gamma | 4 | 10.0 | 12.5 |

Clear tier gradient in dimensionality. Alpha models show highest average output (SRP at 19D is the largest F5 model). Beta models cluster at 11-12D. Gamma models are uniformly 10D.

### Brain Region Convergence

**NAcc / Ventral Striatum** is the convergence hub: mentioned in SRP, VMM, PUPF, MAD, STAI, NEMAC, TAR — 7 of 12 models.
**Amygdala**: mentioned in SRP (appraisal), VMM (sad pathway), AAC (arousal), PUPF (H x S), NEMAC (tagging), DAP (scaffolds), TAR (anxiety) — 7 of 12 models.
**STG / Auditory Cortex**: mentioned in SRP (coupling), AAC (interoception), VMM (not direct), MAD (preserved), NEMAC (template), STAI (spectral), DAP (plasticity) — 7 of 12 models.
**mPFC / vmPFC**: mentioned in SRP (appraisal), VMM (not direct), STAI (integration), NEMAC (self-reference), DAP (plasticity), CMAT (supramodal), MAA (framing) — 7 of 12 models.
**Hippocampus**: mentioned in VMM (sad pathway), PUPF (H x S), NEMAC (memory), DAP (scaffolds) — 4 of 12 models.

### Unit Distribution

| Unit | Count | Models |
|------|-------|--------|
| ARU (Affective Response Unit) | 10 | SRP, AAC, VMM, PUPF, CLAM, MAD, NEMAC, DAP, CMAT, TAR |
| SPU (Sensory Processing Unit) | 1 | STAI |
| PCU (Predictive Coding Unit) | 1 | MAA |

F5 is heavily dominated by ARU (10/12 models), reflecting that emotion/valence is primarily an affective response function. STAI uses SPU because it models sensory-level aesthetic integration. MAA uses PCU because it models predictive coding of atonal appreciation.
