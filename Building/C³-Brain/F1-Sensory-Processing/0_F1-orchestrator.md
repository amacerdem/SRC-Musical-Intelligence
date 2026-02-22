# F1 — Sensory Processing

**Function**: F1 Sensory Processing
**Models**: 14 (from 6 units: SPU, IMU, NDU, ASU, STU, RPU)
**Beliefs**: 17 (5 Core + 7 Appraisal + 5 Anticipation)
**Phase**: 0 (earliest in DAG — R³/H³ grounded, no cross-function dependencies)
**Documented**: BCH + PSCL + PCCR + MPG + MIAA (5/14 models, 12/17 beliefs)

---

## 1. What F1 Does

F1 converts **acoustic signal** into **perceptual features**. It is the sensory foundation — everything the brain "hears" before it starts predicting, attending, remembering, or feeling.

Processing flows from brainstem to cortex:

```
Audio → R³ (97D) → BCH (brainstem consonance)
                      → PSCL (cortical pitch salience)
                        → PCCR (pitch chroma identity)
                          → higher-order (imagery, melody, aesthetics)
```

F1 is **R³/H³ grounded**: all mechanisms read directly from the frozen perceptual front-end. No learned musical structure, no prediction, no cross-function dependencies at the mechanism level.

---

## 2. Architecture — The Two Output Streams

F1 produces two kinds of output that serve fundamentally different purposes:

```
                    ┌──────────────────────────────────────────────────┐
                    │            F1 MECHANISM OUTPUT                    │
                    │            (HORIZONTAL FLOW)                      │
                    │                                                    │
                    │  BCH (16D) ──► PSCL M3      (intra-F1)          │
                    │  PSCL P0  ──► PCCR          (intra-F1)          │
                    │  BCH P0   ──► SRP           (cross-function→F6) │
                    │  PSCL F2  ──► HMCE          (cross-function→F1) │
                    │                                                    │
                    │  Model → Model data flow                          │
                    │  Dimensions accumulate: 16D + 16D + ... = total   │
                    └──────────────────────────────────────────────────┘
                                         │
                              derives from (weighted sums)
                                         │
                    ┌──────────────────────────────────────────────────┐
                    │            F1 BELIEF OUTPUT                      │
                    │            (VERTICAL FLOW)                        │
                    │                                                    │
                    │  mechanism dims ──► observe()                     │
                    │       predict() ◄── H³ trends + context          │
                    │              PE = observed − predicted            │
                    │              gain = π_obs/(π_obs+π_pred)         │
                    │              posterior = update(predicted, PE)     │
                    │                    │                               │
                    │              PE ──► Reward (F6)                   │
                    │          value ──► Salience (F3)                  │
                    │          value ──► Prediction (F2)                │
                    │                                                    │
                    │  Beliefs live in BeliefStore, not in tensors      │
                    └──────────────────────────────────────────────────┘
```

### The Critical Distinction

**Mechanism output dimensions** (HORIZONTAL): Flow between models. BCH outputs 16D, PSCL reads 4 of those dimensions via M3. PCCR will read PSCL outputs. These dimensions accumulate: currently 32D documented, growing as more models are added.

**Belief values** (VERTICAL): Weighted combinations of mechanism dimensions. `pitch_prominence = 0.60×P0 + 0.25×P1 + 0.15×P3` — all from PSCL's 16D. No new dimensions are added. Beliefs are **derived views**, not additional outputs.

**F1 total = 32D mechanism output, NOT 32+6D.**

Beliefs live in the BeliefStore (131 beliefs total across all Functions, 17 from F1). They flow into the Bayesian cycle (predict → observe → PE → reward), not into other models' input tensors.

---

## 3. Complete Model Inventory

| # | Model | Unit | Tier | Depth | Output | Beliefs | Phase | Status |
|---|-------|------|------|-------|--------|---------|-------|--------|
| 1 | **BCH** | SPU | α | 0 | 16D | 4 (1C+2A+1N) | 0a | **done** |
| 2 | **PSCL** | SPU | α | 1 | 16D | 2 (1C+1N) | 0c | **done** |
| 3 | **PCCR** | SPU | α | 2 | 11D | 2 (1C+1A) | 0c | **done** |
| 4 | SDNPS | SPU | γ | — | TBD | 0 | — | — |
| 5 | SDED | SPU | γ | — | TBD | 1 (1A) | — | — |
| 6 | PNH | IMU | α | — | TBD | 0 | — | — |
| 7 | TPRD | IMU | β | — | TBD | 0 | — | — |
| 8 | **MPG** | NDU | α | 0 | 10D | 2 (1A+1N) | 0a | **done** |
| 9 | CSG | ASU | α | — | TBD | 1 (1A) | — | — |
| 10 | **MIAA** | SPU | β | 0 | 11D | 2 (1C+1N) | 0a | **done** |
| 11 | MDNS | STU | α | — | TBD | 0 | — | — |
| 12 | TPIO | STU | β | — | TBD | 0 | — | — |
| 13 | MSPBA | IMU | β | — | TBD | 0 | — | — |
| 14 | LDAC | RPU | γ | — | TBD | 0 | — | — |

*MPG: 1 Appraisal + 1 Anticipation

### Unit Distribution

```
SPU  ███████  7 models (BCH, PSCL, PCCR, SDNPS, SDED, MIAA, + STAI cross-fn)
IMU  ███     3 models (PNH, TPRD, MSPBA)
STU  ██      2 models (MDNS, TPIO)
NDU  █       1 model  (MPG)
ASU  █       1 model  (CSG)
RPU  █       1 model  (LDAC)
```

---

## 4. Depth-Ordered Pipeline

```
R³ (97D) ─────┬──────────────────────────────────────────────────────
H³ tuples ────┤
              ▼
Depth 0:    BCH (relay, 16D)  ← brainstem consonance hierarchy
              │
              ├── E0:nps, E1:harmonicity, P0:consonance_signal, F1:pitch_forecast
              ▼
Depth 1:    PSCL (16D)  ← cortical pitch salience in anterolateral HG
              │
              ├── P0:pitch_prominence_sig, P2:periodicity_clarity, F2:melody_propagation
              ▼
Depth 2:    PCCR (TBD)  ← octave-equivalent chroma encoding
              │
              ▼
Depth ?:    MIAA, MPG, CSG, SDED, ... ← higher-order sensory processing
```

Models with no depth assignment (SDNPS, PNH, TPRD, MDNS, TPIO, MSPBA, LDAC) are either:
- Meta-evidence models (no mechanism computation, only scientific constraints)
- Cross-function models whose primary computation is in another Function

---

## 5. Complete Belief Inventory (17)

| # | Belief | Cat | τ | Owner | Mechanism Source | Status |
|---|--------|-----|---|-------|------------------|--------|
| 1 | `harmonic_stability` | C | 0.3 | BCH | P0(50%)+P1(30%)+E2(20%) | **done** |
| 2 | `pitch_prominence` | C | 0.35 | PSCL | P0(60%)+P1(25%)+P3(15%) | **done** |
| 3 | `pitch_identity` | C | 0.4 | PCCR | TBD | — |
| 4 | `timbral_character` | C | 0.5 | MIAA | TBD | — |
| 5 | `aesthetic_quality` | C | 0.4 | *STAI | TBD | — |
| 6 | `interval_quality` | A | — | BCH | E2:hierarchy | **done** |
| 7 | `harmonic_template_match` | A | — | BCH | P1:template_match | **done** |
| 8 | `spectral_complexity` | A | — | SDED | TBD | — |
| 9 | `consonance_salience_gradient` | A | — | CSG | TBD | — |
| 10 | `spectral_temporal_synergy` | A | — | *STAI | TBD | — |
| 11 | `melodic_contour_tracking` | A | — | MPG | TBD | — |
| 12 | `octave_equivalence` | A | — | PCCR | TBD | — |
| 13 | `pitch_continuation` | N | — | PSCL | F0:pitch_continuation | **done** |
| 14 | `consonance_trajectory` | N | — | BCH | F0:consonance_forecast | **done** |
| 15 | `imagery_recognition` | N | — | MIAA | TBD | — |
| 16 | `contour_continuation` | N | — | MPG | TBD | — |
| 17 | `reward_response_pred` | N | — | *STAI | TBD | — |

*STAI: Cross-function model (F5 primary, F6 secondary). See §7.

---

## 6. Models Without F1 Beliefs

6 of 14 F1 models produce **no F1 beliefs**. They are in F1 because they provide scientific evidence or computational constraints:

| Model | Why It's in F1 | What It Contributes |
|-------|---------------|---------------------|
| SDNPS (SPU-γ1) | Boundary condition | Limits of FFR-consonance correlation (synthetic vs natural) |
| PNH (IMU-α2) | Interval complexity | Pythagorean hierarchy feeds F2 prediction |
| TPRD (IMU-β8) | Meta-evidence | Tonotopic map ≠ perceptual pitch (architectural constraint) |
| MDNS (STU-α3) | Shared substrate | EEG melody decoding — perception and imagery share neural code |
| TPIO (STU-β2) | Shared substrate | Timbre perception and imagery overlap |
| LDAC (RPU-γ1) | Feedback loop | Liking modulates auditory cortex gain (F6 → F1) |

These models constrain the architecture without producing beliefs. They inform precision weights, qualification notes, and cross-function bridges.

---

## 7. Cross-Function Models

Several F1 models have dual or cross-function roles:

| Model | Primary | Secondary | Bridge |
|-------|---------|-----------|--------|
| **STAI** (SPU-β1) | F5 Emotion | F6 Reward | Owns 3 F1 beliefs (aesthetic_quality, spectral_temporal_synergy, reward_response_pred) despite being an F5 model. Its sensory evaluation outputs are F1-relevant. |
| MIAA (SPU-β3) | F1 Sensory | F4 Memory | Musical imagery → auditory cortex activation → memory binding |
| MDNS (STU-α3) | F1 Sensory | F4 Memory | Perception = imagery at neural level |
| TPIO (STU-β2) | F1 Sensory | F4, F7 | Timbre perception → motor imagery |
| MPG (NDU-α1) | F1 Sensory | F2 Prediction | Posterior onset → anterior contour gradient |
| CSG (ASU-α3) | F3 Attention | F1 Sensory | Consonance-dissonance → salience network |
| MSPBA (IMU-β6) | F1 Sensory | F2 Prediction | Broca's area syntax violation → prediction error |
| LDAC (RPU-γ1) | F6 Reward | F1 Sensory | Pleasure feedback → sensory cortex gain |

### STAI Cross-Function Ownership

STAI is NOT in the F1 model list (14 models). Its primary function is F5 (Emotion), secondary F6 (Reward). However, BELIEF-CYCLE.md assigns it 3 F1 beliefs. This reflects that STAI's **computation starts with sensory features** (spectral + temporal integration) even though its **output serves emotion and reward**. When STAI is documented (under F5), its F1 beliefs will be defined there and linked here.

---

## 8. Phase Schedule (F1 Perspective)

```
Phase 0a:  BCH relay (independent, 16D)
           ↓ BCH.E0, E1, P0, F1 available
Phase 0c:  PSCL (reads BCH, 16D)
           Consonance multi-scale (BCH → HTP)
           ↓ PSCL.P0, P2, F2 available

Phase 1:   Salience computation
           ↓ uses F1 beliefs (harmonic_stability, pitch_prominence)

Phase 2a:  Predict + Observe for all F1 Core beliefs
Phase 2b:  PE + Precision
Phase 2c:  Bayesian Update (posterior)
           ↓ F1 Core beliefs finalized

Phase 3:   Reward (uses F1 PEs)
           ↓ harmonic_stability PE, pitch_prominence PE → reward formula
```

---

## 9. Documentation Structure

```
F1-Sensory-Processing/
├── 0_F1-orchestrator.md              ← this file
├── mechanisms/
│   ├── 0_mechanisms-orchestrator.md   BCH + PSCL mechanism overview
│   ├── BCH-extraction.md             BCH E-layer (4D)
│   ├── BCH-temporal-integration.md   BCH M-layer (4D)
│   ├── BCH-cognitive-present.md      BCH P-layer (4D)
│   ├── BCH-forecast.md              BCH F-layer (4D)
│   ├── PSCL-extraction.md            PSCL E-layer (4D)
│   ├── PSCL-temporal-integration.md  PSCL M-layer (4D)
│   ├── PSCL-cognitive-present.md     PSCL P-layer (4D)
│   ├── PSCL-forecast.md             PSCL F-layer (4D)
│   ├── mpg/
│   │   ├── MPG-extraction.md         MPG E-layer (4D)
│   │   ├── MPG-temporal-integration.md MPG M-layer (3D)
│   │   ├── MPG-cognitive-present.md  MPG P-layer (2D)
│   │   └── MPG-forecast.md           MPG F-layer (1D)
│   └── miaa/
│       ├── MIAA-extraction.md         MIAA E-layer (3D)
│       ├── MIAA-temporal-integration.md MIAA M-layer (2D)
│       ├── MIAA-cognitive-present.md  MIAA P-layer (3D)
│       └── MIAA-forecast.md           MIAA F-layer (3D)
└── beliefs/
    ├── 0_beliefs_orchestrator.md      Belief overview (12/17 documented)
    ├── harmonic_stability.md          Core (BCH, τ=0.3)
    ├── interval_quality.md            Appraisal (BCH)
    ├── harmonic_template_match.md     Appraisal (BCH)
    ├── consonance_trajectory.md       Anticipation (BCH)
    ├── pitch_prominence.md            Core (PSCL, τ=0.35)
    ├── pitch_continuation.md          Anticipation (PSCL)
    ├── mpg/
    │   ├── melodic_contour_tracking.md Appraisal (MPG)
    │   └── contour_continuation.md    Anticipation (MPG)
    └── miaa/
        ├── timbral_character.md       Core (MIAA, τ=0.5)
        └── imagery_recognition.md     Anticipation (MIAA)
```

**Next model to document**: SDED (SPU-γ3) — last F1 computational model with beliefs. Remaining 6 models (SDNPS, PNH, TPRD, MDNS, TPIO, MSPBA, LDAC, CSG) are meta-evidence or cross-function with no F1 mechanisms.
