# F7 Mechanism Orchestrator — Motor and Timing

**Function**: F7 Motor and Timing
**Models covered**: 10/10 primary — 1 IMPLEMENTED (PEOM relay) + 9 PENDING
**Total F7 mechanism output**: 110D (11D x 10 models)
**Beliefs**: 17 (5C + 7A + 5N) — from PEOM (2), MSR (1), GSSM (1), ASAP (2), DDSMI (2), VRMSME (1), SPMC (2), NSCP (2), CTBB (2), STC (2)
**H3 demands**: ~140 tuples (15 PEOM-implemented + ~125 pending)
**Architecture**: Depth-ordered — 3 alpha (Depth 0) -> 4 beta (Depth 1) -> 3 gamma (Depth 2)

---

## Model Pipeline (Depth Order)

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
            |
Depth 0:  PEOM   (11D, relay, MPU-alpha1)  <- period entrainment optimization (SMA/putamen period lock)
          MSR    (11D, MPU-alpha2)          <- musician sensorimotor reorganization (PLV/P2 dual)
          GSSM   (11D, MPU-alpha3)          <- gait-synchronized stimulation (M1/SMA phase lock)
            |
            |
Depth 1:  ASAP   (11D, MPU-beta1)   <- action simulation for auditory prediction (dorsal stream)
          DDSMI  (11D, MPU-beta2)   <- dyadic dance social motor integration (mTRF resource)
          VRMSME (11D, MPU-beta3)   <- VR music stimulation motor enhancement (PM-DLPFC-M1)
          SPMC   (11D, MPU-beta4)   <- SMA-premotor-M1 motor circuit (hierarchical flow)
            |
            |
Depth 2:  NSCP   (11D, MPU-gamma1) <- neural synchrony commercial prediction (ISC-popularity)
          CTBB   (11D, MPU-gamma2) <- cerebellar theta-burst balance (iTBS timing)
          STC    (11D, MPU-gamma3) <- singing training connectivity (insula-sensorimotor)
```

---
---

# PEOM — Period Entrainment Optimization Model

**Model**: MPU-alpha1-PEOM
**Type**: Relay (Depth 0) — reads R3/H3 directly, kernel relay wrapper
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 11D per frame (4 layers: E 3D + M 4D + P 2D + F 2D)
**Phase**: 0a (independent relay, parallel with BCH, HMCE, etc.)
**Status**: IMPLEMENTED (relay wrapper)

---

## 1. Identity

PEOM models the period entrainment optimization mechanism from Thaut et al. (2015, 1998b). The motor system entrains to auditory period via dP/dt = alpha * (T - P(t)), producing velocity optimization and variability reduction. Fixed period provides a continuous time reference (CTR) that reduces jerk and smooths velocity profiles. PEOM is the **F7 relay**: it directly bridges R3/H3 features to C3 cognitive-level motor/timing representations.

The relay wrapper exports: `period_lock_strength`, `kinematic_smoothness`, `next_beat_pred`, `velocity_profile_pred`.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[7]** | amplitude | B: Dynamics | Beat strength proxy for temporal intensity |
| 2 | **[8]** | loudness | B: Dynamics | Perceptual intensity for motor drive |
| 3 | **[10]** | spectral_flux | B: Dynamics | Onset detection for beat marker |
| 4 | **[11]** | onset_strength | B: Dynamics | Beat event detection for period tracking |
| 5 | **[21]** | spectral_change | D: Change | Tempo dynamics for period rate change |
| 6 | **[25:33]** | x_l0l5 | F: Interactions | Motor-auditory coupling for continuous time reference |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f01:period_entrainment, f02:velocity_optimization, f03:variability_reduction | 9 | Period lock from beat/onset periodicity at 1s; velocity from coupling periodicity; variability reduction as f01*f02 interaction. Yamashita 2025: CV d=-1.10. Thaut 2015: CTR optimizes velocity. |
| **M** (Temporal) | 4D | motor_period, velocity, acceleration, cv_reduction | 4 | dP/dt = tau^-1*(T-P(t)) with tau=4.0s; velocity v(t)=dx/dt; acceleration a(t)=d^2x/dt^2; CV reduction normalized. Grahn & Brett 2007: putamen Z=5.67. |
| **P** (Present) | 2D | period_lock_strength, kinematic_smoothness | 2 | Lock from coupling periodicity + zero-crossings at 1s. Smoothness from velocity + coupling stability. Fujioka 2012: beta oscillations in SMA. |
| **F** (Forecast) | 2D | next_beat_pred_T, velocity_profile_pred | 0 | Beat prediction from f01 + beat periodicity; velocity prediction from f02 + coupling periodicity. Repp 2005: period correction. |

**Total**: 11D, 15 H3 tuples (L0 + L2)

---

## 4. Output Routing

### 4.1 Internal -> Beliefs

| Output | -> Belief | Type |
|--------|----------|------|
| period_lock_strength + kinematic_smoothness | -> `period_entrainment` | Core (tau=0.65) |
| next_beat_pred_T + velocity_profile_pred | -> `beat_prediction` | Anticipation |

### 4.2 External -> Other Functions

| Output | -> Function | -> Purpose |
|--------|-----------|-----------|
| period_lock_strength | F3 (Attention) | Salience mixer: motor timing signal |
| kinematic_smoothness | F5 (Emotion) | Motor fluency contribution |
| next_beat_pred_T | Reward computation | Temporal prediction component |
| PEOM relay (MPU) | MSR, GSSM (siblings) | Cross-relay sensorimotor context |

---

## 5. Brain Regions

| Region | Role | Evidence |
|--------|------|----------|
| SMA | Period locking and sequence timing | Grahn & Brett 2007 (Z=5.03) |
| Putamen | Beat period entrainment | Grahn & Brett 2007 (Z=5.67) |
| PMd (Premotor dorsal) | Velocity planning | Thaut 2015 (Z=5.30) |
| Cerebellum | Motor timing error correction | Thaut 2009b |

---

## 6. Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [7,8,10,11,21,25:33] | 6 feature groups | Dynamics, change, interactions |
| H3 | 15 tuples | Multi-scale beat/onset periodicity and coupling dynamics |

---
---

# MSR — Musician Sensorimotor Reorganization

**Model**: MPU-alpha2-MSR
**Type**: Mechanism (Depth 0) — reads R3/H3 directly
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 11D per frame (4 layers: E 3D + M 3D + P 3D + F 2D)
**Phase**: 1 (F7 motor models)
**Status**: PENDING

---

## 1. Identity

MSR models the dual sensorimotor reorganization pattern in musicians: enhanced bottom-up precision (40-60 Hz PLV increase, d=1.13) and increased top-down inhibition (P2 vertex suppression, d=1.16). Net sensorimotor efficiency emerges from the PLV-P2 dissociation. The model captures training-dependent auditory-motor processing changes.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[8]** | loudness | B: Dynamics | Perceptual loudness for P2 amplitude proxy |
| 2 | **[10]** | spectral_flux | B: Dynamics | Onset detection for bottom-up precision |
| 3 | **[25:33]** | x_l0l5 | F: Interactions | Motor-auditory coupling for PLV proxy |
| 4 | **[33:41]** | x_l4l5 | G: Interactions | Sensorimotor coupling for training-enhanced binding |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f04:high_freq_plv, f05:p2_suppression, f06:sensorimotor_efficiency | 11 | PLV from coupling at gamma (25-100ms); P2 from loudness entropy + onset periodicity. Efficiency = PLV - P2 (subtractive). L. Zhang 2015: PLV d=1.13, P2 d=1.16, TFD d=1.28. |
| **M** (Temporal) | 3D | plv_high_freq, p2_amplitude, efficiency_index | 5 | Continuous PLV [0.28,0.44] mapped to [0,1]; P2 from loudness features; efficiency = alpha*PLV - beta*P2 (alpha=1.0, beta=0.5). |
| **P** (Present) | 3D | bottom_up_precision, top_down_modulation, training_level | 3 | Precision from gamma coupling; modulation from P2 + phase resets; training = sigma(0.5*f04 + 0.5*(1-f05)). Alpheis 2025: dlPFC-putamen t=4.46. |
| **F** (Forecast) | 2D | performance_efficiency, processing_automaticity | 3 | Trial-level efficiency from PLV/P2 balance + motor dynamics; session-level automaticity from training level + stability. Blasi 2025: structural neuroplasticity. |

**Total**: 11D, 22 H3 tuples (L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| training_level + bottom_up_precision | -> `sensorimotor_expertise` | Appraisal |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Auditory Cortex | 40-60 Hz PLV enhancement (L. Zhang 2015) |
| ACC | P2 suppression / top-down cortical gating |
| PMC / SMA | Motor-area activation across rhythm types (Grahn & Brett 2007) |
| dlPFC-Putamen | Enhanced FC in musicians (Alpheis 2025: t=4.46) |
| Cerebellum | Structural neuroplasticity (Blasi 2025) |

4+ papers: L. Zhang 2015 (EEG, N=24), Alpheis 2025, Blasi 2025, Grahn & Brett 2007.

---
---

# GSSM — Gait-Synchronized Stimulation Model

**Model**: MPU-alpha3-GSSM
**Type**: Mechanism (Depth 0) — reads R3/H3 directly
**Tier**: alpha (Mechanistic, >90% confidence)
**Output**: 11D per frame (4 layers: E 3D + M 4D + P 2D + F 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

GSSM models gait-synchronized dual-site stimulation (tDCS to SMA + gait-phase-locked tACS to M1). Phase synchronization between stimulation rhythm and gait cycle produces stride variability reduction (CV d=-1.10) and balance improvement (Mini-BESTest d=1.05). The CV-balance correlation (r=0.62) demonstrates the variability-balance coupling.

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[7]** | amplitude | B: Dynamics | Step force signal for stride CV |
| 2 | **[10]** | spectral_flux | B: Dynamics | Step onset detection for gait phase marker |
| 3 | **[11]** | onset_strength | B: Dynamics | Step event strength for phase locking |
| 4 | **[22]** | energy_change | D: Change | Energy dynamics for gait energy fluctuation |
| 5 | **[25:33]** | x_l0l5 | F: Interactions | SMA-M1 coupling for dual-site synchronization proxy |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f07:phase_synchronization, f08:cv_reduction, f09:balance_improvement | 7 | Phase lock = cos(phi_gait - phi_stim) from step/coupling periodicity; CV reduction from f07 + coupling; balance = f07*f08 interaction. Yamashita 2025: eta_p^2=0.309, d=-1.10. |
| **M** (Temporal) | 4D | stride_cv, sma_m1_coupling, balance_score, gait_stability | 3 | CV = (SD/Mean)*100 normalized; SMA-M1 sync from coupling periodicity 1s; balance from f09; stability = sigma(0.5*f07 + 0.5*f08). |
| **P** (Present) | 2D | phase_lock_strength, variability_level | 2 | Phase lock from coupling zero-crossings (negative indicator); variability from energy dynamics at 500ms. Grahn & Brett 2007: putamen Z=5.67. |
| **F** (Forecast) | 2D | cv_pred_30min, balance_pred | 0 | CV persistence from f08 + coupling periodicity; balance from f09 + gait stability. Sansare 2025: effects persist >= 30 min. |

**Total**: 11D, 12 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| phase_lock_strength + gait_stability | -> `gait_entrainment` | Appraisal |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| SMA (Fz) | tDCS target; sequence timing (Z=5.03) |
| M1 (Cz lateral) | tACS target; gait-phase-locked execution |
| Putamen | Beat period entrainment for gait (Z=5.67) |

3+ papers: Yamashita 2025 (tACS, N=15), Sansare 2025, Grahn & Brett 2007.

---
---

# ASAP — Action Simulation for Auditory Prediction

**Model**: MPU-beta1-ASAP
**Type**: Mechanism (Depth 1) — reads PEOM, MSR outputs
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame (4 layers: E 3D + M 3D + P 3D + F 2D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

ASAP models the Action Simulation for Auditory Prediction hypothesis (Patel & Iversen 2014). The motor system predicts beat timing ("when" not "what") via continuous action simulation through the parietal dorsal auditory-motor pathway. Beat perception requires bidirectional motor-auditory coupling: motor-to-auditory (forward model) and auditory-to-motor (inverse model/error correction). cTBS to posterior parietal cortex impairs beat-based but NOT interval timing (double dissociation).

**Reads**: R3/H3 directly + PEOM period entrainment context
**Feeds**: PEOM (beat prediction), downstream STU

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[10]** | spectral_flux | B: Dynamics | Beat onset detection for "when" prediction |
| 2 | **[11]** | onset_strength | B: Dynamics | Beat event strength for temporal anchor |
| 3 | **[21]** | spectral_change | D: Change | Tempo dynamics for rate change |
| 4 | **[25:33]** | x_l0l5 | F: Interactions | Motor-auditory coupling for simulation signal |
| 5 | **[33:41]** | x_l4l5 | G: Interactions | Dorsal stream activity for parietal pathway |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f10:beat_prediction, f11:motor_simulation, f12:dorsal_stream | 6 | Beat prediction from onset/beat periodicity 1s; motor simulation from onset+coupling 100ms; dorsal from dorsal periodicity+velocity + f10*f11 interaction. Patel & Iversen 2014: ASAP hypothesis. Ross et al. 2018: parietal cTBS double dissociation. |
| **M** (Temporal) | 3D | prediction_accuracy, simulation_strength, coupling_index | 3 | Accuracy = f10; strength = f11; coupling = sigma(0.5*f11 + 0.5*f12). Barchet 2024: tapping optimal ~2 Hz (beta=0.31). |
| **P** (Present) | 3D | motor_to_auditory, auditory_to_motor, dorsal_activity | 0 | Forward model (motor prediction to auditory cortex); inverse model (auditory error correction to motor); dorsal = f12. Ross & Balasubramaniam 2022: bidirectional coupling. |
| **F** (Forecast) | 2D | beat_when_pred_0.5s, simulation_pred | 0 | Beat "when" from f10 + periodicity; simulation continuation from f11 + coupling. Large et al. 2023: optimal ~2 Hz. |

**Total**: 11D, 9 H3 tuples (L0)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| motor_to_auditory + auditory_to_motor | -> `action_simulation` | Core (tau=0.4) |
| beat_when_pred_0.5s + simulation_pred | -> `motor_prediction` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Posterior Parietal Cortex | Dorsal pathway hub; cTBS impairs beat timing (Ross 2018) |
| SMA / PMC | Motor simulation generation |
| Putamen | Beat-metric response (Grahn & Brett 2007: F(2,38)=20.67) |
| Auditory Cortex | Receives motor temporal predictions |

4+ papers: Patel & Iversen 2014, Ross et al. 2018 (cTBS), Ross & Balasubramaniam 2022, Barchet 2024.

---
---

# DDSMI — Dyadic Dance Social Motor Integration

**Model**: MPU-beta2-DDSMI
**Type**: Mechanism (Depth 1) — reads PEOM, ASAP outputs
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame (4 layers: E 3D + M 3D + P 2D + F 3D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

DDSMI models the four parallel neural tracking processes during dyadic dance (social coordination, music tracking, self-movement, partner tracking), compressed into three distinct computational signals. Resource competition between auditory and social processing is the key mechanism: visual contact shifts resources from music tracking to social coordination (F(1,57)=7.48, p=.033). Self-movement tracking is autonomous from social context (all ps>.224).

**Reads**: R3/H3 directly + ASAP beat prediction, PEOM period entrainment
**Feeds**: ARU (social reward), VRMSME (multi-modal coordination)

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[8]** | loudness | B: Dynamics | Loudness entropy for resource demand |
| 2 | **[10]** | spectral_flux | B: Dynamics | Music onset detection for auditory tracking |
| 3 | **[25:33]** | x_l0l5 | F: Interactions | Music-motor coupling pathway |
| 4 | **[33:41]** | x_l4l5 | G: Interactions | Social coupling / partner coordination pathway |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f13:social_coordination, f14:music_tracking, f15:visual_modulation | 11 | Social from x_l4l5 periodicity multi-scale; music from x_l0l5 periodicity + onset; visual = f13-f14 resource shift + loudness entropy. Bigand 2025: social mTRF F(1,57)=249.75; music F(1,57)=30.22. |
| **M** (Temporal) | 3D | mTRF_social, mTRF_auditory, mTRF_balance | 0 | Social = f13; auditory = f14; balance = sigma(0.5*f13 + 0.5*(1-f14)). Visual contact x music interaction F(1,57)=50.10. |
| **P** (Present) | 2D | partner_sync, music_entrainment | 0 | Partner sync from social mTRF + fast coupling; music entrainment from auditory mTRF + coupling. Wohltjen 2023: beat entrainment predicts social synchrony (d=1.37). |
| **F** (Forecast) | 3D | coordination_pred, music_pred, social_pred | 0 | Coordination from f13 + social period 1s; music from f14 + music period 1s; social from f13 + f15. Sabharwal 2024: Granger causality predicts leader/follower. |

**Total**: 11D, 11 H3 tuples (L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| partner_sync + music_entrainment | -> `social_motor_sync` | Core (tau=0.45) |
| coordination_pred + social_pred | -> `social_coordination` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Left M1 | Self-produced actions (Kohler 2025: MVPA) |
| Right PMC | Other-produced actions (Kohler 2025) |
| Bilateral STG | Auditory tracking during dance |
| Prefrontal | Social coordination (Bigand 2025: mTRF) |

4+ papers: Bigand 2025 (EEG, N=58), Wohltjen 2023 (d=1.37), Kohler 2025, Sabharwal 2024.

---
---

# VRMSME — VR Music Stimulation Motor Enhancement

**Model**: MPU-beta3-VRMSME
**Type**: Mechanism (Depth 1) — reads PEOM, MSR outputs
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame (4 layers: E 3D + M 3D + P 2D + F 3D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

VRMSME models the unique motor-enhancing effect of VR music stimulation (VRMS) compared to VR action observation (VRAO) and VR motor imagery (VRMI). VRMS produces superior bilateral PM&SMA connectivity (p<.01 FDR) and bilateral M1 activation (p<.05 HBT). The PM-DLPFC-M1 heterogeneous connectivity network is uniquely activated by VRMS with 14 significant ROI pairs.

**Reads**: R3/H3 directly + PEOM period entrainment, MSR training level
**Feeds**: SPMC (motor circuit), DDSMI (bilateral social motor)

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[8]** | loudness | B: Dynamics | Loudness entropy for auditory complexity |
| 2 | **[10]** | spectral_flux | B: Dynamics | Music onset detection for VR audio sync |
| 3 | **[11]** | onset_strength | B: Dynamics | Beat marker strength for motor timing |
| 4 | **[25:33]** | x_l0l5 | F: Interactions | VR-audio-motor coupling pathway |
| 5 | **[33:41]** | x_l4l5 | G: Interactions | Sensorimotor binding for bilateral activation |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f16:music_enhancement, f17:bilateral_activation, f18:network_connectivity | 12 | Enhancement from coupling periodicity multi-scale + music onset; bilateral from sensorimotor binding multi-scale; network = f16*f17 interaction + loudness entropy. Liang 2025: VRMS > VRAO bilateral PM&SMA p<.01 FDR. |
| **M** (Temporal) | 3D | vrms_advantage, bilateral_index, connectivity_strength | 0 | Advantage = f16; bilateral = f17; connectivity = sigma(0.5*f16 + 0.5*f18). 14 ROI pairs with significant heterogeneous FC. |
| **P** (Present) | 2D | motor_drive, sensorimotor_sync | 0 | Motor drive from VRMS advantage + fast onset/coupling; sync from bilateral index + connectivity. Li 2025: high-groove music increases coordination 28.7%. |
| **F** (Forecast) | 3D | enhancement_pred, connectivity_pred, bilateral_pred | 0 | Enhancement from f16 + coupling period 1s; connectivity from f18 + sensorimotor period 1s; bilateral from f17 + binding stability. Blasi 2025: neuroplasticity from music/dance (20 RCTs). |

**Total**: 11D, 12 H3 tuples (L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| motor_drive + sensorimotor_sync | -> `vr_motor_enhancement` | Appraisal |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Bilateral PM & SMA | VRMS > VRAO connectivity (p<.01 FDR) |
| Bilateral M1 | VRMS > VRMI activation (p<.05 HBT) |
| DLPFC | PM-DLPFC-M1 heterogeneous FC network |
| S1 | Bilateral sensorimotor activation |

3+ papers: Liang 2025 (fNIRS, N=20), Li 2025 (groove), Blasi 2025 (meta, N=718).

---
---

# SPMC — SMA-Premotor-M1 Motor Circuit

**Model**: MPU-beta4-SPMC
**Type**: Mechanism (Depth 1) — reads PEOM, ASAP, VRMSME outputs
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame (4 layers: E 3D + M 3D + P 2D + F 3D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

SPMC models the hierarchical SMA-Premotor-M1 motor circuit for musically-cued movement. SMA encodes temporal sequences (longest timescale), PMC performs action selection (medium), and M1 executes motor output (shortest). The circuit flow follows a top-down hierarchy where execution depends on both planning and preparation being active. Cerebellar timing precision provides online error correction.

**Reads**: R3/H3 directly + PEOM period entrainment, ASAP beat prediction, VRMSME motor drive
**Feeds**: Motor execution output, cerebellar timing precision

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[7]** | amplitude | B: Dynamics | Motor output strength for M1 execution |
| 2 | **[10]** | spectral_flux | B: Dynamics | Onset detection for SMA sequence markers |
| 3 | **[11]** | onset_strength | B: Dynamics | Beat event for motor timing signal |
| 4 | **[21]** | spectral_change | D: Change | Tempo rate for SMA tempo encoding |
| 5 | **[25:33]** | x_l0l5 | F: Interactions | Hierarchical circuit coupling (SMA-PMC-M1) |
| 6 | **[33:41]** | x_l4l5 | G: Interactions | Sequence regularity for stability measures |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f19:sequence_planning, f20:motor_preparation, f21:execution_output | 6 | SMA sequence from beat periodicity 1s; PMC from circuit periodicity + tempo velocity; M1 = f19*f20 interaction + amplitude. Grahn & Brett 2007: SMA F(2,38)=20.67. Kohler 2025: M1 MVPA. |
| **M** (Temporal) | 3D | circuit_flow, hierarchy_index, timing_precision | 6 | Flow = sigma(0.5*f19+0.5*f21); hierarchy = sigma(0.5*f19+0.5*f20); timing from beat periodicity. Okada 2022: cerebellar dentate timing neurons. |
| **P** (Present) | 2D | sma_activity, m1_output | 4 | SMA from sequence planning + 100ms onset/coupling; M1 from execution + 100ms motor timing. Hoddinott & Grahn 2024: SMA RSA beat strength. |
| **F** (Forecast) | 3D | sequence_pred, execution_pred, timing_pred | 4 | Sequence from f19 + beat period; execution from f21 + tempo mean + stability; timing from precision + tempo variability. Okada 2022: predictive timing neurons. |

**Total**: 11D, 20 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| sma_activity + circuit_flow | -> `motor_hierarchy` | Core (tau=0.4) |
| sequence_pred + timing_pred | -> `motor_timing` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| SMA / pre-SMA | Temporal sequence encoding (Grahn & Brett 2007: Z=5.03) |
| PMC (Premotor Cortex) | Action selection; beta oscillations (Pierrieau 2025) |
| M1 (Primary Motor) | Motor execution (Kohler 2025: MVPA content-specific) |
| Cerebellum (Dentate) | Timing precision; 3 neuron types (Okada 2022) |
| Putamen | Beat-metric response (Grahn & Brett 2007: Z=5.67) |

5+ papers: Grahn & Brett 2007, Hoddinott & Grahn 2024, Kohler 2025, Okada 2022, Pierrieau 2025, Harrison 2025.

---
---

# NSCP — Neural Synchrony Commercial Prediction

**Model**: MPU-gamma1-NSCP
**Type**: Mechanism (Depth 2) — reads PEOM, ASAP, SPMC outputs
**Tier**: gamma (50-70% confidence)
**Output**: 11D per frame (4 layers: E 3D + M 3D + P 2D + F 3D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

NSCP models the pathway from population-level neural synchrony (inter-subject correlation) to commercial success prediction. ISC predicts streaming popularity (R^2=0.619 combined model); 1% ISC increase corresponds to ~2.4M more Spotify streams. Catchiness (groove/motor entrainment) drives repeated listening via an inverted-U syncopation-groove relationship.

**Reads**: PEOM, ASAP, SPMC motor timing outputs + R3/H3
**Feeds**: Popularity proxy, groove response

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[3]** | stumpf | A: Consonance | Harmonic consonance for cross-subject consistency |
| 2 | **[8]** | loudness | B: Dynamics | Loudness entropy for engagement driver |
| 3 | **[10]** | spectral_flux | B: Dynamics | Musical events for ISC engagement |
| 4 | **[25:33]** | x_l0l5 | F: Interactions | Cross-layer coherence as neural sync proxy |
| 5 | **[33:41]** | x_l4l5 | G: Interactions | Multi-feature binding for ISC prediction |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f22:neural_synchrony, f23:commercial_prediction, f24:catchiness_index | 5 | ISC proxy from coherence periodicity + consonance; commercial from f22 + binding periodicity; catchiness from onset periodicity + loudness entropy. Leeuwis 2021: R^2=0.619. Spiech 2022: groove inverted-U F(1,29)=10.515. |
| **M** (Temporal) | 3D | isc_magnitude, sync_consistency, popularity_estimate | 3 | ISC = f22; consistency from coherence + binding periodicity dual; popularity = f23. Leeuwis 2021: early R^2=0.404 vs late R^2=0.393 (stable). |
| **P** (Present) | 2D | coherence_level, groove_response | 6 | Coherence from shortest H3 (25ms-100ms) cross-layer coupling; groove from short-timescale onset tracking. Hasson 2004: ISC content-driven and reliable. |
| **F** (Forecast) | 3D | synchrony_pred, popularity_pred, catchiness_pred | 5 | Synchrony from f22 + coherence period; popularity from f23 + binding period; catchiness from f24 + onset period. ISC temporal stability supports prediction. |

**Total**: 11D, 19 H3 tuples (L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| groove_response + coherence_level | -> `neural_synchrony` | Appraisal |
| popularity_pred + catchiness_pred | -> `commercial_potential` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Frontocentral Cortex | Strongest ISC effects (Leeuwis 2021: EEG) |
| Temporal Cortex | ISC during naturalistic listening (Hasson 2004) |
| NAcc | Predicts future sales (Berns 2010: r=0.33) |
| Motor Cortex | Groove/motor entrainment (Sarasso 2019: eta^2=0.685) |

4+ papers: Leeuwis 2021 (EEG, R^2=0.619), Berns 2010 (fMRI), Spiech 2022, Sarasso 2019, Hasson 2004.

---
---

# CTBB — Cerebellar Theta-Burst Balance

**Model**: MPU-gamma2-CTBB
**Type**: Mechanism (Depth 2) — reads PEOM, GSSM, SPMC outputs
**Tier**: gamma (50-70% confidence)
**Output**: 11D per frame (4 layers: E 3D + M 3D + P 2D + F 3D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

CTBB models cerebellar theta-burst stimulation (iTBS) effects on motor timing and postural control. Cerebellar iTBS reduces postural sway (eta-sq=0.202, F=9.600, p=.004) with effects sustained >= 30 min. The cerebellar dentate nucleus contains three functional neuron types for rhythm prediction, timing control, and error detection. CBI null result (eta-sq=0.045 n.s.) suggests the behavioral improvement may involve alternative circuits (cerebellar-prefrontal, cerebellar-vestibular).

**Reads**: PEOM, GSSM timing signals + R3/H3
**Feeds**: Timing precision, postural control

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[7]** | amplitude | B: Dynamics | Motor output level for postural control |
| 2 | **[10]** | spectral_flux | B: Dynamics | Timing dynamics for cerebellar tempo tracking |
| 3 | **[25:33]** | x_l0l5 | F: Interactions | Cerebellar-M1 coupling stability and periodicity |
| 4 | **[33:41]** | x_l4l5 | G: Interactions | Balance variability monitoring |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f25:cerebellar_timing, f26:m1_modulation, f27:postural_control | 5 | Timing from coupling stability 1s; M1 modulation from coupling periodicity + fast cerebellar signal; postural = f25*f26 interaction + inverted balance variability + amplitude. Sansare 2025: eta-sq=0.202. |
| **M** (Temporal) | 3D | timing_enhancement, sway_reduction, cerebellar_m1_coupling | 3 | Enhancement with TAU_DECAY=1800s; sway = sigma(0.5*f27 + 0.5*(1-balance_var)); coupling = sigma(0.5*f25 + 0.5*f26). CBI null suggests indirect pathway. |
| **P** (Present) | 2D | timing_precision, motor_stability | 0 | Timing precision from f25 + enhancement dynamics; motor stability from sway reduction + coupling. Ivry 1988: lateral cerebellum timing dissociation. |
| **F** (Forecast) | 3D | timing_pred, balance_pred, modulation_pred | 0 | Timing from f25 + coupling stability; balance from f27 + coupling periodicity; modulation from f26 (highest uncertainty). Sansare 2025: sustained >= 30 min. |

**Total**: 11D, 8 H3 tuples (L0 + L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| timing_precision + motor_stability | -> `cerebellar_timing` | Appraisal |
| timing_pred + balance_pred | -> `balance_prediction` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Cerebellum (Dentate) | 3 neuron types: rhythm prediction, timing, error (Okada 2022) |
| Cerebellum (Lateral) | Timing vs execution dissociation (Ivry 1988) |
| M1 | Cerebellar-M1 pathway (CBI null; Sansare 2025) |
| Prefrontal | Alternative cerebellar-prefrontal circuit |
| Vestibular | Balance-related cerebellar output |

4+ papers: Sansare 2025 (iTBS, N=38), Okada 2022, Ivry 1988, Shi 2025, Huang 2005.

---
---

# STC — Singing Training Connectivity

**Model**: MPU-gamma3-STC
**Type**: Mechanism (Depth 2) — reads MSR, SPMC outputs
**Tier**: gamma (50-70% confidence)
**Output**: 11D per frame (4 layers: E 3D + M 3D + P 2D + F 3D)
**Phase**: 1
**Status**: PENDING

---

## 1. Identity

STC models the interoceptive-motor integration underlying singing training connectivity. Singing uniquely engages respiratory control, vocal production, and interoceptive monitoring in an integrated circuit. Training enhances resting-state connectivity between insula and speech/respiratory sensorimotor areas. Right anterior insula (AIC) shows expertise x anesthesia dissociation (F=22.08), confirming its role as the interoceptive hub.

**Reads**: MSR training level, SPMC motor circuit + R3/H3
**Feeds**: Vocal motor output, interoceptive monitoring

---

## 2. R3 Input Map

| # | R3 Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[7]** | amplitude | B: Dynamics | Vocal intensity for production level |
| 2 | **[8]** | loudness | B: Dynamics | Respiratory amplitude and breath entropy |
| 3 | **[12]** | warmth | C: Timbre | Singing resonance quality / laryngeal motor output |
| 4 | **[15]** | tristimulus1 | C: Timbre | Voice harmonic fundamental energy |
| 5 | **[25:33]** | x_l0l5 | F: Interactions | Respiratory timing / breath-phrase coupling |
| 6 | **[33:41]** | x_l4l5 | G: Interactions | Interoceptive-motor / voice-body connection |

---

## 3. Layer Summary

| Layer | Dims | Key Outputs | H3 | Key Computation |
|-------|------|-------------|-----|-----------------|
| **E** (Extraction) | 3D | f28:interoceptive_coupling, f29:respiratory_integration, f30:speech_sensorimotor | 11 | Interoceptive from x_l4l5 periodicity 1s; respiratory from respiratory periodicity + breath entropy; speech motor from vocal warmth 100ms. Kleber 2013: right AIC F=22.08. Zamorano 2023: singing training predicts insula-sensorimotor connectivity. |
| **M** (Temporal) | 3D | connectivity_strength, respiratory_index, voice_body_coupling | 1 | Connectivity = sigma(0.5*f28 + 0.5*interoceptive period); respiratory = f29; voice-body = sigma(0.5*f28 + 0.5*f30). Kleber 2013: AIC to M1/S1/auditory connectivity. |
| **P** (Present) | 2D | insula_activity, vocal_motor | 0 | Insula from f28 + connectivity dynamics; vocal motor from f30 + voice-body coupling. Zarate 2010: involuntary pitch correction supports automatic interoceptive-motor loop. |
| **F** (Forecast) | 3D | connectivity_pred, respiratory_pred, vocal_pred | 0 | Connectivity from f28 + interoceptive period 1s; respiratory from f29 + respiratory period 1s; vocal from f30 + warmth 100ms. Zarate 2010: automatic predictive vocal control. |

**Total**: 11D, 12 H3 tuples (L2)

---

## 4. Output Routing

| Output | -> Belief | Type |
|--------|----------|------|
| insula_activity + vocal_motor | -> `vocal_integration` | Appraisal |
| connectivity_pred + respiratory_pred | -> `singing_connectivity` | Anticipation |

---

## 5. Brain Regions

| Region | Role |
|--------|------|
| Right Anterior Insula (AIC) | Interoceptive hub; expertise x anesthesia (F=22.08; MNI: 48, 0, -3) |
| SMA / M1 | Speech motor execution |
| S1 | Somatosensory feedback for vocal control |
| ACC | Compensatory vocal control network (Zarate 2008) |
| Bilateral Thalamus | Insula co-activation (Zamorano 2023) |
| Left Putamen | Motor sequencing for singing (Zamorano 2023) |

5+ papers: Zamorano 2023 (rs-fMRI), Kleber 2013 (fMRI, anesthesia), Zarate 2008/2010, Tsunada 2024, Criscuolo 2022 (ALE meta, N=3005).

---
---

## Summary Statistics

### Output Dimensions by Model

| Model | Unit | Tier | D | E-Layer | M-Layer | P-Layer | F-Layer | H3 |
|-------|------|------|---|---------|---------|---------|---------|-----|
| PEOM | MPU | alpha | 11 | 3 | 4 | 2 | 2 | 15 |
| MSR | MPU | alpha | 11 | 3 | 3 | 3 | 2 | 22 |
| GSSM | MPU | alpha | 11 | 3 | 4 | 2 | 2 | 12 |
| ASAP | MPU | beta | 11 | 3 | 3 | 3 | 2 | 9 |
| DDSMI | MPU | beta | 11 | 3 | 3 | 2 | 3 | 11 |
| VRMSME | MPU | beta | 11 | 3 | 3 | 2 | 3 | 12 |
| SPMC | MPU | beta | 11 | 3 | 3 | 2 | 3 | 20 |
| NSCP | MPU | gamma | 11 | 3 | 3 | 2 | 3 | 19 |
| CTBB | MPU | gamma | 11 | 3 | 3 | 2 | 3 | 8 |
| STC | MPU | gamma | 11 | 3 | 3 | 2 | 3 | 12 |
| **TOTAL** | | | **110** | **30** | **32** | **22** | **26** | **140** |

### Tier Gradient

| Tier | Count | Avg D | Avg H3 |
|------|-------|-------|--------|
| alpha | 3 | 11.0 | 16.3 |
| beta | 4 | 11.0 | 13.0 |
| gamma | 3 | 11.0 | 13.0 |

F7 is unique among C3 functions in having uniform 11D output across all 10 models. This reflects the standardized 4-layer (E+M+P+F) architecture adopted for all MPU models. H3 demand varies from 8 (CTBB) to 22 (MSR), with MSR's extensive gamma-band PLV tracking requiring the most multi-scale temporal features. Alpha models average highest H3 (16.3) due to their direct R3/H3 feature extraction roles.

### Brain Region Convergence

**SMA / pre-SMA** is the convergence hub: mentioned in PEOM, MSR, GSSM, ASAP, VRMSME, SPMC, STC -- 7 of 10 models.
**M1 / Primary Motor Cortex**: mentioned in GSSM, VRMSME, SPMC, CTBB, STC -- 5 of 10 models.
**Putamen (dorsal striatum)**: mentioned in PEOM, GSSM, ASAP, SPMC, STC -- 5 of 10 models.
**Cerebellum**: mentioned in PEOM, MSR, SPMC, CTBB -- 4 of 10 models.
**PMC (Premotor Cortex)**: mentioned in PEOM, ASAP, VRMSME, SPMC -- 4 of 10 models.
**Anterior Insula**: mentioned in STC -- 1 of 10 models (specialized for singing).

### Unit Distribution

| Unit | Count | Models |
|------|-------|--------|
| MPU (Motor Processing Unit) | 10 | PEOM, MSR, GSSM, ASAP, DDSMI, VRMSME, SPMC, NSCP, CTBB, STC |

F7 is exclusively MPU (10/10 models), reflecting that motor and timing is a unified motor processing function. All models share the same computational unit, distinguished only by depth tier (alpha/beta/gamma).

### Layer Distribution

| Layer Type | Models With | Total Dims |
|------------|-------------|------------|
| E (Extraction) | 10/10 | 30D |
| M (Temporal Integration) | 10/10 | 32D |
| P (Cognitive Present) | 10/10 | 22D |
| F (Forecast) | 10/10 | 26D |

All 10 models have all 4 layers (E+M+P+F), making F7 the only function where every model implements the full 4-layer architecture. The E-layer is uniform at 3D across all models. M-layer varies (3-4D), P-layer is mostly 2D (except MSR and ASAP at 3D), and F-layer is mostly 3D (except PEOM, MSR, GSSM, and ASAP at 2D).
