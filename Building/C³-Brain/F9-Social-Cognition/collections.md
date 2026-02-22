# F9 Social Cognition -- Collections

> **NOTE**: This file was built by independently reading each model doc
> in the primary function mechanism directories and cross-referencing the F9 data specification.
> It does NOT copy from the orchestrator or ontology summaries.
> Counts and dimensions are snapshots -- they will change as models are integrated.

---

## 1. Verified F9 Models (from Model Docs)

Independent scan of all 3 mechanism model doc sets identified
**3 models** for F9 (Social Cognition) with **0 secondary** cross-function models.
F9 is the **SMALLEST cognitive function** in C3 -- only 3 models, 10 beliefs.
Critically, F9 has NO dedicated unit -- all models are cross-unit:
MPU (Motor Processing Unit, 2 models) and RPU (Reward Processing Unit, 1 model).
Output dimensions are uniform (11D each), reflecting the consistent 4-layer EMPF architecture.

### 1.1 Implemented (0 models)

No F9 models are currently implemented. F9 is evidence-only in the current kernel (Phase 3).
F9 mechanism code is a stub (`brain/functions/f9/__init__.py`).

### 1.2 Not Yet Implemented (3 models)

| Model | Unit-Tier | Doc OUTPUT_DIM | Layers | H3 (v1) | Beliefs | Status |
|-------|-----------|----------------|--------|---------|---------|--------|
| NSCP | MPU-g1 | 11D | E+M+P+F | 14 | 2 (1C+1N) | pending |
| SSRI | RPU-b4 | 11D | E+M+P+F | 18 | 6 (5A+1N) | pending |
| DDSMI | MPU-b2 | 11D | E+M+P+F | 11 | 2 (1C+1A) | pending |

### 1.3 Full Model Descriptions

| Model | Full Name | Evidence Tier | Key Mechanism |
|-------|-----------|---------------|---------------|
| NSCP | Neural Synchrony Commercial Prediction | gamma (50-70%) | Population-level ISC proxy, catchiness/groove, commercial success prediction (R^2=0.619) |
| SSRI | Social Synchrony Reward Integration | beta (70-90%) | Social reward amplification 1.3-1.8x, prefrontal inter-brain sync, endorphin-mediated bonding |
| DDSMI | Dyadic Dance Social Motor Integration | beta (70-90%) | Four parallel mTRF tracking processes, auditory-social resource competition, partner coordination |

### 1.4 Cross-Function -- Secondary Models Contributing to F9

F9 has **NO secondary cross-function models**. All 3 models are primary or secondary contributors
from their home functions (F6 and F7) that produce F9-relevant beliefs as a cross-function output.

### 1.5 Cross-Function Assignment

F9 is unique among Functions for having NO dedicated unit. All 3 models reside in units
belonging to other functions. NSCP is the only F9-primary model.

| Primary Function | Models | Count |
|-----------------|--------|-------|
| F9 Social (via MPU) | NSCP | 1 |
| F6 Reward (via RPU) | SSRI | 1 |
| F7 Motor (via MPU) | DDSMI | 1 |

F9 models also contribute to their home functions:
- **F6 Reward**: SSRI (social reward amplification, SPE, endorphin dynamics)
- **F7 Motor**: NSCP (groove/motor entrainment, ISC-based predictions), DDSMI (dyadic motor coordination, mTRF balance)

---

## 2. Implementation Summary

```
Implemented:     0 models (F9 is evidence-only, Phase 3)
Pending:         3 models (NSCP, SSRI, DDSMI)
Cross-function:  0 models (F9 has no secondary contributors)

Current code:    0D mechanism output (no relay, no mechanism code)
                 0 F9 beliefs (none implemented)
                 0 H3 demands (none implemented)

Full F9 total:   33D mechanism output (all 3 models)
                 10 beliefs (2C + 6A + 2N)
                 43 H3 demands (all 3 models)
```

---

## 3. Belief Inventory

| # | Belief | Cat | t | Owner | Status |
|---|--------|-----|---|-------|--------|
| 1 | neural_synchrony | C | 0.65 | NSCP | pending |
| 2 | social_coordination | C | 0.60 | DDSMI | pending |
| 3 | synchrony_reward | A | -- | SSRI | pending |
| 4 | social_bonding | A | -- | SSRI | pending |
| 5 | group_flow | A | -- | SSRI | pending |
| 6 | entrainment_quality | A | -- | SSRI | pending |
| 7 | social_prediction_error | A | -- | SSRI | pending |
| 8 | resource_allocation | A | -- | DDSMI | pending |
| 9 | catchiness_pred | N | -- | NSCP | pending |
| 10 | collective_pleasure_pred | N | -- | SSRI | pending |

**Distribution**: 2 Core + 6 Appraisal + 2 Anticipation = 10 total.
Belief owners: NSCP (2), SSRI (6), DDSMI (2).
SSRI dominates with 6 of 10 beliefs, reflecting its rich social reward architecture (5 E-layer features).

---

## 4. Depth-Ordered Pipeline

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
             |
             v
         NSCP  (11D, MPU-g1)      <- neural synchrony commercial prediction [F9-primary]
         SSRI  (11D, RPU-b4)      <- social synchrony reward integration [F6-primary -> F9]
         DDSMI (11D, MPU-b2)      <- dyadic dance social motor integration [F7-primary -> F9]
```

**Depth assignment rationale**:
F9 models do NOT form a depth-ordered DAG among themselves. Unlike most Functions where
alpha models feed beta which feed gamma, F9's 3 models operate in parallel -- each reads
from R3/H3 and from upstream models within their home units (MPU or RPU), not from each other.
The only cross-model dependency is that SSRI's social prediction error and DDSMI's social
coordination predictions both feed into F6 RewardAggregator downstream.

---

## 5. Unit Distribution

| Unit | Models | Count |
|------|--------|-------|
| MPU (Motor Processing Unit) | NSCP, DDSMI | 2 |
| RPU (Reward Processing Unit) | SSRI | 1 |

F9 is the **only Function** with NO dedicated unit at all. All 3 models are guests in
units belonging to other functions. MPU leads (2 of 3 models) with the motor-social
integration pathway; RPU contributes the reward-social dimension. Output dimensions
are perfectly uniform at 11D each, reflecting the consistent 4-layer EMPF architecture
that all three models share.

---

## 6. H3 Demands (all models)

| Model | H3 Tuples (v1) | Law | Status |
|-------|----------------|-----|--------|
| NSCP | 14 | L2 | doc only |
| SSRI | 18 | L0+L2 | doc only |
| DDSMI | 11 | L2 | doc only |

Total H3 demands from all F9 models: **43 tuples**.
Implemented: **0 tuples** (F9 is evidence-only).

---

## 7. Next Steps

- [ ] Implement NSCP mechanism (MPU-g1, 11D, 14 H3) -- F9-primary, ISC + catchiness + commercial
- [ ] Implement SSRI mechanism (RPU-b4, 11D, 18 H3) -- social reward amplification, 6 beliefs
- [ ] Implement DDSMI mechanism (MPU-b2, 11D, 11 H3) -- dyadic dance, mTRF resource competition
- [ ] Define F9 relay (if warranted) during Phase 3 integration
- [ ] Create F9 belief docs in beliefs/nscp/, beliefs/ssri/, beliefs/ddsmi/
