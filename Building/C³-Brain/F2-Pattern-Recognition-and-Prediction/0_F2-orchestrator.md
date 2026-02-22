# F2 — Pattern Recognition & Prediction

**Function**: F2 Pattern Recognition & Prediction
**Unit**: PCU (Predictive Coding Unit) — all 10 models
**Models**: 10 (3 α-relays + 4 β-depth1 + 3 γ-depth2)
**Total output**: 110D (12+14+13+10+11+10+11+9+10+10)
**Beliefs**: 15 (4 Core + 6 Appraisal + 5 Anticipation) — all from α-tier
**H³ demands**: 173 tuples (57 implemented from α models + 116 from β/γ docs)
**Phase**: 1 (reads F1 beliefs + R³/H³)
**Implemented**: HTP, SPH, ICEM (3/10 models, 15/15 beliefs)

---

## 1. What F2 Does

F2 generates **predictive representations** at multiple timescales. It is the prediction engine — everything the brain "expects" before it arrives. Processing follows a hierarchical temporal pattern from low-level sensory prediction through uncertainty-weighted reward computation:

```
Audio → R³ (97D) ───┬────────────────────────────────────────────
H³ tuples ──────────┤
                    ▼
Depth 0:  HTP  (12D, relay)  ← hierarchical temporal prediction
          SPH  (14D, relay)  ← spatiotemporal prediction hierarchy
          ICEM (13D, relay)  ← information content → emotion model
                    │
                    ▼
Depth 1:  PWUP (10D)  ← precision-weighted uncertainty processing
          WMED (11D)  ← working memory–entrainment dissociation
          UDP  (10D)  ← uncertainty-driven pleasure
          CHPI (11D)  ← cross-modal harmonic predictive integration
                    │
                    ▼
Depth 2:  IGFE  (9D)  ← individual gamma frequency enhancement
          MAA  (10D)  ← multifactorial atonal appreciation
          PSH  (10D)  ← prediction silencing hypothesis
```

F2 is the first function in **Phase 1** (reads F1 beliefs). α-tier relays read R³/H³ directly; β-tier models additionally read α outputs; γ-tier models read α+β outputs.

---

## 2. Complete Model Inventory

| # | Model | Unit | Tier | Depth | Output | H³ | Beliefs | Status |
|---|-------|------|------|-------|--------|-----|---------|--------|
| 1 | **HTP** | PCU | α | 0 | 12D | 18 | 5 (2C+1A+2N) | **done** |
| 2 | **SPH** | PCU | α | 0 | 14D | 21 | 4 (1C+2A+1N) | **done** |
| 3 | **ICEM** | PCU | α | 0 | 13D | 18 | 6 (1C+3A+2N) | **done** |
| 4 | PWUP | PCU | β | 1 | 10D | 14 | 0 | pending |
| 5 | WMED | PCU | β | 1 | 11D | 16 | 0 | pending |
| 6 | UDP | PCU | β | 1 | 10D | 16 | 0 | pending |
| 7 | CHPI | PCU | β | 1 | 11D | 20 | 0 | pending |
| 8 | IGFE | PCU | γ | 2 | 9D | 18 | 0 | pending |
| 9 | MAA | PCU | γ | 2 | 10D | 14 | 0 | pending |
| 10 | PSH | PCU | γ | 2 | 10D | 18 | 0 | pending |

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

## 7. Dependency Graph

```
                          R³ (97D) + H³
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                  ▼
          HTP (α1)         SPH (α2)          ICEM (α3)
         12D relay        14D relay          13D relay
            │                 │                  │
            ├─────────┬───────┴──────────┬───────┤
            ▼         ▼                  ▼       ▼
        PWUP (β1)  WMED (β2)        UDP (β3)  CHPI (β4)
          10D        11D              10D        11D
            │         │                │         │
            ├─────────┼────────┬───────┼─────────┤
            ▼         ▼        ▼       ▼         ▼
         IGFE (γ1)  MAA (γ2)       PSH (γ3)
           9D        10D            10D
```

### Key Dependencies

| Model | Reads From |
|-------|-----------|
| PWUP (β1) | HTP.hierarchy_gradient, ICEM.information_content |
| WMED (β2) | PWUP.precision_weight |
| UDP (β3) | PWUP.uncertainty_index, WMED.wm_contribution |
| CHPI (β4) | HTP.hierarchy_gradient, PWUP.tonal_precision, ICEM.information_content, WMED.entrainment_strength |
| IGFE (γ1) | WMED.wm_contribution, HTP.hierarchy_gradient |
| MAA (γ2) | UDP.pleasure_index, PWUP.uncertainty_index, IGFE.gamma_sync |
| PSH (γ3) | HTP.hierarchy_gradient, PWUP.weighted_error, UDP.confirmation_reward, WMED.dissociation_index, MAA.appreciation_composite |

---

## 8. Documentation Structure

```
F2-Pattern-Recognition-and-Prediction/
├── 0_F2-orchestrator.md                  ← this file
├── collections.md                         ← full model inventory
├── mechanisms/
│   ├── 0_mechanisms-orchestrator.md       ← all 10 models documented
│   ├── htp/
│   │   ├── HTP-extraction.md              HTP E-layer (4D)
│   │   ├── HTP-temporal-integration.md    HTP M-layer (3D)
│   │   ├── HTP-cognitive-present.md       HTP P-layer (3D)
│   │   └── HTP-forecast.md               HTP F-layer (2D)
│   ├── sph/
│   │   ├── SPH-extraction.md              SPH E-layer (4D)
│   │   ├── SPH-temporal-integration.md    SPH M-layer (4D)
│   │   ├── SPH-cognitive-present.md       SPH P-layer (3D)
│   │   └── SPH-forecast.md               SPH F-layer (3D)
│   └── icem/
│       ├── ICEM-extraction.md              ICEM E-layer (4D)
│       ├── ICEM-temporal-integration.md    ICEM M-layer (5D)
│       ├── ICEM-cognitive-present.md       ICEM P-layer (2D)
│       └── ICEM-forecast.md               ICEM F-layer (2D)
└── beliefs/
    ├── 0_beliefs_orchestrator.md           ← all 15 beliefs documented
    ├── htp/
    │   ├── prediction_hierarchy.md        Core (τ=0.4)
    │   ├── prediction_accuracy.md         Core (τ=0.5)
    │   ├── hierarchy_coherence.md         Appraisal
    │   ├── abstract_future.md             Anticipation
    │   └── midlevel_future.md             Anticipation
    ├── sph/
    │   ├── sequence_match.md              Core (τ=0.45)
    │   ├── error_propagation.md           Appraisal
    │   ├── oscillatory_signature.md       Appraisal
    │   └── sequence_completion.md         Anticipation
    └── icem/
        ├── information_content.md         Core (τ=0.35)
        ├── arousal_scaling.md             Appraisal
        ├── valence_inversion.md           Appraisal
        ├── defense_cascade.md             Appraisal
        ├── arousal_change_pred.md         Anticipation
        └── valence_shift_pred.md          Anticipation
```

**3 α-tier models complete (15/15 beliefs, 57 H³ tuples).** Pending: 4 β-tier (PWUP, WMED, UDP, CHPI) + 3 γ-tier (IGFE, MAA, PSH) — 0 beliefs each, 116 H³ tuples total.
