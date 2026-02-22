# F2 Mechanism Orchestrator — Pattern Recognition & Prediction

**Function**: F2 Pattern Recognition & Prediction
**Models covered**: 10/10 — 3 IMPLEMENTED (α) + 7 PENDING (β/γ)
**Total F2 mechanism output**: 110D (12+14+13+10+11+10+11+9+10+10)
**Beliefs**: 15 (4C + 6A + 5N) — all from α-tier models
**H³ demands**: 173 tuples (57 α-implemented + 116 β/γ-pending)
**Architecture**: Depth-ordered pipeline — 3 relays (Depth 0) → 4 β (Depth 1) → 3 γ (Depth 2)

---

## Model Pipeline (Depth Order)

```
R³ (97D) ───┬────────────────────────────────────────────
H³ tuples ──┤
            ▼
Depth 0:  HTP   (12D, relay, PCU-α1)  ← hierarchical temporal prediction
          SPH   (14D, relay, PCU-α2)  ← spatiotemporal prediction hierarchy
          ICEM  (13D, relay, PCU-α3)  ← information content emotion model
            │
            ▼
Depth 1:  PWUP  (10D, PCU-β1)  ← precision-weighted uncertainty (reads HTP+ICEM)
          WMED  (11D, PCU-β2)  ← working memory–entrainment dissociation (reads PWUP)
          UDP   (10D, PCU-β3)  ← uncertainty-driven pleasure (reads PWUP+WMED)
          CHPI  (11D, PCU-β4)  ← cross-modal harmonic prediction (reads HTP+PWUP+ICEM+WMED)
            │
            ▼
Depth 2:  IGFE  ( 9D, PCU-γ1)  ← individual gamma frequency enhancement
          MAA   (10D, PCU-γ2)  ← multifactorial atonal appreciation
          PSH   (10D, PCU-γ3)  ← prediction silencing hypothesis
```

---
---

# HTP — Hierarchical Temporal Prediction

**Model**: PCU-α1-HTP
**Type**: Relay (Depth 0) — reads R³/H³ directly, no C³ mechanisms
**Tier**: α (Mechanistic, 90-95% confidence)
**Output**: 12D per frame (4 layers: E4 + M3 + P3 + F2)
**Phase**: 0c (after BCH in Phase 0a — consonance validation via HTP)
**Status**: IMPLEMENTED

---

## 1. Identity

HTP models how predictive representations follow a hierarchical temporal pattern: high-level abstract features are predicted ~500ms before input, mid-level ~200ms, low-level ~110ms. Post-stimulus, high-level representations are "silenced" (explained away) while low-level persist as prediction errors.

HTP is a **relay**: it transforms R³ acoustic features and H³ temporal morphologies directly into cognitive-level outputs. All computation is deterministic weighted sums.

---

## 2. R³ Input Map (Post-Freeze 97D)

HTP reads **7 direct R³ indices** from 5 groups:

| # | R³ Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[7]** | amplitude | B: Dynamics | Low-level sensory feature |
| 2 | **[11]** | onset_strength | B: Dynamics | Event boundary detection |
| 3 | **[13]** | sharpness | C: Timbre | Brightness proxy (replaces spectral_centroid) |
| 4 | **[17]** | spectral_autocorrelation | C: Timbre | Cross-band coupling (replaces x_l0l5) |
| 5 | **[21]** | spectral_flux | D: Change | Prediction error trigger (was spectral_change) |
| 6 | **[39]** | pitch_salience | F: Pitch/Chroma | Mid-level dynamics (replaces x_l4l5) |
| 7 | **[60]** | tonal_stability | H: Harmony | High-level structure (replaces x_l5l7) |

---

## 3. H³ Temporal Demand (18 tuples)

Multi-scale: H0(25ms) → H1(50ms) → H3(100ms) → H4(125ms) → H8(500ms) → H16(1s)

| # | R³ Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 7 | amplitude | 0 | M0 (value) | L2 | Instantaneous amplitude 25ms |
| 2 | 7 | amplitude | 3 | M0 (value) | L2 | Amplitude at 100ms context |
| 3 | 7 | amplitude | 3 | M2 (std) | L2 | Amplitude variability — PE proxy |
| 4 | 11 | onset_strength | 0 | M0 (value) | L2 | Instant onset — event boundary |
| 5 | 11 | onset_strength | 1 | M1 (mean) | L2 | Mean onset 50ms — sustained detection |
| 6 | 11 | onset_strength | 3 | M14 (period) | L2 | Onset periodicity — rhythmic regularity |
| 7 | 13 | sharpness | 3 | M0 (value) | L2 | Brightness 100ms — mid-level target |
| 8 | 13 | sharpness | 4 | M8 (velocity) | L0 | Brightness velocity — dynamics |
| 9 | 13 | sharpness | 8 | M1 (mean) | L0 | Mean brightness 500ms — timbral context |
| 10 | 21 | spectral_flux | 3 | M8 (velocity) | L0 | Spectral change velocity — PE trigger |
| 11 | 21 | spectral_flux | 4 | M0 (value) | L0 | Spectral change 125ms — mid-timescale |
| 12 | 60 | tonal_stability | 8 | M0 (value) | L0 | Tonal stability 500ms — high-level |
| 13 | 60 | tonal_stability | 8 | M1 (mean) | L0 | Mean tonal stability 500ms |
| 14 | 60 | tonal_stability | 16 | M1 (mean) | L0 | Mean tonal stability 1s — long-range |
| 15 | 60 | tonal_stability | 16 | M13 (entropy) | L0 | Structural uncertainty 1s |
| 16 | 17 | spectral_auto | 3 | M0 (value) | L2 | Cross-band coupling 100ms |
| 17 | 17 | spectral_auto | 3 | M2 (std) | L2 | Coupling variability — PE |
| 18 | 39 | pitch_salience | 4 | M8 (velocity) | L0 | Pitch salience velocity 125ms |

**Total**: 18 tuples (9 L2 + 9 L0)

---

## 4. Pipeline: R³ → H³ → 4-Layer Output (12D)

```
R³ (7 direct)  ────────────────────────────────────────┐
                                                        ▼
                                                ┌──────────────┐
H³ (18 tuples)  ───────────────────────────────►│  E-LAYER (4D) │
                                                │  Extraction   │
                                                └──────┬───────┘
                                                       │ E0..E3
                                                       ▼
                                                ┌──────────────┐
H³ L2+L0 tuples ──────────────────────────────►│  M-LAYER (3D) │
E-layer outputs  ──────────────────────────────►│  Temporal     │
                                                │  Integration  │
                                                └──────┬───────┘
                                                       │ M0..M2
                                                       ▼
                                                ┌──────────────┐
R³ direct  ─────────────────────────────────────►│  P-LAYER (3D) │
H³ L0+L2   ────────────────────────────────────►│  Cognitive    │
M-layer outputs  ───────────────────────────────►│  Present      │
                                                └──────┬───────┘
                                                       │ P0..P2
                                                       ▼
                                                ┌──────────────┐
H³ L0 (trends)  ───────────────────────────────►│  F-LAYER (2D) │
E-layer outputs  ───────────────────────────────►│  Forecast     │
                                                └──────┬───────┘
                                                       │ F0..F1
                                                       ▼
                                                HTP OUTPUT (12D)
```

### Layer Dependency

| Layer | Reads From | Outputs |
|-------|-----------|---------|
| **E** (Extraction) | R³ direct, H³ tuples | E0:high_level_lead, E1:mid_level_lead, E2:low_level_lead, E3:hierarchy_gradient |
| **M** (Memory) | H³ L2+L0, E-layer | M0:latency_high, M1:latency_mid, M2:latency_low |
| **P** (Present) | R³, H³, M-layer | P0:sensory_match, P1:pitch_prediction, P2:abstract_prediction |
| **F** (Forecast) | H³ L0, E-layer | F0:abstract_future_500ms, F1:midlevel_future_200ms |

---

## 5. Output Routing

### 5.1 Internal → Beliefs (this model)

| Output | → Belief | Type |
|--------|----------|------|
| E0(40%)+E1(30%)+E2(30%) | → `prediction_hierarchy` | Core observe (τ=0.4) |
| P0(50%)+P1(30%)+E3(20%) | → `prediction_accuracy` | Core observe (τ=0.5) |
| E3(50%)+P2(30%)+P1(20%) | → `hierarchy_coherence` | Appraisal source |
| F0:abstract_future_500ms | → `abstract_future` | Anticipation source |
| F1:midlevel_future_200ms | → `midlevel_future` | Anticipation source |

### 5.2 External → Other Models

| Output | → Model | Purpose |
|--------|---------|---------|
| E3:hierarchy_gradient | → PWUP (β1) | Hierarchy informs precision weighting |
| E3:hierarchy_gradient | → CHPI (β4) | Harmonic prediction context |
| E3:hierarchy_gradient | → IGFE (γ1) | Gamma enhancement hierarchy |
| E3:hierarchy_gradient | → PSH (γ3) | Silencing hierarchy target |
| P0:sensory_match | → C³ kernel | Consonance validation (Phase 0c) |
| P1:pitch_prediction | → C³ kernel | Precision engine input (Phase 2b) |

---

## 6. Brain Regions

| Region | HTP Role | Evidence |
|--------|----------|----------|
| **aIPL** | Abstract prediction (~500ms) | de Vries & Wurm 2023 (w=0.80) |
| **STG** | Mid-to-long integration 200-500ms | Norman-Haignere 2022 (w=0.75) |
| **A1/HG** | Low-level prediction (110ms) | Forseth 2020 (w=0.85) |
| **Planum Temporale** | Content prediction via high-gamma | Forseth 2020 (w=0.70) |
| **Hippocampus** | Sequence memory / prediction error | Bonetti 2024 (w=0.65) |
| **ACC** | Prediction error integration | Bonetti 2024 (w=0.60) |

---

## 7. Evidence Summary

| Metric | Value |
|--------|-------|
| Papers | 8 primary |
| Primary finding | ηp²=0.49, F(2)=19.9, p=8.3e-7 (de Vries & Wurm 2023, N=22) |
| Evidence modalities | MEG, iEEG, EEG, review |
| Key constraint | High-level preds precede low-level by ~390ms |
| Falsification | 2/5 confirmed |
| Confidence | 90-95% |

---

*See individual layer files:*
- [HTP-extraction.md](htp/HTP-extraction.md) — E-layer (4D)
- [HTP-temporal-integration.md](htp/HTP-temporal-integration.md) — M-layer (3D)
- [HTP-cognitive-present.md](htp/HTP-cognitive-present.md) — P-layer (3D)
- [HTP-forecast.md](htp/HTP-forecast.md) — F-layer (2D)

---
---

# SPH — Spatiotemporal Prediction Hierarchy

**Model**: PCU-α2-SPH
**Type**: Relay (Depth 0) — reads R³/H³ directly
**Tier**: α (Mechanistic, 90-95% confidence)
**Output**: 14D per frame (4 layers: E4 + M4 + P3 + F3)
**Phase**: 0a (independent relay)
**Status**: IMPLEMENTED

---

## 1. Identity

SPH models how auditory memory recognition engages hierarchical feedforward-feedback loops between Heschl's gyrus, hippocampus, and cingulate, with distinct oscillatory signatures: gamma (>30Hz) for matched/memorised sequences, alpha-beta (2-20Hz) for varied/prediction-error sequences. Final tone reshapes hierarchy — cingulate assumes top position.

SPH is a **relay**: it transforms R³ acoustic features and H³ temporal morphologies directly. Conceptually extends HTP's hierarchical timing to spatiotemporal memory recognition.

---

## 2. R³ Input Map (Post-Freeze 97D)

SPH reads **10 direct R³ indices** from 5 groups:

| # | R³ Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[4]** | sensory_pleasantness | A: Consonance | Memory match indicator |
| 2 | **[7]** | amplitude | B: Dynamics | Deviation detection |
| 3 | **[11]** | onset_strength | B: Dynamics | Event boundary (was spectral_flux) |
| 4 | **[17]** | spectral_autocorrelation | C: Timbre | Feedforward pathway (replaces x_l0l5) |
| 5 | **[21]** | spectral_flux | D: Change | Deviation signal (was spectral_change) |
| 6 | **[22]** | distribution_entropy | D: Change | Rate of distributional change |
| 7 | **[25]** | chroma_C | F: Pitch/Chroma | Tonal identity (v2 expansion) |
| 8 | **[37]** | pitch_height | F: Pitch/Chroma | Sequence element (v2 expansion) |
| 9 | **[39]** | pitch_salience | F: Pitch/Chroma | Pitch clarity modulates match |
| 10 | **[60]** | tonal_stability | H: Harmony | Hierarchy position (replaces x_l5l7) |

---

## 3. H³ Temporal Demand (21 tuples)

Multi-scale: H0(25ms) → H3(100ms) → H4(125ms) → H8(500ms) → H16(1s)

All tuples use L0 (memory) or L2 (integration) — no L1 forward prediction.

**Total**: 21 tuples (13 L2 + 8 L0)

Key demands: onset (3: H0/H3/H3-M14), amplitude (2: H3 value+std), consonance (2: H3/H16), spectral flux (2: H3 value+std), entropy (1: H4-M8), spectral_auto (2: H3/H16), tonal_stability (4: H3/H8/H16/H16-M13), pitch v2 (5: chroma/height/salience at cortical timescales).

---

## 4. Layer Outputs

| Layer | Dims | Key Outputs | Scope |
|-------|------|-------------|-------|
| E (4D) | [0:4] | gamma_match, alpha_beta_error, hierarchy_position, feedforward_feedback | internal |
| M (4D) | [4:8] | match_response, varied_response, gamma_power, alpha_beta_power | internal |
| P (3D) | [8:11] | memory_match, prediction_error, deviation_detection | hybrid |
| F (3D) | [11:14] | next_tone_pred_350ms, sequence_completion_2s, decision_evaluation | external |

---

## 5. Output Routing

### Internal → Beliefs

| Output | → Belief | Type |
|--------|----------|------|
| E0(40%)+P0(30%)+M2(30%) | → `sequence_match` | Core observe (τ=0.45) |
| E1(40%)+P1(30%)+M3(30%) | → `error_propagation` | Appraisal |
| M2(40%)+M3(30%)+E3(30%) | → `oscillatory_signature` | Appraisal |
| F1:sequence_completion_2s | → `sequence_completion` | Anticipation |

### External → Other Models

| Output | → Model | Purpose |
|--------|---------|---------|
| P0:memory_match | → ICEM | Gamma match for information content |
| P1:prediction_error | → PWUP | PE for precision weighting |
| P0:memory_match | → IMU | Memory match signal |
| F1:sequence_completion_2s | → IMU | Sequence completion signal |

---

## 6. Brain Regions

| Region | SPH Role | Evidence |
|--------|----------|----------|
| **A1/HG** | Auditory input, feedforward origin | Bonetti 2024 (w=0.85) |
| **Hippocampus** | Memory match/mismatch comparison | Bonetti 2024 (w=0.80) |
| **ACC** | Prediction error evaluation | Bonetti 2024 (w=0.75) |
| **Medial Cingulate** | Sequence recognition, hierarchy top | Bonetti 2024 (w=0.70) |
| **STG** | Non-primary auditory processing | Norman-Haignere 2022 (w=0.75) |
| **IFG** | Phrase-level chunking | Rimmele 2021 (w=0.60) |

---

## 7. Evidence Summary

| Metric | Value |
|--------|-------|
| Papers | 10 primary |
| Primary finding | Feedforward HG→Hipp→Cing, memorised +350ms, varied -250ms (Bonetti 2024, N=83) |
| Replication | Tonal recognition hippocampus+cingulate (Fernandez-Rubio 2022, N=71) |
| Evidence modalities | MEG+DCM, iEEG, review, single-neuron |
| Core-periphery timescales | η²=0.86 (Golesorkhi 2021, N=89) |
| Falsification | 2/5 confirmed |
| Confidence | 90-95% |

---

*See individual layer files:*
- [SPH-extraction.md](sph/SPH-extraction.md) — E-layer (4D)
- [SPH-temporal-integration.md](sph/SPH-temporal-integration.md) — M-layer (4D)
- [SPH-cognitive-present.md](sph/SPH-cognitive-present.md) — P-layer (3D)
- [SPH-forecast.md](sph/SPH-forecast.md) — F-layer (3D)

---
---

# ICEM — Information Content Emotion Model

**Model**: PCU-α3-ICEM
**Type**: Relay (Depth 0) — reads R³/H³ directly
**Tier**: α (Mechanistic, 90-95% confidence)
**Output**: 13D per frame (4 layers: E4 + M5 + P2 + F2)
**Phase**: 0a (independent relay)
**Status**: IMPLEMENTED

---

## 1. Identity

ICEM models how computational Information Content (IC = -log₂(P(event|context))) peaks predict psychophysiological emotional responses: high IC leads to increased arousal/SCR, decreased HR/valence, and defense cascade activation. IC × entropy interaction determines pleasure (inverted-U: surprise under low uncertainty → high pleasure).

ICEM is a **relay**: it transforms R³/H³ directly. Conceptually extends HTP/SPH prediction to emotional responses.

---

## 2. R³ Input Map (Post-Freeze 97D)

ICEM reads **9 direct R³ indices** from 4 groups:

| # | R³ Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[4]** | sensory_pleasantness | A: Consonance | Valence positive contributor |
| 2 | **[10]** | loudness | B: Dynamics | Perceptual intensity (shifted from old [8]) |
| 3 | **[11]** | onset_strength | B: Dynamics | Event detection for arousal |
| 4 | **[21]** | spectral_flux | D: Change | IC surprise signal |
| 5 | **[22]** | distribution_entropy | D: Change | Distributional surprise |
| 6 | **[38]** | pitch_class_entropy | F: Pitch/Chroma | Melodic unpredictability (replaces I:melodic_entropy) |
| 7 | **[39]** | pitch_salience | F: Pitch/Chroma | Arousal pathway (replaces x_l4l5) |
| 8 | **[51]** | key_clarity | H: Harmony | Tonal grounding (relocated from v2) |
| 9 | **[60]** | tonal_stability | H: Harmony | Valence pathway (replaces x_l5l7) |

---

## 3. H³ Temporal Demand (18 tuples)

IC computation at fast timescales (100ms), emotional response at slower timescales (500ms-1s).

**Total**: 18 tuples (8 L2 + 10 L0)

Key demands: spectral_flux (3: H3 value+std+entropy), entropy (1: H3-M8), onset (2: H3/H8), loudness (2: H3/H16), consonance (2: H3/H8), pitch_salience (2: H4-M8/H16), tonal_stability (3: H8/H16/H16-M13), key_clarity (2: H3/H8), pitch_class_entropy (1: H3).

---

## 4. Layer Outputs

| Layer | Dims | Key Outputs | Scope |
|-------|------|-------------|-------|
| E (4D) | [0:4] | information_content, arousal_response, valence_response, defense_cascade | internal |
| M (5D) | [4:9] | ic_value, arousal_pred, valence_pred, scr_pred, hr_pred | internal |
| P (2D) | [9:11] | surprise_signal, emotional_evaluation | hybrid |
| F (2D) | [11:13] | arousal_change_1_3s, valence_shift_2_5s | external |

---

## 5. Output Routing

### Internal → Beliefs

| Output | → Belief | Type |
|--------|----------|------|
| E0(40%)+M0(30%)+P0(30%) | → `information_content` | Core observe (τ=0.35) |
| E3(50%)+M3(30%)+M4(20%) | → `defense_cascade` | Appraisal |
| E1(40%)+M1(30%)+P0(30%) | → `arousal_scaling` | Appraisal |
| E2(40%)+M2(30%)+P1(30%) | → `valence_inversion` | Appraisal |
| F0:arousal_change_1_3s | → `arousal_change_pred` | Anticipation |
| F1:valence_shift_2_5s | → `valence_shift_pred` | Anticipation |

### External → Other Models

| Output | → Model | Purpose |
|--------|---------|---------|
| E0:information_content | → PWUP (β1) | IC for precision weighting |
| E0:information_content | → CHPI (β4) | Surprise modulation |
| P0:surprise_signal | → UDP (β3) | Arousal for reward |
| P1:emotional_evaluation | → ARU | Emotional arousal/valence |

---

## 6. Brain Regions

| Region | ICEM Role | Evidence |
|--------|-----------|----------|
| **STG** | Strongest uncertainty × surprise | Cheung 2019 (w=0.85) |
| **Amygdala** | Joint uncertainty × surprise | Cheung 2019 (w=0.80) |
| **NAc** | Peak pleasure dopamine / uncertainty | Salimpoor 2011 (w=0.75) |
| **Caudate** | Anticipatory dopamine | Salimpoor 2011 (w=0.70) |
| **vmPFC** | Precision weighting of PE | Harding 2025 (w=0.65) |
| **OFC** | Reward processing during chills | Chabin 2020 (w=0.60) |

---

## 7. Evidence Summary

| Metric | Value |
|--------|-------|
| Papers | 10 primary |
| Primary finding | IC → arousal↑, valence↓, SCR↑, HR↓ (Egermann 2013, N=50) |
| IC × entropy | R²=0.654, saddle-shaped pleasure (Cheung 2019, N=79) |
| Inverted-U | Confirmed (Gold 2019, N=70; Gold 2023, N=24) |
| Dopamine | Caudate anticipation, NAc peak (Salimpoor 2011, N=8) |
| Evidence modalities | fMRI, PET, psychophysiology, behavioral, HD-EEG |
| Falsification | 4/7 confirmed |
| Confidence | 90-95% |

---

*See individual layer files:*
- [ICEM-extraction.md](icem/ICEM-extraction.md) — E-layer (4D)
- [ICEM-temporal-integration.md](icem/ICEM-temporal-integration.md) — M-layer (5D)
- [ICEM-cognitive-present.md](icem/ICEM-cognitive-present.md) — P-layer (2D)
- [ICEM-forecast.md](icem/ICEM-forecast.md) — F-layer (2D)

---
---

# PWUP — Precision-Weighted Uncertainty Processing

**Model**: PCU-β1-PWUP
**Type**: Depth 1 — reads α-tier relay outputs + R³/H³
**Tier**: β (Observation-compatible, 70-90% confidence)
**Output**: 10D per frame (3 layers: E4 + P3 + F3)
**Phase**: 1 (after α relays)
**Status**: PENDING

---

## 1. Identity

PWUP describes how prediction errors are precision-weighted according to contextual uncertainty — in high-uncertainty contexts (atonal music), prediction error responses are attenuated compared to mispredicted stimuli in tonal contexts. This implements the core predictive coding principle that precision modulates the influence of prediction errors on belief updating.

---

## 2. R³ Input Map (Post-Freeze 97D)

PWUP reads ~8 direct R³ features (dissolved E/I group features must be remapped):

| # | R³ Index | Feature | Group | Purpose |
|---|----------|---------|-------|---------|
| 1 | **[4]** | sensory_pleasantness | A | Tonal precision proxy |
| 2 | **[5]** | periodicity | A | Tonal certainty |
| 3 | **[11]** | onset_strength | B | Event salience (was [10] spectral_flux) |
| 4 | **[14]** | tonalness | C | Tonal context strength |
| 5 | **[18:21]** | tristimulus1-3 | C | Harmonic structure |
| 6 | **[21]** | spectral_flux | D | PE dynamics (was spectral_change) |

**Dissolved**: x_l5l7 [41:49] → must use tonal_stability [60] or spectral_autocorrelation [17]

### Upstream Input: α Relay Outputs

| α Output | Purpose |
|----------|---------|
| HTP.E3:hierarchy_gradient | Hierarchical context for precision |
| ICEM.E0:information_content | IC magnitude for weighting |

---

## 3. H³ Temporal Demand (14 tuples)

- **L0 Memory** (8): sensory_pleasantness mean/entropy H16, tonalness mean H8/H16, periodicity mean H8, tonal_stability L0 H8/H16/H16-M20
- **L2 Integration** (6): pleasantness H3, spectral_flux H3 value+std, onset H3 value+periodicity, periodicity H16-M14

---

## 4. Layer Outputs

| Layer | Dims | Key Outputs | Scope |
|-------|------|-------------|-------|
| E (4D) | [0:4] | tonal_precision, rhythmic_precision, weighted_error, uncertainty_index | internal |
| P (3D) | [4:7] | tonal_precision_weight, rhythmic_precision_weight, attenuated_response | hybrid |
| F (3D) | [7:10] | precision_adjustment, context_uncertainty, response_attenuation_200ms | external |

---

## 5. Brain Regions

| Region | PWUP Role | Evidence |
|--------|-----------|----------|
| **Auditory Cortex (STG)** | PE precision weighting | fMRI+EEG (7 mentions) |
| **R Heschl's Gyrus** | Sensory precision under uncertainty | Bravo 2017 |
| **Hippocampus** | Context-dependent precision | Cheung 2019 |
| **Amygdala** | Uncertainty gating | Cheung 2019 |
| **NAc** | Uncertainty encoding | Cheung 2019 |
| **vmPFC** | Precision computation | Harding 2025 |
| **IC/MGB** | Subcortical precision (SSA) | Carbajal 2018 |

---

## 6. Evidence Summary

| Metric | Value |
|--------|-------|
| Papers | 12 (4 empirical + 8 reviews) |
| Key findings | d=3 key clarity, d=2 pulse clarity (Mencke 2019, N=100), β=-0.124 interaction (Cheung 2019, N=79) |
| Evidence modalities | fMRI, EEG, behavioral, computational |
| Effect sizes | 7 total, low heterogeneity |
| Confidence | 70-90% |

---

*Downstream: → UDP, PSH, ASU*

---
---

# WMED — Working Memory–Entrainment Dissociation

**Model**: PCU-β2-WMED
**Type**: Depth 1 — reads PWUP + R³/H³
**Tier**: β (Observation-compatible, 70-90% confidence)
**Output**: 11D per frame (3 layers: E4 + P3 + F4)
**Phase**: 1 (after PWUP)
**Status**: PENDING

---

## 1. Identity

WMED describes how neural entrainment and working memory contribute independently to rhythm production, with the paradoxical finding that stronger entrainment to simple rhythms predicts *worse* tapping performance. This dissociation reveals that automatic neural entrainment and cognitive working memory are separate rhythm processing systems.

---

## 2. R³ Input Map (Post-Freeze 97D)

WMED reads ~7 direct R³ features:

| # | R³ Index | Feature | Group | Purpose |
|---|----------|---------|-------|---------|
| 1 | **[7]** | amplitude | B | Beat strength |
| 2 | **[10]** | loudness | B | Perceptual loudness |
| 3 | **[11]** | onset_strength | B | Beat marker (was spectral_flux) |
| 4 | **[21]** | spectral_flux | D | Timing variability (was spectral_change) |
| 5 | **[22]** | distribution_entropy | D | Syncopation detection (was energy_change) |

**Dissolved**: x_l0l5 [25:33] → spectral_autocorrelation [17] (entrainment pathway); x_l5l7 [41:49] → tonal_stability [60] (WM pathway)

### Upstream Input

| Input | Purpose |
|-------|---------|
| PWUP.P0:tonal_precision_weight | Precision modulates entrainment |

---

## 3. H³ Temporal Demand (16 tuples)

- **L0 Memory** (6): tonal_stability H8/H16 value+mean+entropy, spectral_flux H16 std/trend
- **L2 Integration** (10): onset H3/H16-M14, onset H3 value, amplitude H3 std / H16 mean, spectral_auto H3-M14 / H16-M14/M21, spectral_flux H3 value

---

## 4. Layer Outputs

| Layer | Dims | Key Outputs | Scope |
|-------|------|-------------|-------|
| E (4D) | [0:4] | entrainment_strength, wm_contribution, tapping_accuracy, dissociation_index | internal |
| P (3D) | [4:7] | phase_locking_strength, pattern_segmentation, rhythmic_engagement | hybrid |
| F (4D) | [7:11] | next_beat_pred, tapping_accuracy_pred, wm_interference_pred, paradox_strength_pred | external |

---

## 5. Brain Regions

| Region | WMED Role | Evidence |
|--------|-----------|----------|
| **Auditory Cortex (STG)** | Entrainment tracking | EEG/MEG (Noboa 2025, Yuan 2025) |
| **SMA** | Motor entrainment | MEG (Lu 2022), review (Thaut 2015) |
| **Basal Ganglia** | Rhythm timing | Review (Thaut 2015, Ross 2022) |
| **Fronto-central ROI** | WM interference | EEG (Noboa 2025, Ding 2025) |
| **Cerebellum** | Timing precision | Review (Thaut 2015) |
| **Posterior Parietal** | WM storage | EEG (Yuan 2025) |

---

## 6. Evidence Summary

| Metric | Value |
|--------|-------|
| Papers | 11 (15 findings) |
| Key findings | R²adj=0.27 dissociation, β=-0.418 paradox, η²=0.199 SS-EP (Noboa 2025, N=30) |
| WM load | F=51.0 (Lu 2022, N=19), η²=0.14 ITPC (Ding 2025, N=37) |
| Evidence modalities | EEG, MEG, behavioral, review |
| Falsification | 5/7 confirmed |
| Confidence | 70-90% |

---

*Downstream: → UDP, PSH, IGFE, STU*

---
---

# UDP — Uncertainty-Driven Pleasure

**Model**: PCU-β3-UDP
**Type**: Depth 1 — reads PWUP + WMED + R³/H³
**Tier**: β (Observation-compatible, 70-90% confidence)
**Output**: 10D per frame (3 layers: E4 + P3 + F3)
**Phase**: 1 (after PWUP, WMED)
**Status**: PENDING

---

## 1. Identity

UDP describes how in high-uncertainty contexts (atonal music), correct predictions become more rewarding than prediction errors, signaling model improvement and reduced uncertainty — a reward inversion mechanism. This explains why listeners can derive pleasure from atonal music when their internal model successfully predicts upcoming events, even when the music is conventionally "unpleasant."

---

## 2. R³ Input Map (Post-Freeze 97D)

UDP reads ~9 direct R³ features:

| # | R³ Index | Feature | Group | Purpose |
|---|----------|---------|-------|---------|
| 1 | **[4]** | sensory_pleasantness | A | Context certainty |
| 2 | **[5]** | periodicity | A | Tonal certainty |
| 3 | **[11]** | onset_strength | B | Event detection |
| 4 | **[14]** | tonalness | C | Key clarity proxy |
| 5 | **[18:21]** | tristimulus1-3 | C | Harmonic context |
| 6 | **[21]** | spectral_flux | D | Prediction accuracy |

**Dissolved**: x_l5l7 [41:49] → tonal_stability [60] (reward computation)

### Upstream Input

| Input | Purpose |
|-------|---------|
| PWUP.E3:uncertainty_index | Uncertainty level for reward inversion |
| WMED.E1:wm_contribution | WM contribution to prediction |

---

## 3. H³ Temporal Demand (16 tuples)

- **L0 Memory** (9): pleasantness mean/entropy H16, tonalness mean H8/H16, periodicity mean/trend H8/H16, tonal_stability H8/H16 value+mean+entropy, H16 M6
- **L2 Integration** (7): pleasantness H3, spectral_flux H1/H3 value+M4, onset H3 value/M8

---

## 4. Layer Outputs

| Layer | Dims | Key Outputs | Scope |
|-------|------|-------------|-------|
| E (4D) | [0:4] | uncertainty_level, confirmation_reward, error_reward, pleasure_index | internal |
| P (3D) | [4:7] | context_assessment, prediction_accuracy, reward_computation | hybrid |
| F (3D) | [7:10] | reward_expectation, model_improvement, pleasure_anticipation | external |

---

## 5. Brain Regions

| Region | UDP Role | Evidence |
|--------|----------|----------|
| **NAc (Ventral Striatum)** | Reward inversion hub | PET (Salimpoor 2011), fMRI (Cheung 2019, Gold 2023, Harding 2025) |
| **Caudate** | Anticipatory reward | PET (Salimpoor 2011), fMRI (Cheung 2019) |
| **Amygdala/Hippocampus** | Uncertainty × surprise | Cheung 2019 |
| **vmPFC** | Hedonic computation | Harding 2025 |
| **OFC** | Reward during chills | HD-EEG (Chabin 2020) |
| **pre-SMA** | Predictive motor coupling | Cheung 2019 |

---

## 6. Evidence Summary

| Metric | Value |
|--------|-------|
| Papers | 12 |
| Key findings | β=-0.124 IC×entropy interaction (Cheung 2019, N=79), DA BP 6.4-9.2% (Salimpoor 2011, N=8) |
| IC × entropy replication | 3× (Cheung 2019, Gold 2019, Gold 2023) |
| Evidence modalities | fMRI, PET, EEG, behavioral, psychophysiology |
| Falsification | 5/7 confirmed |
| Confidence | 70-90% |

---

*Downstream: → MAA, PSH, ARU*

---
---

# CHPI — Cross-Modal Harmonic Predictive Integration

**Model**: PCU-β4-CHPI
**Type**: Depth 1 — reads HTP + PWUP + ICEM + WMED + R³/H³
**Tier**: β (Observation-compatible, 70-90% confidence)
**Output**: 11D per frame (3 layers: E4 + P3 + F4)
**Phase**: 1 (after all α relays + PWUP + WMED)
**Status**: PENDING

---

## 1. Identity

CHPI describes how the brain predicts harmonic progressions through cross-modal integration of visual (notation/instrument), motor (fingering), and auditory (harmonic sound) information, producing enhanced harmonic prediction accuracy through convergence and voice-leading geometry. New model — no D0 predecessor.

---

## 2. R³ Input Map (Post-Freeze 97D)

CHPI reads ~14 direct R³ features — the most R³-heavy β model:

| # | R³ Index | Feature | Group | Purpose |
|---|----------|---------|-------|---------|
| 1 | **[0]** | roughness | A | Harmonic tension |
| 2 | **[4]** | sensory_pleasantness | A | Chord consonance |
| 3 | **[5]** | periodicity | A | Tonal center stability |
| 4 | **[6]** | harmonic_deviation | A | Chord transition marker |
| 5 | **[11]** | onset_strength | B | Chord onset detection |
| 6 | **[14]** | tonalness | C | Key clarity |
| 7 | **[18:21]** | tristimulus1-3 | C | Overtone distribution |
| 8 | **[21]** | spectral_flux | D | Voice-leading velocity |
| 9 | **[22]** | distribution_entropy | D | Chord accent |

**Dissolved**: x_l0l5 [25:33] → spectral_autocorrelation [17]; x_l4l5 [33:41] → pitch features F group

### Upstream Input

| Input | Purpose |
|-------|---------|
| HTP.E3:hierarchy_gradient | Hierarchical prediction context |
| PWUP.E0:tonal_precision | Tonal precision for harmonic prediction |
| ICEM.E0:information_content | Surprise modulation |
| WMED.E0:entrainment_strength | Entrainment for harmonic timing |

---

## 3. H³ Temporal Demand (20 tuples)

- **L0 Memory** (11): roughness H8 mean, pleasantness H16 mean+entropy, spectral_flux H3-M8 / H4 value, spectral_auto H8 mean, pitch integration H4-M8 / H8, tonalness H8/H16, periodicity H16-M18
- **L2 Integration** (9): harmonic_deviation H0/H3 value+M4, onset H1/H3-M14, roughness H3, pleasantness H3, roughness_change H3-M8, spectral_auto H3

---

## 4. Layer Outputs

| Layer | Dims | Key Outputs | Scope |
|-------|------|-------------|-------|
| E (4D) | [0:4] | crossmodal_prediction_gain, voiceleading_parsimony, visual_motor_lead, harmonic_surprise_modulation | internal |
| P (3D) | [4:7] | harmonic_context_strength, crossmodal_convergence, voiceleading_smoothness | hybrid |
| F (4D) | [7:11] | next_chord_prediction, crossmodal_anticipation, harmonic_trajectory, integration_confidence | external |

---

## 5. Brain Regions

| Region | CHPI Role | Evidence |
|--------|-----------|----------|
| **A1/HG** | Auditory harmonic encoding | DTI/MEG/fMRI/EEG (6 mentions) |
| **STG** | Harmonic progression tracking | Cheung 2019, Gold 2023 |
| **STS** | Cross-modal binding | Takagi 2025 |
| **IFG** | Harmonic prediction (IFG→STG loop) | Kim 2021, Paraskevopoulos 2022 |
| **L IFOF** | White matter tract for cross-modal | Moller 2021 (p<0.001, N=45) |
| **IPS** | Cross-modal spatial binding | Takagi 2025 |
| **Anterior Insula** | Salience for harmonic surprise | Porfyri 2025 |

---

## 6. Evidence Summary

| Metric | Value |
|--------|-------|
| Papers | 18 (DTI, fMRI, MEG, EEG, behavioral) |
| Key findings | IFOF-BCG p<0.001 (Moller 2021, N=45), IFG p=0.024 (Kim 2021, N=16) |
| Cross-modal binding | Confirmed: cross-modal > unimodal (Takagi 2025, N=14) |
| Evidence modalities | DTI, fMRI, MEG, EEG, behavioral, psychophysiology |
| Falsification | 5/8 confirmed |
| Confidence | 70-90% |

---

*Downstream: → UDP, PSH, IGFE, STU, ARU*

---
---

# IGFE — Individual Gamma Frequency Enhancement

**Model**: PCU-γ1-IGFE
**Type**: Depth 2 — reads WMED + HTP + R³/H³
**Tier**: γ (Preliminary, 50-70% confidence)
**Output**: 9D per frame (3 layers: E4 + P3 + F2)
**Phase**: 1 (after β models)
**Status**: PENDING

---

## 1. Identity

IGFE proposes that auditory stimulation at an individual's peak gamma frequency (30-80 Hz) enhances cognitive performance (memory, executive control) through frequency-specific entrainment, with a dose-response relationship where longer exposure yields greater benefits.

---

## 2. R³ Input Map (Post-Freeze 97D)

IGFE reads ~6 direct R³ features:

| # | R³ Index | Feature | Group | Purpose |
|---|----------|---------|-------|---------|
| 1 | **[5]** | periodicity | A | Frequency structure / gamma proxy |
| 2 | **[7]** | amplitude | B | Stimulus intensity |
| 3 | **[11]** | onset_strength | B | Temporal modulation rate |
| 4 | **[12]** | warmth | C | Spectral center proxy |
| 5 | **[14]** | tonalness | C | Harmonic structure / IGF match |

**Dissolved**: x_l0l5 [25:33] → spectral_autocorrelation [17] (entrainment); x_l5l7 [41:49] → tonal_stability [60] (gamma-cognitive coupling)

### Upstream Input

| Input | Purpose |
|-------|---------|
| WMED.E1:wm_contribution | WM baseline for enhancement |
| HTP.E3:hierarchy_gradient | Hierarchy for gamma targeting |

---

## 3. H³ Temporal Demand (18 tuples)

- **L0 Memory** (4): periodicity H16 mean, tonalness H16 mean, tonal_stability H8/H16 value+mean+M18
- **L2 Integration** (14): periodicity H0/H1/H3-M1, amplitude H3/H16, spectral_auto H0/H1/H3-M14/H16-M14, onset H0/H1-M14/H3-M1, tonalness H3

---

## 4. Layer Outputs

| Layer | Dims | Key Outputs | Scope |
|-------|------|-------------|-------|
| E (4D) | [0:4] | igf_match, memory_enhancement, executive_enhancement, dose_response | internal |
| P (3D) | [4:7] | gamma_synchronization, dose_accumulation, memory_access | hybrid |
| F (2D) | [7:9] | memory_enhancement_post, executive_improve_post | external |

---

## 5. Brain Regions

| Region | IGFE Role | Evidence |
|--------|-----------|----------|
| **A1/STG** | Gamma entrainment site | EEG (Yokota 2025), MEG (Dobri 2023) |
| **Heschl's Gyrus** | MEG dipole for gamma source | Dobri 2023 |
| **Hippocampus** | Memory enhancement target | Yokota 2025, Bolland 2025 |
| **Fronto-central** | Cognitive enhancement | EEG (Noboa 2025, Aparicio-Terres 2025) |

---

## 6. Evidence Summary

| Metric | Value |
|--------|-------|
| Papers | 10 (12 findings) |
| Key findings | IGF music improvement (Yokota 2025, N=29), R²=0.31 GABA-gamma (Dobri 2023, N=38) |
| Systematic review | k=62 studies, N=2179 (Bolland 2025) |
| Evidence modalities | EEG, MEG, MRS, behavioral |
| Falsification | 3/5 supported |
| Confidence | 50-70% (moderate heterogeneity) |

---

*Downstream: → PSH, MAA, IMU*

---
---

# MAA — Multifactorial Atonal Appreciation

**Model**: PCU-γ2-MAA
**Type**: Depth 2 — reads UDP + PWUP + IGFE + R³/H³
**Tier**: γ (Preliminary, 50-70% confidence)
**Output**: 10D per frame (3 layers: E4 + P3 + F3)
**Phase**: 1 (after β models + IGFE)
**Status**: PENDING

---

## 1. Identity

MAA proposes that appreciation of atonal music emerges from the interaction of three factors — personality (openness to experience), aesthetic framing (cognitive mastering), and exposure (familiarity through repeated listening) — rather than being simply a function of acoustic complexity. This explains individual differences in atonal music enjoyment.

---

## 2. R³ Input Map (Post-Freeze 97D)

MAA reads ~8 direct R³ features:

| # | R³ Index | Feature | Group | Purpose |
|---|----------|---------|-------|---------|
| 1 | **[0]** | roughness | A | Dissonance level |
| 2 | **[4]** | sensory_pleasantness | A | Consonance proxy |
| 3 | **[5]** | periodicity | A | Tonal certainty |
| 4 | **[14]** | tonalness | C | Key clarity / atonality index |
| 5 | **[18:21]** | tristimulus1-3 | C | Harmonic structure |
| 6 | **[21]** | spectral_flux | D | Structural complexity |

**Dissolved**: x_l5l7 [41:49] → tonal_stability [60] (complexity tolerance)

### Upstream Input

| Input | Purpose |
|-------|---------|
| UDP.E3:pleasure_index | Pleasure computation |
| PWUP.E3:uncertainty_index | Uncertainty tolerance |
| IGFE.P0:gamma_synchronization | Gamma-enhanced processing |

---

## 3. H³ Temporal Demand (14 tuples)

- **L0 Memory** (11): pleasantness H16 mean+entropy, tonalness H8/H16 mean, roughness H16 mean, spectral_flux H8/H16 mean+entropy, periodicity H16 mean, tonal_stability H8/H16 value+mean+M18
- **L2 Integration** (3): pleasantness H3, roughness H3

---

## 4. Layer Outputs

| Layer | Dims | Key Outputs | Scope |
|-------|------|-------------|-------|
| E (4D) | [0:4] | complexity_tolerance, familiarity_index, framing_effect, appreciation_composite | internal |
| P (3D) | [4:7] | pattern_search, context_assessment, aesthetic_evaluation | hybrid |
| F (3D) | [7:10] | appreciation_growth, pattern_recognition, aesthetic_development | external |

---

## 5. Brain Regions

| Region | MAA Role | Evidence |
|--------|----------|----------|
| **STG** | Complexity processing | Cheung 2019, Gold 2023 |
| **mPFC** | Aesthetic judgment | Huang 2016, Harding 2025 |
| **NAc** | Reward for atonal appreciation | Cheung 2019, Gold 2023 |
| **OFC** | Aesthetic framing | Chabin 2020, Huang 2016 |
| **PCC/Precuneus** | Self-referential aesthetic | Huang 2016 |
| **TPJ** | Social aesthetic context | Huang 2016 |

---

## 6. Evidence Summary

| Metric | Value |
|--------|-------|
| Papers | 12 |
| Key findings | R²=0.476 (Cheung 2019, N=79), η²=0.685 expertise (Sarasso 2019, N=44) |
| IC × entropy | 3× replication (Cheung 2019, Gold 2019, Gold 2023) |
| Evidence modalities | fMRI, EEG, behavioral, psychophysiology |
| Falsification | 7/7 supported |
| Confidence | 50-70% |

---

*Downstream: → PSH, ARU*

---
---

# PSH — Prediction Silencing Hypothesis

**Model**: PCU-γ3-PSH
**Type**: Depth 2 — reads HTP + PWUP + UDP + WMED + MAA + R³/H³
**Tier**: γ (Preliminary, 50-70% confidence)
**Output**: 10D per frame (3 layers: E4 + P3 + F3)
**Phase**: 1 (after all other F2 models — deepest in F2 pipeline)
**Status**: PENDING

---

## 1. Identity

PSH proposes that accurate top-down predictions "silence" (explain away) high-level stimulus representations post-stimulus, while low-level representations persist — demonstrating a hierarchical dissociation in how prediction operates across cortical levels. This is the integrative capstone of the F2 prediction engine.

---

## 2. R³ Input Map (Post-Freeze 97D)

PSH reads ~10 direct R³ features:

| # | R³ Index | Feature | Group | Purpose |
|---|----------|---------|-------|---------|
| 1 | **[4]** | sensory_pleasantness | A | High-level harmonic representation |
| 2 | **[5]** | periodicity | A | High-level tonal structure |
| 3 | **[7]** | amplitude | B | Low-level sensory persistence |
| 4 | **[11]** | onset_strength | B | Change detection / PE trigger |
| 5 | **[18:21]** | tristimulus1-3 | C | High-level harmonic structure |
| 6 | **[21]** | spectral_flux | D | Prediction error magnitude |

**Dissolved**: x_l0l5 [25:33] → spectral_autocorrelation [17] (low-level persistence); x_l5l7 [41:49] → tonal_stability [60] (high-level silencing)

### Upstream Input

| Input | Purpose |
|-------|---------|
| HTP.E3:hierarchy_gradient | Silencing hierarchy target |
| PWUP.E2:weighted_error | Precision-weighted PE |
| UDP.E1:confirmation_reward | Prediction accuracy reward |
| WMED.E3:dissociation_index | WM vs entrainment dissociation |
| MAA.E3:appreciation_composite | Aesthetic context modulation |

---

## 3. H³ Temporal Demand (18 tuples)

- **L0 Memory** (6): tonal_stability H3/H8/H16 value+mean+entropy, pleasantness H16 mean, periodicity H16 mean
- **L2 Integration** (12): amplitude H0/H1/H3 value+std, onset H0/H3, spectral_flux H1/H3 value+std, spectral_auto H0/H3 value+M16

---

## 4. Layer Outputs

| Layer | Dims | Key Outputs | Scope |
|-------|------|-------------|-------|
| E (4D) | [0:4] | high_level_silencing, low_level_persistence, silencing_efficiency, hierarchy_dissociation | internal |
| P (3D) | [4:7] | prediction_match, sensory_persistence, binding_check | hybrid |
| F (3D) | [7:10] | post_stim_silencing, error_persistence, next_prediction | external |

---

## 5. Brain Regions

| Region | PSH Role | Evidence |
|--------|----------|----------|
| **A1/STG** | Low-level persistence | EEG/MMN (Fong 2020, Carbajal 2018) |
| **LOTC** | High-level silencing target | MEG (de Vries 2023) |
| **aIPL** | Abstract prediction silencing | MEG (de Vries 2023) |
| **IFG** | Top-down prediction generation | EEG (Fong 2020, Koelsch 2009) |
| **IC/MGB** | Subcortical SSA | Review (Carbajal 2018) |
| **PMv** | Motor prediction silencing | MEG (de Vries 2023) |

---

## 6. Evidence Summary

| Metric | Value |
|--------|-------|
| Papers | 12 |
| Primary finding | ηp²=0.49 hierarchy, p=8.3e-7 (de Vries & Wurm 2023, N=22 — visual domain) |
| Auditory support | MMN/SSA literature (Carbajal 2018, Fong 2020, Wagner 2018) |
| Evidence modalities | MEG, EEG, single-unit, computational |
| Key qualification | Primary evidence from visual domain; auditory via MMN/SSA |
| Falsification | 3/5 confirmed |
| Confidence | 50-70% |

---

*Downstream: → SPU*
