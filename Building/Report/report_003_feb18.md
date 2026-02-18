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

## 11. Open Questions (For Literature Review)

Before implementation begins, the following questions should be investigated through literature search:

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

*Report prepared for: MI Project — C³ Kernel v3.0 Integration Planning*
*Next step: Literature review on 7 open questions → plan revision → Wave 0 implementation*
