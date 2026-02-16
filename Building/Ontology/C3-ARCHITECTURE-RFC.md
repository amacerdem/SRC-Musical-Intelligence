# C³ Belief Architecture — RFC v1.0.0

**Date**: 2026-02-16
**Status**: DRAFT — pending review before ontology freeze
**Author**: Architect + Claude (AI)
**Prerequisite reads**:
- `Building/Ontology/C3-ONTOLOGY-BOUNDARY.md` (current v1.0.0 proposal)
- `Building/C³/C3-BELIEF-ARCHITECTURE-DISCUSSION.md` (design rationale)
- `Building/C³/MODEL-ATLAS.md` (96/96 empirical foundation)
- `Building/Ontology/C3-FAILURE-MODES.md` (10 failure modes)

---

## 0. Purpose

This RFC formalizes the belief-centered architecture for C³ v1.0, as decided in the
architectural discussion of 2026-02-16. It supersedes the execution model in
`C3-ONTOLOGY-BOUNDARY.md` §3.4 and §4 (which describe the mechanism-centered model).

**What changes**: The 96-model execution graph shifts from mechanism-driven depth ordering
to **belief-centered predictive coding**. Mechanisms become pure function libraries.
Beliefs become the primary architectural entity.

**What does NOT change**: Axes A (role hierarchy R→E→A→I→H), B (9 units), C (4 neurochemicals),
scope system, contract tests, freeze policy, pathways — all remain as specified.

---

## 1. Identity Statement

C³ v1.0 is a **distributed belief-level predictive coding** system with:
- H³-informed linear forward models (one per belief)
- Typed precision-weighted prediction errors (one per belief)
- Inverted-U salience-gated reward
- DAG-ordered phase scheduler (single-pass, no iteration)
- Fixed configuration (no learning)

---

## 2. The 5 Core Beliefs

Each belief has exactly ONE owner unit and a single τ (Murray hierarchy inertia constant).
τ determines how fast the belief tracks sensory input: low τ = reactive, high τ = inertial.

| # | Belief | Owner | τ | Phase | Neuroscience basis |
|---|--------|-------|---|-------|--------------------|
| 1 | `perceived_consonance` | SPU | 0.3 | 0 (sensory) | Bidelman 2009; brainstem FFR consonance hierarchy |
| 2 | `tempo_state` | STU | 0.7 | 0 (sensory) | Grahn & Brett 2007; motor-auditory coupling for beat |
| 3 | `salience_state` | ASU | 0.5 | 1 (gate) | Menon & Uddin 2010; salience network as attentional gate |
| 4 | `familiarity_state` | IMU | 0.85 | 2a (recognize) | Peretz et al. 2009; structural familiarity from statistical regularity |
| 5 | `reward_valence` | ARU | 0.8 | 3 (value) | Blood & Zatorre 2001; striatal reward prediction error |

### 2.1 Why These 5

**Empirical grounding** (from MODEL-ATLAS.md):
- SPU: BCH is first computation; P1 pathway feeds everything downstream
- STU: BEP is the most-used mechanism (31 appearances); motor grounding is foundational
- ASU: Perfect mechanism uniformity (BEP+ASA); attention gate before higher processing
- IMU: 15 models / 159D — the largest unit; cannot be ownerless; cross-circuit bridge
- ARU: Global convergence hub — receives from 6 of 8 other units

**What was excluded and why**:
- `prediction_error` — NOT a belief. PE is a transient derivative signal (observed − predicted). Making it a belief would create circular self-prediction.
- `expectation_state` — NOT a separate belief. Expectation is each belief's `predict()` method, distributed across all 5 beliefs. A central expectation belief would be a god-model (FM-1 risk).
- NDU, MPU, RPU — Do not own core beliefs in v1.0. They provide evidence to the 5 belief owners. (NDU→ASU+PCU, MPU→STU, RPU→ARU.)

### 2.2 PCU: The Precision Engine (NOT a belief)

PCU does not own a belief. PCU is the **precision estimation engine**:
- Estimates `precision_pred_i` for each of the 5 beliefs
- Maintains `PE_history_i` per belief (sliding window of recent PE magnitudes)
- NEVER writes belief values — only precision/gain parameters
- τ = 0.6 (medium — precision estimates adapt moderately)

**Atlas validation**: PPC (pitch precision computation), TPC (timbre precision computation),
MEM (precision history memory) — PCU's triple mechanism maps directly to precision estimation.

### 2.3 Familiarity: Structural, Not Autobiographical

**v1.0 definition**: `familiarity_state` measures **structural familiarity** — how
statistically regular the current audio is at long timescales. A 30-second repeating
loop heard for the first time will register as "structurally familiar" because H³
ultra-horizon smoothness is high.

This is NOT autobiographical familiarity ("I've heard this piece before"). True
autobiographical familiarity requires episodic memory indexing, which is v2.0 scope.

**Horizon separation**: Familiarity uses ULTRA horizons (H24–H28, ~60–180s) exclusively.
Prediction uses LOW horizons (H6–H12, ~0.4–4s). This prevents information overlap
between predict() and observe().

---

## 3. Meta-Signals (Transient, Not Stored)

Meta-signals are computed per frame and consumed immediately. They are NOT beliefs —
they have no owner, no τ, no predict()/update() cycle.

| Signal | Formula | Per-belief? | Consumer |
|--------|---------|-------------|----------|
| `PE_i` | `observed_i − predicted_i` | Yes (4 typed: consonance, tempo, salience, familiarity) | PCU, ARU |
| `precision_obs_i` | Belief-specific (see §3.1) | Yes | Update equation |
| `precision_pred_i` | `PCU.estimate(stability_i, τ_i, PE_history_i)` | Yes | Update equation |
| `gain_i` | `π_obs_i / (π_obs_i + π_pred_i)` | Yes | Update equation |

**Note**: `reward_valence` does not have its own PE. It is the TERMINAL belief —
it aggregates PEs from the other 4 beliefs.

### 3.1 Per-Belief Sensory Confidence (precision_obs)

Generic `1/std` is insufficient. Each belief defines its own observation reliability:

| Belief | `precision_obs` formula | Rationale |
|--------|------------------------|-----------|
| perceived_consonance | `spectral_SNR × salience / (H³_std + ε)` | Consonance is unreliable in noise |
| tempo_state | `onset_regularity × salience / (H³_std + ε)` | Beat clarity depends on onset sharpness |
| salience_state | `energy_contrast × onset_strength / (H³_std + ε)` | Salience is unreliable at low energy |
| familiarity_state | `ultra_horizon_consistency / (H³_std + ε)` | Familiarity is unreliable in brief excerpts |

---

## 4. Belief Lifecycle: predict → observe → update

Each belief implements three methods. This is the core computational cycle.

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

**Double Counting Rule**: Maximum 1 first-order morph (M18=trend OR M8=velocity, not both)
+ maximum 1 second-order morph (M14=periodicity OR M3=std, not both) per belief.
Prevents linear instability from correlated morphologies.

### 4.2 Per-Belief H³ Demand Mapping

| Belief | Trend morph | Period morph | Context | Horizon band |
|--------|-------------|--------------|---------|--------------|
| perceived_consonance | h3[(0, H8, M18, L0)] roughness trend | h3[(14, H12, M14, L0)] tonalness periodicity | tempo_{t-1} × 0.1 | meso (H6–H12) |
| tempo_state | h3[(10, H6, M18, L0)] spectral_flux trend | h3[(10, H6, M14, L0)] beat regularity | consonance_{t-1} × 0.05 | meso (H6–H12) |
| salience_state | h3[(7, H6, M18, L0)] amplitude trend | — (salience is aperiodic) | consonance_{t-1}×0.2 + tempo_{t-1}×0.2 | meso (H6–H8) |
| familiarity_state | h3[(14, H24, M18, L0)] tonalness macro trend | — | consonance_{t-1} × 0.1 | ultra (H24–H28) |
| reward_valence | Does not predict — aggregates PEs | — | — | — |

### 4.3 observe() — Deterministic Extraction

```python
def observe(self, r3, h3) -> Likelihood:
    """Extract current observation from sensory input."""
    raw = f(r3, h3)  # deterministic function, full horizon window
    precision = self.compute_precision_obs(r3, h3)  # belief-specific
    return Likelihood(value=raw, precision=precision)
```

**Information separation**: observe() uses the FULL horizon range of H³.
predict() uses only LOW horizons (H6–H12) for the 4 predictive beliefs.
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

Single-pass, DAG-ordered, concurrent within phase.

```
Phase 0  (sensory grounding)
  ├── perceived_consonance.predict()  ─┐
  ├── perceived_consonance.observe()   ├── concurrent
  ├── tempo_state.predict()            │
  └── tempo_state.observe()           ─┘
  → Update both beliefs (Bayesian fusion)

Phase 1  (attentional gate)
  ├── salience_state.predict()  ─┐
  └── salience_state.observe()   ├── sequential (reads Phase 0 beliefs)
  → Update salience belief       ┘

Phase 2a  (predict ∥ recognize)
  ├── familiarity_state.predict()  ─┐
  └── familiarity_state.observe()   ├── concurrent
  → Update familiarity belief       ┘

Phase 2b  (meta-computation)
  ├── PE_i = observed_i − predicted_i     (for i = 1..4)
  ├── precision_pred_i = PCU.estimate(...)
  └── gain_i = π_obs_i / (π_obs_i + π_pred_i)

Phase 3  (value computation)
  └── reward_valence = ARU.compute_reward(PE_i, precision_pred_i, salience_i, familiarity)
```

**Properties**:
- Single-pass per frame (no iteration, no convergence loop)
- predict() reads `beliefs_{t-1}` — all previous-frame values, no intra-phase dependency
- Multi-timescale via τ (Murray hierarchy), not scheduler rate
- Hall of mirrors prevention: Phase 0 always re-computes consonance and tempo from R³/H³

---

## 6. Reward Function — Inverted-U Salience-Gated

```python
def compute_reward(PE_i, precision_pred_i, salience_i, familiarity):
    # Per-belief reward components
    for i in [consonance, tempo, salience, familiarity]:
        surprise_i    = |PE_i| × precision_pred_i × (1 − familiarity)
        resolution_i  = (1 − |PE_i|) × precision_pred_i × familiarity
        exploration_i = entropy(prediction_distribution_i)
        monotony_i    = precision_pred_i²

        reward_i = salience_i × (w1×surprise_i + w2×resolution_i
                                + w3×exploration_i − w4×monotony_i)

    # Aggregate
    reward_valence = Σ reward_i × familiarity_mod
```

**Inverted-U dynamics**:
- Novel + unpredictable → high surprise, low resolution → moderate reward
- Familiar + predictable → low surprise, high monotony → low reward (boring)
- Familiar + violated → high surprise × high familiarity → peak reward (the "aha!")
- Resolution amplified by familiarity (familiar context makes resolution more satisfying)

**Atlas validation**:
- RPU-β1-IUCP directly models the inverted-U complexity preference
- ARU-β4-NEMAC validates familiarity-modulated reward (nostalgia circuit)

---

## 7. Unit Role Mapping

How do the 9 units map to the 5-belief architecture?

| Unit | Belief role | What it does for beliefs |
|------|------------|------------------------|
| **SPU** | Owns `perceived_consonance` | BCH provides raw consonance; higher-tier models refine spectral evidence |
| **STU** | Owns `tempo_state` | HMCE provides beat/meter estimate; motor models provide entrainment evidence |
| **ASU** | Owns `salience_state` | SNEM provides novelty detection; all 9 models compute salience evidence |
| **IMU** | Owns `familiarity_state` | MEAMN provides memory trace; 15 models contribute structural familiarity |
| **ARU** | Owns `reward_valence` | SRP aggregates salience-gated PEs; affect models compute valence components |
| **PCU** | Precision engine | HTP provides base precision; 10 models estimate precision per belief |
| **RPU** | Evidence → ARU | DAED provides DA anticipation; IUCP provides complexity preference → reward |
| **MPU** | Evidence → STU | PEOM provides motor entrainment; 10 models provide beat/groove evidence |
| **NDU** | Evidence → ASU + PCU | MPG provides deviance detection; feeds salience and precision |

### 7.1 Remaining 91 Models

The 5 belief owners are unit-level (SPU, STU, ASU, IMU, ARU). Within each unit,
the **Relay** provides the primary observation, and higher-tier models (Encoders,
Associators, Integrators, Hubs) contribute evidence via likelihood messages.

```
Within SPU:
  BCH (Relay, depth 0)     → primary observe() for perceived_consonance
  PSCL (Encoder, depth 1)  → evidence: pitch_salience likelihood
  PCCR (Encoder, depth 1)  → evidence: chroma purity likelihood
  STAI (Associator, depth 2) → evidence: aesthetic integration
  ...
```

**How 96 models contribute to 5 beliefs**: Each model computes a likelihood message
for one or more beliefs. The belief owner fuses these likelihoods with its prediction
via the Bayesian update. This replaces the current mechanism-based depth execution
with a belief-directed evidence accumulation.

**Detailed 96-model → belief mapping is deferred to v1.0 implementation phase.**

---

## 8. Configuration — YAML Schema

All parameters are externalized. No hardcoded values in compute().

```yaml
c3_beliefs:
  perceived_consonance:
    owner: SPU
    tau: 0.3
    baseline: 0.5
    predict:
      w_trend: 0.15
      w_period: 0.10
      w_ctx:
        tempo_state: 0.10
      h3_trend: [0, 8, 18, 0]     # (r3_idx, horizon, morph, law)
      h3_period: [14, 12, 14, 0]
    observe:
      r3_groups: [A, C, F]
      h3_horizons: [0, 18]         # full range
    precision_obs:
      formula: "spectral_SNR * salience / (h3_std + eps)"
      eps: 1e-6

  tempo_state:
    owner: STU
    tau: 0.7
    baseline: 0.5
    predict:
      w_trend: 0.20
      w_period: 0.25
      w_ctx:
        perceived_consonance: 0.05
      h3_trend: [10, 6, 18, 0]
      h3_period: [10, 6, 14, 0]
    observe:
      r3_groups: [B, D, G]
      h3_horizons: [0, 12]
    precision_obs:
      formula: "onset_regularity * salience / (h3_std + eps)"
      eps: 1e-6

  salience_state:
    owner: ASU
    tau: 0.5
    baseline: 0.5
    predict:
      w_trend: 0.15
      w_period: null               # salience is aperiodic
      w_ctx:
        perceived_consonance: 0.20
        tempo_state: 0.20
      h3_trend: [7, 6, 18, 0]
    observe:
      r3_groups: [A, B, D]
      h3_horizons: [0, 12]
    precision_obs:
      formula: "energy_contrast * onset_strength / (h3_std + eps)"
      eps: 1e-6

  familiarity_state:
    owner: IMU
    tau: 0.85
    baseline: 0.5
    predict:
      w_trend: 0.10
      w_period: null
      w_ctx:
        perceived_consonance: 0.10
      h3_trend: [14, 24, 18, 0]    # ultra horizon
    observe:
      r3_groups: [A, F, H]
      h3_horizons: [24, 28]        # ultra only
    precision_obs:
      formula: "ultra_horizon_consistency / (h3_std + eps)"
      eps: 1e-6

  reward_valence:
    owner: ARU
    tau: 0.8
    baseline: 0.0                   # reward is zero-centered
    # reward does not predict — it aggregates
    reward:
      w_surprise: 1.0
      w_resolution: 1.2
      w_exploration: 0.3
      w_monotony: 0.8

c3_precision:
  owner: PCU
  tau: 0.6
  pe_history_window: 32             # frames
  stability_decay: 0.95

c3_scheduler:
  phases: [0, 1, "2a", "2b", 3]
  phase_0: [perceived_consonance, tempo_state]
  phase_1: [salience_state]
  phase_2a: [familiarity_state]
  phase_2b: [precision_computation]
  phase_3: [reward_valence]
```

**v1.0 = NO LEARNING**. All values above are constants. Bayesian update is inference
(combining prior with likelihood), not parameter learning. The τ, weights, and
precision formulas never change during execution.

**Learning roadmap**:
- v1.1: Gradient-free weight tuning (grid search over w_trend, w_period, w_ctx)
- v2.0: Learned prosthetic heads (MI-PLASTICITY), episodic memory, Hebbian pathway weights

---

## 9. Alignment with Existing Ontology

### 9.1 What This RFC Changes in C3-ONTOLOGY-BOUNDARY.md

| Section | Current | Proposed |
|---------|---------|----------|
| §3.4 (Belief Graph) | ~25 fine-grained beliefs (onset_prob, pitch_salience, ...) | 5 core beliefs + evidence hierarchy. Fine-grained beliefs become evidence contributions, not top-level beliefs |
| §3.4.3 (Belief Update) | Three update methods (bayesian, ema, direct) | Single method: precision-weighted Bayesian fusion for all 5 beliefs |
| §4.4 (Scheduler) | 6-phase depth-ordered execution | 5-phase belief-ordered execution (Phase 0→1→2a→2b→3) |
| §4.6 (Tick pseudocode) | Steps 1-10 mechanism-driven | Replaced by predict→observe→update→reward cycle |
| §7.4 (Mechanism removal) | Mechanisms as metadata | Mechanisms become utility functions; belief lifecycle is the architecture |

### 9.2 What This RFC Does NOT Change

| Component | Status | Why unchanged |
|-----------|--------|---------------|
| Axis A (role hierarchy) | FROZEN | R→E→A→I→H depth ordering still determines within-unit execution |
| Axis B (9 units) | FROZEN | Units remain as organizational containers |
| Axis C (4 neurochemicals) | FROZEN | DA/NE/OPI/5HT still modulate via volume transmission |
| 12 pathways | FROZEN | Cross-unit routing still declared, typed, and unidirectional |
| Scope system | FROZEN | internal/external/hybrid still governs dim visibility |
| Contract tests (§6) | FROZEN | State Declaration, Single-Writer, Causality, Role Consistency all still enforced |
| BrainOutput structure | FROZEN | tensor + RAM(26) + neuro(4) + Ψ³ unchanged |
| Feature Registry (§7.1) | FROZEN | Name-based R³ addressing unchanged |

### 9.3 How Fine-Grained Beliefs Map to Core Beliefs

The ~25 beliefs listed in C3-ONTOLOGY-BOUNDARY.md §3.4.1 become **evidence signals**
within the 5-belief framework:

| Old belief (§3.4.1) | New role | Core belief it feeds |
|---------------------|---------|---------------------|
| `consonance_state` | Primary observation | → perceived_consonance |
| `roughness_state` | Evidence (anti-consonance) | → perceived_consonance |
| `pitch_salience` | Evidence | → perceived_consonance |
| `spectral_tension` | Evidence | → perceived_consonance |
| `tempo_estimate` | Primary observation | → tempo_state |
| `meter_state` | Evidence | → tempo_state |
| `groove_phase` | Evidence | → tempo_state |
| `entrainment_strength` | Evidence | → salience_state |
| `salience_map` | Primary observation | → salience_state |
| `attention_allocation` | Evidence | → salience_state |
| `familiarity` | Primary observation | → familiarity_state |
| `memory_scaffold` | Evidence | → familiarity_state |
| `affect_valence` | Primary observation | → reward_valence |
| `affect_arousal` | Evidence | → reward_valence |
| `aesthetic_pleasure` | Evidence | → reward_valence |
| `narrative_tension` | Evidence | → reward_valence |
| `key_estimate` | Evidence | → perceived_consonance (tonal context) |
| `harmonic_function` | Evidence | → perceived_consonance |
| `phrase_boundary` | Evidence | → familiarity_state (structural segmentation) |
| `section_label` | Evidence | → familiarity_state |
| `timbral_identity` | Evidence | → familiarity_state (sonic identity) |

---

## 10. Relationship to Failure Modes

All 10 failure modes from `C3-FAILURE-MODES.md` remain relevant:

| FM | How belief architecture addresses it |
|----|--------------------------------------|
| FM-1 (flat collapse) | Phase scheduler enforces DAG ordering. Beliefs have declared phases. |
| FM-2 (redundant binding) | Binding Service unchanged — still caches cross-domain products |
| FM-3 (circular deps) | predict() reads `beliefs_{t-1}` only — no intra-frame cycles |
| FM-4 (multiple writers) | Single-Writer Invariant: 1 owner per belief. PCU writes precision, not beliefs. |
| FM-5 (hidden state) | Belief state is the ONLY state. All in `BeliefStore`, fully serializable. |
| FM-6 (causality) | predict() uses L0 only. observe() uses full H³ but is present-frame. |
| FM-7 (neuro race) | Unchanged — weighted average at same depth |
| FM-8 (unbounded memory) | Unchanged — bounded buffer for episodic memory |
| FM-9 (scope leakage) | Unchanged — scope filtering in scheduler |
| FM-10 (index fragility) | Unchanged — Feature Registry for all R³ access |

**New risk identified**: **FM-11 (predict/observe information overlap)**.
If predict() and observe() both read the same H³ windows, PE is trivially small.
**Prevention**: Horizon separation — predict uses H6–H12, observe uses full range.
Familiarity prediction uses H24–H28 exclusively.

---

## 11. Next Steps

### 11.1 Immediate (before freeze)

1. **Review this RFC** — identify gaps, contradictions, or unsupported claims
2. **Reconcile with C3-ONTOLOGY-BOUNDARY.md** — update §3.4, §4, §7.4 to reflect decisions
3. **Minimal kernel prototype** — implement 3-model proof of concept:
   - BCH (SPU Relay) → perceived_consonance observe()
   - HMCE (STU Relay) → tempo_state observe()
   - SNEM (ASU Relay) → salience_state observe()
   - PCU precision engine (PE computation + precision estimation)
   - ARU reward (aggregate PEs → reward_valence)
   - Full predict→observe→update→reward cycle on Swan Lake 30s

### 11.2 Post-freeze (v1.0 implementation)

4. Map all 96 models to belief evidence contributions
5. Implement YAML config loader
6. Implement BeliefStore with serialization
7. Run Swan Lake end-to-end: Audio → R³ → H³ → C³(5 beliefs) → BrainOutput
8. Ablation tests: remove each belief, measure output degradation

### 11.3 Future versions

- **v1.1**: Gradient-free weight tuning, ablation grid, config search
- **v2.0**: Learned prosthetic heads (MI-PLASTICITY §13), episodic memory for
  autobiographical familiarity, Hebbian pathway weights, multi-rate belief cadence

---

## 12. Open Questions

1. **96→5 detailed mapping**: Which models provide evidence to which beliefs? Some models
   (e.g., PCU-β4-CHPI "Cross-Modal Harmonic Predictive Integration") touch multiple beliefs.
   Need per-model assignment table.

2. **Neurochemical integration**: v1.0 decision: neurochemicals remain **metadata only**.
   DA/NE/OPI/5HT accumulate through depth hierarchy (Axis C unchanged) and appear in
   BrainOutput.neuro(4), but they do NOT modulate precision/gain/reward equations in v1.0.
   The precision and reward formulas use only salience, PE, and H³ — no neurochemical terms.
   v1.1 scope: DA→precision scaling, NE→gain modulation, 5HT→τ adjustment, OPI→reward bias.

3. **BrainOutput dimensionality**: Current BrainOutput assembles exportable dims from all
   96 models (~600-700D). How does the belief architecture affect this? Do we export
   belief posteriors (5D) + evidence contributions (~600D) + neuro(4) + RAM(26)?

4. **Multi-rate beliefs**: v1.0 runs all beliefs at frame rate. v1.1 may run familiarity
   at phrase rate, reward at beat rate. How does this interact with the phase scheduler?

5. **Online vs offline predict()**: v1.0 uses L0 only (causal). In offline mode, can
   predict() use L1/L2 for better prediction? What tags need to be set?

---

## 13. Version History

| Version | Date | Changes |
|---------|------|---------|
| RFC v1.0.0 | 2026-02-16 | Initial RFC. 5 beliefs + PCU precision engine, per-belief predict, H³-linear model, inverted-U reward, phase scheduler. |

---

*This RFC is a review draft. It captures decisions from the C³ Belief Architecture
Discussion and proposes a formal specification for the C³ v1.0 belief-centered
predictive coding system. Upon approval, it will be merged into C3-ONTOLOGY-BOUNDARY.md
and the ontology will be frozen.*
