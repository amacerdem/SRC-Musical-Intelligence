# F11 Development & Evolution -- Collections

> **NOTE**: This file was built by independently reading each model doc
> in the primary function mechanism directories and cross-referencing the F11 data specification.
> It does NOT copy from the orchestrator or ontology summaries.
> Counts and dimensions are snapshots -- they will change as models are integrated.

---

## 1. Verified F11 Models (from Model Docs)

Independent scan of all 6 mechanism model doc sets identified
**6 models** for F11 (Development & Evolution) with **0 secondary** cross-function models.
F11 is a **META-LAYER** -- evidence-only, NO beliefs, NO relay.
Critically, F11 has NO dedicated unit -- all models are cross-unit:
NDU (Neural Dynamics Unit, 3 models), IMU (Integrative Memory Unit, 2 models),
and ARU (Affective Response Unit, 1 model).
Output dimensions range from 9D to 12D. SDDP and ONI are F11-primary models.

### 1.1 Implemented (0 models)

No F11 models are currently implemented. F11 is evidence-only (meta-layer, deferred).
F11 mechanism code is a stub (no `brain/functions/f11/` directory exists yet).

### 1.2 Not Yet Implemented (6 models)

| Model | Unit-Tier | Doc OUTPUT_DIM | H3 (v1) | Primary Fn | Status |
|-------|-----------|----------------|---------|-----------|--------|
| DAP | ARU-g | 10D | 6 | F11 | pending |
| DMMS | IMU-g | 10D | 15 | F11 | pending |
| CSSL | IMU-g | 10D | 15 | F11 | pending |
| SDDP | NDU-g | 10D | 16 | F11 | pending |
| ONI | NDU-g | 11D | 16 | F11 | pending |
| DSP | NDU-b | 12D | 18 | F10 | pending |

### 1.3 Full Model Descriptions

| Model | Full Name | Evidence Tier | Key Mechanism |
|-------|-----------|---------------|---------------|
| DAP | Developmental Affective Plasticity | gamma (50-70%) | Lifespan changes in music-evoked emotional processing via amygdala + mPFC + insula plasticity |
| DMMS | Developmental Music Memory Scaffold | gamma (50-70%) | Developmental trajectory of musical memory encoding from infancy through adulthood (Trainor 2005) |
| CSSL | Cross-Species Song Learning | gamma (50-70%) | Shared vocal learning circuits: HVC/RA/Area X (songbird) <-> Broca's/SMA/BG (human) (Jarvis 2004) |
| SDDP | Sex-Dependent Developmental Plasticity | gamma (50-70%) | Sex-differentiated cortical auditory development in Heschl's gyrus + planum temporale (Hyde 2008) |
| ONI | Over-Normalization in Intervention | gamma (50-70%) | Intervention-driven over-regularization of natural variability via prefrontal + basal ganglia (Tervaniemi 2009) |
| DSP | Deviance Salience Processing | beta (70-90%) | Clinical deviance detection in altered neural contexts, attention pathway modulation |

### 1.4 Cross-Function -- Secondary Models Contributing to F11

F11 has **NO secondary cross-function models**. All 6 models are primary contributors
from their home functions (F4, F5, F10, F11) that produce F11-relevant evidence as
cross-function output feeding INTO F1-F9 observe().

### 1.5 Cross-Function Assignment

F11 is unique as a meta-layer: NO dedicated unit, NO beliefs, NO relay. All 6 models
reside in units belonging to other functions. SDDP and ONI are the only F11-primary models.

| Primary Function | Models | Count |
|-----------------|--------|-------|
| F5 Emotion (via ARU) | DAP | 1 |
| F4 Memory (via IMU) | DMMS, CSSL | 2 |
| F10 Clinical (via NDU) | DSP | 1 |
| F11 Development (via NDU) | SDDP, ONI | 2 |

F11 models feed evidence INTO their receiving functions:
- **F1 Sensory**: SDDP (sex-dependent auditory processing context)
- **F3 Attention**: DSP (deviance detection in developmental context)
- **F4 Memory**: DMMS (memory scaffold maturation), CSSL (evolutionary song learning)
- **F5 Emotion**: DAP (affective plasticity), SDDP (sex-dependent emotional processing)
- **F6 Reward**: ONI (over-normalization risk for reward calibration)
- **F8 Learning**: ONI (over-normalization risk for learning adaptation)

---

## 2. Implementation Summary

```
Implemented:     0 models (F11 is evidence-only, meta-layer)
Pending:         6 models (DAP, DMMS, CSSL, SDDP, ONI, DSP)
Cross-function:  0 models (F11 has no secondary contributors)

Current code:    0D mechanism output (no relay, no mechanism code)
                 0 F11 beliefs (meta-layer -- 0 by design)
                 0 H3 demands (none implemented)

Full F11 total:  63D mechanism output (all 6 models)
                 0 beliefs (meta-layer -- evidence only)
                 86 H3 demands (all 6 models)
```

---

## 3. Belief Inventory

**F11 has 0 beliefs.** As a meta-layer, F11 produces evidence signals only.
Evidence feeds unidirectionally INTO F1-F9 observe() -- it does not maintain
its own belief state, precision tracking, or prediction error history.

---

## 4. Developmental Domain Pipeline

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
             |
             v
 [Affective Development]
   DAP    (10D, ARU-g)    <- developmental affective plasticity -> F5
 [Memory Development]
   DMMS   (10D, IMU-g)    <- developmental music memory scaffold -> F4
   CSSL   (10D, IMU-g)    <- cross-species song learning -> F4
 [Neural Development]
   SDDP   (10D, NDU-g)    <- sex-dependent developmental plasticity -> F5/F1
   ONI    (11D, NDU-g)    <- over-normalization in intervention -> F6/F8
   DSP    (12D, NDU-b)    <- deviance salience processing -> F3
```

**Developmental domain rationale**:
F11 models organize into 3 developmental domains rather than a depth-ordered DAG.
Within each domain, models share neural circuits and developmental principles:
- Affective Development: amygdala, mPFC, insula plasticity across lifespan
- Memory Development: hippocampal maturation, evolutionary vocal learning circuits
- Neural Development: cortical auditory development, intervention-normalization dynamics

Within-unit tier ordering (alpha before beta before gamma) applies:
- ARU: DAP (g) is standalone
- IMU: DMMS (g) and CSSL (g) are parallel (both gamma)
- NDU: DSP (b) provides context; SDDP (g) and ONI (g) read from upstream NDU models

---

## 5. Unit Distribution

| Unit | Models | Count |
|------|--------|-------|
| ARU (Affective Response Unit) | DAP | 1 |
| IMU (Integrative Memory Unit) | DMMS, CSSL | 2 |
| NDU (Neural Dynamics Unit) | SDDP, ONI, DSP | 3 |

NDU leads (3/6 models), reflecting the dominance of neural development mechanisms
in the developmental/evolutionary domain: sex-dependent plasticity, over-normalization
dynamics, and deviance processing development. IMU contributes 2 memory-development
models. ARU contributes 1 affective development model.

---

## 6. H3 Demands (all models)

| Model | H3 Tuples (v1) | Primary Fn | Status |
|-------|----------------|-----------|--------|
| DAP | 6 | F11 | doc only |
| DMMS | 15 | F11 | doc only |
| CSSL | 15 | F11 | doc only |
| SDDP | 16 | F11 | doc only |
| ONI | 16 | F11 | doc only |
| DSP | 18 | F10 | doc only |

Total H3 demands from all F11 models: **86 tuples**.
Implemented: **0 tuples** (F11 is evidence-only).

DSP has the highest H3 demand (18 tuples), reflecting the multi-scale temporal tracking
required for deviance salience processing. DAP is most compact (6 tuples),
consistent with its focused affective developmental trajectory architecture.

---

## 7. Next Steps

- [ ] Create SDDP mechanism layer docs (e_layer.md, m_layer.md, p_layer.md, f_layer.md) in mechanisms/sddp/
- [ ] Create ONI mechanism layer docs (e_layer.md, m_layer.md, p_layer.md, f_layer.md) in mechanisms/oni/
- [ ] Verify DAP mechanism docs exist in F5-Emotion-and-Valence/mechanisms/dap/
- [ ] Verify DMMS mechanism docs exist in F4-Memory-Systems/mechanisms/dmms/
- [ ] Verify CSSL mechanism docs exist in F4-Memory-Systems/mechanisms/cssl/
- [ ] Verify DSP mechanism docs exist in F10-Clinical-and-Therapeutic/mechanisms/dsp/
- [ ] Define evidence signal routes (F11 -> F1-F9 observe()) during integration phase
- [ ] Create SDDP, ONI model code in brain/functions/f11/ (if F11 code module is created)
