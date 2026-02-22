# F7 -- Motor & Timing

**Function**: F7 Motor & Timing
**Models**: 10 (MPU complete unit) + 7 secondary (HMCE[STU], ETAM[STU], HGSIC[STU], TMRM[STU], WMED[PCU], MCCN[RPU], SNEM[ASU])
**Beliefs**: 17 (4 Core + 9 Appraisal + 4 Anticipation)
**Total output**: 110D (all 10 models, uniform 11D each)
**H3 demands**: ~131 tuples total (PEOM 15, MSR 22, GSSM 12, ASAP 9, DDSMI 11, VRMSME 12, SPMC 15, NSCP 14, CTBB 9, STC 12)
**Phase**: 0 (parallel with F1, motor initialization)
**Relay**: PEOM (MPU-a1) -- F7 primary relay, provides period_lock_strength/kinematic_smoothness + next_beat/velocity_pred
**Implemented**: PEOM relay done (kernel v4.0), no F7 mechanism models yet

---

## 1. What F7 Does

F7 processes the MOTOR & TIMING dimension of music -- period entrainment (body-beat synchronization), kinematic motor planning (movement efficiency), groove quality (urge to move), meter structure, auditory-motor coupling, and hierarchical temporal context. It is the **motor initialization** pathway, running in Phase 0 alongside F1 to establish the timing scaffold that all downstream Functions depend on.

F7 is in **Phase 0**: PEOM reads R3/H3 directly as the relay (a-tier); MSR and GSSM also read R3/H3 at depth 0; b-models read a outputs; g-models read a+b. F7 receives cross-function inputs from STU (HMCE temporal hierarchy, ETAM attention gating, HGSIC groove state, TMRM tempo reproduction), PCU (WMED working memory dissociation), RPU (MCCN chills motor coupling), and ASU (SNEM beat entrainment).

### Key Neuroscience Circuits

- **Beat Entrainment**: Basal ganglia + SMA + premotor cortex -> internal beat generation (period locking)
- **Auditory-Motor Coupling**: STG/STS -> premotor cortex -> motor planning (auditory-to-motor mapping)
- **Groove Circuit**: Basal ganglia + cerebellum + SMA -> desire-to-move (groove quality, syncopation)
- **Temporal Hierarchy**: Premotor cortex + prefrontal cortex -> multi-level timing (beat/bar/phrase)
- **Motor Prediction**: Cerebellum + SMA -> forward model (next beat, velocity prediction)

```
Audio -> R3 (97D) ---+--------------------------------------------
H3 tuples -----------+
                     |
                     v
Depth 0:  PEOM (11D, relay)  <- period entrainment oscillator model [MPU-a1]
          MSR  (11D)         <- motor sequence representation [MPU-a2]
          GSSM (11D)         <- groove/syncopation sensorimotor model [MPU-a3]
                     |
                     v
Depth 1:  ASAP (11D)         <- auditory-somatosensory action prediction [MPU-b1]
          DDSMI(11D)         <- dynamic desynchronization in sensorimotor integration [MPU-b2]
          VRMSME(11D)        <- vestibular-rhythmic multisensory motor encoding [MPU-b3]
          SPMC (11D)         <- supplementary/premotor cortex model [MPU-b4]
                     |
                     v
Depth 2:  NSCP (11D)         <- neural substrate of coupled periodicity [MPU-g1]
          CTBB (11D)         <- cerebellar timing in beat-based processing [MPU-g2]
          STC  (11D)         <- sensorimotor timing control [MPU-g3]
```

---

## 2. Complete Model Inventory

| # | Model | Unit | Tier | Depth | Output | H3 | Beliefs | Primary Fn | Status |
|---|-------|------|------|-------|--------|-----|---------|-----------|--------|
| 1 | **PEOM** | MPU | a | 0 | 11D | 15 | 5 (2C+2A+1N) | F7 | relay done |
| 2 | MSR | MPU | a | 0 | 11D | 22 | 0 | F7 | pending |
| 3 | GSSM | MPU | a | 0 | 11D | 12 | 0 | F7 | pending |
| 4 | ASAP | MPU | b | 1 | 11D | 9 | 0 | F7 | pending |
| 5 | DDSMI | MPU | b | 1 | 11D | 11 | 0 | F7 | pending |
| 6 | VRMSME | MPU | b | 1 | 11D | 12 | 0 | F7 | pending |
| 7 | SPMC | MPU | b | 1 | 11D | 15 | 0 | F7 | pending |
| 8 | NSCP | MPU | g | 2 | 11D | 14 | 0 | F7 | pending |
| 9 | CTBB | MPU | g | 2 | 11D | 9 | 0 | F7 | pending |
| 10 | STC | MPU | g | 2 | 11D | 12 | 0 | F7 | pending |

**Secondary (cross-function):**

| # | Model | Unit | Primary | F7 Contribution |
|---|-------|------|---------|-----------------|
| * | HMCE | STU-a1 | F2 | Motor timing context hierarchy -- 6 F7 beliefs (short/medium/long context) |
| * | ETAM | STU-b | F3 | Tempo-motor attention gating |
| * | HGSIC | STU-b5 | F7 | Groove state motor planning -- 6 F7 beliefs (groove_quality, beat/meter/coupling/preparation) |
| * | TMRM | STU-g | F5 | Tempo reproduction |
| * | WMED | PCU-b | F2 | Motor-working memory dissociation |
| * | MCCN | RPU-b2 | F6 | Chills motor coupling |
| * | SNEM | ASU-a | F3 | Beat entrainment for motor |

---

## 3. Complete Belief Inventory (17)

| # | Belief | Cat | t | Owner | Mechanism Source | Status |
|---|--------|-----|---|-------|------------------|--------|
| 1 | `period_entrainment` | C | 0.65 | PEOM | basal ganglia period locking, body-beat sync | done |
| 2 | `kinematic_efficiency` | C | 0.60 | PEOM | motor planning smoothness, movement efficiency | done |
| 3 | `groove_quality` | C | 0.55 | HGSIC | desire-to-move, syncopation-groove interaction | done |
| 4 | `context_depth` | C | 0.70 | HMCE | hierarchical temporal context level (beat/bar/phrase) | done |
| 5 | `timing_precision` | A | -- | PEOM | temporal precision of beat tracking | done |
| 6 | `period_lock_strength` | A | -- | PEOM | strength of period entrainment oscillator lock | done |
| 7 | `beat_prominence` | A | -- | HGSIC | salience of beat within rhythmic pattern | done |
| 8 | `meter_structure` | A | -- | HGSIC | hierarchical meter detection (binary/ternary/complex) | done |
| 9 | `auditory_motor_coupling` | A | -- | HGSIC | strength of auditory-to-motor mapping | done |
| 10 | `motor_preparation` | A | -- | HGSIC | motor readiness / premotor activation level | done |
| 11 | `short_context` | A | -- | HMCE | beat-level temporal context (~0.5s window) | done |
| 12 | `medium_context` | A | -- | HMCE | bar-level temporal context (~2s window) | done |
| 13 | `long_context` | A | -- | HMCE | phrase-level temporal context (~8s window) | done |
| 14 | `next_beat_pred` | N | -- | PEOM | prediction of next beat onset time | done |
| 15 | `groove_trajectory` | N | -- | HGSIC | anticipated groove evolution (intensification/relaxation) | done |
| 16 | `phrase_boundary_pred` | N | -- | HMCE | prediction of upcoming phrase boundary | done |
| 17 | `structure_pred` | N | -- | HMCE | prediction of structural change (section boundary) | done |

---

## 4. Observe Formula -- placeholder

No F7 mechanism models implemented yet. PEOM relay is done (kernel v4.0).
F7 Core beliefs use MODERATE tau (0.55-0.70), reflecting motor/timing's characteristic
persistence -- context_depth is slowest (tau=0.70, hierarchical temporal integration) while
groove_quality is fastest (tau=0.55, responsive to rhythmic changes).

**Motor timing formula** (kernel v4.0 -- PEOM relay):
```
PEOM exports: period_lock_strength, kinematic_smoothness, next_beat_pred, velocity_pred
Tempo beliefs: 6 horizons (uniform weights) via PEOM + HMCE F-layer
```

Multi-scale horizons (to be defined per Core belief):
```
period_entrainment:    TBD (multi-scale, 6 tempo horizons)
kinematic_efficiency:  TBD (multi-scale, motor planning)
groove_quality:        TBD (multi-scale, syncopation-groove)
context_depth:         TBD (multi-scale, hierarchical context)
```

---

## 5. Multi-Scale Horizons (all F7 Core Beliefs)

| Core Belief | T_char | Horizons | Band |
|-------------|--------|----------|------|
| period_entrainment | ~0.5s | 6 (tempo) | multi-scale |
| kinematic_efficiency | ~1s | TBD | multi-scale |
| groove_quality | ~2s | TBD | multi-scale |
| context_depth | ~4s | TBD | multi-scale |

---

## 6. Dependency Graph

```
                      R3 (97D) + H3
                          |
        +-----------------+------------------+
        v                 v                  v
    PEOM (a1)         MSR (a2)          GSSM (a3)
    11D relay          11D               11D
        |                |                  |
   +----+----+    +------+------+    +------+
   v         v    v             v    v      v
ASAP(b1) DDSMI(b2) VRMSME(b3) SPMC(b4)
  11D      11D       11D       11D
   |         |         |         |
   +----+----+---------+---------+
   v    v              v         v
NSCP(g1) CTBB(g2)   STC(g3)
  11D      11D        11D
```

### Key Dependencies

| Model | Reads From |
|-------|-----------|
| PEOM (a1) | R3/H3 directly (relay) -- provides motor timing from MPU |
| MSR (a2) | R3/H3 directly -- motor sequence representation |
| GSSM (a3) | R3/H3 directly -- groove/syncopation sensorimotor model |
| ASAP (b1) | PEOM, MSR; auditory-somatosensory action prediction |
| DDSMI (b2) | PEOM, MSR; dynamic desynchronization sensorimotor integration |
| VRMSME (b3) | PEOM, GSSM; vestibular-rhythmic multisensory motor encoding |
| SPMC (b4) | MSR, GSSM; supplementary/premotor cortex model |
| NSCP (g1) | ASAP, DDSMI; neural substrate of coupled periodicity |
| CTBB (g2) | DDSMI, VRMSME; cerebellar timing in beat-based processing |
| STC (g3) | VRMSME, SPMC; sensorimotor timing control |

---

## 7. Unit Architecture

### MPU -- Motor Processing Unit (10 primary F7 models)

MPU is the **DOMINANT UNIT** for F7, housing ALL 10 primary models.
MPU is **PERFECTLY UNIFORM** -- every model produces exactly 11D output (mean 11.0D,
range 11-11D). This is the only unit in the system with zero output-dimension variance.
Motor signals are dimensionally consistent across all tiers.

```
MPU models in F7:   PEOM --- MSR --- GSSM
                      |        |       |
                    ASAP --- DDSMI -- VRMSME --- SPMC
                      |        |       |           |
                    NSCP --- CTBB --- STC
```

F7 also receives cross-function contributions from:
- **STU** (Spectro-Temporal Unit): HMCE (temporal hierarchy), ETAM (tempo-motor attention), HGSIC (groove state), TMRM (tempo reproduction)
- **PCU** (Predictive Coding Unit): WMED (motor-working memory dissociation)
- **RPU** (Reward Processing Unit): MCCN (chills motor coupling)
- **ASU** (Attention-Salience Unit): SNEM (beat entrainment for motor)

---

## 8. Documentation Structure

```
F7-Motor-and-Timing/
+-- 0_F7-orchestrator.md                  <- this file
+-- collections.md                         <- full model inventory
+-- mechanisms/
|   +-- 0_mechanisms-orchestrator.md       <- all 10 models documented
|   +-- peom/ (4 layer docs)
|   +-- msr/ (4 layer docs)
|   +-- gssm/ (4 layer docs)
|   +-- asap/ (4 layer docs)
|   +-- ddsmi/ (4 layer docs)
|   +-- vrmsme/ (4 layer docs)
|   +-- spmc/ (4 layer docs)
|   +-- nscp/ (4 layer docs)
|   +-- ctbb/ (4 layer docs)
|   +-- stc/ (4 layer docs)
+-- beliefs/
    +-- 0_beliefs_orchestrator.md
    +-- peom/ (5 belief docs)
    +-- hgsic/ (6 belief docs)
    +-- hmce/ (6 belief docs)
```

**1 a-tier relay done (PEOM 15 H3 tuples).** Pending: 2 a (MSR, GSSM) + 4 b (ASAP, DDSMI, VRMSME, SPMC) + 3 g (NSCP, CTBB, STC) -- ~116 H3 tuples remaining.
