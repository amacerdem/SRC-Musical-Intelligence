# F4 — Memory Systems

**Function**: F4 Memory Systems
**Models**: 15 IMU models (all from IMU — Integrative Memory Unit) + 6 cross-function models
**Beliefs**: 13 (4 Core + 7 Appraisal + 2 Anticipation)
**Total output**: 159D (all 15 IMU primary models)
**H3 demands**: 288 tuples total (19+15+21+28+18+24+22+16+16+18+18+20+15+15+18)
**Phase**: 2 (reads F1-F3 beliefs + macro H3)
**Relay**: MEAMN (IMU-a1) -- implemented in kernel v4.0
**Implemented**: MEAMN relay (1/15 models, 7/13 beliefs partial from MEAMN)

---

## 1. What F4 Does

F4 manages all forms of musical memory -- autobiographical retrieval, episodic encoding, familiarity recognition, melody preservation, and cross-modal memory consolidation. It is the LARGEST C3 unit (15 models, 213 papers, 471 claims). Processing flows from autobiographical memory retrieval through episodic encoding to memory consolidation.

F4 is in **Phase 2**: it reads F1-F3 beliefs plus macro H3 horizons. The MEAMN relay (a-tier) reads R3/H3 directly; b-models read a outputs + F1-F3 beliefs; g-models read a+b. F4 receives cross-function inputs from STU(HMCE, TMRM), RPU(MEAMR), ARU(NEMAC), PCU(SPH).

### Key Neuroscience Circuits

- **Hippocampal-Cortical Memory Circuit**: Hippocampus + mPFC + PCC -> episodic encoding and retrieval
- **Default Mode Network (DMN)**: mPFC + PCC + angular gyrus -> autobiographical memory
- **Amygdala-Memory Pathway**: Amygdala -> emotional coloring of memories
- **SMA/ACC Preservation**: SMA + pre-SMA + ACC -> preserved semantic musical memory in AD

```
Audio -> R3 (97D) ---+--------------------------------------------
H3 tuples -----------+
                     |
                     v
Depth 0:  MEAMN (12D, relay)  <- autobiographical memory retrieval
          PNH   (11D)         <- Pythagorean ratio encoding
          MMP   (12D)         <- musical mnemonic preservation (clinical)
                     |
                     v
Depth 1:  RASN  (11D)  <- rhythmic auditory stimulation
          PMIM  (11D)  <- predictive memory integration
          OII   (10D)  <- oscillatory intelligence integration
          HCMC  (11D)  <- hippocampal-cortical memory circuit
          RIRI  (10D)  <- RAS rehabilitation integration
          MSPBA (11D)  <- musical syntax in Broca's area
                     |
                     v
Depth 2:  VRIAP (10D)  <- VR-integrated analgesia
          TPRD  (10D)  <- tonotopy-pitch dissociation
          CMAPCC(10D)  <- cross-modal action-perception
          DMMS  (10D)  <- developmental music memory scaffold
          CSSL  (10D)  <- cross-species song learning
          CDEM  (10D)  <- context-dependent emotional memory
```

---

## 2. Complete Model Inventory

| # | Model | Unit | Tier | Depth | Output | H3 | Beliefs | Status |
|---|-------|------|------|-------|--------|-----|---------|--------|
| 1 | **MEAMN** | IMU | a | 0 | 12D | 19 | 7 (3C+3A+1N) | **relay done** |
| 2 | PNH | IMU | a | 0 | 11D | 15 | 0 (F1 cross-fn) | pending |
| 3 | MMP | IMU | a | 0 | 12D | 21 | 3 (0C+2A+1N) | pending |
| 4 | RASN | IMU | b | 1 | 11D | 28 | 0 | pending |
| 5 | PMIM | IMU | b | 1 | 11D | 18 | 0 | pending |
| 6 | OII | IMU | b | 1 | 10D | 24 | 0 | pending |
| 7 | HCMC | IMU | b | 1 | 11D | 22 | 3 (1C+2A+0N) | pending |
| 8 | RIRI | IMU | b | 1 | 10D | 16 | 0 | pending |
| 9 | MSPBA | IMU | b | 1 | 11D | 16 | 0 | pending |
| 10 | VRIAP | IMU | b | 2 | 10D | 18 | 0 | pending |
| 11 | TPRD | IMU | b | 2 | 10D | 18 | 0 | pending |
| 12 | CMAPCC | IMU | b | 2 | 10D | 20 | 0 | pending |
| 13 | DMMS | IMU | g | 2 | 10D | 15 | 0 | pending |
| 14 | CSSL | IMU | g | 2 | 10D | 15 | 0 | pending |
| 15 | CDEM | IMU | g | 2 | 10D | 18 | 0 | pending |

**Secondary (cross-function):**

| # | Model | Unit | Primary | F4 Contribution |
|---|-------|------|---------|-----------------|
| * | PMIM | IMU-b2 | F2 | Predictive memory integration (dual function) |
| * | HMCE | STU | F1/F2 | Temporal context for memory segmentation |
| * | TMRM | STU | F4 | Temporal memory retrieval model |
| * | MEAMR | RPU | F4 | Autobiographical memory reward pathway |
| * | NEMAC | ARU | F5 | Nostalgia-emotion coupling |
| * | SPH | PCU | F2 | Spatiotemporal prediction for memory |

---

## 3. Complete Belief Inventory (13)

| # | Belief | Cat | t | Owner | Mechanism Source | Status |
|---|--------|-----|---|-------|------------------|--------|
| 1 | **`autobiographical_retrieval`** | **C** | **0.85** | **MEAMN** | memory_state + emotional_color | **relay done** |
| 2 | **`nostalgia_intensity`** | **C** | **0.8** | **MEAMN** | nostalgia_link + memory_state | **relay done** |
| 3 | **`emotional_coloring`** | **C** | **0.75** | **MEAMN** | emotional_color + f03_emotion | **relay done** |
| 4 | `episodic_encoding` | C | 0.7 | HCMC | binding_state + segmentation | pending |
| 5 | **`retrieval_probability`** | **A** | -- | **MEAMN** | memory_state aggregation | **relay done** |
| 6 | **`memory_vividness`** | **A** | -- | **MEAMN** | retrieval + emotion interaction | **relay done** |
| 7 | **`self_relevance`** | **A** | -- | **MEAMN** | self_ref from F-layer | **relay done** |
| 8 | `melodic_recognition` | A | -- | MMP | preserved_rec + familiarity | pending |
| 9 | `memory_preservation` | A | -- | MMP | preservation_idx + hippocampal_indep | pending |
| 10 | `episodic_boundary` | A | -- | HCMC | segmentation_state | pending |
| 11 | `consolidation_strength` | A | -- | HCMC | storage_state + cortical transfer | pending |
| 12 | **`vividness_trajectory`** | **N** | -- | **MEAMN** | F-layer prediction | **relay done** |
| 13 | `memory_scaffold_pred` | N | -- | MMP | scaffold_fc prediction | pending |

---

## 4. Observe Formula -- autobiographical_retrieval (kernel v4.0)

The memory observe formula from the current kernel:

```
# Implicit (65%): H3 periodicity + stability
period_signal = mean(M14(tonalness, key_clarity, tonal_stability))
stability = mean(1 / (1 + 5*M2(features)))
implicit = 0.50*periodicity + 0.35*stability + 0.15*R3_tonal

# Explicit (35%): MEAMN memory
explicit = 0.60*memory_state + 0.25*emotional_color + 0.15*self_ref

# Combined: (0.65*implicit + 0.35*explicit) * energy_gate
# Energy gate: sigma(10 * (energy - 0.1))

# Precision: 1/(std(3 periodicity features) + 0.1) * gate
#            + MEAMN: 0.3*(memory*nostalgia) + 0.2*self_ref + 0.1*vividness
```

Multi-scale horizons (autobiographical_retrieval):
```
H10(400ms)  H13(600ms)  H16(1s)  H18(2s)
H21(8s)     H24(16s)    H28(32s) H30(64s)
```

---

## 5. Multi-Scale Horizons (all F4 Core Beliefs)

| Core Belief | T_char | Horizons | Band |
|-------------|--------|----------|------|
| autobiographical_retrieval | 8s | H10, H13, H16, H18, H21, H24, H28, H30 (8) | Macro |
| nostalgia_intensity | 5s | H13, H16, H18, H20, H21, H24 (6) | Macro |
| emotional_coloring | 2s | H13, H16, H18, H21 (4) | Macro |
| episodic_encoding | 4s | H16, H18, H20, H21 (4) | Macro |

---

## 6. Dependency Graph

```
                          R3 (97D) + H3
                              |
            +-----------------+------------------+
            v                 v                  v
        MEAMN (a1)         PNH (a2)          MMP (a3)
        12D relay          11D                12D
            |                |                  |
     +------+------+   +----+----+        +----+----+
     v      v      v   v         v        v         v
  RASN(b1) PMIM(b2) OII(b3)  MSPBA(b4)  HCMC(b5) RIRI(b6)
   11D      11D     10D       11D        11D       10D
     |        |      |         |          |         |
     +---+----+------+---------+----------+---------+
         v         v           v          v         v
      VRIAP(b7)  TPRD(b8)  CMAPCC(b9) DMMS(g1) CSSL(g2) CDEM(g3)
       10D        10D        10D       10D       10D      10D
```

### Key Dependencies

| Model | Reads From |
|-------|-----------|
| RASN (b1) | Beat-entrainment from sensorimotor circuit (F3 cross-fn) |
| PMIM (b2) | PNH; feeds MSPBA, OII, TPRD, MEAMN |
| OII (b3) | PMIM, MEAMN, HCMC, PNH, MSPBA (5 intra-unit -- most connected) |
| HCMC (b5) | MEAMN; feeds MMP, PMIM, CDEM |
| RIRI (b6) | RASN, MEAMN, MMP, HCMC |
| MSPBA (b4) | PNH; feeds PMIM, HCMC |
| VRIAP (b7) | Memory-only (no intra-unit dependencies) |
| TPRD (b8) | Pitch cross-circuit (F1 cross-fn) |
| CMAPCC (b9) | Beat cross-circuit (F3 cross-fn) |
| DMMS (g1) | Feeds ARU.DAP, ARU.NEMAC |
| CSSL (g2) | Memory-only (no intra-unit dependencies) |
| CDEM (g3) | Affect cross-circuit (F5 cross-fn) |

---

## 7. Unit Architecture

### IMU -- Integrative Memory Unit (15 primary F4 models)

IMU is a **SINGLE UNIT** (Integrative Memory Unit). ALL 15 models belong to IMU.
This is unique -- most functions span multiple units (F3 has ASU+STU+PCU).
IMU is the largest single unit in the entire C3 system.

```
IMU models in F4:   MEAMN --- PNH --- MMP
                      |        |        |
                    RASN --- PMIM --- OII --- HCMC --- RIRI --- MSPBA
                      |        |       |        |        |
                    VRIAP --- TPRD   CMAPCC --- DMMS --- CSSL --- CDEM
```

F4 also receives cross-function contributions from:
- **STU** (Sensorimotor Timing Unit): HMCE (temporal context), TMRM (temporal retrieval)
- **RPU** (Reward Prediction Unit): MEAMR (autobiographical reward pathway)
- **ARU** (Aesthetic-Reward Unit): NEMAC (nostalgia-emotion coupling)
- **PCU** (Predictive Coding Unit): SPH (spatiotemporal prediction for memory)

---

## 8. Documentation Structure

```
F4-Memory-Systems/
+-- 0_F4-orchestrator.md                  <- this file
+-- collections.md                         <- full model inventory
+-- mechanisms/
|   +-- 0_mechanisms-orchestrator.md       <- all 15 models documented
|   +-- meamn/ (4 layer docs)
|   +-- pnh/ (4 layer docs)
|   +-- mmp/ (4 layer docs)
|   +-- rasn/ (4 layer docs)
|   +-- pmim/ (4 layer docs)
|   +-- oii/ (4 layer docs)
|   +-- hcmc/ (4 layer docs)
|   +-- riri/ (4 layer docs)
|   +-- mspba/ (4 layer docs)
|   +-- vriap/ (4 layer docs)
|   +-- tprd/ (4 layer docs)
|   +-- cmapcc/ (4 layer docs)
|   +-- dmms/ (4 layer docs)
|   +-- cssl/ (4 layer docs)
|   +-- cdem/ (4 layer docs)
+-- beliefs/
    +-- 0_beliefs_orchestrator.md
    +-- meamn/ (7 belief docs)
    +-- mmp/ (3 belief docs)
    +-- hcmc/ (3 belief docs)
```

**1 a-tier relay done (MEAMN, 19 H3 tuples).** Pending: 2 a (PNH, MMP) + 6 b (RASN, PMIM, OII, HCMC, RIRI, MSPBA) + 6 b/g (VRIAP, TPRD, CMAPCC, DMMS, CSSL, CDEM) -- 269 H3 tuples total.
