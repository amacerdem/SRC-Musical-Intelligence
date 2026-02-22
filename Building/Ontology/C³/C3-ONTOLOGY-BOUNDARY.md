# C³ Ontology & Boundary Specification

**Version**: 2.0.0
**Date**: 2026-02-21
**Status**: ACTIVE — Function-based architecture
**Supersedes**: v1.0.0 (2026-02-16, unit-based architecture)
**Companion documents**:
- `R3-ONTOLOGY-BOUNDARY.md` (FROZEN v1.0.0)
- `H3-ONTOLOGY-BOUNDARY.md` (FROZEN v1.0.0)
- `C3-ARCHITECTURE-RFC.md` (RFC v2.0.0 — Function-based belief architecture)
- `../teminology/TERMINOLOGY.md` (ACTIVE v1.0.0)

---

## 1. Formal Definition

**C³ is the Cognitive Brain**: a depth-ordered, belief-updating, neurochemically-modulated
processing hierarchy that transforms perceptual input (R³ spectral features + H³ temporal
morphology) into cognitive state, regional activation, neurochemical dynamics, and experiential
interpretation.

**Boundary sentence**: C³ owns everything that R³ and H³ constitutionally exclude — state,
prediction, surprise, cross-domain binding, value/salience, learning, and belief.

**One-line test**: "Does this computation require memory of past frames beyond a ±2 window,
or depend on a listener model, or combine features across perceptual domains?" If yes → C³.
If no → check R³/H³ inclusion rules first.

---

## 2. What C³ Is / Is Not

### 2.1 C³ IS

| Property | Description |
|----------|-------------|
| **Stateful** | Nuclei may maintain declared state (EMA, posteriors, counters) — state must be serializable and declared in `state_schema` |
| **Predictive** | F-layer outputs are genuine forecasts; prediction error is computed against observed R³/H³ |
| **Binding** | Cross-domain feature products are computed by a shared Binding Service, not duplicated per nucleus |
| **Hierarchical** | 5-depth processing: Relay(0) → Encoder(1) → Associator(2) → Integrator(3) → Hub(4-5) |
| **Multi-rate** | Different nuclei operate at different cadences (frame, beat, phrase, section) |
| **Neurochemically modulated** | 4 global modulators (DA, NE, OPI, 5HT) accumulate through the depth hierarchy |
| **Belief-based** | Named belief variables with single-writer ownership; others contribute evidence |
| **Scientifically grounded** | Every parameter, pathway, and region link cites published neuroscience |

### 2.2 C³ IS NOT

| Anti-pattern | Why it is excluded |
|-------------|-------------------|
| A flat graph of 96 independent models | Hierarchy is enforced by depth-ordered execution and scope-filtered routing |
| A neural network with opaque weights | All parameters are named, cited, and bounded by published effect sizes |
| A replacement for R³ or H³ | C³ reads R³/H³ outputs; it never re-computes spectral features or temporal morphology |
| A brain region simulator | Regions are anatomical evidence for depth assignment, not execution nodes (§11 of TERMINOLOGY) |
| Stateless | Unlike R³ (frame-local) and H³ (stateless window), C³ explicitly owns state |
| A single-rate system | Nuclei declare cadence; the scheduler respects multi-rate execution |

---

## 3. Ontological Axes

C³ is organized along **four orthogonal axes**. Every nucleus, every belief variable, and every
message in the system can be located by its coordinates on these axes.

### 3.1 Axis A — Functional Role (mandatory, structural)

The processing hierarchy. Every nucleus has exactly one role that determines its execution
depth, input signature, and directory location.

| Role | Code | Depth | Count | Reads | Neuroscience basis |
|------|------|-------|-------|-------|--------------------|
| **Relay** | R | 0 | 9 | R³ + H³ only | First-order thalamic/brainstem relay (LGN, MGN, CN) |
| **Encoder** | E | 1 | 34 | R³ + H³ + Relay outputs | Primary cortical feature detector (A1, V1) |
| **Associator** | A | 2 | 35 | R³ + H³ + Relay + Encoder outputs | Association cortex (parabelt, TPJ, Wernicke) |
| **Integrator** | I | 3 | 15 | R³ + H³ + all upstream + cross-unit | Connector hub (angular gyrus, insula, dlPFC) |
| **Hub** | H | 4-5 | 3 | Everything | Rich-club node (vmPFC, PCC, precuneus) |
| | | | **96** | | |

**Invariants**:
- Each unit has exactly ONE Relay (the foundational transformation)
- Depth determines execution order: all depth-N nuclei complete before depth-(N+1) begins
- Scope-filtering: downstream nuclei see only `internal` + `hybrid` dims from upstream; `external` dims are reserved for final assembly
- Cross-unit inputs are available only at depth ≥ 3 (Integrators and Hubs), except for ARU.SRP and RPU.DAED which are special Relays receiving pathway inputs

**Contract test** (Role Consistency):
```
For each nucleus N:
  assert N.PROCESSING_DEPTH == ROLE_DEPTH[N.ROLE]
  assert N.UPSTREAM_READS ⊆ {names of nuclei with depth < N.PROCESSING_DEPTH in same unit}
  assert N.CROSS_UNIT_READS == () if N.PROCESSING_DEPTH < 3 and N not in {SRP, DAED}
```

### 3.2 Axis B — Anatomical Origin (metadata, 9 units)

Units are the **anatomical origin metadata** for each model. They indicate which published
neuroscience domain the model was derived from. As of v2.0, units are NO LONGER the
runtime execution containers — Functions (Axis B') are.

| Unit | Full Name | Relay | Nuclei | Anatomical domain |
|------|-----------|-------|--------|-------------------|
| **SPU** | Spectral Processing | BCH | 9 | Consonance, pitch, timbre |
| **STU** | Structural-Tonal | HMCE | 14 | Temporal structure, meter, motor coupling |
| **IMU** | Integrative Memory | MEAMN | 15 | Memory encoding, retrieval, consolidation |
| **ASU** | Auditory Salience | SNEM | 9 | Attention, salience, surprise |
| **NDU** | Neurodevelopmental | MPG | 9 | Plasticity, expertise, development |
| **MPU** | Motor-Proprioceptive | PEOM | 10 | Rhythm, movement, entrainment |
| **PCU** | Predictive Coding | HTP | 10 | Prediction, uncertainty, aesthetic judgement |
| **ARU** | Affective-Reward | SRP | 10 | Emotion, valence, clinical applications |
| **RPU** | Reward Processing | DAED | 10 | Dopamine, pleasure, preference |

**v2.0 change**: Units remain as metadata tags on each model (`unit: SPU`) but do NOT
determine execution order, belief ownership, or phase scheduling. See Axis B'.

### 3.2' Axis B' — Functional Domain (runtime, 9 Functions + 3 Meta-Layers)

Functions are the **runtime execution containers** in v2.0. Each Function groups models
by brain function (not by anatomical origin). A Function owns one or more beliefs and
contains models drawn from multiple units.

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

**3 Meta-Layers** (provide evidence, no beliefs):

| # | Meta-Layer | Models | Evidence targets |
|---|------------|:------:|-----------------|
| F10 | Clinical & Therapeutic | 10 | F4, F5, F6, F7 |
| F11 | Development & Evolution | 6 | F4, F8 |
| F12 | Cross-Modal Integration | 5 | F2, F3, F7 |

**Execution phases** (Function-based scheduling):
```
Phase 0: F1 Sensory + F7 Motor — sensory/motor grounding (concurrent)
Phase 1: F2 Prediction + F3 Attention — pattern/attention (reads Phase 0)
Phase 2: F4 Memory + F5 Emotion — memory/emotion (reads Phase 0+1)
Phase 3: F8 Learning + F9 Social — higher cognition (reads Phase 0+1+2)
Phase 4: PE + precision computation — meta-computation (all beliefs)
Phase 5: F6 Reward — terminal aggregation (reads all PEs)
Meta: F10/F11/F12 contribute evidence during Phases 0–3
Assembly: scope-aware concatenation → BrainOutput
```

**Function independence**: Phase 0 Functions (F1, F7) have no cross-function dependencies.
Phase 1+ Functions read previous-phase beliefs via predict() context weights.
F6 Reward is terminal: reads all PEs but no Function reads reward within the same frame.

### 3.3 Axis C — Neuromodulatory Channels (modulatory overlay, semi-orthogonal)

Four global neurochemical signals modulate processing across the entire hierarchy via
volume transmission (broadcast diffusion), not point-to-point wiring.

| Channel | Index | Computational role (Doya 2002) | Timescale | Source nuclei |
|---------|-------|-------------------------------|-----------|---------------|
| **DA** | 0 | Reward prediction error / wanting | ms (phasic) to s (tonic) | ARU-R-SRP, RPU-R-DAED |
| **NE** | 1 | Exploration–exploitation / attentional gain | ms (phasic) to s | ASU-R-SNEM |
| **OPI** | 2 | Hedonic evaluation / liking | seconds | ARU-R-SRP |
| **5HT** | 3 | Temporal discount rate / mood | minutes (slow) | ARU-E-AAC |

**Accumulation model**: `neuro_state` is a `(B, T, 4)` tensor initialized at baseline 0.5.
As execution proceeds through depths 0→5, writer nuclei update the state:
- `produce`: sets the value (source nuclei at depth 0)
- `amplify`: additive increase scaled by 0.2 (downstream nuclei)
- `inhibit`: subtractive decrease scaled by 0.2 (suppressive feedback)

After all writers at a depth complete, the updated `neuro_state` is passed to the next depth.
All nuclei at depth N see the same `neuro_state` (updated through depth N-1).

**Semi-orthogonality**: Neurochemicals are NOT independent of the hierarchy. Receptor
densities correlate with depth (D1 dense in PFC, sparse in brainstem). But the SAME DA
signal modulates both A1 (Relay level) and vmPFC (Hub level) simultaneously. The
neurochemical state can change without the hierarchy changing, and vice versa.

**Interactions between channels**:
```
NE (arousal) ──triggers──► DA (wanting)
5-HT ──inhibits (5-HT2C)──► DA    |    5-HT ──facilitates (5-HT1B)──► DA
NE ──amplifies──► OPI (hedonic salience)
DA (wanting, before) ⊥ OPI (liking, at) — temporally dissociated
DA/OPI experience ──modulates──► 5-HT (background mood)
```

### 3.4 Axis D — Belief Graph (the cognitive hierarchy)

The belief graph is the TRUE hierarchy of C³ — it lives in belief variables, not in
model count. Each belief variable has exactly ONE owning **Function** and zero or more
evidence providers from within or across Functions.

#### 3.4.1 Belief Types — 3 Categories (v3.0)

Beliefs are **cognitive inferences** from mechanisms, NOT signal features.
R³/H³ produce signal features (roughness, periodicity). Beliefs are what the brain INFERS.

Beliefs in 3 categories:

> **NOTE**: Counts are **design estimates** — verified during model integration.
> See per-function `collections.md` and `Docs/C³/Models/` for implemented truth.

| Category | Bayesian Cycle | PE | Role |
|----------|:--------------:|:--:|------|
| **Core** (C) | Full (predict→observe→update) | Yes | Primary cognitive states |
| **Appraisal** (A) | Observe-only | No | Evaluative judgments from mechanisms |
| **Anticipation** (N) | Prediction outputs | No | Forward predictions → Core predict() |

**Per-Function Core Beliefs (estimates):**

| Function | Phase | Core Beliefs | A | N | Total |
|----------|:-----:|--------------|:-:|:-:|:-----:|
| F1 Sensory | 0 | harmonic_stability(0.3), pitch_prominence(0.35), pitch_identity(0.4), timbral_character(0.5), aesthetic_quality(0.4) | 7 | 5 | 17 |
| F7 Motor | 0 | period_entrainment(0.65), kinematic_efficiency(0.6), groove_quality(0.55), context_depth(0.7) | 9 | 4 | 17 |
| F2 Prediction | 1 | prediction_hierarchy(0.4), sequence_match(0.45), information_content(0.35), prediction_accuracy(0.5) | 6 | 5 | 15 |
| F3 Attention | 1 | beat_entrainment(0.35), meter_hierarchy(0.4), attention_capture(0.25), salience_network_activation(0.3) | 7 | 4 | 15 |
| F4 Memory | 2 | autobiographical_retrieval(0.85), nostalgia_intensity(0.8), emotional_coloring(0.75), episodic_encoding(0.7) | 7 | 2 | 13 |
| F5 Emotion | 2 | perceived_happy(0.55), perceived_sad(0.55), emotional_arousal(0.5), nostalgia_affect(0.65) | 8 | 2 | 14 |
| F6 Reward | 5 | wanting(0.6), liking(0.65), pleasure(0.7), prediction_error(0.5), tension(0.55) | 7 | 4 | 16 |
| F8 Learning | 3 | trained_timbre_recognition(0.9), expertise_enhancement(0.92), network_specialization(0.95), statistical_model(0.88) | 8 | 2 | 14 |
| F9 Social | 3 | neural_synchrony(0.65), social_coordination(0.6) | 6 | 2 | 10 |

> Full belief inventory: see BELIEF-CYCLE.md. Counts are provisional.
> Model origin units preserved as metadata. Function determines runtime ownership.

#### 3.4.2 Single-Writer Invariant

```
For each belief variable B:
  assert len({F for F in all_functions if B in F.owned_beliefs}) == 1
  # Exactly one Function owns each belief
  # Models within the Function provide evidence
  # Models in other Functions may contribute cross-function evidence
```

This is the most critical structural constraint of C³. It prevents:
- Race conditions (two Functions writing the same belief simultaneously)
- Incoherent state (contradictory updates to the same variable)
- Responsibility diffusion (no clear owner means no clear debugging)

#### 3.4.3 Belief Update Protocol

```python
# Belief update at each tick — organized by Function phase
for phase in scheduler.phases:
    for function in scheduler.functions_at(phase):
        for belief in function.owned_beliefs:
            # 1. Predict from previous frame
            predicted = belief.predict(beliefs_{t-1}, h3)

            # 2. Observe from current frame
            observed = belief.observe(r3, h3, relay_outputs)

            # 3. Bayesian update
            gain = observed.precision / (observed.precision + precision_pred)
            belief.posterior = (1 - gain) * predicted + gain * observed.value

            belief.prior = belief.posterior  # Shift for next tick
```

**v2.0 change**: All beliefs use precision-weighted Bayesian fusion (single method).
The v1.0 three-method protocol (bayesian/ema/direct) is unified into Bayesian.

---

## 4. Runtime Kernel — The C³ OS

### 4.1 Message Schemas

All data flowing through C³ is typed. Five message types cover all inter-nucleus communication:

```python
@dataclass(frozen=True)
class R3Message:
    """Input from R³ perceptual front-end."""
    features: Tensor          # (B, T, 128) — spectral features, [0,1] normalized
    feature_names: Tuple[str, ...]  # Stable names, not indices
    version: str              # R³ ontology version (e.g., "1.0.0")

@dataclass(frozen=True)
class H3Message:
    """Input from H³ temporal morphology engine."""
    features: Dict[Tuple[int,int,int,int], Tensor]  # 4-tuple → (B,T) sparse
    n_tuples: int             # Number of active tuples
    version: str              # H³ ontology version

@dataclass(frozen=True)
class EvidenceMessage:
    """Likelihood / proposal from an evidence provider to a belief owner."""
    source: str               # Nucleus NAME (e.g., "PSCL")
    target_belief: str        # Belief variable name (e.g., "harmonic_function")
    likelihood: Tensor        # (B, T, belief_dim) — evidence for this belief
    confidence: float         # [0,1] — how reliable this evidence is
    timestamp: int            # Frame index

@dataclass(frozen=True)
class BeliefUpdate:
    """Updated belief state from the owner nucleus."""
    belief_name: str          # e.g., "key_estimate"
    owner: str                # Nucleus NAME
    posterior: Tensor         # (B, T, belief_dim) — updated belief
    prediction: Tensor | None # (B, T, belief_dim) — what was predicted (for error computation)
    timestamp: int

@dataclass(frozen=True)
class ModulatorState:
    """Neurochemical state at a given depth."""
    neuro: Tensor             # (B, T, 4) — [DA, NE, OPI, 5HT]
    depth: int                # Which depth this state reflects
```

### 4.2 The Binding Service

Cross-domain feature products (dissolved Group E from R³) are computed ONCE by a shared
service, not duplicated in every nucleus that needs them.

```python
class BindingService:
    """Computes cross-domain feature products on demand. Caches results."""

    def __init__(self, r3_msg: R3Message, h3_msg: H3Message):
        self._r3 = r3_msg
        self._h3 = h3_msg
        self._cache: Dict[str, Tensor] = {}

    def get_binding(self, binding_name: str) -> Tensor:
        """Compute or retrieve a cross-domain product.

        Examples:
            "consonance_x_energy" → r3[0:7] ⊗ r3[7:12]
            "pitch_x_timbre"      → r3[25:41] ⊗ r3[12:21]
            "temporal_x_spectral" → h3[onset_velocity] * r3[spectral_flux]
        """
        if binding_name not in self._cache:
            self._cache[binding_name] = self._compute(binding_name)
        return self._cache[binding_name]

    def _compute(self, name: str) -> Tensor:
        spec = BINDING_REGISTRY[name]  # Declares which features to combine + how
        left = self._resolve(spec.left_source, spec.left_indices)
        right = self._resolve(spec.right_source, spec.right_indices)
        return spec.combine_fn(left, right)  # element-wise product, outer product, etc.
```

**Binding Registry** — a declared set of named cross-domain products:

| Binding name | Left source | Right source | Combine | Used by |
|-------------|-------------|--------------|---------|---------|
| `consonance_x_energy` | R³ A[0:7] | R³ B[7:12] | element-wise | SPU, ASU, PCU |
| `pitch_x_timbre` | R³ F[25:41] | R³ C[12:21] | outer product | SPU, STU |
| `harmony_x_rhythm` | R³ H[51:63] | R³ G[41:51] | element-wise | STU, MPU |
| `onset_x_spectral_change` | H³(onset, velocity) | R³ D[21:25] | product | ASU, PCU |
| `chroma_x_modulation` | R³ F[25:41] | R³ K[83:97] | element-wise | STU, SPU |

This replaces dissolved Group E (24D cross-domain interactions) which was removed from R³
by constitutional decree. The Binding Service computes the same products but:
1. On demand (only if a nucleus requests it)
2. With caching (computed once per frame, shared across all consumers)
3. With provenance (each binding has a declared specification)

### 4.3 Belief Store

C³ maintains three memory systems, corresponding to distinct neuroscience constructs:

```python
class BeliefStore:
    """Central belief storage with three memory tiers."""

    # Working Memory — fast, frame/beat rate
    # Corresponds to: prefrontal sustained activity, gamma oscillations
    working: Dict[str, BeliefState]    # belief_name → current state
    # Capacity: all active beliefs (~30-50 at any time)
    # Retention: current piece only (cleared on new piece)

    # Episodic Memory — event store
    # Corresponds to: hippocampal indexing, theta oscillations
    episodic: List[EpisodicEvent]      # timestamped snapshots
    # Capacity: bounded buffer (configurable, default 1000 events)
    # Retention: session-length (cleared across sessions unless persisted)

    # Semantic Memory — priors and learned parameters
    # Corresponds to: neocortical long-term storage
    semantic: Dict[str, SemanticPrior]  # stable learned parameters
    # Capacity: grows with experience
    # Retention: persistent across sessions (serializable)
```

```python
@dataclass
class BeliefState:
    """Working memory entry for a single belief variable."""
    name: str
    value: Tensor              # (B, T, dim) current posterior
    prior: Tensor              # (B, T, dim) prediction for this frame
    prediction_error: Tensor   # (B, T, dim) = value - prior
    confidence: float          # [0,1] precision of the belief
    owner: str                 # Nucleus NAME
    last_updated: int          # Frame index
    update_count: int          # Total updates since reset

@dataclass
class EpisodicEvent:
    """Snapshot of a salient moment for later retrieval."""
    frame_start: int
    frame_end: int
    belief_snapshot: Dict[str, Tensor]  # Key beliefs at this moment
    neuro_snapshot: Tensor     # (4,) neurochemical state
    ram_snapshot: Tensor       # (26,) region activation
    salience: float            # Why this was stored (DA-driven threshold)
    tag: str                   # "chill", "phrase_boundary", "key_change", etc.

@dataclass
class SemanticPrior:
    """Long-term learned parameter."""
    name: str
    value: Tensor
    source: str                # "published" | "learned" | "calibrated"
    citation: str              # If source=="published", the paper
    update_rule: str           # "fixed" | "bayesian" | "hebbian"
    learning_rate: float       # 0.0 for fixed (published constants)
```

### 4.4 Scheduler — Function-Phase DAG Execution

```python
class C3Scheduler:
    """Orchestrates Function-phase, DAG-ordered execution."""

    def __init__(self, functions: List[Function], meta_layers: List[MetaLayer]):
        self._functions = functions
        self._meta_layers = meta_layers
        self._phase_groups = self._build_phase_groups()
        self._cadence_map = self._build_cadence_map()

    def tick(self, frame_idx: int, r3: R3Message, h3: H3Message,
             belief_store: BeliefStore, binding_service: BindingService) -> BrainOutput:
        """Execute one frame through the full C³ pipeline."""

        neuro = torch.full((B, T, 4), 0.5)  # Baseline
        outputs: Dict[str, Tensor] = {}
        ram = torch.zeros(B, T, 26)

        # ── Phase 0: F1 Sensory + F7 Motor (concurrent, no dependencies) ──
        for function in self._phase_groups[0]:  # [F1, F7]
            for model in function.models:
                if self._should_execute(model, frame_idx):
                    outputs[model.NAME] = model.compute(h3.features, r3.features)
                    self._apply_neuro_links(neuro, model, outputs[model.NAME])
                    self._apply_region_links(ram, model, outputs[model.NAME])
            # predict + observe + update for all Function beliefs
            for belief in function.owned_beliefs:
                belief.predict(belief_store.previous, h3)
                belief.observe(r3, h3, outputs)
                belief.update()
                belief_store.write(belief)

        # ── Phase 1: F2 Prediction + F3 Attention (reads Phase 0) ──
        for function in self._phase_groups[1]:  # [F2, F3]
            for model in function.models:
                if self._should_execute(model, frame_idx):
                    upstream = self._scope_filter(outputs, model)
                    outputs[model.NAME] = model.compute(h3.features, r3.features, upstream)
                    self._apply_neuro_links(neuro, model, outputs[model.NAME])
                    self._apply_region_links(ram, model, outputs[model.NAME])
            for belief in function.owned_beliefs:
                belief.predict(belief_store.previous, h3)
                belief.observe(r3, h3, outputs)
                belief.update()
                belief_store.write(belief)

        # ── Phase 2: F4 Memory + F5 Emotion (reads Phase 0+1) ──
        # ... same pattern

        # ── Phase 3: F8 Learning + F9 Social (reads Phase 0+1+2) ──
        # ... same pattern

        # ── Meta-Layers: F10/F11/F12 contribute evidence ──
        for meta in self._meta_layers:
            for model in meta.models:
                if self._should_execute(model, frame_idx):
                    upstream = self._scope_filter(outputs, model)
                    outputs[model.NAME] = model.compute(h3.features, r3.features, upstream)
                    # evidence only — no belief updates
                    self._apply_region_links(ram, model, outputs[model.NAME])

        # ── Phase 4: PE + Precision computation ──
        for function in self._functions:
            if function.id == "F6":
                continue  # F6 does not have PE
            for belief in function.owned_beliefs:
                pe = belief.observed - belief.predicted
                precision_pred = self._estimate_precision(belief, pe)
                belief_store.record_pe(belief.name, pe, precision_pred)

        # ── Phase 5: F6 Reward (terminal aggregator) ──
        reward_function = self._get_function("F6")
        reward_function.compute_reward(belief_store, outputs)
        for belief in reward_function.owned_beliefs:
            belief_store.write(belief)

        # ── Assembly ──
        tensor = self._assemble_exportable(outputs)
        neuro = neuro.clamp(0.0, 1.0)

        return BrainOutput(tensor=tensor, ram=ram, neuro=neuro, psi=None)

    def _should_execute(self, nucleus: Nucleus, frame_idx: int) -> bool:
        """Multi-rate gating: skip nuclei whose cadence doesn't match this frame."""
        cadence = self._cadence_map.get(nucleus.NAME, 1)  # default: every frame
        return frame_idx % cadence == 0

    def _scope_filter(self, outputs: Dict[str, Tensor],
                      consumer: Nucleus) -> Dict[str, Tensor]:
        """Filter upstream outputs to only routable dims (internal + hybrid)."""
        filtered = {}
        for name in consumer.UPSTREAM_READS:
            if name in outputs:
                producer = self._nucleus_by_name[name]
                routable = producer.routable_dims  # internal + hybrid indices
                filtered[name] = outputs[name][:, :, list(routable)]
        return filtered

    def _assemble_exportable(self, outputs: Dict[str, Tensor]) -> Tensor:
        """Concatenate external + hybrid dims from all nuclei → (B, T, N_ext)."""
        parts = []
        for nucleus in self._nuclei:
            if nucleus.NAME in outputs:
                exportable = nucleus.exportable_dims  # external + hybrid indices
                parts.append(outputs[nucleus.NAME][:, :, list(exportable)])
        return torch.cat(parts, dim=-1)
```

### 4.5 Cadence Map — Multi-Rate Execution

| Cadence | Period | Nuclei (typical) | Neuroscience basis |
|---------|--------|-------------------|--------------------|
| **frame** | ~5.8ms (every frame) | All Relays, most Encoders | Brainstem/primary cortex: millisecond resolution |
| **beat** | ~500ms (every ~86 frames) | Most Associators, some Encoders | Motor cortex, basal ganglia: beat-locked processing |
| **phrase** | ~4s (every ~690 frames) | Integrators, some Associators | PFC, hippocampus: phrase-level integration |
| **section** | ~30s (every ~5170 frames) | Hubs, memory nuclei | Default mode network: section-scale coherence |

Cadence is a PROPERTY of the nucleus, not a hard constraint. The scheduler uses it for
efficiency (skip computation when nothing has changed), but any nucleus can declare any
cadence. Between executions, the nucleus's last output is held constant.

### 4.6 The Tick — Complete Pseudocode (v2.0 Function-Based)

```
TICK(frame_t, r3_frame, h3_demand_result):

  1. INGEST
     r3_msg = R3Message(features=r3_frame, ...)
     h3_msg = H3Message(features=h3_demand_result, ...)
     binding_service = BindingService(r3_msg, h3_msg)

  2. COMPUTE DEMANDED BINDINGS (lazy — computed on first access)
     # binding_service caches; models call binding_service.get_binding(name)

  3. FUNCTION PHASE EXECUTION
     For each phase p = 0, 1, 2, 3:
       For each Function F at phase p (concurrent within phase):
         a. Execute models within F (depth-ordered within Function):
            For each model in F.models (respecting cadence):
              output = model.compute(h3, r3, upstream, neuro_state)
              store output in outputs[model.NAME]
              apply region_links → RAM
              apply neuro_links → neuro_state
         b. Update beliefs within F:
            For each belief in F.owned_beliefs:
              predicted = belief.predict(beliefs_{t-1}, h3)
              observed = belief.observe(r3, h3, outputs)
              gain = π_obs / (π_obs + π_pred)
              posterior = (1 - gain) × predicted + gain × observed
              Store in belief_store

     Meta-Layers: F10/F11/F12 models execute (evidence only, no beliefs)

  4. COMPUTE PREDICTION ERRORS (Phase 4)
     For each Function F (except F6):
       For each belief in F.owned_beliefs:
         PE = observed - predicted
         Update PE ring buffer
         Estimate precision_pred from PE history

  5. REWARD AGGREGATION (Phase 5)
     F6 Reward: aggregate all PEs + hedonic + dopamine → reward_valence
     Update F6 beliefs (reward_valence, pleasure_state, wanting_state)

  6. UPDATE MODULATORS
     # Done inline during step 3 (neuro_links accumulate per phase)
     neuro = neuro.clamp(0.0, 1.0)

  7. ASSEMBLE OUTPUTS
     tensor = concat(exportable dims from all models)    → (B, T, N_ext)
     ram = aggregated region links                        → (B, T, 26)
     neuro = final neurochemical state                    → (B, T, 4)

  8. INTERPRET (Ψ³)
     psi = PsiInterpreter.interpret(tensor, ram, neuro)  → PsiState

  9. PRODUCE BrainOutput(tensor, ram, neuro, psi)

  10. LOG PROVENANCE
      For each belief updated: log Function, evidence sources, PE, precision
```

---

## 5. Cross-Function Signal Routes

Signal routes are the mechanism for data flow between Functions. They replace the
v1.0 "12 cross-unit pathways". Routes are declared, typed, and carry specific signals.

### 5.1 Cross-Function Routes (v2.0)

| ID | Name | Source Function | Target Function | Type | Signal |
|----|------|----------------|-----------------|------|--------|
| R1 | Sensory→Motor | F1 (BCH) | F7 (PEOM) | forward | consonance, pitch → tempo context |
| R2 | Sensory→Prediction | F1 (BCH) | F2 (HTP) | forward | spectral features → prediction basis |
| R3 | Motor→Attention | F7 (PEOM) | F3 (SNEM) | forward | beat phase, groove → salience gate |
| R4 | Attention→Prediction | F3 (SNEM) | F2 (HTP) | forward | salience → precision weighting |
| R5 | Prediction→Reward | F2 (HTP) | F6 (DAED) | forward | prediction error → reward computation |
| R6 | Sensory→Reward | F1 (BCH) | F6 (SRP) | forward | consonance → hedonic signal |
| R7 | Memory→Reward | F4 (MEAMN) | F6 (SRP) | forward | familiarity → reward modulation |
| R8 | Emotion→Prediction | F5 (VMM) | F2 (PWUP) | backward | valence → precision modulation |
| R9 | Reward→Attention | F6 (RPEM) | F3 (PWSM) | backward | surprise → salience boost |
| R10 | Memory→Sensory | F4 (PNH) | F1 (MDNS) | lateral | tonal memory → pitch context |
| R11 | Motor→Learning | F7 (MSR) | F8 (EDNR) | lateral | motor expertise → plasticity |
| R12 | Emotion→Memory | F5 (NEMAC) | F4 (MEAMN) | lateral | emotional coloring → memory encoding |

### 5.2 Legacy Pathway Mapping

| v1.0 Pathway | v2.0 Route | Change |
|-------------|------------|--------|
| P1 SPU→STU | R1 F1→F7 | Unit→Function |
| P2 STU→MPU | (absorbed within F7) | Both models now in F7 |
| P3 MPU→ASU | R3 F7→F3 | Unit→Function |
| P4 ASU→PCU | R4 F3→F2 | Unit→Function |
| P5 PCU→RPU | R5 F2→F6 | Unit→Function |
| P6 SPU→ARU | R6 F1→F6 | Unit→Function |
| P7 IMU→ARU | R7 F4→F6 | Unit→Function |
| P8 RPU→ARU | (absorbed within F6) | Both models now in F6 |
| P9 ARU→PCU | R8 F5→F2 | Unit→Function |
| P10 RPU→ASU | R9 F6→F3 | Unit→Function |
| P11 IMU→STU | R10 F4→F1 | Unit→Function |
| P12 MPU→NDU | R11 F7→F8 | Unit→Function |

**Route types**:
- **Forward**: ascending direction, bottom-up signal (evidence flows toward higher integration)
- **Backward**: descending direction, top-down signal (predictions/modulation flow back)
- **Lateral**: same-phase communication between Functions

---

## 6. Contract Tests (Non-Negotiable)

These tests are enforceable at compile time (class instantiation) and runtime.
Violations are hard errors, not warnings.

### 6.1 State Declaration Test

**Principle**: No hidden state. Every stateful variable must be declared in a serializable schema.

```python
def test_state_declaration(nucleus: Nucleus) -> List[str]:
    """Every attribute that changes between frames must be in state_schema."""
    errors = []

    # Introspect all instance attributes after compute()
    pre_attrs = snapshot_attrs(nucleus)
    nucleus.compute(dummy_h3, dummy_r3, ...)
    post_attrs = snapshot_attrs(nucleus)

    changed = {k for k in pre_attrs if pre_attrs[k] != post_attrs[k]}
    declared = set(nucleus.state_schema.keys()) if hasattr(nucleus, 'state_schema') else set()
    undeclared = changed - declared - EXEMPT_ATTRS  # EXEMPT: _cache, etc.

    if undeclared:
        errors.append(f"{nucleus.NAME}: undeclared state variables: {undeclared}")

    # Verify serializability
    if hasattr(nucleus, 'state_schema'):
        for key, spec in nucleus.state_schema.items():
            val = getattr(nucleus, key, None)
            if val is not None:
                try:
                    serialized = spec.serialize(val)
                    deserialized = spec.deserialize(serialized)
                    assert torch.allclose(val, deserialized)
                except Exception as e:
                    errors.append(f"{nucleus.NAME}.{key}: not serializable: {e}")

    return errors
```

**What this prevents**: Hidden `self._ema`, `self._counter`, `self._prev_frame` that
accumulate state without declaration. If you need state, declare it.

**Relay exemption**: Relays at depth 0 SHOULD be stateless (like R³/H³). If a Relay needs
state, it must justify this with a citation and the state must be declared.

### 6.2 Single-Writer Belief Test

**Principle**: Each belief variable has exactly one owner. Multiple writers = compile-time error.

```python
def test_single_writer(nuclei: List[Nucleus]) -> List[str]:
    """No two nuclei may own the same belief variable."""
    errors = []
    ownership: Dict[str, str] = {}  # belief_name → owner.NAME

    for nucleus in nuclei:
        for belief_name in nucleus.owned_beliefs:
            if belief_name in ownership:
                errors.append(
                    f"CONFLICT: belief '{belief_name}' owned by both "
                    f"{ownership[belief_name]} and {nucleus.NAME}"
                )
            else:
                ownership[belief_name] = nucleus.NAME

    return errors
```

**What this prevents**: Two nuclei both writing `key_estimate`, producing incoherent state.
If BCH and PSCL both think they determine pitch salience, the compiler catches it.

### 6.3 Causality / Leakage Test

**Principle**: Online (real-time) mode must be causal. No peeking at future frames.

```python
def test_causality(nucleus: Nucleus, mode: str) -> List[str]:
    """ONLINE mode: only L0 (backward) H³ windows allowed."""
    errors = []

    if mode == "online":
        for demand in nucleus.h3_demand:
            if demand.law != 0:  # L0 = memory (backward)
                errors.append(
                    f"{nucleus.NAME}: uses law={demand.law} ({demand.law_name}) "
                    f"in ONLINE mode — only L0 (memory/backward) is causal"
                )

        # Check that no temporal operation looks ahead
        for belief_name in nucleus.owned_beliefs:
            belief = belief_store.working.get(belief_name)
            if belief and belief.prediction is not None:
                # Predictions are allowed — but they must be PREDICTIONS
                # (computed from past), not readings of future frames
                pass  # Runtime verification: prediction computed before observation

    elif mode == "offline":
        # L1 (forward) and L2 (bidirectional) are allowed
        # But output must be tagged
        for demand in nucleus.h3_demand:
            if demand.law in (1, 2):
                # Verify the nucleus tags its output as acausal
                if not hasattr(nucleus, 'acausal_output') or not nucleus.acausal_output:
                    errors.append(
                        f"{nucleus.NAME}: uses law={demand.law} but does not "
                        f"declare acausal_output=True"
                    )

    return errors
```

**Modes**:
- **ONLINE**: Real-time processing. Only L0 (backward/memory) H³ windows. All beliefs
  are causal (computed from past + present only). Latency = 0 frames.
- **OFFLINE**: Full analysis. L0, L1 (forward), L2 (bidirectional) all allowed. Output
  tagged `acausal=True` so downstream consumers know. Used for analysis, not real-time.
- **HYBRID**: Mixed. Framework chooses L0 for time-critical beliefs, L2 for analysis beliefs.
  Each belief carries a `causal: bool` tag.

### 6.4 Provenance Test (recommended, soft enforcement)

**Principle**: Every belief update should log which evidence providers contributed.

```python
def test_provenance(belief_store: BeliefStore) -> List[str]:
    """Every belief update must have a provenance record."""
    warnings = []

    for belief_name, state in belief_store.working.items():
        if state.update_count > 0 and not state.provenance_log:
            warnings.append(
                f"Belief '{belief_name}' updated {state.update_count} times "
                f"without provenance log"
            )

    return warnings
```

### 6.5 Role Consistency Test

**Principle**: Structural invariants of the role hierarchy must hold.

```python
def test_role_consistency(nuclei: List[Nucleus]) -> List[str]:
    """Validate role hierarchy constraints."""
    errors = []

    for nucleus in nuclei:
        # 1. Depth matches role
        expected_depth = {"relay": 0, "encoder": 1, "associator": 2,
                          "integrator": 3, "hub": [4, 5]}
        exp = expected_depth[nucleus.ROLE]
        if isinstance(exp, list):
            if nucleus.PROCESSING_DEPTH not in exp:
                errors.append(f"{nucleus.NAME}: Hub depth {nucleus.PROCESSING_DEPTH} not in {exp}")
        elif nucleus.PROCESSING_DEPTH != exp:
            errors.append(f"{nucleus.NAME}: depth {nucleus.PROCESSING_DEPTH} != expected {exp}")

        # 2. UPSTREAM_READS only reference lower-depth nuclei in same unit
        for upstream_name in nucleus.UPSTREAM_READS:
            upstream = nucleus_by_name.get(upstream_name)
            if upstream and upstream.UNIT != nucleus.UNIT:
                errors.append(f"{nucleus.NAME}: UPSTREAM_READS {upstream_name} is in different unit")
            if upstream and upstream.PROCESSING_DEPTH >= nucleus.PROCESSING_DEPTH:
                errors.append(f"{nucleus.NAME}: reads {upstream_name} at depth "
                              f"{upstream.PROCESSING_DEPTH} >= own depth {nucleus.PROCESSING_DEPTH}")

        # 3. CROSS_UNIT_READS only for Integrators/Hubs (+ special Relays)
        if nucleus.CROSS_UNIT_READS and nucleus.ROLE in ("encoder", "associator"):
            if nucleus.NAME not in ("SRP", "DAED"):  # Special Relays
                errors.append(f"{nucleus.NAME}: {nucleus.ROLE} has cross-unit reads")

        # 4. LAYERS cover [0, OUTPUT_DIM) without gaps or overlaps
        coverage = [0] * nucleus.OUTPUT_DIM
        for layer in nucleus.LAYERS:
            for i in range(layer.start, layer.end):
                coverage[i] += 1
        if any(c == 0 for c in coverage):
            errors.append(f"{nucleus.NAME}: LAYERS have gaps")
        if any(c > 1 for c in coverage):
            errors.append(f"{nucleus.NAME}: LAYERS have overlaps")

        # 5. dimension_names length matches OUTPUT_DIM
        if len(nucleus.dimension_names) != nucleus.OUTPUT_DIM:
            errors.append(f"{nucleus.NAME}: {len(nucleus.dimension_names)} dim names "
                          f"!= OUTPUT_DIM {nucleus.OUTPUT_DIM}")

    return errors
```

### 6.6 Determinism Test (for Substrate layer)

**Principle**: The glass-box Substrate (published science) is deterministic.
Only the Plasticity layer introduces learned/adapted parameters.

```python
def test_determinism(nucleus: Nucleus, mode: str = "substrate") -> List[str]:
    """In substrate mode, same input → same output."""
    errors = []

    if mode == "substrate":
        # Run twice with identical input
        out1 = nucleus.compute(h3, r3, upstream, cross)
        out2 = nucleus.compute(h3, r3, upstream, cross)
        if not torch.allclose(out1, out2, atol=1e-6):
            errors.append(f"{nucleus.NAME}: non-deterministic in substrate mode")

    return errors
```

---

## 7. Integration Plan for 96 Models

### 7.1 Feature Registry — Name-Based Addressing

**Problem**: Model docs reference R³ features by numeric indices (e.g., `r3[0:7]`). But R³
renumbering is guaranteed as features are added/reorganized.

**Solution**: A compile-time Feature Registry that maps stable names to current indices.

```python
class FeatureRegistry:
    """Stable name → current index mapping. Compiled per R³ version."""

    _name_to_idx: Dict[str, int]  # "roughness_sethares" → 0
    _idx_to_name: Dict[int, str]  # 0 → "roughness_sethares"
    _version: str                  # "1.0.0"

    def resolve(self, name: str) -> int:
        """Resolve feature name to current index. Raises if unknown."""
        if name not in self._name_to_idx:
            raise FeatureNotFoundError(f"Unknown feature '{name}' in R³ v{self._version}")
        return self._name_to_idx[name]

    def resolve_range(self, group: str) -> slice:
        """Resolve group name to index range. E.g., 'consonance' → slice(0, 7)."""
        return self._group_ranges[group]

    @classmethod
    def from_r3_version(cls, version: str) -> "FeatureRegistry":
        """Build registry from R³ ontology version."""
        # Load feature definitions for this version
        # Map names to indices
        ...
```

**Migration path**: Existing model docs use indices → add a `feature_names` property
that maps to current indices via the registry. The doc indices become documentation
(historical), the code uses names resolved at import time.

### 7.2 Adapters — Bridging Legacy Patterns

Three adapters bridge the gap between legacy model code and the new ontology:

#### IndexAdapter — R³ index migration

```python
class IndexAdapter:
    """Maps legacy R³ numeric indices to R³@1.0.0 feature names."""

    # Legacy docs used: r3[0] = roughness_sethares
    # New code uses:    registry.resolve("roughness_sethares") → 0

    LEGACY_MAP = {
        0: "roughness_sethares",
        1: "roughness_vassilakis",
        2: "spectral_nps",
        3: "harmonic_coincidence",
        4: "template_match",
        5: "roughness_total",       # was "periodicity" in some docs
        6: "consonance_signal",
        7: "velocity_A",            # was "amplitude" in some docs
        # ... full 128-entry map
    }

    def adapt(self, legacy_idx: int) -> str:
        """Convert legacy index to stable name."""
        return self.LEGACY_MAP[legacy_idx]
```

#### BindingAdapter — Dissolved Group E replacement

```python
class BindingAdapter:
    """Replaces dissolved Group E (24D cross-domain products).

    Legacy models that read r3[dissolved_E_indices] now call
    binding_service.get_binding(name) instead.
    """

    # Maps old Group E dimension names to binding_service calls
    ADAPTATION_MAP = {
        "consonance_energy_interaction": "consonance_x_energy",
        "pitch_timbre_interaction": "pitch_x_timbre",
        "harmony_rhythm_interaction": "harmony_x_rhythm",
        # ... 24 entries covering all dissolved Group E dims
    }

    def adapt(self, old_name: str, binding_service: BindingService) -> Tensor:
        binding_name = self.ADAPTATION_MAP[old_name]
        return binding_service.get_binding(binding_name)
```

#### ContextStatsAdapter — Shared temporal statistics

```python
class ContextStatsAdapter:
    """Shared implementations of EMA/counters that live in C³.

    Dissolved Group I features (melodic_entropy, harmonic_entropy,
    spectral_surprise, predictive_entropy) are now beliefs in C³.
    Models that need them read from the BeliefStore instead of R³.
    """

    def get_melodic_entropy(self, belief_store: BeliefStore) -> Tensor:
        return belief_store.working["melodic_entropy"].value

    def get_harmonic_entropy(self, belief_store: BeliefStore) -> Tensor:
        return belief_store.working["harmonic_entropy"].value

    def get_spectral_surprise(self, belief_store: BeliefStore) -> Tensor:
        return belief_store.working["spectral_surprise"].value

    def get_predictive_entropy(self, belief_store: BeliefStore) -> Tensor:
        return belief_store.working["predictive_entropy"].value
```

### 7.3 Gradual Absorption — Migration Phases

| Phase | Name | Scope | What changes |
|-------|------|-------|--------------|
| **v0.1** | Contract | All 96 nuclei | Add `state_schema`, validate role consistency, run contract tests. No compute changes. |
| **v0.2** | Registry | All 96 nuclei | Replace hard-coded R³ indices with `FeatureRegistry.resolve()` calls. Adapters for legacy. |
| **v0.3** | Beliefs | Owner nuclei (~30) | Declare owned beliefs, implement single-writer protocol. Evidence providers emit likelihoods. |
| **v0.4** | Multi-rate | All 96 nuclei | Declare cadence. Scheduler skips nuclei between their execution beats. |
| **v0.5** | Prediction | PCU, ARU nuclei | Implement genuine F-layer predictions. Compute prediction errors. Feed to RPU for DA. |
| **v1.0** | Full kernel | All | Binding Service, BeliefStore, full tick loop, provenance logging. |
| **v1.1** | Plasticity | Optional | Hebbian pathway weights, Bayesian constant updating, reward-driven adaptation. Behind strict interface. |

**Migration principle**: Each phase is independently deployable. Phase v0.1 can be applied
to all 96 nuclei without changing any compute() logic. Phase v0.5 only affects the ~20
nuclei that produce genuine predictions.

### 7.4 Mechanism Removal Strategy

The old `MECHANISM_NAMES` pattern (BEP, ASA, PPC, TPC, TMH, MEM, AED, CPD, C0P) is
removed as an architectural layer. The transition:

| Old pattern | New pattern |
|-------------|-------------|
| `MECHANISM_NAMES = ("BEP", "ASA")` | Remove. Science lives in `compute()`. |
| `self.mechanisms["BEP"].compute(x)` | Inline the math with citations. |
| Shared mechanism class (30D output) | Shared utility function in `utils/` (if needed). |
| Mechanism as metadata | Remove from metadata. Role + evidence tier + citations remain. |

**Why**: Mechanisms were an abstraction layer that obscured what each nucleus actually
computes. The new architecture makes the science explicit in `compute()`, with shared
mathematical operations (Bayesian surprise, EMA, sigmoid normalization) available as
utility functions rather than named "Mechanisms" with their own identity.

---

## 8. Failure Modes & Prevention

### 8.1 Flat Graph Collapse

**Pattern**: All 96 nuclei execute as peers, each independently reading R³/H³, with no
structure to prevent redundant computation or circular dependencies.

**Prevention**: Depth-ordered execution (R→E→A→I→H) with scope-filtered routing. A nucleus
at depth N can only read from nuclei at depth < N in the same unit. Cross-unit reads only
at depth ≥ 3.

### 8.2 Redundant Feature Reading

**Pattern**: 40 nuclei all independently compute `consonance × energy` because dissolved
Group E is no longer in R³.

**Prevention**: Binding Service computes cross-domain products once and caches. Nuclei
call `binding_service.get_binding("consonance_x_energy")` instead of computing it themselves.

### 8.3 Circular Dependencies

**Pattern**: A reads B's output, B reads A's output → deadlock or undefined order.

**Prevention**: Depth ordering is a strict DAG within each unit. Cross-unit pathways are
typed (forward/backward/lateral) and execute between phases, not within them. No nucleus
can read from another nucleus at the same or higher depth in the same unit.

**Formal proof**:
```
Within unit: depth(consumer) > depth(producer) for all UPSTREAM_READS — acyclic by construction.
Cross-unit: pathways execute between unit computation phases — no intra-phase cross-unit reads.
Therefore: the full execution graph is a DAG.
```

### 8.4 Multiple Writers (Race Condition)

**Pattern**: Both BCH and PSCL write `pitch_salience`, producing contradictory values
depending on execution order.

**Prevention**: Single-Writer Belief Test (§6.2). Each belief has exactly one owner.
Compile-time enforcement — the system refuses to instantiate if two nuclei claim the
same belief.

### 8.5 Hidden State Accumulation

**Pattern**: A nucleus has `self._prev_frame = x` that persists between frames, creating
implicit temporal dependence that nobody knows about.

**Prevention**: State Declaration Test (§6.1). All mutable instance attributes must be in
`state_schema`. Undeclared state is a hard error.

### 8.6 Causality Violation in Online Mode

**Pattern**: An online/real-time system uses H³ L1 (forward window) or L2 (bidirectional
window), peeking at future frames that don't exist yet.

**Prevention**: Causality Test (§6.3). Online mode restricts to L0 (backward/memory) only.
L1/L2 allowed only in offline mode with `acausal=True` tag.

### 8.7 Neurochemical State Race

**Pattern**: Two nuclei at the same depth both `produce` DA, and the result depends on
execution order within that depth.

**Prevention**: When multiple nuclei at the same depth produce the same neurochemical,
the orchestrator takes their weighted average (not sequential overwrite). Subsequent
`amplify`/`inhibit` effects at later depths accumulate additively.

### 8.8 Unbounded Memory Growth

**Pattern**: Episodic memory grows without bound, eventually consuming all RAM.

**Prevention**: Episodic memory is a bounded buffer (default 1000 events). When full,
lowest-salience events are evicted. Semantic memory grows but is explicit and serializable
— visible and manageable.

### 8.9 Scope Leakage

**Pattern**: A downstream nucleus reads `external`-scoped dims that were meant only for
the final output, getting signals not intended for it.

**Prevention**: Scope-filtering in the scheduler. Downstream nuclei receive only
`routable_dims` (internal + hybrid). External dims exist in the tensor but are masked
during upstream→downstream routing.

### 8.10 Feature Index Fragility

**Pattern**: Code uses `r3[:, :, 14]` which breaks when R³ is renumbered.

**Prevention**: Feature Registry (§7.1). All R³ access goes through
`registry.resolve("brightness_kuttruff")` which compiles to the current index.
Numeric indices in code are a lint error.

---

## 9. Freeze Policy

### 9.1 FROZEN (cannot change without constitutional amendment)

| Component | What is frozen | Since |
|-----------|---------------|-------|
| Role hierarchy | R(0)→E(1)→A(2)→I(3)→H(4-5) — five roles, depth ordering | v1.0.0 |
| Single-writer invariant | Each belief has exactly one Function owner | v1.0.0 |
| Scope system | internal / external / hybrid — three scopes | v1.0.0 |
| Output structure | BrainOutput = tensor + RAM(26) + neuro(4) + Ψ³ | v1.0.0 |
| E/M/P/F layers | Four-layer output structure per nucleus | v1.0.0 |
| Causality modes | ONLINE=L0 only, OFFLINE=L0+L1+L2 | v1.0.0 |
| Contract tests | State Declaration, Single-Writer, Causality, Role Consistency | v1.0.0 |
| 9 Functions + 3 Meta-Layers | F1–F9 (belief-owning) + F10–F12 (evidence-only) | v2.0.0 |
| 9 units (metadata) | SPU, STU, IMU, ASU, NDU, MPU, PCU, ARU, RPU | v1.0.0 |
| Neurochemical channels | DA(0), NE(1), OPI(2), 5HT(3) — four channels | v1.0.0 |
| 26 brain regions | The canonical region list for RAM | v1.0.0 |
| Function phase DAG | Phase 0(F1,F7)→1(F2,F3)→2(F4,F5)→3(F8,F9)→4(PE)→5(F6) | v2.0.0 |

### 9.2 STABLE (change with justification + migration plan)

| Component | What can evolve | Process |
|-----------|----------------|---------|
| Nucleus count per unit | New nuclei can be added (new science) | Add with role assignment + tests |
| Pathway list | New pathways can be added | Declare source/target + type + citation |
| Binding registry | New cross-domain products | Declare in registry + specify combine_fn |
| Belief variable list | New beliefs can be added | Declare owner + evidence providers |
| Cadence assignments | Nuclei can change execution rate | Update cadence_map |
| Feature registry | New R³ features (within 128D budget) | Add name mapping |

### 9.3 EVOLVING (change freely within constraints)

| Component | What can change | Constraint |
|-----------|----------------|-----------|
| compute() implementations | Internal algorithms | Must pass contract tests |
| Scientific constants | Coefficient values | Must cite source |
| H³ demand lists | Which tuples a nucleus requests | Must cite rationale |
| Region links / weights | Anatomical mapping refinement | Must cite source |
| Neuro links / effects | Neurochemical mapping refinement | Must cite source |
| Ψ³ interpreter mappings | How tensor+RAM+neuro → PsiState | Must cite behavioral anchor |

---

## 10. Model Atlas — Summary Statistics

Based on systematic analysis of all 96 model documentation files:

### 10.1 Role Distribution

| Role | Count | Output dims (total) | Output dims (mean) |
|------|-------|--------------------|--------------------|
| Relay (R) | 9 | 103 | 11.4 |
| Encoder (E) | 34 | 367 | 10.8 |
| Associator (A) | 35 | 364 | 10.4 |
| Integrator (I) | 15 | 155 | 10.3 |
| Hub (H) | 3 | 30 | 10.0 |
| **Total** | **96** | **~1019** | **10.6** |

**N_ext** (exportable dims) ≈ 600-700D after filtering internal-only dims.

### 10.2 H³ Demand Distribution

| Range | Count | Typical depth |
|-------|-------|---------------|
| 0-10 tuples | 12 | Relays (minimal temporal needs) |
| 11-20 tuples | 48 | Encoders, Associators |
| 21-30 tuples | 28 | Associators, Integrators |
| 31-50 tuples | 8 | Hubs, complex Integrators |
| **Total active** | **~8,600** | ~3.9% of theoretical maximum |

### 10.3 R³ Feature Demand (most consumed)

| R³ Group | Features | Consuming nuclei |
|----------|----------|-----------------|
| A: Consonance [0:7] | roughness, NPS, harmonicity | ~70 nuclei (73%) |
| B: Energy [7:12] | RMS, spectral centroid | ~65 nuclei (68%) |
| C: Timbre [12:21] | spectral shape, brightness | ~55 nuclei (57%) |
| D: Change [21:25] | onset, spectral flux | ~60 nuclei (63%) |
| F: Pitch [25:41] | chroma, F0, melodic contour | ~45 nuclei (47%) |
| G: Rhythm [41:51] | tempo, beat strength | ~40 nuclei (42%) |
| H: Harmony [51:63] | key, chord, harmonic function | ~35 nuclei (36%) |
| J: Timbre Ext [63:83] | formants, MFCC | ~25 nuclei (26%) |
| K: Modulation [83:97] | vibrato, tremolo, AM/FM | ~20 nuclei (21%) |

### 10.4 Cross-Unit Dependencies

| Nuclei with cross-unit reads | Count |
|------------------------------|-------|
| None (intra-unit only) | ~60 |
| 1 cross-unit pathway | ~20 |
| 2+ cross-unit pathways | ~16 |
| **Total with cross-unit** | **~36** (38%) |

All cross-unit reads are at depth ≥ 3 (Integrators/Hubs) except ARU.SRP and RPU.DAED
(special Relays receiving forward pathways).

### 10.5 State Needs

| State type | Count | Examples |
|-----------|-------|---------|
| Stateless (current code) | 96 | All nuclei in current implementation |
| Needs EMA (per docs) | ~30 | Memory smoothing, familiarity tracking |
| Needs posteriors | ~15 | Bayesian belief updating (PCU, ASU) |
| Needs counters | ~10 | Event counting, accumulation |
| **Total needing state** | **~40** (42%) | Phase v0.3+ |

Note: Current code is stateless (all state is deferred). The state needs column reflects
what the model documents describe as necessary for full implementation.

### 10.6 Evidence Tiers

| Tier | Count | Confidence range |
|------|-------|-----------------|
| Alpha (α) | 27 | >90% — direct neural measurements |
| Beta (β) | 43 | 70-90% — multi-method convergence |
| Gamma (γ) | 26 | <70% — theoretical, single-study |

---

## 11. Appendix A: Representative Model Mappings

### 11.1 SPU-R-BCH (Brainstem Consonance Hierarchy) — Relay

```
Role:        Relay (depth 0)
Unit:        SPU
Tier:        Alpha (r=0.81, N=10, Bidelman 2009)
Output:      16D (E:4 + M:4 + P:4 + F:4)
  E [0:4]    scope=internal   → nps, harmonicity, hierarchy, ffr_behavior
  M [4:8]    scope=internal   → consonance_memory, pitch_memory, tonal_memory, spectral_memory
  P [8:12]   scope=external   → consonance_signal, template_match, neural_pitch, tonal_context
  F [12:16]  scope=hybrid     → consonance_forecast, pitch_forecast, tonal_forecast, interval_forecast

R³ demands:  16 features (groups A, C, F, H)
H³ demands:  50 tuples (L0:17, L1:12, L2:21 at H0-H18)
Mechanisms:  None (Relay — reads R³/H³ directly)
Cross-unit:  None
State:       None (stateless)
Beliefs owned: consonance_state, onset_prob (low-level)
Beliefs provided: pitch_salience (evidence to PSCL)

Region links:
  AN(0.7), CN(0.5), IC(0.9), MGB(0.6), A1_HG(0.7), STG(0.4)

Neuro links:
  DA: produce(0.3) from consonance_signal
  5HT: amplify(0.2) from pitch_forecast

Cadence: frame (every frame — brainstem millisecond resolution)
```

### 11.2 PCU-A-PWUP (Precision-Weighted Uncertainty Processing) — Associator

```
Role:        Associator (depth 2)
Unit:        PCU
Tier:        Beta (70-90% confidence)
Output:      12D (E:3 + M:3 + P:3 + F:3)
  E [0:3]    scope=internal   → precision_weight, uncertainty_est, confidence
  M [3:6]    scope=internal   → bayesian_surprise, info_content, prediction_precision
  P [6:9]    scope=external   → tonal_precision, temporal_precision, harmonic_precision
  F [9:12]   scope=hybrid     → precision_forecast, uncertainty_forecast, confidence_forecast

R³ demands:  ~20 features (groups A, B, D, F, H)
H³ demands:  22 tuples (primarily H3-H16, M0-M8, L0+L2)
Mechanisms:  None (science in compute())
Cross-unit:  Reads ARU-E-VMM valence via P9 pathway (backward, at depth 2+)
State:       Needs posterior (Bayesian precision estimation)
Beliefs owned: narrative_tension (high-level, phrase rate)
Beliefs provided: aesthetic_pleasure (evidence to MAA)

Region links:
  IFG(0.6), dlPFC(0.7), ACC(0.5), A1_HG(0.4)

Neuro links: None (reader only — consumes DA for precision scaling)

Cadence: beat (~500ms — integrates over beat-length windows)
```

### 11.3 ARU-H-TAR (Therapeutic Affective Resonance) — Hub

```
Role:        Hub (depth 4)
Unit:        ARU
Tier:        Gamma (<70% — theoretical, clinical extrapolation)
Output:      10D (E:2 + M:3 + P:3 + F:2)
  E [0:2]    scope=internal   → clinical_resonance, therapeutic_potential
  M [2:5]    scope=internal   → affect_integration, mood_stability, emotional_regulation
  P [5:8]    scope=external   → therapeutic_response, resonance_quality, clinical_outcome
  F [8:10]   scope=hybrid     → treatment_forecast, relapse_risk

R³ demands:  ~12 features (groups A, B)
H³ demands:  15 tuples (macro horizons H16-H24, L0+L2)
Mechanisms:  None (science in compute())
Cross-unit:  Reads from RPU (reward), IMU (memory), PCU (prediction) via pathways
State:       Needs EMA (session-level mood tracking), counter (session events)
Beliefs owned: therapeutic_response (high-level, section rate)
Beliefs provided: None (terminal Hub — no downstream consumers in ARU)

Region links:
  vmPFC(0.8), OFC(0.6), amygdala(0.5), hippocampus(0.4), ACC(0.5)

Neuro links:
  5HT: amplify(0.3) from mood_stability
  OPI: amplify(0.2) from resonance_quality

Cadence: section (~30s — slow clinical dynamics)
```

---

## 12. Appendix B: Data Structure Reference

### 12.1 Core Types

```python
# ── Identity ──
class Nucleus(ABC):
    NAME: str                              # "BCH"
    FULL_NAME: str                        # "Brainstem Consonance Hierarchy"
    UNIT: str                             # "SPU"
    ROLE: str                             # "relay" | "encoder" | "associator" | "integrator" | "hub"
    PROCESSING_DEPTH: int                 # 0-5
    OUTPUT_DIM: int                       # Total dims (all scopes)
    LAYERS: Tuple[LayerSpec, ...]        # E/M/P/F structure with scopes
    UPSTREAM_READS: Tuple[str, ...]      # Same-unit dependencies
    CROSS_UNIT_READS: Tuple[CrossUnitPathway, ...]

# ── Output structure ──
@dataclass(frozen=True)
class LayerSpec:
    code: str                             # "E" | "M" | "P" | "F"
    name: str                             # "Extraction" | "Mechanism" | "Percept" | "Forecast"
    start: int                            # Inclusive index
    end: int                              # Exclusive index
    dim_names: Tuple[str, ...]           # Named dimensions
    scope: str = "external"               # "internal" | "external" | "hybrid"

# ── Temporal demand ──
@dataclass(frozen=True)
class H3DemandSpec:
    r3_idx: int                           # R³ feature index [0-127]
    r3_name: str                          # Stable feature name
    horizon: int                          # [0-31]
    horizon_label: str                    # "25ms" | "2s phrase"
    morph: int                            # [0-23]
    morph_name: str                       # "velocity" | "mean" | "entropy"
    law: int                              # 0=memory | 1=forward | 2=integration
    law_name: str                         # "memory" | "forward" | "integration"
    purpose: str                          # Scientific justification
    citation: str                         # Paper reference

# ── Brain regions ──
@dataclass(frozen=True)
class RegionLink:
    dim_name: str                         # Output dimension name
    region: str                           # One of 26 canonical abbreviations
    weight: float                         # [0, 1]
    citation: str

# ── Neurochemicals ──
@dataclass(frozen=True)
class NeuroLink:
    dim_name: str                         # Output dimension name
    channel: int                          # 0=DA | 1=NE | 2=OPI | 3=5HT
    effect: str                           # "produce" | "amplify" | "inhibit"
    weight: float                         # [0, 1]
    citation: str

# ── Cross-unit pathways ──
@dataclass(frozen=True)
class CrossUnitPathway:
    pathway_id: str                       # "P1" through "P12"
    name: str                             # Human-readable
    source_unit: str
    source_model: str
    source_dims: Tuple[str, ...]
    target_unit: str
    target_model: str
    pathway_type: str                     # "forward" | "backward" | "lateral"
    correlation: str                      # Published effect size
    citation: str

# ── Evidence ──
@dataclass(frozen=True)
class ModelMetadata:
    citations: Tuple[Citation, ...]
    evidence_tier: str                    # "alpha" | "beta" | "gamma"
    confidence_range: Tuple[float, float]
    falsification_criteria: Tuple[str, ...]
    version: str = "1.0.0"

@dataclass(frozen=True)
class Citation:
    first_author: str
    year: int
    method: str                           # "fMRI" | "MEG" | "iEEG" | "behavioral" | "review"
    n: int                                # Sample size
    key_finding: str
    effect_size: str                      # "r=0.81" | "η²=0.23" | "p<0.001"

# ── Output ──
@dataclass
class BrainOutput:
    tensor: Tensor                        # (B, T, N_ext)
    ram: Tensor                           # (B, T, 26)
    neuro: Tensor                         # (B, T, 4)
    psi: PsiState                         # Ψ³ interpretation

@dataclass
class PsiState:
    affect: Tensor                        # (B, T, 4) — valence, arousal, tension, dominance
    emotion: Tensor                       # (B, T, 8) — joy, sadness, fear, anger, awe, nostalgia, tenderness, serenity
    aesthetic: Tensor                     # (B, T, 6) — beauty, groove, flow, complexity_pref, surprise, closure
    bodily: Tensor                        # (B, T, 4) — chills, movement_urge, breathing, tension_release
    cognitive: Tensor                     # (B, T, 4) — familiarity, absorption, expectation, attention
    temporal: Tensor                      # (B, T, 5) — anticipation, resolution, buildup, release, cadence

    @property
    def flat(self) -> Tensor:             # (B, T, 31)
        return torch.cat([self.affect, self.emotion, self.aesthetic,
                          self.bodily, self.cognitive, self.temporal], dim=-1)
```

### 12.2 Belief System Types

```python
@dataclass
class BeliefVariable:
    """Declared belief in the belief graph."""
    name: str                             # "key_estimate"
    dim: int                              # Dimensionality
    owner: str                            # Nucleus NAME — single writer
    evidence_providers: Tuple[str, ...]  # Nucleus NAMEs — read-only contributors
    update_method: str                    # "bayesian" | "ema" | "direct"
    update_rate: str                      # "frame" | "beat" | "phrase" | "section"
    abstraction_level: str                # "low" | "mid" | "high"
    default_prior: Tensor                 # Initial value

@dataclass
class BeliefState:
    """Runtime state of a belief variable."""
    name: str
    value: Tensor                         # (B, T, dim) current posterior
    prior: Tensor                         # (B, T, dim) prediction
    prediction_error: Tensor              # (B, T, dim) value - prior
    confidence: float                     # [0, 1] precision
    owner: str
    last_updated: int                     # Frame index
    update_count: int
    provenance_log: List[Tuple[str, float]]  # [(provider_name, weight), ...]

@dataclass
class StateSchema:
    """Declared mutable state for a nucleus."""
    fields: Dict[str, StateFieldSpec]

@dataclass
class StateFieldSpec:
    name: str                             # "ema_consonance"
    dtype: str                            # "float32"
    shape: Tuple[int, ...]               # (7,) or (B, T, 4)
    default: Any                          # Initial value
    citation: str                         # Why this state exists
    serialize: Callable                   # How to save
    deserialize: Callable                 # How to restore
```

---

## 13. Appendix C: Alignment with R³ and H³

### 13.1 What R³ Provides to C³

| R³ output | Shape | C³ consumption |
|-----------|-------|---------------|
| Spectral features | (B, T, 128) | Direct input to all Relays. Feature Registry resolves names→indices. |
| Feature names | Tuple[str, ...] | Used by FeatureRegistry for stable addressing |
| Feature map | R3FeatureMap | Group boundaries (A[0:7], B[7:12], ...) for Binding Service |

**R³ boundary respect**: C³ NEVER modifies R³ features. C³ NEVER computes spectral
features. C³ reads R³ output as immutable input.

### 13.2 What H³ Provides to C³

| H³ output | Shape | C³ consumption |
|-----------|-------|---------------|
| Temporal morphology | Dict[4-tuple, (B,T)] | Sparse access via h3_demand declarations |
| Tuple count | int | Monitoring / validation |

**H³ boundary respect**: C³ NEVER computes temporal morphology. C³ NEVER applies window
operators. C³ reads H³ output as immutable input. H³ computes ONLY the tuples demanded
by C³ nuclei (demand-driven).

### 13.3 What C³ Absorbs From Dissolved R³ Groups

| Dissolved | Destination | Implementation |
|-----------|-------------|---------------|
| Group E (Interactions, 24D) | C³ Binding Service | Cross-domain products computed on-demand, cached |
| Group I — melodic_entropy | C³ belief: `melodic_entropy` | Owned by PCU-R-HTP |
| Group I — harmonic_entropy | C³ belief: `harmonic_entropy` | Owned by STU-R-HMCE |
| Group I — spectral_surprise | C³ belief: `spectral_surprise` | Owned by ASU-R-SNEM |
| Group I — predictive_entropy | C³ belief: `predictive_entropy` | Owned by PCU-R-HTP |
| Group I — information_rate | H³ (as velocity morph) | Already in H³ |
| Group I — 2D redundant | Removed | No replacement needed |

### 13.4 The Complete Pipeline

```
Audio (waveform)
  │
  ▼
Cochlea (mel spectrogram)
  │
  ▼
R³ (128D spectral features, per frame, deterministic, stateless)
  │
  ├──────────────────────────────────────────────────┐
  ▼                                                   ▼
H³ (sparse temporal morphology,                 C³ Binding Service
    demand-driven, stateless)                   (cross-domain products,
  │                                              cached, on-demand)
  │                                                   │
  └───────────────┬───────────────────────────────────┘
                  │
                  ▼
          ┌─── C³ BRAIN ───────────────────────────────────────┐
          │                                                      │
          │  neuro = [0.5, 0.5, 0.5, 0.5]  (baseline)          │
          │                                                      │
          │  Depth 0: 9 Relays                                  │
          │    → outputs + neuro writes                          │
          │  Depth 1: 34 Encoders                               │
          │    → outputs + neuro adjustments                     │
          │  Depth 2: 35 Associators                            │
          │    → outputs (read neuro)                            │
          │  Cross-unit: 12 Pathways route                      │
          │  Depth 3: 15 Integrators                            │
          │    → outputs + cross-unit reads                      │
          │  Depth 4-5: 3 Hubs                                  │
          │    → final integration                               │
          │                                                      │
          │  Assembly:                                           │
          │    tensor  → (B, T, N_ext)  [external+hybrid dims]  │
          │    RAM     → (B, T, 26)     [region activation]     │
          │    neuro   → (B, T, 4)      [DA, NE, OPI, 5HT]     │
          │                                                      │
          │  Ψ³ Interpreter:                                     │
          │    tensor + RAM + neuro → PsiState (B, T, 31)       │
          │                                                      │
          │  OUTPUT: BrainOutput(tensor, ram, neuro, psi)        │
          └─────────────────────────────────────────────────────┘
                  │
                  ▼
          L³ reads R³ + H³ + C³(all four) → Language
```

---

## 14. Appendix D: Glossary

| Term | Definition |
|------|-----------|
| **Nucleus** | Any of the 96 C³ brain components. Generic term when role is irrelevant. |
| **Relay** | Depth-0 nucleus. Foundation transformation from raw R³/H³. One per unit. |
| **Encoder** | Depth-1 nucleus. Feature extraction from Relay output. |
| **Associator** | Depth-2 nucleus. Combines Relay + Encoder outputs. |
| **Integrator** | Depth-3 nucleus. Cross-stream integration, may read cross-unit. |
| **Hub** | Depth-4/5 nucleus. Highest convergence. Reads everything. |
| **Unit** | One of 9 cognitive subsystems (SPU, STU, IMU, ASU, NDU, MPU, PCU, ARU, RPU). |
| **Pathway** | Declared cross-unit data route. 12 total, typed forward/backward/lateral. |
| **Belief** | Named cognitive variable with single owner and evidence providers. |
| **BeliefOwner** | The one nucleus that writes a belief variable. |
| **EvidenceProvider** | A nucleus that contributes likelihood to a belief it doesn't own. |
| **Binding Service** | Shared computation of cross-domain feature products (dissolved Group E). |
| **Feature Registry** | Name→index mapping for R³ features. Prevents index fragility. |
| **RAM** | Region Activation Map. (B,T,26) tensor of brain region activations. |
| **Neuro** | (B,T,4) neurochemical state tensor [DA, NE, OPI, 5HT]. |
| **Ψ³** | Cognitive interpretation. Inside C³. Maps tensor+RAM+neuro → PsiState. |
| **PsiState** | 6-domain experiential output: affect, emotion, aesthetic, bodily, cognitive, temporal. |
| **Scope** | Output routing label: internal (downstream only), external (final only), hybrid (both). |
| **Tier** | Evidence quality: alpha/beta/gamma. Metadata, not structural. |
| **Cadence** | Execution frequency: frame/beat/phrase/section. |
| **State schema** | Declared mutable state. No hidden state allowed. |
| **Contract test** | Enforceable invariant. Violation = hard error. |
| **Substrate** | The deterministic, published-science layer. Glass-box. |
| **Plasticity** | The adaptive layer. Hebbian, Bayesian, reward-driven. Optional, behind interface. |

---

## 15. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-16 | Initial proposal. 9 units, ~25 beliefs, mechanism-centered execution. |
| 2.0.0 | 2026-02-21 | Function-based architecture. 9 Functions + 3 Meta-Layers replace units as runtime structure. Multi-belief per Function. 6-phase DAG scheduler. Cross-function signal routes. |
| 3.0.0 | 2026-02-21 | Mechanism-based beliefs. 131 beliefs in 3 categories (36 Core + 65 Appraisal + 30 Anticipation). Signal features ≠ beliefs. Only Core Beliefs carry PE overhead. |

---

*This document is the constitutional specification for C³. It defines what C³ is, what it
owns, how it executes, and what invariants it must maintain. Combined with the frozen R³
and H³ ontologies, it completes the perceptual-cognitive stack of Musical Intelligence.*

*C³ = Cognitive Cortical Computation. The brain that thinks about music.*
