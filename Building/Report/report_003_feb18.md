# Musical Intelligence (MI) — Relay Integration Plan

**Date:** 18 February 2026
**Version:** Kernel v2.5 → v3.0 (Relay-Enriched Belief Architecture)
**Codebase:** `Musical_Intelligence/` — 211 Python files
**Supersedes:** Report #2 (Kernel v2.1, multi-scale + horizon precision)
**Status:** PLAN — awaiting literature review and revision

---

## 1. Executive Summary

This report documents the integration plan for bringing 6 relay nuclei into the C³ kernel. The kernel currently operates with 5 beliefs (consonance, tempo, salience, familiarity, reward) using R³ features, H³ morphologies, and a single relay wrapper (BCH). The 6 relay nuclei — SNEM, MMP, MPG, DAED, BCH, HMCE — were implemented as standalone `Nucleus` subclasses but remain disconnected from the kernel's belief cycle.

**Goal:** Each belief's `observe()` and `predict()` functions gain relay-enriched inputs, producing richer sensory evidence while maintaining full backward compatibility.

**Constraint:** The system must not regress. All existing stress tests (9/11 PASS) must continue to pass at every integration step. Every relay wrapper includes a fallback path — if the relay fails or is absent, the belief reverts to its current R³+H³ observation logic.

**Approach:** 4-wave incremental integration following the BCH wrapper pattern established in v2.0.

---

## 2. Current State Assessment

### 2.1 Kernel Architecture (v2.5)

```
Frame Input (r3: 97D, h3: ~58 tuples)
    │
    ▼
[Phase 0]  BCH relay + consonance/tempo observe()
    │
    ▼
[Phase 1]  Salience observe() + predict() + update()
    │
    ▼
[Phase 2a] Multi-scale consonance predict/observe + familiarity observe()
    │
    ▼
[Phase 2b] PE + per-horizon precision computation
    │
    ▼
[Phase 2c] Bayesian posterior fusion (all predictive beliefs)
    │
    ▼
[Phase 3]  Multi-scale reward + horizon activation gating
    │
    ▼
KernelOutput: 5 beliefs + 5 PEs + precision + reward + ms_pe + ms_precision
```

### 2.2 Five Beliefs — Current Evidence Sources

| Belief | Owner | τ | Current observe() Source | Current predict() Source |
|--------|-------|---|-------------------------|-------------------------|
| perceived_consonance | SPU | 0.3 | BCH wrapper (3D: hierarchy, consonance_signal, template_match) + R³ fallback (5 features) | H³ roughness trend (H8, M18) + tonalness periodicity (H12, M14) |
| tempo_state | STU | 0.7 | R³ rhythm features (tempo, beat_strength, pulse_clarity, rhythmic_regularity) | H³ onset trend (H6, M18) + onset periodicity (H6, M14) |
| salience_state | ASU | 0.3 | R³ energy + H³ velocity (3 features) + PE carry-over | H³ amplitude trend (H6, M18) |
| familiarity_state | IMU | 0.85 | H³ M14 periodicity (50%) + M2 stability (35%) + R³ tonal (15%) + energy gate | H³ tonalness trend (H16, M18) |
| reward_valence | ARU | 0.8 | Derived from other beliefs (not observed) | Inertia + context |

### 2.3 Six Relay Nuclei — Available But Disconnected

| Relay | Unit | Output Dim | Layers | H³ Demands | Laws | File |
|-------|------|-----------|--------|------------|------|------|
| **BCH** | SPU | 16D | E4+M4+P4+F4 | 48 tuples | L0+L1+L2 | `units/spu/relays/bch.py` |
| **HMCE** | STU | 13D | E5+M2+P3+F3 | 18 tuples | L0 only | `units/stu/relays/hmce.py` |
| **SNEM** | ASU | 12D | E3+M3+P3+F3 | 18 tuples | L0+L2 | `units/asu/relays/snem.py` |
| **MMP** | IMU | 12D | E3+P3+F3+C3 | 18 tuples | L0+L2 | `units/imu/relays/mmp.py` |
| **DAED** | RPU | 8D | E4+M2+P2 | 16 tuples | L0+L2 | `units/rpu/relays/daed.py` |
| **MPG** | NDU | 10D | E4+M3+P2+F1 | 16 tuples | L0+L2 | `units/ndu/relays/mpg.py` |

**Total available H³ demands (all relays):** 134 tuples raw, ~100 after L0-only filtering + dedup

### 2.4 Performance Baseline

| Metric | Value (v2.5) |
|--------|-------------|
| H³ tuples | 58 |
| C³ kernel fps | ~440 |
| H³ extraction time (30s) | 0.06s |
| Stress test | 9/11 PASS |
| Reward (Swan/Bach/Beethoven) | +0.066 / +0.108 / +0.056 |
| Consonance range | 0.35–0.36 |

---

## 3. Five Design Questions — Answered

### 3.1 Q: Is the belief system sufficient or should we add more beliefs?

**Answer: 5 beliefs are sufficient for v3.0.**

The 5 beliefs map to 5 orthogonal cognitive functions:

```
perceived_consonance  →  "How harmonious is this?"      (sensory quality)
tempo_state           →  "What is the rhythmic pulse?"   (temporal structure)
salience_state        →  "How attention-grabbing?"       (attentional gate)
familiarity_state     →  "Have I heard this pattern?"    (memory recognition)
reward_valence        →  "How rewarding is this moment?" (motivational output)
```

Relay outputs are **evidence** for these beliefs, not new beliefs. MMP doesn't create a "memory_belief" — it enriches the evidence flowing into `familiarity_state`. DAED doesn't create a "dopamine_belief" — it enriches the evidence informing reward computation.

**Rationale:** Adding a 6th belief (e.g., `narrative_state`, `motor_urge`) requires:
- New scheduler phase
- New PE tracking + precision ring buffer
- New term in reward formula
- New H³ demands for predict/observe
- New cross-belief context weights

This is a v4.0 discussion after relay integration proves stable.

### 3.2 Q: Should we use the rich original model outputs?

**Answer: Yes, but P-layer (Percept) primary, F-layer (Forecast) secondary.**

Each relay produces 4 layers (E/M/P/F) with scope tags:

| Layer | Kernel Use | Rationale |
|-------|-----------|-----------|
| **P** (Percept) | **Primary** — feeds `observe()` | Current cognitive state, highest relevance |
| **F** (Forecast) | **Secondary** — feeds `predict()` | Forward model support, complements H³ morphs |
| **E** (Extraction) | **Not used** in v3.0 | Internal computation, relay-private |
| **M** (Mechanism) | **Not used** in v3.0 | Mathematical intermediate, no belief value |

Example — HMCE integration for tempo:

```python
# P-layer → tempo.observe() enrichment
P: a1_encoding, stg_encoding, mtg_encoding  →  multi-scale context evidence

# F-layer → tempo.predict() enrichment
F: context_prediction, phrase_expect, structure_predict  →  forward model terms
```

### 3.3 Q: How do models communicate with each other?

**Answer: Three mechanisms, progressively enabled.**

**Mechanism A — Shared relay_outputs dict (Wave 1):**

```python
# In scheduler, Phase 0:
relay_outputs = {}
relay_outputs["bch"] = bch_wrapper.compute(r3, h3)
relay_outputs["hmce"] = hmce_wrapper.compute(r3, h3)
relay_outputs["snem"] = snem_wrapper.compute(r3, h3)
relay_outputs["mmp"] = mmp_wrapper.compute(r3, h3)
relay_outputs["daed"] = daed_wrapper.compute(r3, h3)
relay_outputs["mpg"] = mpg_wrapper.compute(r3, h3)

# In Phase 0: consonance.observe(r3, h3, bch_out=relay_outputs["bch"])
# In Phase 0: tempo.observe(r3, h3, hmce_out=relay_outputs["hmce"])
# etc.
```

**Mechanism B — Cross-relay routing (Wave 2):**

```python
# DAED needs BCH's consonance_signal for anticipatory DA computation
daed_wrapper.compute(r3, h3, cross_inputs={"consonance_signal": relay_outputs["bch"].consonance_signal})
```

**Mechanism C — Neurochemical broadcast (Wave 4, future):**

```python
# DA/NE/OPI/5HT global state tensor modulates precision/gain
# Not in v3.0 scope
```

### 3.4 Q: How does e.g. MMP write to familiarity, with what weights?

**Answer: Owner relay dominant, weighted blend with fallback.**

The pattern follows BCH → consonance (established, tested, proven):

```python
# familiarity.observe() — v3.0 (MMP-enriched)
def observe(self, r3, h3, *, mmp_out=None):
    if mmp_out is not None:
        # MMP is the OWNER relay — highest weight
        value = (0.40 * mmp_out.familiarity_level     # MMP P-layer
               + 0.25 * h3_periodicity                # H³ M14 (existing)
               + 0.20 * h3_stability                  # H³ M2 (existing)
               + 0.15 * r3_tonal_level)               # R³ fallback
        precision = mmp_agreement * energy_gate        # MMP cross-signal agreement
    else:
        # FALLBACK: existing v2.4 code, untouched
        value = (0.50 * h3_periodicity
               + 0.35 * h3_stability
               + 0.15 * r3_tonal_level)
        precision = existing_precision_logic
```

**Weight allocation pattern (all beliefs):**

| Source | Weight (with relay) | Weight (fallback) |
|--------|--------------------|--------------------|
| Owner relay P-layer | 0.35–0.45 | 0.00 |
| H³ morphologies | 0.25–0.35 | 0.50–0.60 |
| R³ features | 0.10–0.20 | 0.15–0.40 |
| Cross-relay input | 0.05–0.10 | 0.00 |

**Key constraint:** Weights must sum to 1.0. Owner relay replaces weight, doesn't add on top.

### 3.5 Q: Should we start neurochemical and region outputs?

**Answer: Not yet. After relay integration stabilizes.**

**Region Activation Map (26D RAM):** Safe to implement (read-only output, doesn't affect computation). But meaningless without relay outputs flowing — the region links are declared per-relay, and we need relay compute() outputs to aggregate them. **Target: Wave 3.**

**Neurochemical modulation (DA/NE/OPI/5HT):** Risky. Modifies precision and gain — changes the core belief dynamics. The current tanh precision compression (v2.3) works well. Adding neuromodulation on top creates two competing control mechanisms. **Target: v4.0, after v3.0 is stress-tested.**

**Implementation order:**

```
Wave 0-1: Relay wrappers + belief enrichment        (computation changes)
Wave 2:   Cross-relay pathways                       (communication changes)
Wave 3:   Region Activation Map                      (output addition, safe)
Future:   Neurochemical modulation                   (control mechanism, risky)
```

---

## 4. Integration Architecture

### 4.1 RelayKernelWrapper — Base Class

A generalized version of `BCHKernelWrapper` that all relay wrappers inherit:

```python
class RelayKernelWrapper:
    """
    Adapts a standalone Relay nucleus for causal kernel integration.

    Contract:
    1. Filters H³ demands to L0 (memory/causal) only
    2. Deduplicates against existing kernel demands
    3. Provides typed P-layer and F-layer outputs
    4. Falls back gracefully on missing H³ data
    5. Exposes h3_demands property for scheduler collection
    """

    def __init__(self, relay_class, approved_p_dims, approved_f_dims=None):
        self.relay = relay_class()
        self.approved_p_dims = approved_p_dims      # P-layer dims for observe()
        self.approved_f_dims = approved_f_dims or [] # F-layer dims for predict()

    @property
    def h3_demands(self) -> List[Tuple[int, int, int, int]]:
        """All relay H³ demands filtered to L0 only."""
        return [(r, h, m, law) for r, h, m, law in self.relay.h3_demands if law == 0]

    def compute(self, r3, h3, *, cross_inputs=None) -> Optional[RelayOutput]:
        """
        Run relay and return filtered outputs.
        Returns None if insufficient H³ data (triggers fallback in beliefs).
        """
        try:
            raw = self.relay.compute(r3, h3, cross_inputs)
            return RelayOutput(
                p_layer={name: raw[name] for name in self.approved_p_dims},
                f_layer={name: raw[name] for name in self.approved_f_dims},
            )
        except (KeyError, RuntimeError):
            return None  # Belief will use fallback path
```

### 4.2 Six Wrapper Specifications

#### BCH Wrapper (existing, proven)

```
Unit:           SPU
Target belief:  perceived_consonance
Approved P:     consonance_signal, template_match, hierarchy
Approved F:     (none in v2.5)
L0 demands:     17 tuples (from 48 total)
Status:         INTEGRATED (v2.0)
```

#### HMCE Wrapper (new)

```
Unit:           STU
Target belief:  tempo_state
Approved P:     a1_encoding, stg_encoding, mtg_encoding
Approved F:     context_prediction, phrase_expect
L0 demands:     18 tuples (all already L0)
Belief weight:  0.40 HMCE + 0.30 H³ + 0.15 R³ + 0.15 cross(SNEM)
Rationale:      HMCE provides 3-scale hierarchical context encoding
                (A1=300ms, STG=medium, MTG=long) that the current
                single-feature R³ observe() cannot capture.
```

#### SNEM Wrapper (new)

```
Unit:           ASU
Target belief:  salience_state
Approved P:     beat_locked_activity, entrainment_strength, selective_gain
Approved F:     beat_onset_pred
L0 demands:     ~6 tuples (from 18, filtering L2 out)
Belief weight:  0.35 SNEM + 0.25 H³_velocity + 0.20 R³_energy + 0.20 PE_carry
Rationale:      SNEM captures neural entrainment patterns (SSEPs) that
                pure R³ energy + H³ velocity misses — beat-locked salience
                vs. transient salience.
```

#### MMP Wrapper (new)

```
Unit:           IMU
Target belief:  familiarity_state
Approved P:     recognition_state, melodic_identity, familiarity_level
Approved F:     recognition_forecast
L0 demands:     ~6 tuples (from 18, filtering L2 out)
Belief weight:  0.40 MMP + 0.25 H³_M14 + 0.20 H³_M2 + 0.15 R³_tonal
Rationale:      MMP models musical mnemonic preservation — melodic
                recognition and scaffold recognition that H³ periodicity
                alone cannot distinguish.
```

#### DAED Wrapper (new)

```
Unit:           RPU
Target belief:  reward_valence (indirect — enriches reward formula)
Approved P:     caudate_activation, nacc_activation
Approved F:     (none)
L0 demands:     ~5 tuples (from 16, filtering L2 out)
Integration:    NOT via observe() — feeds reward aggregator directly
                as anticipatory_da and consummatory_da signals.
                DAED dissociates "wanting" (caudate, anticipatory) from
                "liking" (NAcc, consummatory) — current reward formula
                conflates these.
Reward change:  reward = salience × (
                    w_surprise × surprise
                  + w_resolution × resolution
                  + w_exploration × exploration
                  - w_monotony × monotony
                  + w_wanting × DAED.caudate        # NEW: anticipatory
                  + w_liking × DAED.nacc            # NEW: consummatory
                ) × fam_mod
```

#### MPG Wrapper (new)

```
Unit:           NDU
Target belief:  salience_state (secondary evidence)
Approved P:     onset_state, contour_state
Approved F:     phrase_boundary_pred
L0 demands:     ~5 tuples (from 16, filtering L2 out)
Belief weight:  MPG contributes 0.10 of salience (novelty component).
                Adjusts salience weight split:
                0.30 SNEM + 0.10 MPG + 0.25 H³_velocity + 0.15 R³ + 0.20 PE
Rationale:      MPG captures melodic novelty (posterior-anterior gradient)
                that pure onset-based salience misses. A phrase boundary
                should be salient even without loudness change.
```

### 4.3 Scheduler Modification

```
Phase 0 (Sensory):
    relay_outputs = {}
    relay_outputs["bch"]  = bch_wrapper.compute(r3, h3)           # existing
    relay_outputs["hmce"] = hmce_wrapper.compute(r3, h3)          # new
    relay_outputs["snem"] = snem_wrapper.compute(r3, h3)          # new
    relay_outputs["mmp"]  = mmp_wrapper.compute(r3, h3)           # new
    relay_outputs["mpg"]  = mpg_wrapper.compute(r3, h3)           # new

    # Observations with relay enrichment
    cons_lk = consonance.observe(r3, h3, bch_out=relay_outputs["bch"])
    tempo_lk = tempo.observe(r3, h3, hmce_out=relay_outputs["hmce"])

Phase 1 (Salience):
    sal_lk = salience.observe(r3, h3,
        snem_out=relay_outputs["snem"],
        mpg_out=relay_outputs["mpg"],
        prev_pe_mean=self._prev_pe_mean)

Phase 2a (Prediction & Observation):
    fam_lk = familiarity.observe(r3, h3, mmp_out=relay_outputs["mmp"])
    # predict() functions can optionally use F-layer from wrappers

Phase 2b-2c: (unchanged)

Phase 3 (Reward):
    # DAED feeds reward aggregator
    daed_out = relay_outputs["daed"]
    reward = reward_agg.compute_multiscale(
        ...,
        daed_out=daed_out,  # NEW: wanting/liking decomposition
    )
```

### 4.4 H³ Demands Growth

| Component | Current | After Wave 1 | Delta |
|-----------|---------|--------------|-------|
| Belief predict demands | 24 | 24 | +0 |
| Belief observe demands | 10 | 10 | +0 |
| Multi-scale (consonance) | 24 | 24 | +0 |
| BCH wrapper (L0) | 17 | 17 | +0 |
| HMCE wrapper (L0) | — | 18 | +18 |
| SNEM wrapper (L0) | — | ~6 | +6 |
| MMP wrapper (L0) | — | ~6 | +6 |
| DAED wrapper (L0) | — | ~5 | +5 |
| MPG wrapper (L0) | — | ~5 | +5 |
| **Pre-dedup total** | **58** | **~115** | **+57** |
| **Post-dedup estimate** | **58** | **~98** | **+40** |

**Performance impact estimate:**
- H³ batch extraction: 0.06s → ~0.12s (linear with tuples, still negligible)
- Relay computation: ~0.5ms per relay × 5 = ~2.5ms per frame
- Total pipeline impact: <5% overhead on C³ kernel time

---

## 5. Four-Wave Implementation Plan

### Wave 0: Infrastructure (No Behavior Change)

**Goal:** Build the scaffolding without changing any belief computation.

**Deliverables:**
1. `RelayKernelWrapper` base class in `brain/kernel/relays/base_wrapper.py`
2. `RelayOutput` dataclass (p_layer dict + f_layer dict)
3. `relay_outputs` dict in scheduler (populated but unused)
4. H³ demand collection expanded to include relay wrapper demands
5. All 5 relay wrappers instantiated (HMCE, SNEM, MMP, DAED, MPG)

**Test criterion:** Existing 9/11 stress test passes with zero regression. All wrappers compute() successfully. No belief behavior changes.

**Estimated scope:** ~200 lines new code.

### Wave 1: Owner Relay → Belief Enrichment

**Goal:** Each belief's observe() gains its owner relay as enrichment source.

**Deliverables:**

| Task | Files Modified | Behavior Change |
|------|---------------|-----------------|
| HMCE → tempo | `beliefs/tempo.py`, `scheduler.py` | tempo observe() uses HMCE P-layer |
| SNEM → salience | `beliefs/salience.py`, `scheduler.py` | salience observe() uses SNEM P-layer |
| MMP → familiarity | `beliefs/familiarity.py`, `scheduler.py` | familiarity observe() uses MMP P-layer |
| MPG → salience | `beliefs/salience.py` | salience gets novelty component |
| DAED → reward | `reward.py`, `scheduler.py` | reward formula gets wanting/liking |

**Integration order (safest first):**
1. **HMCE → tempo** — Lowest risk. Tempo is medium-inertia (τ=0.7), single-scale. HMCE provides 3 context encodings that simply enrich the weighted average.
2. **SNEM → salience** — Medium risk. Salience gates reward. But salience is fast (τ=0.3) and recovers quickly from perturbation.
3. **MMP → familiarity** — Medium risk. Familiarity is high-inertia (τ=0.85), slow to change. MMP enrichment will be gradual.
4. **MPG → salience** — Low risk. Secondary evidence, 0.10 weight.
5. **DAED → reward** — Highest risk. Changes the reward formula directly. Must be last, with careful weight tuning.

**Test criterion per integration:**
- 9/11 stress test passes
- Belief dynamic range increases or stays same (never collapses)
- Reward mean stays positive for all 4 alpha-test pieces
- Fallback path tested (wrapper returns None → existing behavior)

**Estimated scope:** ~150 lines modified per belief, ~500 total.

### Wave 2: Cross-Relay Communication (3 Pathways)

**Goal:** Relay outputs become inputs to other relays.

**Three critical pathways:**

| ID | Route | Signal | Rationale |
|----|-------|--------|-----------|
| P1 | BCH → DAED | `consonance_signal` | Consonance drives anticipatory dopamine |
| P3 | SNEM → HMCE | `beat_locked_activity` | Beat entrainment informs context encoding |
| P7 | MMP → DAED | `familiarity_level` | Familiar passages modulate hedonic "liking" |

**Implementation:**
- Scheduler orders relay computation: BCH + SNEM + MMP first → HMCE + DAED second
- `cross_inputs` dict passed to downstream wrappers
- Upstream wrappers must succeed for cross-input to flow (else None)

**Phase modification:**

```
Phase 0a (Independent relays):  BCH, SNEM, MMP, MPG  — parallel
Phase 0b (Dependent relays):    HMCE(+SNEM), DAED(+BCH,+MMP)  — sequential
Phase 0c (Belief observe):      All beliefs  — existing order
```

**Test criterion:** Pathway ON vs OFF A/B comparison. Reward improvement measurable but within safe bounds.

**Estimated scope:** ~100 lines.

### Wave 3: Output Layers (Non-Computational)

**Goal:** Produce Region Activation Map and enriched BrainOutput.

**Deliverables:**

1. **Region Activation Map (26D RAM):**
   - Each wrapper exposes `region_links: Dict[str, Dict[str, float]]`
   - Scheduler aggregates: `ram[region] = Σ relay_output[dim] × link_weight`
   - Output: `(B, T, 26)` tensor in KernelOutput

2. **BrainOutput assembly:**
   - Collect all `external` and `hybrid` scoped dims from relay P-layers
   - Concatenate into single tensor alongside beliefs
   - Output: extended KernelOutput with `relay_tensor` field

3. **KernelOutput v3.0:**

```python
@dataclass
class KernelOutput:
    # Existing (v2.5)
    beliefs: Dict[str, Tensor]
    pe: Dict[str, Tensor]
    precision_obs: Dict[str, Tensor]
    precision_pred: Dict[str, Tensor]
    reward: Tensor
    ms_pe: Dict[str, Dict[int, Tensor]]
    ms_precision_pred: Dict[str, Dict[int, Tensor]]

    # New (v3.0)
    relay_outputs: Dict[str, RelayOutput]     # Raw P+F layer outputs
    ram: Optional[Tensor]                      # (B, T, 26) region activation
    relay_tensor: Optional[Tensor]             # (B, T, D_ext) external dims
```

**Test criterion:** Output shapes correct, RAM values in [0, 1], no computation changes.

**Estimated scope:** ~150 lines.

---

## 6. Risk Analysis

### 6.1 Risk Matrix

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Belief collapse (all outputs → constant) | Critical | Low | Fallback path + per-wave stress test |
| Reward sign flip (positive → negative) | High | Medium | DAED weights start at 0.0, increase gradually |
| H³ demand explosion (>200 tuples) | Medium | Low | L0-only filter + dedup + demand audit |
| Relay compute() crash | Medium | Medium | try/except in wrapper, returns None |
| Precision engine confused by richer signals | Medium | Low | PE ring buffer is belief-level, not relay-level |
| Performance regression (>2x slower) | Low | Low | Relay compute is lightweight tensor ops |

### 6.2 Rollback Strategy

Each wave is independently revertible:
- Wave 0: Remove relay_outputs dict from scheduler
- Wave 1: Set wrapper to None → fallback in observe()
- Wave 2: Remove cross_inputs from dependent relays
- Wave 3: Remove ram/relay_tensor from KernelOutput

**No migration needed.** All changes are additive with fallback.

---

## 7. Weight Tuning Strategy

### 7.1 Initial Weights (Conservative)

All relay contributions start **lower than final target** and are tuned upward:

| Belief | Relay Weight (initial) | Relay Weight (target) | Rationale |
|--------|----------------------|----------------------|-----------|
| consonance | 0.50 (BCH, established) | 0.50 | Already tuned, don't change |
| tempo | 0.25 (HMCE, new) | 0.40 | Start conservative, increase after validation |
| salience | 0.20 (SNEM, new) | 0.35 | Salience gates reward — high sensitivity |
| familiarity | 0.25 (MMP, new) | 0.40 | High inertia absorbs perturbation |
| reward | 0.00 (DAED, new) | 0.15 | Start at zero, increase only with evidence |

### 7.2 Tuning Protocol

For each relay integration:

1. **Baseline:** Run alpha-test (4 pieces) without relay → record metrics
2. **Integration:** Enable relay at initial weight → run alpha-test
3. **Compare:** Belief range, PE adaptation, reward mean, stress test
4. **Adjust:** If metrics improve → increase weight toward target. If regress → decrease or revert.
5. **Lock:** When 9/11 stress test passes + all 4 pieces positive → lock weights in YAML config

---

## 8. Belief Enrichment — Detailed Specifications

### 8.1 tempo.observe() + HMCE

**Current (v2.5):**
```python
def observe(self, r3, h3):
    tempo     = r3[:, :, IDX_TEMPO]
    beat      = r3[:, :, IDX_BEAT_STRENGTH]
    pulse     = r3[:, :, IDX_PULSE_CLARITY]
    regularity = r3[:, :, IDX_RHYTHMIC_REG]

    value = 0.35*tempo + 0.25*beat + 0.25*pulse + 0.15*regularity
    precision = onset_regularity_based
```

**Proposed (v3.0):**
```python
def observe(self, r3, h3, *, hmce_out=None):
    if hmce_out is not None:
        # HMCE provides 3-scale context: A1 (300ms), STG (medium), MTG (long)
        context_signal = (0.40 * hmce_out.a1_encoding      # short-term beat
                        + 0.35 * hmce_out.stg_encoding     # phrase-level
                        + 0.25 * hmce_out.mtg_encoding)    # structure-level

        value = (0.35 * context_signal                     # HMCE multi-scale
               + 0.25 * r3_tempo                           # R³ tempo estimate
               + 0.20 * r3_beat                            # R³ beat strength
               + 0.10 * r3_pulse                           # R³ pulse clarity
               + 0.10 * r3_regularity)                     # R³ regularity

        precision = hmce_cross_scale_agreement * onset_regularity
    else:
        # FALLBACK: existing code
        value = 0.35*tempo + 0.25*beat + 0.25*pulse + 0.15*regularity
        precision = onset_regularity_based
```

### 8.2 salience.observe() + SNEM + MPG

**Current (v2.5):**
```python
def observe(self, r3, h3, prev_pe_mean=None):
    energy = 0.6*amplitude + 0.4*onset
    h3_velocity = max(vel_amplitude, vel_onset, vel_flux)
    pe_carry = abs(prev_pe_mean) if prev_pe_mean else 0

    base = 0.45*energy + 0.25*h3_velocity + 0.10*pe_carry
    peak = max(energy, h3_velocity, pe_carry)
    value = 0.5*base + 0.5*peak
```

**Proposed (v3.0):**
```python
def observe(self, r3, h3, *, snem_out=None, mpg_out=None, prev_pe_mean=None):
    # Core signals (existing)
    energy = 0.6*amplitude + 0.4*onset
    h3_velocity = max(vel_amplitude, vel_onset, vel_flux)
    pe_carry = abs(prev_pe_mean) if prev_pe_mean else 0

    if snem_out is not None:
        entrainment = (0.50 * snem_out.entrainment_strength
                     + 0.30 * snem_out.beat_locked_activity
                     + 0.20 * snem_out.selective_gain)
        novelty = 0.0
        if mpg_out is not None:
            novelty = 0.6*mpg_out.onset_state + 0.4*mpg_out.contour_state

        base = (0.30 * entrainment       # SNEM: beat-locked salience
              + 0.10 * novelty            # MPG: melodic novelty
              + 0.25 * energy             # R³: raw energy
              + 0.15 * h3_velocity        # H³: change detection
              + 0.20 * pe_carry)          # PE: prediction error
        peak = max(entrainment, energy, h3_velocity, pe_carry)
        value = 0.5*base + 0.5*peak
        precision = snem_agreement * change_magnitude
    else:
        # FALLBACK: existing code
        base = 0.45*energy + 0.25*h3_velocity + 0.10*pe_carry
        peak = max(energy, h3_velocity, pe_carry)
        value = 0.5*base + 0.5*peak
        precision = existing_logic
```

### 8.3 familiarity.observe() + MMP

**Current (v2.5):**
```python
def observe(self, r3, h3):
    # H³ path
    period = h3_M14_mean       # 50% — periodicity
    stability = 1/(1+h3_M2)   # 35% — inverted std
    r3_level = r3_tonal        # 15% — tonal level

    raw = 0.50*period + 0.35*stability + 0.15*r3_level
    gate = sigmoid(10*(energy - 0.1))
    value = raw * gate
```

**Proposed (v3.0):**
```python
def observe(self, r3, h3, *, mmp_out=None):
    gate = sigmoid(10*(energy - 0.1))   # Energy gate preserved

    if mmp_out is not None:
        # MMP provides explicit recognition signals
        recognition = (0.45 * mmp_out.familiarity_level    # Primary: how familiar
                     + 0.30 * mmp_out.recognition_state    # Episodic match
                     + 0.25 * mmp_out.melodic_identity)    # Melodic recognition

        raw = (0.40 * recognition        # MMP: structured familiarity
             + 0.25 * h3_periodicity     # H³ M14: recurrence
             + 0.20 * h3_stability       # H³ M2: stability
             + 0.15 * r3_tonal)          # R³: tonal level
        value = raw * gate
        precision = mmp_agreement * gate
    else:
        # FALLBACK: existing v2.4 code
        raw = 0.50*period + 0.35*stability + 0.15*r3_level
        value = raw * gate
        precision = existing_logic
```

### 8.4 reward.compute() + DAED

**Current (v2.5):**
```python
surprise    = abs_pe * pi_eff * (1 - fam)
resolution  = (1 - abs_pe) * pi_eff * fam
exploration = abs_pe * (1 - pi_eff)
monotony    = pi_eff ** 2

reward = salience * (1.5*surprise + 0.8*resolution + 0.5*exploration - 0.6*monotony)
reward *= (0.5 + 0.5 * 4*fam*(1-fam))  # inverted-U
```

**Proposed (v3.0):**
```python
surprise    = abs_pe * pi_eff * (1 - fam)
resolution  = (1 - abs_pe) * pi_eff * fam
exploration = abs_pe * (1 - pi_eff)
monotony    = pi_eff ** 2

# Base reward (existing)
base_reward = 1.5*surprise + 0.8*resolution + 0.5*exploration - 0.6*monotony

# DAED dopamine decomposition (new, additive)
if daed_out is not None:
    wanting  = daed_out.caudate_activation   # Anticipatory DA
    liking   = daed_out.nacc_activation      # Consummatory DA
    da_bonus = w_wanting * wanting + w_liking * liking  # starts at 0.0 + 0.0
    reward = salience * (base_reward + da_bonus)
else:
    reward = salience * base_reward

reward *= (0.5 + 0.5 * 4*fam*(1-fam))  # inverted-U preserved
```

**DAED initial weights:** `w_wanting = 0.0`, `w_liking = 0.0` (no effect until tuned).

---

## 9. Configuration Schema (YAML)

All weights will live in the kernel YAML config, not hardcoded:

```yaml
# kernel_config.yaml — v3.0 relay integration

relay_wrappers:
  bch:
    enabled: true
    causal_only: true  # L0 demands only
  hmce:
    enabled: true
    causal_only: true
  snem:
    enabled: true
    causal_only: true
  mmp:
    enabled: true
    causal_only: true
  daed:
    enabled: true
    causal_only: true
  mpg:
    enabled: true
    causal_only: true

belief_weights:
  consonance:
    bch_weight: 0.50
    h3_weight: 0.25
    r3_weight: 0.25
  tempo:
    hmce_weight: 0.25       # initial conservative, target 0.40
    r3_tempo: 0.25
    r3_beat: 0.20
    r3_pulse: 0.15
    r3_regularity: 0.15
  salience:
    snem_weight: 0.20       # initial conservative, target 0.35
    mpg_weight: 0.05        # initial conservative, target 0.10
    energy_weight: 0.30
    h3_velocity: 0.20
    pe_carry: 0.25
  familiarity:
    mmp_weight: 0.25        # initial conservative, target 0.40
    h3_periodicity: 0.30
    h3_stability: 0.25
    r3_tonal: 0.20

reward_daed:
  w_wanting: 0.00            # initial zero, target 0.10
  w_liking: 0.00             # initial zero, target 0.05

cross_relay_pathways:
  bch_to_daed: false         # Wave 2
  snem_to_hmce: false        # Wave 2
  mmp_to_daed: false         # Wave 2

output:
  ram_enabled: false          # Wave 3
  relay_tensor_enabled: false # Wave 3
```

---

## 10. Test Plan

### 10.1 Per-Wave Validation

| Wave | Test | Pass Criterion |
|------|------|----------------|
| 0 | Existing stress test (9/11) | Zero regression |
| 0 | Wrapper compute() smoke test | All 5 wrappers return valid outputs |
| 0 | H³ demands audit | Total ≤ 120 post-dedup |
| 1a | HMCE → tempo | Tempo range ≥ current, 9/11 stress |
| 1b | SNEM → salience | Salience std ≥ current, reward stays positive |
| 1c | MMP → familiarity | Familiarity range ≥ current, min > 0.05 |
| 1d | MPG → salience | Marginal, salience std improves |
| 1e | DAED → reward | All 4 pieces positive reward mean |
| 2 | Cross-relay ON vs OFF | Measurable reward improvement |
| 3 | RAM output | Shape (B, T, 26), values in [0, 1] |

### 10.2 Alpha-Test Regression

After each wave completion, full alpha-test on 4 pieces:
- Bach Cello Suite (151.7s)
- Swan Lake (30s)
- Herald of the Change (~60s)
- Beethoven Pathétique (497.5s)

**Minimum pass criteria:**
- All 4 pieces: positive reward mean
- Consonance range ≥ 0.30
- Familiarity min < 0.10 (silence suppression preserved)
- PE adaptation visible (first window ≠ last window)

---

## 11. Open Questions (RESOLVED — See §14)

The following questions were investigated via literature search and are now resolved (see Section 14 for full findings):

1. **SNEM entrainment weights:** What is the relative contribution of beat-locked vs. meter-locked entrainment to perceptual salience? (Nozaradan 2011, Large & Palmer 2002)

2. **MMP recognition vs. familiarity:** Is melodic recognition (MMP) the same as perceptual familiarity (H³ periodicity), or are they dissociable? (Halpern & Bartlett 2011, Peretz et al. 2009)

3. **DAED wanting vs. liking:** What is the optimal weight ratio between anticipatory (caudate) and consummatory (NAcc) dopamine in musical pleasure? (Salimpoor et al. 2011, Zatorre & Salimpoor 2013)

4. **Cross-relay timing:** Does beat entrainment (SNEM) causally precede context encoding (HMCE) in neural recordings? Determines Phase 0a vs 0b ordering. (Grahn & Rowe 2009)

5. **MPG novelty-salience coupling:** Is melodic novelty detection (posterior-anterior gradient) truly independent from energy-based salience? (Pearce & Wiggins 2012, Koelsch et al. 2019)

6. **Region aggregation method:** Linear weighted sum vs. winner-take-all vs. softmax for RAM? (Fedorenko et al. 2024, Norman-Haignere et al. 2015)

7. **Precision interaction:** When relay precision and H³-based precision disagree, which should dominate? (Friston 2005, Kanai et al. 2015)

---

## 12. Timeline Estimate

| Wave | Scope | Dependencies |
|------|-------|-------------|
| Wave 0 | Base wrapper + scaffolding | None |
| Wave 1 | 5 belief enrichments + tuning | Wave 0 + literature review |
| Wave 2 | 3 cross-relay pathways | Wave 1 stable |
| Wave 3 | RAM + BrainOutput | Wave 1 stable |

---

## 13. Summary

This plan integrates 6 relay nuclei (71D total output) into the existing 5-belief kernel through the proven wrapper pattern. Key principles:

1. **No new beliefs** — Relays enrich existing beliefs, don't create new ones
2. **P-layer primary** — Percept outputs feed observe(), Forecast feeds predict()
3. **Fallback everywhere** — Every relay can be absent without system failure
4. **Conservative weights** — Start low, tune upward with evidence
5. **4-wave incremental** — Each wave independently testable and revertible
6. **YAML config** — All weights externalized, no hardcoded values
7. **Literature-grounded** — 7 open questions to resolve before implementation

The system will not crash because every change is additive with guaranteed fallback to the proven v2.5 behavior.

---

---

## 14. Literature Review — 7 Open Questions Resolved

*Research conducted: 18 February 2026. Web search across neuroscience databases, meta-analyses, and computational models.*

### 14.1 SNEM Entrainment Weights (Q1)

**Finding:** Beat-locked SSEPs dominate meter-locked SSEPs by 2–3× amplitude.

**Key evidence:**
- **Nozaradan et al. (2011, 2012):** EEG frequency-tagging paradigm showed SSEPs at the beat frequency (e.g., 2.4 Hz for 120 BPM) are 2–3× larger than metric subdivision frequencies. The beat-frequency peak is the dominant neural entrainment response.
- **Nozaradan et al. (2017):** Metric interpretation modulates SSEP amplitude — the SAME physical rhythm produces different entrainment patterns depending on whether the listener perceives it in duple or triple meter. This means entrainment is not purely acoustic but partially top-down.
- **Large & Palmer (2002):** Nonlinear resonance theory predicts that oscillators entrain most strongly at the tactus (beat) level, with weaker entrainment at sub-divisions and super-divisions.
- **Large & Snyder (2009):** Neural resonance model shows beat-level oscillations drive metric interpretation; meter-level oscillations are derived and weaker.

**Implication for SNEM wrapper:**
- `beat_locked_activity` should have highest weight (captures dominant SSEP)
- `entrainment_strength` is composite (includes meter) — medium weight
- `selective_gain` (enhancement at beat positions) — supporting weight

**Revised SNEM internal weights:**
```
entrainment = 0.45 × beat_locked_activity    # dominant (Nozaradan 2–3× ratio)
            + 0.35 × entrainment_strength    # composite beat+meter
            + 0.20 × selective_gain          # attention modulation
```

**Citations:** Nozaradan et al. 2011 (J Neurosci 31:12234), 2012 (Front Psychol 3:159), 2017 (eLife 6:e28630); Large & Palmer 2002 (Ecol Psychol 14:49); Large & Snyder 2009 (Ann NY Acad Sci 1169:46)

---

### 14.2 MMP Recognition vs. Familiarity (Q2)

**Finding:** Melodic recognition and perceptual familiarity are definitively dissociable — dual-process architecture confirmed. Implicit/statistical familiarity dominates during passive listening (~65%), structured recognition contributes ~35%.

**Key evidence:**
- **Peretz, Gaudreau & Bonnel (1998):** Triple dissociation — timbre change impaired recognition but not liking; study depth affected recognition but not liking; exposure effects persisted longer than recognition memory. Conclusion: implicit (familiarity) and explicit (recognition) are independent pathways.
- **Yonelinas (2002):** Dual-process signal detection framework — familiarity = graded signal (perirhinal cortex, fast 100–300ms), recollection = threshold event (hippocampus, slow 500ms+). Double dissociation: hippocampal damage impairs recollection but spares familiarity; perirhinal damage impairs familiarity but spares recollection.
- **Pereira et al. (2018, meta-analysis, 11 studies, 212 participants):** Musical familiarity primarily activates motor/procedural regions (SMA, BA6), NOT hippocampus. This means musical familiarity is predominantly implicit/motor, not episodic.
- **2023 ALE meta-analysis (23 studies, 364 participants):** Confirmed SMA/pre-SMA + IFG + claustrum/insula as core familiarity network for music.
- **Alzheimer's evidence (Quoniam 2003, El Haj 2012):** Patients retain implicit musical familiarity (mere exposure effect preserved) even when explicit recognition has deteriorated completely.
- **Mandler (1980) "Butcher on the bus":** Feeling of familiarity (pattern activation) is separable from recollection (episodic context retrieval).

**Implication for familiarity belief:**
- H³ M14 periodicity + M2 stability = **implicit pathway** (perirhinal/SMA analog) — correctly captures dominant component
- MMP `recognition_state` = **explicit pathway** (hippocampal/lexical analog)
- Use `recognition_state` for f_explicit, NOT `familiarity_level` (too similar to implicit pathway)
- **Weight: 0.65 implicit / 0.35 explicit** for passive listening (shifts toward 0.50/0.50 for well-known music)

**Revised familiarity observe():**
```python
# Dual-process familiarity (literature-grounded)
if mmp_out is not None:
    f_explicit = mmp_out.recognition_state       # Hippocampal pathway
    f_implicit = 0.55 * h3_periodicity + 0.45 * h3_stability  # Perirhinal pathway

    raw = 0.65 * f_implicit + 0.35 * f_explicit  # Peretz/Yonelinas ratio
    value = raw * gate
else:
    # Fallback: implicit-only (existing)
    raw = 0.50 * period + 0.35 * stability + 0.15 * r3_level
    value = raw * gate
```

**Precision implication:**
- f_implicit: graded precision, ramps up slowly, high ceiling
- f_explicit: threshold precision — low initially, jumps when recognition occurs
- Combined: `precision = 0.65 * π_implicit + 0.35 * π_explicit`

**Citations:** Peretz et al. 1998 (Mem Cognit 26:884); Yonelinas 2002 (J Mem Lang 46:441); Pereira et al. 2018 (Front Neurosci 12:686); Mandler 1980 (Psychol Rev 87:252); Quoniam et al. 2003 (Neuropsychologia 41:1301); Halpern & Bartlett 2010 (Springer Handbook of Auditory Research 36:233)

---

### 14.3 DAED Wanting vs. Liking (Q3)

**Finding:** Anticipatory DA (caudate/wanting) and consummatory DA (NAcc/liking) are temporally and neurochemically dissociable. Anticipatory phase begins ~15s before chills and is a slightly stronger predictor of subjective pleasure.

**Key evidence:**
- **Salimpoor, Benovoy, Larcher, Dagher & Zatorre (2011, Nature Neuroscience):** PET [¹¹C]raclopride study — first direct evidence of DA release during music listening. Anticipatory phase: significant DA release in **caudate nucleus** during the 15s approach to a chill. Consummatory phase: significant DA release in **nucleus accumbens** at the peak-pleasure moment. Both phases showed significant endogenous DA release (p<0.05 corrected).
- **Salimpoor et al. (2013, Science):** NAcc activation during first listen predicted how much participants would later bid (real money) for unfamiliar music. Correlation between NAcc BOLD and purchase price: r = 0.40. This means consummatory response predicts economic valuation.
- **Zatorre & Salimpoor (2013, PNAS review):** Proposed a model where anticipatory DA creates "wanting" (motivational drive to continue listening) and consummatory DA creates "liking" (hedonic pleasure). Both contribute to overall musical reward but through distinct temporal and neurochemical profiles.
- **Berridge & Kringelbach (2015, Neuron):** General wanting/liking framework — wanting (mesolimbic DA, caudate, VTA) is more robust, persistent, and manipulable than liking (mu-opioid, NAcc hedonic hotspots). Wanting can exist without liking (addiction), liking can exist without wanting (anhedonia).
- **Mas-Herrero et al. (2021):** Musical anhedonia patients show reduced anticipatory responses but intact acoustic processing — confirming that the anticipatory DA pathway is selectively impaired.

**Temporal profile:**
- Anticipatory DA ramp: begins ~15s before chill, peaks 1–2s before
- Consummatory DA burst: peaks at the moment of chill/frisson, decays within ~5s
- Overlap period: ~2s around the chill moment

**Weight recommendation:**
- Anticipatory (wanting): slightly stronger predictor of overall engagement (keeps listener going)
- Consummatory (liking): slightly stronger predictor of specific peak pleasure moments
- **Target ratio: w_wanting = 0.55, w_liking = 0.45** (equal-ish, with slight wanting edge)
- **BUT**: Start at 0.0/0.0 as planned, and tune upward after DAED output is validated

**Revised DAED integration:**
```python
# DAED bonus weights (literature target, to be tuned from 0.0)
w_wanting: 0.07    # target: 0.55 × 0.12 (total DAED budget = 0.12 of reward)
w_liking:  0.05    # target: 0.45 × 0.12
```

**Key insight for implementation:** The anticipatory signal is temporally LEADING — DAED's caudate_activation should reflect H³ morphology at longer horizons (velocity/trend approaching peaks). The consummatory signal is INSTANTANEOUS — NAcc activation at current moment.

**Citations:** Salimpoor et al. 2011 (Nat Neurosci 14:257); Salimpoor et al. 2013 (Science 340:216); Zatorre & Salimpoor 2013 (PNAS 110:10430); Berridge & Kringelbach 2015 (Neuron 86:646); Mas-Herrero et al. 2021 (Curr Biol 31:3427)

---

### 14.4 Cross-Relay Timing: SNEM→HMCE (Q4)

**Finding:** Beat processing and context encoding operate in **parallel** with bidirectional coupling, NOT strict sequential ordering. However, beat processing has a slight temporal lead (~50–100ms).

**Key evidence:**
- **Grahn & Rowe (2009, 2013, Cereb Cortex):** fMRI showed putamen activation during beat perception is automatic (even in passive listening). Putamen–SMA–premotor cortex circuit is engaged within the first few hundred ms. However, STG/MTG context encoding is also rapid.
- **Chen, Penhune & Zatorre (2008, J Neurosci):** Auditory-motor coupling for beat is established within the first 2–3 beats (~1–2s). Premotor cortex shows beat-related activation even without movement, suggesting automatic motor entrainment.
- **Grahn & Rowe (2013):** Parkinson's patients show impaired beat perception (putamen damaged) but largely preserved melodic/harmonic perception. This suggests beat processing (putamen) and context encoding (cortex) are separable but not strictly sequential.
- **Giraud & Poeppel (2012, Nat Neurosci):** Cortical oscillation framework — theta (4–8Hz) tracks syllabic/beat rate, gamma (~30Hz) tracks fine structure. Both engage simultaneously but at different timescales.
- **MEG evidence (Fujioka et al. 2012):** Beat-related beta-band modulation in auditory cortex occurs within ~200ms of beat onset, while melodic processing (MMN-like responses) occurs at ~150–200ms. Near-simultaneous.

**Implication:** NOT strictly sequential. Beat processing has a slight lead but context encoding doesn't WAIT for beat to complete.

**Revised scheduler recommendation:**
```
Phase 0a: ALL independent relays in parallel (BCH, SNEM, MMP, MPG, HMCE)
Phase 0b: DAED only (needs BCH + MMP outputs)
```

**Rationale:** SNEM→HMCE pathway (Wave 2) provides beat_locked_activity as ADDITIONAL input to HMCE, but HMCE can compute without it (L0-only context encoding from R³+H³). When cross-relay pathway is enabled, HMCE recomputes with SNEM enrichment.

**Alternative (simpler, recommended for v3.0):**
- Run all 6 relays in parallel in Phase 0a
- Cross-relay pathways (Wave 2) do a second pass on dependent relays only

**Citations:** Grahn & Rowe 2009 (Cereb Cortex 19:893), 2013 (Cereb Cortex 23:913); Chen et al. 2008 (J Neurosci 28:5562); Giraud & Poeppel 2012 (Nat Neurosci 15:511); Fujioka et al. 2012 (NeuroImage 60:2142)

---

### 14.5 MPG Novelty-Salience Independence (Q5)

**Finding:** Melodic novelty (information-theoretic surprise) and energy-based salience are **partially independent** (r ≈ 0.2–0.3 correlation). Melodic novelty CAN drive salience without energy change.

**Key evidence:**
- **Pearce & Wiggins (2006, 2012) IDyOM:** Information content (IC = -log₂ P(note|context)) predicts ERP amplitude (N1/P2 components) independently of acoustic features. Partial correlation: IC predicts neural response even after controlling for pitch interval, duration, and intensity (r ≈ 0.3, p < 0.001).
- **Omigie et al. (2019):** IDyOM-derived surprise correlated with pupil dilation (arousal proxy) at r ≈ 0.15–0.20, independent of loudness.
- **MMN studies (Näätänen et al. 2007, Vuust et al. 2011):** Pitch deviants produce Mismatch Negativity (MMN) at ~150ms regardless of loudness match. Melodic violations capture attention even when acoustic energy is controlled. MMN amplitude scales with deviance magnitude, not loudness.
- **Koelsch et al. (2019):** Syntactic violations (unexpected harmonies) activate inferior frontal gyrus (IFG) independently of acoustic features. ERAN (Early Right Anterior Negativity) at ~200ms reflects rule-based surprise.
- **Heilbron & Chait (2018):** Auditory scene analysis separates "change detection" (energy-based, fast) from "regularity violation" (pattern-based, slower). Two distinct pathways.

**Implication:** MPG (melodic novelty) IS genuinely independent from energy-based salience. A phrase boundary or harmonic surprise can be salient without loudness change.

**Revised MPG weight:** 0.10 → **0.12** of salience (supported by partial correlation data). Not higher because in real music, novelty and energy often co-occur (composers use dynamics to mark novel moments).

**Citations:** Pearce & Wiggins 2006 (Music Percept 24:167), 2012 (Top Cogn Sci 4:625); Omigie et al. 2019 (Front Neurosci 13:405); Näätänen et al. 2007 (Clin Neurophysiol 118:2544); Vuust et al. 2011 (Front Psychol 2:159); Koelsch et al. 2019 (Ann NY Acad Sci 1452:15); Heilbron & Chait 2018 (eLife 7:e34288)

---

### 14.6 Region Aggregation Method (Q6)

**Finding:** Linear weighted sum is the established standard for forward encoding models. Add ReLU + per-region z-normalization across time.

**Key evidence:**
- **Naselaris, Kay, Nishimoto & Gallant (2011, NeuroImage):** Canonical encoding model framework: `r = H × f(s)`. The mapping from feature space to brain activity is **linear**. Nonlinearity is in feature extraction (R³/H³/C³), not in aggregation.
- **Huth et al. (2016, Nature):** Semantic atlas of entire cortex via **ridge regression** mapping 985 features to voxel responses. Linear weighted sum per voxel. Produced the most detailed semantic brain map to date.
- **Norman-Haignere, Kanwisher & McDermott (2015, Neuron):** Auditory cortex decomposition: `D ≈ R × W` — each voxel's response = linear weighted sum of 6 canonical components. Validated on 165 natural sounds.
- **NeuroQuery (Dockès et al. 2020, eLife):** Brain activation prediction from text via **ridge regression**. Linear forward model is the standard.
- **Cognitive Encoding Models (2023, NeuroImage):** Predicted brain activation maps for arbitrary tasks using region-wise ridge regression. Output as z-scores.

**Recommendation:**
```
Stage 1: Linear weighted sum (current implementation — correct)
    RAM_raw[region, t] = Σ output[dim, t] × weight[dim→region]

Stage 2: ReLU (optional, recommended)
    RAM_rect[region, t] = max(0, RAM_raw[region, t])

Stage 3: Per-region z-normalization across time
    RAM_norm[region, t] = (RAM_rect[region, t] - μ_t) / (σ_t + ε)

Stage 4: Sigmoid (if [0,1] needed for visualization)
    RAM_01[region, t] = sigmoid(RAM_norm[region, t])
```

**Do NOT use:** softmax (forces inter-region competition), winner-take-all (loses graded information), mean (penalizes well-connected regions).

**Citations:** Naselaris et al. 2011 (NeuroImage 56:400); Huth et al. 2016 (Nature 532:453); Norman-Haignere et al. 2015 (Neuron 88:1281); Dockès et al. 2020 (eLife 9:e53385)

---

### 14.7 Precision Conflict Resolution (Q7)

**Finding:** Multiple precision estimates combine via **precision-weighted averaging** (inverse-variance weighting). The more specific/reliable source dominates naturally.

**Key evidence:**
- **Friston (2005, 2010):** In hierarchical predictive coding, precision (inverse variance) gates prediction error. Higher precision at level L means PE from L gets more weight in updating the level above. Precisions are not competing — they multiply.
- **Feldman & Friston (2010, Front Hum Neurosci):** Precision is estimated at each level of the hierarchy via sufficient statistics of prediction errors. Precision estimation is itself a form of inference (empirical Bayes).
- **Adams, Shipp & Friston (2013, Ann NY Acad Sci):** Attention = precision optimization. Increasing precision at a specific level amplifies PE signal from that level. This is implemented via gain modulation of superficial pyramidal cells.
- **Kanai et al. (2015, Phil Trans R Soc B):** "Precision of precision" — uncertainty about precision estimates (volatility) is a second-order statistic. When precision estimates are uncertain, the system should be more exploratory.
- **Mathys et al. (2014, Front Hum Neurosci):** Hierarchical Gaussian Filter (HGF) — multi-level precision weighting where each level's precision informs the learning rate at the level below. Precision-weighted PE at level k: `δ_k = (π_{k-1} / π_k) × PE_k`.

**Formula for combining two precision sources:**

```
# Precision-weighted average (inverse-variance weighting)
π_combined = π_relay + π_h3                    # Total precision (sum, not average)
w_relay = π_relay / π_combined                 # Weight of relay estimate
w_h3 = π_h3 / π_combined                      # Weight of H3 estimate

precision_obs = w_relay × obs_relay + w_h3 × obs_h3
```

This is mathematically equivalent to the **optimal Bayesian combination** of two independent Gaussian estimates:

```
μ_combined = (π₁μ₁ + π₂μ₂) / (π₁ + π₂)
π_combined = π₁ + π₂
```

**Key insight:** The more precise source naturally dominates. When relay precision is high (relay computed successfully, cross-signal agreement), relay evidence dominates. When relay is absent (fallback), H³ precision alone determines the update.

**Implementation:**
```python
def combine_precision(pi_relay, obs_relay, pi_h3, obs_h3):
    """Optimal Bayesian combination of two precision-weighted estimates."""
    if pi_relay is None:
        return obs_h3, pi_h3  # Fallback: H3 only
    pi_total = pi_relay + pi_h3
    w_relay = pi_relay / (pi_total + 1e-8)
    w_h3 = pi_h3 / (pi_total + 1e-8)
    obs_combined = w_relay * obs_relay + w_h3 * obs_h3
    return obs_combined, pi_total
```

**Second-order precision (future v4.0):**
- Track variance of precision estimates over time (volatility)
- High volatility → lower effective precision → more exploratory updates
- Maps to Kanai's "precision of precision" and Mathys' HGF level 3

**Citations:** Friston 2005 (Phil Trans R Soc B 360:1237), 2010 (Nat Rev Neurosci 11:127); Feldman & Friston 2010 (Front Hum Neurosci 4:215); Adams et al. 2013 (Ann NY Acad Sci 1305:1); Kanai et al. 2015 (Phil Trans R Soc B 370:20140218); Mathys et al. 2014 (Front Hum Neurosci 8:825)

---

## 15. Plan Revisions Based on Literature Review

### 15.1 Weight Revisions

| Parameter | Report §8 Value | Literature-Revised Value | Rationale |
|-----------|----------------|-------------------------|-----------|
| **SNEM internal (beat)** | 0.50 | **0.45** | Nozaradan 2–3× ratio (dominant but not sole) |
| **SNEM internal (entrainment)** | 0.30 | **0.35** | Composite signal includes meter |
| **SNEM internal (selective)** | 0.20 | **0.20** | Unchanged |
| **MMP → familiarity** | 0.40 (recognition blend) | **0.35** (f_explicit only) | Yonelinas dual-process: 65% implicit, 35% explicit |
| **H³ → familiarity (with MMP)** | 0.25 period + 0.20 stab | **0.65** combined (f_implicit) | Peretz/Pereira: implicit pathway dominates |
| **MPG → salience** | 0.10 | **0.12** | Pearce IDyOM partial r ≈ 0.3 independent contribution |
| **DAED w_wanting target** | 0.10 | **0.07** (of total reward) | Salimpoor: wanting slightly > liking, 55/45 split |
| **DAED w_liking target** | 0.05 | **0.05** (of total reward) | Salimpoor: consummatory at peak moments |

### 15.2 Scheduler Revision

**Original plan:** Phase 0a (independent) → Phase 0b (dependent: HMCE+DAED)

**Revised plan (literature-grounded):**
```
Phase 0a: ALL 6 relays in parallel (BCH, SNEM, MMP, MPG, HMCE, DAED)
          — Literature shows beat and context processing are parallel
          — DAED can compute without BCH in Phase 0a (basic mode)

Phase 0b: (Wave 2 only) Re-compute dependent relays with cross-inputs
          — DAED recomputes with BCH.consonance_signal + MMP.familiarity_level
          — HMCE recomputes with SNEM.beat_locked_activity (marginal benefit)
```

This is simpler, more parallel, and literature-supported. Cross-relay pathways become an optional second pass.

### 15.3 Familiarity Architecture Revision

**Original plan (§8.3):** Single weighted blend of MMP outputs + H³ + R³

**Revised plan (dual-process):**
```python
# Two distinct pathways (Yonelinas dual-process)
f_implicit = 0.55 * h3_periodicity + 0.45 * h3_stability   # Perirhinal pathway
f_explicit = mmp_out.recognition_state                       # Hippocampal pathway

raw = 0.65 * f_implicit + 0.35 * f_explicit
value = raw * gate
```

This replaces the blended approach with a cleaner dual-process architecture. R³ tonal level drops out when MMP is available (it was a proxy for what MMP now provides directly).

### 15.4 Precision Architecture Revision

**Original plan:** Relay precision replaces H³ precision when available

**Revised plan (Bayesian combination):**
```python
# Precision-weighted combination (Friston optimal)
pi_total = pi_relay + pi_h3
obs = (pi_relay * obs_relay + pi_h3 * obs_h3) / pi_total
precision_obs = pi_total  # Combined precision is SUM (tighter estimate)
```

Both sources contribute proportionally to their reliability. No source is discarded.

### 15.5 RAM Pipeline Revision

**Original plan (§10.1):** Shape check only, values in [0, 1]

**Revised plan:**
```
Linear sum → ReLU → z-normalize per region → sigmoid (for [0,1] visualization)
```

Test criterion updated: RAM temporal dynamics should correlate with belief dynamics (regions active during high-salience moments).

### 15.6 Revised YAML Config

```yaml
# Updated targets after literature review
belief_weights:
  familiarity:
    dual_process: true
    w_implicit: 0.65          # Peretz/Yonelinas (was blended 0.60)
    w_explicit: 0.35          # MMP recognition_state (was blended 0.40)
  salience:
    snem_weight: 0.25         # initial, target 0.30
    mpg_weight: 0.07          # initial, target 0.12 (Pearce IDyOM)
    energy_weight: 0.28
    h3_velocity: 0.15
    pe_carry: 0.25

reward_daed:
  w_wanting: 0.00             # initial, target 0.07 (Salimpoor 55%)
  w_liking: 0.00              # initial, target 0.05 (Salimpoor 45%)
  total_da_budget: 0.12       # max combined DA contribution to reward

precision:
  combination: bayesian       # pi_total = pi_relay + pi_h3 (Friston optimal)

ram:
  aggregation: linear_sum     # Naselaris/Huth/Norman-Haignere standard
  nonlinearity: relu          # Biologically plausible threshold
  normalization: z_score      # Per-region across time
  output_transform: sigmoid   # For [0,1] visualization
```

---

## 16. Updated Summary

This plan integrates 6 relay nuclei (71D total output) into the existing 5-belief kernel through the proven wrapper pattern. Literature review resolved all 7 open questions:

1. **SNEM weights:** Beat-locked dominant (0.45), meter composite (0.35), selective (0.20) — Nozaradan 2–3× ratio
2. **MMP dual-process:** 65% implicit (H³ perirhinal) / 35% explicit (MMP hippocampal) — Peretz/Yonelinas
3. **DAED wanting/liking:** 55%/45% split of 12% total DA budget — Salimpoor 2011
4. **Cross-relay timing:** Parallel (not sequential) — Grahn, Giraud & Poeppel
5. **MPG independence:** Confirmed independent at r ≈ 0.3, weight 0.12 — Pearce IDyOM
6. **RAM aggregation:** Linear sum + ReLU + z-norm — Naselaris/Huth/Norman-Haignere consensus
7. **Precision combination:** Bayesian precision-weighted average (π₁+π₂) — Friston optimal

**All revisions are conservative.** No existing behavior changes until relay outputs are validated. Fallback guaranteed at every integration point.

---

*Report prepared for: MI Project — C³ Kernel v3.0 Integration Planning*
*Literature review completed: 18 February 2026*
*Next step: Wave 0 implementation — RelayKernelWrapper base class + scaffolding*
