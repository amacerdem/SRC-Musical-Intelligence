# F5 Emotion & Valence -- Collections

> **NOTE**: This file was built by independently reading each model doc
> in `Docs/C3/Models/` and cross-referencing `Building/Ontology/C3/MODEL-ATLAS.md`.
> It does NOT copy from the orchestrator or ontology summaries.
> Counts and dimensions are snapshots -- they will change as models are integrated.

---

## 1. Verified F5 Models (from Model Docs + MODEL-ATLAS v2.0)

Independent scan of all 96 model docs + MODEL-ATLAS v2.0 function assignments identified
**12 primary** + **3 secondary** models for F5 (Emotion & Valence). The dominant unit is
ARU (Aesthetic-Reward Unit) with 10 of 12 models. Two non-ARU models round out the function:
MAA (PCU) and STAI (SPU). Cross-function contributions come from PCU and IMU.

### 1.1 Implemented (1 model -- relay partial)

| Model | Unit-Tier | Doc OUTPUT_DIM | Code OUTPUT_DIM | Layers | H3 (v1) | Beliefs | Status |
|-------|-----------|----------------|-----------------|--------|---------|---------|--------|
| SRP | ARU-a1 | 19D | 19D | E5+M5+P4+F5 | ~124 | 0 (F6 beliefs) | relay partial |

SRP is the F5/F6 relay (kernel relay wrapper in `brain/kernel/`). It reads R3/H3 directly.
The relay exports `wanting`, `liking`, `pleasure` + `tension`, `reward`, `chills`, `resolution`.
SRP is F6-primary (reward pathway) but housed in ARU alongside the other F5 models.
F5 mechanism code beyond the relay is a stub (`brain/functions/f5/__init__.py`).

### 1.2 Not Yet Implemented (11 primary models)

| Model | Unit-Tier | Doc OUTPUT_DIM | Layers | H3 (v1) | Beliefs | Status |
|-------|-----------|----------------|--------|---------|---------|--------|
| AAC | ARU-a2 | 14D | E4+M3+P3+F4 | ~50 | 4 (1C+2A+1N) | pending |
| VMM | ARU-a3 | 12D | E3+M3+P3+F3 | 7 | 6 (2C+4A) | pending |
| PUPF | ARU-b1 | 12D | E3+M3+P3+F3 | 21 | 0 | pending |
| CLAM | ARU-b2 | 11D | E3+M3+P2+F3 | 12 | 0 | pending |
| MAD | ARU-b3 | 11D | E3+M3+P2+F3 | 9 | 0 | pending |
| NEMAC | ARU-b4 | 11D | E3+M3+P2+F3 | 13 | 4 (1C+2A+1N) | pending |
| STAI | SPU-b5 | 12D | E3+M3+P3+F3 | 14 | 0 | pending |
| DAP | ARU-g1 | 10D | E3+M2+P2+F3 | 6 | 0 | pending |
| CMAT | ARU-g2 | 10D | E3+M2+P2+F3 | 9 | 0 | pending |
| TAR | ARU-g3 | 10D | E3+M2+P2+F3 | 21 | 0 | pending |
| MAA | PCU-g4 | 10D | E3+M2+P2+F3 | 14 | 0 | pending |

### 1.3 Full Model Descriptions

| Model | Full Name | Evidence Tier | Key Mechanism |
|-------|-----------|---------------|---------------|
| SRP | Striatal Reward Prediction | a (>90%) | Reward pathway, wanting/liking, chills, tension-resolution |
| AAC | Autonomic-Affective Coupling | a (>90%) | Physiological arousal, ANS responses, chills/frisson |
| VMM | Valence-Mode Mapping | a (>90%) | Major/minor mode detection, happy/sad classification |
| PUPF | Psycho-Neuro-Pharmacological Unified Framework | b (70-90%) | Dopamine, serotonin, endorphin pathways in music |
| CLAM | Closed-Loop Affective Modulation | b (70-90%) | Feedback-driven emotion regulation through music |
| MAD | Musical Anhedonia Disconnection | b (70-90%) | Disconnection between auditory and reward systems |
| NEMAC | Nostalgia-Enhanced Memory-Affect Coupling | b (70-90%) | Nostalgia-wellbeing link, self-referential processing |
| STAI | Spectral-Temporal Aesthetic Integration | b (70-90%) | Spectral/temporal feature integration for aesthetic emotion |
| DAP | Developmental Affective Plasticity | g (50-70%) | Age-related changes in musical emotion processing |
| CMAT | Cross-Modal Affective Transfer | g (50-70%) | Emotion transfer across sensory modalities |
| TAR | Therapeutic Affective Resonance | g (50-70%) | Music therapy affective mechanisms |
| MAA | Multifactorial Atonal Appreciation | g (50-70%) | Emotional responses to atonal/dissonant music |

### 1.4 Cross-Function -- Secondary Models Contributing to F5

| Model | Unit-Tier | Primary Function | F5 Contribution |
|-------|-----------|-----------------|-----------------|
| ICEM | PCU-a3 | F2 Prediction | Information content -> emotional arousal mapping |
| MEAMN | IMU-a1 | F4 Memory | Emotional coloring of autobiographical memories |
| CDEM | IMU-g3 | F4 Memory | Context-dependent emotional memory formation |

### 1.5 Cross-Function Assignment

While ARU dominates (10 of 12), NOT all ARU models are F5-primary. The Building/F5
directory documents the COMPLETE ARU unit + 2 non-ARU models for organizational coherence:

| Primary Function | Models | Count |
|-----------------|--------|-------|
| F5 Emotion (ARU) | VMM, AAC, CLAM, CMAT, TAR | 5 |
| F5 Emotion (non-ARU) | MAA, STAI | 2 |
| F6 Reward | SRP | 1 |
| F2 Prediction | PUPF | 1 |
| F4 Memory | NEMAC | 1 |
| F10 Clinical | MAD | 1 |
| F11 Development | DAP | 1 |

---

## 2. Implementation Summary

```
Implemented:     1 model (SRP relay partial), 0 F5 beliefs
Pending:         11 models (AAC, VMM, PUPF, CLAM, MAD, NEMAC, STAI,
                            DAP, CMAT, TAR, MAA)
Cross-function:  3 models (ICEM*->arousal, MEAMN*->emotional coloring,
                           CDEM*->emotional memory)

Current code:    19D mechanism output (SRP relay partial)
                 0 F5 beliefs (SRP feeds F6 beliefs)
                 ~124 H3 demands (SRP relay)

Full F5 total:   142D mechanism output (all 12 primary models)
                 ~283 H3 demands (all 12 primary models)
```

---

## 3. Belief Inventory (from BELIEF-CYCLE.md)

| # | Belief | Cat | t | Owner | Status |
|---|--------|-----|---|-------|--------|
| 1 | perceived_happy | C | 0.55 | VMM | pending |
| 2 | perceived_sad | C | 0.55 | VMM | pending |
| 3 | emotional_arousal | C | 0.5 | AAC | pending |
| 4 | nostalgia_affect | C | 0.65 | NEMAC | pending |
| 5 | mode_detection | A | -- | VMM | pending |
| 6 | emotion_certainty | A | -- | VMM | pending |
| 7 | happy_pathway | A | -- | VMM | pending |
| 8 | sad_pathway | A | -- | VMM | pending |
| 9 | chills_intensity | A | -- | AAC | pending |
| 10 | ans_dominance | A | -- | AAC | pending |
| 11 | self_referential_nostalgia | A | -- | NEMAC | pending |
| 12 | wellbeing_enhancement | A | -- | NEMAC | pending |
| 13 | driving_signal | N | -- | AAC | pending |
| 14 | nostalgia_peak_pred | N | -- | NEMAC | pending |

**Distribution**: 4 Core + 8 Appraisal + 2 Anticipation = 14 total.
Belief owners: VMM (6), AAC (4), NEMAC (4), b/g models (0 currently).

---

## 4. Depth-Ordered Pipeline

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
F1-F3 ------+
             |
             v
Depth 0:  SRP  (19D, relay, ARU)   <- striatal reward pathway [F6 primary]
          AAC  (14D, ARU)          <- autonomic-affective coupling
          VMM  (12D, ARU)          <- valence-mode mapping
             |
             v
Depth 1:  PUPF (12D, ARU)         <- psycho-neuro-pharmacological framework (reads SRP)
          CLAM (11D, ARU)          <- closed-loop affective modulation (reads AAC+SRP)
          MAD  (11D, ARU)          <- musical anhedonia disconnection (reads SRP+AAC)
          NEMAC(11D, ARU)          <- nostalgia-enhanced memory-affect (reads MEAMN relay+AAC)
          STAI (12D, SPU)          <- spectral-temporal aesthetic integration (reads VMM+AAC)
             |
             v
Depth 2:  DAP  (10D, ARU)         <- developmental affective plasticity (reads NEMAC+DMMS)
          CMAT (10D, ARU)          <- cross-modal affective transfer (reads VMM+AAC+CLAM)
          TAR  (10D, ARU)          <- therapeutic affective resonance (reads CLAM+MAD+AAC)
          MAA  (10D, PCU)          <- multifactorial atonal appreciation (reads VMM+STAI)
```

**Depth assignment rationale**:
- **Depth 0 (a)**: Read R3/H3 directly. SRP, AAC, and VMM have no mechanism dependencies.
- **Depth 1 (b)**: PUPF reads SRP. CLAM reads AAC+SRP. MAD reads SRP+AAC.
  NEMAC reads MEAMN relay (F4 cross-fn) + AAC. STAI reads VMM+AAC.
- **Depth 2 (g)**: DAP reads NEMAC + DMMS (F4 cross-fn). CMAT reads VMM+AAC+CLAM.
  TAR reads CLAM+MAD+AAC. MAA reads VMM+STAI.

---

## 5. Unit Distribution

| Unit | Primary Models | Secondary Models | Count |
|------|---------------|-----------------|-------|
| ARU | 10 (SRP, AAC, VMM, PUPF, CLAM, MAD, NEMAC, DAP, CMAT, TAR) | 0 | 10 |
| PCU | 1 (MAA) | 1 (ICEM*) | 2 |
| SPU | 1 (STAI) | 0 | 1 |
| IMU | 0 | 2 (MEAMN*, CDEM*) | 2 |

ARU is the **dominant unit** for F5 (10 of 12 primary models). Unlike F4's single-unit
architecture (all 15 in IMU), F5 spans 3 units: ARU (10), PCU (1), SPU (1).
ARU is shared with F6 -- SRP is F6-primary but housed here for organizational coherence.

---

## 6. H3 Demands (all primary models)

| Model | H3 Tuples (v1) | Law | Status |
|-------|----------------|-----|--------|
| SRP | ~124 | L0 | relay partial |
| AAC | ~50 | L0 | doc only |
| VMM | 7 | L0 | doc only |
| PUPF | 21 | L0 | doc only |
| CLAM | 12 | L0 | doc only |
| MAD | 9 | L0 | doc only |
| NEMAC | 13 | L0 | doc only |
| STAI | 14 | L0 | doc only |
| DAP | 6 | L0 | doc only |
| CMAT | 9 | L0 | doc only |
| TAR | 21 | L0 + L2 | doc only |
| MAA | 14 | L0 | doc only |

Total H3 demands from all F5 primary models: **~283 tuples**.
Implemented: **~124 tuples** (from SRP relay partial).

---

## 7. Next Steps

- [x] Implement SRP relay wrapper (ARU-a1, 19D, ~124 H3) -- partial
- [ ] Implement AAC mechanism (ARU-a2, 14D, ~50 H3)
- [ ] Implement VMM mechanism (ARU-a3, 12D, 7 H3)
- [ ] Implement PUPF mechanism (ARU-b1, 12D, 21 H3)
- [ ] Implement CLAM mechanism (ARU-b2, 11D, 12 H3)
- [ ] Implement MAD mechanism (ARU-b3, 11D, 9 H3)
- [ ] Implement NEMAC mechanism (ARU-b4, 11D, 13 H3)
- [ ] Implement STAI mechanism (SPU-b5, 12D, 14 H3)
- [ ] Implement DAP mechanism (ARU-g1, 10D, 6 H3)
- [ ] Implement CMAT mechanism (ARU-g2, 10D, 9 H3)
- [ ] Implement TAR mechanism (ARU-g3, 10D, 21 H3)
- [ ] Implement MAA mechanism (PCU-g4, 10D, 14 H3)
- [ ] Define beliefs for b/g models during implementation
- [ ] Link cross-function models (ICEM, MEAMN, CDEM) when F5 kernel is extended
