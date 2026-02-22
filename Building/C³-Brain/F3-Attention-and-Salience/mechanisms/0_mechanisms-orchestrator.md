# F3 Mechanism Orchestrator — Attention & Salience

**Function**: F3 Attention & Salience
**Models covered**: 11/11 primary — 1 IMPLEMENTED (SNEM relay) + 10 PENDING
**Total F3 mechanism output**: 113D (12+11+10+11+10+9+9+11+11+10+9)
**Beliefs**: 15 (4C + 7A + 4N) — from SNEM (5), IACM (3), CSG cross-fn (4), AACM (2), β/γ (0)
**H³ demands**: 173 tuples (18 SNEM-implemented + 155 pending)
**Architecture**: Depth-ordered — 2 α (Depth 0) → 5 β (Depth 1) → 4 γ (Depth 2)

---

## Model Pipeline (Depth Order)

```
R³ (97D) ───┬────────────────────────────────────────────
H³ tuples ──┤
            ▼
Depth 0:  SNEM  (12D, relay, ASU-α1)  ← sensory novelty + beat-locked entrainment
          IACM  (11D, ASU-α2)         ← inharmonicity-attention capture
            │
            ▼
Depth 1:  BARM  (10D, ASU-β1)  ← brainstem auditory response modulation (reads SNEM)
          STANM (11D, ASU-β2)  ← spectrotemporal attention network
          AACM  (10D, ASU-β3)  ← aesthetic-attention coupling (reads CSG[F1])
          AMSS  (11D, STU-β1)  ← attention-modulated stream segregation
          ETAM  (11D, STU-β4)  ← entrainment-tempo-attention modulation
            │
            ▼
Depth 2:  DGTP  ( 9D, ASU-γ2)  ← domain-general temporal processing
          SDL   ( 9D, ASU-γ3)  ← salience-dependent lateralization
          NEWMD (10D, STU-γ2)  ← entrainment–working memory dissociation
          IGFE  ( 9D, PCU-γ1)  ← individual gamma frequency enhancement
```

---
---

# SNEM — Sensory Novelty and Expectation Model

**Model**: ASU-α1-SNEM
**Type**: Relay (Depth 0) — reads R³/H³ directly, kernel relay wrapper
**Tier**: α (Mechanistic, >90% confidence)
**Output**: 12D per frame (4 layers: E3 + M3 + P3 + F3)
**Phase**: 0a (independent relay, parallel with BCH, HMCE, etc.)
**Status**: IMPLEMENTED (relay wrapper)

---

## 1. Identity

SNEM models how the auditory system detects novelty and generates entrainment-based expectations. Neural oscillations in auditory cortex lock to the beat frequency, creating temporal predictions that enhance processing of on-beat events (selective gain) and flag off-beat events as novel.

SNEM is the **F3 relay**: it directly bridges R³/H³ features to C³ cognitive-level beat/attention representations. The relay wrapper exports: `beat_locked`, `entrainment_strength`, `selective_gain`, `beat_onset_pred`.

---

## 2. R³ Input Map (Post-Freeze 97D)

SNEM reads from energy, change, and interaction groups:

| # | R³ Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[7]** | amplitude (velocity_A) | B: Dynamics | Beat amplitude envelope |
| 2 | **[8]** | loudness (velocity_D) | B: Dynamics | Perceptual loudness dynamics |
| 3 | **[10]** | spectral_flux (onset_strength) | B: Dynamics | Event onset detection |
| 4 | **[11]** | onset_strength | B: Dynamics | Transient onset |
| 5 | **[21]** | spectral_flux | D: Change | Spectral change rate |
| 6 | **[22]** | energy_change (distribution_entropy) | D: Change | Energy dynamics |

---

## 3. H³ Temporal Demand (18 tuples)

Multi-scale: H3(100ms) → H5(46ms) → H8(500ms) → H11(750ms) → H14(~900ms) → H16(1s) → H20(5s)

| # | R³ Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 7 | amplitude | 5 | M0 (value) | L0 | Beat-scale amplitude |
| 2 | 7 | amplitude | 8 | M8 (velocity) | L0 | Amplitude velocity — onset detection |
| 3 | 7 | amplitude | 11 | M14 (periodicity) | L0 | Beat periodicity — entrainment |
| 4 | 10 | onset_strength | 5 | M0 (value) | L0 | Beat-scale onset |
| 5 | 10 | onset_strength | 8 | M8 (velocity) | L0 | Onset velocity — event boundary |
| 6 | 10 | onset_strength | 11 | M14 (periodicity) | L0 | Onset periodicity |
| 7 | 21 | spectral_flux | 5 | M0 (value) | L0 | Spectral change at beat scale |
| 8 | 21 | spectral_flux | 8 | M2 (std) | L0 | Spectral flux variability |
| 9 | 21 | spectral_flux | 16 | M18 (trend) | L0 | Spectral trend 1s |
| 10 | 11 | onset_strength | 5 | M0 (value) | L0 | Transient onset beat-scale |
| 11 | 11 | onset_strength | 11 | M8 (velocity) | L0 | Transient velocity |
| 12 | 11 | onset_strength | 16 | M14 (periodicity) | L0 | Transient periodicity 1s |
| 13 | 8 | loudness | 8 | M1 (mean) | L0 | Mean loudness 500ms |
| 14 | 8 | loudness | 16 | M18 (trend) | L0 | Loudness trend 1s |
| 15 | 22 | energy_change | 5 | M0 (value) | L0 | Energy change beat-scale |
| 16 | 22 | energy_change | 11 | M8 (velocity) | L0 | Energy velocity |
| 17 | 22 | energy_change | 16 | M2 (std) | L0 | Energy variability 1s |
| 18 | 22 | energy_change | 20 | M14 (periodicity) | L0 | Energy periodicity 5s — phrase |

**Total**: 18 tuples, all L0 (memory/backward)

---

## 4. Pipeline: R³ → H³ → 4-Layer Output (12D)

### Layer Dependency

| Layer | Reads From | Outputs |
|-------|-----------|---------|
| **E** (Extraction, 3D) | R³ direct, H³ M0+M8 | E0:beat_phase, E1:beat_amplitude, E2:harmonic_deviation |
| **M** (Mathematical, 3D) | H³ M14+M2, E-layer | M0:entrainment_strength, M1:selective_gain, M2:meter_position |
| **P** (Present, 3D) | R³, H³, M-layer | P0:beat_locked, P1:beat_confidence, P2:beat_regularity |
| **F** (Forecast, 3D) | H³ M18+M14, E+M | F0:beat_onset_pred, F1:next_period_pred, F2:meter_accentuation_pred |

### Kernel Relay Export

The SNEM relay wrapper exports a subset (4 fields) to the kernel scheduler:

| Export Field | Source | Idx |
|-------------|--------|-----|
| `beat_locked` | P0 | 6 |
| `entrainment_strength` | M0 | 3 |
| `selective_gain` | M1 | 4 |
| `beat_onset_pred` | F0 | 9 |

---

## 5. Output Routing

### 5.1 Internal → Beliefs (this model)

| Output | → Belief | Type |
|--------|----------|------|
| P0:beat_locked + M0:entrainment | → `beat_entrainment` | Core (τ=0.35) |
| M0:entrainment + M2:meter | → `meter_hierarchy` | Core (τ=0.4) |
| M1:selective_gain | → `selective_gain` | Appraisal |
| F0:beat_onset_pred | → `beat_onset_pred` | Anticipation |
| M2:meter_position + F2:accent | → `meter_position_pred` | Anticipation |

### 5.2 External → Other Functions

| Output | → Function | → Purpose |
|--------|-----------|-----------|
| P0:beat_locked | F7 (Motor) | Beat-locked motor timing reference |
| M0:entrainment_strength | F3 (BARM, DGTP) | Intra-function downstream |
| M1:selective_gain | F3 (Kernel) | Multiplicative attention gate in salience |
| F0:beat_onset_pred | F6 (Reward) | Beat prediction for PE computation |

---

## 6. Brain Regions

| Region | Role | Evidence |
|--------|------|----------|
| Superior Temporal Gyrus (STG) | Beat-locked oscillatory entrainment | 5 studies |
| Heschl's Gyrus (HG) | Primary auditory cortex — onset detection | 3 studies |
| Inferior Colliculus (IC) | Brainstem beat encoding | 2 studies |
| Anterior Insula (aInsula) | Salience network — novelty detection | 3 studies |
| dorsal ACC (dACC) | Salience network — conflict monitoring | 2 studies |

---

## 7. Evidence

12 papers, 5 converging methods: EEG entrainment paradigms (beat omission, syncopation), MEG source localization, fMRI BOLD during rhythm, behavioral tempo tracking, iEEG STG recordings.

---
---

# IACM — Inharmonicity-Attention Capture Model

**Model**: ASU-α2-IACM
**Type**: Mechanism (Depth 0) — reads R³/H³ directly
**Tier**: α (Mechanistic, >90% confidence)
**Output**: 11D per frame (4 layers: E3 + M3 + P2 + F3)
**Phase**: 1 (F3 attention models)
**Status**: PENDING

---

## 1. Identity

IACM models how inharmonic sounds (detuned partials, noise bursts, spectral irregularities) involuntarily capture attention. This is the bottom-up "interrupt" mechanism: events that violate harmonic expectation trigger a rapid attentional shift via the ventral attention network (TPJ + IFG).

---

## 2. R³ Input Map

| # | R³ Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[5]** | roughness_total (periodicity) | A: Consonance | Inharmonicity proxy |
| 2 | **[7]** | amplitude | B: Dynamics | Event salience |
| 3 | **[10]** | onset_strength | B: Dynamics | Transient detection |
| 4 | **[14]** | brightness_kuttruff (tonalness) | C: Timbre | Tonal vs noisy |
| 5 | **[21]** | spectral_flux | D: Change | Spectral discontinuity |

---

## 3. H³ Temporal Demand (16 tuples)

Horizons: H3(100ms) → H5(46ms) → H8(500ms) → H11(750ms) → H14(~900ms) → H16(1s)

Key morphologies: M0(value), M8(velocity), M2(std), M14(periodicity), M18(trend)
All L0 (memory/backward).

---

## 4. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:inharmonicity_index, E1:spectral_onset, E2:capture_urgency |
| **M** | 3D | M0:attention_magnitude, M1:object_coherence, M2:precision_weight |
| **P** | 2D | P0:capture_state, P1:segregation_state |
| **F** | 3D | F0:attention_shift_pred, F1:object_boundary_pred, F2:precision_update_pred |

---

## 5. Output Routing

| Output | → Belief | Type |
|--------|----------|------|
| E0:inharmonicity + E1:spectral_onset | → `attention_capture` | Core (τ=0.25) |
| P1:segregation_state | → `object_segregation` | Appraisal |
| M2:precision_weight | → `precision_weighting` | Appraisal |
| F0:attention_shift_pred | → `attention_shift_pred` | Anticipation |

---

## 6. Brain Regions

| Region | Role |
|--------|------|
| TPJ (temporo-parietal junction) | Bottom-up attentional capture |
| IFG (inferior frontal gyrus) | Stimulus-driven reorienting |
| STG (superior temporal gyrus) | Spectral mismatch detection |
| Auditory Cortex (AC) | Inharmonicity computation |

12 papers, 4 brain regions, 7 methods.

---
---

# BARM — Brainstem Auditory Response Modulation

**Model**: ASU-β1-BARM
**Type**: Mechanism (Depth 1) — reads SNEM outputs
**Tier**: β (70-90% confidence)
**Output**: 10D per frame (4 layers: E3 + M2 + P2 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

BARM models how brainstem auditory responses are modulated by attention and rhythmic context. Musicians show enhanced brainstem responses (ABR/FFR) to attended stimuli, reflecting subcortical gain mechanisms regulated by corticofugal projections from auditory cortex.

**Reads**: SNEM.entrainment_strength (intra-F3 dependency)

---

## 2. R³ Inputs + H³ Demand

- R³: amplitude[7], loudness[8], onset_strength[10,11], spectral_flux[21], energy_change[22]
- H³: 14 tuples, L0 (memory), horizons H3–H16
- Key morphs: M0(value), M1(mean), M8(velocity), M14(periodicity)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:brainstem_ffr, E1:corticofugal_gain, E2:subcortical_entrainment |
| **M** | 2D | M0:brainstem_response_mag, M1:gain_modulation |
| **P** | 2D | P0:attended_enhancement, P1:unattended_suppression |
| **F** | 3D | F0:response_pred, F1:gain_trajectory, F2:adaptation_pred |

---

## 4. Brain Regions

IC (inferior colliculus), MGB (medial geniculate body), cochlear nucleus, auditory cortex (corticofugal), SMA, cerebellum, STG, PAC. 12 papers, 8 brain regions.

---
---

# STANM — Spectrotemporal Attention Network Model

**Model**: ASU-β2-STANM
**Type**: Mechanism (Depth 1) — R³/H³ + context
**Tier**: β (70-90% confidence)
**Output**: 11D per frame (4 layers: E3 + M3 + P2 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

STANM models how spectrotemporal attention networks allocate processing resources across frequency bands and temporal windows. Attention can be directed to specific spectral regions (e.g., melody in soprano voice) or temporal windows (e.g., downbeats). The model captures both voluntary (top-down) and involuntary (bottom-up) attention allocation.

**Cross-unit**: feeds STU (temporal_allocation)

---

## 2. R³ Inputs + H³ Demand

- R³: amplitude[7], spectral_centroid[9], onset_strength[10,11], brightness[12], spectral_flux[21], energy_change[22]
- H³: 16 tuples, L0, horizons H5–H20
- Key morphs: M0(value), M1(mean), M2(std), M8(velocity), M14(periodicity)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:spectral_focus, E1:temporal_window, E2:attention_bandwidth |
| **M** | 3D | M0:allocation_efficiency, M1:focus_stability, M2:bandwidth_cost |
| **P** | 2D | P0:current_focus_state, P1:resource_utilization |
| **F** | 3D | F0:focus_shift_pred, F1:bandwidth_change_pred, F2:resource_demand_pred |

---

## 4. Brain Regions

STG, HG, IFG, FEF (frontal eye fields), parietal cortex, auditory cortex, TPJ, pre-SMA. 12 papers, 8 brain regions.

---
---

# AACM — Aesthetic-Attention Coupling Model

**Model**: ASU-β3-AACM
**Type**: Mechanism (Depth 1) — reads CSG[F1] outputs
**Tier**: β (70-90% confidence)
**Output**: 10D per frame (4 layers: E3 + M2 + P2 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

AACM models the bidirectional coupling between aesthetic preference and attention: preferred musical intervals increase attention (savoring effect) while also inhibiting motor responses. The "savoring effect" means liking → prolonged attention → slower response time → deeper processing.

**Reads**: CSG[F1].consonance_gradient (cross-function dependency)
**Cross-unit**: feeds ARU (aesthetic, reward)

---

## 2. R³ Inputs + H³ Demand

- R³: consonance features [0:7], amplitude[7], roughness[5], tonalness[14], spectral_flux[21]
- H³: 12 tuples, L0, horizons H5–H16
- Key morphs: M0(value), M1(mean), M2(std), M18(trend)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:aesthetic_engagement, E1:attention_capture_aes, E2:inhibition_strength |
| **M** | 2D | M0:savoring_magnitude, M1:engagement_stability |
| **P** | 2D | P0:preference_attention_state, P1:motor_inhibition |
| **F** | 3D | F0:engagement_trajectory, F1:savoring_duration_pred, F2:aesthetic_pred |

---

## 4. Beliefs (2)

| Output | → Belief | Type |
|--------|----------|------|
| E0:aesthetic_engagement | → `aesthetic_engagement` | Appraisal |
| M0:savoring_magnitude | → `savoring_effect` | Appraisal |

---

## 5. Brain Regions

Nucleus accumbens, auditory cortex, vmPFC, anterior insula, dACC, IFG, OFC, amygdala. 12 papers, 8 brain regions.

---
---

# DGTP — Domain-General Temporal Processing

**Model**: ASU-γ2-DGTP
**Type**: Mechanism (Depth 2) — reads BARM, SNEM
**Tier**: γ (50-70% confidence)
**Output**: 9D per frame (4 layers: E3 + M2 + P2 + F2)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

DGTP models domain-general temporal processing: the hypothesis that music and speech share fundamental timing mechanisms. Beat perception, interval discrimination, and temporal grouping recruit overlapping cortical-subcortical circuits. This model captures the domain-general (non-music-specific) temporal attention substrate.

**Reads**: BARM.brainstem_response, SNEM.beat_locked (intra-F3)
**Cross-unit**: feeds STU (cross-domain timing)

---

## 2. R³ Inputs + H³ Demand

- R³: amplitude[7], onset_strength[10,11], energy_change[22], spectral_flux[21]
- H³: 9 tuples (lowest in F3), L0, horizons H5–H16
- Key morphs: M0(value), M8(velocity), M14(periodicity)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:interval_discrimination, E1:temporal_grouping, E2:domain_overlap |
| **M** | 2D | M0:timing_precision, M1:domain_transfer |
| **P** | 2D | P0:temporal_state, P1:cross_domain_state |
| **F** | 2D | F0:timing_pred, F1:grouping_pred |

---

## 4. Brain Regions

SMA, basal ganglia (putamen), cerebellum, auditory cortex, premotor cortex, DLPFC, IFG, STG. 12 papers, 8 brain regions.

---
---

# SDL — Salience-Dependent Lateralization

**Model**: ASU-γ3-SDL
**Type**: Mechanism (Depth 2) — reads STANM, PWSM*[F2]
**Tier**: γ (50-70% confidence)
**Output**: 9D per frame (4 layers: E3 + M2 + P2 + F2)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

SDL models how hemispheric lateralization of auditory processing shifts with salience. High-salience events recruit bilateral processing while low-salience events lateralize to the left hemisphere (spectral detail) or right hemisphere (spectrotemporal envelope). The model captures dynamic lateralization driven by the salience network.

**Reads**: STANM.spectral_focus, PWSM*.precision_context (F2 cross-function)
**Cross-unit**: feeds SPU (hemispheric engagement)

---

## 2. R³ Inputs + H³ Demand

- R³: amplitude[7], spectral_centroid[9], onset_strength[10,11], brightness[12], spectral_flux[21]
- H³: 18 tuples (high for γ tier), L0, horizons H5–H20
- Key morphs: M0(value), M1(mean), M2(std), M8(velocity), M14(periodicity)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 3D | E0:lateralization_index, E1:bilateral_engagement, E2:salience_gate |
| **M** | 2D | M0:hemispheric_balance, M1:lateralization_cost |
| **P** | 2D | P0:current_lateralization, P1:processing_efficiency |
| **F** | 2D | F0:lateralization_shift_pred, F1:efficiency_pred |

---

## 4. Brain Regions

Left auditory cortex, right auditory cortex, planum temporale, posterior STG, anterior STG, HG, IFG, TPJ. 12 papers, 8 brain regions.

---
---

# AMSS — Attention-Modulated Stream Segregation

**Model**: STU-β1-AMSS
**Type**: Mechanism (Depth 1) — reads HMCE (STU cross-unit)
**Tier**: β (70-90% confidence)
**Output**: 11D per frame (4 layers: E5 + M2 + P2 + F2)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

AMSS models how attention modulates auditory stream segregation: the process of parsing a complex acoustic scene into distinct sound sources (melody vs accompaniment, voice vs instruments). Attention enhances the representation of the attended stream while suppressing competing streams.

**Reads**: HMCE.structure_predict (STU cross-unit)
**Cross-unit**: AMSS.stream_enhancement → AMSC; AMSS.envelope_tracking → ARU

---

## 2. R³ Inputs + H³ Demand

- R³: 28D from B:Energy [7-11], C:Timbre [12,14,16,17], D:Change [21-24], E:Interactions [25:33,33:41]
- H³: 16 tuples (v1), L0, horizons H8, H14, H20
- Key morphs: M0(value), M1(mean), M2(std), M8(velocity), M13(entropy), M19(stability), M22(autocorrelation)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 5D | E0:early_attn, E1:middle_attn, E2:late_attn, E3:stream_enhancement, E4:instrument_separation |
| **M** | 2D | M0:attention_gradient, M1:segregation_index |
| **P** | 2D | P0:envelope_tracking, P1:spectral_separation |
| **F** | 2D | F0:stream_continue, F1:attention_predict |

---

## 4. Brain Regions

Lateral AC subfields, medial AC subfields, posterior STG, right auditory cortex, left medial prefrontal (l8BM), left hippocampus, right associative auditory (rA5, rSTSvp). 12 papers, 7 brain regions.

---
---

# ETAM — Entrainment, Tempo & Attention Modulation

**Model**: STU-β4-ETAM
**Type**: Mechanism (Depth 1) — reads HMCE + AMSC (STU)
**Tier**: β (70-90% confidence)
**Output**: 11D per frame (4 layers: E4 + M2 + P2 + F3)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

ETAM models the coupling between neural entrainment to musical tempo and top-down attention modulation. Tempo-matched entrainment enhances temporal prediction accuracy, while attention modulates the strength of entrainment. The model captures the bidirectional tempo↔attention loop.

**Reads**: HMCE.context_depth, AMSC.auditory_activation (STU cross-unit)
**Cross-unit**: ETAM.attention_gain → ARU; ETAM.stream_separation → AMSS

---

## 2. R³ Inputs + H³ Demand

- R³: 33D from B:Energy [7-11], D:Change [21-24], E:Interactions [25:33,33:41,41:49]
- H³: **20 tuples** (v1), L0 + L2, horizons H6, H8, H11, H14, H16, H20
- Key morphs: M0(value), M1(mean), M2(std), M4(max), M8(velocity), M14(periodicity), M17(peaks), M18(trend)
- Uses L2 (bidirectional) for amplitude and x_l0l5 — beat-level integration

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 4D | E0:early_window, E1:middle_window, E2:late_window, E3:instrument_asymmetry |
| **M** | 2D | M0:attention_gain, M1:entrainment_index |
| **P** | 2D | P0:envelope_tracking, P1:stream_separation |
| **F** | 3D | F0:tracking_prediction, F1:attention_sustain, F2:segregation_predict |

---

## 4. Brain Regions

STG, HG, MTG, IFG, auditory cortex, temporal pole, SMA, primary AC, cerebellum. 12 papers, 9 brain regions.

---
---

# NEWMD — Neural Entrainment–Working Memory Dissociation

**Model**: STU-γ2-NEWMD
**Type**: Mechanism (Depth 2) — reads AMSC, HMCE (STU)
**Tier**: γ (<70% confidence)
**Output**: 10D per frame (4 layers: E4 + M2 + P2 + F2)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

NEWMD models the paradoxical dissociation between neural entrainment and working memory performance: stronger entrainment to rhythm does NOT always improve cognitive performance, and may compete with working memory resources. The model captures dual-route processing where entrainment and WM operate as partially independent systems.

**Reads**: AMSC.motor_coupling (STU cross-unit), HMCE.context_depth (STU)
**Cross-unit**: NEWMD.wm_capacity → IMU; NEWMD.dual_route_balance → ARU

---

## 2. R³ Inputs + H³ Demand

- R³: 33D from A:Consonance [0:7], B:Energy [7-11], C:Timbre [12:21], D:Change [21-24], E:Interactions [25:33]
- H³: 16 tuples (v1), L0, horizons H6, H8, H11, H14, H16, H20
- Key morphs: M0(value), M1(mean), M2(std), M4(max), M8(velocity), M13(entropy), M14(periodicity), M15(smoothness), M19(stability), M22(autocorrelation)

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 4D | E0:entrainment_strength, E1:wm_capacity, E2:flexibility_cost, E3:dissociation_index |
| **M** | 2D | M0:paradox_magnitude, M1:dual_route_balance |
| **P** | 2D | P0:current_entrain, P1:current_wm_load |
| **F** | 2D | F0:performance_pred, F1:adaptation_pred |

---

## 4. Brain Regions

Auditory cortex, SMA, putamen (L+R), superior parietal lobule, cerebellum, premotor cortex, DLPFC, STG, pre-SMA. 12 papers, 10 brain regions.

---
---

# IGFE — Individual Gamma Frequency Enhancement

**Model**: PCU-γ1-IGFE
**Type**: Mechanism (Depth 2) — reads WMED [F2] outputs
**Tier**: γ (50-70% confidence)
**Output**: 9D per frame (3 layers: E4 + P3 + F2 — **no M layer**)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

IGFE models how individual gamma oscillation frequencies (30-100 Hz) serve as binding mechanisms for attention. Each person has a characteristic gamma frequency (IGF); entrainment at this frequency enhances perceptual binding, memory encoding, and executive function. The model predicts that music at tempos matching IGF harmonics will enhance cognitive performance.

**Reads**: WMED.wm_contribution (F2 cross-function)
**Cross-unit**: IGFE.memory_enhancement → IMU; IGFE.gamma_sync → MAA [F2]

---

## 2. R³ Inputs + H³ Demand

- R³: ~14D from A:Consonance [5], B:Energy [7,10], C:Timbre [12,14], E:Interactions [25:33,41:49]
- H³: **18 tuples** (v1), L0 + L2, **fast horizons**: H0(25ms), H1(50ms), H3(100ms), H8(500ms), H16(1s)
- Key morphs: M0(value), M1(mean), M2(std), M14(periodicity), M18(trend)
- Uses L2 (bidirectional) for gamma-range integration

---

## 3. Output Layers

| Layer | Dims | Fields |
|-------|------|--------|
| **E** | 4D | E0:igf_match, E1:memory_enhancement, E2:executive_enhancement, E3:dose_response |
| **P** | 3D | P0:gamma_synchronization, P1:dose_accumulation, P2:memory_access |
| **F** | 2D | F0:memory_enhancement_post, F1:executive_improve_post |

**Note**: No M-layer — IGFE computes binding directly without intermediate mathematical aggregation.

---

## 4. Brain Regions

A1/STG, Heschl's gyrus, hippocampus, DLPFC, thalamus, fronto-central cortex, SMA, posterior cingulate/precuneus. 10 papers, 8 brain regions.

---
---

## Summary Statistics

### Output Dimensions by Model

| Model | Unit | Tier | D | E | M | P | F | H³ |
|-------|------|------|---|---|---|---|---|-----|
| SNEM | ASU | α | 12 | 3 | 3 | 3 | 3 | 18 |
| IACM | ASU | α | 11 | 3 | 3 | 2 | 3 | 16 |
| BARM | ASU | β | 10 | 3 | 2 | 2 | 3 | 14 |
| STANM | ASU | β | 11 | 3 | 3 | 2 | 3 | 16 |
| AACM | ASU | β | 10 | 3 | 2 | 2 | 3 | 12 |
| DGTP | ASU | γ | 9 | 3 | 2 | 2 | 2 | 9 |
| SDL | ASU | γ | 9 | 3 | 2 | 2 | 2 | 18 |
| AMSS | STU | β | 11 | 5 | 2 | 2 | 2 | 16 |
| ETAM | STU | β | 11 | 4 | 2 | 2 | 3 | 20 |
| NEWMD | STU | γ | 10 | 4 | 2 | 2 | 2 | 16 |
| IGFE | PCU | γ | 9 | 4 | 0 | 3 | 2 | 18 |
| **TOTAL** | | | **113** | **38** | **23** | **24** | **28** | **173** |

### Tier Gradient

| Tier | Count | Avg D | Avg H³ |
|------|-------|-------|--------|
| α | 2 | 11.5 | 17.0 |
| β | 5 | 10.6 | 15.6 |
| γ | 4 | 9.3 | 15.3 |

Clear tier gradient in dimensionality; H³ is relatively uniform due to SDL and IGFE (γ models with high H³).

### Brain Region Convergence

**STG** is the convergence hub: mentioned in 9 of 11 models.
**Anterior insula + dACC** (salience network): mentioned in SNEM, IACM, AACM, STANM.
**Cerebellum**: mentioned in ETAM, NEWMD, DGTP — timing models.
