# C³ Implementation Tree — Unified R³→H³→C³ DAG

**Created**: 2026-02-21, **Updated**: 2026-02-21 (v2.0 Function-based)
**Scope**: All 96 C³ models mapped to a single execution DAG
**Key insight**: Function grouping ≠ implementation order. The kernel phase schedule IS the implementation backbone.

---

## 0. The Circular Dependency Paradox

### Problem

```
consonance_t needs reward_{t-1}  (prediction uses beliefs_{t-1})
reward_t     needs consonance_t  (reward aggregates PE from consonance)
prediction   needs domain signal → domain signal needs PE feedback

→ Reward is not an independent domain — it is reward OF consonance, OF beat, OF timbre
→ Prediction is not independent — it is prediction OF each domain
→ Flat domains are WRONG. There is a Function hierarchy.
```

### Resolution: Temporal Unfolding (Already in scheduler.py)

```
Frame t:
  Phase 0:  observe(R³, H³)         ← NO dependency on reward
  Phase 2a: predict(beliefs_{t-1})   ← uses reward from PREVIOUS frame
  Phase 2b: PE = observed − predicted
  Phase 3:  reward = f(PE, salience, familiarity, DA, hedonic)

Frame t+1:
  Phase 2a: predict(beliefs_t)       ← reward_t feeds back HERE
  → Cycle broken by one-frame delay. Single pass. No iteration.
```

### Implication

The 96 models are NOT independent domains. They are nodes in ONE DAG.
Each model has three coordinates:
- **Function** (F1–F12) — runtime grouping (which brain function)
- **Phase** (WHEN it runs) — determines execution order within Function DAG
- **Unit** (anatomical origin) — metadata, shared R³/H³ infrastructure

---

## 1. The Per-Frame Execution DAG

```
LAYER 0: R³ (97D)
  ├── A[0:7]   consonance ──────────┐
  ├── B[7:12]  energy ──────────────┤
  ├── C[12:21] timbre ──────────────┤
  ├── D[21:25] change ──────────────┤ → ALL computed in
  ├── F[25:41] spectral ────────────┤   one parallel pass
  ├── G[41:51] temporal ────────────┤   (already implemented)
  ├── H[51:63] harmonic ────────────┤
  ├── J[63:83] cross-domain ────────┤
  └── K[83:97] information ─────────┘
          │
          ▼
LAYER 1: H³ (131+ tuples)
  4-tuple: (r3_idx, horizon, morph, law)
  Computed in one batch pass from R³ time series
  (already implemented)
          │
          ▼
LAYER 2: C³ Phase 0 — Sensory Grounding (F1 + F7) ─────────────────
  Independent relay observation — read ONLY R³+H³:
  ┌─────────┬──────┬────────────────┬─────┬─────┬──────────┐
  │ Relay   │ Unit │ R³ Primary     │  D  │ H³  │ Function │
  ├─────────┼──────┼────────────────┼─────┼─────┼──────────┤
  │ BCH     │ SPU  │ A,C            │  12 │  17 │ F1       │
  │ PEOM    │ MPU  │ B,D,E          │  11 │   3 │ F7       │
  │ SNEM    │ ASU  │ B,D,E          │  12 │  18 │ F3(→F7)  │
  │ MPG     │ NDU  │ B,D,E          │  10 │   2 │ F1(→F3)  │
  │ HTP     │ PCU  │ A,B,C,D,E      │  12 │   9 │ F2(→F1)  │
  │ MEAMN   │ IMU  │ A,C,D,E        │  12 │  11 │ F4       │
  │ SRP     │ ARU  │ A,B,D          │  19 │   5 │ F6       │
  └─────────┴──────┴────────────────┴─────┴─────┴──────────┘
  Cross-relay dependent (Phase 0b):
  ┌─────────┬──────┬──────────────────────────────┬──────────┐
  │ HMCE    │ STU  │ ← SNEM.beat_locked_activity   │ F2       │
  │ DAED    │ RPU  │ ← BCH.consonance + MEAMN.mem  │ F6       │
  └─────────┴──────┴──────────────────────────────┴──────────┘
  F1 beliefs: consonance(R³+BCH+HTP), pitch_salience, timbre_quality
  F7 beliefs: tempo(R³+HMCE+PEOM), groove, entrainment
  + enrichment models (same phase, parallel) — see §3
          │
          ▼
LAYER 3: C³ Phase 1 — Pattern + Attention (F2 + F3) ───────────────
  F2 beliefs: prediction_state(HTP+HMCE), temporal_expectation, IC
  F3 beliefs: salience(R³+H³+PE_prev+SNEM+MPG+SRP.tension),
              attention_allocation
          │
          ▼
LAYER 4: C³ Phase 2 — Memory + Emotion (F4 + F5) ─────────────────
  F4 beliefs: familiarity(R³+H³+MEAMN+MPG), memory_scaffold
  F5 beliefs: affect_valence(VMM+MEAMN), emotional_arousal
          │
          ▼
LAYER 5: C³ Phase 3 — Learning + Social (F8 + F9) ────────────────
  F8 beliefs: plasticity_state, expertise_level
  F9 beliefs: social_synchrony
          │
          ▼
LAYER 6: C³ Phase 4 — PE + Precision ─────────────────────────────
  PE = observed − predicted   (for ALL Function beliefs)
  precision = f(PE_history) + HTP boost
  posterior = Bayesian(likelihood, prior, precision)
          │
          ▼
LAYER 7: C³ Phase 5 — Reward (F6, terminal) ──────────────────────
  F6 beliefs: reward_valence = f(ALL PEs × precision × salience
               × familiarity + DAED.DA_gain + SRP.hedonic
               + MEAMN.emotion)
              pleasure_state, wanting_state
          │
          ▼
  Meta-Layers: F10/F11/F12 contribute evidence during Phase 0–3
               (no beliefs, no phases — evidence providers only)
          │
          ▼
OUTPUT:  beliefs(N) + PE(N) + precision(N) + reward(1) + RAM(26)
         where N = total active beliefs across 9 Functions
```

---

## 2. R³ Input Domain Map — All 96 Models

Primary R³ group that each model depends on most. This determines
shared test infrastructure and implementation grouping WITHIN each wave.

### Domain A: Consonance-Rooted (primary R³ A[0:7])

| Model | Unit | Tier | R³ Groups | D | H³ | Cross-Deps |
|-------|------|------|-----------|---|-----|------------|
| **BCH** | SPU | α1 | A,C,F,H | 12 | 17 | **RELAY** → DAED, consonance belief |
| PSCL | SPU | α2 | A,C,D,E | 12 | 14 | reads BCH |
| PCCR | SPU | α3 | A,C,D,E | 11 | 14 | → IMU, STU |
| STAI | SPU | β1 | A,B,C,D,E | 12 | 14 | → SRP |
| SDNPS | SPU | γ1 | A,C,E | 10 | 10 | intra-SPU reads BCH,PSCL,SDED,STAI |
| SDED | SPU | γ3 | A,C,E | 10 | 9 | → ARU, STU |
| CSG | ASU | α3 | A,B,C,D,E | 12 | 18 | → ARU.affect, ARU.reward |
| AACM | ASU | β3 | A,B,C,D,E | 10 | 12 | → ARU.aesthetic |
| PNH | IMU | α2 | A,B,C,E | 11 | 15 | → BCH, PSCL, SRP |
| MSPBA | IMU | β6 | A,B,D,E | 11 | 16 | PNH → MSPBA → SRP |
| TPRD | IMU | β8 | A,B,C,D,E | 10 | 18 | pitch cross-circuit |
| DMMS | IMU | γ1 | A,B,C,D,E | 10 | 15 | → DAP, NEMAC |
| NEMAC | ARU | β4 | A,B,C,D,E | 11 | 13 | SRP mod via memory |
| **DAED** | RPU | α1 | A,B,D,E | 8 | 16 | **RELAY** → reward DA gain |
| MORMR | RPU | α2 | A,B,C,D,E | 7 | 15 | → ARU; intra MCCN,DAED,IUCP,RPEM |
| RPEM | RPU | α3 | A,B,D,E | 8 | 16 | → IMU; intra DAED,MORMR |
| IOTMS | RPU | γ2 | A,B,C,E | 5 | 12 | → ARU |

### Domain B: Energy/Beat-Rooted (primary R³ B[7:12])

| Model | Unit | Tier | R³ Groups | D | H³ | Cross-Deps |
|-------|------|------|-----------|---|-----|------------|
| **SNEM** | ASU | α1 | B,D,E | 12 | 18 | **RELAY** → HMCE, salience belief |
| BARM | ASU | β1 | B,D,E | 10 | 14 | → STU |
| DGTP | ASU | γ2 | B,D,E | 9 | 9 | → STU |
| **HMCE** | STU | α1 | B,D | 13 | 18 | **RELAY** (+SNEM) → tempo belief |
| AMSC | STU | α2 | B,C,D | 12 | 16 | reads beat pathway |
| EDTA | STU | β3 | B,D | 10 | ~15 | intra AMSC,HGSIC,ETAM,OMS |
| ETAM | STU | β4 | B,D | 11 | ~20 | intra HMCE,AMSC,MDNS,AMSS |
| HGSIC | STU | β5 | B,D | 11 | ~15 | intra AMSC,ETAM,OMS,EDTA |
| TMRM | STU | γ1 | B,D | 10 | 15 | → ARU affect |
| **PEOM** | MPU | α1 | B,D,E | 11 | 15 | **RELAY** → tempo belief |
| MSR | MPU | α2 | B,D,E | 11 | 22 | → STU |
| GSSM | MPU | α3 | B,D,E | 11 | 12 | → STU |
| ASAP | MPU | β1 | B,D,E | 11 | 9 | → STU |
| SPMC | MPU | β4 | B,D,E | 11 | 15 | → STU |
| VRMSME | MPU | β3 | B,D,E | 11 | 12 | → ARU |
| CTBB | MPU | γ2 | B,D,E | 11 | 9 | → STU |
| MCCN | RPU | β2 | A,B,D,E | 7 | 16 | → ARU (chills) |
| SSRI | RPU | β4 | A,B,C,D,E | 11 | 18 | → STU, ARU |
| RASN | IMU | β1 | A,B,D,E | 11 | 28 | reads beat pathway |
| CMAPCC | IMU | β9 | A,B,E | 10 | 20 | beat cross-circuit |
| AAC | ARU | α2 | A,B,C,D,E | 14 | ~50 | shares w/ SRP |
| TAR | ARU | γ3 | A,B,C,D,E | 10 | 21 | integrates all ARU |
| CLAM | ARU | β2 | A,B,C,D,E | 11 | 12 | SRP affect basis |

### Domain C: Timbre-Rooted (primary R³ C[12:21])

| Model | Unit | Tier | R³ Groups | D | H³ | Cross-Deps |
|-------|------|------|-----------|---|-----|------------|
| TSCP | SPU | β2 | A,C,D,E | 10 | 12 | → MIAA, ESME, ARU |
| MIAA | SPU | β3 | A,B,C,D,E | 11 | 11 | ← TSCP+BCH; → IMU, STU |
| ESME | SPU | γ2 | A,B,C,D,E | 11 | 12 | ← BCH,TSCP,SDED; → ARU,IMU,STU |
| IACM | ASU | α2 | A,B,C,D,E | 11 | 16 | → ARU.affect, SPU.scene |
| STANM | ASU | β2 | B,C,D,E | 11 | 16 | → STU (temporal_alloc) |
| SDL | ASU | γ3 | B,C,D,E | 9 | 18 | → SPU (hemispheric) |
| MDNS | STU | α3 | A,B,C,D | 12 | ~18 | intra HMCE,AMSC,TPIO |
| AMSS | STU | β1 | B,C,D | 11 | 16 | → ARU |
| TPIO | STU | β2 | B,C,D | 10 | ~18 | intra HMCE,AMSC,AMSS,ETAM |
| CMAT | ARU | γ2 | A,B,C,D,E | 10 | 9 | SRP/CLAM/TAR visual |
| STC | MPU | γ3 | B,C,D,E | 11 | 12 | → ARU |

### Domain D: Change/Novelty-Rooted (primary R³ D[21:25])

| Model | Unit | Tier | R³ Groups | D | H³ | Cross-Deps |
|-------|------|------|-----------|---|-----|------------|
| **MPG** | NDU | α1 | B,C,D,E | 10 | 16 | **RELAY** → salience, familiarity |
| SDD | NDU | α2 | A,B,D,E,H | 11 | 18 | → CDMR, EDNR, SLEE |
| DSP | NDU | β1 | A,B,C,D,E | 12 | 18 | → ARU |
| CDMR | NDU | β2 | B,C,D,E,H | 11 | 16 | → ARU, IMU |
| SLEE | NDU | β3 | B,C,D,E,H | 13 | 18 | → IMU |
| SDDP | NDU | γ1 | A,B,C,D,E | 10 | 16 | → ARU (infant) |
| ONI | NDU | γ2 | B,C,D,E | 11 | 16 | → ARU |
| ECT | NDU | γ3 | A,B,C,D,E | 12 | 18 | → IMU, SPU |
| EDNR | NDU | α3 | A,B,C,E | 10 | 16 | → SDD, SLEE, ECT |
| PWSM | ASU | γ1 | A,B,D,E | 9 | 16 | → NDU |
| IUCP | RPU | β1 | A,B,D,E | 6 | 14 | → IMU |
| SSPS | RPU | γ3 | A,B,D,E | 6 | 14 | → IMU |
| LDAC | RPU | γ1 | A,B,C,D,E | 6 | 12 | → ASU |
| PUPF | ARU | β1 | A,B,C,D,E | 12 | 21 | reads SPU,STU,IMU |

### Domain E: Prediction-Rooted (primary multi-group, emphasis on precision)

| Model | Unit | Tier | R³ Groups | D | H³ | Cross-Deps |
|-------|------|------|-----------|---|-----|------------|
| **HTP** | PCU | α1 | A,B,C,D,E | 12 | 18 | **RELAY** → consonance, precision |
| SPH | PCU | α2 | A,C,D,E | 14 | 16 | → ICEM, PWUP, IMU |
| ICEM | PCU | α3 | A,B,C,D,E | 13 | 15 | → PWUP, UDP, ARU |
| PWUP | PCU | β1 | A,C,D,E | 10 | 14 | → ASU |
| WMED | PCU | β2 | B,D,E | 11 | 16 | → UDP, STU |
| UDP | PCU | β3 | A,C,D,E | 10 | 16 | → MAA, ARU |
| CHPI | PCU | β4 | A,B,C,D,E | 11 | 20 | → UDP, STU, ARU |
| IGFE | PCU | γ1 | A,B,C,E | 9 | 18 | → IMU |
| MAA | PCU | γ2 | A,C,D,E | 10 | 14 | → ARU |
| PSH | PCU | γ3 | A,B,C,D,E | 10 | 18 | → SPU |

### Domain F: Memory-Rooted (primary long-horizon H³)

| Model | Unit | Tier | R³ Groups | D | H³ | Cross-Deps |
|-------|------|------|-----------|---|-----|------------|
| **MEAMN** | IMU | α1 | A,C,D,E | 12 | 11 | **RELAY** → familiarity, reward, DAED |
| MMP | IMU | α3 | A,B,C,D,E | 12 | 21 | → HCMC, RASN, RIRI; → AAC |
| PMIM | IMU | β2 | A,B,C,D,E | 11 | 18 | PNH→PMIM; → MSPBA,OII,TPRD,MEAMN |
| OII | IMU | β3 | A,B,C,D,E | 10 | 24 | → PMIM,MEAMN,HCMC,PNH,MSPBA |
| HCMC | IMU | β4 | A,B,C,D,E | 11 | 22 | MEAMN↔HCMC; → MMP,PMIM,CDEM |
| RIRI | IMU | β5 | A,B,C,D,E | 10 | 16 | ← RASN,MEAMN,MMP,HCMC; → VRIAP |
| VRIAP | IMU | β7 | A,B,C,D,E | 10 | 18 | memory-only |
| CSSL | IMU | γ2 | A,B,C,D,E | 10 | 15 | memory-only |
| CDEM | IMU | γ3 | A,B,C,D,E | 10 | 18 | affect cross-circuit |
| MEAMR | RPU | β3 | A,B,C,D,E | 6 | 14 | → IMU (familiarity) |

### Domain G: Reward/Affect-Rooted (convergence hub)

| Model | Unit | Tier | R³ Groups | D | H³ | Cross-Deps |
|-------|------|------|-----------|---|-----|------------|
| **SRP** | ARU | α1 | A,B,D,F | 19 | ~124 | **RELAY** hub: reads SPU,STU,IMU,NDU |
| VMM | ARU | α3 | A,C,H,J | 12 | 7 | SRP+AAC shared |
| MAD | ARU | β3 | A,B,C,D,E | 11 | 9 | lesion validation of SRP |
| DAP | ARU | γ1 | A,B,C,D,E | 10 | 6 | background for ALL ARU |

### Domain H: Cross-Domain (wide R³, no single primary)

| Model | Unit | Tier | R³ Groups | D | H³ | Cross-Deps |
|-------|------|------|-----------|---|-----|------------|
| OMS | STU | β6 | B,D,E | 10 | ~15 | intra HMCE,AMSC,MDNS,HGSIC |
| NEWMD | STU | γ2 | A,B,C,D,E | 10 | — | intra AMSC,HMCE,EDTA |
| MTNE | STU | γ3 | A,B,C,D,E | 10 | — | intra HMCE,AMSC,PTGMP |
| PTGMP | STU | γ4 | B,D,E | 10 | — | intra HMCE,AMSC,TPIO |
| MPFS | STU | γ5 | B,D,E | 10 | 20 | intra HMCE,AMSC,OMS |
| DDSMI | MPU | β2 | B,D,E | 11 | 11 | → ARU (bonding) |
| NSCP | MPU | γ1 | A,B,D,E | 11 | 14 | → ARU (engagement) |

---

## 3. Implementation Waves — The Unified Plan

### Wave 0: EAR + Kernel Scaffold (DONE)

```
✓ R³ pipeline: 97D per frame (ear/r3/)
✓ H³ pipeline: batch morphology (ear/h3/)
✓ 9 relay wrappers (kernel/relays/)
✓ 5 primary beliefs (F1:cons, F7:tempo, F3:sal, F4:fam, F6:reward)
✓ precision + reward + RAM (kernel/)
✓ scheduler.py phase schedule (v1.0: 5-belief, v2.0: Function DAG)
```

### Wave 1: α-Tier Relay Models — Full Implementation (9 models)

Currently relay wrappers are SIMPLIFIED versions. Wave 1 = make each relay
match its full model doc (§11 pseudocode). Each relay serves a Function.

```
Phase 0a parallel (F1, F7, F3, F2, F4, F6 relays):
  BCH  [F1] (SPU-α1): 12D, 17 H³  — consonance hierarchy
  PEOM [F7] (MPU-α1): 11D, 15 H³  — period entrainment
  SNEM [F3] (ASU-α1): 12D, 18 H³  — beat/meter entrainment
  MPG  [F1] (NDU-α1): 10D, 16 H³  — melodic pitch gradient
  HTP  [F2] (PCU-α1): 12D, 18 H³  — hierarchical temporal prediction
  MEAMN[F4] (IMU-α1): 12D, 11 H³  — autobiographical memory
  SRP  [F6] (ARU-α1): 19D,~124 H³ — striatal reward pathway

Phase 0b sequential:
  HMCE [F2] (STU-α1): 13D, 18 H³  — needs SNEM.beat_locked
  DAED [F6] (RPU-α1):  8D, 16 H³  — needs BCH.cons + MEAMN.mem

Total: 9 models, 109D, 131 H³ tuples
```

### Wave 2: α-Tier Enrichment (18 models)

These models run PARALLEL to their unit's relay in Phase 0a/0b.
Grouped by R³ input domain for shared test infrastructure.

```
CONSONANCE cluster (shared test: pure intervals, chord progressions):
  Wave 2.1 — No cross-model deps:
    IMU-α2-PNH:  A,B,C,E → 11D  — pythagorean hierarchy
    ASU-α3-CSG:  A,B,C,D,E → 12D — consonance-salience gradient
  Wave 2.2 — Reads BCH:
    SPU-α2-PSCL: A,C,D,E → 12D  — pitch salience (reads BCH)
    SPU-α3-PCCR: A,C,D,E → 11D  — chroma (→ IMU, STU)

BEAT/TIMING cluster (shared test: metronome, syncopation):
  Wave 2.3 — No cross-model deps:
    ASU-α2-IACM: A,B,C,D,E → 11D — inharmonicity-attention
    MPU-α2-MSR:  B,D,E → 11D     — sensorimotor reorganization
    MPU-α3-GSSM: B,D,E → 11D     — gait synchronization
  Wave 2.4 — Reads HMCE/AMSC:
    STU-α2-AMSC: B,C,D → 12D     — auditory-motor coupling
    STU-α3-MDNS: A,B,C,D → 12D   — melody decoding

NOVELTY cluster (shared test: oddball paradigms):
  Wave 2.5 — No cross-model deps:
    NDU-α2-SDD:  A,B,D,E,H → 11D — deviance detection
    NDU-α3-EDNR: A,B,C,E → 10D   — expertise network

PREDICTION cluster (shared test: expectation violation):
  Wave 2.6:
    PCU-α2-SPH:  A,C,D,E → 14D   — spatiotemporal prediction
    PCU-α3-ICEM: A,B,C,D,E → 13D — information-emotion

MEMORY cluster (shared test: repeated exposure):
  Wave 2.7:
    IMU-α3-MMP:  A,B,C,D,E → 12D — musical memory preservation

REWARD cluster (shared test: liked vs disliked music):
  Wave 2.8:
    ARU-α2-AAC:  A,B,C,D,E → 14D — autonomic coupling
    ARU-α3-VMM:  A,C,H,J → 12D   — valence-mode mapping
    RPU-α2-MORMR: A,B,C,D,E → 7D — mu-opioid reward
    RPU-α3-RPEM: A,B,D,E → 8D    — reward prediction error

Total: 18 models, 204D, ~260 additional H³ tuples
```

### Wave 3: β-Tier (42 models)

β-tier models add cross-domain connections. Within each cluster,
ordered by intra-unit dependency (models that are READ come first).

```
CONSONANCE β:
  3.1a SPU-β1-STAI:  A,B,C,D,E → 12D — spectral-temporal aesthetic
  3.1b SPU-β2-TSCP:  A,C,D,E → 10D   — timbre cortical plasticity
  3.1c SPU-β3-MIAA:  A,B,C,D,E → 11D — imagery activation (← TSCP+BCH)
  3.1d IMU-β6-MSPBA: A,B,D,E → 11D   — Broca's syntax (← PNH)
  3.1e IMU-β8-TPRD:  A,B,C,D,E → 10D — tonotopy-pitch dissociation
  3.1f ARU-β4-NEMAC: A,B,C,D,E → 11D — nostalgia-affect (SRP mod)

BEAT/TIMING β:
  3.2a ASU-β1-BARM:  B,D,E → 10D     — brainstem response mod
  3.2b ASU-β2-STANM: B,C,D,E → 11D   — spectrotemporal attention
  3.2c STU-β1-AMSS:  B,C,D → 11D     — synchronization system
  3.2d STU-β2-TPIO:  B,C,D → 10D     — timbre perception-imagery
  3.2e STU-β3-EDTA:  B,D → 10D       — expertise tempo accuracy
  3.2f STU-β4-ETAM:  B,D → 11D       — entrainment-tempo-attention
  3.2g STU-β5-HGSIC: B,D → 11D       — groove state integration
  3.2h STU-β6-OMS:   B,D,E → 10D     — oscillatory motor sync
  3.2i MPU-β1-ASAP:  B,D,E → 11D     — adaptive processing
  3.2j MPU-β2-DDSMI: B,D,E → 11D     — dyadic dance
  3.2k MPU-β3-VRMSME:B,D,E → 11D     — VR motor enhancement
  3.2l MPU-β4-SPMC:  B,D,E → 11D     — SMA-premotor-M1
  3.2m IMU-β1-RASN:  A,B,D,E → 11D   — rhythmic stimulation (← beat)
  3.2n IMU-β9-CMAPCC:A,B,E → 10D     — action-perception (← beat)
  3.2o RPU-β2-MCCN:  A,B,D,E → 7D    — chills (→ ARU)
  3.2p RPU-β4-SSRI:  A,B,C,D,E → 11D — social synchrony (→ STU,ARU)
  3.2q ARU-β2-CLAM:  A,B,C,D,E → 11D — closed-loop affect

NOVELTY β:
  3.3a NDU-β1-DSP:   A,B,C,D,E → 12D — deviance-specific processing
  3.3b NDU-β2-CDMR:  B,C,D,E,H → 11D — context-dependent mismatch
  3.3c NDU-β3-SLEE:  B,C,D,E,H → 13D — statistical learning

PREDICTION β:
  3.4a PCU-β1-PWUP:  A,C,D,E → 10D   — precision-weighted update
  3.4b PCU-β2-WMED:  B,D,E → 11D     — WM-entrainment dissociation
  3.4c PCU-β3-UDP:   A,C,D,E → 10D   — uncertainty-driven pleasure
  3.4d PCU-β4-CHPI:  A,B,C,D,E → 11D — cross-modal harmonic pred.

MEMORY β:
  3.5a IMU-β2-PMIM:  A,B,C,D,E → 11D — predictive memory integration
  3.5b IMU-β3-OII:   A,B,C,D,E → 10D — oscillatory intelligence
  3.5c IMU-β4-HCMC:  A,B,C,D,E → 11D — hippocampal-cortical
  3.5d IMU-β5-RIRI:  A,B,C,D,E → 10D — rehabilitation integration
  3.5e IMU-β7-VRIAP: A,B,C,D,E → 10D — VR analgesia

REWARD β:
  3.6a RPU-β1-IUCP:  A,B,D,E → 6D    — inverted-U complexity
  3.6b RPU-β3-MEAMR: A,B,C,D,E → 6D  — memory-evoked reward
  3.6c ARU-β1-PUPF:  A,B,C,D,E → 12D — psycho-neuro-pharm
  3.6d ARU-β3-MAD:   A,B,C,D,E → 11D — anhedonia model

Total: 42 models, ~441D
```

### Wave 4: γ-Tier (27 models)

γ-tier = speculative/theoretical. Lowest priority. Many lack H³ demands.

```
CONSONANCE γ:
  4.1a SPU-γ1-SDNPS: A,C,E → 10D     — stimulus-dependent NPS
  4.1b SPU-γ2-ESME:  A,B,C,D,E → 11D — expertise MMN
  4.1c SPU-γ3-SDED:  A,C,E → 10D     — sensory dissonance
  4.1d IMU-γ1-DMMS:  A,B,C,D,E → 10D — developmental scaffold
  4.1e IMU-γ3-CDEM:  A,B,C,D,E → 10D — emotional memory

BEAT/TIMING γ:
  4.2a ASU-γ2-DGTP:  B,D,E → 9D      — domain-general temporal
  4.2b ASU-γ3-SDL:   B,C,D,E → 9D    — salience lateralization
  4.2c STU-γ1-TMRM:  B,D → 10D       — tempo memory reproduction
  4.2d STU-γ2-NEWMD: A,B,C,D,E → 10D — entrainment-WM dissociation
  4.2e STU-γ3-MTNE:  A,B,C,D,E → 10D — training neural efficiency
  4.2f STU-γ4-PTGMP: B,D,E → 10D     — piano training plasticity
  4.2g STU-γ5-MPFS:  B,D,E → 10D     — prodigy flow state
  4.2h MPU-γ1-NSCP:  A,B,D,E → 11D   — neural sync commercial
  4.2i MPU-γ2-CTBB:  B,D,E → 11D     — cerebellar theta-burst
  4.2j MPU-γ3-STC:   B,C,D,E → 11D   — singing training

NOVELTY γ:
  4.3a NDU-γ1-SDDP:  A,B,C,D,E → 10D — sex-dependent plasticity
  4.3b NDU-γ2-ONI:   B,C,D,E → 11D   — over-normalization
  4.3c NDU-γ3-ECT:   A,B,C,D,E → 12D — expertise compartment.

PREDICTION γ:
  4.4a PCU-γ1-IGFE:  A,B,C,E → 9D    — gamma frequency enhancement
  4.4b PCU-γ2-MAA:   A,C,D,E → 10D   — atonal appreciation
  4.4c PCU-γ3-PSH:   A,B,C,D,E → 10D — prediction silencing

MEMORY γ:
  4.5a IMU-γ2-CSSL:  A,B,C,D,E → 10D — cross-species song learning
  4.5b ASU-γ1-PWSM:  A,B,D,E → 9D    — precision-weighted salience

REWARD γ:
  4.6a RPU-γ1-LDAC:  A,B,C,D,E → 6D  — liking-dependent cortex
  4.6b RPU-γ2-IOTMS: A,B,C,E → 5D    — opioid tone sensitivity
  4.6c RPU-γ3-SSPS:  A,B,D,E → 6D    — preference surface
  4.6d ARU-γ1-DAP:   A,B,C,D,E → 10D — developmental plasticity
  4.6e ARU-γ2-CMAT:  A,B,C,D,E → 10D — cross-modal transfer
  4.6f ARU-γ3-TAR:   A,B,C,D,E → 10D — therapeutic resonance

Total: 27 models, ~268D
```

---

## 4. R³ Usage Heatmap (by Unit — Metadata)

Which R³ groups each unit/tier reads. Numbers = model count.
Units are metadata (anatomical origin); runtime grouping is by Function (see §7).

```
         A(cons) B(energy) C(timbre) D(change) E(interact) H/J/K
SPU α:    3/3      0/3       3/3       2/3        2/3       1(BCH)
SPU β:    3/3      2/3       3/3       2/3        3/3       0
SPU γ:    3/3      1/3       2/3       1/3        2/3       0
──────────────────────────────────────────────────────────────
ASU α:    2/3      3/3       2/3       3/3        3/3       0
ASU β:    1/3      3/3       2/3       3/3        3/3       0
ASU γ:    1/3      2/3       1/3       3/3        3/3       0
──────────────────────────────────────────────────────────────
STU α:    1/3      3/3       2/3       3/3        0/3       0
STU β:    0/6      6/6       3/6       6/6        1/6       0
STU γ:    2/5      5/5       2/5       5/5        4/5       0
──────────────────────────────────────────────────────────────
IMU α:    3/3      2/3       2/3       1/3        2/3       0
IMU β:    8/9      9/9       7/9       8/9        9/9       0
IMU γ:    3/3      3/3       3/3       3/3        3/3       0
──────────────────────────────────────────────────────────────
MPU α:    0/3      3/3       0/3       3/3        3/3       0
MPU β:    0/4      4/4       0/4       4/4        4/4       0
MPU γ:    1/3      3/3       1/3       3/3        3/3       0
──────────────────────────────────────────────────────────────
NDU α:    2/3      3/3       1/3       2/3        3/3       1(SDD)
NDU β:    1/3      3/3       3/3       3/3        3/3       2(CDMR,SLEE)
NDU γ:    2/3      3/3       2/3       3/3        3/3       0
──────────────────────────────────────────────────────────────
PCU α:    3/3      2/3       2/3       2/3        2/3       0
PCU β:    3/4      2/4       2/4       4/4        4/4       0
PCU γ:    2/3      2/3       2/3       1/3        2/3       0
──────────────────────────────────────────────────────────────
RPU α:    3/3      3/3       1/3       2/3        2/3       0
RPU β:    3/4      4/4       3/4       4/4        4/4       0
RPU γ:    2/3      2/3       1/3       2/3        2/3       0
──────────────────────────────────────────────────────────────
ARU α:    3/3      2/3       1/3       1/3        0/3       2(VMM,SRP)
ARU β:    4/4      4/4       4/4       4/4        4/4       0
ARU γ:    3/3      3/3       3/3       3/3        3/3       0

TOTALS (96 models):
  A(consonance): 82/96 = 85%  — near-universal
  B(energy):     84/96 = 88%  — near-universal
  C(timbre):     62/96 = 65%  — selective
  D(change):     79/96 = 82%  — near-universal
  E(interact):   73/96 = 76%  — common
  H/J/K:          6/96 =  6%  — rare (BCH, VMM, SRP, SDD, CDMR, SLEE)
```

### Key Finding
R³ groups A, B, D are near-universal inputs (>80%). Group C (timbre)
discriminates: timbre-rooted models vs non-timbre models. Groups H/J/K
are used by only 6 specialized models.

---

## 5. Cross-Model Dependency Graph (Code-Level)

Not all cross-unit connections in MODEL-ATLAS are code dependencies.
These are the ACTUAL read dependencies at compute() time:

### Tier 1: No Dependencies (read only R³+H³)

77 of 96 models have NO cross-model code dependencies.
They can be implemented in ANY order within their wave.

### Tier 2: Intra-Unit Dependencies

```
SPU: BCH → PSCL, MIAA, ESME, SDNPS, SDED (5 models read BCH)
     TSCP → MIAA, ESME (2 models read TSCP)
ASU: SNEM → BARM, STANM, PWSM, DGTP (4 models read SNEM)
IMU: PNH → MSPBA (1 reads PNH)
     MEAMN ↔ HCMC (bidirectional)
     MMP → HCMC, RASN, RIRI (3 read MMP)
     PMIM → MSPBA, OII, TPRD, MEAMN (4 read PMIM)
STU: HMCE → all other STU models (hub)
     AMSC → many STU β models
NDU: SDD → CDMR, SLEE (2 read SDD)
     EDNR → SDD, SLEE, ECT (3 read EDNR — bidirectional w/ SDD)
PCU: SPH → ICEM, PWUP (2 read SPH)
     ICEM → PWUP, UDP (2 read ICEM)
RPU: DAED → MORMR, RPEM (2 read DAED)
ARU: SRP → all other ARU models (hub)
```

### Tier 3: Cross-Unit Dependencies (already in kernel)

```
SNEM.beat_locked → HMCE (Phase 0b)
BCH.consonance   → DAED (Phase 0b)
MEAMN.memory     → DAED (Phase 0b)
BCH → consonance belief (Phase 0c)
HTP → consonance belief (Phase 0c)
HMCE → tempo belief (Phase 0c)
PEOM → tempo belief (Phase 0c)
SNEM → salience belief (Phase 1)
MPG → salience belief (Phase 1)
SRP.tension → salience belief (Phase 1)
MEAMN → familiarity belief (Phase 2a)
MPG → familiarity belief (Phase 2a)
HTP → precision engine (Phase 2b)
DAED → reward (Phase 3)
SRP → reward (Phase 3)
MEAMN → reward (Phase 3)
```

---

## 6. H³ Demand Aggregation by Wave

| Wave | Models | H³ Tuples (unique) | Cumulative |
|------|--------|--------------------|------------|
| 0 (kernel) | 9 | 131 | 131 |
| 1 (α enrichment) | 18 | ~260 | ~350* |
| 2 (β-tier) | 42 | ~600 | ~800* |
| 3 (γ-tier) | 27 | ~350 | ~950* |

*Estimated with heavy deduplication — many models share tuples.
Actual unique count requires aggregating all h3_demand lists.

---

## 7. Function Belief Integration Points (Provisional)

> **NOTE**: Belief counts per function are **design estimates**. Final counts are
> determined during model integration. See per-function `collections.md` for truth.

Only **Core Beliefs** carry PE/precision overhead. Appraisal/Anticipation are direct mechanism outputs.

### F1 Sensory (Phase 0)
Core: harmonic_stability(BCH), pitch_prominence(PSCL), pitch_identity(PCCR), timbral_character(MIAA), aesthetic_quality(STAI)
Wave 1: BCH→harmonic_stability + interval_quality + harmonic_template_match
Wave 2: PSCL→pitch_prominence + pitch_continuation; PCCR→pitch_identity + octave_equivalence
Wave 3: MIAA→timbral_character + imagery_recognition; STAI→aesthetic_quality + reward_response_pred

### F7 Motor (Phase 0)
Core: period_entrainment(PEOM), kinematic_efficiency(PEOM), groove_quality(HGSIC), context_depth(HMCE)
Wave 1: PEOM→period_entrainment + timing_precision + period_lock_strength + next_beat_pred
Wave 2: HMCE→context_depth + short/medium/long_context + phrase_boundary_pred
Wave 3: HGSIC→groove_quality + beat_prominence + meter_structure + groove_trajectory

### F3 Attention (Phase 1)
Core: beat_entrainment(SNEM), meter_hierarchy(SNEM), attention_capture(IACM), salience_network_activation(CSG)
Wave 1: SNEM→beat_entrainment + selective_gain + beat_onset_pred + meter_position_pred
Wave 2: IACM→attention_capture + object_segregation + precision_weighting
Wave 3: AACM→aesthetic_engagement + savoring_effect

### F4 Memory (Phase 2)
Core: autobiographical_retrieval(MEAMN), nostalgia_intensity(MEAMN), emotional_coloring(MEAMN), episodic_encoding(HCMC)
Wave 1: MEAMN→all 3 Core + retrieval_probability + memory_vividness + self_relevance + vividness_trajectory
Wave 2: HCMC→episodic_encoding + episodic_boundary + consolidation_strength
Wave 3: MMP→melodic_recognition + memory_preservation + memory_scaffold_pred

### F2 Prediction (Phase 1)
Core: prediction_hierarchy(HTP), sequence_match(SPH), information_content(ICEM), prediction_accuracy(HTP)
Wave 1: HTP→prediction_hierarchy + hierarchy_coherence + abstract_future + midlevel_future
Wave 2: SPH→sequence_match + error_propagation + oscillatory_signature + sequence_completion
Wave 3: ICEM→information_content + defense_cascade + arousal_scaling + valence_inversion

### F5 Emotion (Phase 2)
Core: perceived_happy(VMM), perceived_sad(VMM), emotional_arousal(AAC), nostalgia_affect(NEMAC)
Wave 2: VMM→perceived_happy/sad + mode_detection + emotion_certainty + happy/sad_pathway
Wave 3: AAC→emotional_arousal + chills_intensity + ans_dominance + driving_signal
Wave 3: NEMAC→nostalgia_affect + self_referential_nostalgia + wellbeing_enhancement

### F6 Reward (Phase 5)
Core: wanting(SRP), liking(SRP), pleasure(SRP), prediction_error(SRP), tension(SRP)
Wave 1: SRP→wanting + liking + pleasure + prediction_match + peak_detection + chills_proximity
Wave 2: DAED→dissociation_index + temporal_phase + da_caudate + da_nacc + wanting_ramp
Wave 3: SRP→harmonic_tension + resolution_expectation + reward_forecast

### F8 Learning (Phase 3)
Core: trained_timbre_recognition(TSCP), expertise_enhancement(ESME), network_specialization(EDNR), statistical_model(SLEE)
Wave 4: All F8 models activate. Very high τ (0.88–0.95) — minimal per-frame change.

### F9 Social (Phase 3)
Core: neural_synchrony(NSCP), social_coordination(DDSMI)
Wave 5: All F9 models activate. Requires multi-agent context.

---

## 8. Implementation Checkpoints

After each wave, run the full pipeline and verify:

### Wave 0 Checkpoint (DONE)
- [x] All 5 beliefs produce valid [0,1] output
- [x] Reward is consistently positive
- [x] 131 H³ tuples computed correctly
- [x] 44/44 relay fields consumed by beliefs

### Wave 1 Checkpoint (α enrichment)
- [ ] Each α model produces correct output dimensions
- [ ] No NaN propagation from new models
- [ ] Belief enrichment improves Alpha-Test scores
- [ ] H³ demand grows to ~350 tuples

### Wave 2 Checkpoint (β-tier)
- [ ] Intra-unit dependencies resolve correctly
- [ ] Cross-unit pathways function
- [ ] No precision/reward divergence with increased inputs
- [ ] Unit aggregation: each unit sums all model outputs

### Wave 3 Checkpoint (γ-tier)
- [ ] Models without H³ (NEWMD, MTNE, PTGMP) degrade gracefully
- [ ] Full 96-model pipeline runs end-to-end
- [ ] Total output: ~1,011D per frame per unit across all models
