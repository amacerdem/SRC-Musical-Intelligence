# F4 Mechanism Orchestrator — Memory Systems

**Function**: F4 Memory Systems
**Models covered**: 15/15 primary — 1 IMPLEMENTED (MEAMN relay) + 14 PENDING
**Total F4 mechanism output**: 163D (12+11+12+11+11+10+11+10+11+10+10+10+10+10+10)
**Beliefs**: 13 (3C + 7A + 3N) — from MEAMN (3), HCMC (3), PMIM (2), MMP (2), PNH (1), MSPBA (2)
**H3 demands**: 283 tuples (19 MEAMN-implemented + 264 pending)
**Architecture**: Depth-ordered — 3 alpha (Depth 0) -> 6 beta (Depth 1) -> 3 beta (Depth 2) -> 3 gamma (Depth 2)

---

## Model Pipeline (Depth Order)

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
            |
Depth 0:  MEAMN (12D, relay, IMU-alpha1) <- music-evoked autobiographical memory
          PNH   (11D, IMU-alpha2)        <- Pythagorean ratio hierarchy
          MMP   (12D, IMU-alpha3)        <- musical mnemonic preservation (clinical)
            |
            |
Depth 1:  RASN  (11D, IMU-beta1)  <- rhythmic auditory stimulation neuroplasticity (reads beat-entrainment)
          PMIM  (11D, IMU-beta2)  <- predictive memory integration (reads PNH)
          OII   (10D, IMU-beta3)  <- oscillatory intelligence integration (5 intra-unit connections)
          HCMC  (11D, IMU-beta4)  <- hippocampal-cortical memory circuit (reads MEAMN)
          RIRI  (10D, IMU-beta5)  <- RAS rehabilitation integration (reads RASN, MEAMN, MMP, HCMC)
          MSPBA (11D, IMU-beta6)  <- musical syntax in Broca's area (reads PNH)
            |
            |
Depth 2:  VRIAP  (10D, IMU-beta7)  <- VR-integrated analgesia paradigm (memory-only)
          TPRD   (10D, IMU-beta8)  <- tonotopy-pitch representation dissociation (pitch cross-circuit)
          CMAPCC (10D, IMU-beta9)  <- cross-modal action-perception common code (beat cross-circuit)
          DMMS   (10D, IMU-gamma1) <- developmental music memory scaffold
          CSSL   (10D, IMU-gamma2) <- cross-species song learning (memory-only)
          CDEM   (10D, IMU-gamma3) <- context-dependent emotional memory (affect cross-circuit)
```

---
---

# MEAMN — Music-Evoked Autobiographical Memory Network

**Model**: IMU-alpha1-MEAMN
**Type**: Relay (Depth 0) — reads R3/H3 directly, kernel relay wrapper
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 12D per frame (4 layers: E3 + M2 + P3 + F4)
**Phase**: 0a (independent relay, parallel with BCH, HMCE, etc.)
**Status**: IMPLEMENTED (relay wrapper)

---

## 1. Identity

MEAMN models how music evokes autobiographical memories. The hippocampus-mPFC-PCC hub binds musical features to personal history, producing vivid memory retrieval when familiar music is encountered. MEAMN is the **F4 relay**: it directly bridges R3/H3 features to C3 cognitive-level memory representations.

The relay wrapper exports: `memory_state`, `emotional_color`, `nostalgia_link` + 3 F-preds (`mem_vividness_fc`, `emo_response_fc`, `self_ref_fc`).

---

## 2. R3 Input Map (Post-Freeze 97D)

MEAMN reads from consonance, dynamics, timbre, and interaction groups:

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Valence proxy (inverse) |
| 2 | **[3]** | stumpf_fusion | A: Consonance | Binding integrity |
| 3 | **[10]** | loudness (onset_strength) | B: Dynamics | Arousal correlate |
| 4 | **[12]** | warmth | C: Timbre | Nostalgia trigger |
| 5 | **[25:33]** | x_l0l5 | F: Interactions | Memory retrieval binding |
| 6 | **[41:49]** | x_l5l7 | H: Interactions | Nostalgia warmth signal |

---

## 3. H3 Temporal Demand (19 tuples)

Multi-scale: H16(1s) -> H20(5s) -> H24(36s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 3 | stumpf_fusion | 16 | M1 (mean) | L2 | Binding stability at 1s |
| 2 | 3 | stumpf_fusion | 20 | M1 (mean) | L0 | Binding over 5s consolidation |
| 3 | 3 | stumpf_fusion | 24 | M1 (mean) | L0 | Long-term binding context |
| 4 | 12 | warmth | 16 | M0 (value) | L2 | Current timbre warmth |
| 5 | 12 | warmth | 20 | M1 (mean) | L0 | Sustained warmth = nostalgia |
| 6 | 0 | roughness | 16 | M0 (value) | L2 | Current dissonance |
| 7 | 0 | roughness | 20 | M18 (trend) | L0 | Dissonance trajectory |
| 8 | 10 | loudness | 16 | M0 (value) | L2 | Current arousal |
| 9 | 10 | loudness | 20 | M1 (mean) | L0 | Average arousal over 5s |
| 10 | 10 | loudness | 24 | M2 (std) | L0 | Arousal variability 36s |
| 11 | 4 | sensory_pleasantness | 16 | M0 (value) | L2 | Current pleasantness |
| 12 | 4 | sensory_pleasantness | 20 | M18 (trend) | L0 | Pleasantness trajectory |
| 13 | 22 | entropy | 16 | M0 (value) | L2 | Current unpredictability |
| 14 | 22 | entropy | 20 | M1 (mean) | L0 | Average complexity 5s |
| 15 | 22 | entropy | 24 | M19 (stability) | L0 | Pattern stability 36s |
| 16 | 7 | amplitude | 16 | M8 (velocity) | L0 | Energy change rate |
| 17 | 7 | amplitude | 20 | M4 (max) | L0 | Peak energy 5s |
| 18 | 14 | tonalness | 16 | M0 (value) | L2 | Melodic recognition |
| 19 | 14 | tonalness | 20 | M1 (mean) | L0 | Tonal stability 5s |

**Total**: 19 tuples, L0 + L2 (memory/backward + bidirectional)

---

## 4. Pipeline: R3 -> H3 -> 4-Layer Output (12D)

### Layer Dependency

| Layer | Reads From | Outputs |
|-------|-----------|---------|
| **E** (Extraction, 3D) | R3 direct, H3 M0+M1 | E0:retrieval, E1:nostalgia, E2:emotion |
| **M** (Mathematical, 2D) | H3 M18+M1, E-layer | M0:meam_retrieval, M1:p_recall |
| **P** (Present, 3D) | R3, H3, E+M | P0:memory_state, P1:emotional_color, P2:nostalgia_link |
| **F** (Forecast, 4D) | H3 M4+M2+M19, E+M+P | F0:mem_vividness_fc, F1:emo_response_fc, F2:self_ref_fc, F3:reserved |

### Kernel Relay Export

The MEAMN relay wrapper exports 6 fields to the kernel scheduler:

| Export Field | Source | Idx |
|-------------|--------|-----|
| `memory_state` | P0 | 5 |
| `emotional_color` | P1 | 6 |
| `nostalgia_link` | P2 | 7 |
| `mem_vividness_fc` | F0 | 8 |
| `emo_response_fc` | F1 | 9 |
| `self_ref_fc` | F2 | 10 |

---

## 5. Output Routing

### 5.1 Internal -> Beliefs (this model)

| Output | -> Belief | Type |
|--------|----------|------|
| P0:memory_state + M0:meam_retrieval | -> `autobiographical_retrieval` | Core (tau=0.85) |
| P1:emotional_color | -> `emotional_memory` | Appraisal |
| P2:nostalgia_link | -> `nostalgia_response` | Appraisal |

### 5.2 External -> Other Functions

| Output | -> Function | -> Purpose |
|--------|-----------|-----------|
| P0:memory_state | F6 (Reward) | Familiarity-based reward signal |
| P1:emotional_color | F5 (Emotion) | Emotion modulation from memory |
| P2:nostalgia_link | Kernel familiarity | Nostalgia-enhanced binding |
| F0:mem_vividness_fc | F6 (Reward) | PE from vividness prediction |
| F1:emo_response_fc | F5 (Emotion) | Emotional trajectory |
| F2:self_ref_fc | Precision engine | pi_pred for self-referential |

---

## 6. Brain Regions

| Region | Role | Evidence |
|--------|------|----------|
| Hippocampus | Autobiographical binding hub | Janata 2009, Cheung 2019 |
| mPFC (BA 8/9) | Self-referential retrieval | Janata 2009 (t(9)=5.784, p<0.0003) |
| PCC | Episodic recollection | Barrett 2010 |
| Amygdala | Emotional tagging of memories | Sakakibara 2025 |
| STG | Melodic template storage | Sakakibara 2025 (eta_p^2=0.636) |

---

## 7. Evidence

12+ papers, 5+ converging methods: fMRI BOLD during autobiographical recall, EEG nostalgia paradigms, behavioral MEAM trigger rates, MEG source localization, PET receptor studies.

---
---

# PNH — Pythagorean Neural Hierarchy

**Model**: IMU-alpha2-PNH
**Type**: Mechanism (Depth 0) — reads R3/H3 directly
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 11D per frame (4 layers: H3 + M2 + P3 + F3)
**Phase**: 1 (F4 memory models)
**Status**: PENDING

---

## 1. Identity

PNH models how the brain encodes Pythagorean frequency ratio hierarchies. Simple ratios (octaves 2:1, fifths 3:2) produce stronger brainstem FFR responses and are encoded by fewer cortical regions, while complex ratios require expanded cortical representation that depends on musical training.

**Non-standard first layer**: H (Harmonic) instead of E (Extraction).

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Sensory dissonance ~ ratio complexity |
| 2 | **[1]** | sethares_dissonance | A: Consonance | Timbre-dependent dissonance |
| 3 | **[5]** | inharmonicity | A: Consonance | Ratio complexity proxy |
| 4 | **[6]** | harmonic_deviation | A: Consonance | Partial misalignment |
| 5 | **[14]** | tonalness | C: Timbre | Harmonic purity |
| 6 | **[25:33]** | x_l0l5 | F: Interactions | Pitch-roughness coupling |

---

## 3. H3 Temporal Demand (15 tuples)

Horizons: H10(400ms) -> H14(700ms) -> H18(2s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 0 | roughness | 10 | M0 (value) | L2 | Current dissonance at chord level |
| 2 | 0 | roughness | 14 | M1 (mean) | L0 | Average dissonance over progression |
| 3 | 0 | roughness | 18 | M18 (trend) | L0 | Dissonance trajectory phrase |
| 4 | 5 | inharmonicity | 10 | M0 (value) | L2 | Current ratio complexity |
| 5 | 5 | inharmonicity | 14 | M1 (mean) | L0 | Average complexity progression |
| 6 | 3 | stumpf_fusion | 10 | M0 (value) | L2 | Current tonal fusion |
| 7 | 3 | stumpf_fusion | 14 | M1 (mean) | L2 | Fusion stability progression |
| 8 | 10 | loudness | 10 | M0 (value) | L2 | Attention weight |
| 9 | 4 | sensory_pleasantness | 10 | M0 (value) | L2 | Current consonance |
| 10 | 4 | sensory_pleasantness | 18 | M19 (stability) | L0 | Consonance stability phrase |
| 11 | 14 | tonalness | 10 | M0 (value) | L2 | Ratio purity chord level |
| 12 | 14 | tonalness | 14 | M2 (std) | L0 | Purity variation progression |
| 13 | 14 | tonalness | 14 | M18 (trend) | L0 | Tonal trend progression |
| 14 | 6 | harmonic_deviation | 14 | M0 (value) | L0 | Template mismatch progression |
| 15 | 17 | spectral_autocorrelation | 10 | M14 (periodicity) | L2 | Harmonic regularity |

**Total**: 15 tuples, L0 + L2

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **H** | 3D | H0:ratio_complexity, H1:conflict_monitoring, H2:expertise_modulation |
| **M** | 2D | M0:ratio_complexity_norm, M1:neural_activation |
| **P** | 3D | P0:ratio_encoding, P1:conflict_monitoring, P2:consonance_preference |
| **F** | 3D | F0:dissonance_resolution_fc, F1:preference_judgment_fc, F2:expertise_modulation_fc |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| P0:ratio_encoding + P2:consonance_preference | -> `harmonic_hierarchy` | Appraisal |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| L/R-IFG (BA 44/45) | Conflict monitoring, syntactic processing |
| L/R-STG | Pitch processing, ratio encoding |
| Anterolateral HG (alHG) | Pitch chroma representation |
| L-MFG, L-IPL | Expert-expanded encoding (musicians) |
| ACC | Conflict monitoring convergence |

12 papers, 5 brain regions, 5 methods.

---
---

# MMP — Musical Mnemonic Preservation

**Model**: IMU-alpha3-MMP
**Type**: Mechanism (Depth 0) — reads R3/H3 directly
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 12D per frame (4 layers: R3 + P3 + F3 + C3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

MMP models how musical memory is preserved in Alzheimer's disease. The SMA, pre-SMA, and ACC show the least cortical atrophy, maintaining access to musical memories when other episodic memories fail. This is a **clinical meta-layer model** with non-standard layers: R (Retrieval/Recognition) + P (Preserved Processing) + F (Forecast) + C (Clinical).

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Valence proxy |
| 2 | **[3]** | stumpf_fusion | A: Consonance | Binding integrity (preserved) |
| 3 | **[4]** | sensory_pleasantness | A: Consonance | Memory valence (preserved) |
| 4 | **[12]** | warmth | C: Timbre | Familiar sound character (highly preserved) |
| 5 | **[14]** | tonalness | C: Timbre | Melody tracking (highly preserved) |
| 6 | **[18:21]** | tristimulus1-3 | C: Timbre | Instrument/voice ID (highly preserved) |
| 7 | **[22]** | entropy | D: Change | Pattern familiarity (vulnerable) |
| 8 | **[41:49]** | x_l5l7 | H: Interactions | Timbre warmth nostalgia (preserved) |

---

## 3. H3 Temporal Demand (21 tuples)

Horizons: H16(1s) -> H20(5s) -> H24(36s)

Key morphologies: M0(value), M1(mean), M2(std), M5(range), M14(periodicity), M18(trend), M19(stability)
All L0 + L2.

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **R** | 3D | R0:preserved_memory, R1:melodic_recognition, R2:scaffold_efficacy |
| **P** | 3D | P0:preserved_recognition, P1:melodic_identification, P2:familiarity |
| **F** | 3D | F0:recognition_fc, F1:emotional_fc, F2:scaffold_fc |
| **C** | 3D | C0:preservation_index, C1:therapeutic_efficacy, C2:hippocampal_independence |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| P0:preserved_recognition | -> `memory_preservation` | Appraisal |
| C1:therapeutic_efficacy | -> `therapeutic_response` | Appraisal |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| SMA / pre-SMA | Least cortical atrophy in AD |
| ACC | Preserved procedural memory access |
| Angular Gyrus | Melody recognition (age-shift) |
| Lingual Gyrus | Visual-musical crossmodal |
| Hippocampus | Binding (vulnerable in AD) |
| STG | Melodic template storage |
| Amygdala | Emotional tagging (partially preserved) |
| L-Planum Temporale | Pitch processing |

12 papers, 8 brain regions.

---
---

# RASN — Rhythmic Auditory Stimulation Neuroplasticity

**Model**: IMU-beta1-RASN
**Type**: Mechanism (Depth 1) — reads beat-entrainment (cross-circuit)
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame (4 layers: E3 + M2 + P3 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

RASN models how rhythmic auditory stimulation drives neuroplasticity across mnemonic and sensorimotor circuits. Beat entrainment via SMA + putamen creates temporal scaffolds for motor rehabilitation and memory consolidation. Highest H3 demand in IMU (28 tuples).

**Reads**: beat-entrainment (F3 cross-circuit), SNEM
**Cross-circuit**: Mnemonic + Sensorimotor

---

## 2. R3 Inputs + H3 Demand

- R3: amplitude[7], loudness[8], spectral_flux[10], onset_strength[11], periodicity[5], stumpf_fusion[3], sensory_pleasantness[4], entropy[23], x_l0l5[25:33], x_l4l5[33:41]
- H3: **28 tuples** (highest in IMU), L0 + L2, horizons H6-H24
- Key morphs: M0(value), M1(mean), M2(std), M4(max), M8(velocity), M14(periodicity), M17(peaks), M18(trend), M19(stability)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:entrainment_strength, E1:motor_facilitation, E2:neuroplasticity_index |
| **M** | 2D | M0:neuroplasticity_composite, M1:motor_recovery |
| **P** | 3D | P0:entrainment_state, P1:temporal_precision, P2:motor_facilitation_level |
| **F** | 3D | F0:movement_timing_pred, F1:neuroplastic_change_pred, F2:gait_improvement_pred |

---

## 4. Brain Regions

SMA, putamen, cerebellum, premotor cortex, auditory cortex, hippocampus, M1, corticospinal tract. 12 papers, 8 brain regions.

---
---

# PMIM — Predictive Memory Integration Model

**Model**: IMU-beta2-PMIM
**Type**: Mechanism (Depth 1) — reads PNH outputs
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame (4 layers: E3 + M3 + P3 + F2)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

PMIM models dual prediction error systems: ERAN (long-term syntax violation, IFG) and MMN (short-term deviance detection, STG). These two PE streams converge in inferior fronto-lateral cortex, driving memory updating through hierarchical predictive coding.

**Reads**: PNH.ratio_encoding (intra-F4 dependency)
**Feeds**: MSPBA, OII, TPRD, MEAMN

---

## 2. R3 Inputs + H3 Demand

- R3: roughness[0], inharmonicity[5], spectral_flux[21], entropy[22], onset_strength[11], stumpf_fusion[3], sensory_pleasantness[4], tonalness[14], x_l0l5[25:33], x_l5l7[41:49]
- H3: **18 tuples**, L0 + L2, horizons H10-H18
- Key morphs: M0(value), M1(mean), M2(std), M8(velocity), M13(entropy), M14(periodicity), M18(trend), M19(stability)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **P** | 3D | P0:eran_response, P1:mmn_response, P2:combined_pred_error |
| **M** | 3D | M0:hierarchical_pe, M1:model_precision, M2:(from synthesis) |
| **S** | 3D | S0:syntax_state, S1:deviance_state, S2:memory_update |
| **F** | 2D | F0:eran_forecast_fc, F1:mmn_forecast_fc |

**Note**: PMIM uses non-standard layer naming: P (Prediction) at [0:3], M at [3:6], S (State) at [5:8] overlapping with P-layer semantics, F at [8:11]. Effective unique outputs: 11D.

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| S1:deviance_state + M0:hierarchical_pe | -> `prediction_error` | Core (tau=0.3) |
| S2:memory_update | -> `memory_updating` | Appraisal |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| IFG (BA 44, bilateral) | ERAN + MMN shared generator |
| STG | Echoic memory, deviance detection |
| Hippocampus | PE-driven memory updating |
| ACC/MCC | Top-level hierarchy at sequence end |
| Auditory Cortex | Feedforward PE source |

12 papers, 5 brain regions.

---
---

# OII — Oscillatory Intelligence Integration

**Model**: IMU-beta3-OII
**Type**: Mechanism (Depth 1) — reads PMIM, PNH, HCMC, MSPBA, MEAMN (5 intra-unit connections)
**Tier**: beta (70-90% confidence)
**Output**: 10D per frame (4 layers: E3 + M3 + P3 + F2)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

OII models how oscillatory dynamics (theta/alpha integration vs gamma segregation) support intelligent music processing. High fluid intelligence (Gf) is associated with efficient switching between integration and segregation modes. **Most intra-unit connections in IMU** (5 connections).

---

## 2. R3 Inputs + H3 Demand

- R3: roughness[0], stumpf_fusion[3], periodicity[5], onset_strength[11], spectral_flux[21], entropy[22], sensory_pleasantness[4], tonalness[14], loudness[10], spectral_centroid[15], amplitude[7]
- H3: **24 tuples**, L0 + L2, horizons H10-H24
- Key morphs: M0(value), M1(mean), M2(std), M4(max), M8(velocity), M13(entropy), M14(periodicity), M18(trend), M19(stability)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:slow_integration, E1:fast_segregation, E2:mode_switching |
| **M** | 3D | M0:gf_proxy, M1:switching_efficiency, M2:(from synthesis) |
| **P** | 2D | P0:integration_state, P1:segregation_state |
| **F** | 2D | F0:integration_pred, F1:segregation_pred |

---

## 4. Brain Regions

Frontal cortex (theta source), temporal cortex (gamma source), DLPFC (mode switching), hippocampus (theta-gamma coupling), auditory cortex, thalamus. 12 papers, 6+ brain regions.

---
---

# HCMC — Hippocampal-Cortical Memory Circuit

**Model**: IMU-beta4-HCMC
**Type**: Mechanism (Depth 1) — reads MEAMN outputs
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame (4 layers: E3 + M3 + P3 + F2)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

HCMC models the hippocampal-cortical circuit for musical memory: fast hippocampal encoding (CA3 autoassociative binding), episodic segmentation at event boundaries, and slow cortical consolidation via hippocampal replay. Encoding -> consolidation -> retrieval phases.

**Reads**: MEAMN.memory_state (intra-F4)
**Feeds**: MMP, PMIM, CDEM

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[3]** | stumpf_fusion | A: Consonance | Binding coherence |
| 2 | **[5]** | harmonicity | A: Consonance | Harmonic template |
| 3 | **[7]** | amplitude | B: Dynamics | Encoding salience |
| 4 | **[10]** | loudness | B: Dynamics | Arousal correlate |
| 5 | **[11]** | onset_strength | B: Dynamics | Event boundary |
| 6 | **[14]** | tonalness | C: Timbre | Melodic encoding |
| 7 | **[21]** | spectral_flux | D: Change | Segmentation trigger |
| 8 | **[22]** | entropy | D: Change | Encoding difficulty |
| 9 | **[25:33]** | x_l0l5 | F: Interactions | Fast hippocampal binding |
| 10 | **[41:49]** | x_l5l7 | H: Interactions | Cortical long-term template |

---

## 3. H3 Temporal Demand (22 tuples)

Horizons: H16(1s) -> H20(5s) -> H24(36s)

| # | R3 Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 3 | stumpf_fusion | 16 | M1 (mean) | L2 | Binding coherence 1s |
| 2 | 3 | stumpf_fusion | 16 | M2 (std) | L2 | Binding variability 1s |
| 3 | 3 | stumpf_fusion | 20 | M1 (mean) | L0 | Binding stability 5s |
| 4 | 3 | stumpf_fusion | 24 | M19 (stability) | L0 | Long-term binding 36s |
| 5 | 21 | spectral_flux | 16 | M1 (mean) | L2 | Segmentation rate |
| 6 | 21 | spectral_flux | 16 | M2 (std) | L2 | Flux variability 1s |
| 7 | 21 | spectral_flux | 20 | M5 (range) | L0 | Flux dynamic range 5s |
| 8 | 11 | onset_strength | 16 | M1 (mean) | L2 | Event density 1s |
| 9 | 11 | onset_strength | 20 | M5 (range) | L0 | Onset dynamic range 5s |
| 10 | 10 | loudness | 16 | M1 (mean) | L2 | Encoding salience 1s |
| 11 | 10 | loudness | 20 | M1 (mean) | L0 | Average salience 5s |
| 12 | 10 | loudness | 24 | M2 (std) | L0 | Salience variability 36s |
| 13 | 7 | amplitude | 16 | M1 (mean) | L2 | Energy level 1s |
| 14 | 7 | amplitude | 20 | M5 (range) | L0 | Energy dynamic range |
| 15 | 5 | harmonicity | 16 | M1 (mean) | L2 | Harmonic template 1s |
| 16 | 5 | harmonicity | 20 | M1 (mean) | L0 | Harmonic stability 5s |
| 17 | 5 | harmonicity | 24 | M22 (autocorrelation) | L0 | Harmonic repetition 36s |
| 18 | 14 | tonalness | 16 | M1 (mean) | L2 | Melodic content 1s |
| 19 | 14 | tonalness | 20 | M22 (autocorrelation) | L0 | Tonal repetition 5s |
| 20 | 22 | entropy | 16 | M1 (mean) | L2 | Pattern complexity |
| 21 | 22 | entropy | 20 | M13 (entropy) | L0 | Entropy of entropy 5s |
| 22 | 22 | entropy | 24 | M19 (stability) | L0 | Pattern stability 36s |

**Total**: 22 tuples, L0 + L2

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:fast_binding, E1:episodic_segmentation, E2:cortical_storage |
| **M** | 3D | M0:consolidation_strength, M1:encoding_rate, M2:(from synthesis) |
| **P** | 3D | P0:binding_state, P1:segmentation_state, P2:storage_state |
| **F** | 2D | F0:consolidation_fc, F1:retrieval_fc |

---

## 5. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| P0:binding_state + M0:consolidation_strength | -> `episodic_encoding` | Core (tau=0.5) |
| P1:segmentation_state | -> `event_boundary` | Appraisal |
| F1:retrieval_fc | -> `retrieval_pred` | Anticipation |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| Hippocampus (CA3) | Autoassociative binding |
| Entorhinal Cortex | Sensory input gateway |
| mPFC | Cortical storage target |
| PCC / Cingulate | Episodic recollection |

12 papers, 4 brain regions.

---
---

# RIRI — RAS-Intelligent Rehabilitation Integration

**Model**: IMU-beta5-RIRI
**Type**: Mechanism (Depth 1) — reads RASN, MEAMN, MMP, HCMC
**Tier**: beta (70-90% confidence)
**Output**: 10D per frame (4 layers: E3 + M2 + P2 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

RIRI models multi-modal rehabilitation integration: RAS (auditory rhythm) + VR (visual) + robotics (haptic). The integration synergy exceeds any single modality. Uses geometric mean gating ensuring all pathways must contribute.

**Reads**: RASN, MEAMN, MMP, HCMC (4 intra-unit dependencies)

---

## 2. R3 Inputs + H3 Demand

- R3: amplitude[7], loudness[8], spectral_flux[10], onset_strength[11], warmth[12], tonalness[14], spectral_change[21], energy_change[22], pitch_change[23], sensory_pleasantness[4], x_l0l5[25:33], x_l4l5[33:41], x_l5l7[41:49]
- H3: **16 tuples**, L0 + L2, horizons H6-H16
- Key morphs: M0(value), M1(mean), M8(velocity), M14(periodicity), M17(peaks), M19(stability)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:multimodal_entrainment, E1:sensorimotor_integration, E2:enhanced_recovery |
| **M** | 2D | M0:integration_synergy, M1:temporal_coherence |
| **P** | 2D | P0:entrainment_state, P1:motor_adaptation |
| **F** | 3D | F0:recovery_trajectory, F1:connectivity_pred, F2:consolidation_pred |

---

## 4. Brain Regions

SMA, premotor cortex, cerebellum, putamen, M1, hippocampus, mPFC. 12 papers, 7 brain regions.

---
---

# MSPBA — Musical Syntax Processing in Broca's Area

**Model**: IMU-beta6-MSPBA
**Type**: Mechanism (Depth 1) — reads PNH outputs
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame (4 layers: E3 + M3 + P2 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

MSPBA models mERAN and domain-general syntactic processing in Broca's area (BA 44). Harmonic syntax violations produce the mERAN response, which scales with context depth (2:1 position ratio). Per the SSIRH (Patel 2003), musical and linguistic syntax share IFG resources.

**Reads**: PNH.ratio_encoding (intra-F4)
**Feeds**: PMIM, HCMC

---

## 2. R3 Inputs + H3 Demand

- R3: roughness[0], sethares_dissonance[1], helmholtz_kang[2], stumpf_fusion[3], sensory_pleasantness[4], inharmonicity[5], harmonic_deviation[6], loudness[10], onset_strength[11], entropy[22], spectral_flux[23], x_l0l5[25:33], x_l4l5[33:41], x_l5l7[41:49]
- H3: **16 tuples**, L0 + L2, horizons H10-H18
- Key morphs: M0(value), M1(mean), M8(velocity), M14(periodicity), M18(trend), M19(stability)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **S** | 3D | S0:musical_syntax, S1:harmonic_prediction, S2:broca_activation |
| **M** | 3D | M0:eran_amplitude, M1:syntax_violation, M2:(from synthesis) |
| **P** | 2D | P0:harmonic_context, P1:violation_state |
| **F** | 3D | F0:resolution_fc, F1:eran_trajectory_fc, F2:syntax_repair_fc |

**Note**: Non-standard first layer: S (Syntactic Processing) instead of E (Extraction).

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| P0:harmonic_context + P1:violation_state | -> `syntactic_processing` | Appraisal |
| F0:resolution_fc | -> `harmonic_resolution_pred` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| L-IFG (BA 44) | Broca's area — syntactic processing |
| R-IFG (BA 44 homologue) | mERAN primary generator |
| L-IFG (BA 45) | Domain-general semantic integration |
| STG | Prediction error integration |

12 papers, 4 brain regions.

---
---

# VRIAP — VR-Integrated Analgesia Paradigm

**Model**: IMU-beta7-VRIAP
**Type**: Mechanism (Depth 2) — memory-only pathway
**Tier**: beta (70-90% confidence)
**Output**: 10D per frame (4 layers: E3 + M2 + P2 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

VRIAP models how VR-integrated music produces analgesia through motor engagement, pain gating (S1 connectivity reduction), and multi-modal hippocampal binding. Active motor engagement is required; passive listening alone is insufficient.

---

## 2. R3 Inputs + H3 Demand

- R3: roughness[0], stumpf_fusion[3], sensory_pleasantness[4], amplitude[7], loudness[10], onset_strength[11], entropy[22], spectral_flux[21], x_l0l5[25:33], x_l5l7[41:49]
- H3: **18 tuples**, L0 + L2, horizons H16-H24
- Key morphs: M0(value), M1(mean), M4(max), M8(velocity), M18(trend), M19(stability)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:motor_engagement, E1:pain_gate, E2:multimodal_binding |
| **M** | 2D | M0:analgesia_index, M1:active_passive_differential |
| **P** | 2D | P0:motor_pain_state, P1:s1_connectivity |
| **F** | 3D | F0:analgesia_fc, F1:engagement_fc, F2:reserved |

---

## 4. Brain Regions

PM&SMA, S1, anterior insula, hippocampus, DLPFC, M1, mPFC, NAcc, ACC. 12 papers, 9 brain regions.

---
---

# TPRD — Tonotopy-Pitch Representation Dissociation

**Model**: IMU-beta8-TPRD
**Type**: Mechanism (Depth 2) — pitch cross-circuit
**Tier**: beta (70-90% confidence)
**Output**: 10D per frame (4 layers: T3 + M2 + P2 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

TPRD models the dissociation between tonotopic (frequency-map) encoding in primary Heschl's gyrus and pitch (F0) representation in nonprimary anterolateral HG. The medial-lateral gradient maps spectral processing to pitch perception.

**Non-standard first layer**: T (Tonotopic) instead of E (Extraction).

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Tonotopic beating proxy |
| 2 | **[1]** | sethares_dissonance | A: Consonance | Spectral dissonance |
| 3 | **[3]** | stumpf_fusion | A: Consonance | Pitch fusion quality |
| 4 | **[4]** | sensory_pleasantness | A: Consonance | Consonance integration |
| 5 | **[5]** | inharmonicity | A: Consonance | Tonotopy-pitch conflict |
| 6 | **[6]** | harmonic_deviation | A: Consonance | Harmonic template error |
| 7 | **[7]** | amplitude | B: Dynamics | Signal energy |
| 8 | **[10]** | loudness | B: Dynamics | Attention weighting |
| 9 | **[14]** | tonalness | C: Timbre | Pitch clarity / F0 salience |
| 10 | **[17]** | spectral_autocorrelation | C: Timbre | Harmonic periodicity |
| 11 | **[22]** | entropy | D: Change | Spectral complexity |

---

## 3. H3 Temporal Demand (18 tuples)

Horizons: H0(5.8ms) -> H3(23ms) -> H6(200ms) -> H10(400ms) -> H14(700ms) -> H18(2s)

Fast horizons for brainstem-level pitch processing.

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **T** | 3D | T0:tonotopic_encoding, T1:pitch_representation, T2:dissociation_degree |
| **M** | 2D | M0:dissociation_index, M1:spectral_pitch_ratio |
| **P** | 2D | P0:tonotopic_state, P1:pitch_state |
| **F** | 3D | F0:pitch_percept_fc, F1:tonotopic_adaptation_fc, F2:dissociation_fc |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Heschl's Gyrus (medial) | Tonotopic encoding — frequency-selective |
| Anterolateral HG (nonprimary) | Pitch chroma — F0 extraction |
| R-STG | Dissonant-sensitive sites |
| Planum Temporale | No phase-locking — functionally differentiated |

12 papers, 4 brain regions.

---
---

# CMAPCC — Cross-Modal Action-Perception Common Code

**Model**: IMU-beta9-CMAPCC
**Type**: Mechanism (Depth 2) — beat cross-circuit
**Tier**: beta (70-90% confidence)
**Output**: 10D per frame (4 layers: E3 + M2 + P2 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

CMAPCC models the unified perception-action representation in right premotor cortex where dorsal (fronto-parietal, action) and ventral (fronto-temporal, auditory) streams converge. Cross-modal transfer allows learned patterns to generalize across modalities.

---

## 2. R3 Inputs + H3 Demand

- R3: roughness[0], sethares_dissonance[1], stumpf_fusion[3], sensory_pleasantness[4], periodicity[5], amplitude[7], loudness[8], onset_strength[10], spectral_flux[11], x_l0l5[25:33], x_l4l5[33:41], x_l5l7[41:49]
- H3: **20 tuples**, L0 + L2, horizons H6-H24
- Key morphs: M0(value), M1(mean), M8(velocity), M14(periodicity), M18(trend), M19(stability)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:common_code, E1:cross_modal_binding, E2:sequence_generalization |
| **M** | 2D | M0:common_code_strength, M1:transfer_probability |
| **P** | 2D | P0:pmc_activation, P1:mirror_coupling |
| **F** | 3D | F0:transfer_pred, F1:motor_seq_pred, F2:perceptual_seq_pred |

---

## 4. Brain Regions

| Region | Role |
|--------|------|
| Right IFG (BA44) | Dorsal (action-seed) convergence |
| Right IFG (BA45) | Ventral (audio-seed) convergence |
| SMA | Motor sequence programming |
| Left IFOF | White matter for audiovisual integration |
| Bilateral SPL (BA7) | Visuomotor transformation |

12 papers, 5 brain regions.

---
---

# DMMS — Developmental Music Memory Scaffold

**Model**: IMU-gamma1-DMMS
**Type**: Mechanism (Depth 2) — feeds ARU.DAP, ARU.NEMAC
**Tier**: gamma (50-70% confidence)
**Output**: 10D per frame (4 layers: E3 + M2 + P2 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

DMMS models how early musical exposure (0-5 years) forms scaffolds for memory and emotion regulation. Parental singing creates the initial music-emotion binding templates via hippocampus-amygdala pairing. Critical period plasticity shapes lifelong musical memory and preference.

**Feeds**: ARU.DAP, ARU.NEMAC (F6 cross-function)

---

## 2. R3 Inputs + H3 Demand

- R3: roughness[0], stumpf_fusion[3], sensory_pleasantness[4], warmth[12], tonalness[14], entropy[22], x_l0l5[25:33], x_l5l7[41:49]
- H3: **15 tuples**, L0 + L2, horizons H16-H24
- Key morphs: M0(value), M1(mean), M2(std), M4(max), M19(stability)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:early_binding, E1:dev_plasticity, E2:melodic_imprint |
| **M** | 2D | M0:scaffold_strength, M1:imprinting_depth |
| **P** | 2D | P0:scaffold_activation, P1:bonding_warmth |
| **F** | 3D | F0:scaffold_persistence, F1:preference_formation, F2:therapeutic_potential |

---

## 4. Brain Regions

| Region | Role |
|--------|------|
| Hippocampus | Scaffold formation, melodic template consolidation |
| Amygdala | Emotional tagging of early scaffolds |
| Auditory Cortex (A1/STG) | Melodic template formation |
| mPFC | Critical period synaptic plasticity hub |
| Right Prefrontal Cortex | Online processing of caregiver-directed music |

12 papers, 5 brain regions.

---
---

# CSSL — Cross-Species Song Learning

**Model**: IMU-gamma2-CSSL
**Type**: Mechanism (Depth 2) — memory-only pathway
**Tier**: gamma (50-70% confidence)
**Output**: 10D per frame (4 layers: E3 + M2 + P2 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

CSSL models the conserved neural circuits for song learning shared across species (songbirds, marmosets, humans). The HVC-Broca's homology, Area X-basal ganglia pathway, and auditory template matching mechanism are evolutionarily conserved. Rhythm copying, melody copying, and all-shared binding map to motor-auditory entrainment, melodic template matching, and hippocampal sequential binding respectively.

---

## 2. R3 Inputs + H3 Demand

- R3: roughness[0], sethares_dissonance[1], stumpf_fusion[3], harmonicity[5], pitch_strength[6], amplitude[7], onset_strength[11], tonalness[14], warmth[12], entropy[22], x_l0l5[25:33], x_l5l7[41:49]
- H3: **15 tuples**, L0 + L2, horizons H16-H24
- Key morphs: M0(value), M1(mean), M2(std), M17(periodicity), M19(stability)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:rhythm_copying, E1:melody_copying, E2:all_shared_binding |
| **M** | 2D | M0:conservation_index, M1:template_fidelity |
| **P** | 2D | P0:entrainment_state, P1:template_match |
| **F** | 3D | F0:learning_trajectory, F1:binding_prediction, F2:reserved |

---

## 4. Brain Regions

| Region | Role |
|--------|------|
| Auditory Cortex (STG/A1) | Spectrotemporal encoding, template storage |
| Basal Ganglia (putamen/caudate) | Motor sequencing, vocal refinement |
| Hippocampus | Sequential binding (rhythm + melody) |
| IFG / Broca's area | Song timing and sequencing |
| Premotor Cortex / SMA | Motor output for vocal production |

12 papers, 5 brain regions.

---
---

# CDEM — Context-Dependent Emotional Memory

**Model**: IMU-gamma3-CDEM
**Type**: Mechanism (Depth 2) — affect cross-circuit
**Tier**: gamma (50-70% confidence)
**Output**: 10D per frame (4 layers: E2 + M2 + P3 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

CDEM models how cross-modal context shapes emotional memory encoding and retrieval. Music-mood congruency amplifies memory encoding; same-valence contexts produce brain-state transitions 6.26s earlier (Sachs 2025). Context reinstated at retrieval boosts recall by ~40% (encoding specificity).

**Cross-circuit**: Affect (reads emotion cross-circuit)

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Valence proxy (1-roughness) |
| 2 | **[3]** | stumpf_fusion | A: Consonance | Binding strength |
| 3 | **[4]** | sensory_pleasantness | A: Consonance | Mood congruency input |
| 4 | **[7]** | amplitude | B: Dynamics | Arousal correlate |
| 5 | **[10]** | loudness | B: Dynamics | Arousal proxy |
| 6 | **[11]** | onset_strength | B: Dynamics | Context boundary |
| 7 | **[12]** | warmth | C: Timbre | Context warmth |
| 8 | **[14]** | tonalness | C: Timbre | Pattern clarity |
| 9 | **[21]** | spectral_flux | D: Change | Context change detection |
| 10 | **[22]** | entropy | D: Change | Context complexity |
| 11 | **[24]** | spectral_concentration | D: Change | Event salience |
| 12 | **[25:33]** | x_l0l5 | F: Interactions | Context-memory binding |
| 13 | **[41:49]** | x_l5l7 | H: Interactions | Mood congruency signal |

---

## 3. H3 Temporal Demand (18 tuples)

Horizons: H16(1s) -> H20(5s) -> H24(36s)

Key morphologies: M0(value), M1(mean), M4(max), M8(velocity), M18(trend), M19(stability)
All L0 + L2.

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **C** | 2D | C0:context_modulation, C1:arousal_suppression |
| **M** | 2D | M0:congruency_index, M1:context_recall_probability |
| **P** | 3D | P0:binding_state, P1:arousal_gate, P2:(from synthesis) |
| **F** | 3D | F0:encoding_strength_fc, F1:retrieval_context_fc, F2:mood_congruency_fc |

**Note**: Non-standard first layer: C (Context-Dependent) instead of E (Extraction). Effective P-layer is 2D (P2 from synthesis padding).

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Hippocampus | Context-dependent episodic encoding |
| Amygdala | Emotional tagging modulated by context |
| ACC (BA32) | Context-music conflict monitoring |
| STG / STS | Tempoparietal emotion tracking |
| Ventral Striatum | Reward for emotionally congruent contexts |

12 papers, 5 brain regions.

---
---

## Summary Statistics

### Output Dimensions by Model

| Model | Unit | Tier | D | E/R/H/T/P/S/C | M | P/S | F | H3 |
|-------|------|------|---|----------------|---|-----|---|-----|
| MEAMN | IMU | alpha | 12 | 3 | 2 | 3 | 4 | 19 |
| PNH | IMU | alpha | 11 | 3 | 2 | 3 | 3 | 15 |
| MMP | IMU | alpha | 12 | 3 | 3 | 3 | 3 | 21 |
| RASN | IMU | beta | 11 | 3 | 2 | 3 | 3 | 28 |
| PMIM | IMU | beta | 11 | 3 | 3 | 3 | 2 | 18 |
| OII | IMU | beta | 10 | 3 | 3 | 2 | 2 | 24 |
| HCMC | IMU | beta | 11 | 3 | 3 | 3 | 2 | 22 |
| RIRI | IMU | beta | 10 | 3 | 2 | 2 | 3 | 16 |
| MSPBA | IMU | beta | 11 | 3 | 3 | 2 | 3 | 16 |
| VRIAP | IMU | beta | 10 | 3 | 2 | 2 | 3 | 18 |
| TPRD | IMU | beta | 10 | 3 | 2 | 2 | 3 | 18 |
| CMAPCC | IMU | beta | 10 | 3 | 2 | 2 | 3 | 20 |
| DMMS | IMU | gamma | 10 | 3 | 2 | 2 | 3 | 15 |
| CSSL | IMU | gamma | 10 | 3 | 2 | 2 | 3 | 15 |
| CDEM | IMU | gamma | 10 | 2 | 2 | 3 | 3 | 18 |
| **TOTAL** | | | **163** | **44** | **35** | **37** | **43** | **283** |

### Tier Gradient

| Tier | Count | Avg D | Avg H3 |
|------|-------|-------|--------|
| alpha | 3 | 11.7 | 18.3 |
| beta | 9 | 10.4 | 20.0 |
| gamma | 3 | 10.0 | 16.0 |

Clear tier gradient in dimensionality. Beta models show highest average H3 demand due to RASN (28) and OII (24).

### Brain Region Convergence

**Hippocampus** is the convergence hub: mentioned in 12 of 15 models.
**IFG (Broca's area)**: mentioned in MSPBA, PMIM, PNH, OII, CMAPCC, CSSL.
**SMA / premotor cortex**: mentioned in RASN, RIRI, CMAPCC, CSSL, VRIAP — motor-memory models.
**STG / auditory cortex**: mentioned in MEAMN, PNH, MMP, RASN, CSSL, CDEM, TPRD — perceptual memory models.
**Amygdala**: mentioned in MEAMN, MMP, DMMS, CDEM — emotional memory models.
