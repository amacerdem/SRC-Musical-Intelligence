# F3 — Attention & Salience

**Function**: F3 Attention & Salience
**Models**: 14 (11 primary from 3 units: ASU×7, STU×3, PCU×1 + 3 secondary: CSG*, SDD*, PWSM*)
**Beliefs**: 15 (4 Core + 7 Appraisal + 4 Anticipation)
**Total output**: 113D (12+11+10+11+10+9+9+11+11+10+9) — primary models
**H³ demands**: 173 tuples (18 implemented from SNEM relay + 155 from docs)
**Phase**: 1 (reads F1 beliefs + R³/H³ — same phase as F2)
**Relay**: SNEM (ASU-α1)
**Implemented**: SNEM relay (1/11 models, 5/15 beliefs partial)

---

## 1. What F3 Does

F3 determines **what the brain pays attention to** in the musical signal. It converts raw perceptual input into prioritized, filtered representations — deciding which events are salient, which auditory streams to track, and how metric structure organizes temporal attention.

Processing flows from novelty detection to attentional gating:

```
Audio → R³ (97D) ───┬────────────────────────────────────────────
H³ tuples ──────────┤
                    ▼
Depth 0:  SNEM (12D, relay)  ← beat-locked oscillation + selective gain
          IACM (11D)         ← inharmonicity captures involuntary attention
                    │
                    ▼
Depth 1:  BARM (10D)  ← brainstem auditory response modulation
          STANM(11D)  ← spectrotemporal attention network
          AACM (10D)  ← aesthetic-attention coupling
          AMSS (11D)  ← attention-modulated stream segregation
          ETAM (11D)  ← entrainment-tempo-attention modulation
                    │
                    ▼
Depth 2:  DGTP  (9D)  ← domain-general temporal processing
          SDL   (9D)  ← salience-dependent lateralization
          NEWMD(10D)  ← entrainment–working memory dissociation
          IGFE  (9D)  ← individual gamma frequency enhancement
```

F3 is in **Phase 1** (same as F2): α-relays read R³/H³ directly; β-models read α outputs; γ-models read α+β. F3 receives F1 beliefs (harmonic_stability, pitch_prominence) as context signals for salience computation. CSG (F1 primary) contributes 4 F3 beliefs via cross-function pathways.

### Key Neuroscience Circuits

- **Salience Network**: anterior insula (aInsula) + dorsal anterior cingulate cortex (dACC) → detects behaviorally relevant events
- **Ventral Attention Network**: temporo-parietal junction (TPJ) + inferior frontal gyrus (IFG) → stimulus-driven reorienting
- **Auditory Cortex Beat-Locking**: STG + HG → neural oscillations entrain to beat structure (SNEM)
- **Brainstem Modulation**: IC + MGB → early gain control gates attention (BARM)

---

## 2. Complete Model Inventory

| # | Model | Unit | Tier | Depth | Output | H³ | Beliefs | Status |
|---|-------|------|------|-------|--------|-----|---------|--------|
| 1 | **SNEM** | ASU | α | 0 | 12D | 18 | 5 (2C+1A+2N) | **relay done** |
| 2 | IACM | ASU | α | 0 | 11D | 16 | 3 (1C+1A+1N) | pending |
| 3 | BARM | ASU | β | 1 | 10D | 14 | 0 | pending |
| 4 | STANM | ASU | β | 1 | 11D | 16 | 0 | pending |
| 5 | AACM | ASU | β | 1 | 10D | 12 | 2 (2A) | pending |
| 6 | DGTP | ASU | γ | 2 | 9D | 9 | 0 | pending |
| 7 | SDL | ASU | γ | 2 | 9D | 18 | 0 | pending |
| 8 | AMSS | STU | β | 1 | 11D | 16 | 0 | pending |
| 9 | ETAM | STU | β | 1 | 11D | 20 | 0 | pending |
| 10 | NEWMD | STU | γ | 2 | 10D | 16 | 0 | pending |
| 11 | IGFE | PCU | γ | 2 | 9D | 18 | 0 | pending |

**Secondary (cross-function):**

| # | Model | Unit | Primary | F3 Contribution |
|---|-------|------|---------|-----------------|
| * | CSG | ASU-α3 | F1 | 4 F3 beliefs (1C+2A+1N) |
| * | SDD | NDU-α2 | F2 | Deviance detection evidence |
| * | PWSM | ASU-γ1 | F2 | Precision-weighted salience context |

---

## 3. Complete Belief Inventory (15)

| # | Belief | Cat | τ | Owner | Mechanism Source | Status |
|---|--------|-----|---|-------|------------------|--------|
| 1 | **`beat_entrainment`** | **C** | **0.35** | **SNEM** | beat_locked + entrainment_strength | **relay done** |
| 2 | **`meter_hierarchy`** | **C** | **0.4** | **SNEM** | entrainment multi-scale (H10+H16) | **relay done** |
| 3 | `attention_capture` | C | 0.25 | IACM | inharmonicity_index + spectral_onset | pending |
| 4 | `salience_network_activation` | C | 0.3 | CSG | consonance_gradient + energy_salience | cross-function |
| 5 | **`selective_gain`** | **A** | — | **SNEM** | attention-gated amplification | **relay done** |
| 6 | `object_segregation` | A | — | IACM | stream separation / auditory scene | pending |
| 7 | `sensory_load` | A | — | CSG | processing resource demand | cross-function |
| 8 | `consonance_valence_mapping` | A | — | CSG | consonance → emotional valence | cross-function |
| 9 | `aesthetic_engagement` | A | — | AACM | preferred intervals → attention | pending |
| 10 | `savoring_effect` | A | — | AACM | liking → slower response → sustained | pending |
| 11 | `precision_weighting` | A | — | IACM | context stability → PE weight | pending |
| 12 | **`beat_onset_pred`** | **N** | — | **SNEM** | next beat time prediction | **relay done** |
| 13 | `meter_position_pred` | N | — | SNEM | current position in metric hierarchy | pending |
| 14 | `attention_shift_pred` | N | — | IACM | frontal attention shift ~400ms | pending |
| 15 | `processing_load_pred` | N | — | CSG | upcoming sensory load estimate | cross-function |

---

## 4. Observe Formula — beat_entrainment (kernel v4.0)

The salience/attention observe formula from the current kernel:

```
energy = 0.6×amplitude + 0.4×onset
h3_change = max(|vel_amp|, |vel_onset|, |vel_flux|)  # beat scale
            × 0.60 + phrase_scale × 0.40

# 4-signal mixing (with relays):
base = 0.25×energy + 0.25×h3_change + 0.15×|PE_prev| + 0.35×relay
value = 0.5×base + 0.5×max(all signals)   # peak preservation

# SNEM attention gate (multiplicative):
value *= 1 + 0.3 × selective_gain

# Precision: (0.5×energy + 0.5×h3_change) × 10, clamped [0.5, 10]
```

Multi-scale horizons (beat_entrainment):
```
H5(46ms)  H7(250ms)  H10(400ms)  H13(600ms)
H18(2s)   H21(8s)
```

---

## 5. Multi-Scale Horizons (all F3 Core Beliefs)

| Core Belief | T_char | Horizons | Band |
|-------------|--------|----------|------|
| beat_entrainment | 400ms | H5, H7, H10, H13, H18, H21 (6) | Meso |
| meter_hierarchy | 1s | H10, H13, H16, H18 (4) | Macro |
| attention_capture | 250ms | H3, H5, H7, H10 (4) | Meso |
| salience_network_activation | 400ms | H5, H7, H10, H13, H18, H21 (6) | Meso |

---

## 6. Dependency Graph

```
                          R³ (97D) + H³
                              │
            ┌─────────────────┼──────────────┐
            ▼                 ▼              ▼
        SNEM (α1)         IACM (α2)      [CSG (F1)]
        12D relay         11D              [12D relay]
            │                │                │
     ┌──────┴─────┐    ┌────┴────┐      ┌────┴────┐
     ▼            ▼    ▼         ▼      ▼         ▼
  BARM (β1)  STANM(β2) AMSS(β1)  ETAM(β4)  AACM(β3)
    10D        11D      11D       11D        10D
     │            │      │         │          │
     ├────┬───────┴──────┼─────────┤          │
     ▼    ▼              ▼         ▼          │
  DGTP(γ2) SDL(γ3)   NEWMD(γ2)  IGFE(γ1)    │
    9D      9D         10D        9D          │
                                              │
     Cross-unit feeds:                        │
     AMSS ← HMCE (STU context)              │
     ETAM ← HMCE + AMSC (STU)              │
     AACM ← CSG (F1 consonance)  ←─────────┘
     IGFE ← WMED (F2 β-tier)
     DGTP ← BARM + SNEM
     SDL  ← STANM + PWSM* (F2)
```

### Key Dependencies

| Model | Reads From |
|-------|-----------|
| BARM (β1) | SNEM.entrainment_strength |
| STANM (β2) | R³/H³ direct (spectrotemporal pattern) |
| AACM (β3) | CSG.consonance_gradient (F1 cross-function) |
| AMSS (β1) | HMCE.structure_predict (STU cross-unit) |
| ETAM (β4) | HMCE.context_depth, AMSC.auditory_activation (STU) |
| DGTP (γ2) | BARM.brainstem_response, SNEM.beat_locked |
| SDL (γ3) | STANM.temporal_allocation, PWSM.precision_context (F2) |
| NEWMD (γ2) | AMSC.motor_coupling (STU cross-unit) |
| IGFE (γ1) | WMED.wm_contribution (F2 cross-function) |

---

## 7. Unit Architecture

### ASU — Auditory Salience Unit (7 primary F3 models)

ASU is F3's primary unit. ALL 9 ASU models use beat + auditory-scene mechanisms —
the most uniform signature in the system. CSG (α3) is F1 primary; PWSM (γ1) is F2 primary.

```
ASU models in F3:        SNEM ─── IACM
                           │         │
                         BARM ─── STANM ─── AACM
                           │         │
                         DGTP       SDL
```

### STU — Sensorimotor Timing Unit (3 F3 models)

AMSS, ETAM, NEWMD are STU models assigned to F3 by MODEL-ATLAS v2.0. They share
the attention/timing interface: AMSS does stream segregation, ETAM does tempo-attention
coupling, NEWMD models the entrainment-WM paradox.

### PCU — Predictive Coding Unit (1 F3 model)

IGFE is the only PCU model assigned to F3. It models individual gamma frequency
enhancement — gamma oscillations as the binding mechanism for attention.

---

## 8. Documentation Structure

```
F3-Attention-and-Salience/
├── 0_F3-orchestrator.md                  ← this file
├── collections.md                         ← full model inventory
├── mechanisms/
│   └── 0_mechanisms-orchestrator.md       ← all 11 primary models documented
└── beliefs/
    └── 0_beliefs_orchestrator.md          ← all 15 beliefs documented
```

**1 α-tier relay done (SNEM, 18 H³ tuples).** Pending: 1 α (IACM) + 4 β (BARM, STANM, AACM, AMSS, ETAM) + 4 γ (DGTP, SDL, NEWMD, IGFE) — 155 H³ tuples total.
