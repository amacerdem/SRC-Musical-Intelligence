# F10 -- Clinical & Therapeutic

**Function**: F10 Clinical & Therapeutic
**Type**: META-LAYER -- evidence-only, NO beliefs, NO relay
**Models**: 10 total (all cross-unit: IMU 4, MPU 2, ARU 3, NDU 1) + 0 secondary
**Beliefs**: 0 (meta-layer -- evidence feeds INTO F1-F9 observe())
**Total output**: 119D (MMP 12D + RASN 11D + RIRI 10D + VRIAP 10D + GSSM 11D + VRMSME 11D + CLAM 11D + MAD 11D + TAR 10D + DSP 12D)
**H3 demands**: 167 tuples total (MMP 21, RASN 28, RIRI 16, VRIAP 18, GSSM 12, VRMSME 12, CLAM 12, MAD 9, TAR 21, DSP 18)
**Phase**: meta (deferred -- evidence-only)
**Relay**: NONE -- F10 is a meta-layer with no dedicated relay
**Implemented**: no F10 mechanism models yet

---

## 1. What F10 Does

F10 processes the CLINICAL AND THERAPEUTIC dimension of music -- neurodegeneration, motor rehabilitation, pain modulation, affect regulation, and brain-computer interface applications. It captures how music engages preserved neural pathways in clinical populations: spared musical memory in Alzheimer's, rhythmic auditory stimulation for gait in Parkinson's and stroke, closed-loop affect modulation for pain and anhedonia, and deviance detection in clinical contexts.

F10 is a **META-LAYER** -- it has **NO beliefs** and **NO relay**. All 10 models produce evidence that feeds unidirectionally INTO F1-F9 observe() via cross-function signal routes. This architecture reflects that clinical/therapeutic phenomena are not separate cognitive processes but rather modulations of the same F1-F9 machinery under altered neural conditions: preserved memory (F4), rehabilitated motor timing (F7), modulated emotion (F5), gated reward (F6), and redirected attention (F3).

F10 has **NO dedicated unit**. Its 10 models are distributed across 4 units belonging to other functions: IMU (Integrative Memory Unit, 4 models), MPU (Motor Processing Unit, 2 models), ARU (Affective Response Unit, 3 models), and NDU (Neural Dynamics Unit, 1 model). DSP is the only model whose mechanism docs live in F10; the other 9 are documented in their primary function directories (F4, F5, F7).

### Clinical Domains

1. **Neurodegeneration**: MMP (Alzheimer's music memory preservation)
2. **Motor Rehabilitation**: RASN, RIRI, GSSM, VRMSME (stroke, Parkinson's, gait)
3. **Pain & Affect**: VRIAP, CLAM, MAD, TAR, DSP (analgesia, anhedonia, affect regulation, BCI)

### Key Neuroscience Circuits

- **Preserved Musical Memory**: SMA + hippocampal bypass -> spared procedural/emotional music memory in Alzheimer's (Jacobsen 2015, Baird 2018)
- **Rhythmic Auditory Stimulation**: Basal ganglia + cerebellum + premotor -> tempo-locked gait entrainment in Parkinson's and stroke (Thaut 2015, Dalla Bella 2017)
- **Pain Modulation**: PAG + ACC + insula -> music-induced analgesia via descending pain modulation (Garza-Villarreal 2014, Roy 2008)
- **Affective BCI**: Prefrontal + amygdala -> closed-loop EEG-music affect regulation (Daly 2016, Ramirez 2015)
- **Anhedonia Circuitry**: NAcc + VTA + mPFC -> reward circuit lesion patterns in musical anhedonia (Mas-Herrero 2014, Martinez-Molina 2016)

```
Audio -> R3 (97D) ---+--------------------------------------------
H3 tuples -----------+
                     |
                     v
 [Neurodegeneration]  MMP    (12D, IMU-a)    <- music memory preservation
 [Motor Rehab]        RASN   (11D, IMU-b)    <- rhythmic auditory stimulation neuroplasticity
                      RIRI   (10D, IMU-b)    <- rhythm-induced rehabilitation integration
                      GSSM   (11D, MPU-a)    <- gait-sound synchronization model
                      VRMSME (11D, MPU-b)    <- VR-music sensorimotor enhancement
 [Pain & Affect]      VRIAP  (10D, IMU-b)    <- VR-integrated analgesic processing
                      CLAM   (11D, ARU-b)    <- closed-loop affect modulation
                      MAD    (11D, ARU-b)    <- musical anhedonia dissociation
                      TAR    (10D, ARU-g)    <- therapeutic auditory resonance
                      DSP    (12D, NDU-b)    <- deviance salience processing
                     |
                     v
         Evidence -> F1-F9 observe() (unidirectional)
```

---

## 2. Complete Model Inventory

| # | Model | Unit | Tier | Output | H3 | Primary Fn | Status |
|---|-------|------|------|--------|-----|-----------|--------|
| 1 | **MMP** | IMU | a | 12D | 21 | F4 | pending |
| 2 | **RASN** | IMU | b | 11D | 28 | F4 | pending |
| 3 | **RIRI** | IMU | b | 10D | 16 | F4 | pending |
| 4 | **VRIAP** | IMU | b | 10D | 18 | F4 | pending |
| 5 | **GSSM** | MPU | a | 11D | 12 | F7 | pending |
| 6 | **VRMSME** | MPU | b | 11D | 12 | F7 | pending |
| 7 | **CLAM** | ARU | b | 11D | 12 | F5 | pending |
| 8 | **MAD** | ARU | b | 11D | 9 | F5 | pending |
| 9 | **TAR** | ARU | g | 10D | 21 | F5 | pending |
| 10 | **DSP** | NDU | b | 12D | 18 | F10 | pending |

9/10 models have mechanism layer docs in their primary function directories:
- **MMP**: `F4-Memory-Systems/mechanisms/mmp/`
- **RASN**: `F4-Memory-Systems/mechanisms/rasn/`
- **RIRI**: `F4-Memory-Systems/mechanisms/riri/`
- **VRIAP**: `F4-Memory-Systems/mechanisms/vriap/`
- **GSSM**: `F7-Motor-and-Timing/mechanisms/gssm/`
- **VRMSME**: `F7-Motor-and-Timing/mechanisms/vrmsme/`
- **CLAM**: `F5-Emotion-and-Valence/mechanisms/clam/`
- **MAD**: `F5-Emotion-and-Valence/mechanisms/mad/`
- **TAR**: `F5-Emotion-and-Valence/mechanisms/tar/`

1/10 models is F10-primary with docs in this directory:
- **DSP**: `F10-Clinical-and-Therapeutic/mechanisms/dsp/` (NEW -- pending layer docs)

---

## 3. Meta-Layer Architecture -- NO Beliefs

F10 is fundamentally different from F1-F9. It has **0 beliefs**, **0 Core**, **0 Appraisal**, **0 Anticipation**. There is no Bayesian update cycle, no precision engine, no prediction error tracking.

Instead, F10 models produce **evidence signals** that feed INTO F1-F9 observe() unidirectionally:

```
F10 Models -> F1-F9 Evidence Routes:
MMP    -> F4.autobiographical_retrieval   (preservation context)
RASN   -> F7.period_entrainment           (RAS plasticity)
RIRI   -> F7 Motor                        (multi-modal synergy)
VRIAP  -> F5 Emotion                      (pain modulation valence)
GSSM   -> F7.period_entrainment           (gait variability)
VRMSME -> F7 Motor                        (VR-music enhancement)
CLAM   -> F5 Emotion                      (closed-loop affect)
MAD    -> F6 Reward                       (anhedonia lesion)
TAR    -> F5/F6                           (therapeutic resonance)
DSP    -> F3 Attention                    (deviance in clinical context)
```

This evidence-only architecture means:
- No tau values (no Core beliefs)
- No precision tracking (no PE history)
- No relay wrapper (no kernel integration)
- No phase in the scheduler (meta-layer)
- All computation is deferred to the receiving F1-F9 beliefs

---

## 4. Dependency Graph

```
                R3 (97D) + H3
                    |
    +---+---+---+---+---+---+---+---+---+---+
    v   v   v   v   v   v   v   v   v   v
   MMP RASN RIRI VRIAP GSSM VRMSME CLAM MAD TAR DSP
   12D 11D  10D  10D   11D   11D   11D  11D 10D 12D
   IMU IMU  IMU  IMU   MPU   MPU   ARU  ARU ARU NDU
    |   |    |    |     |     |     |    |   |   |
    v   v    v    v     v     v     v    v   v   v
   F4  F7   F7   F5    F7    F7    F5   F6  F5  F3
        |                                   F6
        Evidence -> F1-F9 observe()
```

### Key Dependencies

| Model | Reads From |
|-------|-----------|
| MMP (IMU-a) | R3/H3 + upstream MEAMN memory outputs (IMU) |
| RASN (IMU-b) | R3/H3 + upstream MMP, MEAMN outputs (IMU) |
| RIRI (IMU-b) | R3/H3 + upstream MMP, MEAMN outputs (IMU) |
| VRIAP (IMU-b) | R3/H3 + upstream MMP, MEAMN outputs (IMU) |
| GSSM (MPU-a) | R3/H3 + upstream PEOM motor outputs (MPU) |
| VRMSME (MPU-b) | R3/H3 + upstream GSSM, PEOM outputs (MPU) |
| CLAM (ARU-b) | R3/H3 + upstream SRP affect outputs (ARU) |
| MAD (ARU-b) | R3/H3 + upstream SRP, DAED outputs (ARU) |
| TAR (ARU-g) | R3/H3 + upstream CLAM, MAD, SRP outputs (ARU) |
| DSP (NDU-b) | R3/H3 + upstream MPG outputs (NDU) |

### Cross-Function Evidence Flow

F10 models feed evidence into F1-F9 unidirectionally:
- **F3 Attention**: DSP deviance salience context
- **F4 Memory**: MMP music memory preservation signals
- **F5 Emotion**: VRIAP pain valence, CLAM closed-loop affect, TAR therapeutic resonance
- **F6 Reward**: MAD anhedonia lesion evidence, TAR therapeutic reward
- **F7 Motor**: RASN rhythmic plasticity, RIRI multi-modal synergy, GSSM gait variability, VRMSME VR enhancement

---

## 5. Unit Architecture

### IMU -- Integrative Memory Unit (4 F10 models)

IMU houses 4 of 10 F10 models (MMP, RASN, RIRI, VRIAP). All capture the memory-clinical intersection:
MMP models preserved musical memory in neurodegeneration, RASN models rhythmic auditory stimulation neuroplasticity, RIRI models rhythm-induced rehabilitation integration, and VRIAP models VR-integrated analgesic processing via memory-pain pathways.

```
IMU models in F10:  MMP (a) --- RASN (b) --- RIRI (b) --- VRIAP (b)
                    memory      RAS          rhythm        VR pain
                    preservation plasticity  rehab         analgesia
```

### MPU -- Motor Processing Unit (2 F10 models)

MPU contributes 2 models to F10: GSSM (gait-sound synchronization, alpha) and VRMSME (VR-music sensorimotor enhancement, beta). Both capture motor rehabilitation through music-driven entrainment.

```
MPU models in F10:  GSSM (a) --- VRMSME (b)
                    gait sync    VR-motor
                    model        enhancement
```

### ARU -- Affective Response Unit (3 F10 models)

ARU contributes 3 models to F10: CLAM (closed-loop affect modulation, beta), MAD (musical anhedonia dissociation, beta), and TAR (therapeutic auditory resonance, gamma). These cover affect-clinical applications from BCI to anhedonia to therapeutic resonance.

```
ARU models in F10:  CLAM (b) --- MAD (b) --- TAR (g)
                    closed-loop  anhedonia   therapeutic
                    affect       dissociation resonance
```

### NDU -- Neural Dynamics Unit (1 F10 model)

NDU contributes 1 model to F10: DSP (deviance salience processing, beta). This is the only F10-primary model -- its mechanism docs reside in this directory.

```
NDU models in F10:  DSP (b)
                    deviance
                    salience
```

---

## 6. Documentation Structure

```
F10-Clinical-and-Therapeutic/
+-- 0_F10-orchestrator.md                  <- this file
+-- collections.md                         <- full model inventory
+-- mechanisms/
    +-- 0_mechanisms-orchestrator.md       <- cross-references + DSP summary
    +-- dsp/                              <- DSP mechanism layer docs (NEW, pending)
```

**NOTE**: F10 has NO beliefs directory -- meta-layers have 0 beliefs.
9/10 models have their mechanism docs in their primary unit function directories:
- MMP, RASN, RIRI, VRIAP: `F4-Memory-Systems/mechanisms/`
- GSSM, VRMSME: `F7-Motor-and-Timing/mechanisms/`
- CLAM, MAD, TAR: `F5-Emotion-and-Valence/mechanisms/`

Only DSP has mechanism docs in this directory: `F10-Clinical-and-Therapeutic/mechanisms/dsp/`

**0 models implemented.** Pending: 1 a (MMP) + 1 a (GSSM) + 6 b (RASN, RIRI, VRIAP, VRMSME, CLAM, MAD, DSP) + 1 g (TAR) -- 167 H3 tuples total.
