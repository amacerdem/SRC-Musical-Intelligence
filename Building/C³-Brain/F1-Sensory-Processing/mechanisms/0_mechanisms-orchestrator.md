# F1 Mechanism Orchestrator — Sensory Processing

**Function**: F1 Sensory Processing
**Models covered**: 10/10 — ALL IMPLEMENTED
**Total F1 mechanism output**: 117D (16+16+11+11+10+10+12+10+11+10)
**Beliefs**: 14 (4C + 5A + 5N)
**H³ demands**: ~151 tuples
**Architecture**: Depth-ordered pipeline — 8 relays (Depth 0) → PSCL (Depth 1) → PCCR (Depth 2)

---

## Model Pipeline (Depth Order)

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

# BCH — Brainstem Consonance Hierarchy

**Model**: SPU-α1-BCH
**Type**: Relay (Depth 0) — reads R³/H³ directly, no C³ mechanisms
**Tier**: α (Mechanistic, >90% confidence)
**Output**: 16D per frame (4 layers × 4D)
**Phase**: 0a (independent relay, no cross-relay dependencies)

---

## 1. Identity

BCH models how the brainstem (auditory nerve → inferior colliculus) preferentially encodes consonant musical intervals over dissonant ones. This is the earliest neural correlate of consonance perception — before cortical processing.

BCH is a **relay**: it transforms R³ acoustic features and H³ temporal morphologies directly into cognitive-level outputs. It does not use C³ mechanisms (no learned parameters, no belief state). All computation is deterministic weighted sums.

---

## 2. R³ Input Map (Post-Freeze 97D)

BCH reads **14 direct R³ indices** from 4 groups:

| # | R³ Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[0]** | roughness | A: Consonance | Plomp & Levelt 1965 — sensory dissonance |
| 2 | **[1]** | sethares_dissonance | A: Consonance | Sethares 1999 — psychoacoustic dissonance |
| 3 | **[2]** | helmholtz_kang | A: Consonance | Helmholtz 1863, Kang 2009 — integer ratio detection |
| 4 | **[3]** | stumpf_fusion | A: Consonance | Stumpf 1890 — tonal fusion strength |
| 5 | **[4]** | sensory_pleasantness | A: Consonance | Sethares 2005 — spectral regularity |
| 6 | **[5]** | inharmonicity | A: Consonance | Fletcher 1934 — harmonic series deviation |
| 7 | **[6]** | harmonic_deviation | A: Consonance | Jensen 1999 — energy variance in partials |
| 8 | **[14]** | tonalness | C: Timbre | Harmonic-to-noise ratio (pitch clarity proxy) |
| 9 | **[17]** | spectral_autocorrelation | C: Timbre | Harmonic periodicity |
| 10 | **[18]** | tristimulus1 | C: Timbre | Fundamental strength (Pollard & Jansson 1982) |
| 11 | **[19]** | tristimulus2 | C: Timbre | 2nd–4th harmonic energy |
| 12 | **[20]** | tristimulus3 | C: Timbre | 5th+ harmonic energy |
| 13 | **[38]** | pitch_class_entropy | F: Pitch/Chroma | Chroma distribution entropy (Krumhansl 1990) |
| 14 | **[39]** | pitch_salience | F: Pitch/Chroma | Harmonic peak prominence (Parncutt 1989) |
| 15 | **[51]** | key_clarity | H: Harmony | Krumhansl-Schmuckler tonal center strength |
| 16 | **[60]** | tonal_stability | H: Harmony | Stability of tonal center (Krumhansl 1990) |

### Dissolved Feature: Coupling

Old R³[41] (`rough_x_warmth`, Group E) was a cross-domain product. Per R³ ontology freeze v1.0.0, Group E is dissolved. BCH now computes coupling internally:

```
coupling = r3[:,:,0] × r3[:,:,14]   # roughness × tonalness (consonance×timbre)
```

This interaction is computed in BCH's own extraction layer, not from R³.

---

## 3. H³ Temporal Demand (48 tuples)

BCH operates at 3 brainstem timescales plus extended memory/forecast horizons.

### 3.1 Brainstem Timescales

| H# | Duration | Band | Neural Correlate |
|----|----------|------|------------------|
| H0 | 5.8ms | Micro | Phase-locking instant (single frame) |
| H3 | 23.2ms | Micro | Consonant onset (FFR window) |
| H6 | 200ms | Micro | Consonance interval evaluation |
| H12 | 525ms | Meso | Two-beat motif (memory) |
| H16 | 1s | Macro | Single measure (extended memory) |
| H18 | 2s | Macro | Single measure @ 120 BPM (extended memory) |

### 3.2 Present Demands (L2 — Integration, 19 tuples)

| # | R³ Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 0 | roughness | 0 | M0 (value) | L2 | Current dissonance |
| 2 | 0 | roughness | 3 | M1 (mean) | L2 | Mean dissonance 23ms |
| 3 | 2 | helmholtz_kang | 0 | M0 (value) | L2 | Current consonance |
| 4 | 2 | helmholtz_kang | 3 | M1 (mean) | L2 | Mean consonance 23ms |
| 5 | 3 | stumpf_fusion | 0 | M0 (value) | L2 | Current tonal fusion |
| 6 | 5 | inharmonicity | 0 | M0 (value) | L2 | Current inharmonicity |
| 7 | 6 | harmonic_deviation | 0 | M0 (value) | L2 | Current deviation |
| 8 | 18 | tristimulus1 | 0 | M0 (value) | L2 | F0 energy |
| 9 | 19 | tristimulus2 | 0 | M0 (value) | L2 | Mid-harmonic energy |
| 10 | 20 | tristimulus3 | 0 | M0 (value) | L2 | High-harmonic energy |
| 11 | 38 | pitch_class_entropy | 0 | M0 (value) | L2 | Instantaneous tonal clarity |
| 12 | 38 | pitch_class_entropy | 3 | M1 (mean) | L2 | Sustained tonal clarity 23ms |
| 13 | 39 | pitch_salience | 0 | M0 (value) | L2 | Instantaneous pitch salience |
| 14 | 39 | pitch_salience | 3 | M0 (value) | L2 | Pitch salience at 23ms |
| 15 | 39 | pitch_salience | 6 | M0 (value) | L2 | Pitch salience at 200ms |
| 16 | 51 | key_clarity | 3 | M0 (value) | L2 | Key clarity at 23ms |
| 17 | 51 | key_clarity | 3 | M1 (mean) | L2 | Sustained key clarity 23ms |
| 18 | 51 | key_clarity | 6 | M0 (value) | L2 | Key clarity at 200ms |
| 19 | 60 | tonal_stability | 3 | M0 (value) | L2 | Tonal stability at 23ms |

### 3.3 Past Demands (L0 — Memory, 17 tuples)

| # | R³ Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 0 | roughness | 6 | M18 (trend) | L0 | Dissonance trajectory 200ms |
| 2 | 0 | roughness | 12 | M1 (mean) | L0 | Mean dissonance 525ms |
| 3 | 0 | roughness | 16 | M1 (mean) | L0 | Mean dissonance 1s |
| 4 | 2 | helmholtz_kang | 12 | M1 (mean) | L0 | Mean consonance 525ms |
| 5 | 2 | helmholtz_kang | 18 | M1 (mean) | L0 | Mean consonance 2s |
| 6 | 3 | stumpf_fusion | 6 | M1 (mean) | L0 | Fusion over 200ms |
| 7 | 3 | stumpf_fusion | 16 | M1 (mean) | L0 | Fusion over 1s |
| 8 | 5 | inharmonicity | 3 | M18 (trend) | L0 | Inharmonicity trajectory 23ms |
| 9 | 5 | inharmonicity | 12 | M1 (mean) | L0 | Mean inharmonicity 525ms |
| 10 | 6 | harmonic_deviation | 3 | M1 (mean) | L0 | Mean deviation 23ms |
| 11 | 6 | harmonic_deviation | 12 | M1 (mean) | L0 | Mean deviation 525ms |
| 12 | 39 | pitch_salience | 12 | M1 (mean) | L0 | Mean pitch salience 525ms |
| 13 | 39 | pitch_salience | 18 | M1 (mean) | L0 | Mean pitch salience 2s |
| 14 | 51 | key_clarity | 12 | M1 (mean) | L0 | Mean key clarity 525ms |
| 15 | 51 | key_clarity | 18 | M1 (mean) | L0 | Mean key clarity 2s |
| 16 | 60 | tonal_stability | 6 | M1 (mean) | L0 | Tonal stability 200ms |
| 17 | 60 | tonal_stability | 18 | M1 (mean) | L0 | Tonal stability 2s |

### 3.4 Future Demands (L1 — Forward, 12 tuples)

| # | R³ Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 0 | roughness | 6 | M1 (mean) | L1 | Expected roughness 200ms |
| 2 | 0 | roughness | 12 | M18 (trend) | L1 | Roughness trend 525ms ahead |
| 3 | 2 | helmholtz_kang | 6 | M1 (mean) | L1 | Expected consonance 200ms |
| 4 | 2 | helmholtz_kang | 12 | M1 (mean) | L1 | Expected consonance 525ms |
| 5 | 3 | stumpf_fusion | 6 | M1 (mean) | L1 | Expected fusion 200ms |
| 6 | 5 | inharmonicity | 6 | M18 (trend) | L1 | Inharmonicity trend 200ms ahead |
| 7 | 39 | pitch_salience | 6 | M1 (mean) | L1 | Expected pitch salience 200ms |
| 8 | 39 | pitch_salience | 12 | M1 (mean) | L1 | Expected pitch salience 525ms |
| 9 | 51 | key_clarity | 6 | M1 (mean) | L1 | Expected key clarity 200ms |
| 10 | 51 | key_clarity | 16 | M1 (mean) | L1 | Expected key clarity 1s |
| 11 | 60 | tonal_stability | 6 | M1 (mean) | L1 | Expected tonal stability 200ms |
| 12 | 60 | tonal_stability | 12 | M1 (mean) | L1 | Expected tonal stability 525ms |

**Total**: 48 tuples (19 L2 + 17 L0 + 12 L1) of 223,488 theoretical = 0.021%

---

## 4. Pipeline: R³ → H³ → 4-Layer Output (16D)

```
R³ (14 direct)  ──────────────────────────────────────┐
                                                       ▼
                                               ┌──────────────┐
H³ (48 tuples)  ──────────────────────────────►│  E-LAYER (4D) │
                                               │  Extraction   │
  coupling = r3[0]×r3[14] (internal)  ────────►│               │
                                               └──────┬───────┘
                                                      │ f01, f02, f03, f04
                                                      ▼
                                               ┌──────────────┐
H³ L2 (present) ──────────────────────────────►│  M-LAYER (4D) │
H³ L0 (past)    ──────────────────────────────►│  Temporal     │
                                               │  Integration  │
                                               └──────┬───────┘
                                                      │ M0..M3
                                                      ▼
                                               ┌──────────────┐
R³ direct  ────────────────────────────────────►│  P-LAYER (4D) │
H³ L0+L2   ───────────────────────────────────►│  Cognitive    │
E-layer outputs  ─────────────────────────────►│  Present      │
                                               └──────┬───────┘
                                                      │ P0..P3
                                                      ▼
                                               ┌──────────────┐
E+M+P outputs  ───────────────────────────────►│  F-LAYER (4D) │
H³ L0+L1 (trends)  ──────────────────────────►│  Forecast     │
                                               └──────┬───────┘
                                                      │ F0..F3
                                                      ▼
                                               BCH OUTPUT (16D)
```

### Layer Dependency

| Layer | Reads From | Outputs |
|-------|-----------|---------|
| **E** (Extraction) | R³ direct, coupling (internal) | f01_nps, f02_harmonicity, f03_hierarchy, f04_ffr_behavior |
| **M** (Memory) | H³ L2+L0 tuples, R³[4] | M0:consonance_memory, M1:pitch_memory, M2:tonal_memory, M3:spectral_memory |
| **P** (Present) | R³ direct, H³ L0+L2, E-layer | P0:consonance_signal, P1:template_match, P2:neural_pitch, P3:tonal_context |
| **F** (Forecast) | E+M+P outputs, H³ L0+L1 trends | F0:consonance_forecast, F1:pitch_forecast, F2:tonal_forecast, F3:interval_forecast |

---

## 5. Output Routing

### 5.1 Internal → Beliefs (this model)

| Output | → Belief | Type |
|--------|----------|------|
| P0:consonance_signal | → `harmonic_stability` (50% weight) | Core observe |
| P1:template_match | → `harmonic_stability` (30% weight) | Core observe |
| E2:hierarchy | → `harmonic_stability` (20% weight) | Core observe |
| E2:hierarchy | → `interval_quality` | Appraisal source |
| P1:template_match | → `harmonic_template_match` | Appraisal source |
| F0:consonance_forecast | → `consonance_trajectory` | Anticipation source |

### 5.2 External → Other Models

| Output | → Model | Purpose |
|--------|---------|---------|
| E0:nps | → PSCL (SPU-α2) | Cortical pitch salience input |
| E1:harmonicity | → PCCR (SPU-α3) | Chroma tuning from harmonicity |
| P0:consonance_signal | → SRP (ARU-α1) | Consonance → opioid_proxy (F6) |
| E1:harmonicity | → SRP (ARU-α1) | Harmonicity → pleasure (F6) |
| P0:consonance_signal | → MEAMN (IMU-α3) | Consonance → memory binding (F4) |
| P0:consonance_signal | → STAI (SPU-β1) | Aesthetic evaluation input |
| E0:nps | → SDED (SPU-γ3) | Early roughness signal baseline |

---

## 6. Brain Regions

| Region | Location | BCH Role | Evidence |
|--------|----------|----------|----------|
| **Inferior Colliculus** | Brainstem (0,−32,−8) | FFR generation (primary) | Bidelman 2009, 2013 |
| **Auditory Nerve** | Peripheral | Pitch salience encoding (70-fiber model) | Bidelman & Heinz 2011 |
| **Cochlear Nucleus** | Brainstem (±10,−38,−40) | Early spectral processing | Cousineau 2015 |
| **Auditory Brainstem** | Brainstem (0,−30,−10) | Harmonic encoding, consonance hierarchy | Bidelman & Krishnan 2009 |
| **Heschl's Gyrus (A1)** | Cortex (±44,−18,8) | Phase-locked dissonance representation | Fishman 2001; Tabas 2019 |
| **Superior Temporal Gyrus** | Lateral temporal | High gamma dissonance sensitivity | Foo 2016 |

---

## 7. Evidence Summary

| Metric | Value |
|--------|-------|
| Papers | 13 primary + supporting |
| Primary correlation | r = 0.81 (Bidelman 2009, synthetic, N=10) |
| Replication | r = 0.34 (Cousineau 2015, synthetic, N=14) |
| Natural sounds | NOT significant (Cousineau 2015) |
| Evidence modalities | FFR, AN model, ECoG, MEG, ERP, intracranial, behavioral |
| Falsification | 2/5 confirmed |
| Key qualification | NPS-behavior correlation is stimulus-dependent |

---

*See individual layer files for exact computation formulas:*
- [BCH-extraction.md](bch/BCH-extraction.md) — E-layer (4D)
- [BCH-temporal-integration.md](bch/BCH-temporal-integration.md) — M-layer (4D)
- [BCH-cognitive-present.md](bch/BCH-cognitive-present.md) — P-layer (4D)
- [BCH-forecast.md](bch/BCH-forecast.md) — F-layer (4D)

---
---

# PSCL — Pitch Salience Cortical Localization

**Model**: SPU-α2-PSCL
**Type**: Depth 1 — reads BCH relay output + R³/H³
**Tier**: α (Mechanistic, >90% confidence)
**Output**: 16D per frame (4 layers × 4D)
**Phase**: 0c (after BCH in Phase 0a — reads BCH output)

---

## 1. Identity

PSCL models how pitch salience is represented in anterolateral Heschl's Gyrus (non-primary auditory cortex). This is the cortical stage of pitch salience processing — after BCH's brainstem analysis. PSCL answers: "How strongly does the cortex represent this pitch?"

PSCL is a **Depth 1 model**: it reads BCH's relay output (brainstem NPS, harmonicity, consonance signal, pitch forecast) and combines this with direct R³/H³ features to produce cortical-level pitch salience representations.

---

## 2. R³ Input Map (Post-Freeze 97D)

PSCL reads **26 direct R³ indices** from 4 groups:

| # | R³ Index | Feature | Group | Scientific Basis |
|---|----------|---------|-------|------------------|
| 1 | **[4]** | sensory_pleasantness | A: Consonance | Sethares 2005 — spectral regularity |
| 2 | **[5]** | inharmonicity | A: Consonance | Fletcher 1934 — harmonic series deviation |
| 3 | **[14]** | tonalness | C: Timbre | Harmonic-to-noise ratio |
| 4 | **[15]** | clarity | C: Timbre | Signal clarity |
| 5 | **[16]** | spectral_smoothness | C: Timbre | Spectral shape |
| 6 | **[17]** | spectral_autocorrelation | C: Timbre | Harmonic periodicity |
| 7 | **[18]** | tristimulus1 | C: Timbre | Fundamental strength (F0) |
| 8 | **[19]** | tristimulus2 | C: Timbre | 2nd–4th harmonic energy |
| 9 | **[20]** | tristimulus3 | C: Timbre | 5th+ harmonic energy |
| 10 | **[22]** | distribution_entropy | D: Change | Spectral complexity |
| 11 | **[23]** | distribution_flatness | D: Change | Wiener entropy |
| 12 | **[24]** | distribution_concentration | D: Change | Herfindahl spectral focus |
| 13–24 | **[25:37]** | chroma_vector (12D) | F: Pitch/Chroma | Pitch class distribution |
| 25 | **[37]** | pitch_height | F: Pitch/Chroma | Log-frequency register |
| 26 | **[39]** | pitch_salience | F: Pitch/Chroma | Harmonic peak prominence |

### Dissolved Features

Old R³ Group E interactions (`x_l0l5` [25:33], `x_l5l7` [41:49]) are dissolved per R³ ontology freeze v1.0.0. PSCL no longer reads these; its E-layer and M-layer use direct R³ features.

### Upstream Input: BCH Relay (16D)

PSCL reads 4 BCH outputs via M3 integration:

| BCH Output | Layer | Purpose |
|------------|-------|---------|
| E0:nps | E-layer | Brainstem neural pitch salience |
| E1:harmonicity | E-layer | Harmonic series conformity |
| P0:consonance_signal | P-layer | Perceptual consonance |
| F1:pitch_forecast | F-layer | Brainstem pitch trajectory |

---

## 3. H³ Temporal Demand (24 tuples)

PSCL operates at cortical timescales: H3 (23ms auditory processing) and H6 (200ms cortical evaluation).

### 3.1 Present Demands (L2 — Integration, 11 tuples)

| # | R³ Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 14 | tonalness | 3 | M0 (value) | L2 | Current tonal quality |
| 2 | 15 | clarity | 3 | M0 (value) | L2 | Current signal clarity |
| 3 | 17 | spectral_autocorrelation | 3 | M0 (value) | L2 | Current harmonic periodicity |
| 4 | 5 | inharmonicity | 3 | M0 (value) | L2 | Current inharmonicity |
| 5 | 18 | tristimulus1 | 3 | M0 (value) | L2 | Current F0 strength |
| 6 | 22 | distribution_entropy | 3 | M0 (value) | L2 | Current spectral complexity |
| 7 | 24 | distribution_concentration | 3 | M0 (value) | L2 | Current spectral focus |
| 8 | 4 | sensory_pleasantness | 3 | M0 (value) | L2 | Current pleasantness |
| 9 | 39 | pitch_salience | 3 | M0 (value) | L2 | Pitch salience at 23ms |
| 10 | 39 | pitch_salience | 6 | M0 (value) | L2 | Pitch salience at 200ms |
| 11 | 37 | pitch_height | 6 | M0 (value) | L2 | Pitch height at 200ms |

### 3.2 Memory Demands (L0 — Backward, 9 tuples)

| # | R³ Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 14 | tonalness | 6 | M1 (mean) | L0 | Sustained tonalness 200ms |
| 2 | 17 | spectral_autocorrelation | 6 | M1 (mean) | L0 | Sustained autocorrelation 200ms |
| 3 | 18 | tristimulus1 | 6 | M1 (mean) | L0 | Sustained F0 strength 200ms |
| 4 | 22 | distribution_entropy | 6 | M1 (mean) | L0 | Sustained entropy 200ms |
| 5 | 39 | pitch_salience | 6 | M1 (mean) | L0 | Mean pitch salience 200ms |
| 6 | 14 | tonalness | 6 | M18 (trend) | L0 | Tonalness trend 200ms |
| 7 | 39 | pitch_salience | 6 | M18 (trend) | L0 | Pitch salience trend 200ms |
| 8 | 37 | pitch_height | 6 | M8 (velocity) | L0 | Pitch height velocity 200ms |
| 9 | 24 | distribution_concentration | 6 | M14 (periodicity) | L0 | Concentration periodicity 200ms |

### 3.3 Forward Demands (L1 — Prediction, 4 tuples)

| # | R³ Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 14 | tonalness | 6 | M1 (mean) | L1 | Expected tonalness 200ms ahead |
| 2 | 39 | pitch_salience | 6 | M1 (mean) | L1 | Expected pitch salience 200ms ahead |
| 3 | 37 | pitch_height | 6 | M1 (mean) | L1 | Expected pitch height 200ms ahead |
| 4 | 24 | distribution_concentration | 6 | M18 (trend) | L1 | Concentration trend 200ms ahead |

**Total**: 24 tuples (11 L2 + 9 L0 + 4 L1) of 223,488 theoretical = 0.011%

---

## 4. Pipeline: R³ → H³ → BCH → 4-Layer Output (16D)

```
R³ (26 direct)  ──────────────────────────────────────┐
                                                       ▼
                                               ┌──────────────┐
                                               │  E-LAYER (4D) │
                                               │  Extraction   │
                                               └──────┬───────┘
                                                      │ E0..E3
                                                      ▼
                                               ┌──────────────┐
H³ L2+L0 tuples  ────────────────────────────►│  M-LAYER (4D) │
BCH relay (16D)  ─────────────────────────────►│  Temporal     │
                                               │  Integration  │
                                               └──────┬───────┘
                                                      │ M0..M3
                                                      ▼
                                               ┌──────────────┐
R³ direct  ────────────────────────────────────►│  P-LAYER (4D) │
H³ L2     ─────────────────────────────────────►│  Cognitive    │
E+M outputs  ──────────────────────────────────►│  Present      │
                                               └──────┬───────┘
                                                      │ P0..P3
                                                      ▼
                                               ┌──────────────┐
P+M outputs  ──────────────────────────────────►│  F-LAYER (4D) │
H³ L0+L1 (trends)  ───────────────────────────►│  Forecast     │
BCH.F1  ───────────────────────────────────────►│               │
                                               └──────┬───────┘
                                                      │ F0..F3
                                                      ▼
                                               PSCL OUTPUT (16D)
```

### Layer Dependency

| Layer | Reads From | Outputs |
|-------|-----------|---------|
| **E** (Extraction) | R³ direct only | E0:pitch_salience_raw, E1:hg_activation_proxy, E2:salience_gradient, E3:spectral_focus |
| **M** (Memory) | H³ L2+L0 tuples, R³, BCH relay | M0:salience_sustained, M1:spectral_coherence, M2:tonal_salience_ctx, M3:bch_integration |
| **P** (Present) | R³, H³, E-layer, M-layer | P0:pitch_prominence_sig, P1:hg_cortical_response, P2:periodicity_clarity, P3:salience_hierarchy |
| **F** (Forecast) | P+M outputs, H³ L0+L1, BCH.F1 | F0:pitch_continuation, F1:salience_direction, F2:melody_propagation, F3:register_trajectory |

---

## 5. Output Routing

### 5.1 Internal → Beliefs (this model)

| Output | → Belief | Type |
|--------|----------|------|
| P0:pitch_prominence_sig | → `pitch_prominence` (60% weight) | Core observe |
| P1:hg_cortical_response | → `pitch_prominence` (25% weight) | Core observe |
| P3:salience_hierarchy | → `pitch_prominence` (15% weight) | Core observe |
| F0:pitch_continuation | → `pitch_continuation` | Anticipation source |

### 5.2 External → Other Models

| Output | → Model | Purpose |
|--------|---------|---------|
| P0:pitch_prominence_sig | → PCCR (SPU-α3) | Pitch prominence gates chroma identification |
| P2:periodicity_clarity | → PCCR (SPU-α3) | Periodicity quality for chroma tuning |
| F2:melody_propagation | → HMCE (STU-α1) | Melody stream → temporal encoding |
| F1:salience_direction | → PCCR (SPU-α3) | Salience trajectory for chroma prediction |
| P0:pitch_prominence_sig | → SRP (ARU-α1) | Pitch salience → reward computation |

---

## 6. Brain Regions

| Region | Location | PSCL Role | Evidence |
|--------|----------|-----------|----------|
| **Anterolateral HG (R)** | Tal: (48,−11,3) | Primary pitch salience representation | Penagos 2004 (fMRI) |
| **Anterolateral HG (L)** | Tal: (−55,−5,3) | Bilateral pitch salience | Penagos 2004 (fMRI) |
| **Anterolateral HG (R)** | Tal: (43,−6,18) | Pitch chroma source (IRN) | Briley 2013 (EEG) |
| **Right HG** | MNI: (48,−10,7) | Low-salience upregulation | Bravo 2017 (fMRI) |
| **Right STG (anterior)** | ECoG grid | Dissonant-sensitive gradient | Foo 2016 (ECoG) |
| **Primary AC (medial HG)** | Control | Tonotopy only — NOT pitch salience | Briley 2013 |

---

## 7. Evidence Summary

| Metric | Value |
|--------|-------|
| Papers | 14 primary |
| Evidence modalities | fMRI (3T+7T), MEG, EEG, ECoG, intracranial depth |
| Total N | ~190+ |
| Convergent finding | Anterolateral HG = primary cortical pitch salience hub |
| Key qualification | Pitch sensitivity (focal) ≠ pitch selectivity (distributed) — Allen 2022 |
| Coordinate convergence | alHG bilateral, 5–15mm spread across methods |

---

*See individual layer files for exact computation formulas:*
- [PSCL-extraction.md](pscl/PSCL-extraction.md) — E-layer (4D)
- [PSCL-temporal-integration.md](pscl/PSCL-temporal-integration.md) — M-layer (4D)
- [PSCL-cognitive-present.md](pscl/PSCL-cognitive-present.md) — P-layer (4D)
- [PSCL-forecast.md](pscl/PSCL-forecast.md) — F-layer (4D)

---
---

# PCCR — Pitch Chroma Cortical Representation

**Model**: SPU-α3-PCCR
**Type**: Associator (Depth 2) — reads BCH + PSCL upstream + R³/H³
**Tier**: α (Mechanistic, 75-90% confidence)
**Output**: 11D per frame — E(4) + M(1) + P(3) + F(3)
**Phase**: After PSCL (reads BCH + PSCL outputs)

---

## 1. Identity

PCCR transforms BCH (brainstem consonance) and PSCL (cortical pitch salience) outputs alongside R³ chroma features and H³ temporal morphologies into an 11D octave-invariant pitch-class representation. This is the deepest model in the F1 pipeline.

## 2. Key Features

- **Upstream reads**: BCH E1:harmonicity, E2:hierarchy, PSCL P0:pitch_prominence, P2:periodicity_clarity
- **Graceful degradation**: Without BCH → P1/P2 degraded; without PSCL → P0/P2 degraded; without both → R³-only E-layer (functional but weak)
- **Chroma vector**: Reads R³[25:37] (12D pitch class distribution)

## 3. H³ Temporal Demand (14 tuples)

- **L2 Integration** (5): PCE at H3/H6, pitch_height at H3/H6, tonalness at H6
- **L0 Memory** (5): PCE trend/mean, pitch_height velocity, tonalness periodicity, pitch_salience mean
- **L1 Prediction** (4): Expected PCE, pitch_height, tonalness, pitch_salience at 200ms

## 4. Layer Outputs

| Layer | Dims | Key Outputs |
|-------|------|-------------|
| E (4D) | [0:4] | chroma_energy, chroma_clarity, octave_coherence, pitch_class_confidence |
| M (1D) | [4:5] | chroma_stability |
| P (3D) | [5:8] | chroma_identity_signal, octave_equivalence_index, chroma_salience |
| F (3D) | [8:11] | chroma_continuation, chroma_transition, chroma_resolution |

## 5. Beliefs (2)

| Belief | Type | Source |
|--------|------|--------|
| pitch_identity | Core (τ=0.4) | from PCCR mechanism |
| octave_equivalence | Appraisal | from PCCR mechanism |

## 6. Brain Regions

- **Anterolateral HG**: Chroma encoding center (Patterson 2002, Briley 2013)
- **STG**: Octave-invariant pitch (Warren 2003)
- **STS**: Pitch class processing (Griffiths 2010)
- **IFG**: Pitch categorization (Zatorre 2002)

*Layer files:* [PCCR-extraction.md](pccr/PCCR-extraction.md), [PCCR-temporal-integration.md](pccr/PCCR-temporal-integration.md), [PCCR-cognitive-present.md](pccr/PCCR-cognitive-present.md), [PCCR-forecast.md](pccr/PCCR-forecast.md)

---
---

# MIAA — Musical Imagery Auditory Activation

**Model**: SPU-β3-MIAA
**Type**: Relay (Depth 0) — reads R³/H³ directly
**Tier**: β (Observation-compatible, 70-90% confidence)
**Output**: 11D per frame — E(3) + M(2) + P(3) + F(3)
**Phase**: 0a (independent relay)

---

## 1. Identity

MIAA models auditory cortex activation during musical imagery — when a listener imagines music without physical sound. Kraemer 2005: AC active during silence, F(1,14)=48.92, p<.0001. Familiarity enhances BA22 activation (p<.0001). Instrumental > lyrics in A1 (p<.0005).

## 2. R³ Inputs (10 features)

[5] inharmonicity, [10] loudness, [12] warmth, [14] tonalness, [15] clarity, [17] spectral_autocorrelation (replaces dissolved x_l5l7), [18-20] tristimulus1-3, [21] spectral_flux

## 3. H³ Temporal Demand (11 tuples)

- **L2 Integration** (5): tonalness/tristimulus1-3 at H2 gamma, inharmonicity at H5
- **L0 Memory** (6): tonalness/warmth/clarity/loudness means, spectral_flux entropy, spectral_auto at H5/H8

## 4. Layer Outputs

| Layer | Dims | Key Outputs |
|-------|------|-------------|
| E (3D) | [0:3] | imagery_activation, familiarity_enhancement, a1_modulation |
| M (2D) | [3:5] | activation_function, familiarity_effect |
| P (3D) | [5:8] | melody_retrieval, continuation_prediction, phrase_structure |
| F (3D) | [8:11] | melody_continuation_pred, ac_activation_pred, recognition_pred |

## 5. Beliefs (2)

| Belief | Type | Source |
|--------|------|--------|
| timbral_character | Core (τ=0.5) | from MIAA mechanism |
| imagery_recognition | Anticipation | from MIAA mechanism |

## 6. Brain Regions

- **BA22 / posterior STG**: Imagery activation hub (Kraemer 2005)
- **Primary AC (A1_HG)**: Instrumental imagery modulation (Kraemer 2005)

*Layer files:* [MIAA-extraction.md](miaa/MIAA-extraction.md), [MIAA-temporal-integration.md](miaa/MIAA-temporal-integration.md), [MIAA-cognitive-present.md](miaa/MIAA-cognitive-present.md), [MIAA-forecast.md](miaa/MIAA-forecast.md)

---
---

# SDED — Sensory Dissonance Early Detection

**Model**: SPU-γ3-SDED
**Type**: Relay (Depth 0) — reads R³/H³ directly
**Tier**: γ (Preliminary, 50-70% confidence)
**Output**: 10D per frame — E(3) + M(1) + P(3) + F(3)
**Phase**: 0a (independent relay)

---

## 1. Identity

SDED models pre-attentive roughness detection at brainstem-cortex level. Key insight: neural machinery for dissonance detection is universal (early MMN 152-258ms), but behavioral discrimination is expertise-dependent (late MMN 232-314ms musicians only). Crespo-Bojorque 2018, N=32.

## 2. R³ Inputs (8 features)

[0] roughness, [1] sethares, [2] helmholtz_kang, [3] stumpf, [5] inharmonicity, [14] tonalness, [17] spectral_autocorrelation (replaces dissolved x_l5l7), [18] tristimulus1

## 3. H³ Temporal Demand (9 tuples)

- **L2 Integration** (8): roughness/sethares/helmholtz/inharmonicity/tristimulus1 at H0, roughness mean/helmholtz mean/spectral_auto at H3
- **L0 Memory** (1): tonalness mean at H3

## 4. Layer Outputs

| Layer | Dims | Key Outputs |
|-------|------|-------------|
| E (3D) | [0:3] | early_detection, mmn_dissonance, behavioral_accuracy |
| M (1D) | [3:4] | detection_function |
| P (3D) | [4:7] | roughness_detection, deviation_detection, behavioral_response |
| F (3D) | [7:10] | dissonance_detection_pred, behavioral_accuracy_pred, training_effect_pred |

## 5. Beliefs (1)

| Belief | Type | Source |
|--------|------|--------|
| spectral_complexity | Appraisal | M0, P0, P1 |

## 6. Brain Regions

- **Heschl's Gyrus (A1)**: Phase-locked roughness encoder (Fishman 2001)
- **Inferior Colliculus**: Innate consonance hierarchy (Bidelman 2013)
- **Right STG**: High-gamma dissonance sites (Foo 2016)

*Layer files:* [SDED-extraction.md](sded/SDED-extraction.md), [SDED-temporal-integration.md](sded/SDED-temporal-integration.md), [SDED-cognitive-present.md](sded/SDED-cognitive-present.md), [SDED-forecast.md](sded/SDED-forecast.md)

---
---

# CSG — Consonance-Salience Gradient

**Model**: ASU-α3-CSG
**Type**: Relay (Depth 0) — reads R³/H³ directly
**Tier**: α (Mechanistic, 90-95% confidence)
**Output**: 12D per frame — E(3) + M(3) + P(3) + F(3)
**Phase**: 0a (independent relay)

---

## 1. Identity

CSG models how consonance level systematically modulates salience network activation. Bravo 2017: strong dissonance activates ACC/bilateral AI (d=5.16); intermediate dissonance increases Heschl's gyrus load (d=1.9); consonance enables efficient processing with positive valence (d=3.31, N=45 behavioral + N=12 imaging).

**NOTE**: CSG uses tanh [-1, 1] for valence dimensions (E2:consonance_valence, P1:affective_evaluation, F0:valence_pred). Output clamped to [-1, 1] not [0, 1].

## 2. R³ Inputs (9 features)

[0] roughness, [1] sethares, [4] sensory_pleasantness, [9] spectral_centroid, [10] loudness, [12] warmth, [17] spectral_autocorrelation (replaces dissolved x_l0l5), [21] spectral_flux, [22] energy_change

## 3. H³ Temporal Demand (18 tuples)

Multi-scale: H0(25ms) → H3(100ms) → H4(125ms) → H8(500ms) → H16(1000ms)
- **Roughness** (4): H0 value, H3 mean+std, H16 mean
- **Pleasantness** (3): H3 value+velocity, H16 mean
- **Loudness** (3): H3 value+entropy, H16 mean
- **Sethares** (2): H3 value, H8 velocity
- **Spectral flux** (1): H4 velocity
- **Spectral auto** (3): H3/H8/H16 value+mean
- **Energy change** (1): H3 velocity
- **Centroid** (1): H3 value

## 4. Layer Outputs

| Layer | Dims | Key Outputs |
|-------|------|-------------|
| E (3D) | [0:3] | salience_activation, sensory_evidence, consonance_valence (tanh) |
| M (3D) | [3:6] | salience_response, rt_valence_judgment, aesthetic_appreciation |
| P (3D) | [6:9] | salience_network, affective_evaluation (tanh), sensory_load |
| F (3D) | [9:12] | valence_pred (tanh), processing_pred, aesthetic_pred |

## 5. Beliefs (1)

| Belief | Type | Source |
|--------|------|--------|
| consonance_salience_gradient | Appraisal | P0, E0, M0 |

## 6. Brain Regions

- **ACC**: Salience hub for dissonance (Bravo 2017, d=5.16)
- **Anterior insula**: Salience network partner (Bravo 2017)
- **Heschl's Gyrus**: Sensory evidence weighting (Bravo 2017)
- **Amygdala**: Dissonance-driven salience (Koelsch 2006)

*Layer files:* [CSG-extraction.md](csg/CSG-extraction.md), [CSG-temporal-integration.md](csg/CSG-temporal-integration.md), [CSG-cognitive-present.md](csg/CSG-cognitive-present.md), [CSG-forecast.md](csg/CSG-forecast.md)

---
---

# MPG — Melodic Processing Gradient

**Model**: NDU-α1-MPG
**Type**: Relay (Depth 0) — reads R³/H³ directly
**Tier**: α (Mechanistic, 80-92% confidence)
**Output**: 10D per frame — E(4) + M(3) + P(2) + F(1)
**Phase**: 0a (independent relay)

---

## 1. Identity

MPG models the posterior-to-anterior cortical gradient for melodic processing. Posterior regions (medial HG) process sequence onset; anterior regions (STG) process subsequent notes and pitch variation (Rupp et al. 2022, MEG, N=20).

## 2. R³ Inputs (8 features)

[7] amplitude, [11] onset_strength, [13] sharpness, [21] spectral_flux, [37] pitch_height (replaces dissolved pitch_change), [38] pitch_class_entropy, [39] pitch_salience (replaces dissolved x_l4l5), [42] beat_strength (replaces dissolved x_l0l5)

## 3. H³ Temporal Demand (16 tuples)

- **L2 Integration** (13): spectral_flux H0/H1/H3, onset H0/H3/H16, sharpness H3 value+std, pitch_height H3/H16, PCE H4, amplitude H3, beat_strength H3
- **L0 Memory** (3): sharpness velocity H4, pitch_height trend H4, pitch_salience velocity H3

## 4. Layer Outputs

| Layer | Dims | Key Outputs |
|-------|------|-------------|
| E (4D) | [0:4] | onset_posterior, sequence_anterior, contour_complexity, gradient_ratio |
| M (3D) | [4:7] | activity_x, posterior_activity, anterior_activity |
| P (2D) | [7:9] | onset_state, contour_state |
| F (1D) | [9:10] | phrase_boundary_pred |

## 5. Beliefs (2)

| Belief | Type | Source |
|--------|------|--------|
| melodic_contour_tracking | Appraisal | from MPG mechanism |
| contour_continuation | Anticipation | from MPG mechanism |

## 6. Brain Regions

- **Medial HG (A1)**: Onset pitch detection, posterior processing (Patterson 2002)
- **STG**: Melodic contour, anterior processing (Rupp 2022, Foo 2016)
- **IFG**: Phrase boundary integration (Cheung 2019)

*Layer files:* [MPG-extraction.md](mpg/MPG-extraction.md), [MPG-temporal-integration.md](mpg/MPG-temporal-integration.md), [MPG-cognitive-present.md](mpg/MPG-cognitive-present.md), [MPG-forecast.md](mpg/MPG-forecast.md)

---
---

# SDNPS — Stimulus-Dependent Neural Pitch Salience

**Model**: SPU-γ1-SDNPS
**Type**: Relay (Depth 0) — reads R³/H³ directly
**Tier**: γ (Preliminary, 40-70% confidence)
**Output**: 10D per frame — E(3) + M(1) + P(3) + F(3)
**Phase**: 0a (independent relay)

---

## 1. Identity

SDNPS models the critical finding that brainstem FFR-derived Neural Pitch Salience predicts behavioral consonance for synthetic tones (r=0.34, p<0.03) but fails to generalize to natural sounds (sax r=0.24 n.s., voice r=-0.10 n.s.). NPS ↔ roughness is the one invariant (r=-0.57, p<1e-05). Cousineau et al. 2015, N=14.

## 2. R³ Inputs (7 features)

[0] roughness, [1] sethares, [5] inharmonicity, [14] tonalness, [17] spectral_autocorrelation, [18-20] tristimulus1-3

Key derived feature: `tristimulus_balance = 1 - std(trist1, trist2, trist3)` — uses `correction=0` to avoid NaN for T=1.

## 3. H³ Temporal Demand (10 tuples)

- **L2 Integration / H0 Gamma** (5): roughness, helmholtz_kang, inharmonicity, tonalness, tristimulus1 all at H0
- **L2 Integration / H3 Alpha-Beta** (3): roughness mean, inharmonicity mean, spectral_auto periodicity
- **L0 Memory** (1): tonalness mean H3 — generalization limit predictor
- **L0 Memory / H6** (1): roughness periodicity H6 — stimulus regularity

## 4. Layer Outputs

| Layer | Dims | Key Outputs |
|-------|------|-------------|
| E (3D) | [0:3] | nps_value (FFR proxy), stimulus_dependency, roughness_corr (r=-0.57) |
| M (1D) | [3:4] | nps_stimulus_function (E0×E1 product) |
| P (3D) | [4:7] | ffr_encoding, harmonicity_proxy, roughness_interference |
| F (3D) | [7:10] | behavioral_consonance_pred, roughness_response_pred, generalization_limit |

## 5. Beliefs

None at this time. May gain beliefs as integration matures.

## 6. Brain Regions

- **Inferior Colliculus**: FFR generator for NPS (Cousineau 2015)
- **Anterolateral HG**: Cortical pitch salience (Penagos 2004)
- **Right STG**: Dissonance-sensitive gradient (Foo 2016)

*Layer files:* [SDNPS-extraction.md](sdnps/SDNPS-extraction.md), [SDNPS-temporal-integration.md](sdnps/SDNPS-temporal-integration.md), [SDNPS-cognitive-present.md](sdnps/SDNPS-cognitive-present.md), [SDNPS-forecast.md](sdnps/SDNPS-forecast.md)

---
---

# PNH — Pythagorean Neural Hierarchy

**Model**: IMU-α2-PNH
**Type**: Relay (Depth 0) — reads R³/H³ directly
**Tier**: α (Mechanistic, 90-100% confidence)
**Output**: 11D per frame — H(3) + M(2) + P(3) + F(3)
**Phase**: 0a (independent relay)

---

## 1. Identity

PNH models how neural responses to musical intervals follow the Pythagorean ratio complexity hierarchy: log₂(n×d) predicts BOLD activation in IFG/ACC. Musicians show this pattern in 5 ROIs (L-IFG, L-STG, L-MFG, L-IPL, ACC); non-musicians in R-IFG only. Bidelman & Krishnan 2009, r≥0.81, N=10.

## 2. R³ Inputs (10 features)

[0] roughness, [1] sethares, [2] helmholtz_kang, [3] stumpf, [4] sensory_pleasantness, [5] inharmonicity, [6] harmonic_deviation, [8] velocity_D (doc said [10] loudness — corrected), [14] tonalness, [17] spectral_autocorrelation

**R³ correction**: Model doc references `x_l0l5[25:33]` (dissolved E group). Replaced with inline `velocity_D × roughness` energy-consonance coupling.

## 3. H³ Temporal Demand (15 tuples)

- **L2 / H10 Chord** (7): roughness, inharmonicity, stumpf, pleasantness, tonalness, velocity_D values + spectral_auto periodicity
- **L2 / H14** (1): stumpf mean
- **L0 / H14** (4): roughness mean, inharmonicity mean, tonalness std, harmonic_deviation value
- **L0 / H18** (3): roughness trend, pleasantness stability, helmholtz mean

## 4. Layer Outputs

| Layer | Dims | Key Outputs |
|-------|------|-------------|
| H (3D) | [0:3] | ratio_encoding (α=0.75), conflict_response (β=0.70), expertise_mod (γ=0.60) |
| M (2D) | [3:5] | ratio_complexity (log₂(n×d) proxy), neural_activation (H0×H1) |
| P (3D) | [5:8] | ratio_enc, conflict_mon (IFG/ACC), consonance_pref (η²p=0.685) |
| F (3D) | [8:11] | dissonance_res_fc, pref_judgment_fc, expertise_mod_fc |

## 5. Beliefs

None at this time. May gain beliefs as integration matures.

## 6. Brain Regions

- **L-IFG (BA 44/45)**: Conflict monitoring for ratio complexity (Kim 2021)
- **ACC**: Salience detection for dissonance (Bidelman & Krishnan 2009)
- **L-STG**: Auditory encoding (Kim 2021)
- **alHG**: Early consonance encoding, POR (Tabas 2019)

*Layer files:* [PNH-extraction.md](pnh/PNH-extraction.md), [PNH-temporal-integration.md](pnh/PNH-temporal-integration.md), [PNH-cognitive-present.md](pnh/PNH-cognitive-present.md), [PNH-forecast.md](pnh/PNH-forecast.md)

---
---

# TPRD — Tonotopy-Pitch Representation Dissociation

**Model**: IMU-β8-TPRD
**Type**: Relay (Depth 0) — reads R³/H³ directly
**Tier**: β (Observation-compatible, 70-90% confidence)
**Output**: 10D per frame — T(3) + M(2) + P(2) + F(3)
**Phase**: 0a (independent relay)

---

## 1. Identity

TPRD models the fundamental distinction between tonotopic (frequency) encoding in primary/medial Heschl's gyrus and pitch (F0) representation in nonprimary/lateral HG. Resolves the long-standing debate: tonotopy ≠ pitch. Briley et al. 2013, Cerebral Cortex 23(11):2601-2610.

## 2. R³ Inputs (6 features)

[0] roughness, [5] inharmonicity, [7] velocity_A, [14] tonalness, [17] spectral_autocorrelation, [22] entropy

**R³ corrections applied**:
- `[10] loudness` → `[8] velocity_D` (97D naming)
- `x_l0l5[25:33]` dissolved → inline energy×consonance coupling
- `x_l5l7[41:49]` dissolved → spectral_autocorrelation [17]

## 3. H³ Temporal Demand (18 tuples)

Dual horizon sets:
- **Pitch-processing chain H0→H3→H6** (10): stumpf/tonalness at H0, stumpf/tonalness means + spectral_auto periodicity at H3, stumpf/tonalness means + spectral_auto period + entropy + velocity_A at H6
- **Mnemonic horizons H10→H14→H18** (8): roughness/inharmonicity/harmonic_deviation/velocity_D at H10, roughness/inharmonicity/entropy means at H14, pleasantness stability at H18

## 4. Layer Outputs

| Layer | Dims | Key Outputs |
|-------|------|-------------|
| T (3D) | [0:3] | tonotopic (medial HG), pitch (lateral HG), dissociation |
| M (2D) | [3:5] | dissociation_idx (0=pitch, 0.5=balanced, 1=tono), spectral_pitch_r |
| P (2D) | [5:7] | tonotopic_state, pitch_state |
| F (3D) | [7:10] | pitch_percept_fc (50-200ms), tonotopic_adpt_fc (200-700ms), dissociation_fc (0.5-2s) |

## 5. Beliefs

None at this time. May gain beliefs as integration matures.

## 6. Brain Regions

- **Medial HG (primary)**: Tonotopic encoding — T0, P0 (Briley 2013)
- **Anterolateral HG (nonprimary)**: Pitch representation — T1, P1 (Briley 2013, Norman-Haignere 2013)
- **Right STG**: Dissonance-sensitive gradient — T2 (Foo 2016)

*Layer files:* [TPRD-extraction.md](tprd/TPRD-extraction.md), [TPRD-temporal-integration.md](tprd/TPRD-temporal-integration.md), [TPRD-cognitive-present.md](tprd/TPRD-cognitive-present.md), [TPRD-forecast.md](tprd/TPRD-forecast.md)
