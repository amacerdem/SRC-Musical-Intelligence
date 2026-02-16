# C³ Belief Architecture Discussion

**Date**: 2026-02-16
**Participants**: Architect (human) + Claude (AI)
**Status**: Design decisions finalized, pending formal spec write-up
**Prerequisite**: C3-ONTOLOGY-BOUNDARY.md (v1.0.0), MODEL-ATLAS.md (96/96), C3-FAILURE-MODES.md

---

## Context

After completing the C³ Model Atlas (96/96 models), we conducted a structured architectural discussion to design the C³ belief system. The atlas revealed 5 critical facts that drove the design:

1. **All 96 models are stateless** — state lives in orchestrator, not models
2. **Every unit has a fixed mechanism signature** — mechanism = functional axis, not region
3. **ARU is the global convergence hub** — receives from 6 of 8 other units
4. **IMU is the cross-circuit bridge** — only unit that reads cross-circuit mechanisms
5. **H³ demand is sparse and homogeneous** — avg ~16 tuples, SRP outlier at ~124

These facts led to the conclusion that the current architecture is a "paper-aggregation graph" (literature-driven grouping) rather than a runtime cognitive architecture. The discussion produced a belief-centered redesign.

---

## Decision 1: From Mechanism-Centered to Belief-Centered

**Problem**: 96 models execute as mechanism-bound nodes. No epistemic hierarchy. No belief state. Dataflow is implicit.

**Decision**: Mechanisms become pure function libraries (update rules). Beliefs become the primary architectural entity. Models become belief contributors.

**Rationale**: Atlas shows mechanism signatures are computational style, not cognitive function. The cognitive function is what the mechanism computes FOR — which is a belief.

```
BEFORE: Model → Mechanism → M-layer → Output
AFTER:  Model → Belief.observe/predict/update → PE → Reward → Output
```

---

## Decision 2: Six Core Beliefs

### Initial Proposal (5 beliefs)

| # | Belief | Owner | Rationale |
|---|--------|-------|-----------|
| 1 | consonance | SPU | BCH is first computation, P1 pathway feeds everything |
| 2 | tempo | STU | BEP most used mechanism (31 appearances), motor grounding |
| 3 | salience | ASU | Attention gate, ASU perfect uniformity (BEP+ASA) |
| 4 | prediction_error | PCU | Learning signal, heaviest mechanism (PPC+TPC+MEM) |
| 5 | reward_valence | ARU | Convergence hub, receives from 6 units |

### Architect Corrections

**Correction 1**: `prediction_error` is NOT a belief — it's a transient meta-signal (derivative of belief minus observation). Originally replaced with `expectation_state`, but later revised (see Correction 13).

**Correction 2**: Raw `consonance` is an R³ primitive, not a belief. Renamed to `perceived_consonance` (posterior, confidence-weighted).

**Correction 3**: Added `familiarity_state` (IMU) as belief — IMU is 15 models / 159D, the largest unit, and cannot be ownerless. Familiarity is critical for IUCP (inverted-U complexity preference).

**Correction 13** (final round): `expectation_state` is NOT a separate belief — expectation is each belief's `predict()` method, distributed across all beliefs. PCU owns precision estimation, not a belief. This reduces beliefs from 6 to 5, with PCU as a meta-engine.

**Correction 14**: v1.0 familiarity is **structural familiarity** (pattern stability), NOT autobiographical familiarity (personal memory). A 30s loop heard for the first time will register as "structurally familiar" due to high ultra-horizon smoothness. This is a known v1.0 limitation — true autobiographical familiarity requires episodic memory (v2.0).

**Correction 15**: Horizon separation to prevent over-correlation: expectation (predict) uses LOW horizons (H6–H12), familiarity uses ULTRA horizons (H24–H28). Documented to prevent information overlap.

**Correction 16**: `precision_obs` must be belief-specific, not a generic formula. Each belief defines its own sensory confidence measure:
- consonance: spectral SNR × salience / std
- tempo: onset regularity × salience / std
- salience: energy contrast × onset_strength / std
- familiarity: ultra-horizon consistency / std

**Correction 17**: v1.0 = NO LEARNING. All parameters fixed in YAML config. Bayesian update is inference, not learning. τ, weights, precision rules are constants. v1.1 adds weight tuning, v2.0 adds learned heads.

### Final 5 Beliefs + PCU Precision Engine

| # | Belief | Owner | τ (Murray) | Phase |
|---|--------|-------|------------|-------|
| 1 | perceived_consonance | SPU | 0.3 (fast) | Phase 0 |
| 2 | tempo_state | STU | 0.7 (medium) | Phase 0 |
| 3 | salience_state | ASU | 0.5 (medium-fast) | Phase 1 |
| 4 | familiarity_state | IMU | 0.85 (slow) | Phase 2a |
| 5 | reward_valence | ARU | 0.8 (slow) | Phase 3 |
| — | precision (per-belief) | PCU | — | Phase 2b (meta) |

PCU is NOT a belief owner. PCU is the **precision engine**: estimates `precision_pred_i` for each belief, maintains PE_history, NEVER writes belief values. Expectation is distributed — each belief's `predict()` method.

### Meta-Signals (transient, not beliefs)

- `PE_i` = typed per-belief prediction error (4 typed: consonance, tempo, salience, familiarity)
- `precision_obs_i` = belief-specific sensory confidence (NOT generic formula — per-belief override)
- `precision_pred_i` = prediction confidence per belief (PCU estimates from stability, τ, PE_history)

---

## Decision 3: Belief-Level Prediction (NOT Observation-Level)

**Question**: Does expectation_state predict R³ observations or belief states?

**Decision**: Belief-level. `E[belief_{t+1}]`, not `E[o_t | state]`.

**Rationale**:
- R³ and H³ are FROZEN and deterministic. Predicting them = predicting audio, not cognition.
- Cognitive prediction = "how will my interpretation change", not "what will the spectrum look like"
- This makes C³ genuinely cognitive, not an audio prediction model

**Hall of Mirrors Prevention**: Phase 0 beliefs (consonance, tempo) are re-computed from R³/H³ every frame — sensory anchor is mathematically guaranteed. Beliefs never drift from reality because observation likelihood always enters the Bayesian update.

---

## Decision 4: Per-Belief Forward Models (NOT Centralized PCU)

**Question**: Should PCU be a central prediction engine, or should each belief predict itself?

**Decision**: Per-belief. Each belief owns its own `predict()` method.

**Rationale**:
- Central PCU = god-model, single point of failure, FM-1 (flat collapse) risk
- Per-belief = modular, ablatable, single-writer preserved
- Cross-belief context available via `beliefs_{t-1}` (no dependency — all read previous frame)
- PCU's new role: **precision estimator**, not prediction engine

**PCU Role Redefinition**:
- PCU estimates `precision_pred_i` for each belief
- PCU maintains PE_history per belief
- PCU NEVER writes belief values — only precision/gain parameters
- Atlas validation: PPC (pitch precision), TPC (timbre precision), MEM (precision history)

---

## Decision 5: H³-Informed Linear Prediction

**Question**: What is the predict() implementation? AR(1)? HMM? Neural? Symbolic?

**Decision**: Linear combination of H³ morphologies.

```python
predicted = τ * value_prev + (1-τ) * baseline
          + w_trend * H³_M18(trend)
          + w_period * H³_M14(periodicity)
          + w_ctx * Σ(context_weights × beliefs_{t-1})
```

**Rationale**:
- H³ morphologies (M18=trend, M8=velocity, M14=periodicity, M3=std) ARE prediction features
- H³ is already computed and frozen — zero additional cost
- Linear = glass-box, every coefficient visible
- Atlas validation: model H³ demands already include trend/velocity morphologies

**Architect Correction — Double Counting Rule**: Max 1 first-order morph (trend OR velocity, not both) + max 1 second-order morph (periodicity OR std) per belief. Prevents linear instability from correlated morphologies.

### Per-Belief H³ Mapping

**perceived_consonance** (SPU, τ=0.3):
```
trend:       h3[(0, H8, M18, L0)]    — roughness trend at meso
periodicity: h3[(14, H12, M14, L0)]  — tonalness periodicity at phrase
context:     tempo_{t-1} × 0.1
```

**tempo_state** (STU, τ=0.7):
```
trend:       h3[(10, H6, M18, L0)]   — spectral_flux trend at beat
periodicity: h3[(10, H6, M14, L0)]   — spectral_flux periodicity (beat regularity)
context:     consonance_{t-1} × 0.05
```

**salience_state** (ASU, τ=0.5):
```
trend:       h3[(7, H6, M18, L0)]    — amplitude trend
periodicity: —                        — salience is aperiodic
context:     consonance_{t-1} × 0.2 + tempo_{t-1} × 0.2
```

**expectation_state** (PCU, τ=0.6):
```
Not a traditional predict — PCU estimates precision, not belief values.
precision_pred_i = g(belief_stability_i, τ_i, PE_history_consistency_i)
```

**familiarity_state** (IMU, τ=0.85):
```
trend:       h3[(14, H24, M18, L0)]  — tonalness trend at macro (~60s)
periodicity: —
context:     consonance_{t-1} × 0.1
observe():   h3 ultra-horizon smoothness (H28, M15) as proxy for pattern stability
```

**reward_valence** (ARU, τ=0.8):
```
Does not predict directly — aggregates salience-gated PEs.
reward = Σ(salience_i × (surprise + resolution + exploration − monotony) × familiarity_mod)
```

---

## Decision 6: DAG-Ordered Phase Scheduler

**Question**: Sequential or concurrent belief updates?

**Decision**: DAG determines ordering. Independent beliefs concurrent within phase, dependent beliefs sequential across phases.

```
Phase 0:   [perceived_consonance ∥ tempo_state]     — sensory grounding (concurrent)
Phase 1:   [salience_state]                          — attentional gate
Phase 2a:  [expectation_state ∥ familiarity_state]   — predict + recognize (concurrent)
Phase 2b:  [typed PE + precision computation]        — meta-signals (transient)
Phase 3:   [reward_valence]                          — salience-gated aggregation
```

**Properties**:
- Single-pass per frame (no iteration)
- predict() reads `beliefs_{t-1}` — no intra-phase dependency
- Multi-timescale via τ (Murray hierarchy), not scheduler
- v0.4 may add multi-rate (some beliefs skip frames)

---

## Decision 7: Bayesian Update with Likelihood Form

**Architect Correction**: `observed` should produce a likelihood, not directly write to belief.

```python
def compute_likelihood(self, r3, h3):
    raw = self.observe(r3, h3)  # deterministic
    precision = energy * salience / (H³_std + ε)  # belief-specific sensory confidence
    return Likelihood(value=raw, precision=precision)

def update(self, likelihood, predicted, precision_pred):
    gain = likelihood.precision / (likelihood.precision + precision_pred)
    posterior = (1 - gain) * predicted + gain * likelihood.value
    return posterior
```

**Architect Correction on precision_obs**: Not just `1/std`. Should be:
```
precision_obs = f(energy, SNR, H³_std, salience)
```
Because low variance ≠ high reliability (e.g., low-energy stable signal is unreliable).

---

## Decision 8: Reward Function with Inverted-U

```python
def compute_reward(PE_i, precision_pred_i, salience_i, familiarity):
    surprise = |PE_i| * precision_pred_i * (1 - familiarity)
    resolution = (1 - |PE_i|) * precision_pred_i * familiarity
    exploration = entropy_of_prediction_distribution  # epistemic bonus
    monotony = precision_pred_i ** 2  # too predictable = boring

    reward_i = salience_i * (w1*surprise + w2*resolution + w3*exploration - w4*monotony)
    return reward_i
```

**Atlas validation**: RPU-β1-IUCP (Inverted-U Complexity Preference) directly models this. ARU-β4-NEMAC (nostalgia) validates familiarity-modulated reward.

---

## Decision 9: Unit Role Mapping

| Unit | Owns | Role |
|------|------|------|
| SPU | perceived_consonance | Sensory grounding (pitch/consonance) |
| STU | tempo_state | Sensory grounding (temporal/motor) |
| ASU | salience_state | Attentional gating |
| PCU | precision (per-belief) | Precision estimation, PE history |
| IMU | familiarity_state | Long-term pattern recognition |
| ARU | reward_valence | Convergence hub, value computation |
| RPU | — (evidence → ARU) | Surprise/resolution computation |
| MPU | — (evidence → STU) | Motor evidence for tempo |
| NDU | — (evidence → ASU + PCU) | Deviance detection for salience + precision |

---

## Decision 10: Information Overlap Prevention

**Architect Correction**: predict() and observe() must minimize shared information.

- `predict()`: uses `beliefs_{t-1}` + LOW horizon H³ morphologies
- `observe()`: uses FULL horizon R³/H³ (current frame)

This prevents the scenario where prediction and observation draw from the same H³ window, which would make PE trivially small.

---

## Architectural Corrections Log

| # | Correction | Source | Impact |
|---|-----------|--------|--------|
| 1 | PE is meta-signal, not belief | Architect | expectation_state replaces prediction_error |
| 2 | consonance → perceived_consonance | Architect | Belief is posterior, not R³ primitive |
| 3 | reward reads salience-gated PEs, not raw beliefs | Architect | Preserves gating ontology |
| 4 | Phase 2a/2b separation | Architect | PE computation is distinct sub-phase |
| 5 | Single-pass scheduler ⊥ multi-timescale dynamics | Architect | τ is internal to belief, not scheduler |
| 6 | Per-belief forward model, not central PCU | Architect | PCU = precision estimator |
| 7 | Max 1 first-order + 1 second-order H³ morph per belief | Architect | Prevents double counting |
| 8 | precision_obs = f(energy, SNR, std, salience) | Architect | Low variance ≠ high reliability |
| 9 | predict/observe information overlap minimization | Architect | Low horizon for predict, full for observe |
| 10 | precision_pred = g(stability, τ, PE_history) | Architect | Not just PE magnitude |
| 11 | exploration = entropy of prediction distribution | Architect | Not directly PE-based |
| 12 | familiarity_state added as 6th belief (IMU) | Joint decision | IMU too large to be ownerless |

---

## C³ v1.0 Final Specification Summary

```
IDENTITY:
  Distributed belief-level predictive coding with typed precision-weighted
  prediction errors, H³-informed linear forward models, and inverted-U
  salience-gated reward.

BELIEFS (5):
  perceived_consonance  (SPU, τ=0.3, fast)
  tempo_state           (STU, τ=0.7, medium)
  salience_state        (ASU, τ=0.5, medium-fast)
  familiarity_state     (IMU, τ=0.85, slow)         — H³ ultra-horizon proxy in v1.0
  reward_valence        (ARU, τ=0.8, slow)

PCU PRECISION ENGINE (not a belief, τ=0.6):
  precision_pred_i = PCU.estimate(stability, τ, PE_history)

META-SIGNALS (transient, not stored):
  PE_i = obs_i − expected_i                (typed, per-belief)
  precision_obs_i = energy × salience / (H³_std + ε)
  precision_pred_i = PCU.estimate(stability, τ, PE_history)

PREDICT:
  Linear(τ × prev + w_trend × H³_M18 + w_period × H³_M14 + w_ctx × beliefs_{t-1})
  Max 1 first-order + 1 second-order morph per belief.
  Reads beliefs_{t-1} (no intra-phase dependency).

OBSERVE:
  Deterministic f(R³, H³) → Likelihood(value, precision)
  Full horizon window. Separate from predict information.

UPDATE:
  gain = π_obs / (π_obs + π_pred)
  posterior = (1 - gain) × predicted + gain × observed

REWARD:
  reward_i = salience_i × (w1×surprise + w2×resolution + w3×exploration − w4×monotony)
  surprise = |PE_i| × π_pred × (1 − familiarity)
  resolution = (1 − |PE_i|) × π_pred × familiarity
  exploration = entropy(prediction_distribution)
  monotony = π_pred²

SCHEDULE:
  Phase 0 → 1 → 2a → 2b → 3, single-pass, concurrent within phase.
  DAG = scheduler. Topological sort is the only correct ordering.

CONFIG:
  All weights, τ values, thresholds in YAML.
  No hardcoded values. v1.0 = fixed config, no learning.

MIGRATION:
  v1.0: Fixed weights, H³-linear predict, ultra-horizon familiarity proxy
  v1.1: Weight tuning, gradient-free search, ablation grid
  v2.0: Learned prosthetic heads (MI-PLASTICITY), episodic memory for familiarity
```

---

## Open Questions for Future Discussion

1. **96 models → 5 beliefs**: How do individual models map to belief contributions? (e.g., which SPU models contribute to perceived_consonance and how?)
2. **Neurochemical integration**: DA/NE/OPI/5HT → precision modulation? reward scaling? τ adjustment?
3. **BrainOutput mapping**: Which beliefs map to RAM[26], neuro[4], Ψ³[31]?
4. **Online vs offline**: L1/L2 H³ laws in predict() — causality constraint
5. **Config tuning**: Initial weight values — literature-derived or grid-searched?
6. **Test harness**: How to validate belief dynamics (Swan Lake test with beliefs)?

---

## References to Existing Documents

- `Building/Ontology/C3-ONTOLOGY-BOUNDARY.md` — v1.0.0 (needs update to reflect belief architecture)
- `Building/Ontology/C3-FAILURE-MODES.md` — 10 failure modes (all still relevant)
- `Building/C³/MODEL-ATLAS.md` — 96/96 models (data foundation for all decisions)
- `Building/Ontology/R3-ONTOLOGY-BOUNDARY.md` — FROZEN
- `Building/Ontology/H3-ONTOLOGY-BOUNDARY.md` — FROZEN
- `Docs/MI-PLASTICITY.md` — v2.0 learned heads path
