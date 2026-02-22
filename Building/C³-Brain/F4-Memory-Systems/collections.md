# F4 Memory Systems -- Collections

> **NOTE**: This file was built by independently reading each model doc
> in `Docs/C3/Models/` and cross-referencing `Building/Ontology/C3/MODEL-ATLAS.md`.
> It does NOT copy from the orchestrator or ontology summaries.
> Counts and dimensions are snapshots -- they will change as models are integrated.

---

## 1. Verified F4 Models (from Model Docs + MODEL-ATLAS v2.0)

Independent scan of all 96 model docs + MODEL-ATLAS v2.0 function assignments identified
**15 primary** + **6 secondary** models for F4 (Memory Systems). All 15 primary models
belong to a single unit (IMU -- Integrative Memory Unit), making F4 unique in the system.
Cross-function contributions come from STU, RPU, ARU, and PCU.

### 1.1 Implemented (1 model -- relay only)

| Model | Unit-Tier | Doc OUTPUT_DIM | Code OUTPUT_DIM | Layers | H3 (v1) | Beliefs | Status |
|-------|-----------|----------------|-----------------|--------|---------|---------|--------|
| MEAMN | IMU-a1 | 12D | 12D | E3+M3+P3+F3 | 19 | 7 (3C+3A+1N) | relay done |

MEAMN is the F4 relay (kernel relay wrapper in `brain/kernel/`). It reads R3/H3 directly.
The relay exports `memory_state`, `emotional_color`, `nostalgia_link` + 3 F-layer predictions.
F4 mechanism code beyond the relay is a stub (`brain/functions/f4/__init__.py`).

### 1.2 Not Yet Implemented (14 primary models)

| Model | Unit-Tier | Doc OUTPUT_DIM | Layers | H3 (v1) | Beliefs | Status |
|-------|-----------|----------------|--------|---------|---------|--------|
| PNH | IMU-a2 | 11D | E3+M3+P2+F3 | 15 | 0 (F1 cross-fn) | pending |
| MMP | IMU-a3 | 12D | E3+M3+P3+F3 | 21 | 3 (0C+2A+1N) | pending |
| RASN | IMU-b1 | 11D | E3+M3+P2+F3 | 28 | 0 | pending |
| PMIM | IMU-b2 | 11D | E3+M3+P2+F3 | 18 | 0 | pending |
| OII | IMU-b3 | 10D | E3+M2+P2+F3 | 24 | 0 | pending |
| HCMC | IMU-b5 | 11D | E3+M3+P2+F3 | 22 | 3 (1C+2A+0N) | pending |
| RIRI | IMU-b6 | 10D | E3+M2+P2+F3 | 16 | 0 | pending |
| MSPBA | IMU-b4 | 11D | E3+M3+P2+F3 | 16 | 0 | pending |
| VRIAP | IMU-b7 | 10D | E3+M2+P2+F3 | 18 | 0 | pending |
| TPRD | IMU-b8 | 10D | E3+M2+P2+F3 | 18 | 0 | pending |
| CMAPCC | IMU-b9 | 10D | E3+M2+P2+F3 | 20 | 0 | pending |
| DMMS | IMU-g1 | 10D | E3+M2+P2+F3 | 15 | 0 | pending |
| CSSL | IMU-g2 | 10D | E3+M2+P2+F3 | 15 | 0 | pending |
| CDEM | IMU-g3 | 10D | E3+M2+P2+F3 | 18 | 0 | pending |

### 1.3 Full Model Descriptions

| Model | Full Name | Evidence Tier | Key Mechanism |
|-------|-----------|---------------|---------------|
| MEAMN | Music-Evoked Autobiographical Memory Network | a (>90%) | Autobiographical memory retrieval, emotional coloring, nostalgia |
| PNH | Pythagorean Neural Hierarchy | a (>90%) | Pythagorean ratio encoding, harmonic relationships |
| MMP | Musical Mnemonic Preservation | a (>90%) | Preserved melodic recognition in AD, hippocampal independence |
| RASN | Rhythmic Auditory Stimulation Neuroplasticity | b (70-90%) | Rhythmic entrainment for motor rehabilitation |
| PMIM | Predictive Memory Integration Model | b (70-90%) | Prediction-based memory encoding, expectation consolidation |
| OII | Oscillatory Intelligence Integration | b (70-90%) | Oscillatory binding across memory subsystems |
| HCMC | Hippocampal-Cortical Memory Circuit | b (70-90%) | Episodic encoding, segmentation, cortical consolidation |
| RIRI | RAS-Intelligent Rehabilitation Integration | b (70-90%) | RAS rehabilitation with memory-guided adaptation |
| MSPBA | Musical Syntax Processing in Broca's Area | b (70-90%) | Musical syntax in Broca's area, structural memory |
| VRIAP | VR-Integrated Analgesia Paradigm | b (70-90%) | VR-music integration for memory-based analgesia |
| TPRD | Tonotopy-Pitch Representation Dissociation | b (70-90%) | Tonotopic vs pitch representation dissociation |
| CMAPCC | Cross-Modal Action-Perception Common Code | b (70-90%) | Cross-modal action-perception common coding |
| DMMS | Developmental Music Memory Scaffold | g (50-70%) | Developmental scaffolding for music memory |
| CSSL | Cross-Species Song Learning | g (50-70%) | Cross-species vocal/song learning parallels |
| CDEM | Context-Dependent Emotional Memory | g (50-70%) | Context-dependent emotional memory formation |

### 1.4 Cross-Function -- Secondary Models Contributing to F4

| Model | Unit-Tier | Primary Function | F4 Contribution |
|-------|-----------|-----------------|-----------------|
| PMIM | IMU-b2 | F2 Prediction | Predictive memory integration (dual function -- listed in both F2 and F4) |
| HMCE | STU | F1/F2 Sensory | Temporal context for memory segmentation |
| TMRM | STU | F4 Memory | Temporal memory retrieval model |
| MEAMR | RPU | F4 Memory | Autobiographical memory reward pathway |
| NEMAC | ARU | F5 Emotion | Nostalgia-emotion coupling |
| SPH | PCU | F2 Prediction | Spatiotemporal prediction for memory |

### 1.5 Cross-Function Assignment

While all 15 models are housed in IMU, NOT all are F4-primary. The Building/F4
directory documents the COMPLETE IMU unit for organizational coherence:

| Primary Function | Models | Count |
|-----------------|--------|-------|
| F4 Memory | MEAMN, MMP, HCMC, DMMS, CSSL, CDEM | 6 |
| F1 Sensory | PNH, TPRD, MSPBA | 3 |
| F2 Prediction | PMIM | 1 |
| F8 Learning | OII | 1 |
| F10 Clinical | RASN, RIRI, VRIAP | 3 (clinical) |
| F12 Cross-Modal | CMAPCC | 1 |

---

## 2. Implementation Summary

```
Implemented:     1 model (MEAMN relay), 7 F4 beliefs from a model
Pending:         14 models (PNH, MMP, RASN, PMIM, OII, HCMC, RIRI, MSPBA,
                            VRIAP, TPRD, CMAPCC, DMMS, CSSL, CDEM)
Cross-function:  6 models (PMIM*->dual, HMCE->segmentation, TMRM->retrieval,
                           MEAMR->reward, NEMAC->nostalgia, SPH->prediction)

Current code:    12D mechanism output (MEAMN relay)
                 7 beliefs (from MEAMN -- see S3)
                 19 H3 demands (MEAMN relay)

Full F4 total:   159D mechanism output (all 15 primary models)
                 288 H3 demands (all 15 primary models)
```

---

## 3. Belief Inventory (from BELIEF-CYCLE.md)

| # | Belief | Cat | t | Owner | Status |
|---|--------|-----|---|-------|--------|
| 1 | autobiographical_retrieval | C | 0.85 | MEAMN | relay done |
| 2 | nostalgia_intensity | C | 0.8 | MEAMN | relay done |
| 3 | emotional_coloring | C | 0.75 | MEAMN | relay done |
| 4 | episodic_encoding | C | 0.7 | HCMC | pending |
| 5 | retrieval_probability | A | -- | MEAMN | relay done |
| 6 | memory_vividness | A | -- | MEAMN | relay done |
| 7 | self_relevance | A | -- | MEAMN | relay done |
| 8 | melodic_recognition | A | -- | MMP | pending |
| 9 | memory_preservation | A | -- | MMP | pending |
| 10 | episodic_boundary | A | -- | HCMC | pending |
| 11 | consolidation_strength | A | -- | HCMC | pending |
| 12 | vividness_trajectory | N | -- | MEAMN | relay done |
| 13 | memory_scaffold_pred | N | -- | MMP | pending |

**Distribution**: 4 Core + 7 Appraisal + 2 Anticipation = 13 total.
Belief owners: MEAMN (7), MMP (3), HCMC (3), b/g models (0 currently).

---

## 4. Depth-Ordered Pipeline

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
             |
             v
Depth 0:  MEAMN (12D, relay, IMU)  <- autobiographical memory retrieval
          PNH   (11D, IMU)         <- Pythagorean ratio encoding
          MMP   (12D, IMU)         <- musical mnemonic preservation (clinical)
             |
             v
Depth 1:  RASN  (11D, IMU)        <- rhythmic auditory stimulation (reads beat-entrainment)
          PMIM  (11D, IMU)        <- predictive memory integration (reads PNH)
          OII   (10D, IMU)        <- oscillatory intelligence integration (reads PMIM+MEAMN+HCMC+PNH+MSPBA)
          HCMC  (11D, IMU)        <- hippocampal-cortical memory circuit (reads MEAMN)
          RIRI  (10D, IMU)        <- RAS rehabilitation integration (reads RASN+MEAMN+MMP+HCMC)
          MSPBA (11D, IMU)        <- musical syntax in Broca's area (reads PNH)
             |
             v
Depth 2:  VRIAP (10D, IMU)        <- VR-integrated analgesia (memory-only)
          TPRD  (10D, IMU)        <- tonotopy-pitch dissociation (pitch cross-circuit)
          CMAPCC(10D, IMU)        <- cross-modal action-perception (beat cross-circuit)
          DMMS  (10D, IMU)        <- developmental music memory scaffold
          CSSL  (10D, IMU)        <- cross-species song learning (memory-only)
          CDEM  (10D, IMU)        <- context-dependent emotional memory (affect cross-circuit)
```

**Depth assignment rationale**:
- **Depth 0 (a)**: Read R3/H3 directly. MEAMN, PNH, and MMP have no mechanism dependencies.
- **Depth 1 (b)**: PMIM reads PNH. HCMC reads MEAMN. MSPBA reads PNH.
  OII reads PMIM+MEAMN+HCMC+PNH+MSPBA (5 intra-unit -- most connected).
  RASN reads beat-entrainment (F3 cross-fn). RIRI reads RASN+MEAMN+MMP+HCMC.
- **Depth 2 (b/g)**: VRIAP is memory-only. TPRD has pitch cross-circuit (F1).
  CMAPCC has beat cross-circuit (F3). DMMS feeds ARU.DAP, ARU.NEMAC.
  CSSL is memory-only. CDEM has affect cross-circuit (F5).

---

## 5. Unit Distribution

| Unit | Primary Models | Secondary Models | Count |
|------|---------------|-----------------|-------|
| IMU | 15 (MEAMN, PNH, MMP, RASN, PMIM, OII, HCMC, RIRI, MSPBA, VRIAP, TPRD, CMAPCC, DMMS, CSSL, CDEM) | 0 | 15 |
| STU | 0 | 2 (HMCE*, TMRM) | 2 |
| RPU | 0 | 1 (MEAMR) | 1 |
| ARU | 0 | 1 (NEMAC) | 1 |
| PCU | 0 | 1 (SPH*) | 1 |

IMU is the **only unit** for F4 primary models (15 of 15). This is unique in the system --
most functions span multiple units (F3 has ASU+STU+PCU). IMU is also the largest single
unit in the entire C3 system by model count.

---

## 6. H3 Demands (all primary models)

| Model | H3 Tuples (v1) | Law | Status |
|-------|----------------|-----|--------|
| MEAMN | 19 | L0 | relay done |
| PNH | 15 | L0 | doc only |
| MMP | 21 | L0 | doc only |
| RASN | 28 | L0 | doc only |
| PMIM | 18 | L0 | doc only |
| OII | 24 | L0 + L2 | doc only |
| HCMC | 22 | L0 | doc only |
| RIRI | 16 | L0 | doc only |
| MSPBA | 16 | L0 | doc only |
| VRIAP | 18 | L0 | doc only |
| TPRD | 18 | L0 | doc only |
| CMAPCC | 20 | L0 + L2 | doc only |
| DMMS | 15 | L0 | doc only |
| CSSL | 15 | L0 | doc only |
| CDEM | 18 | L0 | doc only |

Total H3 demands from all F4 primary models: **288 tuples**.
Implemented: **19 tuples** (from MEAMN relay).

---

## 7. Next Steps

- [x] Implement MEAMN relay wrapper (IMU-a1, 12D, 19 H3) -- done
- [ ] Implement PNH mechanism (IMU-a2, 11D, 15 H3)
- [ ] Implement MMP mechanism (IMU-a3, 12D, 21 H3)
- [ ] Implement RASN mechanism (IMU-b1, 11D, 28 H3)
- [ ] Implement PMIM mechanism (IMU-b2, 11D, 18 H3)
- [ ] Implement OII mechanism (IMU-b3, 10D, 24 H3)
- [ ] Implement HCMC mechanism (IMU-b5, 11D, 22 H3)
- [ ] Implement RIRI mechanism (IMU-b6, 10D, 16 H3)
- [ ] Implement MSPBA mechanism (IMU-b4, 11D, 16 H3)
- [ ] Implement VRIAP mechanism (IMU-b7, 10D, 18 H3)
- [ ] Implement TPRD mechanism (IMU-b8, 10D, 18 H3)
- [ ] Implement CMAPCC mechanism (IMU-b9, 10D, 20 H3)
- [ ] Implement DMMS mechanism (IMU-g1, 10D, 15 H3)
- [ ] Implement CSSL mechanism (IMU-g2, 10D, 15 H3)
- [ ] Implement CDEM mechanism (IMU-g3, 10D, 18 H3)
- [ ] Define beliefs for b/g models during implementation
- [ ] Link cross-function models (HMCE, TMRM, MEAMR, NEMAC, SPH) when F4 kernel is extended
