# F8 Learning & Plasticity -- Collections

> **NOTE**: This file was built by independently reading each model doc
> in `mechanisms/` and cross-referencing the F8 data specification.
> It does NOT copy from the orchestrator or ontology summaries.
> Counts and dimensions are snapshots -- they will change as models are integrated.

---

## 1. Verified F8 Models (from Model Docs)

Independent scan of all 6 mechanism model doc sets identified
**6 primary** + **8 secondary** models for F8 (Learning & Plasticity). Unlike most Functions,
F8 has NO single dominant unit -- models span NDU (Neural Development Unit, 4 models) and
SPU (Spectral Processing Unit, 2 models). Output dimensions are heterogeneous (10D--13D),
reflecting the diverse nature of plasticity processes.
Cross-function contributions come from IMU, MPU, STU, and PCU.

### 1.1 Implemented (0 models)

No F8 models are currently implemented. F8 is evidence-only in the current kernel (Phase 5 deferred).
F8 mechanism code is a stub (`brain/functions/f8/__init__.py`).

### 1.2 Not Yet Implemented (6 primary models)

| Model | Unit-Tier | Doc OUTPUT_DIM | Layers | H3 (v1) | Beliefs | Status |
|-------|-----------|----------------|--------|---------|---------|--------|
| EDNR | NDU-a | 10D | E+M+P+F | 16 | 2 (1C+1A) | pending |
| TSCP | SPU-b1 | 10D | E+M+P+F | 12 | 2 (1C+1A) | pending |
| CDMR | NDU-b1 | 11D | E+M+P+F | 16 | 0 | pending |
| SLEE | NDU-b2 | 13D | E+M+P+F | 18 | 3 (1C+2A) | pending |
| ESME | SPU-g1 | 11D | E+M+P+F | 12 | 5 (1C+3A+1N) | pending |
| ECT | NDU-g1 | 12D | E+M+P+F | 18 | 2 (1A+1N) | pending |

### 1.3 Full Model Descriptions

| Model | Full Name | Evidence Tier | Key Mechanism |
|-------|-----------|---------------|---------------|
| EDNR | Expertise-Dependent Network Reorganization | a (>90%) | Within-network compartmentalization, expertise-driven connectivity reorganization |
| TSCP | Timbre-Specific Cortical Plasticity | b (70-90%) | N1m timbre-selective enhancement, instrument-specific cortical maps |
| CDMR | Context-Dependent Mismatch Response | b (70-90%) | Context-modulated deviance detection, subadditivity in combined deviants |
| SLEE | Statistical Learning Expertise Enhancement | b (70-90%) | Supramodal regularity extraction, IFG hub for statistical patterns |
| ESME | Expertise-Specific MMN Enhancement | g (50-70%) | Domain-specific MMN amplification across pitch/rhythm/timbre |
| ECT | Expertise Compartmentalization Trade-off | g (50-70%) | Within-network gains vs between-network losses, flexibility cost |

### 1.4 Cross-Function -- Secondary Models Contributing to F8

| Model | Unit-Tier | Primary Function | F8 Contribution |
|-------|-----------|-----------------|-----------------|
| OII | IMU-b | F4 Memory | Oscillatory intelligence -- learning-dependent oscillation patterns |
| MSR | MPU-a2 | F7 Motor | Sensorimotor reorganization -- motor plasticity from musical training |
| STC | MPU-g3 | F7 Motor | Singing connectivity -- vocal training sensorimotor plasticity |
| EDTA | STU-b | F8 secondary | Expertise-dependent tempo accuracy |
| MTNE | STU-g | F8 secondary | Music training neural efficiency |
| PTGMP | STU-g | F8 primary | Piano training grey matter plasticity |
| MPFS | STU-g | F8 secondary | Musical prodigy flow state |
| MAA | PCU-g | F5 secondary | Multifactorial atonal appreciation |

### 1.5 Cross-Function Assignment

F8 is unique among Functions for having NO single dominant unit. NDU and SPU share the
primary model space (4:2 split). This distributed architecture reflects the multi-domain
nature of plasticity: structural reorganization (NDU) and spectral-perceptual refinement
(SPU) are distinct but interacting processes.

| Primary Function | Models | Count |
|-----------------|--------|-------|
| F8 Learning (NDU) | EDNR, CDMR, SLEE, ECT | 4 |
| F8 Learning (SPU) | TSCP, ESME | 2 |

NDU and SPU models also contribute to other functions:
- **F1 Sensory**: EDNR (expertise modulates sensory processing gain)
- **F2 Prediction**: SLEE (statistical model informs prediction), CDMR (mismatch for predictive coding)
- **F4 Memory**: SLEE (long-term statistical representations), OII cross-link
- **F5 Emotion**: ESME (enhanced emotional salience of trained sounds), MAA cross-link
- **F7 Motor**: EDNR (motor network reorganization), MSR + STC cross-links

---

## 2. Implementation Summary

```
Implemented:     0 models (F8 is evidence-only, Phase 5 deferred)
Pending:         6 models (EDNR, TSCP, CDMR, SLEE, ESME, ECT)
Cross-function:  8 models (OII*->oscillatory, MSR*->motor,
                           STC*->singing, EDTA*->tempo,
                           MTNE*->efficiency, PTGMP*->grey matter,
                           MPFS*->flow, MAA*->atonal)

Current code:    0D mechanism output (no relay, no mechanism code)
                 0 F8 beliefs (none implemented)
                 0 H3 demands (none implemented)

Full F8 total:   67D mechanism output (all 6 primary models)
                 14 beliefs (4C + 8A + 2N)
                 92 H3 demands (all 6 primary models)
```

---

## 3. Belief Inventory

| # | Belief | Cat | t | Owner | Status |
|---|--------|-----|---|-------|--------|
| 1 | network_specialization | C | 0.95 | EDNR | pending |
| 2 | trained_timbre_recognition | C | 0.90 | TSCP | pending |
| 3 | statistical_model | C | 0.88 | SLEE | pending |
| 4 | expertise_enhancement | C | 0.92 | ESME | pending |
| 5 | within_connectivity | A | -- | EDNR | pending |
| 6 | plasticity_magnitude | A | -- | TSCP | pending |
| 7 | pitch_mmn | A | -- | ESME | pending |
| 8 | rhythm_mmn | A | -- | ESME | pending |
| 9 | timbre_mmn | A | -- | ESME | pending |
| 10 | compartmentalization_cost | A | -- | ECT | pending |
| 11 | detection_accuracy | A | -- | SLEE | pending |
| 12 | multisensory_binding | A | -- | SLEE | pending |
| 13 | expertise_trajectory | N | -- | ESME | pending |
| 14 | transfer_limitation | N | -- | ECT | pending |

**Distribution**: 4 Core + 8 Appraisal + 2 Anticipation = 14 total.
Belief owners: EDNR (2), TSCP (2), SLEE (3), ESME (5), ECT (2), CDMR (0).

---

## 4. Depth-Ordered Pipeline

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
             |
             v
Depth 0:  EDNR  (10D, NDU)           <- expertise-dependent network reorganization [F8 foundation]
             |
             v
Depth 1:  TSCP  (10D, SPU)           <- timbre-specific cortical plasticity (reads EDNR)
          CDMR  (11D, NDU)           <- context-dependent mismatch response (reads EDNR)
          SLEE  (13D, NDU)           <- statistical learning expertise enhancement (reads EDNR)
             |
             v
Depth 2:  ESME  (11D, SPU)           <- expertise-specific MMN enhancement (reads EDNR+TSCP+CDMR)
          ECT   (12D, NDU)           <- expertise compartmentalization trade-off (reads EDNR+CDMR+SLEE)
```

**Depth assignment rationale**:
- **Depth 0 (a)**: EDNR reads R3/H3 directly. It is the foundational model -- network reorganization enables all downstream expertise effects.
- **Depth 1 (b)**: TSCP reads R3/H3 + EDNR (timbre plasticity modulated by network state). CDMR reads R3/H3 + EDNR (mismatch modulated by expertise). SLEE reads R3/H3 + EDNR (statistical learning enhanced by reorganization).
- **Depth 2 (g)**: ESME reads EDNR + TSCP + CDMR (expertise-specific MMN from network state + timbre + mismatch). ECT reads EDNR + CDMR + SLEE (compartmentalization cost from reorganization + mismatch + learning).

---

## 5. Unit Distribution

| Unit | Primary Models | Secondary Models | Count |
|------|---------------|-----------------|-------|
| NDU | 4 (EDNR, CDMR, SLEE, ECT) | 0 | 4 |
| SPU | 2 (TSCP, ESME) | 0 | 2 |
| IMU | 0 | 1 (OII*) | 1 |
| MPU | 0 | 2 (MSR*, STC*) | 2 |
| STU | 0 | 4 (EDTA*, MTNE*, PTGMP*, MPFS*) | 4 |
| PCU | 0 | 1 (MAA*) | 1 |

F8 is the **only Function** with NO single dominant unit for primary models. NDU leads (4 of 6)
but SPU contributes meaningfully (2 of 6). Output dimensions are heterogeneous: NDU ranges
10D--13D (mean 11.5D), SPU ranges 10D--11D (mean 10.5D). This variability reflects the
diverse representational requirements of plasticity processes -- from compact network state
summaries (EDNR 10D) to rich statistical models (SLEE 13D).

---

## 6. H3 Demands (all primary models)

| Model | H3 Tuples (v1) | Law | Status |
|-------|----------------|-----|--------|
| EDNR | 16 | L0+L2 | doc only |
| TSCP | 12 | L0+L2 | doc only |
| CDMR | 16 | L0+L2 | doc only |
| SLEE | 18 | L0+L2 | doc only |
| ESME | 12 | L0+L2 | doc only |
| ECT | 18 | L0+L2 | doc only |

Total H3 demands from all F8 primary models: **92 tuples**.
Implemented: **0 tuples** (F8 is evidence-only).

---

## 7. Next Steps

- [ ] Implement EDNR mechanism (NDU-a, 10D, 16 H3) -- foundational, must be first
- [ ] Implement TSCP mechanism (SPU-b1, 10D, 12 H3)
- [ ] Implement CDMR mechanism (NDU-b1, 11D, 16 H3)
- [ ] Implement SLEE mechanism (NDU-b2, 13D, 18 H3)
- [ ] Implement ESME mechanism (SPU-g1, 11D, 12 H3) -- requires EDNR + TSCP + CDMR
- [ ] Implement ECT mechanism (NDU-g1, 12D, 18 H3) -- requires EDNR + CDMR + SLEE
- [ ] Define F8 relay (if warranted) during Phase 5 integration
- [ ] Link cross-function models (OII, MSR, STC, EDTA, MTNE, PTGMP, MPFS, MAA) when F8 kernel is extended
