# F8 -- Learning & Plasticity

**Function**: F8 Learning & Plasticity
**Models**: 6 primary (NDU 4, SPU 2) + 8 secondary (OII[IMU], MSR[MPU], STC[MPU], EDTA[STU], MTNE[STU], PTGMP[STU], MPFS[STU], MAA[PCU])
**Beliefs**: 14 (4 Core + 8 Appraisal + 2 Anticipation)
**Total output**: 67D (EDNR 10D + TSCP 10D + CDMR 11D + SLEE 13D + ESME 11D + ECT 12D)
**H3 demands**: 92 tuples total (EDNR 16, TSCP 12, CDMR 16, SLEE 18, ESME 12, ECT 18)
**Phase**: evidence-only (Phase 5 deferred -- no relay, no kernel integration)
**Relay**: NONE -- F8 has no relay in the current kernel
**Implemented**: no F8 mechanism models yet

---

## 1. What F8 Does

F8 processes the LEARNING & PLASTICITY dimension of music -- expertise-dependent neural reorganization, timbre-specific cortical plasticity, statistical learning enhancement, mismatch negativity modulation, and the trade-offs of expertise compartmentalization. It captures how musical training reshapes neural architecture over long timescales, producing both gains (enhanced perceptual acuity) and costs (reduced cross-network flexibility).

F8 is **evidence-only** in the current kernel: mechanism models are documented but not yet implemented. F8 has NO single primary unit -- models span NDU (Neural Development Unit, 4 models) and SPU (Spectral Processing Unit, 2 models). This distributed architecture reflects the multi-domain nature of plasticity: structural reorganization (NDU) and spectral-perceptual refinement (SPU) are distinct but interacting processes.

F8 has the **highest tau values in all of C3** (0.88--0.95), reflecting the characteristically slow timescale of expertise accumulation -- these beliefs change over months/years, not seconds.

### Key Neuroscience Circuits

- **Network Reorganization**: Bilateral STG + IFG -> increased within-network connectivity, decreased between-network (compartmentalization)
- **Timbre-Specific Plasticity**: Auditory cortex N1m enhancement -> trained instrument timbre selectivity (Pantev 2001)
- **Statistical Learning**: IFG (area 47m) hub -> supramodal regularity extraction across modalities
- **Mismatch Enhancement**: STG + IFG (BA44) -> enhanced pre-attentive deviance detection (pitch/rhythm/timbre MMN)
- **Compartmentalization Trade-off**: Within-network gains vs between-network losses -> expertise cost-benefit

```
Audio -> R3 (97D) ---+--------------------------------------------
H3 tuples -----------+
                     |
                     v
Depth 0:  EDNR (10D)           <- expertise-dependent network reorganization [NDU-a]
                     |
                     v
Depth 1:  TSCP (10D)           <- timbre-specific cortical plasticity [SPU-b1]
          CDMR (11D)           <- context-dependent mismatch response [NDU-b1]
          SLEE (13D)           <- statistical learning expertise enhancement [NDU-b2]
                     |
                     v
Depth 2:  ESME (11D)           <- expertise-specific MMN enhancement [SPU-g1]
          ECT  (12D)           <- expertise compartmentalization trade-off [NDU-g1]
```

---

## 2. Complete Model Inventory

| # | Model | Unit | Tier | Depth | Output | H3 | Beliefs | Primary Fn | Status |
|---|-------|------|------|-------|--------|-----|---------|-----------|--------|
| 1 | **EDNR** | NDU | a | 0 | 10D | 16 | 2 (1C+1A) | F8 | pending |
| 2 | TSCP | SPU | b | 1 | 10D | 12 | 2 (1C+1A) | F8 | pending |
| 3 | CDMR | NDU | b | 1 | 11D | 16 | 0 | F8 | pending |
| 4 | SLEE | NDU | b | 1 | 13D | 18 | 3 (1C+2A) | F8 | pending |
| 5 | **ESME** | SPU | g | 2 | 11D | 12 | 5 (1C+3A+1N) | F8 | pending |
| 6 | **ECT** | NDU | g | 2 | 12D | 18 | 2 (1A+1N) | F8 | pending |

**Secondary (cross-function):**

| # | Model | Unit | Primary | F8 Contribution |
|---|-------|------|---------|-----------------|
| * | OII | IMU-b | F4 Memory | Oscillatory intelligence -- learning-dependent oscillation patterns |
| * | MSR | MPU-a2 | F7 Motor | Sensorimotor reorganization -- motor plasticity from training |
| * | STC | MPU-g3 | F7 Motor | Singing connectivity -- vocal training sensorimotor plasticity |
| * | EDTA | STU-b | F8 secondary | Expertise-dependent tempo accuracy |
| * | MTNE | STU-g | F8 secondary | Music training neural efficiency |
| * | PTGMP | STU-g | F8 primary | Piano training grey matter plasticity |
| * | MPFS | STU-g | F8 secondary | Musical prodigy flow state |
| * | MAA | PCU-g | F5 secondary | Multifactorial atonal appreciation |

---

## 3. Complete Belief Inventory (14)

| # | Belief | Cat | t | Owner | Mechanism Source | Status |
|---|--------|-----|---|-------|------------------|--------|
| 1 | `network_specialization` | C | 0.95 | EDNR | within-network compartmentalization, expertise-driven reorganization | pending |
| 2 | `trained_timbre_recognition` | C | 0.90 | TSCP | timbre-specific N1m cortical enhancement, instrument selectivity | pending |
| 3 | `statistical_model` | C | 0.88 | SLEE | internal distribution representation, regularity extraction | pending |
| 4 | `expertise_enhancement` | C | 0.92 | ESME | domain-specific MMN amplification, pre-attentive refinement | pending |
| 5 | `within_connectivity` | A | -- | EDNR | intra-network coupling strength measure | pending |
| 6 | `plasticity_magnitude` | A | -- | TSCP | degree of cortical reorganization from training | pending |
| 7 | `pitch_mmn` | A | -- | ESME | pitch deviance detection strength (enhanced in singers/violinists) | pending |
| 8 | `rhythm_mmn` | A | -- | ESME | rhythm deviance detection strength (enhanced in drummers/jazz) | pending |
| 9 | `timbre_mmn` | A | -- | ESME | timbre deviance detection strength (enhanced for trained instrument) | pending |
| 10 | `compartmentalization_cost` | A | -- | ECT | between-network connectivity loss from expertise | pending |
| 11 | `detection_accuracy` | A | -- | SLEE | irregularity identification rate in auditory streams | pending |
| 12 | `multisensory_binding` | A | -- | SLEE | cross-modal integration strength from training | pending |
| 13 | `expertise_trajectory` | N | -- | ESME | predicted expertise evolution (enhancement/plateau) | pending |
| 14 | `transfer_limitation` | N | -- | ECT | anticipated cross-domain transfer constraint from compartmentalization | pending |

---

## 4. Observe Formula -- placeholder

No F8 mechanism models implemented yet. F8 is evidence-only (Phase 5 deferred, no relay).
F8 Core beliefs use the HIGHEST tau values in C3 (0.88--0.95), reflecting expertise-scale
persistence -- network_specialization is slowest (tau=0.95, structural reorganization over years)
while statistical_model is fastest (tau=0.88, regularity extraction over months).

**Expertise timescale** (no relay -- future kernel):
```
EDNR: network reorganization foundation (enables all downstream expertise effects)
TSCP: timbre-specific cortical maps
SLEE: statistical learning precision
ESME: domain-specific MMN enhancement (reads EDNR + TSCP + CDMR)
ECT:  cost-benefit of compartmentalization (reads EDNR + CDMR + SLEE)
```

Multi-scale horizons (to be defined per Core belief):
```
network_specialization:     TBD (multi-scale, structural reorganization)
trained_timbre_recognition: TBD (multi-scale, timbre cortical maps)
statistical_model:          TBD (multi-scale, regularity extraction)
expertise_enhancement:      TBD (multi-scale, MMN amplification)
```

---

## 5. Multi-Scale Horizons (all F8 Core Beliefs)

| Core Belief | T_char | Horizons | Band |
|-------------|--------|----------|------|
| network_specialization | ~years | TBD | multi-scale |
| trained_timbre_recognition | ~months | TBD | multi-scale |
| statistical_model | ~weeks | TBD | multi-scale |
| expertise_enhancement | ~months | TBD | multi-scale |

---

## 6. Dependency Graph

```
                      R3 (97D) + H3
                          |
            +-------------+---------------+
            v             v               v
        EDNR (a)       TSCP (b1)      CDMR (b1)    SLEE (b2)
        10D NDU         10D SPU       11D NDU      13D NDU
            |              |              |            |
            +------+-------+--------------+            |
                   v                      v            |
               ESME (g1)              ECT (g1)         |
               11D SPU               12D NDU           |
```

### Key Dependencies

| Model | Reads From |
|-------|-----------|
| EDNR (a) | R3/H3 directly -- foundational network reorganization (NDU) |
| TSCP (b1) | R3/H3 + EDNR; timbre plasticity modulated by network state (SPU) |
| CDMR (b1) | R3/H3 + EDNR; context-dependent mismatch modulated by expertise (NDU) |
| SLEE (b2) | R3/H3 + EDNR; statistical learning enhanced by reorganization (NDU) |
| ESME (g1) | EDNR + TSCP + CDMR; expertise-specific MMN from all upstream sources (SPU) |
| ECT (g1) | EDNR + CDMR + SLEE; compartmentalization cost from reorganization + learning (NDU) |

---

## 7. Unit Architecture

### NDU -- Neural Development Unit (4 primary F8 models)

NDU is the **DOMINANT UNIT** for F8, housing 4 of 6 primary models (EDNR, CDMR, SLEE, ECT).
NDU models have variable output dimensions (10D--13D, mean 11.5D), reflecting the
heterogeneous nature of neural development and plasticity processes. EDNR is the foundational
alpha-tier model that enables all downstream expertise effects.

```
NDU models in F8:   EDNR (a)
                      |
                  CDMR (b1) --- SLEE (b2)
                      |            |
                  ECT (g1) -------+
```

### SPU -- Spectral Processing Unit (2 primary F8 models)

SPU contributes 2 models to F8: TSCP (timbre-specific plasticity, beta) and ESME
(expertise-specific MMN enhancement, gamma). These capture the perceptual refinement
dimension of plasticity -- how training enhances spectral discrimination.

```
SPU models in F8:   TSCP (b1)
                      |
                  ESME (g1) --- (also reads EDNR[NDU], CDMR[NDU])
```

F8 also receives cross-function contributions from:
- **IMU** (Integration-Memory Unit): OII (oscillatory intelligence patterns from learning)
- **MPU** (Motor Processing Unit): MSR (motor plasticity), STC (singing connectivity)
- **STU** (Spectro-Temporal Unit): EDTA (tempo accuracy), MTNE (neural efficiency), PTGMP (grey matter plasticity), MPFS (flow state)
- **PCU** (Predictive Coding Unit): MAA (atonal appreciation)

---

## 8. Documentation Structure

```
F8-Learning-and-Plasticity/
+-- 0_F8-orchestrator.md                  <- this file
+-- collections.md                         <- full model inventory
+-- mechanisms/
|   +-- 0_mechanisms-orchestrator.md       <- all 6 models documented
|   +-- ednr/ (4 layer docs)
|   +-- tscp/ (4 layer docs)
|   +-- cdmr/ (4 layer docs)
|   +-- slee/ (4 layer docs)
|   +-- esme/ (4 layer docs)
|   +-- ect/ (4 layer docs)
+-- beliefs/
    +-- 0_beliefs_orchestrator.md
    +-- ednr/ (2 belief docs)
    +-- tscp/ (2 belief docs)
    +-- slee/ (3 belief docs)
    +-- esme/ (5 belief docs)
    +-- ect/ (2 belief docs)
```

**0 models implemented.** Pending: 1 a (EDNR) + 3 b (TSCP, CDMR, SLEE) + 2 g (ESME, ECT) -- 92 H3 tuples total.
