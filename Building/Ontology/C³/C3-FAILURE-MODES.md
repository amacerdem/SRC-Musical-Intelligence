# C³ Failure Modes & Prevention

**Version**: 2.0.0
**Date**: 2026-02-21 (v2.0 Function-based update)
**Companion**: `C3-ONTOLOGY-BOUNDARY.md` §8

This document characterizes 12 concrete failure patterns that arise when 96 cognitive
models execute without proper architectural constraints, and specifies how the C³
design prevents each one. FM-1 through FM-10 apply to models within Functions.
FM-11 and FM-12 are Function-level failure modes (v2.0).

---

## FM-1: Flat Graph Collapse

**Pattern**: All 96 nuclei execute as independent peers. No hierarchy, no ordering.
Each nucleus reads R³/H³ directly, computes independently, and writes to a shared output
tensor. Result: a 96-wide flat DAG with no structure.

**Why it fails**:
- No way to express "BCH's consonance informs PSCL's pitch salience" — they're peers
- Associators can't combine Encoder outputs because there's no ordering guarantee
- Hubs (MAA, PSH, TAR) can't integrate because their inputs haven't been computed yet
- Output is a bag of 96 independent signals with no coherence

**Prevention**: Depth-ordered execution (R→E→A→I→H). Each nucleus declares a role with
a fixed depth. The scheduler guarantees depth-N completes before depth-(N+1) begins.
Scope-filtering ensures downstream nuclei see only routable dims from upstream.

**Contract**: Role Consistency Test (§6.5 of ontology).

---

## FM-2: Redundant Cross-Domain Binding

**Pattern**: Dissolved Group E (24D cross-domain interactions) was removed from R³.
Now 40+ nuclei each independently compute `consonance × energy`, `pitch × timbre`, etc.
Same products computed 40 times per frame.

**Why it fails**:
- Wasted computation (40× redundancy)
- Subtle inconsistencies if implementations drift
- No single source of truth for cross-domain products
- Memory waste from 40 copies of identical tensors

**Prevention**: Binding Service (§4.2 of ontology). A shared, caching service computes
each cross-domain product ONCE on first access. All nuclei call
`binding_service.get_binding(name)` and receive the same cached tensor.

**Contract**: Binding Registry declares every legal product. Undeclared products = error.

---

## FM-3: Circular Dependencies

**Pattern**: Nucleus A reads B's output, B reads C's output, C reads A's output.
Execution order is undefined → deadlock or unstable oscillation.

**Why it fails**:
- No topological ordering possible for a cycle
- Result depends on execution order (non-deterministic)
- Iterative fixed-point convergence is expensive and may not converge

**Prevention**: Depth ordering is a strict DAG.
- Within a unit: `depth(consumer) > depth(producer)` for all UPSTREAM_READS
- Cross-unit: pathways execute BETWEEN unit computation phases, not within
- Formal proof: the full execution graph is acyclic by construction

**Contract**: Role Consistency Test verifies `UPSTREAM_READS ⊆ {lower-depth nuclei}`.

---

## FM-4: Multiple Writers to Same Belief

**Pattern**: Both BCH and PSCL write `pitch_salience`. BCH writes 0.8, PSCL overwrites
with 0.6. Or: execution order determines which value "wins" — a race condition.

**Why it fails**:
- Downstream consumers see different values depending on execution order
- No clear debugging — "who set pitch_salience to 0.6?"
- Responsibility diffusion — nobody owns the belief
- Contradictory updates if writers disagree

**Prevention**: Single-Writer Invariant (§3.4.2 of ontology). Each belief variable has
exactly ONE owner. Others contribute evidence (likelihoods) but never write the posterior.

**Contract**: Single-Writer Belief Test (§6.2). Compile-time enforcement.

**Example**:
```
✗ BCH.owns("pitch_salience") AND PSCL.owns("pitch_salience")  → COMPILE ERROR
✓ BCH.owns("pitch_salience"), PSCL.provides_evidence("pitch_salience")  → OK
```

---

## FM-5: Hidden State Accumulation

**Pattern**: A nucleus has `self._prev_consonance = x` that persists between frames.
This creates implicit temporal dependence. Nobody knows this state exists. It can't be
serialized, inspected, or reset.

**Why it fails**:
- State leaks across pieces/sessions (previous piece's memory affects current)
- Non-reproducible results (depends on history)
- Can't serialize/restore for checkpointing
- Can't inspect for debugging ("why is consonance stuck at 0.9?")
- Violates the glass-box principle

**Prevention**: State Declaration Test (§6.1). Every mutable attribute must be declared
in `state_schema` with type, shape, default, serialization, and citation.

**Contract**: Runtime introspection after `compute()` — undeclared changed attributes = error.

**Example**:
```python
# ✗ Hidden state
class BadNucleus(Encoder):
    def __init__(self):
        self._ema = 0.0  # Not declared anywhere

    def compute(self, ...):
        self._ema = 0.9 * self._ema + 0.1 * x  # Invisible accumulation

# ✓ Declared state
class GoodNucleus(Encoder):
    state_schema = StateSchema(fields={
        "ema_consonance": StateFieldSpec(
            name="ema_consonance", dtype="float32", shape=(),
            default=0.5, citation="Tillmann 2000",
            serialize=torch.save, deserialize=torch.load
        )
    })
```

---

## FM-6: Causality Violation in Online Mode

**Pattern**: A real-time processing system uses H³ L1 (forward window) or L2 (bidirectional
window). These windows require future frames that don't exist yet in online mode.

**Why it fails**:
- Forward window reads frames [t, t+W-1] — frame t+1 hasn't arrived yet
- Bidirectional window reads [t-W/2, t+W/2] — same problem
- Result: either crash, or silent use of zeros/garbage for future frames
- Predictions based on non-existent data are meaningless

**Prevention**: Causality Test (§6.3). Online mode restricts ALL H³ demands to L0
(backward/memory) only. L1 and L2 are available only in offline mode, and their outputs
must be tagged `acausal=True`.

**Contract**: H³ demand inspection at instantiation time — L1/L2 in online = hard error.

---

## FM-7: Neurochemical State Race

**Pattern**: Two Relays at depth 0 both `produce` DA: SRP writes DA=0.78, then DAED
writes DA=0.72. Final value depends on execution order within depth 0.

**Why it fails**:
- Non-deterministic if parallel execution
- Order-dependent if sequential
- Downstream nuclei see different DA values depending on who ran last

**Prevention**: When multiple nuclei at the same depth produce the same neurochemical,
the orchestrator takes their **weighted average** for the initial set (not sequential
overwrite). Subsequent `amplify`/`inhibit` at later depths accumulate additively with
0.2 scaling.

**Deterministic rule**:
```
depth_0_producers[DA] = [(SRP, 0.78, weight=0.6), (DAED, 0.72, weight=0.4)]
DA_after_depth_0 = weighted_mean = 0.78*0.6 + 0.72*0.4 = 0.756
```

---

## FM-8: Unbounded Memory Growth

**Pattern**: Every salient moment is stored in episodic memory. A 3-hour concert
generates thousands of events. Memory grows without bound.

**Why it fails**:
- OOM crash on long pieces
- Linear search degradation
- No garbage collection strategy

**Prevention**: Bounded buffer (default 1000 events). When full, lowest-salience events
are evicted (salience = DA value at storage time). Semantic memory grows but is explicit,
serializable, and visible.

---

## FM-9: Scope Leakage

**Pattern**: An Encoder reads `external`-scoped dims from the Relay's output. These dims
were meant only for the final BrainOutput tensor, not for intra-unit processing.

**Why it fails**:
- External dims may encode information not appropriate for downstream processing
- Breaks the semantic contract of the scope system
- Makes it impossible to change external dims without breaking downstream nuclei

**Prevention**: Scope-filtering in the scheduler. When routing upstream outputs to
downstream consumers, only `routable_dims` (internal + hybrid) are exposed. External
dims exist in the full tensor but are masked during routing.

---

## FM-10: Feature Index Fragility

**Pattern**: Code contains `consonance = r3[:, :, 14]`. R³ is reorganized (features
added, groups reordered). Index 14 now points to a different feature. All hard-coded
indices silently break.

**Why it fails**:
- Silent corruption — code runs without errors but produces wrong results
- 96 model files × ~15 indices each = ~1440 hard-coded references to update
- R³ renumbering is GUARANTEED as the 31D gap space is filled

**Prevention**: Feature Registry (§7.1 of ontology). All R³ access uses
`registry.resolve("brightness_kuttruff")` which compiles to the current index for the
active R³ version. Numeric indices in code are a lint error.

**Migration**: IndexAdapter (§7.2) maps legacy indices to stable names for the transition period.

---

---

## FM-11: Cross-Function Model Contradiction (v2.0)

**Pattern**: Model X has primary assignment F2 (Prediction) and secondary assignment F5
(Emotion). X produces evidence for both Functions. F2 interprets X's output as "high
prediction confidence" while F5 interprets the same output as "high emotional arousal."
These interpretations conflict — high confidence implies stability, high arousal implies change.

**Why it fails**:
- Same model output carries contradictory semantics in different Functions
- No arbitration mechanism — both Functions trust the evidence equally
- Debugging becomes impossible ("is X a prediction model or an emotion model?")
- Downstream beliefs diverge based on which Function's interpretation dominates

**Prevention**: Primary/Secondary distinction (§3.2' of ontology). A model's primary
Function receives full output weight. Secondary Functions receive only specific
pre-declared output fields (dims), not the full model output. Each field has exactly one
semantic interpretation declared in the model's Function manifest.

**Contract**: Function Manifest Test — every model declares which output dims map to
which Function with what semantic tag. Conflicting tags = compile error.

---

## FM-12: Function Belief Explosion (v3.0 — 3-Category)

**Pattern**: Unbounded belief declarations cause PE computation to explode O(N²),
precision buffers consume O(N × H × W) memory, reward signal is diluted.

**Why it fails**:
- Computational cost scales quadratically with belief count (cross-belief context)
- Memory for PE ring buffers: N_beliefs × N_horizons × window_size
- Reward signal is diluted: averaging over many PEs → everything converges to mean
- τ tuning becomes intractable with too many independent inertia parameters
- Debugging: "which of 131 beliefs caused this reward spike?"

**Prevention (v3.0)**: 3-category system controls PE overhead:

| Category | Cap/Function | PE | Precision buffer | Reward input |
|----------|:------------:|:--:|:----------------:|:------------:|
| **Core** | max 5 | Yes | Yes (ring buffer) | Yes (PE-based) |
| **Appraisal** | max 10 | No | No | No (evidence only) |
| **Anticipation** | max 5 | No | No | No (prediction only) |

Total per Function: max 20 beliefs. System-wide: max 180 theoretical.
**Actual**: 131 beliefs (36 Core + 65 Appraisal + 30 Anticipation).

**Only 36 Core Beliefs** carry PE/precision/reward overhead. This is manageable
(vs 131 full-cycle beliefs which would be intractable).

**Contract**: Function Belief Registry with category validation:
```
✗ F7.register_core_belief("a", "b", "c", "d", "e", "f")
  → ERROR: 6 Core beliefs exceed max 5

✓ F7.register_core_belief("period_entrainment", "kinematic_efficiency", "groove_quality", "context_depth")
  F7.register_appraisal_belief("timing_precision", "period_lock_strength", ...)
  F7.register_anticipation_belief("next_beat_pred", "groove_trajectory", ...)
  → OK: 4 Core + 9 Appraisal + 4 Anticipation = 17 ≤ 20
```

---

## Summary Matrix

| # | Failure Mode | Severity | Prevention | Contract Test |
|---|-------------|----------|------------|---------------|
| FM-1 | Flat graph collapse | Critical | Depth-ordered execution | Role Consistency |
| FM-2 | Redundant binding | Performance | Binding Service + cache | Binding Registry |
| FM-3 | Circular dependencies | Critical | DAG by construction | Role Consistency |
| FM-4 | Multiple writers | Critical | Single-Writer Invariant | Single-Writer Test |
| FM-5 | Hidden state | Correctness | State Declaration | State Declaration Test |
| FM-6 | Causality violation | Correctness | Online=L0 only | Causality Test |
| FM-7 | Neuro state race | Correctness | Weighted average at depth | Determinism Test |
| FM-8 | Unbounded memory | Performance | Bounded buffer | Runtime monitor |
| FM-9 | Scope leakage | Correctness | Scope-filtering in scheduler | Role Consistency |
| FM-10 | Index fragility | Correctness | Feature Registry | Compile-time resolution |
| FM-11 | Cross-Function contradiction | Correctness | Primary/Secondary + manifest | Function Manifest Test |
| FM-12 | Belief explosion | Performance | 3-category caps (5C+10A+5N/Function) | Function Belief Registry |
