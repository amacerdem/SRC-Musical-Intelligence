# F2 Prediction Engine — Collections

> **NOTE**: This file was built by independently reading each model doc
> in `Docs/C³/Models/` and each mechanism in `Musical_Intelligence/brain/functions/f2/`.
> It does NOT copy from the orchestrator or ontology summaries.
> Counts and dimensions are snapshots — they will change as models are integrated.

---

## 1. Verified F2 Models (from Model Docs)

Independent scan of all 96 model docs confirmed that **all 10 PCU models** belong to F2
(Prediction Engine), and **no non-PCU models** have F2 as primary or secondary function.
PCU = Predictive Coding Unit — the entire unit maps to F2.

### 1.1 Implemented (3 models)

| Model | Unit-Tier | Doc OUTPUT_DIM | Code OUTPUT_DIM | Layers | H3 (v1) | Beliefs | Status |
|-------|-----------|----------------|-----------------|--------|---------|---------|--------|
| HTP | PCU-α1 | 12D | 12D | E4+M3+P3+F2 | 18 | 5 (2C+1A+2N) | done |
| SPH | PCU-α2 | 14D | 14D | E4+M4+P3+F3 | 21 | 4 (1C+2A+1N) | done |
| ICEM | PCU-α3 | 13D | 13D | E4+M5+P2+F2 | 18 | 6 (1C+3A+2N) | done |

All three are Relay nuclei (depth 0) — read R³/H³ directly, no upstream dependencies.
All doc dimensions match code exactly.

### 1.2 Not Yet Implemented (7 models)

| Model | Unit-Tier | Doc OUTPUT_DIM | Layers | H3 (v1) | Beliefs | Status |
|-------|-----------|----------------|--------|---------|---------|--------|
| PWUP | PCU-β1 | 10D | E4+P3+F3 | 14 | 0 | pending |
| WMED | PCU-β2 | 11D | E4+P3+F4 | 16 | 0 | pending |
| UDP | PCU-β3 | 10D | E4+P3+F3 | 16 | 0 | pending |
| CHPI | PCU-β4 | 11D | E4+P3+F4 | 20 | 0 | pending |
| IGFE | PCU-γ1 | 9D | E4+P3+F2 | 18 | 0 | pending |
| MAA | PCU-γ2 | 10D | E4+P3+F3 | 14 | 0 | pending |
| PSH | PCU-γ3 | 10D | E4+P3+F3 | 18 | 0 | pending |

**Structural pattern**: All β/γ models use 3-layer structure (E+P+F, no M layer),
while all α models use 4-layer structure (E+M+P+F). This reflects the maturity
gradient: α models have dedicated memory layers; β/γ models are computationally
simpler.

### 1.3 Full Model Descriptions

| Model | Full Name | Evidence Tier | Key Mechanism |
|-------|-----------|---------------|---------------|
| HTP | Hierarchical Temporal Prediction | α (>90%) | High-level ~500ms, mid ~200ms, low ~110ms prediction timing |
| SPH | Spatiotemporal Prediction Hierarchy | α (>90%) | Feedforward-feedback memory recognition, gamma vs alpha-beta |
| ICEM | Information Content Emotion Model | α (>90%) | IC = -log₂(P) → arousal/valence/defense cascade |
| PWUP | Precision-Weighted Uncertainty Processing | β (70-90%) | Precision weights for prediction error attenuation |
| WMED | Working Memory-Entrainment Dissociation | β (70-90%) | WM capacity vs entrainment paradox |
| UDP | Uncertainty-Driven Pleasure | β (70-90%) | Uncertainty × surprise → pleasure (saddle-shaped) |
| CHPI | Cross-Modal Harmonic Predictive Integration | β (70-90%) | Cross-modal (audio+visual) harmonic prediction |
| IGFE | Individual Gamma Frequency Enhancement | γ (50-70%) | Individual gamma frequency for prediction binding |
| MAA | Multifactorial Atonal Appreciation | γ (50-70%) | Schema-free appreciation of atonal music |
| PSH | Prediction Silencing Hypothesis | γ (50-70%) | High-level silenced, low-level persists post-stimulus |

### 1.4 Cross-Function — No Non-PCU Models Claim F2

Scan of all 86 non-PCU model docs found **zero** models with F2 as primary or
secondary function assignment. Several models (PMIM/IMU-β2, OII/IMU-β3, MPFS/STU-γ5,
MTNE/STU-γ3, PCCR/SPU-α3) include prediction-related output dimensions (forecasts,
prediction errors) but these are local computational features, not F2 function
assignments.

---

## 2. Implementation Summary

```
Implemented:     3 models (HTP, SPH, ICEM), 15 beliefs
Pending:         7 models (PWUP, WMED, UDP, CHPI, IGFE, MAA, PSH)
Cross-function:  0 models

Current code:    39D mechanism output (12 + 14 + 13)
                 15 beliefs (4C + 6A + 5N... see §3)
                 57 H3 demands (implemented models)

Full F2 total:   110D mechanism output (all 10 models)
                 173 H3 demands (all 10 models)
```

---

## 3. Belief Inventory (as implemented)

| # | Belief | Cat | τ | Owner | Source Layer | Status |
|---|--------|-----|---|-------|-------------|--------|
| 1 | prediction_hierarchy | C | 0.35 | HTP | E0:high_level_lead + E2:low_level_lead | done |
| 2 | prediction_accuracy | C | 0.40 | HTP | P0:sensory_match | done |
| 3 | sequence_match | C | 0.45 | SPH | P0:memory_match + E0:gamma_match | done |
| 4 | information_content | C | 0.30 | ICEM | E0:information_content | done |
| 5 | hierarchy_coherence | A | — | HTP | E3:hierarchy_gradient | done |
| 6 | error_propagation | A | — | SPH | P1:prediction_error | done |
| 7 | oscillatory_signature | A | — | SPH | M2:gamma_power + M3:alpha_beta_power | done |
| 8 | arousal_scaling | A | — | ICEM | E1:arousal_response | done |
| 9 | valence_inversion | A | — | ICEM | E2:valence_response | done |
| 10 | defense_cascade | A | — | ICEM | E3:defense_cascade | done |
| 11 | abstract_future | N | — | HTP | F0:abstract_future_500ms | done |
| 12 | midlevel_future | N | — | HTP | F1:midlevel_future_200ms | done |
| 13 | sequence_completion | N | — | SPH | F1:sequence_completion_2s | done |
| 14 | arousal_change_pred | N | — | ICEM | F0:arousal_change_1_3s | done |
| 15 | valence_shift_pred | N | — | ICEM | F1:valence_shift_2_5s | done |

**Distribution**: 4 Core + 6 Appraisal + 5 Anticipation = 15 total.
Additional beliefs will be defined when β/γ models are implemented.

---

## 4. Depth-Ordered Pipeline

```
R³ (97D) ───┬────────────────────────────────────────────
H³ tuples ──┤
            ▼
Depth 0:  HTP   (12D, relay, PCU)  ← hierarchical temporal prediction
          SPH   (14D, relay, PCU)  ← spatiotemporal prediction hierarchy
          ICEM  (13D, relay, PCU)  ← information content emotion model
            │
            ▼
Depth 1:  PWUP  (10D, PCU)        ← precision-weighted uncertainty (reads HTP+SPH)
          WMED  (11D, PCU)        ← working memory-entrainment dissociation
          UDP   (10D, PCU)        ← uncertainty-driven pleasure (reads ICEM)
          CHPI  (11D, PCU)        ← cross-modal harmonic prediction
            │
            ▼
Depth 2:  IGFE  (9D, PCU)         ← individual gamma frequency enhancement
          MAA   (10D, PCU)        ← multifactorial atonal appreciation
          PSH   (10D, PCU)        ← prediction silencing (reads HTP+PWUP+UDP)
```

**Depth assignment rationale**:
- **Depth 0 (α)**: Read R³/H³ directly. No upstream mechanism dependencies.
- **Depth 1 (β)**: Cross-unit pathway docs show PWUP reads HTP PE signal,
  UDP reads ICEM IC signal, CHPI reads harmonic context.
- **Depth 2 (γ)**: PSH doc shows it reads HTP, PWUP, UDP, WMED, MAA outputs.
  IGFE and MAA have lower evidence and build on established predictions.

---

## 5. Code Dimensions vs Doc Dimensions

All 3 implemented F2 models have **exact dimension match** between doc and code:

| Model | Doc | Code | Match |
|-------|-----|------|-------|
| HTP | 12D | 12D | exact |
| SPH | 14D | 14D | exact |
| ICEM | 13D | 13D | exact |

No discrepancies. This is expected because F2 models were implemented after the
R³ ontology freeze, so no legacy dimension drift.

---

## 6. H3 Demands (all models)

| Model | H3 Tuples (v1) | Law | Status |
|-------|----------------|-----|--------|
| HTP | 18 | L0 + L2 | implemented |
| SPH | 21 | L0 + L2 | implemented |
| ICEM | 18 | L0 + L2 | implemented |
| PWUP | 14 | L0 + L2 | doc only |
| WMED | 16 | L0 + L2 | doc only |
| UDP | 16 | L0 | doc only |
| CHPI | 20 | L0 + L2 | doc only |
| IGFE | 18 | L0 + L2 | doc only |
| MAA | 14 | L0 | doc only |
| PSH | 18 | L0 + L2 | doc only |

Total H3 demands from all F2 models: **173 tuples**.
Implemented: **57 tuples** (from HTP+SPH+ICEM).

---

## 7. Next Steps

- [x] Implement HTP mechanism (PCU-α1, 12D, 18 H3) — done
- [x] Implement SPH mechanism (PCU-α2, 14D, 21 H3) — done
- [x] Implement ICEM mechanism (PCU-α3, 13D, 18 H3) — done
- [ ] Implement PWUP mechanism (PCU-β1, 10D, 14 H3)
- [ ] Implement WMED mechanism (PCU-β2, 11D, 16 H3)
- [ ] Implement UDP mechanism (PCU-β3, 10D, 16 H3)
- [ ] Implement CHPI mechanism (PCU-β4, 11D, 20 H3)
- [ ] Implement IGFE mechanism (PCU-γ1, 9D, 18 H3)
- [ ] Implement MAA mechanism (PCU-γ2, 10D, 14 H3)
- [ ] Implement PSH mechanism (PCU-γ3, 10D, 18 H3)
- [ ] Define beliefs for β/γ models during implementation
