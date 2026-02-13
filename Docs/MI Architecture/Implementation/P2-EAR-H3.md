# Phase 2: Ear -- H3 Temporal Morphology Layer

**Phase**: P2-H3
**Depends on**: P1 (Contracts)
**Parallelizable with**: P2-R3 (no cross-dependency)
**Output**: 38 Python files in `Musical_Intelligence/ear/h3/`
**Gate**: G2-H3 -- H3Extractor produces sparse dict `{(r3_idx, horizon, morph, law): (B, T)}`

---

## Overview

H3 is the temporal morphology layer. It takes the dense R3 spectral tensor `(B, T, 128)` and produces a sparse dictionary of temporal descriptors -- one `(B, T)` tensor per demanded 4-tuple `(r3_idx, horizon, morph, law)`.

| Sub-package | Files | Purpose |
|-------------|:-----:|---------|
| `constants/` | 5 | Horizon, morph, law, and scaling constants |
| `attention/` | 5 | Exponential decay kernel and 3 law windows |
| `morphology/` | 12 | 24 morph functions across 6 categories + dispatch |
| `demand/` | 4 | DemandTree routing, EventHorizon, aggregation |
| `bands/` | 5 | Band-specific horizon metadata (Micro/Meso/Macro/Ultra) |
| `pipeline/` | 3 | 7-phase execution loop and warm-up handling |
| Top-level | 2 | H3Extractor orchestrator + package init |
| **Total** | **38** | |

### Key Constants

- **32 horizons**: H0 (5.8 ms / 1 frame) to H31 (981 s / 168,999 frames)
- **24 morphs**: 6 categories (Level 4, Dispersion 3, Shape 4, Dynamics 9, Rhythm 3, Information 1)
- **3 laws**: L0 Memory (causal), L1 Prediction (anticipatory), L2 Integration (bidirectional)
- **Frame rate**: 172.27 Hz (hop=256, sr=44100), 5.804 ms/frame
- **Kernel**: `A(dt) = exp(-3|dt|/H)`, peak=1.0, boundary~5%
- **Address space**: 128 x 32 x 24 x 3 = 294,912 theoretical; ~8,600 actual (~2.9%)

### Implementation Order

```
P2-H3.1: Constants       -- 5 files (horizons, morphs, laws, scaling, __init__)
P2-H3.2: Attention       -- 5 files (kernel, memory, prediction, integration, __init__)
P2-H3.3: Morphology      -- 12 files (6 morph modules, 5 __init__s, computer.py)
P2-H3.4: Demand          -- 4 files (demand_tree, event_horizon, aggregator, __init__)
P2-H3.5: Bands           -- 5 files (micro, meso, macro, ultra, __init__)
P2-H3.6: Pipeline        -- 3 files (executor, warmup, __init__)
P2-H3.7: Orchestrator    -- 2 files (extractor.py, ear/h3/__init__.py)
```

Sub-phases P2-H3.1 through P2-H3.5 are parallelizable. P2-H3.6 depends on H3.1-H3.3. P2-H3.7 depends on H3.6.

### `__init__.py` Convention

Each sub-package has an `__init__.py` that re-exports its public API. These are not documented individually below; they are pure re-export modules with no primary docs.

---

## P2-H3.1 -- Constants

### `ear/h3/constants/horizons.py`

**Purpose**: Define all 32 horizon durations, frame counts, and band assignments.

**Primary Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 4: complete horizon table
- `Docs/H3/Registry/HorizonCatalog.md` -- authoritative 32-horizon catalog

**Related Docs**:
- `Docs/H3/Bands/Micro/H0-H5-SubBeat.md`, `H6-H7-BeatSubdivision.md`
- `Docs/H3/Bands/Meso/H8-H11-BeatPeriod.md`, `H12-H15-Phrase.md`
- `Docs/H3/Bands/Macro/H16-H17-Measure.md`, `H18-H23-Section.md`
- `Docs/H3/Bands/Ultra/H24-H28-Movement.md`, `H29-H31-Piece.md`

**Depends On**: Nothing (leaf constants).

**Exports**: `HORIZON_MS` (32 floats), `HORIZON_FRAMES` (32 ints), `BAND_ASSIGNMENTS` (32 str), `BAND_RANGES` (dict), `N_HORIZONS` (32), `FRAME_RATE` (172.27), `FRAME_DURATION_MS` (5.804).

**Key Constraints**:
- `HORIZON_MS` = `(5.8, 11.6, 17.4, 23.2, 34.8, 46.4, 200, 250, 300, 350, 400, 450, 525, 600, 700, 800, 1000, 1500, 2000, 3000, 5000, 8000, 15000, 25000, 36000, 60000, 120000, 200000, 414000, 600000, 800000, 981000)`
- `HORIZON_FRAMES` derived as `max(1, round(ms / 1000 * 172.27))`
- Bands: H0-H7=micro, H8-H15=meso, H16-H23=macro, H24-H31=ultra
- All containers immutable (tuples)

**Verification Checklist**:
- [ ] 32 entries in HORIZON_MS matching doc
- [ ] HORIZON_FRAMES: H0=1, H7=43, H15=138, H23=4307, H31=168999
- [ ] BAND_ASSIGNMENTS: 8 per band, correct ordering

---

### `ear/h3/constants/morphs.py`

**Purpose**: Define 24 morph names, categories, minimum window requirements, signed flags.

**Primary Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 5: morph table (M0-M23)
- `Docs/H3/Registry/MorphCatalog.md` -- morph catalog with formulas and min windows

**Related Docs**:
- `Docs/H3/Morphology/Distribution.md`, `Dynamics.md`, `Rhythm.md`, `Information.md`, `Symmetry.md`
- `Docs/H3/Contracts/MorphComputer.md` -- signed flags and min windows

**Depends On**: Nothing (leaf constants).

**Exports**: `MORPH_NAMES` (24 str), `MORPH_CATEGORIES` (dict), `MORPH_MIN_WINDOW` (24 ints), `SIGNED_MORPHS` (frozenset), `N_MORPHS` (24).

**Key Constraints**:
- Names: `("value", "mean", "std", "median", "max", "range", "skewness", "kurtosis", "velocity", "velocity_mean", "velocity_std", "acceleration", "acceleration_mean", "acceleration_std", "periodicity", "smoothness", "curvature", "shape_period", "trend", "stability", "entropy", "zero_crossings", "peaks", "symmetry")`
- 6 categories from architecture doc Section 5.2: Level={0,1,3,4}, Dispersion={2,5,19}, Shape={6,7,16,23}, Dynamics={8-13,15,18,21}, Rhythm={14,17,22}, Information={20}
- `SIGNED_MORPHS` = frozenset({6, 8, 9, 11, 12, 16, 18, 23})

**Verification Checklist**:
- [ ] 24 names matching doc order
- [ ] 6 categories covering all 24 without overlap
- [ ] MORPH_MIN_WINDOW matches MorphComputer.md Section 4
- [ ] SIGNED_MORPHS correct

---

### `ear/h3/constants/laws.py`

**Purpose**: Define the 3 temporal law names, indices, and attention decay constant.

**Primary Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 6: law definitions
- `Docs/H3/Registry/LawCatalog.md` -- law catalog with cognitive basis

**Related Docs**:
- `Docs/H3/Laws/L0-Memory.md`, `L1-Prediction.md`, `L2-Integration.md`

**Depends On**: Nothing (leaf constants).

**Exports**: `LAW_NAMES` (`("memory", "prediction", "integration")`), `LAW_MEMORY` (0), `LAW_PREDICTION` (1), `LAW_INTEGRATION` (2), `ATTENTION_DECAY` (3.0), `N_LAWS` (3).

**Key Constraints**:
- L0=Memory (past->present), L1=Prediction (present->future), L2=Integration (bidirectional)
- `ATTENTION_DECAY = 3.0`; boundary weight `exp(-3) = 0.0498`

**Verification Checklist**:
- [ ] 3 law names matching doc
- [ ] ATTENTION_DECAY = 3.0
- [ ] Integer constants correct

---

### `ear/h3/constants/scaling.py`

**Purpose**: Define MORPH_SCALE[24] normalization constants and signed/unsigned normalization functions.

**Primary Docs**:
- `Docs/H3/Morphology/MorphScaling.md` -- MORPH_SCALE array, normalization formulas
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 5.3: MORPH_SCALE values

**Related Docs**:
- `Docs/H3/Contracts/MorphComputer.md` -- Section 7: normalization not in MorphComputer

**Depends On**: `ear/h3/constants/morphs.py` (SIGNED_MORPHS).

**Exports**: `MORPH_SCALE` (24 floats), `normalize_unsigned(raw, scale)`, `normalize_signed(raw, scale)`.

**Key Constraints**:
- `MORPH_SCALE` = `(1.0, 1.0, 0.25, 1.0, 1.0, 1.0, 2.0, 5.0, 0.1, 0.05, 0.05, 0.01, 0.005, 0.005, 1.0, 1.0, 0.1, 100.0, 0.01, 1.0, 3.0, 20.0, 10.0, 1.0)`
- Unsigned: `clamp(raw / scale, 0, 1)`
- Signed: `clamp((raw / scale + 1) / 2, 0, 1)` -- zero maps to 0.5

**Verification Checklist**:
- [ ] 24 values match MorphScaling.md Section 3
- [ ] normalize_signed(0, 2.0) = 0.5
- [ ] Clamping to [0, 1] on extreme values

---

## P2-H3.2 -- Attention

### `ear/h3/attention/kernel.py`

**Purpose**: Implement the exponential decay attention kernel `A(dt) = exp(-3|dt|/H)`.

**Primary Docs**:
- `Docs/H3/Contracts/AttentionKernel.md` -- formula, edge cases, normalization protocol
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 7: kernel properties

**Related Docs**:
- `Docs/H3/Pipeline/ExecutionModel.md` -- Phase 5: weight usage
- `Docs/H3/Pipeline/WarmUp.md` -- boundary truncation

**Depends On**: `ear/h3/constants/laws.py` (ATTENTION_DECAY).

**Exports**: `AttentionKernel` (class with `compute_weights(window_size, device)` method).

**Key Constraints**:
- `positions = linspace(0, 1, window_size); weights = exp(-ATTENTION_DECAY * (1 - positions))`
- Peak=1.0 (newest), boundary=exp(-3)=0.0498 (oldest). Monotonically increasing.
- Weights NOT normalized here; caller normalizes after truncation
- Edge: window_size=1 -> `ones(1)`, window_size=0 -> empty tensor

**Verification Checklist**:
- [ ] `compute_weights(1)` = tensor([1.0])
- [ ] `compute_weights(100)[0]` ~ 0.0498, `[-1]` = 1.0
- [ ] Monotonically increasing, unnormalized

---

### `ear/h3/attention/memory.py`

**Purpose**: L0 Memory law -- causal past-to-present window selection.

**Primary Docs**:
- `Docs/H3/Laws/L0-Memory.md` -- window formula, cognitive basis
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 6.1

**Related Docs**:
- `Docs/H3/Contracts/H3Extractor.md` -- Section 5.1: law window selection
- `Docs/H3/Pipeline/WarmUp.md` -- L0 warm-up at start

**Depends On**: `ear/h3/constants/laws.py` (LAW_MEMORY).

**Exports**: `MemoryWindow` (class with `select(t, n_frames, T)` -> `(start, end)`).

**Key Constraints**:
- Window: `[max(0, t - n_frames + 1), t + 1)` -- past frames only
- Returns half-open range. Never negative start or end > T.

**Verification Checklist**:
- [ ] `select(0, 10, 100)` = (0, 1); `select(9, 10, 100)` = (0, 10); `select(50, 10, 100)` = (41, 51)

---

### `ear/h3/attention/prediction.py`

**Purpose**: L1 Prediction law -- anticipatory present-to-future window selection.

**Primary Docs**:
- `Docs/H3/Laws/L1-Prediction.md` -- window formula, cognitive basis
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 6.2

**Related Docs**:
- `Docs/H3/Contracts/H3Extractor.md` -- Section 5.1
- `Docs/H3/Pipeline/WarmUp.md` -- L1 warm-up at end

**Depends On**: `ear/h3/constants/laws.py` (LAW_PREDICTION).

**Exports**: `PredictionWindow` (class with `select(t, n_frames, T)` -> `(start, end)`).

**Key Constraints**:
- Window: `[t, min(T, t + n_frames))` -- future frames only. Mirror of L0.

**Verification Checklist**:
- [ ] `select(99, 10, 100)` = (99, 100); `select(90, 10, 100)` = (90, 100); `select(50, 10, 100)` = (50, 60)

---

### `ear/h3/attention/integration.py`

**Purpose**: L2 Integration law -- bidirectional symmetric window selection.

**Primary Docs**:
- `Docs/H3/Laws/L2-Integration.md` -- window formula, cognitive basis
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 6.3

**Related Docs**:
- `Docs/H3/Contracts/H3Extractor.md` -- Section 5.1
- `Docs/H3/Pipeline/WarmUp.md` -- L2 warm-up at both boundaries

**Depends On**: `ear/h3/constants/laws.py` (LAW_INTEGRATION).

**Exports**: `IntegrationWindow` (class with `select(t, n_frames, T)` -> `(start, end)`).

**Key Constraints**:
- `half = n_frames // 2`. Window: `[max(0, t - half), min(T, t + n_frames - half))`
- Symmetric around current frame when not at boundaries.

**Verification Checklist**:
- [ ] `select(0, 10, 100)` = (0, 5); `select(99, 10, 100)` = (94, 100); `select(50, 10, 100)` = (45, 55)

---

## P2-H3.3 -- Morphology

### `ear/h3/morphology/distribution/central.py`

**Purpose**: Level/central-tendency morphs: M0 weighted_mean, M1 mean, M3 median.

**Primary Docs**:
- `Docs/H3/Morphology/Distribution.md` -- formulas
- `Docs/H3/Contracts/MorphComputer.md` -- Section 4: M0, M1, M3

**Related Docs**: `Docs/H3/Registry/MorphCatalog.md`

**Depends On**: Nothing (pure functions, torch only).

**Exports**: `m0_weighted_mean`, `m1_mean`, `m3_median` -- each `(window(B,W), weights(W,)) -> (B,)`.

**Key Constraints**:
- M0: `sum(weights * window, dim=-1)`. M1: `mean(window)`. M3: `median(window)`.
- All unsigned. Min window = 1.

**Verification Checklist**:
- [ ] M0 uses weights; M1/M3 ignore weights
- [ ] Single-frame: M0=M1=M3=value

---

### `ear/h3/morphology/distribution/spread.py`

**Purpose**: Dispersion morphs: M2 std, M5 range.

**Primary Docs**:
- `Docs/H3/Morphology/Distribution.md`; `Docs/H3/Contracts/MorphComputer.md` -- M2, M5

**Depends On**: Nothing.

**Exports**: `m2_std`, `m5_range`.

**Key Constraints**:
- M2: `std(window)`. M5: `max - min`. Both unsigned. Min window = 2.
- Return 0 for constant input. Return zeros(B) for win_len < 2.

**Verification Checklist**:
- [ ] M2=0 for constant; M5=0 for constant, 1.0 for [0,1] extremes

---

### `ear/h3/morphology/distribution/shape.py`

**Purpose**: Shape morphs: M4 max, M6 skewness, M7 kurtosis.

**Primary Docs**:
- `Docs/H3/Morphology/Distribution.md`; `Docs/H3/Contracts/MorphComputer.md` -- M4, M6, M7

**Related Docs**: `Docs/H3/Morphology/MorphScaling.md` -- M6 signed, M7 unsigned

**Depends On**: Nothing.

**Exports**: `m4_max`, `m6_skewness`, `m7_kurtosis`.

**Key Constraints**:
- M4: `max(window)`. Min=1. Unsigned.
- M6: `E[(x-mu)^3]/sigma^3`. Min=3. **Signed**. sigma.clamp(min=1e-8).
- M7: `E[(x-mu)^4]/sigma^4 - 3`. Min=4. Unsigned.

**Verification Checklist**:
- [ ] M6/M7 return 0 for constant window; division guarded

---

### `ear/h3/morphology/dynamics/derivatives.py`

**Purpose**: Derivative morphs: M8-M10 velocity, M11-M13 acceleration.

**Primary Docs**:
- `Docs/H3/Morphology/Dynamics.md`; `Docs/H3/Contracts/MorphComputer.md` -- M8-M13

**Related Docs**: `Docs/H3/Morphology/MorphScaling.md` -- signed flags

**Depends On**: Nothing.

**Exports**: `m8_velocity`, `m9_velocity_mean`, `m10_velocity_std`, `m11_acceleration`, `m12_acceleration_mean`, `m13_acceleration_std`.

**Key Constraints**:
- M8: last diff. Signed. Min=2. M9: mean(diff). Signed. Min=2. M10: std(diff). Unsigned. Min=3.
- M11: last second diff. Signed. Min=3. M12: mean(diff(diff)). Signed. Min=3. M13: std(diff(diff)). Unsigned. Min=4.
- All return zeros(B) below minimum.

**Verification Checklist**:
- [ ] M8 last diff; M9 mean diffs; M11 last second diff
- [ ] Min window guards correct per morph

---

### `ear/h3/morphology/dynamics/smoothness.py`

**Purpose**: M15 smoothness (inverse velocity variability).

**Primary Docs**:
- `Docs/H3/Morphology/Dynamics.md`; `Docs/H3/Contracts/MorphComputer.md` -- M15

**Depends On**: Nothing.

**Exports**: `m15_smoothness`.

**Key Constraints**: `1 / (1 + std(diff(x)))`. Unsigned. Min=3. Range (0,1]. Returns 1.0 for constant.

**Verification Checklist**:
- [ ] Returns 1.0 for constant window; (0,1] for varying

---

### `ear/h3/morphology/dynamics/trend.py`

**Purpose**: M18 trend (linear regression slope) and M21 zero crossings.

**Primary Docs**:
- `Docs/H3/Morphology/Dynamics.md`; `Docs/H3/Contracts/MorphComputer.md` -- M18, M21

**Related Docs**: `Docs/H3/Morphology/MorphScaling.md` -- M18 signed, M21 unsigned

**Depends On**: Nothing.

**Exports**: `m18_trend`, `m21_zero_crossings`.

**Key Constraints**:
- M18: weighted linear regression slope. **Signed**. Min=2. Uses weights.
- M21: count of mean-crossings. Unsigned. Min=2. Raw count (scaling downstream).

**Verification Checklist**:
- [ ] M18 positive for ascending, negative for descending; uses weights
- [ ] M21=0 for monotonic

---

### `ear/h3/morphology/rhythm/periodicity.py`

**Purpose**: Rhythm morphs: M14 periodicity, M17 shape_period, M22 peaks.

**Primary Docs**:
- `Docs/H3/Morphology/Rhythm.md`; `Docs/H3/Contracts/MorphComputer.md` -- M14, M17, M22

**Related Docs**: `Docs/H3/Registry/MorphCatalog.md`

**Depends On**: Nothing.

**Exports**: `m14_periodicity`, `m17_shape_period`, `m22_peaks`.

**Key Constraints**:
- M14: autocorrelation peak ratio. Unsigned. Min=8.
- M17: dominant period in frames. Unsigned. Min=8. Shares autocorrelation with M14.
- M22: local maxima count. Unsigned. Min=3.

**Verification Checklist**:
- [ ] M14 high for periodic, 0 for constant/aperiodic
- [ ] M22=0 for monotonic

---

### `ear/h3/morphology/information/entropy.py`

**Purpose**: M20 Shannon entropy with 16-bin histogram.

**Primary Docs**:
- `Docs/H3/Morphology/Information.md`; `Docs/H3/Contracts/MorphComputer.md` -- M20

**Related Docs**: `Docs/H3/Morphology/MorphScaling.md` -- scale=3.0, max=log2(16)=4.0

**Depends On**: Nothing.

**Exports**: `m20_entropy`.

**Key Constraints**: `-sum(p * log2(p))`, 16 bins. Min=4. Unsigned. Max raw=4.0. Returns 0 for constant.

**Verification Checklist**:
- [ ] Returns 0 for constant; ~4.0 for uniform distribution

---

### `ear/h3/morphology/symmetry/features.py`

**Purpose**: Symmetry morphs: M16 curvature, M19 stability, M23 time-reversal symmetry.

**Primary Docs**:
- `Docs/H3/Morphology/Symmetry.md`; `Docs/H3/Contracts/MorphComputer.md` -- M16, M19, M23

**Related Docs**: `Docs/H3/Morphology/MorphScaling.md` -- M16 signed, M19 unsigned, M23 signed

**Depends On**: Nothing.

**Exports**: `m16_curvature`, `m19_stability`, `m23_symmetry`.

**Key Constraints**:
- M16: `mean(|diff(diff(x))|)`. **Signed**. Min=3.
- M19: `1/(1+std(x))`. Unsigned. Min=2. Returns 1.0 for constant.
- M23: Pearson correlation first-half vs reversed second-half. **Signed**. Min=4. Range [-1,1].

**Verification Checklist**:
- [ ] M16=0 for linear; M19=1 for constant; M23=1 for palindrome, -1 for anti-symmetric

---

### `ear/h3/morphology/scaling.py`

**Purpose**: Apply MORPH_SCALE normalization to raw morph outputs, dispatching signed vs unsigned.

**Primary Docs**: `Docs/H3/Morphology/MorphScaling.md`

**Related Docs**: `Docs/H3/Contracts/MorphComputer.md` -- Section 7

**Depends On**: `ear/h3/constants/scaling.py`, `ear/h3/constants/morphs.py` (SIGNED_MORPHS).

**Exports**: `normalize_morph(raw, morph_idx)` -> value in [0, 1].

**Key Constraints**:
- Dispatches signed/unsigned by `morph_idx in SIGNED_MORPHS`
- Called by pipeline executor, NOT by MorphComputer

**Verification Checklist**:
- [ ] Signed M8, raw=0 -> 0.5; unsigned M1, raw=0.5 -> 0.5

---

### `ear/h3/morphology/computer.py`

**Purpose**: MorphComputer -- dispatch table mapping morph indices 0-23 to computation functions.

**Primary Docs**: `Docs/H3/Contracts/MorphComputer.md` -- dispatch table, compute() interface, edge cases

**Related Docs**: `Docs/H3/Morphology/00-INDEX.md`; `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 5

**Depends On**: All morph function modules (central, spread, shape, derivatives, smoothness, trend, periodicity, entropy, features).

**Exports**: `MorphComputer` -- `compute(window(B,W), weights(W,), morph_idx) -> (B,)`.

**Key Constraints**:
- Dispatch table covers indices 0-23 with no gaps
- Raw output NOT normalized (scaling is downstream)
- Returns safe defaults for below-min-window (zeros or ones)
- Stateless, no parameters

**Verification Checklist**:
- [ ] 24 dispatch entries; compute(w, w, 0) = weighted_mean; compute(w, w, 23) = symmetry
- [ ] Invalid morph_idx raises error

---

## P2-H3.4 -- Demand

### `ear/h3/demand/demand_tree.py`

**Purpose**: DemandTree groups flat 4-tuple demand sets by horizon for attention weight reuse.

**Primary Docs**: `Docs/H3/Contracts/DemandTree.md` -- build() interface, invariants

**Related Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 9
- `Docs/H3/Pipeline/ExecutionModel.md` -- Phase 2
- `Docs/H3/Registry/DemandAddressSpace.md`

**Depends On**: `ear/h3/constants/horizons.py`, `morphs.py`, `laws.py` (for validation bounds).

**Exports**: `DemandTree` -- `build(demand)` (static), `summary(demand)` (static), `unique_horizons()`, `tuples_at(horizon)`.

**Key Constraints**:
- Input: `Set[Tuple[int,int,int,int]]` -- `{(r3_idx, horizon, morph, law), ...}`
- Output: `{horizon: {(r3_idx, morph, law), ...}}`
- Dedup inherent (set). Empty -> empty. Validates ranges.

**Verification Checklist**:
- [ ] `build(set())` = {}; 3 tuples at horizon 4 -> 1 key with 3 entries
- [ ] Validates r3_idx [0,127], horizon [0,31], morph [0,23], law [0,2]

---

### `ear/h3/demand/event_horizon.py`

**Purpose**: EventHorizon maps horizon index to frames, ms, seconds, band.

**Primary Docs**: `Docs/H3/Contracts/EventHorizon.md`

**Related Docs**: `Docs/H3/Registry/HorizonCatalog.md`; `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 4

**Depends On**: `ear/h3/constants/horizons.py` (HORIZON_FRAMES, HORIZON_MS, BAND_ASSIGNMENTS).

**Exports**: `EventHorizon` -- `__init__(index)`, properties: `frames`, `ms`, `seconds`, `band`, `__repr__()`.

**Key Constraints**:
- Asserts `0 <= index < 32`. Pure lookup, no mutable state.

**Verification Checklist**:
- [ ] EH(0).frames=1, EH(31).frames=168999, EH(8).band="meso"
- [ ] EH(32) raises

---

### `ear/h3/demand/aggregator.py`

**Purpose**: Aggregate H3DemandSpec from multiple C3 models, deduplicate, build DemandTree.

**Primary Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 9: aggregation pipeline
- `Docs/H3/Registry/DemandAddressSpace.md` -- sparsity analysis

**Related Docs**:
- `Docs/H3/Demand/SPU-H3-DEMAND.md` through `RPU-H3-DEMAND.md`
- `Docs/H3/Pipeline/ExecutionModel.md` -- Phase 1

**Depends On**: `contracts/dataclasses/demand_spec.py` (H3DemandSpec), `ear/h3/demand/demand_tree.py`.

**Exports**: `aggregate_demands(models)` -> DemandTree, `demand_statistics(demand_set)` -> dict.

**Key Constraints**:
- Collects `h3_demand` from each model, converts via `.as_tuple()`, deduplicates
- Expected ~8,600 unique tuples from 96 models

**Verification Checklist**:
- [ ] 2 models same tuple -> 1 entry; empty models -> empty tree

---

## P2-H3.5 -- Bands

### `ear/h3/bands/micro.py`, `meso.py`, `macro.py`, `ultra.py`

**Purpose**: Per-band horizon metadata classes (musical character, neuroscience basis, mechanism associations).

Each file follows the same pattern. Only band-specific details differ.

**Primary Docs** (per band):

| Band | Horizons | Docs |
|------|----------|------|
| Micro | H0-H7, 5.8ms-250ms | `Docs/H3/Bands/Micro/00-INDEX.md`, `H0-H5-SubBeat.md`, `H6-H7-BeatSubdivision.md` |
| Meso | H8-H15, 300ms-800ms | `Docs/H3/Bands/Meso/00-INDEX.md`, `H8-H11-BeatPeriod.md`, `H12-H15-Phrase.md` |
| Macro | H16-H23, 1s-25s | `Docs/H3/Bands/Macro/00-INDEX.md`, `H16-H17-Measure.md`, `H18-H23-Section.md` |
| Ultra | H24-H31, 36s-981s | `Docs/H3/Bands/Ultra/00-INDEX.md`, `H24-H28-Movement.md`, `H29-H31-Piece.md` |

**Related Docs**: `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 4.1, `Docs/H3/Pipeline/WarmUp.md`

**Depends On**: `ear/h3/constants/horizons.py` (HORIZON_MS, HORIZON_FRAMES).

**Exports**: `MicroBand`, `MesoBand`, `MacroBand`, `UltraBand` -- each with `name`, `horizon_range`, `musical_character`, `neuroscience_basis` per horizon, `primary_mechanisms`.

**Key Constraints per Band**:

| Band | Frames | Key Mechanisms | Demand Share |
|------|--------|---------------|:------------:|
| Micro | 1-43 | PPC (H0,H3,H6), ASA (H3,H6) | ~17% |
| Meso | 52-138 | BEP (H6,H9,H11), TPC (H12) | ~27% |
| Macro | 172-4307 | TMH (H16-H22), SYN (H16,H18), C0P (H18-H20) | ~46% |
| Ultra | 6202-168999 | MEM (H18-H25) | ~10% |

**Verification Checklist** (all 4 bands):
- [ ] Correct horizon indices per band
- [ ] Duration/frame values match architecture doc
- [ ] Musical character descriptions from band docs

---

## P2-H3.6 -- Pipeline

### `ear/h3/pipeline/executor.py`

**Purpose**: 7-phase H3 execution loop processing demands horizon-by-horizon.

**Primary Docs**:
- `Docs/H3/Pipeline/ExecutionModel.md` -- 7 phases, data flow, complexity
- `Docs/H3/Contracts/H3Extractor.md` -- Sections 4-5: execution flow, _compute_morph_series

**Related Docs**:
- `Docs/H3/Pipeline/SparsityStrategy.md`, `Performance.md`
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 12.4: execution pseudocode

**Depends On**: `demand_tree.py`, `event_horizon.py`, `kernel.py`, `memory.py`, `prediction.py`, `integration.py`, `computer.py`, `scaling.py`, `warmup.py`.

**Exports**: `H3Executor` -- `execute(r3_tensor, demand_tree) -> Dict[4-tuple, Tensor(B,T)]`.

**Key Constraints**:
- 7 phases: (1) demand collection, (2) tree build, (3) horizon loop (sorted), (4) window selection by law, (5) attention weights (once per horizon, truncate/renormalize per frame), (6) morph dispatch, (7) result packing
- Weight renormalization: `w = weights[:win_len]; w = w / w.sum().clamp(min=1e-8)`
- All output values in [0, 1] after normalize_morph

**Verification Checklist**:
- [ ] Horizons iterated sorted; weights computed once per horizon
- [ ] Law dispatch: L0->Memory, L1->Prediction, L2->Integration
- [ ] Weight renormalization after truncation
- [ ] normalize_morph applied; output in [0, 1]
- [ ] Output keys are 4-tuples, values (B, T)

---

### `ear/h3/pipeline/warmup.py`

**Purpose**: Handle warm-up effects at sequence boundaries where windows are incomplete.

**Primary Docs**: `Docs/H3/Pipeline/WarmUp.md` -- per-law patterns, duration by band

**Related Docs**:
- `Docs/H3/Pipeline/ExecutionModel.md` -- Phase 4-5
- `Docs/H3/Contracts/AttentionKernel.md` -- Section 7

**Depends On**: `ear/h3/constants/horizons.py`, `laws.py`.

**Exports**: `WarmUpHandler` -- `warmup_frames(horizon, law)`, `is_warmed(t, horizon, law, T)`, `warmup_fraction(horizon, T)`.

**Key Constraints**:
- L0: first n_frames. L1: last n_frames. L2: first+last n_frames//2.
- No explicit flag in output; consumers must check.
- Ultra may never fully warm for short audio.

**Verification Checklist**:
- [ ] L0 warm-up = HORIZON_FRAMES[h]; L1 same; L2 = HORIZON_FRAMES[h]//2
- [ ] Fraction correct for various audio lengths

---

## P2-H3.7 -- Orchestrator

### `ear/h3/extractor.py`

**Purpose**: H3Extractor -- top-level orchestrator and sole entry point for H3 extraction.

**Primary Docs**: `Docs/H3/Contracts/H3Extractor.md` -- constructor, extract(), execution flow

**Related Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 12
- `Docs/H3/Pipeline/ExecutionModel.md`, `SparsityStrategy.md`

**Depends On**: `aggregator.py`, `demand_tree.py`, `executor.py`, `computer.py`.

**Exports**: `H3Extractor` -- `__init__(config)`, `extract(r3, demand) -> Dict[4-tuple, Tensor(B,T)]`.

**Key Constraints**:
- Input: R3 `(B, T, 128)`, demand set (set of 4-tuples or H3DemandSpec list)
- Output: sparse dict, one entry per demanded tuple, all values [0, 1]
- Builds DemandTree, delegates to H3Executor
- No GPU alloc at construction. Stateless between calls.

**Verification Checklist**:
- [ ] Returns dict with entries == demanded tuples
- [ ] Output shapes (B, T). All values [0, 1].
- [ ] Empty demand -> empty dict. Duplicates -> single computation.

---

### `ear/h3/__init__.py`

**Purpose**: Package init; re-export `H3Extractor`, `DemandTree`, `EventHorizon`, `MorphComputer`, `AttentionKernel`.

---

## Verification Gate G2-H3

After completing all P2-H3 files:

```python
import torch
from Musical_Intelligence.ear.h3 import (
    H3Extractor, DemandTree, EventHorizon, MorphComputer, AttentionKernel
)
from Musical_Intelligence.ear.h3.constants import (
    HORIZON_MS, HORIZON_FRAMES, BAND_ASSIGNMENTS, MORPH_NAMES,
    MORPH_SCALE, SIGNED_MORPHS, LAW_NAMES, ATTENTION_DECAY, FRAME_RATE,
    N_HORIZONS, N_MORPHS, N_LAWS
)

# G2-H3.1: Constants
assert (N_HORIZONS, N_MORPHS, N_LAWS) == (32, 24, 3)
assert len(HORIZON_MS) == 32 and len(HORIZON_FRAMES) == 32
assert HORIZON_FRAMES[0] == 1 and HORIZON_FRAMES[31] == 168999
assert HORIZON_MS[0] == 5.8 and HORIZON_MS[31] == 981000
assert ATTENTION_DECAY == 3.0 and FRAME_RATE == 172.27
assert SIGNED_MORPHS == frozenset({6, 8, 9, 11, 12, 16, 18, 23})

# G2-H3.2: Bands
assert all(BAND_ASSIGNMENTS[i] == "micro" for i in range(8))
assert all(BAND_ASSIGNMENTS[i] == "meso" for i in range(8, 16))
assert all(BAND_ASSIGNMENTS[i] == "macro" for i in range(16, 24))
assert all(BAND_ASSIGNMENTS[i] == "ultra" for i in range(24, 32))

# G2-H3.3: EventHorizon
assert EventHorizon(0).frames == 1 and EventHorizon(31).frames == 168999
try: EventHorizon(32); assert False
except (AssertionError, ValueError): pass

# G2-H3.4: AttentionKernel
kernel = AttentionKernel()
w1 = kernel.compute_weights(1)
assert w1.shape == (1,) and torch.isclose(w1[0], torch.tensor(1.0))
w100 = kernel.compute_weights(100)
assert torch.isclose(w100[-1], torch.tensor(1.0), atol=1e-6)
assert abs(w100[0].item() - 0.0498) < 0.01
assert all(w100[i] <= w100[i+1] for i in range(99))

# G2-H3.5: MorphComputer
mc = MorphComputer()
window = torch.rand(2, 10)
weights = torch.ones(10) / 10.0
for m in range(24):
    assert mc.compute(window, weights, m).shape == (2,)

# G2-H3.6: DemandTree
demand = {(0, 4, 0, 0), (0, 4, 2, 0), (5, 10, 8, 1)}
tree = DemandTree.build(demand)
assert len(tree[4]) == 2 and len(tree[10]) == 1
assert DemandTree.build(set()) == {}

# G2-H3.7: H3Extractor end-to-end
extractor = H3Extractor()
r3 = torch.rand(2, 100, 128)
demand = {(0, 6, 0, 0), (7, 6, 8, 0), (0, 16, 14, 2)}
h3_out = extractor.extract(r3, demand)
assert len(h3_out) == 3
for key, val in h3_out.items():
    assert len(key) == 4 and val.shape == (2, 100)
    assert val.min() >= 0.0 and val.max() <= 1.0

# G2-H3.8: Sparsity
assert len(h3_out) == len(demand)

print("G2-H3 GATE PASSED")
```

### Gate Criteria Summary

| Check | Criterion |
|-------|-----------|
| G2-H3.1 | Constants: 32H, 24M, 3L, MORPH_SCALE, ATTENTION_DECAY match docs |
| G2-H3.2 | Band assignments: 8 per band, correct order |
| G2-H3.3 | EventHorizon lookups match horizon tables |
| G2-H3.4 | AttentionKernel: peak=1.0, boundary~5%, monotonic |
| G2-H3.5 | MorphComputer dispatches all 24 morphs, correct shapes |
| G2-H3.6 | DemandTree groups by horizon, deduplicates, handles empty |
| G2-H3.7 | H3Extractor returns Dict[4-tuple, (B,T)] in [0,1] |
| G2-H3.8 | Sparsity: output entries == demanded tuples |

---

## File Dependency Graph

```
P1 contracts (H3DemandSpec, etc.)
 |
 v
ear/h3/constants/ (horizons, morphs, laws, scaling)     [P2-H3.1]
 |
 +---> ear/h3/attention/ (kernel, memory, prediction, integration)  [P2-H3.2]
 |
 +---> ear/h3/morphology/ (24 morphs, dispatch, scaling)            [P2-H3.3]
 |
 +---> ear/h3/demand/ (demand_tree, event_horizon, aggregator)      [P2-H3.4]
 |
 +---> ear/h3/bands/ (micro, meso, macro, ultra metadata)           [P2-H3.5]
 |
 +---> ear/h3/pipeline/ (executor, warmup)                          [P2-H3.6]
 |         depends on: attention, morphology, demand
 |
 +---> ear/h3/extractor.py (H3Extractor)                            [P2-H3.7]
           depends on: pipeline, demand
```
