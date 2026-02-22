# F1 Sensory Processing — Collections

> **NOTE**: This file was built by independently reading each model doc
> in `Docs/C³/Models/`. It does NOT copy from the orchestrator or ontology
> summaries. Counts and dimensions are snapshots — they will change as
> models are integrated and code is written.

---

## 1. Verified F1 Models (from Model Docs)

Independent scan of all 96 model docs identified the following models with
F1 (Sensory Processing) involvement. Models are grouped by implementation status.

### 1.1 Implemented (10 models)

| Model | Unit-Tier | Doc OUTPUT_DIM | Code OUTPUT_DIM | Layers | H³ (v1) | Beliefs | Status |
|-------|-----------|----------------|-----------------|--------|---------|---------|--------|
| BCH | SPU-α1 | 12D | 16D | E4+M2+P3+F3 | 26 | 4 (1C+2A+1N) | done |
| PSCL | SPU-α2 | 12D | 16D | E4+M2+P3+F3 | 14 | 2 (1C+1N) | done |
| PCCR | SPU-α3 | 11D | 11D | E4+M1+P3+F3 | 14 | 2 (1C+1A) | done |
| MIAA | SPU-β3 | 11D | 11D | E3+M2+P3+F3 | 11 | 2 (1C+1N) | done |
| SDNPS | SPU-γ1 | 10D | 10D | E3+M1+P3+F3 | 10 | 0 | done |
| SDED | SPU-γ3 | 10D | 10D | E3+M1+P3+F3 | 9 | 1 (1A) | done |
| CSG | ASU-α3 | 12D | 12D | E3+M3+P3+F3 | 18 | 1 (1A) | done |
| MPG | NDU-α1 | 10D | 10D | E4+M3+P2+F1 | 16 | 2 (1A+1N) | done |
| PNH | IMU-α2 | 11D | 11D | H3+M2+P3+F3 | 15 | 0 | done |
| TPRD | IMU-β8 | 10D | 10D | T3+M2+P2+F3 | 18 | 0 | done |

**Dimension discrepancies** (doc vs code):
- **BCH**: Doc says 12D, code is 16D — BCH kernel injection adds 4D (hierarchy product)
- **PSCL**: Doc says 12D, code is 16D — implementation expanded layers during integration

These discrepancies are expected: model docs describe the theoretical architecture,
code dimensions may grow during integration when cross-model feeds are added.

### 1.2 All Confirmed F1 Models Now Implemented

SDNPS, PNH, and TPRD were implemented on Feb 22, 2026. All three produce
correct output tensors, no NaN, values in [0, 1]. Zero beliefs at this time
— may gain beliefs as integration matures.

**R³ mapping corrections applied during implementation:**
- PNH: `[10] loudness` → `[8] velocity_D` (97D naming fix)
- TPRD: `[10] loudness` → `[8] velocity_D` (same fix)
- Both: `x_l0l5[25:33]` dissolved → replaced with inline energy×consonance coupling
- TPRD: `x_l5l7[41:49]` dissolved → replaced with spectral_autocorrelation

### 1.3 Contested — Orchestrator Lists as F1, Docs Don't Confirm

The F1 orchestrator lists 14 models. These 4 models appear in that list but
their model docs do **not** assign them to F1:

| Model | Unit-Tier | Doc OUTPUT_DIM | Doc Function | Orchestrator Claim |
|-------|-----------|----------------|--------------|-------------------|
| MDNS | STU-α3 | 12D | sensorimotor (STU) | "shared substrate — perception = imagery" |
| TPIO | STU-β2 | 10D | sensorimotor (STU) | "timbre perception-imagery overlap" |
| MSPBA | IMU-β6 | 11D | syntax (IMU) | "Broca's syntax → prediction error" |
| LDAC | RPU-γ1 | 6D | reward (RPU) | "liking → auditory cortex gain" |

**Decision**: These 4 models have mechanism computation but belong to other
functions (F7/F4/F2/F6 respectively). They may have cross-unit pathways that
touch F1 but their primary computation is not sensory processing. They should
NOT be implemented under F1 mechanism code. Instead, they'll be implemented
in their own function and their F1-relevant outputs will flow via cross-function
pathways.

### 1.4 Cross-Function — Not in F1 Model List but Owns F1 Beliefs

| Model | Unit-Tier | Primary Function | F1 Beliefs Claimed |
|-------|-----------|-----------------|-------------------|
| STAI | SPU-β1 | F5 Emotion | 3 (aesthetic_quality, spectral_temporal_synergy, reward_response_pred) |

STAI is documented under F5. Its sensory evaluation outputs are F1-relevant.
When STAI is integrated, its 3 F1 beliefs will be linked here.

---

## 2. Implementation Summary

```
Implemented:     10 models, 14 beliefs
Contested:       4 models — reassigned to other functions
Cross-function:  1 model (STAI) — 3 additional F1 beliefs pending

Current code:    117D mechanism output (16+16+11+11+10+10+12+10+11+10)
                 14 beliefs (4C + 5A + 5N... see §3)
                 151 H³ demands
```

---

## 3. Belief Inventory (as implemented)

| # | Belief | Cat | τ | Owner | Source Dims | Status |
|---|--------|-----|---|-------|-------------|--------|
| 1 | harmonic_stability | C | 0.3 | BCH | P0(50%)+P1(30%)+E2(20%) | done |
| 2 | pitch_prominence | C | 0.35 | PSCL | P0(60%)+P1(25%)+P3(15%) | done |
| 3 | pitch_identity | C | 0.4 | PCCR | from PCCR mechanism | done |
| 4 | timbral_character | C | 0.5 | MIAA | from MIAA mechanism | done |
| 5 | interval_quality | A | — | BCH | E2:hierarchy | done |
| 6 | harmonic_template_match | A | — | BCH | P1:template_match | done |
| 7 | spectral_complexity | A | — | SDED | M0(40%)+P0(30%)+P1(30%) | done |
| 8 | consonance_salience_gradient | A | — | CSG | P0(40%)+E0(30%)+M0(30%) | done |
| 9 | melodic_contour_tracking | A | — | MPG | from MPG mechanism | done |
| 10 | octave_equivalence | A | — | PCCR | from PCCR mechanism | done |
| 11 | consonance_trajectory | N | — | BCH | F0:consonance_forecast | done |
| 12 | pitch_continuation | N | — | PSCL | F0:pitch_continuation | done |
| 13 | imagery_recognition | N | — | MIAA | from MIAA mechanism | done |
| 14 | contour_continuation | N | — | MPG | from MPG mechanism | done |

**Pending** (from cross-function STAI, not yet integrated):
- aesthetic_quality (C)
- spectral_temporal_synergy (A)
- reward_response_pred (N)

---

## 4. Depth-Ordered Pipeline

```
R³ (97D) ───┬────────────────────────────────────────────
H³ tuples ──┤
            ▼
Depth 0:  BCH   (16D, relay, SPU)  ← brainstem consonance hierarchy
          CSG   (12D, relay, ASU)  ← consonance-salience gradient
          MIAA  (11D, relay, SPU)  ← musical imagery auditory activation
          MPG   (10D, relay, NDU)  ← melodic processing gradient
          PNH   (11D, relay, IMU)  ← Pythagorean neural hierarchy
          SDNPS (10D, relay, SPU)  ← stimulus-dependent neural pitch salience
          SDED  (10D, relay, SPU)  ← sensory dissonance early detection
          TPRD  (10D, relay, IMU)  ← tonotopy-pitch dissociation
            │
            ▼
Depth 1:  PSCL  (16D, SPU)        ← cortical pitch salience (reads BCH)
            │
            ▼
Depth 2:  PCCR  (11D, SPU)        ← pitch chroma representation (reads BCH+PSCL)
```

---

## 5. Code Dimensions vs Doc Dimensions

The model docs describe theoretical architecture. Code implementations
may differ because:

1. **Layer expansion**: Integration may add dimensions for cross-model feeds
2. **BCH kernel injection**: Adds hierarchy product dims beyond doc spec
3. **Precision fields**: Some models add precision-related dims during integration
4. **Relay wrappers**: BCH relay wrapper outputs differ from raw mechanism dims

**Rule**: Code dimensions are authoritative. Doc dimensions are the starting spec.
When writing collections for other functions, always verify against code after
implementation.

---

## 6. H³ Demands (implemented models)

| Model | H³ Tuples (v1) | Law |
|-------|----------------|-----|
| BCH | 26 | L0 only (17 via relay) |
| PSCL | 14 | L0 |
| PCCR | 14 | L0 |
| MIAA | 11 | L0 |
| SDED | 9 | L0 |
| CSG | 18 | L0 |
| MPG | 16 | L0 |
| SDNPS | 10 | L0+L2 |
| PNH | 15 | L0+L2 |
| TPRD | 18 | L0+L2 |

Total H³ demands from implemented F1 models: ~151 tuples.

---

## 7. Next Steps

- [x] Implement SDNPS mechanism (SPU-γ1, 10D, 10 H³) — Feb 22, 2026
- [x] Implement PNH mechanism (IMU-α2, 11D, 15 H³) — Feb 22, 2026
- [x] Implement TPRD mechanism (IMU-β8, 10D, 18 H³) — Feb 22, 2026
- [ ] Integrate STAI F1 beliefs when F5 is implemented
- [ ] Verify contested models (MDNS, TPIO, MSPBA, LDAC) during their function integration
