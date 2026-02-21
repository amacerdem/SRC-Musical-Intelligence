# F1 Mechanism Orchestrator — BCH (Brainstem Consonance Hierarchy)

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
- [BCH-extraction.md](BCH-extraction.md) — E-layer (4D)
- [BCH-temporal-integration.md](BCH-temporal-integration.md) — M-layer (4D)
- [BCH-cognitive-present.md](BCH-cognitive-present.md) — P-layer (4D)
- [BCH-forecast.md](BCH-forecast.md) — F-layer (4D)
