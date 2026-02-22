# C³ Belief Architecture — RFC v2.0.0

**Date**: 2026-02-21
**Status**: ACTIVE — Function-based architecture
**Author**: Architect + Claude (AI)
**Supersedes**: RFC v1.0.0 (2026-02-16, 5-belief unit-owned architecture)
**Prerequisite reads**:
- `Building/Ontology/C3-ONTOLOGY-BOUNDARY.md` (v2.0.0)
- `Building/C³-Brain/Functions/96-model-functional-brain-map.md` (12 functional categories)
- `Building/C³/C3-BELIEF-ARCHITECTURE-DISCUSSION.md` (design rationale)
- `Building/C³/MODEL-ATLAS.md` (96/96 empirical foundation)
- `Building/Ontology/C3-FAILURE-MODES.md` (12 failure modes)

---

## 0. Purpose

This RFC formalizes the **Function-based belief architecture** for C³ v2.0. It supersedes
RFC v1.0.0 (5-belief unit-owned architecture of 2026-02-16).

**What changes (v1.0 → v2.0)**:
- **5 Core Beliefs → 9 Functions × multiple beliefs**: Each Function owns multiple beliefs.
  The old 1:1 unit→belief mapping is replaced by a richer Function→belief hierarchy.
- **Units → Functions as runtime structure**: The 9 units (SPU, STU, ...) become metadata
  (anatomical origin). The 12 functional categories (F1–F12) become the runtime execution
  containers.
- **Phase scheduler**: 5 phases (0→1→2a→2b→3) → 6 phases (0→1→2→3→4→5) over 9 Functions.
- **3 Meta-Layers (F10–F12)**: Clinical, Development, Cross-Modal provide evidence but
  own no beliefs.

**What does NOT change**: Axis A (role hierarchy R→E→A→I→H), Axis C (4 neurochemicals),
scope system, contract tests, freeze policy, Bayesian predict→observe→update cycle,
BrainOutput structure, Feature Registry — all remain as specified.

---

## 1. Identity Statement

C³ v2.0 is a **Function-centered distributed predictive coding** system with:
- 9 cognitive Functions, each owning multiple beliefs
- 3 Meta-Layers providing evidence without owning beliefs
- H³-informed linear forward models (one per belief)
- Typed precision-weighted prediction errors (one per predictive belief)
- Inverted-U salience-gated reward (F6 terminal aggregator)
- DAG-ordered Function-phase scheduler (single-pass, no iteration)
- Fixed configuration (no learning in v2.0)

---

## 2. The 9 Functions

Each Function is a coherent cognitive subsystem that groups models by **brain function**
(not by anatomical origin). A Function owns one or more beliefs and contains a set of
contributing models drawn from multiple units.

### 2.1 Function Registry

| # | Function | Models | Phase | Primary Relay | Description |
|---|----------|:------:|:-----:|---------------|-------------|
| F1 | Sensory Processing | 14 | 0 | BCH | Acoustic feature extraction: pitch, timbre, consonance |
| F2 | Pattern Recognition & Prediction | 18 | 1 | HTP | Expectation, prediction error, information content |
| F3 | Attention & Salience | 14 | 1 | SNEM | Resource allocation, filtering, selective focus |
| F4 | Memory Systems | 12 | 2 | MEAMN | Encoding, consolidation, retrieval |
| F5 | Emotion & Valence | 11 | 2 | SRP | Emotion generation, affective coloring, mood |
| F6 | Reward & Motivation | 16 | 5 | DAED | Dopamine, pleasure, wanting, preference |
| F7 | Motor & Timing | 21 | 0 | PEOM | Entrainment, synchronization, groove, tempo |
| F8 | Learning & Plasticity | 14 | 3 | — | Experience-dependent change, neural efficiency |
| F9 | Social Cognition | 4 | 3 | — | Group coordination, social reward |

### 2.2 Beliefs Per Function — 3 Categories (v3.0)

Beliefs are **cognitive inferences**, NOT signal features. R³/H³ produce signal features
(roughness, periodicity). Beliefs are what the brain INFERS from those features.

Beliefs in 3 categories:

> **NOTE**: Counts below are **design estimates**. Authoritative belief/mechanism
> counts are determined during model integration. See per-function `collections.md`
> and `Docs/C³/Models/` for the implemented truth.

| Category | Symbol | Bayesian Cycle | PE | Description |
|----------|--------|:--------------:|:--:|-------------|
| **Core** | C | Full (predict→observe→update) | Yes | Primary cognitive states with τ-controlled inertia |
| **Appraisal** | A | Observe-only (no predict) | No | Evaluative judgments from mechanisms |
| **Anticipation** | N | Prediction outputs | No | Forward predictions; feed Core predict() |

**Per-Function Summary (estimates — verified during integration):**

| Function | Core | Appraisal | Anticipation | Est. Total | τ range (Core) |
|----------|:----:|:---------:|:------------:|:----------:|:--------------:|
| **F1 Sensory** | ~5 | ~7 | ~5 | ~17 | 0.3–0.5 |
| **F2 Prediction** | ~4 | ~6 | ~5 | ~15 | 0.35–0.5 |
| **F3 Attention** | ~4 | ~7 | ~4 | ~15 | 0.25–0.4 |
| **F4 Memory** | ~4 | ~7 | ~2 | ~13 | 0.7–0.85 |
| **F5 Emotion** | ~4 | ~8 | ~2 | ~14 | 0.5–0.65 |
| **F6 Reward** | ~5 | ~7 | ~4 | ~16 | 0.5–0.7 |
| **F7 Motor** | ~4 | ~9 | ~4 | ~17 | 0.55–0.7 |
| **F8 Learning** | ~4 | ~8 | ~2 | ~14 | 0.88–0.95 |
| **F9 Social** | ~2 | ~6 | ~2 | ~10 | 0.6–0.65 |

**Example (F6 Reward)**:
- Core: `wanting`(τ=0.6), `liking`(τ=0.65), `pleasure`(τ=0.7), `prediction_error`(τ=0.5), `tension`(τ=0.55)
- Appraisal: `prediction_match`, `peak_detection`, `harmonic_tension`, `dissociation_index`, `temporal_phase`, `da_caudate`, `da_nacc`
- Anticipation: `wanting_ramp`, `chills_proximity`, `resolution_expectation`, `reward_forecast`

> Full belief inventory: see BELIEF-CYCLE.md §Belief Inventory
> Counts are provisional — verified during model integration.

**Naming convention**: `function.belief_name` (e.g., `F1.harmonic_stability`, `F7.period_entrainment`)

**Single-Writer Invariant**: Each belief has exactly ONE Function owner. Models within
the Function provide evidence; models in other Functions may contribute cross-function
evidence but never write the belief.

### 2.3 Why 9 Functions (Not 5 Beliefs, Not 12 Categories)

**From 5 beliefs to 9 Functions**: The functional brain map (96-model analysis) revealed
that the 9 units cross-pollinate heavily across functions. For example:
- IMU (15 models) touches 9 different functional categories — it cannot be reduced to
  "familiarity" alone
- STU (14 models) contributes to 7 categories — motor (10), prediction (2), attention (3),
  sensory (3), memory (2), learning (4), social (1)
- RPU (10 models) spans reward (9) AND prediction (4) — a pure "evidence→ARU" role is
  too narrow

**From 12 categories to 9+3**: F10 Clinical, F11 Development, F12 Cross-Modal are
meta-layers that modulate rather than produce real-time beliefs. They provide evidence
to core Functions but do not have their own predict→observe→update cycle.

**What was excluded and why**:
- `prediction_error` — Still NOT a belief. PE remains a transient derivative signal.
- Central `expectation_state` — Still NOT needed. Each belief has its own predict().
- PCU as a separate entity — Absorbed into F2 (Prediction). Precision estimation is
  a prediction function, not a standalone service.

### 2.4 Precision Engine — Distributed Across Functions

In v1.0, PCU was a standalone precision engine. In v2.0, precision estimation is
**distributed**: each Function computes precision for its own beliefs.

F2 (Prediction) provides the cross-function precision infrastructure:
- PE history ring buffers (per-belief, per-horizon)
- Stability/consistency estimation
- HTP hierarchical boost (sensory_match, pitch_prediction, abstract_prediction)

Each Function's beliefs define their own `precision_obs` formula (see §3.1).

### 2.5 Units as Metadata

The 9 units (SPU, STU, IMU, ASU, NDU, MPU, PCU, ARU, RPU) are preserved as **metadata**
on each model. They indicate anatomical origin and the published neuroscience source.
They no longer determine:
- Runtime execution order (Functions do)
- Belief ownership (Functions do)
- Phase scheduling (Functions do)
- Cross-model pathways (cross-function routes do)

**Example**: Model `SPU-β1-STAI` has `unit: SPU` (metadata) but `function: F5` (Emotion)
as its primary runtime container, with `secondary: [F6]` (Reward).

### 2.6 Meta-Layers (F10–F12)

Three functional categories do NOT produce runtime beliefs. They provide evidence and
modulation to core Functions.

| Meta-Layer | Models | Evidence targets | Role |
|------------|:------:|-----------------|------|
| F10 Clinical & Therapeutic | 10 | F4, F5, F6, F7 | Rehabilitation, therapy, anhedonia modeling |
| F11 Development & Evolution | 6 | F4, F8 | Critical periods, early childhood, phylogeny |
| F12 Cross-Modal Integration | 5 | F2, F3, F7 | Cross-sensory shared codes, multimodal binding |

**Why no beliefs**: These models describe modulation, clinical deviation, or developmental
change that operates on a different timescale (sessions, years) than the frame-by-frame
belief cycle. They contribute evidence to core Function beliefs.

---

## 3. Meta-Signals (Transient, Not Stored)

Meta-signals are computed per frame and consumed immediately. They are NOT beliefs —
they have no owner, no τ, no predict()/update() cycle.

| Signal | Formula | Per-belief? | Consumer |
|--------|---------|-------------|----------|
| `PE_i` | `observed_i − predicted_i` | Yes (all predictive beliefs) | F2, F6 |
| `precision_obs_i` | Belief-specific (see §3.1) | Yes | Update equation |
| `precision_pred_i` | `estimate(stability_i, τ_i, PE_history_i)` | Yes | Update equation |
| `gain_i` | `π_obs_i / (π_obs_i + π_pred_i)` | Yes | Update equation |

**Note**: F6 `reward_valence` does not have its own PE. It is the TERMINAL belief —
it aggregates PEs from all other Function beliefs.

### 3.1 Per-Belief Sensory Confidence (precision_obs)

Each belief defines its own observation reliability. Representative examples:

| Function | Belief | `precision_obs` formula | Rationale |
|----------|--------|------------------------|-----------|
| F1 | consonance | `spectral_SNR × salience / (H³_std + ε)` | Consonance unreliable in noise |
| F1 | pitch_salience | `harmonic_ratio × energy / (H³_std + ε)` | Pitch clarity depends on harmonicity |
| F7 | tempo_state | `onset_regularity × salience / (H³_std + ε)` | Beat clarity from onset sharpness |
| F7 | groove_phase | `syncopation × beat_strength / (H³_std + ε)` | Groove needs clear rhythmic structure |
| F3 | salience_state | `energy_contrast × onset_strength / (H³_std + ε)` | Salience unreliable at low energy |
| F4 | familiarity_state | `ultra_horizon_consistency / (H³_std + ε)` | Familiarity unreliable in brief excerpts |
| F5 | affect_valence | `mode_clarity × consonance / (H³_std + ε)` | Valence needs clear tonal context |
| F2 | prediction_state | `context_stability × regularity / (H³_std + ε)` | Prediction needs stable context |
| F8 | plasticity_state | `exposure_duration × consistency / (H³_std + ε)` | Plasticity needs sustained exposure |

---

## 4. Belief Lifecycle: predict → observe → update

The core computational cycle is UNCHANGED from v1.0. Every belief in every Function
implements three methods.

### 4.1 predict() — H³-Informed Linear Forward Model

```
predicted_i = τ_i × value_prev_i + (1 − τ_i) × baseline_i
            + w_trend_i  × H³_M18(r3_idx_i, horizon_i, L0)
            + w_period_i × H³_M14(r3_idx_i, horizon_i, L0)
            + w_ctx_i    × Σ(context_weights × beliefs_{t-1})
```

**Properties**:
- Reads `beliefs_{t-1}` (previous frame) — no intra-frame dependency
- Uses H³ L0 (backward/memory) only — causal in online mode
- All coefficients (τ, w_trend, w_period, w_ctx, context_weights) are YAML constants
- Context weights can reference beliefs from ANY Function (cross-function context)

**Double Counting Rule**: Maximum 1 first-order morph (M18=trend OR M8=velocity, not both)
+ maximum 1 second-order morph (M14=periodicity OR M3=std, not both) per belief.
Prevents linear instability from correlated morphologies.

### 4.2 Per-Function H³ Demand Mapping

| Function | Belief | Trend morph | Period morph | Context | Horizon band |
|----------|--------|-------------|--------------|---------|--------------|
| F1 | consonance | h3[(0, H8, M18, L0)] roughness trend | h3[(14, H12, M14, L0)] tonalness periodicity | F7.tempo_{t-1} × 0.1 | meso (H6–H12) |
| F1 | pitch_salience | h3[(39, H8, M18, L0)] pitch trend | h3[(39, H10, M14, L0)] pitch periodicity | F1.consonance_{t-1} × 0.1 | meso (H6–H12) |
| F7 | tempo_state | h3[(10, H6, M18, L0)] onset trend | h3[(10, H6, M14, L0)] beat regularity | F1.consonance_{t-1} × 0.05 | meso (H6–H12) |
| F7 | groove_phase | h3[(47, H6, M18, L0)] groove trend | h3[(42, H8, M14, L0)] beat periodicity | F7.tempo_{t-1} × 0.15 | meso (H6–H10) |
| F3 | salience_state | h3[(7, H6, M18, L0)] amplitude trend | — (salience is aperiodic) | F1.consonance×0.2 + F7.tempo×0.2 | meso (H6–H8) |
| F4 | familiarity_state | h3[(14, H24, M18, L0)] tonalness macro | — | F1.consonance_{t-1} × 0.1 | ultra (H24–H28) |
| F2 | prediction_state | h3[(21, H8, M18, L0)] flux trend | h3[(51, H10, M14, L0)] key periodicity | F3.salience_{t-1} × 0.1 | meso (H6–H12) |
| F5 | affect_valence | h3[(0, H10, M18, L0)] consonance trend | — | F1.consonance×0.15 + F4.familiarity×0.1 | meso (H8–H16) |
| F6 | reward_valence | Does not predict — aggregates PEs | — | — | — |
| F8 | plasticity_state | h3[(14, H24, M18, L0)] stability trend | — | F4.familiarity_{t-1} × 0.1 | ultra (H21–H28) |
| F9 | social_synchrony | h3[(42, H10, M18, L0)] beat trend | — | F7.entrainment_{t-1} × 0.2 | meso (H8–H13) |

### 4.3 observe() — Deterministic Extraction

```python
def observe(self, r3, h3, relay_outputs) -> Likelihood:
    """Extract current observation from sensory input."""
    raw = f(r3, h3, relay_outputs)  # deterministic function
    precision = self.compute_precision_obs(r3, h3)  # belief-specific
    return Likelihood(value=raw, precision=precision)
```

**Information separation**: observe() uses the FULL horizon range of H³.
predict() uses only LOW horizons (H6–H12) for predictive beliefs.
This prevents PE from being trivially small.

### 4.4 update() — Bayesian Precision-Weighted Fusion

```python
def update(self, likelihood, predicted, precision_pred):
    gain = likelihood.precision / (likelihood.precision + precision_pred)
    posterior = (1 - gain) * predicted + gain * likelihood.value
    return posterior
```

**Properties**:
- When `precision_obs >> precision_pred`: gain→1, posterior≈observed (sensory dominance)
- When `precision_pred >> precision_obs`: gain→0, posterior≈predicted (prior dominance)
- This is Bayesian inference, NOT learning. All precision parameters are fixed.

---

## 5. Phase Scheduler

Single-pass, DAG-ordered, concurrent within phase. 9 Functions execute in 6 phases.

```
Phase 0  (sensory + motor grounding — no dependencies)
  ├── F1 Sensory: predict + observe → consonance, pitch_salience, timbre   ─┐
  └── F7 Motor: predict + observe → tempo, groove, entrainment            ─┘ concurrent
  → Update all Phase 0 beliefs (Bayesian fusion)

Phase 1  (pattern + attention — reads Phase 0)
  ├── F2 Prediction: predict + observe → prediction_state, expectation     ─┐
  └── F3 Attention: predict + observe → salience, attention_allocation     ─┘ concurrent
  → Update all Phase 1 beliefs

Phase 2  (memory + emotion — reads Phase 0+1)
  ├── F4 Memory: predict + observe → familiarity, memory_scaffold          ─┐
  └── F5 Emotion: predict + observe → affect_valence, emotional_arousal    ─┘ concurrent
  → Update all Phase 2 beliefs

Phase 3  (higher cognition — reads Phase 0+1+2)
  ├── F8 Learning: predict + observe → plasticity_state, expertise         ─┐
  └── F9 Social: predict + observe → social_synchrony                      ─┘ concurrent
  → Update all Phase 3 beliefs

Phase 4  (PE + precision — meta-computation)
  ├── PE_i = observed_i − predicted_i     (for all predictive beliefs)
  ├── precision_pred_i = estimate(stability_i, τ_i, PE_history_i)
  └── gain_i = π_obs_i / (π_obs_i + π_pred_i)

Phase 5  (reward — terminal aggregator)
  └── F6 Reward: aggregate PEs + hedonic + dopamine → reward_valence, pleasure, wanting

Meta-Layers: F10/F11/F12 contribute evidence during Phases 0–3
             (no beliefs, no dedicated phase — evidence providers only)

RAM: assemble after Phase 5
Output: BrainOutput(tensor, ram, neuro, psi)
```

**Properties**:
- Single-pass per frame (no iteration, no convergence loop)
- predict() reads `beliefs_{t-1}` — all previous-frame values, no intra-phase dependency
- Multi-timescale via τ (Murray hierarchy), not scheduler rate
- Hall of mirrors prevention: Phase 0 always re-computes sensory and motor beliefs from R³/H³
- F6 Reward is terminal: it reads PEs from all Functions but no Function reads reward
  within the same frame (reward_{t-1} feeds back at next frame via predict() context weights)

### 5.1 Phase Dependency DAG

```
F1 Sensory ──┬──→ F2 Prediction ──┬──→ F4 Memory ──┬──→ F8 Learning ──┐
             │                    │                │                  │
F7 Motor ───┘──→ F3 Attention ──┘──→ F5 Emotion ──┘──→ F9 Social ───┤
                                                                      │
                                    PE + Precision ◄─── all beliefs ──┤
                                                                      │
                                    F6 Reward ◄─── PE + hedonic ──────┘
```

---

## 6. Reward Function — Inverted-U Salience-Gated

```python
def compute_reward(all_PEs, all_precisions, salience, familiarity):
    # Per-belief reward components (across all predictive Functions)
    for belief_i in all_predictive_beliefs:
        surprise_i    = |PE_i| × π_eff_i × (1 − familiarity)
        resolution_i  = (1 − |PE_i|) × π_eff_i × familiarity
        exploration_i = |PE_i| × (1 − π_eff_i)
        monotony_i    = π_eff_i²

        reward_i = salience × (w1×surprise_i + w2×resolution_i
                                + w3×exploration_i − w4×monotony_i)

    # Aggregate
    reward_valence = Σ reward_i × familiarity_mod × emotional_mod × da_gain
```

**v3.0 change**: Reward now aggregates PEs from ALL 36 Core Beliefs across 8 Functions
(F1–F5, F7–F9). Appraisal/Anticipation beliefs do NOT produce PE — they are direct mechanism
outputs. The formula is identical; the summation scope is over Core Beliefs only.

**Weights**: w_s=1.5, w_r=0.8, w_e=0.5, w_m=0.6 (same as v1.0 rebalanced)

**Modulations** (unchanged):
- Familiarity mod: `0.5 + 0.5 × 4 × fam × (1 − fam)` (inverted-U, peak at 0.5)
- SRP hedonic: F6-internal blend of wanting/liking/pleasure/tension
- MEAMN emotional: F5 emotional modulation `0.85 + 0.15 × emo_response`
- DAED dopamine: F6-internal DA gain `1 + 0.25 × da_signal`

---

## 7. Function → Model Mapping

How models are distributed across Functions. Each model has a PRIMARY Function (runtime
container) and optional SECONDARY Functions (evidence contributions).

### 7.1 Primary Function Assignments

| Function | Primary Models (by unit origin) |
|----------|--------------------------------|
| **F1 Sensory** (14) | SPU: BCH, PSCL, PCCR, SDNPS, SDED. IMU: PNH, TPRD. NDU: MPG. ASU: CSG. SPU: MIAA. STU: MDNS, TPIO. IMU: MSPBA. RPU: LDAC |
| **F2 Prediction** (18) | PCU: HTP, SPH, ICEM, PWUP, PSH, UDP, CHPI, WMED. RPU: RPEM, IUCP, SSPS. ARU: PUPF. IMU: PMIM. ASU: PWSM. NDU: SDD, CDMR, SLEE. STU: HMCE |
| **F3 Attention** (14) | ASU: SNEM, IACM, CSG, BARM, STANM, AACM, PWSM, DGTP, SDL. STU: AMSS, ETAM, NEWMD. NDU: SDD. PCU: IGFE |
| **F4 Memory** (12) | IMU: MEAMN, MMP, HCMC, DMMS, CDEM, PMIM, CSSL. STU: HMCE, TMRM. RPU: MEAMR. ARU: NEMAC. PCU: SPH |
| **F5 Emotion** (11) | ARU: VMM, AAC, CLAM, NEMAC, CMAT, TAR. PCU: ICEM, MAA. IMU: MEAMN, CDEM. SPU: STAI |
| **F6 Reward** (16) | ARU: SRP, PUPF, MAD. RPU: DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, SSRI, LDAC, IOTMS, SSPS. PCU: UDP. SPU: STAI. ASU: AACM |
| **F7 Motor** (21) | MPU: PEOM, MSR, GSSM, ASAP, DDSMI, VRMSME, SPMC, CTBB, STC. STU: AMSC, EDTA, ETAM, HGSIC, OMS, TMRM, NEWMD, MPFS. ASU: SNEM, BARM. RPU: MCCN. PCU: WMED |
| **F8 Learning** (14) | SPU: TSCP, ESME. NDU: EDNR, CDMR, SLEE, ECT. STU: EDTA, MTNE, PTGMP, MPFS. MPU: MSR, STC. IMU: OII. PCU: MAA |
| **F9 Social** (4) | RPU: SSRI. MPU: DDSMI, NSCP. STU: OMS |

> **Note**: Some models appear in multiple Functions' primary lists because they have dual
> primary membership (e.g., ASU-CSG is primary in both F1 and F3). The cross-intersection
> matrix in `96-model-functional-brain-map.md` details all assignments.

### 7.2 Function Relay Structure

Each Function has a primary relay model that provides the main observation signal.
Not all Functions have their own relay — some share or compose from existing relays.

| Function | Primary Relay | Observe Source | Evidence Contributors |
|----------|---------------|----------------|----------------------|
| F1 Sensory | BCH (SPU) | R³ consonance/pitch/timbre | PSCL, PCCR, PNH, SDED, SDNPS |
| F2 Prediction | HTP (PCU) | H³ prediction signals | SPH, PWUP, IUCP, SSPS |
| F3 Attention | SNEM (ASU) | R³ onset/energy + H³ velocity | IACM, CSG, BARM, STANM |
| F4 Memory | MEAMN (IMU) | H³ periodicity/stability | HCMC, PMIM, MMP, CDEM |
| F5 Emotion | SRP (ARU) — partial | R³ mode + relay outputs | VMM, AAC, ICEM |
| F6 Reward | DAED (RPU) + SRP (ARU) | PE aggregation + hedonic | MORMR, RPEM, MCCN |
| F7 Motor | PEOM (MPU) | R³ beat/onset + H³ tempo | AMSC, ETAM, ASAP, SPMC |
| F8 Learning | — (no relay) | H³ macro stability | EDNR, SLEE, MSR, MTNE |
| F9 Social | — (no relay) | Cross-model synchrony | SSRI, DDSMI, OMS |

---

## 8. Configuration — YAML Schema

All parameters are externalized. No hardcoded values in compute().
The config is organized by Function, not by individual belief.

```yaml
c3_functions:
  F1_sensory:
    models: [BCH, PSCL, PCCR, SDNPS, SDED, PNH, TPRD, MPG, CSG, MIAA, MDNS, TPIO, MSPBA, LDAC]
    primary_relay: BCH
    beliefs:
      consonance:
        tau: 0.3
        baseline: 0.5
        predict:
          w_trend: 0.15
          w_period: 0.10
          w_ctx: { F7.tempo_state: 0.10 }
          h3_trend: [0, 8, 18, 0]
          h3_period: [14, 12, 14, 0]
        observe:
          r3_groups: [A, C, F]
          h3_horizons: [0, 18]
        precision_obs:
          formula: "spectral_SNR * salience / (h3_std + eps)"
      pitch_salience:
        tau: 0.4
        baseline: 0.5
        predict:
          w_trend: 0.12
          w_period: 0.10
          w_ctx: { F1.consonance: 0.10 }
          h3_trend: [39, 8, 18, 0]
          h3_period: [39, 10, 14, 0]
        observe:
          r3_groups: [A, F]
          h3_horizons: [0, 12]
        precision_obs:
          formula: "harmonic_ratio * energy / (h3_std + eps)"
      timbre_quality:
        tau: 0.5
        baseline: 0.5
        predict:
          w_trend: 0.10
          w_period: null
          w_ctx: { F1.consonance: 0.05 }
          h3_trend: [12, 10, 18, 0]
        observe:
          r3_groups: [C, J]
          h3_horizons: [0, 12]
        precision_obs:
          formula: "spectral_flatness * energy / (h3_std + eps)"

  F7_motor:
    models: [PEOM, MSR, GSSM, ASAP, DDSMI, VRMSME, SPMC, CTBB, STC, AMSC, EDTA, ETAM, HGSIC, OMS, TMRM, NEWMD, MPFS, SNEM, BARM, MCCN, WMED]
    primary_relay: PEOM
    beliefs:
      tempo_state:
        tau: 0.7
        baseline: 0.5
        predict:
          w_trend: 0.20
          w_period: 0.25
          w_ctx: { F1.consonance: 0.05 }
          h3_trend: [10, 6, 18, 0]
          h3_period: [10, 6, 14, 0]
        observe:
          r3_groups: [B, D, G]
          h3_horizons: [0, 12]
        precision_obs:
          formula: "onset_regularity * salience / (h3_std + eps)"
      groove_phase:
        tau: 0.6
        baseline: 0.5
        predict:
          w_trend: 0.15
          w_period: 0.20
          w_ctx: { F7.tempo_state: 0.15 }
          h3_trend: [47, 6, 18, 0]
          h3_period: [42, 8, 14, 0]
        observe:
          r3_groups: [G]
          h3_horizons: [0, 10]
        precision_obs:
          formula: "syncopation * beat_strength / (h3_std + eps)"
      entrainment_strength:
        tau: 0.5
        baseline: 0.5
        predict:
          w_trend: 0.10
          w_period: null
          w_ctx: { F7.tempo_state: 0.20 }
          h3_trend: [42, 8, 18, 0]
        observe:
          r3_groups: [B, G]
          h3_horizons: [0, 10]
        precision_obs:
          formula: "beat_clarity * onset_strength / (h3_std + eps)"

  # ... (F2–F6, F8, F9 follow same pattern)

  F6_reward:
    models: [SRP, DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, SSRI, LDAC, IOTMS, SSPS, PUPF, UDP, STAI, AACM, MAD]
    primary_relay: DAED
    beliefs:
      reward_valence:
        tau: 0.8
        baseline: 0.0
        # reward does not predict — it aggregates PEs from all Functions
        reward:
          w_surprise: 1.5
          w_resolution: 0.8
          w_exploration: 0.5
          w_monotony: 0.6
      pleasure_state:
        tau: 0.7
        baseline: 0.0
        # SRP hedonic pathway
      wanting_state:
        tau: 0.6
        baseline: 0.0
        # DAED anticipatory dopamine

c3_precision:
  pe_history_window: 32
  stability_decay: 0.95
  # precision now distributed — each Function belief has its own PE buffer

c3_scheduler:
  phases: [0, 1, 2, 3, 4, 5]
  phase_0: { functions: [F1, F7], label: "sensory + motor grounding" }
  phase_1: { functions: [F2, F3], label: "prediction + attention" }
  phase_2: { functions: [F4, F5], label: "memory + emotion" }
  phase_3: { functions: [F8, F9], label: "learning + social" }
  phase_4: { label: "PE + precision computation" }
  phase_5: { functions: [F6], label: "reward aggregation" }
  meta_layers: [F10, F11, F12]  # contribute evidence, no dedicated phase

c3_meta_layers:
  F10_clinical:
    models: [MMP, RASN, RIRI, VRIAP, GSSM, VRMSME, CLAM, MAD, TAR, DSP]
    evidence_targets: [F4, F5, F6, F7]
  F11_development:
    models: [DAP, DMMS, CSSL, DSP, SDDP, ONI]
    evidence_targets: [F4, F8]
  F12_cross_modal:
    models: [CMAT, CMAPCC, CHPI, DGTP, SDD]
    evidence_targets: [F2, F3, F7]
```

**v2.0 = NO LEARNING**. All values above are constants. Bayesian update is inference
(combining prior with likelihood), not parameter learning.

**Learning roadmap**:
- v2.1: Gradient-free weight tuning (grid search over w_trend, w_period, w_ctx per Function)
- v3.0: Learned prosthetic heads (MI-PLASTICITY), episodic memory, Hebbian pathway weights

---

## 9. Alignment with Existing Ontology

### 9.1 What RFC v2.0 Changes

| Component | v1.0 | v2.0 |
|-----------|------|------|
| Beliefs | 5 (unit-owned) | 131 mechanism-level (36 Core + 65 Appraisal + 30 Anticipation) |
| Runtime containers | 9 units | 9 Functions + 3 Meta-Layers |
| Units | Runtime structure | Metadata (anatomical origin) |
| Phase scheduler | 5 phases (0→1→2a→2b→3) | 6 phases (0→1→2→3→4→5) |
| Precision engine | PCU standalone | Distributed (F2 provides infrastructure) |
| Belief ownership | 1 unit = 1 belief | 1 Function = N beliefs |
| Cross-model routes | 12 unit-to-unit pathways | Cross-function signal routes |
| Config structure | Per-belief YAML | Per-Function YAML |

### 9.2 What v2.0 Does NOT Change

| Component | Status | Why unchanged |
|-----------|--------|---------------|
| Axis A (role hierarchy) | FROZEN | R→E→A→I→H depth ordering still valid within Functions |
| Axis C (4 neurochemicals) | FROZEN | DA/NE/OPI/5HT still modulate via volume transmission |
| Scope system | FROZEN | internal/external/hybrid still governs dim visibility |
| Contract tests | FROZEN | State Declaration, Single-Writer, Causality, Role Consistency |
| BrainOutput structure | FROZEN | tensor + RAM(26) + neuro(4) + Ψ³ unchanged |
| Feature Registry | FROZEN | Name-based R³ addressing unchanged |
| predict→observe→update cycle | FROZEN | Bayesian fusion formulas identical |
| Reward formula | FROZEN | Same inverted-U with extended summation scope |

### 9.3 How v1.0 Beliefs Map to v2.0 Functions

| v1.0 Belief | v1.0 Owner | v2.0 Function | v2.0 Status |
|-------------|-----------|---------------|-------------|
| `perceived_consonance` | SPU | F1 Sensory | → `harmonic_stability` Core Belief |
| `tempo_state` | STU | F7 Motor | → `period_entrainment` Core Belief |
| `salience_state` | ASU | F3 Attention | → `beat_entrainment` Core Belief |
| `familiarity_state` | IMU | F4 Memory | → `autobiographical_retrieval` Core Belief |
| `reward_valence` | ARU | F6 Reward | → `wanting` Core Belief |
| — | PCU (precision) | F2 Prediction | Absorbed; new `prediction_state` belief |
| — | RPU (evidence) | F6 Reward | DAED+RPU models move to F6 |
| — | MPU (evidence) | F7 Motor | PEOM+MPU models move to F7 |
| — | NDU (evidence) | F8 Learning | MPG+NDU models distribute across F1, F2, F8 |

**Backward compatibility**: The 5 original beliefs exist as primary beliefs within their
respective Functions. Existing kernel code (scheduler.py with 5 beliefs) can operate
as a subset of the new architecture — it runs F1.consonance, F7.tempo, F3.salience,
F4.familiarity, F6.reward as the minimum viable belief set.

---

## 10. Relationship to Failure Modes

All 10 original failure modes remain relevant. Two new failure modes added for v2.0:

| FM | How Function architecture addresses it |
|----|----------------------------------------|
| FM-1 (flat collapse) | Function phase scheduler enforces DAG ordering |
| FM-2 (redundant binding) | Binding Service unchanged |
| FM-3 (circular deps) | predict() reads `beliefs_{t-1}` only — no intra-frame cycles |
| FM-4 (multiple writers) | Single-Writer per Function. Each belief has 1 Function owner |
| FM-5 (hidden state) | Belief state in BeliefStore, fully serializable |
| FM-6 (causality) | predict() uses L0 only. observe() uses full H³ |
| FM-7 (neuro race) | Unchanged — weighted average at same depth |
| FM-8 (unbounded memory) | Unchanged — bounded buffer |
| FM-9 (scope leakage) | Unchanged — scope filtering |
| FM-10 (index fragility) | Unchanged — Feature Registry |
| **FM-11 (cross-Function contradiction)** | A model in 3 Functions must not produce contradictory evidence. Prevention: primary Function determines authoritative output |
| **FM-12 (belief explosion)** | Each Function declares a bounded belief list: max 5 Core + 10 Appraisal + 5 Anticipation = 20 per Function. Only Core Beliefs (36 total) carry PE overhead. Prevention: YAML schema validation |

---

## 11. Next Steps

### 11.1 Immediate

1. **Reconcile ontology documents** — update C3-ONTOLOGY-BOUNDARY.md, MODEL-ATLAS.md,
   BELIEF-CYCLE.md, REGION-ACTIVATION-MAP.md, IMPLEMENTATION-TREE.md to reflect v2.0
2. **Define all beliefs** — finalize the per-Function belief list with τ values,
   baselines, horizon bands, and context weights
3. **Cross-function pathway specification** — replace 12 unit-pathways with
   Function-to-Function signal routes

### 11.2 Implementation

4. Update kernel scheduler.py for 6-phase Function execution
5. Extend BeliefStore for multi-belief-per-Function
6. Update YAML config loader for Function-based schema
7. Run existing test suite (alpha-test v3.1) to verify backward compatibility
8. Run Swan Lake end-to-end with expanded belief set

### 11.3 Future versions

- **v2.1**: Gradient-free weight tuning per Function
- **v3.0**: Learned prosthetic heads, episodic memory, Hebbian pathway weights

---

## 12. Open Questions

1. **Belief count finalized**: v3.0 declares 131 mechanism-level beliefs (36 Core + 65 Appraisal
   + 30 Anticipation) across 9 Functions. See BELIEF-CYCLE.md v3.0 for complete inventory.

2. **F8 Learning beliefs**: What does `plasticity_state` observe per-frame? Learning operates
   on session/training timescales, not frame rate. Possible: observe neural efficiency
   markers, expertise indicators. Very high τ (0.95) means almost no frame-to-frame change.

3. **F9 Social beliefs**: Only 4 models. Is this sufficient for a standalone Function?
   Alternative: merge F9 into F7 (Motor) since 3 of 4 social models involve motor synchrony.

4. **Multi-rate within Functions**: Should different beliefs within the same Function
   update at different rates? E.g., F7: tempo at frame rate, groove at beat rate.

5. **Meta-Layer evidence routing**: How do F10–F12 models deliver evidence? Do they
   contribute to specific beliefs in specific Functions, or provide a general modulation?

---

## 13. Version History

| Version | Date | Changes |
|---------|------|---------|
| RFC v1.0.0 | 2026-02-16 | Initial RFC. 5 beliefs + PCU precision engine, unit-owned. |
| RFC v2.0.0 | 2026-02-21 | Function-based architecture. 9 Functions × multiple beliefs. Units → metadata. 6-phase scheduler. 3 Meta-Layers (F10–F12). |
| RFC v3.0.0 | 2026-02-21 | Mechanism-based beliefs. 131 beliefs in 3 categories (Core/Appraisal/Anticipation). Signal features ≠ beliefs. Only 36 Core Beliefs carry PE overhead. |

---

*This RFC defines the Function-centered belief architecture for C³ v2.0. It captures
the evolution from unit-based organization (v1.0) to brain-function-based organization,
as determined by functional analysis of all 96 models. The 9 Functions group models by
what they compute (brain function), not where they sit (anatomical unit). This produces
a richer, more faithful brain model with multiple beliefs per cognitive function.*
