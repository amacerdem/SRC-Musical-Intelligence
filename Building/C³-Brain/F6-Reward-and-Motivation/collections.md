# F6 Reward & Motivation -- Collections

> **NOTE**: This file was built by independently reading each model doc
> in `Docs/C3/Models/` and cross-referencing `Building/Ontology/C3/MODEL-ATLAS.md`.
> It does NOT copy from the orchestrator or ontology summaries.
> Counts and dimensions are snapshots -- they will change as models are integrated.

---

## 1. Verified F6 Models (from Model Docs + MODEL-ATLAS v2.0)

Independent scan of all 96 model docs + MODEL-ATLAS v2.0 function assignments identified
**11 primary** + **5 secondary** models for F6 (Reward & Motivation). The dominant unit is
RPU (Reward Processing Unit) with 10 of 11 models. One non-RPU model provides the relay:
SRP (ARU). Cross-function contributions come from ARU, PCU, SPU, and ASU.

### 1.1 Implemented (2 models -- relays done)

| Model | Unit-Tier | Doc OUTPUT_DIM | Code OUTPUT_DIM | Layers | H3 (v1) | Beliefs | Status |
|-------|-----------|----------------|-----------------|--------|---------|---------|--------|
| SRP | ARU-a1 | 19D | 19D | E5+M5+P4+F5 | ~124 | 10 (5C+2A+3N) | relay done |
| DAED | RPU-a1 | 8D | 8D | E4+M2+P2+F0 | 16 | 6 (3A+3N) | relay done |

SRP is the F6 primary relay (kernel relay wrapper in `brain/kernel/`). It reads R3/H3 directly.
The relay exports `wanting`, `liking`, `pleasure` + `tension`, `reward`, `chills`, `resolution`.
SRP is housed in ARU alongside F5 models but is F6-primary (reward pathway).
DAED is the secondary belief owner (dopamine dissociation). It reads R3/H3 + BCH + MEAMN cross-relays.
F6 mechanism code beyond the relays is a stub (`brain/functions/f6/__init__.py`).

### 1.2 Not Yet Implemented (9 primary models)

| Model | Unit-Tier | Doc OUTPUT_DIM | Layers | H3 (v1) | Beliefs | Status |
|-------|-----------|----------------|--------|---------|---------|--------|
| MORMR | RPU-a2 | 7D | E4+M1+P1+F1 | 15 | 0 | pending |
| RPEM | RPU-a3 | 8D | E4+M2+P2+F0 | 16 | 0 | pending |
| IUCP | RPU-b1 | 6D | E4+P1+F1 (no M) | 14 | 0 | pending |
| MCCN | RPU-b2 | 7D | E4+P2+F1 (no M) | 16 | 0 | pending |
| MEAMR | RPU-b3 | 6D | E4+P1+F1 (no M) | 14 | 0 | pending |
| SSRI | RPU-b4 | 11D | E3+M2+P3+F3 | 18 | 0 | pending |
| LDAC | RPU-g1 | 6D | E4+P1+F1 (no M) | 12 | 0 | pending |
| IOTMS | RPU-g2 | 5D | E4+P1+F0 | 12 | 0 | pending |
| SSPS | RPU-g3 | 6D | E4+P1+F1 (no M) | 14 | 0 | pending |

### 1.3 Full Model Descriptions

| Model | Full Name | Evidence Tier | Key Mechanism |
|-------|-----------|---------------|---------------|
| SRP | Striatal Reward Prediction | a (>90%) | Reward pathway, wanting/liking, chills, tension-resolution |
| DAED | Dopamine Anticipation-Experience Dissociation | a (>90%) | Caudate anticipation vs NAcc experience, DA temporal separation |
| MORMR | mu-Opioid Receptor Music Reward | a (>90%) | Opioid-mediated consummatory pleasure, feeds ARU |
| RPEM | Reward Prediction Error in Music | a (>90%) | TD error computation, prediction update; intra DAED, MORMR |
| IUCP | Inverted-U Complexity Preference | b (70-90%) | Optimal complexity zone, Wundt curve, feeds IMU |
| MCCN | Musical Chills Cortical Network | b (70-90%) | Chills cortical pathway, arousal; ->ARU (chills, arousal) |
| MEAMR | Music-Evoked Autobiographical Memory Reward | b (70-90%) | Nostalgia-reward coupling; ->IMU (familiarity, encoding) |
| SSRI | Social Synchrony Reward Integration | b (70-90%) | Social bonding, coordinated pleasure; ->STU, ->ARU |
| LDAC | Liking-Dependent Auditory Cortex | g (50-70%) | Reward modulates auditory cortex gain; ->ASU (sensory_gain) |
| IOTMS | Individual Opioid Tone Music Sensitivity | g (50-70%) | Individual differences in opioid-mediated sensitivity; ->ARU |
| SSPS | Saddle-Shaped Preference Surface | g (50-70%) | Complexity-familiarity interaction surface; ->IMU (optimal zone) |

### 1.4 Cross-Function -- Secondary Models Contributing to F6

| Model | Unit-Tier | Primary Function | F6 Contribution |
|-------|-----------|-----------------|-----------------|
| PUPF | ARU-b1 | F2 Prediction | Pharmacological reward modulation (DA/serotonin/endorphin) |
| MAD | ARU-b3 | F10 Clinical | Anhedonia / reward lesion disconnection |
| UDP | PCU-b | F2 Prediction | Surprise -> pleasure pathway |
| STAI | SPU-b | F1 Sensory | Aesthetic -> reward feedback |
| AACM | ASU-b | F3 Attention | Liking -> attention feedback loop |

### 1.5 Cross-Function Assignment

While RPU dominates (10 of 11), NOT all RPU models are F6-primary. The Building/F6
directory documents the COMPLETE RPU unit + 1 ARU relay for organizational coherence:

| Primary Function | Models | Count |
|-----------------|--------|-------|
| F6 Reward (RPU) | DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, SSRI, LDAC, IOTMS, SSPS | 10 |
| F6 Reward (ARU relay) | SRP | 1 |

RPU models also contribute to other functions:
- **F1 Sensory**: LDAC (liking-dependent auditory cortex)
- **F2 Prediction**: RPEM (reward prediction error), IUCP (complexity preference), SSPS (preference surface)
- **F4 Memory**: MEAMR (autobiographical memory reward)
- **F7 Motor**: MCCN (chills cortical network)
- **F9 Social**: SSRI (social synchrony reward)

---

## 2. Implementation Summary

```
Implemented:     2 models (SRP relay done, DAED relay done), 16 F6 beliefs
Pending:         9 models (MORMR, RPEM, IUCP, MCCN, MEAMR, SSRI,
                           LDAC, IOTMS, SSPS)
Cross-function:  5 models (PUPF*->pharmacological, MAD*->anhedonia,
                           UDP*->surprise, STAI*->aesthetic, AACM*->liking)

Current code:    27D mechanism output (SRP 19D relay + DAED 8D relay)
                 16 F6 beliefs (SRP 10 + DAED 6)
                 ~140 H3 demands (SRP ~124 + DAED 16)

Full F6 total:   89D mechanism output (all 11 primary models)
                 ~271 H3 demands (all 11 primary models)
```

---

## 3. Belief Inventory (from BELIEF-CYCLE.md)

| # | Belief | Cat | t | Owner | Status |
|---|--------|-----|---|-------|--------|
| 1 | wanting | C | 0.6 | SRP | done |
| 2 | liking | C | 0.65 | SRP | done |
| 3 | pleasure | C | 0.7 | SRP | done |
| 4 | prediction_error | C | 0.5 | SRP | done |
| 5 | tension | C | 0.55 | SRP | done |
| 6 | prediction_match | A | -- | SRP | done |
| 7 | peak_detection | A | -- | SRP | done |
| 8 | harmonic_tension | A | -- | SRP | done |
| 9 | dissociation_index | A | -- | DAED | done |
| 10 | temporal_phase | A | -- | DAED | done |
| 11 | da_caudate | A | -- | DAED | done |
| 12 | da_nacc | A | -- | DAED | done |
| 13 | wanting_ramp | N | -- | DAED | done |
| 14 | chills_proximity | N | -- | SRP | done |
| 15 | resolution_expectation | N | -- | SRP | done |
| 16 | reward_forecast | N | -- | SRP | done |

**Distribution**: 5 Core + 7 Appraisal + 4 Anticipation = 16 total.
Belief owners: SRP (10), DAED (6), b/g models (0 currently).

---

## 4. Depth-Ordered Pipeline

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
F1-F8 PEs --+
             |
             v
Depth 0:  SRP  (19D, relay, ARU)   <- striatal reward pathway [F6 primary]
          DAED (8D, RPU)           <- dopamine anticipation-experience dissociation
          MORMR(7D, RPU)           <- mu-opioid receptor music reward
          RPEM (8D, RPU)           <- reward prediction error in music
             |
             v
Depth 1:  IUCP (6D, RPU)          <- inverted-U complexity preference (reads SRP+MORMR)
          MCCN (7D, RPU)          <- musical chills cortical network (reads SRP+DAED)
          MEAMR(6D, RPU)          <- music-evoked autobiographical memory reward (reads MEAMN relay+SRP)
          SSRI (11D, RPU)         <- social synchrony reward integration (reads SRP+DAED)
             |
             v
Depth 2:  LDAC (6D, RPU)          <- liking-dependent auditory cortex (reads IUCP+MCCN)
          IOTMS(5D, RPU)          <- individual opioid tone music sensitivity (reads MORMR+DAED)
          SSPS (6D, RPU)          <- saddle-shaped preference surface (reads IUCP+MEAMR)
```

**Depth assignment rationale**:
- **Depth 0 (a)**: Read R3/H3 directly. SRP, DAED, MORMR, and RPEM have no mechanism dependencies.
- **Depth 1 (b)**: IUCP reads SRP+MORMR. MCCN reads SRP+DAED. MEAMR reads MEAMN relay (F4 cross-fn) + SRP. SSRI reads SRP+DAED.
- **Depth 2 (g)**: LDAC reads IUCP+MCCN (feeds ASU sensory_gain). IOTMS reads MORMR+DAED (feeds ARU individual sensitivity). SSPS reads IUCP+MEAMR (feeds IMU optimal zone).

---

## 5. Unit Distribution

| Unit | Primary Models | Secondary Models | Count |
|------|---------------|-----------------|-------|
| RPU | 10 (DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, SSRI, LDAC, IOTMS, SSPS) | 0 | 10 |
| ARU | 1 (SRP) | 2 (PUPF*, MAD*) | 3 |
| PCU | 0 | 1 (UDP*) | 1 |
| SPU | 0 | 1 (STAI*) | 1 |
| ASU | 0 | 1 (AACM*) | 1 |

RPU is the **dominant unit** for F6 (10 of 11 primary models). RPU produces the
**smallest outputs** in the system (mean 7.0D, range 5-11D). Reward signals are
dimensionally compact. Only SSRI (11D, social synchrony) breaks this pattern.
SRP (ARU) is the relay -- F6-primary but housed in ARU alongside F5 models.

---

## 6. H3 Demands (all primary models)

| Model | H3 Tuples (v1) | Law | Status |
|-------|----------------|-----|--------|
| SRP | ~124 | L0 | relay done |
| DAED | 16 | L0 | relay done |
| MORMR | 15 | L0 | doc only |
| RPEM | 16 | L0 | doc only |
| IUCP | 14 | L0 | doc only |
| MCCN | 16 | L0 | doc only |
| MEAMR | 14 | L0 | doc only |
| SSRI | 18 | L0 | doc only |
| LDAC | 12 | L0 | doc only |
| IOTMS | 12 | L0 | doc only |
| SSPS | 14 | L0 | doc only |

Total H3 demands from all F6 primary models: **~271 tuples**.
Implemented: **~140 tuples** (from SRP relay done + DAED relay done).

---

## 7. Next Steps

- [x] Implement SRP relay wrapper (ARU-a1, 19D, ~124 H3) -- done
- [x] Implement DAED relay wrapper (RPU-a1, 8D, 16 H3) -- done
- [ ] Implement MORMR mechanism (RPU-a2, 7D, 15 H3)
- [ ] Implement RPEM mechanism (RPU-a3, 8D, 16 H3)
- [ ] Implement IUCP mechanism (RPU-b1, 6D, 14 H3)
- [ ] Implement MCCN mechanism (RPU-b2, 7D, 16 H3)
- [ ] Implement MEAMR mechanism (RPU-b3, 6D, 14 H3)
- [ ] Implement SSRI mechanism (RPU-b4, 11D, 18 H3)
- [ ] Implement LDAC mechanism (RPU-g1, 6D, 12 H3)
- [ ] Implement IOTMS mechanism (RPU-g2, 5D, 12 H3)
- [ ] Implement SSPS mechanism (RPU-g3, 6D, 14 H3)
- [ ] Define beliefs for b/g models during implementation
- [ ] Link cross-function models (PUPF, MAD, UDP, STAI, AACM) when F6 kernel is extended
