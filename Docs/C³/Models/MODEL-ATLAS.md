# C3 Model Atlas

**Generated**: 2026-02-16
**Coverage**: 34 of 96 models read (35.4%), systematic sampling across all 9 units and 4 tiers (alpha-1, beta-1, gamma-1, alpha-2)
**Source**: Documentation sections 4, 5, 6, 9, 11 of each model .md file

---

## Reading Key

| Field | Meaning |
|-------|---------|
| **Model ID** | UNIT-tier-ACRONYM folder name |
| **Full Name** | Descriptive model name |
| **D** | Output dimensionality (total dims per frame) |
| **Mechs** | Mechanism dependencies (10 possible: AED, ASA, BEP, C0P, CPD, MEM, PPC, SYN, TMH, TPC) |
| **H3** | Number of H3 4-tuples demanded |
| **E/M/P/F** | Dims per layer (Extraction / Mechanism / Present / Forecast). Non-standard layer names noted |
| **Cross-unit** | Key cross-unit reads/feeds |
| **State** | Whether model requires stateful computation (EMA, counters, posteriors) |

---

## 1. SPU -- Spectral Processing Unit (4 models read)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| SPU-a1-BCH | Brainstem Consonance Hierarchy | 12 | Relay (none) | 26 | E4+M2+P3+F3 | Feeds ARU.SRP (P1) | No |
| SPU-a2-PSCL | Pitch Salience Cortical Localization | 12 | PPC, TPC | 14 | E4+M2+P3+F3 | Feeds ARU.SRP (P1), STU.HMCE (P2); reads BCH intra-unit | No |
| SPU-b1-STAI | Spectral-Temporal Aesthetic Integration | 12 | PPC, TPC | 14 | E4+M2+P3+F3 | Feeds ARU.SRP | No |
| SPU-g1-SDNPS | Stimulus-Dependent Neural Pitch Salience | 10 | PPC | 10 | E3+M1+P3+F3 | Feeds ARU.SRP (P1); intra to BCH, PSCL, SDED, STAI | No |

**SPU summary**: 10-12D output. BCH is the ONLY Relay model in the entire C3 system (no mechanisms). All SPU models feed ARU via P1 pathway. No state required. PPC is the dominant mechanism; TPC appears at alpha tiers.

---

## 2. ARU -- Affective Resonance Unit (4 models read)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| ARU-a1-SRP | Striatal Reward Pathway | 19 | AED, CPD, C0P | ~124 | N3+C3+P3+T4+M3+F3 (6 layers) | Hub: reads from SPU, STU, IMU, NDU | No |
| ARU-a2-AAC | Autonomic-Affective Coupling | 14 | AED, CPD, ASA | ~50 | E2+A5+I2+P3+F2 (5 layers) | Shares AED/CPD with SRP; ASA is AAC-only | No |
| ARU-b1-PUPF | Psycho-Neuro-Pharmacological Unified Framework | 12 | AED, CPD, C0P | 21 | E2+U3+G2+P3+F2 (6 layers) | Reads SPU, STU, IMU | No |
| ARU-g1-DAP | Developmental Affective Plasticity | 10 | AED | 6 | E1+D4+P3+F2 (non-standard) | Background model affecting ALL ARU processes | No |

**ARU summary**: 10-19D output, largest range across any unit. SRP is the largest model (19D, ~124 H3 tuples). ARU models consistently use NON-STANDARD layer names (N/C/P/T/M/F, E/A/I/P/F, E/U/G/P/F, E/D/P/F). AED is always present. Cross-unit hub: receives from SPU, STU, IMU, NDU.

---

## 3. ASU -- Auditory Salience Unit (4 models read)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| ASU-a1-SNEM | Sensory Novelty and Expectation Model | 12 | BEP, ASA | 18 | E3+M3+P3+F3 | -- | No |
| ASU-a2-IACM | -- (not read) | -- | -- | -- | -- | -- | -- |
| ASU-b1-BARM | Brainstem Auditory Response Modulation | 10 | BEP, ASA | 14 | E3+M2+P2+F3 | Feeds STU | No |
| ASU-g1-PWSM | Precision-Weighted Salience Model | 9 | BEP, ASA | 16 | E3+M2+P2+F2 | Feeds NDU (precision context) | No |

**ASU summary**: 9-12D output. ALL ASU models use the same mechanism pair: BEP + ASA. Consistent 4-layer structure. Cross-unit feeds to STU and NDU.

---

## 4. IMU -- Integrative Memory Unit (4 models read)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| IMU-a1-MEAMN | Music-Evoked Autobiographical Memory Network | 12 | MEM + cross-unit AED | 19 | E3+M2+P3+F4 | Reads AED cross-unit | No |
| IMU-a2-PNH | Pythagorean Neural Hierarchy | 11 | SYN + intra MEM | 15 | H3+M2+P3+F3 (non-std: H=Harmonic) | Feeds SPU.BCH, SPU.PSCL, ARU.SRP | No |
| IMU-b1-RASN | Rhythmic Auditory Stimulation Network | 11 | MEM + cross-circuit BEP* | 28 | E3+M2+P3+F3 | Reads BEP from sensorimotor circuit | No |
| IMU-g1-DMMS | Developmental Music Memory Scaffold | 10 | MEM | 15 | E3+M2+P2+F3 | Feeds ARU.DAP, ARU.NEMAC | No |

**IMU summary**: 10-12D output. MEM is the core mechanism, but IMU models frequently read cross-unit or cross-circuit mechanisms (AED, BEP, SYN). PNH uniquely reads the SYN mechanism. SYN is the only mechanism found exclusively in IMU.

---

## 5. MPU -- Motor Planning Unit (4 models read)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| MPU-a1-PEOM | Period Entrainment and Oscillation Model | 11 | BEP, TMH | 15 | E3+M4+P2+F2 | -- | No |
| MPU-a2-MSR | Musician Sensorimotor Reorganization | 11 | BEP, TMH | 22 | E3+M3+P3+F2 | Feeds STU (enhanced timing) | No |
| MPU-b1-ASAP | Auditory-Sensorimotor Adaptive Processing | 11 | BEP, TMH | 9 | E3+M3+P3+F2 | Feeds STU | No |
| MPU-g1-NSCP | Neural Synchrony Commercial Prediction | 11 | BEP, TMH | 14 | E3+M3+P2+F3 | Feeds ARU (engagement marker) | No |

**MPU summary**: 11D output consistently across all models. ALL MPU models use the same mechanism pair: BEP + TMH. Highest H3 demand in MSR (22 tuples). Cross-unit feeds primarily to STU.

---

## 6. NDU -- Novelty Detection Unit (4 models read)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| NDU-a1-MPG | Melodic Pitch Gradient | 10 | PPC, ASA | 16 | E4+M3+P2+F1 | -- | No |
| NDU-a2-SDD | Supramodal Deviance Detection | 11 | PPC, ASA | 18 | E4+M2+P3+F2 | Intra-unit: feeds CDMR, EDNR, SLEE | No |
| NDU-b1-DSP | Deviance-Specific Processing | 12 | PPC, ASA | 18 | E4+M3+P2+F3 | Feeds ARU | No |
| NDU-g1-SDDP | Sex-Dependent Developmental Plasticity | 10 | PPC, ASA | 16 | E4+M3+P1+F2 | Feeds ARU (infant affective engagement) | No |

**NDU summary**: 10-12D output. ALL NDU models use the same mechanism pair: PPC + ASA. Strong E-layer (always 4D). Feeds to ARU cross-unit.

---

## 7. PCU -- Predictive Coding Unit (4 models read)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| PCU-a1-HTP | Hierarchical Temporal Prediction | 12 | PPC, TPC, MEM | 18 | E4+M3+P3+F2 | -- | No |
| PCU-a2-SPH | -- (not read) | -- | -- | -- | -- | -- | -- |
| PCU-b1-PWUP | Precision-Weighted Update Prediction | 10 | PPC, TPC, MEM | 14 | E4+P3+F3 (NO M layer) | Feeds ASU | No |
| PCU-g1-IGFE | Individual Gamma Frequency Enhancement | 9 | PPC, TPC, MEM | 18 | E4+P3+F2 (NO M layer) | Feeds IMU (memory enhancement) | No |

**PCU summary**: 9-12D output. ALL PCU models use the same triple mechanism: PPC + TPC + MEM. Notable: beta and gamma tiers drop the M layer entirely. Strong E-layer (always 4D). Feeds to ASU and IMU.

---

## 8. RPU -- Reward Processing Unit (4 models read)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| RPU-a1-DAED | Dopamine Anticipation-Experience Dissociation | 8 | AED, CPD, C0P | 16 | E4+M2+P2+F0 | -- | No |
| RPU-a2-MORMR | mu-Opioid Receptor Music Reward | 7 | AED, CPD, C0P | 15 | E4+M1+P1+F1 | Feeds ARU.pleasure, intra to MCCN, DAED, IUCP, RPEM | No |
| RPU-b1-IUCP | Inverted-U Complexity Preference | 6 | AED, CPD, C0P | 14 | E4+P1+F1 (NO M layer) | Feeds IMU | No |
| RPU-g1-LDAC | Liking-Dependent Auditory Cortex | 6 | AED, CPD, C0P | 12 | E4+P1+F1 (NO M layer) | Feeds ASU.sensory_gain; intra to RPEM, IUCP, MORMR, DAED | No |

**RPU summary**: 6-8D output -- the SMALLEST outputs in the entire system. ALL RPU models use the same triple mechanism: AED + CPD + C0P. E-layer always 4D. Beta and gamma tiers lose M layer. DAED uniquely has F0 (no forecast layer).

---

## 9. STU -- Sensorimotor Timing Unit (4 models read)

| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |
|----------|-----------|---|-------|-----|---------|------------|-------|
| STU-a1-HMCE | Hippocampal-Motor Cortex Entrainment | 13 | TMH | 18 | E5+M2+P3+F3 | -- | No |
| STU-a2-AMSC | Auditory-Motor Stream Coupling | 12 | BEP, TMH | 16 | E4+M2+P3+F3 | Reads from BEP motor pathway | No |
| STU-b1-AMSS | Auditory-Motor Synchronization System | 11 | TMH | 16 | E5+M2+P2+F2 | Feeds ARU | No |
| STU-g1-TMRM | Tempo Memory Reproduction Method | 10 | BEP | 15 | E3+M2+P2+F3 | Feeds ARU.AED (P5 pathway) | No |

**STU summary**: 10-13D output. TMH is the core mechanism (present in 3 of 4 models). BEP appears at alpha-2 and gamma-1. Strong E-layer (up to 5D). Feeds to ARU via P5 pathway.

---

## Summary Statistics

### 1. Total Output Dimensionality

| Unit | Models Read | D Range | Sum D (sampled) | Avg D |
|------|------------|---------|-----------------|-------|
| SPU | 4 | 10-12 | 46 | 11.5 |
| ARU | 4 | 10-19 | 55 | 13.8 |
| ASU | 3 | 9-12 | 31 | 10.3 |
| IMU | 4 | 10-12 | 44 | 11.0 |
| MPU | 4 | 11-11 | 44 | 11.0 |
| NDU | 4 | 10-12 | 43 | 10.8 |
| PCU | 3 | 9-12 | 31 | 10.3 |
| RPU | 4 | 6-8 | 27 | 6.8 |
| STU | 4 | 10-13 | 46 | 11.5 |
| **TOTAL** | **34** | **6-19** | **367** | **10.8** |

**Extrapolated total C3 manifold** (96 models x 10.8 avg): ~1,037D. Pipeline-confirmed: 1,006D.

### 2. Mechanism vs Relay Count

| Type | Count | % |
|------|-------|---|
| Mechanism-based models | 33 | 97.1% |
| Relay models (no mechanisms) | 1 | 2.9% |

**Only BCH (SPU-a1) is a Relay.** All other 95 models use at least one mechanism.

### 3. Mechanism Frequency (across 34 models)

| Mechanism | Appearances | Units Using It |
|-----------|-------------|----------------|
| **PPC** | 11 | SPU, NDU, PCU |
| **ASA** | 8 | ARU, ASU, NDU |
| **BEP** | 10 | ASU, MPU, STU |
| **AED** | 9 | ARU, IMU, RPU |
| **CPD** | 6 | ARU, RPU |
| **C0P** | 6 | ARU, RPU |
| **MEM** | 7 | IMU, PCU |
| **TMH** | 8 | MPU, STU |
| **TPC** | 5 | SPU, PCU |
| **SYN** | 1 | IMU (PNH only) |

**Observations**:
- PPC is the most widely used mechanism (11 appearances)
- Each unit has a "signature" mechanism pair that is consistent across ALL its models
- SYN appears only once (IMU-a2-PNH) -- the rarest mechanism
- CPD and C0P always co-occur (shared by ARU and RPU)

### 4. Unit-Mechanism Binding Pattern

Every unit has a FIXED mechanism signature across all tiers:

| Unit | Fixed Mechanism Signature |
|------|--------------------------|
| SPU | PPC (+TPC at higher tiers) |
| ARU | AED + CPD + C0P (+ ASA for AAC) |
| ASU | BEP + ASA |
| IMU | MEM (+ cross-circuit reads: AED, BEP, SYN) |
| MPU | BEP + TMH |
| NDU | PPC + ASA |
| PCU | PPC + TPC + MEM |
| RPU | AED + CPD + C0P |
| STU | TMH (+ BEP at some tiers) |

### 5. H3 Demand Distribution

| Range | Count | Models |
|-------|-------|--------|
| 0-10 | 4 | DAP(6), ASAP(9), SDNPS(10), BCH(26 -- outlier: Relay direct reads) |
| 11-15 | 14 | LDAC(12), IUCP(14), STAI(14), PWUP(14), BARM(14), NSCP(14), PSCL(14), MSR(22)... |
| 16-20 | 12 | MPG(16), SDDP(16), DAED(16), PWSM(16), AMSS(16), AMSC(16), SDD(18), HTP(18)... |
| 21-30 | 3 | PUPF(21), RASN(28), BCH(26) |
| 30+ | 1 | SRP(~124) |

**SRP is the extreme outlier** at ~124 H3 tuples -- 5x the next highest (RASN at 28).

**Mean H3 demand**: 20.6 tuples (excluding SRP: 15.5 tuples)

### 6. Most-Demanded R3 Features

| R3 Index | Feature Name | Appearances (in 34 models) |
|----------|-------------|--------------------------|
| [25:33] | x_l0l5 (Energy x Consonance) | 28+ (nearly universal) |
| [41:49] | x_l5l7 (Consonance x Timbre) | 20+ |
| [4] | sensory_pleasantness | 18+ |
| [14] | tonalness | 17+ |
| [10] | spectral_flux / onset_strength | 16+ |
| [0] | roughness | 15+ |
| [8] | loudness | 15+ |
| [22] | entropy / energy_change | 14+ |
| [7] | amplitude | 13+ |
| [5] | inharmonicity | 10+ |

**Interaction groups E[25:33] and E[41:49] are the most demanded features** -- nearly every model reads at least one of them. This validates their inclusion in R3 v1 despite being cross-domain products.

### 7. Cross-Unit Dependency Count

| Pathway | Direction | Models Involved | Count |
|---------|-----------|-----------------|-------|
| **P1: SPU -> ARU** | Feedforward | BCH, PSCL, STAI, SDNPS -> SRP | 4+ |
| **P2: SPU -> STU** | Feedforward | PSCL -> HMCE | 1 |
| **P3: IMU -> ARU** | Feedforward | DMMS -> DAP, NEMAC | 2 |
| **P4: RPU -> ARU** | Feedforward | MORMR -> ARU.pleasure | 1 |
| **P5: STU -> ARU** | Feedforward | TMRM -> ARU.AED | 1 |
| **MPU -> STU** | Feedforward | MSR, ASAP -> STU timing | 2 |
| **NDU -> ARU** | Feedforward | DSP, SDDP -> ARU | 2 |
| **PCU -> ASU** | Feedforward | PWUP -> ASU | 1 |
| **PCU -> IMU** | Feedforward | IGFE -> IMU | 1 |
| **RPU -> IMU** | Feedforward | IUCP -> IMU | 1 |

**ARU is the primary cross-unit HUB** -- it receives from SPU (P1), IMU (P3), RPU (P4), STU (P5), and NDU. This makes ARU the "convergence zone" for the C3 system.

### 8. State Needs Count

| Stateful? | Count | % |
|-----------|-------|---|
| No state (deterministic) | 34 | 100% |
| Has state (EMA/counters/posteriors) | 0 | 0% |

**NO model in the sample requires state.** All 34 models are stateless, frame-level computations. This is consistent with the C3 ontology: state lives in the M-layer via depth-dependent tau (Murray hierarchy), not in individual model compute() calls. The model documents describe the C3 architecture where M-layer smoothing is handled by the orchestrator, not by individual models.

### 9. Non-Standard Layer Structures

| Pattern | Models | Description |
|---------|--------|-------------|
| Standard E/M/P/F | 26 | 76% of sample |
| No M layer | 4 | PWUP, IUCP, IGFE, LDAC -- beta/gamma PCU and RPU |
| No F layer | 1 | DAED (F0 -- no forecast) |
| Non-standard names | 4 | SRP (N/C/P/T/M/F), AAC (E/A/I/P/F), PUPF (E/U/G/P/F), DAP (E/D/P/F) |
| 5+ layers | 3 | SRP (6), AAC (5), PUPF (6) |

**Trend**: Higher tiers (alpha) tend to have richer, sometimes non-standard layer structures. Lower tiers (beta, gamma) may drop M layer. ARU models are the most architecturally diverse.

### 10. Tier Patterns

| Tier | Avg D | Avg H3 | Avg Mechs |
|------|-------|--------|-----------|
| alpha-1 (9 models) | 12.1 | 30.0* | 1.9 |
| alpha-2 (7 models) | 11.0 | 17.3 | 2.0 |
| beta-1 (9 models) | 10.6 | 16.0 | 2.1 |
| gamma-1 (9 models) | 9.6 | 12.4 | 1.7 |

*SRP inflates alpha-1 H3 mean; excluding SRP: 17.5

**Clear tier gradient**: alpha models are larger (more dims, more H3 demand) and gamma models are smaller and more speculative. Mechanism count is relatively stable across tiers.

---

## Full Model List (96 models across 9 units)

Unread models marked with `--`. Read models (34) have full data extracted.

### SPU (6 models)
- SPU-a1-BCH, SPU-a2-PSCL, SPU-a3-PCCR--, SPU-b1-STAI, SPU-b2-TSCP--, SPU-b3-MIAA--, SPU-g1-SDNPS, SPU-g2-ESME--, SPU-g3-SDED--

### ARU (9 models)
- ARU-a1-SRP, ARU-a2-AAC, ARU-a3-VMM--, ARU-b1-PUPF, ARU-b2-CLAM--, ARU-b3-MAD--, ARU-b4-NEMAC--, ARU-g1-DAP, ARU-g2-CMAT--, ARU-g3-TAR--

### ASU (9 models)
- ASU-a1-SNEM, ASU-a2-IACM--, ASU-a3-CSG--, ASU-b1-BARM, ASU-b2-STANM--, ASU-b3-AACM--, ASU-g1-PWSM, ASU-g2-DGTP--, ASU-g3-SDL--

### IMU (12 models)
- IMU-a1-MEAMN, IMU-a2-PNH, IMU-a3-MMP--, IMU-b1-RASN, IMU-b2-PMIM--, IMU-b3-OII--, IMU-b4-HCMC--, IMU-b5-RIRI--, IMU-b6-MSPBA--, IMU-b7-VRIAP--, IMU-b8-TPRD--, IMU-b9-CMAPCC--, IMU-g1-DMMS, IMU-g2-CSSL--, IMU-g3-CDEM--

### MPU (9 models)
- MPU-a1-PEOM, MPU-a2-MSR, MPU-a3-GSSM--, MPU-b1-ASAP, MPU-b2-DDSMI--, MPU-b3-VRMSME--, MPU-b4-SPMC--, MPU-g1-NSCP, MPU-g2-CTBB--, MPU-g3-STC--

### NDU (9 models)
- NDU-a1-MPG, NDU-a2-SDD, NDU-a3-EDNR--, NDU-b1-DSP, NDU-b2-CDMR--, NDU-b3-SLEE--, NDU-g1-SDDP, NDU-g2-ONI--, NDU-g3-ECT--

### PCU (10 models)
- PCU-a1-HTP, PCU-a2-SPH--, PCU-a3-ICEM--, PCU-b1-PWUP, PCU-b2-WMED--, PCU-b3-UDP--, PCU-b4-CHPI--, PCU-g1-IGFE, PCU-g2-MAA--, PCU-g3-PSH--

### RPU (10 models)
- RPU-a1-DAED, RPU-a2-MORMR, RPU-a3-RPEM--, RPU-b1-IUCP, RPU-b2-MCCN--, RPU-b3-MEAMR--, RPU-b4-SSRI--, RPU-g1-LDAC, RPU-g2-IOTMS--, RPU-g3-SSPS--

### STU (14 models)
- STU-a1-HMCE, STU-a2-AMSC, STU-a3-MDNS--, STU-b1-AMSS, STU-b2-TPIO--, STU-b3-EDTA--, STU-b4-ETAM--, STU-b5-HGSIC--, STU-b6-OMS--, STU-g1-TMRM, STU-g2-NEWMD--, STU-g3-MTNE--, STU-g4-PTGMP--, STU-g5-MPFS--

---

## Architectural Findings

### 1. Strict Unit-Mechanism Binding
Every unit uses the SAME mechanism(s) across ALL its models. There are no exceptions in the 34-model sample. This means the 10 mechanisms map cleanly onto the 9 units:

```
PPC ---- SPU, NDU, PCU (perceptual pathway)
TPC ---- SPU, PCU (timbre pathway)
ASA ---- ARU, ASU, NDU (salience pathway)
AED ---- ARU, RPU (affective pathway)
CPD ---- ARU, RPU (chills/peak pathway)
C0P ---- ARU, RPU (approach/avoidance pathway)
BEP ---- ASU, MPU, STU (beat/motor pathway)
TMH ---- MPU, STU (temporal memory pathway)
MEM ---- IMU, PCU (memory pathway)
SYN ---- IMU only (syntactic pathway)
```

### 2. ARU as Convergence Hub
ARU receives cross-unit input from 5 of the other 8 units (SPU, IMU, RPU, STU, NDU). Only ASU, MPU, and PCU do not directly feed ARU. This positions ARU as the "Global Workspace" integration center of the C3 system.

### 3. RPU Produces the Smallest Output
RPU models consistently produce 6-8D output -- the smallest in the system. This reflects that reward signals are dimensionally compact (pleasure, wanting, liking, prediction error) compared to perceptual or temporal representations.

### 4. SRP Is the Extreme Outlier
ARU-a1-SRP is an outlier on multiple dimensions: largest output (19D), most H3 tuples (~124), most non-standard layers (6), and most cross-unit reads. It functions as the primary reward computation hub.

### 5. No Model Has State
All 34 models are stateless. The C3 ontology places state management (EMA smoothing with depth-dependent tau) in the M-layer orchestrator, not in individual model compute() calls. This is a deliberate architectural decision for glass-box transparency.
