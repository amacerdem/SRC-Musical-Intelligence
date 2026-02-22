# F2 — Pattern Recognition & Prediction

**Function**: F2 Pattern Recognition & Prediction
**Models**: 10 (from PCU unit) + cross-function contributions
**Beliefs**: 15 (4 Core + 6 Appraisal + 5 Anticipation)
**Phase**: 1 (reads F1 beliefs + R³/H³)
**Documented**: HTP, SPH, ICEM (3/10 models, 15/15 beliefs)

---

## 1. What F2 Does

F2 generates **predictive representations** at multiple timescales. It is the prediction engine — everything the brain "expects" before it arrives. Processing follows a hierarchical temporal pattern:

```
Audio → R³ (97D) → HTP (hierarchical temporal prediction)
                      → SPH (spatiotemporal prediction hierarchy)
                        → ICEM (information content emotion model)
                          → supporting models (PWUP, WMED, UDP, ...)
```

F2 is the first function in **Phase 1** (reads F1 beliefs). All core mechanisms read R³/H³ directly, but beliefs can reference F1 belief values as prediction context.

---

## 2. Complete Model Inventory

| # | Model | Unit | Tier | Depth | Output | Beliefs | Phase | Status |
|---|-------|------|------|-------|--------|---------|-------|--------|
| 1 | **HTP** | PCU | α | 0 | 12D | 5 (2C+1A+2N) | 1 | **done** |
| 2 | **SPH** | PCU | α | 0 | 14D | 4 (1C+2A+1N) | 1 | **done** |
| 3 | **ICEM** | PCU | α | 0 | 13D | 6 (1C+3A+2N) | 1 | **done** |
| 4 | PWUP | PCU | β | — | TBD | 0 | — | — |
| 5 | WMED | PCU | β | — | TBD | 0 | — | — |
| 6 | UDP | PCU | β | — | TBD | 0 | — | — |
| 7 | CHPI | PCU | β | — | TBD | 0 | — | — |
| 8 | IGFE | PCU | γ | — | TBD | 0 | — | — |
| 9 | MAA | PCU | γ | — | TBD | 0 | — | — |
| 10 | PSH | PCU | γ | — | TBD | 0 | — | — |

---

## 3. Complete Belief Inventory (15)

| # | Belief | Cat | τ | Owner | Mechanism Source | Status |
|---|--------|-----|---|-------|------------------|--------|
| 1 | **`prediction_hierarchy`** | **C** | **0.4** | **HTP** | E0(40%)+E1(30%)+E2(30%) | **done** |
| 2 | **`sequence_match`** | **C** | **0.45** | **SPH** | E0(40%)+P0(30%)+M2(30%) | **done** |
| 3 | **`information_content`** | **C** | **0.35** | **ICEM** | E0(40%)+M0(30%)+P0(30%) | **done** |
| 4 | **`prediction_accuracy`** | **C** | **0.5** | **HTP** | P0(50%)+P1(30%)+E3(20%) | **done** |
| 5 | **`hierarchy_coherence`** | **A** | — | **HTP** | E3(50%)+P2(30%)+P1(20%) | **done** |
| 6 | **`error_propagation`** | **A** | — | **SPH** | E1(40%)+P1(30%)+M3(30%) | **done** |
| 7 | **`oscillatory_signature`** | **A** | — | **SPH** | M2(40%)+M3(30%)+E3(30%) | **done** |
| 8 | **`defense_cascade`** | **A** | — | **ICEM** | E3(50%)+M3(30%)+M4(20%) | **done** |
| 9 | **`arousal_scaling`** | **A** | — | **ICEM** | E1(40%)+M1(30%)+P0(30%) | **done** |
| 10 | **`valence_inversion`** | **A** | — | **ICEM** | E2(40%)+M2(30%)+P1(30%) | **done** |
| 11 | **`abstract_future`** | **N** | — | **HTP** | F0:abstract_future_500ms | **done** |
| 12 | **`midlevel_future`** | **N** | — | **HTP** | F1:midlevel_future_200ms | **done** |
| 13 | **`sequence_completion`** | **N** | — | **SPH** | F1:sequence_completion_2s | **done** |
| 14 | **`arousal_change_pred`** | **N** | — | **ICEM** | F0:arousal_change_1_3s | **done** |
| 15 | **`valence_shift_pred`** | **N** | — | **ICEM** | F1:valence_shift_2_5s | **done** |

---

## 4. HTP R³ Ontology Mapping (Key Dissolved Features)

HTP's original spec referenced dissolved interaction features. Post-freeze replacements:

| Old Feature | Old Index | New Feature | New Index | Rationale |
|-------------|-----------|-------------|-----------|-----------|
| x_l0l5 (low coupling) | 25 | spectral_autocorrelation | 17 | Cross-band coupling serves same role |
| x_l4l5 (mid coupling) | 33 | pitch_salience | 39 | Perceptual mid-level pitch dynamics |
| x_l5l7 (high coupling) | 41 | tonal_stability | 60 | High-level tonal structure |
| spectral_centroid | 9 | sharpness | 13 | Perceptual brightness proxy |
| spectral_flux (onset) | 10 | onset_strength | 11 | Shifted in B group |
| M20 (entropy) | — | M13 (entropy) | — | Standard morph correction |

---

## 5. SPH R³ Ontology Mapping (Key Dissolved Features)

SPH's original spec referenced dissolved interaction features. Post-freeze replacements:

| Old Feature | Old Index | New Feature | New Index | Rationale |
|-------------|-----------|-------------|-----------|-----------|
| x_l0l5 (feedforward) | 25 | spectral_autocorrelation | 17 | Cross-band coupling serves feedforward role |
| x_l5l7 (hierarchy) | 41 | tonal_stability | 60 | High-level structural predictability |
| spectral_flux (onset) | 10 | onset_strength | 11 | Shifted in B group |
| spectral_change | 21 | spectral_flux | 21 | Same index, renamed |
| energy_change | 22 | distribution_entropy | 22 | Same index, different concept |
| chroma (v2) | 49 | chroma_C | 25 | F group first chroma bin |
| pitch_height (v2) | 61 | pitch_height | 37 | F group in 97D |
| pitch_salience (v2) | 63 | pitch_salience | 39 | F group in 97D |
| M20 (entropy) | — | M13 (entropy) | — | Standard morph correction |

---

## 6. ICEM R³ Ontology Mapping (Key Dissolved Features)

ICEM's original spec referenced dissolved interaction and information features. Post-freeze replacements:

| Old Feature | Old Index | New Feature | New Index | Rationale |
|-------------|-----------|-------------|-----------|-----------|
| x_l4l5 (arousal) | 33 | pitch_salience | 39 | Mid-level coupling for arousal pathway |
| x_l5l7 (valence) | 41 | tonal_stability | 60 | High-level abstraction for valence |
| loudness | 8 | loudness | 10 | Shifted in B group |
| spectral_flux (onset) | 10 | onset_strength | 11 | Shifted+renamed in B group |
| spectral_change | 21 | spectral_flux | 21 | Same index, renamed |
| energy_change | 22 | distribution_entropy | 22 | Same index, different concept |
| melodic_entropy (I group) | 87 | pitch_class_entropy | 38 | Dissolved I group → F group |
| key_clarity (v2) | 75 | key_clarity | 51 | Relocated to H group |
| M20 (entropy) | — | M13 (entropy) | — | Standard morph correction |

---

## 7. Documentation Structure

```
F2-Pattern-Recognition-and-Prediction/
├── 0_F2-orchestrator.md              ← this file
├── mechanisms/
│   ├── htp/
│   │   ├── HTP-extraction.md          HTP E-layer (4D)
│   │   ├── HTP-temporal-integration.md HTP M-layer (3D)
│   │   ├── HTP-cognitive-present.md   HTP P-layer (3D)
│   │   └── HTP-forecast.md            HTP F-layer (2D)
│   ├── sph/
│   │   ├── SPH-extraction.md          SPH E-layer (4D)
│   │   ├── SPH-temporal-integration.md SPH M-layer (4D)
│   │   ├── SPH-cognitive-present.md   SPH P-layer (3D)
│   │   └── SPH-forecast.md            SPH F-layer (3D)
│   └── icem/
│       ├── ICEM-extraction.md          ICEM E-layer (4D)
│       ├── ICEM-temporal-integration.md ICEM M-layer (5D)
│       ├── ICEM-cognitive-present.md   ICEM P-layer (2D)
│       └── ICEM-forecast.md            ICEM F-layer (2D)
└── beliefs/
    ├── htp/
    │   ├── prediction_hierarchy.md    Core (τ=0.4)
    │   ├── prediction_accuracy.md     Core (τ=0.5)
    │   ├── hierarchy_coherence.md     Appraisal
    │   ├── abstract_future.md         Anticipation
    │   └── midlevel_future.md         Anticipation
    ├── sph/
    │   ├── sequence_match.md          Core (τ=0.45)
    │   ├── error_propagation.md       Appraisal
    │   ├── oscillatory_signature.md   Appraisal
    │   └── sequence_completion.md     Anticipation
    └── icem/
        ├── information_content.md     Core (τ=0.35)
        ├── arousal_scaling.md         Appraisal
        ├── valence_inversion.md       Appraisal
        ├── defense_cascade.md         Appraisal
        ├── arousal_change_pred.md     Anticipation
        └── valence_shift_pred.md      Anticipation
```

**All 3 α-tier models complete (15/15 beliefs).** Next: β-tier supporting models (PWUP, WMED, UDP, CHPI) — 0 beliefs each.
