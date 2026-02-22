# F10 Clinical & Therapeutic -- Collections

> **NOTE**: This file was built by independently reading each model doc
> in the primary function mechanism directories and cross-referencing the F10 data specification.
> It does NOT copy from the orchestrator or ontology summaries.
> Counts and dimensions are snapshots -- they will change as models are integrated.

---

## 1. Verified F10 Models (from Model Docs)

Independent scan of all 10 mechanism model doc sets identified
**10 models** for F10 (Clinical & Therapeutic) with **0 secondary** cross-function models.
F10 is a **META-LAYER** -- evidence-only, NO beliefs, NO relay.
Critically, F10 has NO dedicated unit -- all models are cross-unit:
IMU (Integrative Memory Unit, 4 models), MPU (Motor Processing Unit, 2 models),
ARU (Affective Response Unit, 3 models), and NDU (Neural Dynamics Unit, 1 model).
Output dimensions range from 10D to 12D. DSP is the only F10-primary model.

### 1.1 Implemented (0 models)

No F10 models are currently implemented. F10 is evidence-only (meta-layer, deferred).
F10 mechanism code is a stub (no `brain/functions/f10/` directory exists yet).

### 1.2 Not Yet Implemented (10 models)

| Model | Unit-Tier | Doc OUTPUT_DIM | H3 (v1) | Primary Fn | Status |
|-------|-----------|----------------|---------|-----------|--------|
| MMP | IMU-a | 12D | 21 | F4 | pending |
| RASN | IMU-b | 11D | 28 | F4 | pending |
| RIRI | IMU-b | 10D | 16 | F4 | pending |
| VRIAP | IMU-b | 10D | 18 | F4 | pending |
| GSSM | MPU-a | 11D | 12 | F7 | pending |
| VRMSME | MPU-b | 11D | 12 | F7 | pending |
| CLAM | ARU-b | 11D | 12 | F5 | pending |
| MAD | ARU-b | 11D | 9 | F5 | pending |
| TAR | ARU-g | 10D | 21 | F5 | pending |
| DSP | NDU-b | 12D | 18 | F10 | pending |

### 1.3 Full Model Descriptions

| Model | Full Name | Evidence Tier | Key Mechanism |
|-------|-----------|---------------|---------------|
| MMP | Music Memory Preservation | alpha (>90%) | Spared procedural/emotional music memory in Alzheimer's via SMA + hippocampal bypass |
| RASN | Rhythmic Auditory Stimulation Neuroplasticity | beta (70-90%) | RAS-driven gait entrainment plasticity in stroke and Parkinson's (Thaut 2015) |
| RIRI | Rhythm-Induced Rehabilitation Integration | beta (70-90%) | Multi-modal rhythmic rehabilitation synergy across motor domains |
| VRIAP | VR-Integrated Analgesic Processing | beta (70-90%) | Virtual reality + music analgesia via descending pain modulation |
| GSSM | Gait-Sound Synchronization Model | alpha (>90%) | Tempo-locked gait entrainment, step variability reduction (Dalla Bella 2017) |
| VRMSME | VR-Music Sensorimotor Enhancement | beta (70-90%) | VR-music combined motor enhancement beyond single-modality rehabilitation |
| CLAM | Closed-Loop Affect Modulation | beta (70-90%) | EEG-music BCI for real-time affect regulation (Daly 2016) |
| MAD | Musical Anhedonia Dissociation | beta (70-90%) | Reward circuit lesion patterns in specific musical anhedonia (Mas-Herrero 2014) |
| TAR | Therapeutic Auditory Resonance | gamma (50-70%) | Therapeutic resonance across emotion and reward pathways |
| DSP | Deviance Salience Processing | beta (70-90%) | Clinical deviance detection in altered neural contexts, attention pathway modulation |

### 1.4 Cross-Function -- Secondary Models Contributing to F10

F10 has **NO secondary cross-function models**. All 10 models are primary contributors
from their home functions (F4, F5, F7, F10) that produce F10-relevant evidence as
cross-function output feeding INTO F1-F9 observe().

### 1.5 Cross-Function Assignment

F10 is unique as a meta-layer: NO dedicated unit, NO beliefs, NO relay. All 10 models
reside in units belonging to other functions. DSP is the only F10-primary model.

| Primary Function | Models | Count |
|-----------------|--------|-------|
| F4 Memory (via IMU) | MMP, RASN, RIRI, VRIAP | 4 |
| F5 Emotion (via ARU) | CLAM, MAD, TAR | 3 |
| F7 Motor (via MPU) | GSSM, VRMSME | 2 |
| F10 Clinical (via NDU) | DSP | 1 |

F10 models feed evidence INTO their receiving functions:
- **F3 Attention**: DSP (deviance salience in clinical context)
- **F4 Memory**: MMP (preservation context for autobiographical_retrieval)
- **F5 Emotion**: VRIAP (pain modulation valence), CLAM (closed-loop affect), TAR (therapeutic resonance)
- **F6 Reward**: MAD (anhedonia lesion), TAR (therapeutic resonance)
- **F7 Motor**: RASN (RAS plasticity), RIRI (multi-modal synergy), GSSM (gait variability), VRMSME (VR enhancement)

---

## 2. Implementation Summary

```
Implemented:     0 models (F10 is evidence-only, meta-layer)
Pending:         10 models (MMP, RASN, RIRI, VRIAP, GSSM, VRMSME, CLAM, MAD, TAR, DSP)
Cross-function:  0 models (F10 has no secondary contributors)

Current code:    0D mechanism output (no relay, no mechanism code)
                 0 F10 beliefs (meta-layer -- 0 by design)
                 0 H3 demands (none implemented)

Full F10 total:  119D mechanism output (all 10 models)
                 0 beliefs (meta-layer -- evidence only)
                 167 H3 demands (all 10 models)
```

---

## 3. Belief Inventory

**F10 has 0 beliefs.** As a meta-layer, F10 produces evidence signals only.
Evidence feeds unidirectionally INTO F1-F9 observe() -- it does not maintain
its own belief state, precision tracking, or prediction error history.

---

## 4. Clinical Domain Pipeline

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
             |
             v
 [Neurodegeneration]
   MMP    (12D, IMU-a)    <- music memory preservation -> F4
 [Motor Rehabilitation]
   RASN   (11D, IMU-b)    <- RAS neuroplasticity -> F7
   RIRI   (10D, IMU-b)    <- rhythm rehab integration -> F7
   GSSM   (11D, MPU-a)    <- gait-sound synchronization -> F7
   VRMSME (11D, MPU-b)    <- VR-music motor enhancement -> F7
 [Pain & Affect]
   VRIAP  (10D, IMU-b)    <- VR-integrated analgesia -> F5
   CLAM   (11D, ARU-b)    <- closed-loop affect -> F5
   MAD    (11D, ARU-b)    <- musical anhedonia -> F6
   TAR    (10D, ARU-g)    <- therapeutic resonance -> F5/F6
   DSP    (12D, NDU-b)    <- deviance salience -> F3
```

**Clinical domain rationale**:
F10 models organize into 3 clinical domains rather than a depth-ordered DAG.
Within each domain, models share neural circuits and evidence pathways:
- Neurodegeneration: hippocampal bypass, SMA preservation
- Motor Rehabilitation: basal ganglia, cerebellum, premotor entrainment
- Pain & Affect: PAG, ACC, insula, NAcc, prefrontal

Within-unit depth ordering (alpha before beta before gamma) applies:
- IMU: MMP (a) feeds context to RASN, RIRI, VRIAP (all b)
- MPU: GSSM (a) feeds context to VRMSME (b)
- ARU: CLAM (b) and MAD (b) in parallel; TAR (g) reads from both

---

## 5. Unit Distribution

| Unit | Models | Count |
|------|--------|-------|
| IMU (Integrative Memory Unit) | MMP, RASN, RIRI, VRIAP | 4 |
| MPU (Motor Processing Unit) | GSSM, VRMSME | 2 |
| ARU (Affective Response Unit) | CLAM, MAD, TAR | 3 |
| NDU (Neural Dynamics Unit) | DSP | 1 |

IMU leads (4/10 models), reflecting the dominance of memory-clinical intersections:
preserved memory in neurodegeneration (MMP), rhythmic stimulation plasticity (RASN),
multi-modal rehabilitation (RIRI), and VR-pain modulation via memory circuits (VRIAP).
ARU follows with 3 models covering affect-clinical applications.
MPU contributes 2 motor rehabilitation models.
NDU contributes 1 model (DSP) -- the only F10-primary.

---

## 6. H3 Demands (all models)

| Model | H3 Tuples (v1) | Primary Fn | Status |
|-------|----------------|-----------|--------|
| MMP | 21 | F4 | doc only |
| RASN | 28 | F4 | doc only |
| RIRI | 16 | F4 | doc only |
| VRIAP | 18 | F4 | doc only |
| GSSM | 12 | F7 | doc only |
| VRMSME | 12 | F7 | doc only |
| CLAM | 12 | F5 | doc only |
| MAD | 9 | F5 | doc only |
| TAR | 21 | F5 | doc only |
| DSP | 18 | F10 | doc only |

Total H3 demands from all F10 models: **167 tuples**.
Implemented: **0 tuples** (F10 is evidence-only).

RASN has the highest H3 demand (28 tuples), reflecting the multi-scale temporal tracking
required for rhythmic auditory stimulation neuroplasticity. MAD is most compact (9 tuples),
consistent with its focused reward-circuit lesion architecture.

---

## 7. Next Steps

- [ ] Create DSP mechanism layer docs (e_layer.md, m_layer.md, p_layer.md, f_layer.md) in mechanisms/dsp/
- [ ] Verify MMP, RASN, RIRI, VRIAP mechanism docs exist in F4-Memory-Systems/mechanisms/
- [ ] Verify GSSM, VRMSME mechanism docs exist in F7-Motor-and-Timing/mechanisms/
- [ ] Verify CLAM, MAD, TAR mechanism docs exist in F5-Emotion-and-Valence/mechanisms/
- [ ] Define evidence signal routes (F10 -> F1-F9 observe()) during integration phase
- [ ] Create DSP model code in brain/functions/f10/ (if F10 code module is created)
