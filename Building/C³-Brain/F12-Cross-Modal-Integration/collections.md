# F12 Cross-Modal Integration -- Collections

> **NOTE**: This file was built by independently reading each model doc
> in the primary function mechanism directories and cross-referencing the F12 data specification.
> It does NOT copy from the orchestrator or ontology summaries.
> Counts and dimensions are snapshots -- they will change as models are integrated.

---

## 1. Verified F12 Models (from Model Docs)

Independent scan of all 5 mechanism model doc sets identified
**5 models** for F12 (Cross-Modal Integration) with **0 secondary** cross-function models.
F12 is a **META-LAYER** -- evidence-only, NO beliefs, NO relay.
Critically, F12 has NO dedicated unit -- all models are cross-unit with maximal spread:
ARU (Affective Response Unit, 1 model), IMU (Integrative Memory Unit, 1 model),
PCU (Predictive Coding Unit, 1 model), ASU (Auditory Salience Unit, 1 model),
and NDU (Neural Dynamics Unit, 1 model).
Output dimensions range from 9D to 11D. CHPI and SDD have the highest H3 demands (20 and 18).

### 1.1 Implemented (0 models)

No F12 models are currently implemented. F12 is evidence-only (meta-layer, deferred).
F12 mechanism code is a stub (no `brain/functions/f12/` directory exists yet).

### 1.2 Not Yet Implemented (5 models)

| Model | Unit-Tier | Doc OUTPUT_DIM | H3 (v1) | Primary Fn | Status |
|-------|-----------|----------------|---------|-----------|--------|
| CMAT | ARU-g | 10D | 9 | F12 | pending |
| CMAPCC | IMU-b | 10D | 20 | F12 | pending |
| CHPI | PCU-b | 11D | 20 | F12 | pending |
| DGTP | ASU-g | 9D | 9 | F12 | pending |
| SDD | NDU-a | 11D | 18 | F12 | pending |

### 1.3 Full Model Descriptions

| Model | Full Name | Evidence Tier | Key Mechanism |
|-------|-----------|---------------|---------------|
| CMAT | Cross-Modal Affective Transfer | gamma (50-70%) | Music-evoked emotions transfer to visual/tactile domains via amygdala + STS + insula (Logeswaran & Bhatt 2012) |
| CMAPCC | Cross-Modal Action-Perception Common Code | beta (70-90%) | Shared motor-perceptual representations for music via mirror neuron system + SMA (Kohler 2002, Zatorre 2007) |
| CHPI | Cross-Modal Harmonic Predictive Integration | beta (70-90%) | Multimodal tonal prediction integration via STG + IPS + prefrontal convergence zones (Lee & Noppeney 2011) |
| DGTP | Domain-General Temporal Processing | gamma (50-70%) | Shared timing mechanisms across auditory, visual, and motor domains via BG + cerebellum (Grahn & Brett 2007) |
| SDD | Supramodal Deviance Detection | alpha (>90%) | Amodal surprise signals via frontal-temporal-parietal network transcending sensory channels (Escera 2014) |

### 1.4 Cross-Function -- Secondary Models Contributing to F12

F12 has **NO secondary cross-function models**. All 5 models are primary contributors
from their home functions (F2, F3, F5, F12) that produce F12-relevant evidence as
cross-function output feeding INTO F1-F9 observe().

### 1.5 Cross-Function Assignment

F12 is unique as a meta-layer: NO dedicated unit, NO beliefs, NO relay. All 5 models
reside in units belonging to other functions. F12 has maximal unit spread (1 model per unit
across 5 different units) -- the broadest distribution of any function.

| Primary Function | Models | Count |
|-----------------|--------|-------|
| F5 Emotion (via ARU) | CMAT | 1 |
| F4 Memory (via IMU) | CMAPCC | 1 |
| F2 Prediction (via PCU) | CHPI | 1 |
| F3 Attention (via ASU) | DGTP | 1 |
| F2 Prediction (via NDU) | SDD | 1 |

F12 models feed evidence INTO their receiving functions:
- **F2 Prediction**: CHPI (multimodal harmonic prediction), SDD (supramodal deviance)
- **F3 Attention**: DGTP (domain-general timing), SDD (supramodal deviance)
- **F4 Memory**: CMAPCC (action-perception common code, motor-memory bridge)
- **F5 Emotion**: CMAT (cross-modal affective transfer)
- **F7 Motor**: CMAPCC (action-perception common code), DGTP (cross-domain timing)

---

## 2. Implementation Summary

```
Implemented:     0 models (F12 is evidence-only, meta-layer)
Pending:         5 models (CMAT, CMAPCC, CHPI, DGTP, SDD)
Cross-function:  0 models (F12 has no secondary contributors)

Current code:    0D mechanism output (no relay, no mechanism code)
                 0 F12 beliefs (meta-layer -- 0 by design)
                 0 H3 demands (none implemented)

Full F12 total:  51D mechanism output (all 5 models)
                 0 beliefs (meta-layer -- evidence only)
                 76 H3 demands (all 5 models)
```

---

## 3. Belief Inventory

**F12 has 0 beliefs.** As a meta-layer, F12 produces evidence signals only.
Evidence feeds unidirectionally INTO F1-F9 observe() -- it does not maintain
its own belief state, precision tracking, or prediction error history.

---

## 4. Cross-Modal Domain Pipeline

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
             |
             v
 [Affective Transfer]
   CMAT   (10D, ARU-g)    <- cross-modal affective transfer -> F5
 [Action-Perception Coding]
   CMAPCC (10D, IMU-b)    <- action-perception common code -> F7/F4
 [Multimodal Prediction]
   CHPI   (11D, PCU-b)    <- cross-modal harmonic prediction -> F2
 [Domain-General Timing]
   DGTP   (9D,  ASU-g)    <- domain-general temporal processing -> F3/F7
 [Supramodal Deviance]
   SDD    (11D, NDU-a)    <- supramodal deviance detection -> F2/F3
```

**Cross-modal domain rationale**:
F12 models organize into 5 cross-modal domains -- one model per domain.
This 1:1 domain-model mapping is unique among all functions and reflects
the breadth of cross-modal integration: each model captures a distinct
integration pathway rather than depth-ordered processing within a single domain.

Unlike F10-F11 which have some within-unit depth ordering, F12 models are
maximally distributed (1 per unit) with NO within-unit dependencies.
All models operate independently on R3/H3 + their unit's upstream outputs.

---

## 5. Unit Distribution

| Unit | Models | Count |
|------|--------|-------|
| ARU (Affective Response Unit) | CMAT | 1 |
| IMU (Integrative Memory Unit) | CMAPCC | 1 |
| PCU (Predictive Coding Unit) | CHPI | 1 |
| ASU (Auditory Salience Unit) | DGTP | 1 |
| NDU (Neural Dynamics Unit) | SDD | 1 |

F12 has **maximal unit spread**: 5 models across 5 different units (1 each).
No other function achieves this level of unit distribution. This reflects
the pervasive nature of cross-modal integration -- it touches affect (ARU),
memory (IMU), prediction (PCU), attention (ASU), and novelty detection (NDU).

---

## 6. H3 Demands (all models)

| Model | H3 Tuples (v1) | Primary Fn | Status |
|-------|----------------|-----------|--------|
| CMAT | 9 | F12 | doc only |
| CMAPCC | 20 | F12 | doc only |
| CHPI | 20 | F12 | doc only |
| DGTP | 9 | F12 | doc only |
| SDD | 18 | F12 | doc only |

Total H3 demands from all F12 models: **76 tuples**.
Implemented: **0 tuples** (F12 is evidence-only).

CMAPCC and CHPI share the highest H3 demand (20 tuples each), reflecting the
rich multi-scale temporal tracking required for action-perception coding and
multimodal harmonic prediction. CMAT and DGTP are most compact (9 tuples each),
consistent with their focused gamma-tier architectures.

---

## 7. Next Steps

- [ ] Create CHPI mechanism layer docs in mechanisms/chpi/ (F12-primary)
- [ ] Create SDD mechanism layer docs in mechanisms/sdd/ (F12 cross-reference)
- [ ] Verify CMAT mechanism docs exist in F5-Emotion-and-Valence/mechanisms/cmat/
- [ ] Verify CMAPCC mechanism docs exist in F4-Memory-Systems/mechanisms/cmapcc/
- [ ] Verify DGTP mechanism docs exist in F3-Attention-and-Salience/mechanisms/dgtp/
- [ ] Define evidence signal routes (F12 -> F1-F9 observe()) during integration phase
- [ ] Create model code in brain/functions/f12/ (if F12 code module is created)
