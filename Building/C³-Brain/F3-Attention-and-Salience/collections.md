# F3 Attention & Salience — Collections

> **NOTE**: This file was built by independently reading each model doc
> in `Docs/C³/Models/` and cross-referencing `Building/Ontology/C³/MODEL-ATLAS.md`.
> It does NOT copy from the orchestrator or ontology summaries.
> Counts and dimensions are snapshots — they will change as models are integrated.

---

## 1. Verified F3 Models (from Model Docs + MODEL-ATLAS v2.0)

Independent scan of all 96 model docs + MODEL-ATLAS v2.0 function assignments identified
**11 primary** + **3 secondary** models for F3 (Attention & Salience). Models come from
3 units (ASU primary, STU secondary, PCU one model) plus cross-function contributions.

### 1.1 Implemented (1 model — relay only)

| Model | Unit-Tier | Doc OUTPUT_DIM | Code OUTPUT_DIM | Layers | H³ (v1) | Beliefs | Status |
|-------|-----------|----------------|-----------------|--------|---------|---------|--------|
| SNEM | ASU-α1 | 12D | 12D | E3+M3+P3+F3 | 18 | 4 (2C+1A+1N) | relay done |

SNEM is the F3 relay (kernel relay wrapper in `brain/kernel/`). It reads R³/H³ directly.
The relay exports `beat_locked`, `entrainment_strength`, `selective_gain`, `beat_onset_pred`.
F3 mechanism code beyond the relay is a stub (`brain/functions/f3/__init__.py`).

### 1.2 Not Yet Implemented (10 primary models)

| Model | Unit-Tier | Doc OUTPUT_DIM | Layers | H³ (v1) | Beliefs | Status |
|-------|-----------|----------------|--------|---------|---------|--------|
| IACM | ASU-α2 | 11D | E3+M3+P2+F3 | 16 | 3 (1C+1A+1N) | pending |
| BARM | ASU-β1 | 10D | E3+M2+P2+F3 | 14 | 0 | pending |
| STANM | ASU-β2 | 11D | E3+M3+P2+F3 | 16 | 0 | pending |
| AACM | ASU-β3 | 10D | E3+M2+P2+F3 | 12 | 2 (2A) | pending |
| DGTP | ASU-γ2 | 9D | E3+M2+P2+F2 | 9 | 0 | pending |
| SDL | ASU-γ3 | 9D | E3+M2+P2+F2 | 18 | 0 | pending |
| AMSS | STU-β1 | 11D | E5+M2+P2+F2 | 16 | 0 | pending |
| ETAM | STU-β4 | 11D | E4+M2+P2+F3 | 20 | 0 | pending |
| NEWMD | STU-γ2 | 10D | E4+M2+P2+F2 | 16 | 0 | pending |
| IGFE | PCU-γ1 | 9D | E4+P3+F2 | 18 | 0 | pending |

### 1.3 Full Model Descriptions

| Model | Full Name | Evidence Tier | Key Mechanism |
|-------|-----------|---------------|---------------|
| SNEM | Sensory Novelty and Expectation Model | α (>90%) | Beat-locked oscillation, selective gain, entrainment |
| IACM | Inharmonicity-Attention Capture Model | α (>90%) | Inharmonic events capture involuntary attention |
| BARM | Brainstem Auditory Response Modulation | β (70-90%) | Beat ability regulatory, brainstem modulation |
| STANM | Spectrotemporal Attention Network Model | β (70-90%) | Spectrotemporal attention allocation |
| AACM | Aesthetic-Attention Coupling Model | β (70-90%) | Preferred intervals increase attention+inhibition |
| DGTP | Domain-General Temporal Processing | γ (50-70%) | Cross-domain timing, non-music specific |
| SDL | Salience-Dependent Lateralization | γ (50-70%) | Hemispheric engagement shifts with salience |
| AMSS | Attention-Modulated Stream Segregation | β (70-90%) | Auditory stream segregation via attention |
| ETAM | Entrainment, Tempo & Attention Modulation | β (70-90%) | Tempo-attention coupling, entrainment index |
| NEWMD | Neural Entrainment-Working Memory Dissociation | γ (<70%) | Entrainment vs WM trade-off paradox |
| IGFE | Individual Gamma Frequency Enhancement | γ (50-70%) | Individual gamma frequency for binding |

### 1.4 Cross-Function — Secondary Models Contributing to F3

| Model | Unit-Tier | Primary Function | F3 Contribution |
|-------|-----------|-----------------|-----------------|
| CSG | ASU-α3 | F1 Sensory | 4 beliefs: salience_network_activation (C) + sensory_load (A) + consonance_valence_mapping (A) + processing_load_pred (N) |
| SDD | NDU-α2 | F2 Prediction | Deviance detection evidence feeds salience |
| PWSM | ASU-γ1 | F2 Prediction | Precision-weighted salience context |

CSG is the most significant cross-function contributor: it owns an F3 **Core belief**
(`salience_network_activation`). This is analogous to STAI (F5 primary) owning F1 beliefs.

---

## 2. Implementation Summary

```
Implemented:     1 model (SNEM relay), 4 F3 beliefs from α models
Pending:         10 models (IACM, BARM, STANM, AACM, DGTP, SDL, AMSS, ETAM, NEWMD, IGFE)
Cross-function:  3 models (CSG→4 beliefs, SDD→evidence, PWSM→evidence)

Current code:    12D mechanism output (SNEM relay)
                 4 beliefs (from SNEM+CSG — see §3)
                 18 H³ demands (SNEM relay)

Full F3 total:   113D mechanism output (all 11 primary models)
                 173 H³ demands (all 11 primary models)
```

---

## 3. Belief Inventory (from BELIEF-CYCLE.md)

| # | Belief | Cat | τ | Owner | Status |
|---|--------|-----|---|-------|--------|
| 1 | beat_entrainment | C | 0.35 | SNEM | relay done |
| 2 | meter_hierarchy | C | 0.4 | SNEM | relay done |
| 3 | attention_capture | C | 0.25 | IACM | pending |
| 4 | salience_network_activation | C | 0.3 | CSG | cross-function (F1) |
| 5 | selective_gain | A | — | SNEM | relay done |
| 6 | object_segregation | A | — | IACM | pending |
| 7 | sensory_load | A | — | CSG | cross-function (F1) |
| 8 | consonance_valence_mapping | A | — | CSG | cross-function (F1) |
| 9 | aesthetic_engagement | A | — | AACM | pending |
| 10 | savoring_effect | A | — | AACM | pending |
| 11 | precision_weighting | A | — | IACM | pending |
| 12 | beat_onset_pred | N | — | SNEM | relay done |
| 13 | meter_position_pred | N | — | SNEM | pending (SNEM relay exports partial) |
| 14 | attention_shift_pred | N | — | IACM | pending |
| 15 | processing_load_pred | N | — | CSG | cross-function (F1) |

**Distribution**: 4 Core + 7 Appraisal + 4 Anticipation = 15 total.
Belief owners: SNEM (5), IACM (3), CSG (4), AACM (2), β/γ models (0 currently).

---

## 4. Depth-Ordered Pipeline

```
R³ (97D) ───┬────────────────────────────────────────────
H³ tuples ──┤
            ▼
Depth 0:  SNEM  (12D, relay, ASU)  ← sensory novelty + entrainment
          IACM  (11D, ASU)         ← inharmonicity attention capture
          CSG*  (12D, relay, ASU)  ← consonance-salience gradient [F1 primary]
            │
            ▼
Depth 1:  BARM  (10D, ASU)        ← brainstem auditory response (reads SNEM)
          STANM (11D, ASU)        ← spectrotemporal attention network
          AACM  (10D, ASU)        ← aesthetic-attention coupling (reads CSG)
          AMSS  (11D, STU)        ← attention-modulated stream segregation
          ETAM  (11D, STU)        ← entrainment-tempo-attention modulation
            │
            ▼
Depth 2:  DGTP  (9D, ASU)         ← domain-general temporal (reads BARM+SNEM)
          SDL   (9D, ASU)         ← salience-dependent lateralization (reads STANM+PWSM*)
          NEWMD (10D, STU)        ← entrainment-WM dissociation
          IGFE  (9D, PCU)         ← individual gamma frequency (reads WMED [F2])
```

**Depth assignment rationale**:
- **Depth 0 (α)**: Read R³/H³ directly. SNEM and IACM have no mechanism dependencies.
  CSG operates at depth 0 but belongs to F1.
- **Depth 1 (β)**: BARM reads SNEM. AACM reads CSG. AMSS reads HMCE.
  ETAM reads HMCE+AMSC.
- **Depth 2 (γ)**: DGTP reads BARM+SNEM. SDL reads STANM+PWSM. NEWMD reads AMSC+HMCE.
  IGFE reads WMED (F2 β-tier).

---

## 5. Unit Distribution

| Unit | Primary Models | Secondary Models | Count |
|------|---------------|-----------------|-------|
| ASU | 7 (SNEM, IACM, BARM, STANM, AACM, DGTP, SDL) | 2 (CSG*, PWSM*) | 9 |
| STU | 3 (AMSS, ETAM, NEWMD) | 0 | 3 |
| PCU | 1 (IGFE) | 0 | 1 |
| NDU | 0 | 1 (SDD*) | 1 |

ASU is the dominant unit (7 of 11 primary). The most uniform mechanism signature
in the system: all ASU models use beat + auditory-scene mechanisms.

---

## 6. H³ Demands (all primary models)

| Model | H³ Tuples (v1) | Law | Status |
|-------|----------------|-----|--------|
| SNEM | 18 | L0 | relay done |
| IACM | 16 | L0 | doc only |
| BARM | 14 | L0 | doc only |
| STANM | 16 | L0 | doc only |
| AACM | 12 | L0 | doc only |
| DGTP | 9 | L0 | doc only |
| SDL | 18 | L0 | doc only |
| AMSS | 16 | L0 | doc only |
| ETAM | 20 | L0 + L2 | doc only |
| NEWMD | 16 | L0 | doc only |
| IGFE | 18 | L0 + L2 | doc only |

Total H³ demands from all F3 primary models: **173 tuples**.
Implemented: **18 tuples** (from SNEM relay).

---

## 7. Next Steps

- [x] Implement SNEM relay wrapper (ASU-α1, 12D, 18 H³) — done
- [ ] Implement IACM mechanism (ASU-α2, 11D, 16 H³)
- [ ] Implement BARM mechanism (ASU-β1, 10D, 14 H³)
- [ ] Implement STANM mechanism (ASU-β2, 11D, 16 H³)
- [ ] Implement AACM mechanism (ASU-β3, 10D, 12 H³)
- [ ] Implement DGTP mechanism (ASU-γ2, 9D, 9 H³)
- [ ] Implement SDL mechanism (ASU-γ3, 9D, 18 H³)
- [ ] Implement AMSS mechanism (STU-β1, 11D, 16 H³)
- [ ] Implement ETAM mechanism (STU-β4, 11D, 20 H³)
- [ ] Implement NEWMD mechanism (STU-γ2, 10D, 16 H³)
- [ ] Implement IGFE mechanism (PCU-γ1, 9D, 18 H³)
- [ ] Define beliefs for β/γ models during implementation
- [ ] Link CSG cross-function beliefs when F3 kernel is extended
