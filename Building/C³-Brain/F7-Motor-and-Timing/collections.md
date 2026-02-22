# F7 Motor & Timing -- Collections

> **NOTE**: This file was built by independently reading each model doc
> in `Docs/C3/Models/` and cross-referencing `Building/Ontology/C3/MODEL-ATLAS.md`.
> It does NOT copy from the orchestrator or ontology summaries.
> Counts and dimensions are snapshots -- they will change as models are integrated.

---

## 1. Verified F7 Models (from Model Docs + MODEL-ATLAS v2.0)

Independent scan of all 96 model docs + MODEL-ATLAS v2.0 function assignments identified
**10 primary** + **7 secondary** models for F7 (Motor & Timing). The dominant unit is
MPU (Motor Processing Unit) with ALL 10 models. MPU is unique in the system for its
perfect output-dimension uniformity: every model produces exactly 11D.
Cross-function contributions come from STU, PCU, RPU, and ASU.

### 1.1 Implemented (1 model -- relay done)

| Model | Unit-Tier | Doc OUTPUT_DIM | Code OUTPUT_DIM | Layers | H3 (v1) | Beliefs | Status |
|-------|-----------|----------------|-----------------|--------|---------|---------|--------|
| PEOM | MPU-a1 | 11D | 11D | E+M+P+F | 15 | 5 (2C+2A+1N) | relay done |

PEOM is the F7 primary relay (kernel relay wrapper in `brain/kernel/`). It reads R3/H3 directly.
The relay exports `period_lock_strength`, `kinematic_smoothness` + `next_beat_pred`, `velocity_pred`.
PEOM is housed in MPU as the a1 anchor for the entire Motor & Timing pipeline.
F7 mechanism code beyond the relay is a stub (`brain/functions/f7/__init__.py`).

### 1.2 Not Yet Implemented (9 primary models)

| Model | Unit-Tier | Doc OUTPUT_DIM | Layers | H3 (v1) | Beliefs | Status |
|-------|-----------|----------------|--------|---------|---------|--------|
| MSR | MPU-a2 | 11D | E+M+P+F | 22 | 0 | pending |
| GSSM | MPU-a3 | 11D | E+M+P+F | 12 | 0 | pending |
| ASAP | MPU-b1 | 11D | E+M+P+F | 9 | 0 | pending |
| DDSMI | MPU-b2 | 11D | E+M+P+F | 11 | 0 | pending |
| VRMSME | MPU-b3 | 11D | E+M+P+F | 12 | 0 | pending |
| SPMC | MPU-b4 | 11D | E+M+P+F | 15 | 0 | pending |
| NSCP | MPU-g1 | 11D | E+M+P+F | 14 | 0 | pending |
| CTBB | MPU-g2 | 11D | E+M+P+F | 9 | 0 | pending |
| STC | MPU-g3 | 11D | E+M+P+F | 12 | 0 | pending |

### 1.3 Full Model Descriptions

| Model | Full Name | Evidence Tier | Key Mechanism |
|-------|-----------|---------------|---------------|
| PEOM | Period Entrainment Oscillator Model | a (>90%) | Period locking, body-beat synchronization, motor kinematics |
| MSR | Motor Sequence Representation | a (>90%) | Sequence encoding, motor planning for rhythmic patterns |
| GSSM | Groove/Syncopation Sensorimotor Model | a (>90%) | Groove generation, syncopation-driven motor response |
| ASAP | Auditory-Somatosensory Action Prediction | b (70-90%) | Cross-modal action prediction, sensorimotor integration |
| DDSMI | Dynamic Desynchronization in Sensorimotor Integration | b (70-90%) | Beta desynchronization, sensorimotor timing dissociation |
| VRMSME | Vestibular-Rhythmic Multisensory Motor Encoding | b (70-90%) | Vestibular-rhythm coupling, multisensory motor encoding |
| SPMC | Supplementary/Premotor Cortex Model | b (70-90%) | SMA/premotor cortex motor planning, timing generation |
| NSCP | Neural Substrate of Coupled Periodicity | g (50-70%) | Coupled oscillator networks, neural periodicity binding |
| CTBB | Cerebellar Timing in Beat-Based Processing | g (50-70%) | Cerebellar forward model, sub-second timing precision |
| STC | Sensorimotor Timing Control | g (50-70%) | Integrated timing control, sensorimotor feedback loops |

### 1.4 Cross-Function -- Secondary Models Contributing to F7

| Model | Unit-Tier | Primary Function | F7 Contribution |
|-------|-----------|-----------------|-----------------|
| HMCE | STU-a1 | F2 Prediction | Motor timing context hierarchy -- 6 F7 beliefs (context_depth + short/medium/long_context + phrase/structure_pred) |
| ETAM | STU-b | F3 Attention | Tempo-motor attention gating |
| HGSIC | STU-b5 | F7 Motor | Groove state motor planning -- 6 F7 beliefs (groove_quality + beat_prominence/meter_structure/auditory_motor_coupling/motor_preparation + groove_trajectory) |
| TMRM | STU-g | F5 Emotion | Tempo reproduction |
| WMED | PCU-b | F2 Prediction | Motor-working memory dissociation |
| MCCN | RPU-b2 | F6 Reward | Chills motor coupling |
| SNEM | ASU-a | F3 Attention | Beat entrainment for motor |

### 1.5 Cross-Function Assignment

MPU dominates completely (10 of 10 primary models). Unlike other Functions, F7 has NO
non-MPU primary models -- the relay (PEOM) is also MPU. This makes F7 the most
unit-homogeneous Function in the system.

| Primary Function | Models | Count |
|-----------------|--------|-------|
| F7 Motor (MPU) | PEOM, MSR, GSSM, ASAP, DDSMI, VRMSME, SPMC, NSCP, CTBB, STC | 10 |

MPU models also contribute to other functions:
- **F1 Sensory**: PEOM (timing scaffold for sensory processing)
- **F2 Prediction**: MSR (sequence prediction), GSSM (groove prediction)
- **F3 Attention**: PEOM (beat-based attentional entrainment), SNEM cross-link
- **F5 Emotion**: GSSM (groove-affect coupling), TMRM cross-link
- **F6 Reward**: PEOM (tempo -> reward timing), MCCN cross-link

---

## 2. Implementation Summary

```
Implemented:     1 model (PEOM relay done), 5 F7 beliefs (PEOM-owned)
                 + 12 cross-function beliefs (HMCE 6, HGSIC 6)
Pending:         9 models (MSR, GSSM, ASAP, DDSMI, VRMSME, SPMC,
                           NSCP, CTBB, STC)
Cross-function:  7 models (HMCE*->hierarchy, ETAM*->attention,
                           HGSIC*->groove, TMRM*->tempo,
                           WMED*->working memory, MCCN*->chills,
                           SNEM*->entrainment)

Current code:    11D mechanism output (PEOM 11D relay)
                 17 F7 beliefs (PEOM 5 + HGSIC 6 + HMCE 6)
                 15 H3 demands (PEOM 15)

Full F7 total:   110D mechanism output (all 10 primary models)
                 ~131 H3 demands (all 10 primary models)
```

---

## 3. Belief Inventory (from BELIEF-CYCLE.md)

| # | Belief | Cat | t | Owner | Status |
|---|--------|-----|---|-------|--------|
| 1 | period_entrainment | C | 0.65 | PEOM | done |
| 2 | kinematic_efficiency | C | 0.60 | PEOM | done |
| 3 | groove_quality | C | 0.55 | HGSIC | done |
| 4 | context_depth | C | 0.70 | HMCE | done |
| 5 | timing_precision | A | -- | PEOM | done |
| 6 | period_lock_strength | A | -- | PEOM | done |
| 7 | beat_prominence | A | -- | HGSIC | done |
| 8 | meter_structure | A | -- | HGSIC | done |
| 9 | auditory_motor_coupling | A | -- | HGSIC | done |
| 10 | motor_preparation | A | -- | HGSIC | done |
| 11 | short_context | A | -- | HMCE | done |
| 12 | medium_context | A | -- | HMCE | done |
| 13 | long_context | A | -- | HMCE | done |
| 14 | next_beat_pred | N | -- | PEOM | done |
| 15 | groove_trajectory | N | -- | HGSIC | done |
| 16 | phrase_boundary_pred | N | -- | HMCE | done |
| 17 | structure_pred | N | -- | HMCE | done |

**Distribution**: 4 Core + 9 Appraisal + 4 Anticipation = 17 total.
Belief owners: PEOM (5), HGSIC (6), HMCE (6), b/g MPU models (0 currently).

---

## 4. Depth-Ordered Pipeline

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
             |
             v
Depth 0:  PEOM  (11D, relay, MPU)  <- period entrainment oscillator model [F7 primary]
          MSR   (11D, MPU)         <- motor sequence representation
          GSSM  (11D, MPU)         <- groove/syncopation sensorimotor model
             |
             v
Depth 1:  ASAP  (11D, MPU)        <- auditory-somatosensory action prediction (reads PEOM+MSR)
          DDSMI (11D, MPU)         <- dynamic desynchronization sensorimotor integration (reads PEOM+MSR)
          VRMSME(11D, MPU)         <- vestibular-rhythmic multisensory motor encoding (reads PEOM+GSSM)
          SPMC  (11D, MPU)         <- supplementary/premotor cortex model (reads MSR+GSSM)
             |
             v
Depth 2:  NSCP  (11D, MPU)        <- neural substrate of coupled periodicity (reads ASAP+DDSMI)
          CTBB  (11D, MPU)         <- cerebellar timing in beat-based processing (reads DDSMI+VRMSME)
          STC   (11D, MPU)         <- sensorimotor timing control (reads VRMSME+SPMC)
```

**Depth assignment rationale**:
- **Depth 0 (a)**: Read R3/H3 directly. PEOM, MSR, and GSSM have no mechanism dependencies.
- **Depth 1 (b)**: ASAP reads PEOM+MSR. DDSMI reads PEOM+MSR. VRMSME reads PEOM+GSSM. SPMC reads MSR+GSSM.
- **Depth 2 (g)**: NSCP reads ASAP+DDSMI (coupled periodicity from action prediction + desynchronization). CTBB reads DDSMI+VRMSME (cerebellar timing from desynchronization + vestibular). STC reads VRMSME+SPMC (timing control from vestibular + premotor).

---

## 5. Unit Distribution

| Unit | Primary Models | Secondary Models | Count |
|------|---------------|-----------------|-------|
| MPU | 10 (PEOM, MSR, GSSM, ASAP, DDSMI, VRMSME, SPMC, NSCP, CTBB, STC) | 0 | 10 |
| STU | 0 | 4 (HMCE*, ETAM*, HGSIC*, TMRM*) | 4 |
| PCU | 0 | 1 (WMED*) | 1 |
| RPU | 0 | 1 (MCCN*) | 1 |
| ASU | 0 | 1 (SNEM*) | 1 |

MPU is the **sole unit** for F7 primary models (10 of 10). MPU produces
**perfectly uniform outputs** (all 11D, zero variance). This is unique in the system --
no other unit has such dimensional consistency. The uniform 11D reflects the consistent
dimensionality requirements of motor/timing representations across all processing depths.

---

## 6. H3 Demands (all primary models)

| Model | H3 Tuples (v1) | Law | Status |
|-------|----------------|-----|--------|
| PEOM | 15 | L0 | relay done |
| MSR | 22 | L0 | doc only |
| GSSM | 12 | L0 | doc only |
| ASAP | 9 | L0 | doc only |
| DDSMI | 11 | L0 | doc only |
| VRMSME | 12 | L0 | doc only |
| SPMC | 15 | L0 | doc only |
| NSCP | 14 | L0 | doc only |
| CTBB | 9 | L0 | doc only |
| STC | 12 | L0 | doc only |

Total H3 demands from all F7 primary models: **~131 tuples**.
Implemented: **15 tuples** (from PEOM relay done).

---

## 7. Next Steps

- [x] Implement PEOM relay wrapper (MPU-a1, 11D, 15 H3) -- done
- [ ] Implement MSR mechanism (MPU-a2, 11D, 22 H3)
- [ ] Implement GSSM mechanism (MPU-a3, 11D, 12 H3)
- [ ] Implement ASAP mechanism (MPU-b1, 11D, 9 H3)
- [ ] Implement DDSMI mechanism (MPU-b2, 11D, 11 H3)
- [ ] Implement VRMSME mechanism (MPU-b3, 11D, 12 H3)
- [ ] Implement SPMC mechanism (MPU-b4, 11D, 15 H3)
- [ ] Implement NSCP mechanism (MPU-g1, 11D, 14 H3)
- [ ] Implement CTBB mechanism (MPU-g2, 11D, 9 H3)
- [ ] Implement STC mechanism (MPU-g3, 11D, 12 H3)
- [ ] Define beliefs for b/g models during implementation
- [ ] Link cross-function models (HMCE, ETAM, HGSIC, TMRM, WMED, MCCN, SNEM) when F7 kernel is extended
