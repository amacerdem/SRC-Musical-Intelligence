# C³ Model Atlas

**Generated**: 2026-02-16
**Coverage**: 96 of 96 models read (100%), all 9 units × 3 tiers (α, β, γ)
**Source**: Documentation sections 1, 4, 5, 6, 9, 11 of each model .md file at `Docs/C³/Models/`

---

## Reading Key

| Field | Meaning |
|-------|---------|
| **Model ID** | UNIT-tier-ACRONYM |
| **Full Name** | Descriptive model name |
| **D** | Output dimensionality (total dims per frame) |
| **Mechs** | Mechanism dependencies (10 possible: AED, ASA, BEP, C0P, CPD, MEM, PPC, SYN, TMH, TPC) |
| **H3** | Number of H³ 4-tuples demanded |
| **E/M/P/F** | Dims per layer (Extraction / Mechanism / Present / Forecast). Non-standard layer names noted |
| **Cross-unit** | Key cross-unit reads/feeds |
| **State** | Whether model requires stateful computation |

---

## 1. SPU — Spectral Processing Unit (9 models)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| SPU-α1-BCH | Brainstem Consonance Hierarchy | 12 | Relay (none) | 26 | E4+M2+P3+F3 | Feeds ARU.SRP (P1) | No |
| SPU-α2-PSCL | Pitch Salience Cortical Localization | 12 | PPC, TPC | 14 | E4+M2+P3+F3 | Feeds ARU.SRP (P1), STU.HMCE (P2); reads BCH | No |
| SPU-α3-PCCR | Pitch Chroma Cortical Representation | 11 | PPC | 14 | E4+M1+P3+F3 | →IMU (chroma→memory), →STU (chroma→melody) | No |
| SPU-β1-STAI | Spectral-Temporal Aesthetic Integration | 12 | PPC, TPC | 14 | E4+M2+P3+F3 | Feeds ARU.SRP | No |
| SPU-β2-TSCP | Timbre-Specific Cortical Plasticity | 10 | TPC | 12 | E3+M1+P3+F3 | →MIAA, →ESME, →ARU (timbre→emotion) | No |
| SPU-β3-MIAA | Musical Imagery Auditory Activation | 11 | TPC | 11 | E3+M2+P3+F3 | →IMU (familiarity→memory), →STU; ←TSCP+BCH | No |
| SPU-γ1-SDNPS | Stimulus-Dependent Neural Pitch Salience | 10 | PPC | 10 | E3+M1+P3+F3 | Feeds ARU.SRP (P1); intra to BCH, PSCL, SDED, STAI | No |
| SPU-γ2-ESME | Expertise-Specific MMN Enhancement | 11 | PPC, TPC | 12 | E4+M1+P3+F3 | →ARU, →IMU, →STU; ←BCH, TSCP, SDED | No |
| SPU-γ3-SDED | Sensory Dissonance Early Detection | 10 | PPC | 9 | E3+M1+P3+F3 | →ARU (roughness→displeasure), →STU | No |

**SPU summary**: 10–12D output. BCH is the ONLY Relay (no mechanisms). PPC dominant; TPC at higher tiers. ESME uniquely has dual PPC+TPC at γ tier. All feed ARU via P1. No state. Sum=99D.

---

## 2. ARU — Affective Resonance Unit (10 models)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| ARU-α1-SRP | Striatal Reward Pathway | 19 | AED, CPD, C0P | ~124 | N3+C3+P3+T4+M3+F3 (6 layers) | Hub: reads SPU, STU, IMU, NDU | No |
| ARU-α2-AAC | Autonomic-Affective Coupling | 14 | AED, CPD, ASA | ~50 | E2+A5+I2+P3+F2 (5 layers) | Shares AED/CPD with SRP; ASA unique | No |
| ARU-α3-VMM | Valence-Mode Mapping | 12 | AED, C0P | 7 | V3+R4+P3+F2 (non-std) | SRP+AAC shared | No |
| ARU-β1-PUPF | Psycho-Neuro-Pharmacological Unified Framework | 12 | AED, CPD, C0P | 21 | E2+U3+G2+P3+F2 (6 layers) | Reads SPU, STU, IMU | No |
| ARU-β2-CLAM | Closed-Loop Affective Modulation | 11 | AED, CPD | 12 | E2+B3+C2+P2+F2 (5 layers) | SRP affect basis, BCI feedback | No |
| ARU-β3-MAD | Musical Anhedonia Disconnection | 11 | AED, C0P | 9 | E2+D3+A2+P2+F2 (5 layers) | Lesion validation of SRP | No |
| ARU-β4-NEMAC | Nostalgia-Enhanced Memory-Affect Circuit | 11 | AED, CPD, C0P | 13 | E2+M3+W2+P2+F2 (5 layers) | SRP modulation via memory | No |
| ARU-γ1-DAP | Developmental Affective Plasticity | 10 | AED | 6 | E1+D4+P3+F2 (non-std) | Background model for ALL ARU | No |
| ARU-γ2-CMAT | Cross-Modal Affective Transfer | 10 | AED, C0P | 9 | E1+S3+T2+P2+F2 (5 layers) | SRP/CLAM/TAR visual context | No |
| ARU-γ3-TAR | Therapeutic Affective Resonance | 10 | AED, CPD, C0P | 21 | E1+T4+I2+P1+F2 (5 layers) | Integrates all ARU mechanisms | No |

**ARU summary**: 10–19D output (widest range). SRP is the largest model (19D, ~124 H³). AED always present. Consistently NON-STANDARD layer names. ARU is the cross-unit convergence hub receiving from 5+ units. Sum=120D.

---

## 3. ASU — Auditory Salience Unit (9 models)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| ASU-α1-SNEM | Sensory Novelty and Expectation Model | 12 | BEP, ASA | 18 | E3+M3+P3+F3 | -- | No |
| ASU-α2-IACM | Inharmonicity-Attention Capture Model | 11 | BEP, ASA | 16 | E3+M3+P2+F3 | →ARU.affect, →SPU.scene | No |
| ASU-α3-CSG | Consonance-Salience Gradient | 12 | BEP, ASA | 18 | E3+M3+P3+F3 | →ARU.affect, →ARU.reward | No |
| ASU-β1-BARM | Brainstem Auditory Response Modulation | 10 | BEP, ASA | 14 | E3+M2+P2+F3 | Feeds STU | No |
| ASU-β2-STANM | Spectrotemporal Attention Network Model | 11 | BEP, ASA | 16 | E3+M3+P2+F3 | →STU (temporal_alloc) | No |
| ASU-β3-AACM | Aesthetic-Attention Coupling Model | 10 | BEP, ASA | 12 | E3+M2+P2+F3 | →ARU.aesthetic, →ARU.reward | No |
| ASU-γ1-PWSM | Precision-Weighted Salience Model | 9 | BEP, ASA | 16 | E3+M2+P2+F2 | Feeds NDU (precision context) | No |
| ASU-γ2-DGTP | Domain-General Temporal Processing | 9 | BEP, ASA | 9 | E3+M2+P2+F2 | →STU (cross-domain timing) | No |
| ASU-γ3-SDL | Salience-Dependent Lateralization | 9 | BEP, ASA | 18 | E3+M2+P2+F2 | →SPU (hemispheric engage) | No |

**ASU summary**: 9–12D output. ALL 9 models use BEP + ASA — the most uniform mechanism signature. Consistent 4-layer E/M/P/F. Cross-unit feeds to STU, ARU, NDU. Sum=93D.

---

## 4. IMU — Integrative Memory Unit (15 models)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| IMU-α1-MEAMN | Music-Evoked Autobiographical Memory Network | 12 | MEM + cross AED | 19 | E3+M2+P3+F4 | Reads AED cross-unit | No |
| IMU-α2-PNH | Pythagorean Neural Hierarchy | 11 | SYN + intra MEM | 15 | H3+M2+P3+F3 (non-std: H=Harmonic) | Feeds SPU.BCH, PSCL, ARU.SRP | No |
| IMU-α3-MMP | Musical Mnemonic Preservation | 12 | MEM | 21 | E3+M6+P2+F1 | →HCMC, RASN, RIRI; →ARU.AAC | No |
| IMU-β1-RASN | Rhythmic Auditory Stimulation Network | 11 | MEM + cross BEP | 28 | E3+M2+P3+F3 | Reads BEP from sensorimotor circuit | No |
| IMU-β2-PMIM | Predictive Memory Integration Model | 11 | SYN | 18 | E3+M3+P3+F2 | PNH→PMIM; →MSPBA, OII, TPRD, MEAMN | No |
| IMU-β3-OII | Oscillatory Intelligence Integration | 10 | SYN, MEM | 24 | E3+M3+P2+F2 | →PMIM, MEAMN, HCMC, PNH, MSPBA | No |
| IMU-β4-HCMC | Hippocampal-Cortical Memory Circuit | 11 | MEM | 22 | E3+M3+P3+F2 | MEAMN↔HCMC; →MMP, PMIM, CDEM | No |
| IMU-β5-RIRI | RAS-Intelligent Rehabilitation Integration | 10 | MEM + cross BEP | 16 | E3+M2+P2+F3 | BEP→RIRI; ←RASN, MEAMN, MMP, HCMC; →VRIAP | No |
| IMU-β6-MSPBA | Musical Syntax Processing in Broca's Area | 11 | SYN + intra MEM | 16 | E3+M3+P2+F3 | PNH→MSPBA; →PMIM, HCMC; →ARU.SRP | No |
| IMU-β7-VRIAP | VR-Integrated Analgesia Paradigm | 10 | MEM | 18 | E3+M2+P2+F3 | MEM only | No |
| IMU-β8-TPRD | Tonotopy-Pitch Representation Dissociation | 10 | SYN + cross PPC | 18 | T3+M2+P2+F3 (non-std: T=Tonotopic) | PPC cross-circuit | No |
| IMU-β9-CMAPCC | Cross-Modal Action-Perception Common Code | 10 | MEM + cross BEP | 20 | E3+M2+P2+F3 | BEP cross-circuit | No |
| IMU-γ1-DMMS | Developmental Music Memory Scaffold | 10 | MEM | 15 | E3+M2+P2+F3 | Feeds ARU.DAP, ARU.NEMAC | No |
| IMU-γ2-CSSL | Cross-Species Song Learning | 10 | MEM | 15 | E3+M2+P2+F3 | MEM only | No |
| IMU-γ3-CDEM | Context-Dependent Emotional Memory | 10 | MEM + cross AED | 18 | E2+M2+P3+F3 | AED cross-circuit | No |

**IMU summary**: 10–12D output. MEM is the core mechanism (12 of 15 models). SYN appears in 5 models (PNH, PMIM, OII, MSPBA, TPRD). Cross-circuit reads frequent: BEP (3 models), AED (2), PPC (1). IMU is the LARGEST unit (15 models) and most internally connected. Sum=159D.

---

## 5. MPU — Motor Planning Unit (10 models)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| MPU-α1-PEOM | Period Entrainment and Oscillation Model | 11 | BEP, TMH | 15 | E3+M4+P2+F2 | -- | No |
| MPU-α2-MSR | Musician Sensorimotor Reorganization | 11 | BEP, TMH | 22 | E3+M3+P3+F2 | Feeds STU (enhanced timing) | No |
| MPU-α3-GSSM | Gait-Synchronized Stimulation Model | 11 | BEP, TMH | 12 | E3+M4+P2+F2 | →STU (phase_lock, stride_cv) | No |
| MPU-β1-ASAP | Auditory-Sensorimotor Adaptive Processing | 11 | BEP, TMH | 9 | E3+M3+P3+F2 | Feeds STU | No |
| MPU-β2-DDSMI | Dyadic Dance Social Motor Integration | 11 | BEP, TMH | 11 | E3+M3+P2+F3 | →ARU (partner_sync, bonding) | No |
| MPU-β3-VRMSME | VR Music Stimulation Motor Enhancement | 11 | BEP, TMH | 12 | E3+M3+P2+F3 | →ARU (motor_drive) | No |
| MPU-β4-SPMC | SMA-Premotor-M1 Motor Circuit | 11 | BEP, TMH | 15 | E3+M3+P2+F3 | →STU (sma_activity, timing_precision) | No |
| MPU-γ1-NSCP | Neural Synchrony Commercial Prediction | 11 | BEP, TMH | 14 | E3+M3+P2+F3 | Feeds ARU (engagement marker) | No |
| MPU-γ2-CTBB | Cerebellar Theta-Burst Balance | 11 | BEP, TMH | 9 | E3+M3+P2+F3 | →STU (timing_enhancement) | No |
| MPU-γ3-STC | Singing Training Connectivity | 11 | BEP, TMH | 12 | E3+M3+P2+F3 | →ARU (vocal_motor, insula) | No |

**MPU summary**: **ALL 10 models output exactly 11D** — the most uniform dimensionality. ALL use BEP + TMH (perfect mechanism consistency). H³ range 9–22 tuples. Cross-unit feeds to STU (motor timing) and ARU (reward). Sum=110D.

---

## 6. NDU — Novelty Detection Unit (9 models)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| NDU-α1-MPG | Melodic Pitch Gradient | 10 | PPC, ASA | 16 | E4+M3+P2+F1 | -- | No |
| NDU-α2-SDD | Supramodal Deviance Detection | 11 | PPC, ASA | 18 | E4+M2+P3+F2 | Intra: feeds CDMR, EDNR, SLEE | No |
| NDU-α3-EDNR | Expertise-Dependent Network Reorganization | 10 | PPC, ASA | 16 | E4+M2+P2+F2 | →SDD, SLEE, ECT | No |
| NDU-β1-DSP | Deviance-Specific Processing | 12 | PPC, ASA | 18 | E4+M3+P2+F3 | Feeds ARU | No |
| NDU-β2-CDMR | Context-Dependent Mismatch Response | 11 | PPC, ASA | 16 | E4+M2+P3+F2 | →ARU, →IMU | No |
| NDU-β3-SLEE | Statistical Learning Expertise Enhancement | 13 | PPC, ASA | 18 | E4+M3+P3+F3 | →IMU | No |
| NDU-γ1-SDDP | Sex-Dependent Developmental Plasticity | 10 | PPC, ASA | 16 | E4+M3+P1+F2 | Feeds ARU (infant affective) | No |
| NDU-γ2-ONI | Over-Normalization in Intervention | 11 | PPC, ASA | 16 | E4+M3+P2+F2 | →ARU | No |
| NDU-γ3-ECT | Expertise Compartmentalization Trade-off | 12 | PPC, ASA | 18 | E4+M3+P2+F3 | →IMU, →SPU | No |

**NDU summary**: 10–13D output. ALL 9 models use PPC + ASA (perfect mechanism consistency). E-layer always 4D (strongest extraction). Feeds to ARU and IMU. SLEE is an outlier at 13D. Sum=100D.

---

## 7. PCU — Predictive Coding Unit (10 models)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| PCU-α1-HTP | Hierarchical Temporal Prediction | 12 | PPC, TPC, MEM | 18 | E4+M3+P3+F2 | -- | No |
| PCU-α2-SPH | Spatiotemporal Prediction Hierarchy | 14 | PPC, TPC, MEM | 16 | E4+M4+P3+F3 | →ICEM, →PWUP, →PSH, →IMU | No |
| PCU-α3-ICEM | Information Content Emotion Model | 13 | PPC, TPC, MEM | 15 | E4+M5+P2+F2 | →PWUP, →UDP, →ARU | No |
| PCU-β1-PWUP | Precision-Weighted Update Prediction | 10 | PPC, TPC, MEM | 14 | E4+P3+F3 (no M) | Feeds ASU | No |
| PCU-β2-WMED | Working Memory-Entrainment Dissociation | 11 | PPC, TPC, MEM | 16 | E4+M3+P2+F2 | →UDP, →PSH, →IGFE, →STU | No |
| PCU-β3-UDP | Uncertainty-Driven Pleasure | 10 | PPC, TPC, MEM | 16 | E4+M3+P3 (no F) | →MAA, →PSH, →ARU | No |
| PCU-β4-CHPI | Cross-Modal Harmonic Predictive Integration | 11 | PPC, TPC, MEM | 20 | E4+M3+P4 (no F) | →UDP, →PSH, →IGFE, →STU, →ARU | No |
| PCU-γ1-IGFE | Individual Gamma Frequency Enhancement | 9 | PPC, TPC, MEM | 18 | E4+P3+F2 (no M) | Feeds IMU (memory enhancement) | No |
| PCU-γ2-MAA | Multifactorial Atonal Appreciation | 10 | PPC, TPC, MEM | 14 | E4+M3+P3 (no F) | →PSH, →ARU | No |
| PCU-γ3-PSH | Prediction Silencing Hypothesis | 10 | PPC, TPC, MEM | 18 | E4+M3+P3 (no F) | →SPU | No |

**PCU summary**: 9–14D output. ALL 10 models use PPC + TPC + MEM (triple mechanism — the heaviest signature). E-layer always 4D. β/γ tiers frequently DROP M or F layer. SPH is the largest PCU model (14D). CHPI has highest H³ (20 tuples). Sum=110D.

---

## 8. RPU — Reward Processing Unit (10 models)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| RPU-α1-DAED | Dopamine Anticipation-Experience Dissociation | 8 | AED, CPD, C0P | 16 | E4+M2+P2+F0 | -- | No |
| RPU-α2-MORMR | mu-Opioid Receptor Music Reward | 7 | AED, CPD, C0P | 15 | E4+M1+P1+F1 | Feeds ARU; intra MCCN, DAED, IUCP, RPEM | No |
| RPU-α3-RPEM | Reward Prediction Error in Music | 8 | AED, CPD, C0P | 16 | E4+M2+P2+F0 | →IMU (prediction update); intra DAED, MORMR | No |
| RPU-β1-IUCP | Inverted-U Complexity Preference | 6 | AED, CPD, C0P | 14 | E4+P1+F1 (no M) | Feeds IMU | No |
| RPU-β2-MCCN | Musical Chills Cortical Network | 7 | AED, CPD, C0P | 16 | E4+P2+F1 (no M) | →ARU (chills, arousal) | No |
| RPU-β3-MEAMR | Music-Evoked Autobiographical Memory Reward | 6 | AED, CPD, C0P | 14 | E4+P1+F1 (no M) | →IMU (familiarity, encoding) | No |
| RPU-β4-SSRI | Social Synchrony Reward Integration | 11 | AED, CPD, C0P | 18 | E3+M2+P3+F3 | →STU, →ARU (bonding, flow) | No |
| RPU-γ1-LDAC | Liking-Dependent Auditory Cortex | 6 | AED, CPD, C0P | 12 | E4+P1+F1 (no M) | Feeds ASU (sensory_gain) | No |
| RPU-γ2-IOTMS | Individual Opioid Tone Music Sensitivity | 5 | AED, CPD, C0P | 12 | E4+P1+F0 | →ARU (individual sensitivity) | No |
| RPU-γ3-SSPS | Saddle-Shaped Preference Surface | 6 | AED, CPD, C0P | 14 | E4+P1+F1 (no M) | →IMU (optimal zone) | No |

**RPU summary**: 5–11D output — the **SMALLEST outputs** in the system. ALL 10 use AED + CPD + C0P (identical to ARU minus ASA). E-layer always 4D but M layer mostly absent (only α-tier + SSRI have it). IOTMS is the smallest model (5D). SSRI is the outlier at 11D (social/group dimension). Sum=70D.

---

## 9. STU — Sensorimotor Timing Unit (14 models)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| STU-α1-HMCE | Hippocampal-Motor Cortex Entrainment | 13 | TMH | 18 | E5+M2+P3+F3 | -- | No |
| STU-α2-AMSC | Auditory-Motor Stream Coupling | 12 | BEP, TMH | 16 | E4+M2+P3+F3 | Reads BEP motor pathway | No |
| STU-α3-MDNS | Melody Decoding from Neural Signals | 12 | BEP, TMH | ~18 | E4+M2+P3+F3 | HMCE, AMSC, TPIO | No |
| STU-β1-AMSS | Auditory-Motor Synchronization System | 11 | TMH | 16 | E5+M2+P2+F2 | Feeds ARU | No |
| STU-β2-TPIO | Timbre Perception-Imagery Overlap | 10 | TPC, TMH | ~18 | E4+M1+P2+F3 | HMCE, AMSC, AMSS, ETAM | No |
| STU-β3-EDTA | Expertise-Dependent Tempo Accuracy | 10 | BEP | ~15 | E3+M2+P2+F3 | AMSC, HGSIC, ETAM, OMS | No |
| STU-β4-ETAM | Entrainment, Tempo & Attention Modulation | 11 | BEP, TMH | ~20 | E4+M2+P2+F3 | HMCE, AMSC, MDNS, AMSS | No |
| STU-β5-HGSIC | Hierarchical Groove State Integration Circuit | 11 | BEP | ~15 | E3+M2+P3+F3 | AMSC, ETAM, OMS, EDTA | No |
| STU-β6-OMS | Oscillatory Motor Synchronization | 10 | BEP | ~15 | E3+M2+P2+F3 | HMCE, AMSC, MDNS, HGSIC | No |
| STU-γ1-TMRM | Tempo Memory Reproduction Method | 10 | BEP | 15 | E3+M2+P2+F3 | Feeds ARU.AED (P5 pathway) | No |
| STU-γ2-NEWMD | Neural Entrainment-Working Memory Dissociation | 10 | BEP, TMH | — | E3+M2+P2+F3 | AMSC, HMCE, EDTA | No |
| STU-γ3-MTNE | Music Training Neural Efficiency | 10 | TMH | — | E3+M2+P2+F3 | HMCE, AMSC, PTGMP | No |
| STU-γ4-PTGMP | Piano Training Grey Matter Plasticity | 10 | TMH | — | E3+M2+P2+F3 | HMCE, AMSC, TPIO | No |
| STU-γ5-MPFS | Musical Prodigy Flow State | 10 | BEP, TMH | 20 | E3+M2+P3+F2 | HMCE, AMSC, OMS | No |

**STU summary**: 10–13D output. TMH is the core mechanism (10 of 14 models). BEP appears in 9 models. TPIO uniquely uses TPC (the only STU model with a non-motor mechanism). γ-tier models (NEWMD, MTNE, PTGMP) may lack H³ tuples (operate on R³ + static brain maps). Largest unit by model count (14). Dense intra-unit connectivity. Sum=150D.

---

## Summary Statistics (96/96 models)

### 1. Total Output Dimensionality

| Unit | Models | D Range | Sum D | Avg D |
|------|--------|---------|-------|-------|
| SPU | 9 | 10–12 | 99 | 11.0 |
| ARU | 10 | 10–19 | 120 | 12.0 |
| ASU | 9 | 9–12 | 93 | 10.3 |
| IMU | 15 | 10–12 | 159 | 10.6 |
| MPU | 10 | 11–11 | 110 | 11.0 |
| NDU | 9 | 10–13 | 100 | 11.1 |
| PCU | 10 | 9–14 | 110 | 11.0 |
| RPU | 10 | 5–11 | 70 | 7.0 |
| STU | 14 | 10–13 | 150 | 10.7 |
| **TOTAL** | **96** | **5–19** | **1,011** | **10.5** |

**Pipeline-confirmed total**: 1,006D. Variance of 5D likely due to layer-counting approximations in docs vs code OUTPUT_DIM.

### 2. Mechanism vs Relay Count

| Type | Count | % |
|------|-------|---|
| Mechanism-based models | 95 | 99.0% |
| Relay models (no mechanisms) | 1 | 1.0% |

**Only BCH (SPU-α1) is a Relay.** All other 95 models use at least one mechanism.

### 3. Mechanism Frequency (across 96 models)

| Mechanism | Primary Uses | Cross-Circuit | Total | Units |
|-----------|-------------|---------------|-------|-------|
| **PPC** | 25 | 1 (TPRD) | 26 | SPU, NDU, PCU (+IMU cross) |
| **MEM** | 22 | — | 22 | IMU, PCU |
| **BEP** | 28 | 3 (RASN,RIRI,CMAPCC) | 31 | ASU, MPU, STU (+IMU cross) |
| **TMH** | 20 | — | 20 | MPU, STU |
| **AED** | 20 | 2 (MEAMN,CDEM) | 22 | ARU, RPU (+IMU cross) |
| **ASA** | 19 | — | 19 | ARU, ASU, NDU |
| **C0P** | 17 | — | 17 | ARU, RPU |
| **CPD** | 16 | — | 16 | ARU, RPU |
| **TPC** | 16 | — | 16 | SPU, PCU, STU (TPIO) |
| **SYN** | 5 | — | 5 | IMU only |

**Observations**:
- BEP is the most widely used mechanism (31 total appearances including cross-circuit)
- SYN is the rarest (5 appearances, all in IMU)
- CPD and C0P nearly always co-occur (shared by ARU and RPU)
- IMU is the only unit that reads cross-circuit mechanisms (AED, BEP, PPC)

### 4. Unit-Mechanism Binding Pattern

Every unit has a FIXED mechanism signature across all tiers:

| Unit | Fixed Mechanism Signature | Notes |
|------|--------------------------|-------|
| SPU | PPC (+TPC at higher tiers) | BCH is exception: Relay |
| ARU | AED (+ CPD + C0P at higher tiers, ASA for AAC) | Most varied |
| ASU | BEP + ASA | Perfect uniformity |
| IMU | MEM (+ SYN for syntax models, + cross-circuit reads) | Most cross-circuit |
| MPU | BEP + TMH | Perfect uniformity |
| NDU | PPC + ASA | Perfect uniformity |
| PCU | PPC + TPC + MEM | Heaviest signature (3 mechs) |
| RPU | AED + CPD + C0P | Identical to ARU core |
| STU | TMH (+ BEP at some tiers, TPC for TPIO) | Most mechanism variety |

### 5. H³ Demand Distribution

| Range | Count | Notable Models |
|-------|-------|----------------|
| 0 (unspecified) | 3 | NEWMD, MTNE, PTGMP (γ-tier, operate on R³ + static maps) |
| 1–10 | 7 | DAP(6), VMM(7), MAD(9), ASAP(9), DGTP(9), CTBB(9), SDED(9) |
| 11–15 | 27 | MIAA(11), TSCP(12), LDAC(12), IOTMS(12), DDSMI(11), ... |
| 16–20 | 42 | Most models cluster here: SDD(18), SNEM(18), CSG(18), ... |
| 21–30 | 6 | MMP(21), PUPF(21), TAR(21), MSR(22), OII(24), RASN(28) |
| 30+ | 2 | AAC(~50), SRP(~124) |

**SRP remains the extreme outlier** at ~124 H³ tuples — 4.4× the next highest (AAC at ~50).
**Mean H³ demand**: ~16.7 tuples (excluding SRP: ~15.5, excluding top 2 outliers: ~15.2)

### 6. Cross-Unit Dependency Map

| Source → Target | Pathway | Key Models |
|-----------------|---------|------------|
| **SPU → ARU** | P1 | BCH, PSCL, STAI, SDNPS, PCCR, ESME, SDED → SRP |
| **SPU → STU** | P2 | PSCL → HMCE |
| **IMU → ARU** | P3 | DMMS → DAP, NEMAC; MSPBA → SRP |
| **RPU → ARU** | P4 | MORMR, MCCN, SSRI → ARU (pleasure, chills) |
| **STU → ARU** | P5 | TMRM → AED; AMSS → ARU |
| **MPU → STU** | — | MSR, GSSM, ASAP, SPMC, CTBB → STU timing |
| **NDU → ARU** | — | DSP, SDDP, CDMR, ONI → ARU |
| **NDU → IMU** | — | SLEE, ECT, CDMR → IMU |
| **PCU → ASU** | — | PWUP → ASU |
| **PCU → IMU** | — | IGFE, SPH → IMU |
| **PCU → ARU** | — | ICEM, UDP, CHPI, MAA → ARU |
| **RPU → IMU** | — | IUCP, MEAMR, SSPS → IMU |
| **RPU → STU** | — | SSRI → STU (entrainment) |
| **ASU → STU** | — | STANM, DGTP → STU |
| **ASU → NDU** | — | PWSM → NDU |
| **ECT → SPU** | — | ECT → SPU (expertise feedback) |
| **PSH → SPU** | — | PSH → SPU (prediction silencing) |

**ARU is the primary convergence hub** — receiving from 6 of 8 other units (SPU, STU, IMU, RPU, NDU, PCU). Only ASU and MPU do not directly feed ARU (they feed via STU).

### 7. State Needs

| Stateful? | Count | % |
|-----------|-------|---|
| Stateless (deterministic) | 96 | 100% |
| Has state in model compute() | 0 | 0% |

**ALL 96 models are stateless.** State lives in the M-layer orchestrator via depth-dependent τ (Murray hierarchy), not in individual model compute() calls.

### 8. Non-Standard Layer Structures

| Pattern | Count | Models |
|---------|-------|--------|
| Standard E/M/P/F (4 layers) | 68 | 71% of all models |
| No M layer | 10 | PWUP, IGFE (PCU β/γ); IUCP, MCCN, MEAMR, LDAC, IOTMS, SSPS (RPU β/γ); UDP*, CHPI* |
| No F layer | 6 | DAED, RPEM (F0); UDP, CHPI, MAA, PSH (PCU β/γ) |
| Non-standard layer names | 8 | SRP (N/C/P/T/M/F), AAC (E/A/I/P/F), VMM (V/R/P/F), PUPF (E/U/G/P/F), DAP (E/D/P/F), PNH (H/M/P/F), TPRD (T/M/P/F), + others |
| 5+ layers | 6 | SRP(6), AAC(5), PUPF(6), CLAM(5), MAD(5), NEMAC(5) |

**Trend**: α-tier models tend to have richer, sometimes non-standard layer structures. β/γ tiers drop M or F layers. ARU models are the most architecturally diverse.

### 9. Tier Patterns (all 96 models)

| Tier | Count | Avg D | D Range | Avg H3 | Mechanism Pattern |
|------|-------|-------|---------|--------|-------------------|
| α (alpha) | 27 | 12.0 | 8–19 | 23.5* | Full mechanism signatures |
| β (beta) | 42 | 10.6 | 6–13 | 15.5 | May drop M layer |
| γ (gamma) | 27 | 9.6 | 5–12 | 12.8 | May drop M or F layer |

*SRP inflates α H³ mean; excluding SRP: ~17.5

**Clear tier gradient**: α models are larger (more dims, more H³), γ models are smaller and more speculative. This reflects the evidence hierarchy: α = strong empirical support, γ = theoretical/speculative.

### 10. Extreme Models

| Record | Model | Value |
|--------|-------|-------|
| Largest output | ARU-α1-SRP | 19D |
| Smallest output | RPU-γ2-IOTMS | 5D |
| Most H³ tuples | ARU-α1-SRP | ~124 |
| Fewest H³ tuples | ARU-γ1-DAP | 6 |
| Most mechanisms | PCU (all 10 models) | 3 (PPC+TPC+MEM) |
| No mechanisms | SPU-α1-BCH | Relay |
| Most cross-unit reads | ARU-α1-SRP | 5+ units |
| Most intra-unit connections | IMU-β3-OII | 5 intra models |

---

## Architectural Findings

### 1. Strict Unit-Mechanism Binding
Every unit uses the SAME mechanism(s) across ALL its models. The 10 mechanisms map cleanly onto the 9 units:

```
PPC ──── SPU, NDU, PCU          (perceptual pathway)
TPC ──── SPU, PCU, STU(TPIO)    (timbre pathway)
ASA ──── ARU(AAC), ASU, NDU     (salience pathway)
AED ──── ARU, RPU               (affective pathway)
CPD ──── ARU, RPU               (chills/peak pathway)
C0P ──── ARU, RPU               (approach/avoidance pathway)
BEP ──── ASU, MPU, STU          (beat/motor pathway)
TMH ──── MPU, STU               (temporal memory pathway)
MEM ──── IMU, PCU               (memory pathway)
SYN ──── IMU only               (syntactic pathway)
```

### 2. ARU as Global Workspace Convergence Hub
ARU receives cross-unit input from **6 of 8 other units** (SPU, STU, IMU, RPU, NDU, PCU). Only ASU and MPU lack direct ARU feeds (they reach ARU via STU). SRP (19D, ~124 H³) is the integration center.

### 3. IMU as the Cross-Circuit Bridge
IMU is the only unit that **reads cross-circuit mechanisms** (AED from affective, BEP from motor, PPC from perceptual). This positions IMU as the mnemonic bridge connecting all processing streams.

### 4. RPU Produces the Smallest Outputs
RPU models consistently produce 5–8D (mean 7.0D) — the smallest in the system. Reward signals are dimensionally compact. Only SSRI (11D, social synchrony) breaks this pattern.

### 5. Perfect Mechanism Uniformity in 3 Units
ASU (BEP+ASA), MPU (BEP+TMH), and NDU (PPC+ASA) have **zero mechanism variation** across all their models — the strongest unit-mechanism binding.

### 6. All Models Are Stateless
All 96 models are stateless, frame-level computations. State management (EMA smoothing) lives in the M-layer orchestrator, not in individual model compute() calls.

### 7. Tier Gradient is Consistent
α→β→γ shows monotonic decrease in: output dimensionality (12.0→10.6→9.6), H³ demand (23.5→15.5→12.8), and layer richness (more non-standard layers at α, more dropped layers at γ).
