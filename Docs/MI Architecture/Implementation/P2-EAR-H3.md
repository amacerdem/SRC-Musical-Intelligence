# Phase 2: Ear -- H3 Temporal Morphology Layer

**Phase**: P2-H3
**Depends on**: P1 (Contracts)
**Parallelizable with**: P2-R3 (no cross-dependency)
**Output**: 38 Python files in `Musical_Intelligence/ear/h3/`
**Gate**: G2-H3 -- H3Extractor produces sparse dict `{(r3_idx, horizon, morph, law): (B, T)}`

---

## Overview

H3 is the temporal morphology layer. It takes the dense R3 spectral tensor `(B, T, 128)` and produces a sparse dictionary of temporal descriptors -- one `(B, T)` tensor per demanded 4-tuple `(r3_idx, horizon, morph, law)`.

The implementation is organized into 7 sub-packages:

| Sub-package | Files | Purpose |
|-------------|:-----:|---------|
| `constants/` | 5 | Horizon, morph, law, and scaling constants |
| `attention/` | 5 | Exponential decay kernel and 3 law windows |
| `morphology/` | 12 | 24 morph functions across 5 categories + dispatch |
| `demand/` | 4 | DemandTree routing, EventHorizon, aggregation |
| `bands/` | 5 | Band-specific horizon metadata (Micro/Meso/Macro/Ultra) |
| `pipeline/` | 3 | 7-phase execution loop and warm-up handling |
| Top-level | 2 | H3Extractor orchestrator + package init |
| **Total** | **38** | |

### Key Numerical Constants

- **32 horizons**: H0 (5.8 ms / 1 frame) through H31 (981 s / 168,999 frames)
- **24 morphs**: 5 categories (Distribution 8, Dynamics 9, Rhythm 3, Information 1, Symmetry 3)
- **3 laws**: L0 Memory (causal), L1 Prediction (anticipatory), L2 Integration (bidirectional)
- **Frame rate**: 172.27 Hz (hop=256, sr=44100), 5.804 ms/frame
- **Kernel**: `A(dt) = exp(-3|dt|/H)`, peak=1.0, boundary=exp(-3)=4.98%
- **Address space**: 128 x 32 x 24 x 3 = 294,912 theoretical; ~8,600 actual (~2.9%)

### Implementation Order

```
P2-H3.1: Constants (horizons, morphs, laws, scaling)       -- 5 files
P2-H3.2: Attention (kernel, memory, prediction, integration) -- 5 files
P2-H3.3: Morphology (distribution, dynamics, rhythm, info, symmetry, dispatch) -- 12 files
P2-H3.4: Demand (demand_tree, event_horizon, aggregator)   -- 4 files
P2-H3.5: Bands (micro, meso, macro, ultra metadata)        -- 5 files
P2-H3.6: Pipeline (executor, warmup)                       -- 3 files
P2-H3.7: Orchestrator (H3Extractor, package init)          -- 2 files
```

---

## P2-H3.1 -- Constants

### `ear/h3/constants/__init__.py`

**Purpose**: Re-export all H3 constant modules for convenient import.

**Exports**: `HORIZON_MS`, `HORIZON_FRAMES`, `BAND_ASSIGNMENTS`, `MORPH_NAMES`, `MORPH_CATEGORIES`, `LAW_NAMES`, `MORPH_SCALE`, `SIGNED_MORPHS`, `ATTENTION_DECAY`, `FRAME_RATE`, `N_HORIZONS`, `N_MORPHS`, `N_LAWS`.

**No primary docs** -- pure re-export module.

---

### `ear/h3/constants/horizons.py`

**Purpose**: Define all 32 horizon durations, frame counts, and band assignments.

**Primary Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 4: complete horizon table with ms, frames, band
- `Docs/H3/Registry/HorizonCatalog.md` -- authoritative 32-horizon catalog with neuroscience basis

**Related Docs**:
- `Docs/H3/Bands/Micro/H0-H5-SubBeat.md` -- Micro band H0-H5 detail
- `Docs/H3/Bands/Micro/H6-H7-BeatSubdivision.md` -- Micro band H6-H7 detail
- `Docs/H3/Bands/Meso/H8-H11-BeatPeriod.md` -- Meso band H8-H11 detail
- `Docs/H3/Bands/Meso/H12-H15-Phrase.md` -- Meso band H12-H15 detail
- `Docs/H3/Bands/Macro/H16-H17-Measure.md` -- Macro band H16-H17 detail
- `Docs/H3/Bands/Macro/H18-H23-Section.md` -- Macro band H18-H23 detail
- `Docs/H3/Bands/Ultra/H24-H28-Movement.md` -- Ultra band H24-H28 detail
- `Docs/H3/Bands/Ultra/H29-H31-Piece.md` -- Ultra band H29-H31 detail

**Depends On**: Nothing (leaf constants).

**Exports**:
- `HORIZON_MS` -- Tuple of 32 floats (milliseconds)
- `HORIZON_FRAMES` -- Tuple of 32 ints (frame counts at 172.27 Hz)
- `BAND_ASSIGNMENTS` -- Tuple of 32 str ("micro", "meso", "macro", "ultra")
- `BAND_RANGES` -- Dict mapping band name to (start_idx, end_idx)
- `N_HORIZONS` -- int (32)
- `FRAME_RATE` -- float (172.27)
- `FRAME_DURATION_MS` -- float (5.804)

**Key Constraints**:
- `HORIZON_MS` must match H3-TEMPORAL-ARCHITECTURE.md Section 4.1 exactly: `[5.8, 11.6, 17.4, 23.2, 34.8, 46.4, 200, 250, 300, 350, 400, 450, 525, 600, 700, 800, 1000, 1500, 2000, 3000, 5000, 8000, 15000, 25000, 36000, 60000, 120000, 200000, 414000, 600000, 800000, 981000]`
- `HORIZON_FRAMES` derived as `max(1, round(ms / 1000 * 172.27))` for each horizon
- Band assignments: H0-H7 = micro, H8-H15 = meso, H16-H23 = macro, H24-H31 = ultra
- All values immutable (tuple, not list)

**Verification Checklist**:
- [ ] 32 entries in HORIZON_MS matching doc exactly
- [ ] 32 entries in HORIZON_FRAMES: H0=1, H7=43, H15=138, H23=4307, H31=168999
- [ ] BAND_ASSIGNMENTS has 32 entries, 8 per band
- [ ] FRAME_RATE = 172.27
- [ ] All containers are immutable (tuples)

---

### `ear/h3/constants/morphs.py`

**Purpose**: Define all 24 morph names, categories, minimum window requirements, and signed flags.

**Primary Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 5: complete morph table (M0-M23)
- `Docs/H3/Registry/MorphCatalog.md` -- authoritative morph catalog with formulas and min windows

**Related Docs**:
- `Docs/H3/Morphology/Distribution.md` -- Distribution category morphs (M0-M7)
- `Docs/H3/Morphology/Dynamics.md` -- Dynamics category morphs (M8-M13, M15, M18, M21)
- `Docs/H3/Morphology/Rhythm.md` -- Rhythm category morphs (M14, M17, M22)
- `Docs/H3/Morphology/Information.md` -- Information category morph (M20)
- `Docs/H3/Morphology/Symmetry.md` -- Symmetry category morphs (M16, M19, M23)
- `Docs/H3/Contracts/MorphComputer.md` -- Morph table with signed flags and min windows

**Depends On**: Nothing (leaf constants).

**Exports**:
- `MORPH_NAMES` -- Tuple of 24 str
- `MORPH_CATEGORIES` -- Dict mapping category name to tuple of morph indices
- `MORPH_MIN_WINDOW` -- Tuple of 24 ints (minimum frame requirement per morph)
- `SIGNED_MORPHS` -- FrozenSet of morph indices that produce signed output
- `N_MORPHS` -- int (24)

**Key Constraints**:
- `MORPH_NAMES` must be: `("value", "mean", "std", "median", "max", "range", "skewness", "kurtosis", "velocity", "velocity_mean", "velocity_std", "acceleration", "acceleration_mean", "acceleration_std", "periodicity", "smoothness", "curvature", "shape_period", "trend", "stability", "entropy", "zero_crossings", "peaks", "symmetry")`
- Categories: Distribution={M0,M1,M3,M4}, Dispersion={M2,M5,M19}, Shape={M6,M7,M16,M23}, Dynamics={M8-M13,M15,M18,M21}, Rhythm={M14,M17,M22}, Information={M20}
- Note: docs group into 5 categories in the user prompt (Distribution 8, Dynamics 9, Rhythm 3, Information 1, Symmetry 3) but architecture doc uses 6 categories (Level 4, Dispersion 3, Shape 4, Dynamics 9, Rhythm 3, Information 1). Use the 6-category grouping from H3-TEMPORAL-ARCHITECTURE.md Section 5.2
- `SIGNED_MORPHS` = frozenset({6, 8, 9, 11, 12, 16, 18, 23})
- Min windows from MorphComputer contract: M0-M5=1-2, M6/M8/M16/M18/M21=2-3, M7/M11-M13/M15/M19/M20/M23=3-4, M14/M17=8, M22=3

**Verification Checklist**:
- [ ] 24 names in MORPH_NAMES matching doc order exactly
- [ ] 6 category entries covering all 24 morphs without overlap
- [ ] MORPH_MIN_WINDOW matches MorphComputer.md Section 4
- [ ] SIGNED_MORPHS = {6, 8, 9, 11, 12, 16, 18, 23}
- [ ] N_MORPHS = 24

---

### `ear/h3/constants/laws.py`

**Purpose**: Define the 3 temporal law names, indices, and kernel parameters.

**Primary Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 6: law definitions, window formulas
- `Docs/H3/Registry/LawCatalog.md` -- authoritative law catalog with cognitive basis

**Related Docs**:
- `Docs/H3/Laws/L0-Memory.md` -- L0 causal past-to-present
- `Docs/H3/Laws/L1-Prediction.md` -- L1 anticipatory present-to-future
- `Docs/H3/Laws/L2-Integration.md` -- L2 bidirectional symmetric

**Depends On**: Nothing (leaf constants).

**Exports**:
- `LAW_NAMES` -- Tuple of 3 str: `("memory", "prediction", "integration")`
- `LAW_MEMORY` -- int (0)
- `LAW_PREDICTION` -- int (1)
- `LAW_INTEGRATION` -- int (2)
- `ATTENTION_DECAY` -- float (3.0)
- `N_LAWS` -- int (3)

**Key Constraints**:
- L0 = Memory (causal, past->present)
- L1 = Prediction (anticipatory, present->future)
- L2 = Integration (bidirectional, past<->future)
- `ATTENTION_DECAY = 3.0` is a system-wide constant; `exp(-3) = 0.0498` at boundary

**Verification Checklist**:
- [ ] 3 law names matching doc: memory, prediction, integration
- [ ] Integer constants: LAW_MEMORY=0, LAW_PREDICTION=1, LAW_INTEGRATION=2
- [ ] ATTENTION_DECAY = 3.0
- [ ] N_LAWS = 3

---

### `ear/h3/constants/scaling.py`

**Purpose**: Define MORPH_SCALE[24] normalization constants and signed/unsigned normalization formulas.

**Primary Docs**:
- `Docs/H3/Morphology/MorphScaling.md` -- complete MORPH_SCALE array, signed vs unsigned formulas, calibration protocol
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 5.3: MORPH_SCALE values

**Related Docs**:
- `Docs/H3/Contracts/MorphComputer.md` -- Section 7: normalization not applied within MorphComputer
- `Docs/H3/Expansion/R3v2-H3-Impact.md` -- scaling considerations for expanded R3

**Depends On**: `ear/h3/constants/morphs.py` (SIGNED_MORPHS for dispatch).

**Exports**:
- `MORPH_SCALE` -- Tuple of 24 floats
- `normalize_unsigned(raw, scale)` -- `clamp(raw / scale, 0.0, 1.0)`
- `normalize_signed(raw, scale)` -- `clamp((raw / scale + 1) / 2, 0.0, 1.0)`

**Key Constraints**:
- MORPH_SCALE values must match MorphScaling.md Section 3 exactly: `(1.0, 1.0, 0.25, 1.0, 1.0, 1.0, 2.0, 5.0, 0.1, 0.05, 0.05, 0.01, 0.005, 0.005, 1.0, 1.0, 0.1, 100.0, 0.01, 1.0, 3.0, 20.0, 10.0, 1.0)`
- Unsigned formula: `clamp(raw / MORPH_SCALE[m], 0.0, 1.0)`
- Signed formula: `clamp((raw / MORPH_SCALE[m] + 1) / 2, 0.0, 1.0)` -- centers zero at 0.5
- Signed morphs: M6, M8, M9, M11, M12, M16, M18, M23
- All outputs guaranteed [0, 1] after normalization

**Verification Checklist**:
- [ ] 24 MORPH_SCALE values match doc exactly
- [ ] normalize_unsigned(0.125, 0.25) = 0.5
- [ ] normalize_signed(0.0, 2.0) = 0.5
- [ ] normalize_signed(2.0, 2.0) = 1.0
- [ ] normalize_signed(-2.0, 2.0) = 0.0
- [ ] Clamping to [0, 1] on extreme values

---

## P2-H3.2 -- Attention

### `ear/h3/attention/__init__.py`

**Purpose**: Re-export attention kernel and law window modules.

**Exports**: `AttentionKernel`, `MemoryWindow`, `PredictionWindow`, `IntegrationWindow`.

**No primary docs** -- pure re-export module.

---

### `ear/h3/attention/kernel.py`

**Purpose**: Implement the exponential decay attention kernel `A(dt) = exp(-3|dt|/H)`.

**Primary Docs**:
- `Docs/H3/Contracts/AttentionKernel.md` -- formula, edge cases, normalization protocol
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 7: kernel properties, boundary weight, half-life

**Related Docs**:
- `Docs/H3/Pipeline/ExecutionModel.md` -- Phase 5: how weights are used in the pipeline
- `Docs/H3/Pipeline/WarmUp.md` -- boundary truncation and re-normalization

**Depends On**:
- `ear/h3/constants/laws.py` (ATTENTION_DECAY)

**Exports**:
- `AttentionKernel` (class with `compute_weights(window_size, device)` method)

**Key Constraints**:
- Formula: `positions = linspace(0, 1, window_size); weights = exp(-ATTENTION_DECAY * (1 - positions))`
- Peak weight = 1.0 at newest frame (position = 1.0)
- Boundary weight = exp(-3.0) = 0.0498 at oldest frame (position = 0.0)
- Weights are NOT normalized within this class; caller normalizes after truncation
- Edge cases: window_size=1 returns `ones(1)`, window_size=0 returns empty tensor
- Half-life at 0.231 * H frames from anchor

**Verification Checklist**:
- [ ] `compute_weights(1)` returns tensor([1.0])
- [ ] `compute_weights(100)[-1]` = 1.0 (newest frame)
- [ ] `compute_weights(100)[0]` approximately 0.0498 (oldest frame)
- [ ] Weights monotonically increasing
- [ ] Weights NOT summing to 1.0 (unnormalized)
- [ ] Device parameter respected

---

### `ear/h3/attention/memory.py`

**Purpose**: Implement L0 Memory law -- causal past-to-present window selection.

**Primary Docs**:
- `Docs/H3/Laws/L0-Memory.md` -- L0 window formula, cognitive basis, primary users
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 6.1: L0 window definition

**Related Docs**:
- `Docs/H3/Contracts/H3Extractor.md` -- Section 5.1: law window selection table
- `Docs/H3/Pipeline/WarmUp.md` -- L0 warm-up at start of sequence

**Depends On**:
- `ear/h3/constants/laws.py` (LAW_MEMORY)

**Exports**:
- `MemoryWindow` (class with `select(t, n_frames, T)` -> `(start, end)`)

**Key Constraints**:
- Window: `[max(0, t - n_frames + 1), t + 1)` -- past frames only
- At t=0: window contains only 1 frame (warm-up)
- At t >= n_frames-1: window is fully populated
- Returns (start, end) as half-open range for tensor slicing

**Verification Checklist**:
- [ ] `select(0, 10, 100)` = `(0, 1)` -- single frame at start
- [ ] `select(9, 10, 100)` = `(0, 10)` -- first full window
- [ ] `select(50, 10, 100)` = `(41, 51)` -- standard mid-sequence
- [ ] Never returns negative start or end > T

---

### `ear/h3/attention/prediction.py`

**Purpose**: Implement L1 Prediction law -- anticipatory present-to-future window selection.

**Primary Docs**:
- `Docs/H3/Laws/L1-Prediction.md` -- L1 window formula, cognitive basis, primary users
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 6.2: L1 window definition

**Related Docs**:
- `Docs/H3/Contracts/H3Extractor.md` -- Section 5.1: law window selection table
- `Docs/H3/Pipeline/WarmUp.md` -- L1 warm-up at end of sequence

**Depends On**:
- `ear/h3/constants/laws.py` (LAW_PREDICTION)

**Exports**:
- `PredictionWindow` (class with `select(t, n_frames, T)` -> `(start, end)`)

**Key Constraints**:
- Window: `[t, min(T, t + n_frames))` -- future frames only
- At t=T-1: window contains only 1 frame (warm-up)
- At t <= T-n_frames: window is fully populated
- Mirror image of L0

**Verification Checklist**:
- [ ] `select(99, 10, 100)` = `(99, 100)` -- single frame at end
- [ ] `select(90, 10, 100)` = `(90, 100)` -- last full window
- [ ] `select(50, 10, 100)` = `(50, 60)` -- standard mid-sequence
- [ ] Never returns start < 0 or end > T

---

### `ear/h3/attention/integration.py`

**Purpose**: Implement L2 Integration law -- bidirectional symmetric window selection.

**Primary Docs**:
- `Docs/H3/Laws/L2-Integration.md` -- L2 window formula, cognitive basis, primary users
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 6.3: L2 window definition

**Related Docs**:
- `Docs/H3/Contracts/H3Extractor.md` -- Section 5.1: law window selection table
- `Docs/H3/Pipeline/WarmUp.md` -- L2 warm-up at both boundaries

**Depends On**:
- `ear/h3/constants/laws.py` (LAW_INTEGRATION)

**Exports**:
- `IntegrationWindow` (class with `select(t, n_frames, T)` -> `(start, end)`)

**Key Constraints**:
- `half = n_frames // 2`
- Window: `[max(0, t - half), min(T, t + n_frames - half))`
- Both boundaries affected, each warm-up zone is half the size of L0/L1
- Symmetric around current frame when not at boundaries

**Verification Checklist**:
- [ ] `select(0, 10, 100)` = `(0, 5)` -- truncated left
- [ ] `select(99, 10, 100)` = `(94, 100)` -- truncated right
- [ ] `select(50, 10, 100)` = `(45, 55)` -- symmetric mid-sequence
- [ ] Window size never exceeds n_frames
- [ ] Never returns start < 0 or end > T

---

## P2-H3.3 -- Morphology

### `ear/h3/morphology/__init__.py`

**Purpose**: Re-export MorphComputer and morph sub-modules.

**Exports**: `MorphComputer`.

**No primary docs** -- pure re-export module.

---

### `ear/h3/morphology/distribution/__init__.py`

**Purpose**: Re-export distribution morph sub-modules.

**Exports**: Central tendency and spread functions from `central.py`, `spread.py`, `shape.py`.

---

### `ear/h3/morphology/distribution/central.py`

**Purpose**: Implement Level/central-tendency morphs: M0 weighted_mean, M1 mean, M3 median.

**Primary Docs**:
- `Docs/H3/Morphology/Distribution.md` -- Distribution category morph formulas
- `Docs/H3/Contracts/MorphComputer.md` -- Section 4: M0, M1, M3 specifications

**Related Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 5.1: morph table
- `Docs/H3/Registry/MorphCatalog.md` -- per-morph detail

**Depends On**: Nothing (pure functions, torch only).

**Exports**:
- `m0_weighted_mean(window, weights)` -> `(B,)`
- `m1_mean(window, weights)` -> `(B,)`
- `m3_median(window, weights)` -> `(B,)`

**Key Constraints**:
- M0: `sum(weights * window, dim=-1)` (weights pre-normalized)
- M1: `mean(window, dim=-1)` (ignores weights)
- M3: `median(window, dim=-1)` (ignores weights)
- All produce unsigned [0,1] values since R3 input is [0,1]
- Min window: 1 frame for all three

**Verification Checklist**:
- [ ] M0 uses weights; M1 and M3 do not
- [ ] Single-frame window: M0=M1=M3=value
- [ ] Output shape is (B,) for input (B, W)

---

### `ear/h3/morphology/distribution/spread.py`

**Purpose**: Implement Dispersion morphs: M2 std, M5 range.

**Primary Docs**:
- `Docs/H3/Morphology/Distribution.md` -- Distribution category morph formulas
- `Docs/H3/Contracts/MorphComputer.md` -- Section 4: M2, M5 specifications

**Related Docs**:
- `Docs/H3/Registry/MorphCatalog.md` -- min window, edge cases

**Depends On**: Nothing (pure functions, torch only).

**Exports**:
- `m2_std(window, weights)` -> `(B,)`
- `m5_range(window, weights)` -> `(B,)`

**Key Constraints**:
- M2: `std(window, dim=-1)`. Min window = 2. Returns 0 for constant input.
- M5: `max(window) - min(window)`. Min window = 2. Range [0, 1].
- Both unsigned

**Verification Checklist**:
- [ ] M2 returns 0.0 for constant window
- [ ] M5 returns 0.0 for constant window, 1.0 for [0, 1] extremes
- [ ] Min window guards: returns zeros(B) for win_len < 2

---

### `ear/h3/morphology/distribution/shape.py`

**Purpose**: Implement Shape morphs from the distribution family: M4 max, M6 skewness, M7 kurtosis.

**Primary Docs**:
- `Docs/H3/Morphology/Distribution.md` -- Distribution category morph formulas
- `Docs/H3/Contracts/MorphComputer.md` -- Section 4: M4, M6, M7 specifications

**Related Docs**:
- `Docs/H3/Morphology/MorphScaling.md` -- M6 signed, M7 unsigned
- `Docs/H3/Registry/MorphCatalog.md` -- min window constraints

**Depends On**: Nothing (pure functions, torch only).

**Exports**:
- `m4_max(window, weights)` -> `(B,)`
- `m6_skewness(window, weights)` -> `(B,)`
- `m7_kurtosis(window, weights)` -> `(B,)`

**Key Constraints**:
- M4: `max(window, dim=-1)`. Min window = 1. Unsigned.
- M6: `E[(x-mu)^3] / sigma^3`. Min window = 3. **Signed**. Returns 0 for constant input (division guarded by clamp).
- M7: `E[(x-mu)^4] / sigma^4 - 3` (excess kurtosis). Min window = 4. Unsigned per MorphScaling.md. Returns 0 for constant input.
- Division-by-zero guard: `sigma.clamp(min=1e-8)`

**Verification Checklist**:
- [ ] M6 returns 0.0 for constant or symmetric window
- [ ] M7 returns 0.0 for constant window
- [ ] Division by sigma guarded against zero
- [ ] Min window guards for M6 (3) and M7 (4)

---

### `ear/h3/morphology/dynamics/__init__.py`

**Purpose**: Re-export dynamics morph sub-modules.

**Exports**: Functions from `derivatives.py`, `smoothness.py`, `trend.py`.

---

### `ear/h3/morphology/dynamics/derivatives.py`

**Purpose**: Implement derivative-based morphs: M8-M10 velocity, M11-M13 acceleration.

**Primary Docs**:
- `Docs/H3/Morphology/Dynamics.md` -- Dynamics category morph formulas
- `Docs/H3/Contracts/MorphComputer.md` -- Section 4: M8-M13 specifications

**Related Docs**:
- `Docs/H3/Morphology/MorphScaling.md` -- signed flags for M8, M9, M11, M12

**Depends On**: Nothing (pure functions, torch only).

**Exports**:
- `m8_velocity(window, weights)` -> `(B,)` -- `x[t] - x[t-1]` (last pair)
- `m9_velocity_mean(window, weights)` -> `(B,)` -- `mean(diff(x))`
- `m10_velocity_std(window, weights)` -> `(B,)` -- `std(diff(x))`
- `m11_acceleration(window, weights)` -> `(B,)` -- `diff(diff(x))` (last triple)
- `m12_acceleration_mean(window, weights)` -> `(B,)` -- `mean(diff(diff(x)))`
- `m13_acceleration_std(window, weights)` -> `(B,)` -- `std(diff(diff(x)))`

**Key Constraints**:
- M8 (velocity): signed. Min window = 2.
- M9 (velocity_mean): signed. Min window = 2.
- M10 (velocity_std): unsigned. Min window = 3.
- M11 (acceleration): signed. Min window = 3.
- M12 (acceleration_mean): signed. Min window = 3.
- M13 (acceleration_std): unsigned. Min window = 4.
- All return zeros(B) when window is below minimum

**Verification Checklist**:
- [ ] M8 returns last diff value
- [ ] M9 returns mean of all diffs
- [ ] M11 returns last second diff
- [ ] Min window guards: M8/M9 at 2, M10/M11/M12 at 3, M13 at 4
- [ ] Signed/unsigned flags match MorphScaling.md

---

### `ear/h3/morphology/dynamics/smoothness.py`

**Purpose**: Implement M15 smoothness (inverse jerk).

**Primary Docs**:
- `Docs/H3/Morphology/Dynamics.md` -- Dynamics category morph formulas
- `Docs/H3/Contracts/MorphComputer.md` -- Section 4: M15 specification

**Related Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 5.1: M15 formula

**Depends On**: Nothing (pure function, torch only).

**Exports**:
- `m15_smoothness(window, weights)` -> `(B,)`

**Key Constraints**:
- Formula: `1 / (1 + velocity_std)` per MorphComputer.md; or `1 / (1 + |jerk| / sigma)` per architecture doc
- Use MorphComputer.md as primary: `1 / (1 + std(diff(x)))`
- Unsigned. Min window = 3. Range (0, 1].
- Returns 1.0 for constant input (maximum smoothness)

**Verification Checklist**:
- [ ] Returns 1.0 for constant window
- [ ] Returns value in (0, 1] for varying window
- [ ] Min window guard at 3

---

### `ear/h3/morphology/dynamics/trend.py`

**Purpose**: Implement M18 linear regression trend and M21 zero crossings.

**Primary Docs**:
- `Docs/H3/Morphology/Dynamics.md` -- Dynamics category morph formulas
- `Docs/H3/Contracts/MorphComputer.md` -- Section 4: M18, M21 specifications

**Related Docs**:
- `Docs/H3/Morphology/MorphScaling.md` -- M18 signed, M21 unsigned

**Depends On**: Nothing (pure functions, torch only).

**Exports**:
- `m18_trend(window, weights)` -> `(B,)` -- weighted linear regression slope
- `m21_zero_crossings(window, weights)` -> `(B,)` -- count of mean-crossings

**Key Constraints**:
- M18: weighted linear regression slope. **Signed**. Min window = 2. Uses attention weights.
- M21: count of sign changes around mean, normalized. Unsigned. Min window = 2.
- M21 normalization: raw count (not divided by MORPH_SCALE here; scaling is downstream)

**Verification Checklist**:
- [ ] M18 positive for ascending window, negative for descending
- [ ] M18 uses weights parameter
- [ ] M21 returns 0 for monotonic window
- [ ] M21 returns positive count for oscillating window
- [ ] Min window guards at 2

---

### `ear/h3/morphology/rhythm/__init__.py`

**Purpose**: Re-export rhythm morph sub-module.

**Exports**: Functions from `periodicity.py`.

---

### `ear/h3/morphology/rhythm/periodicity.py`

**Purpose**: Implement rhythm morphs: M14 autocorrelation periodicity, M17 shape_period, M22 peaks.

**Primary Docs**:
- `Docs/H3/Morphology/Rhythm.md` -- Rhythm category morph formulas
- `Docs/H3/Contracts/MorphComputer.md` -- Section 4: M14, M17, M22 specifications

**Related Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 5.1: morph table
- `Docs/H3/Registry/MorphCatalog.md` -- min window constraints

**Depends On**: Nothing (pure functions, torch only).

**Exports**:
- `m14_periodicity(window, weights)` -> `(B,)` -- autocorrelation peak ratio
- `m17_shape_period(window, weights)` -> `(B,)` -- dominant period from autocorrelation
- `m22_peaks(window, weights)` -> `(B,)` -- count of local maxima

**Key Constraints**:
- M14: autocorrelation peak ratio, normalized [0,1]. Min window = 8 (per architecture doc; 4 per MorphComputer.md -- use 8 from architecture doc as it is more conservative). Unsigned.
- M17: dominant period in frames from autocorrelation lag. Min window = 8. Unsigned.
- M22: count of local maxima (normalized). Min window = 3. Unsigned.
- M14 and M17 share autocorrelation computation -- compute once, extract both

**Verification Checklist**:
- [ ] M14 returns 0 for aperiodic/constant window
- [ ] M14 returns high value (near 1.0) for periodic window
- [ ] M17 returns dominant period in frames
- [ ] M22 returns 0 for monotonic window
- [ ] Min window guards: M14/M17 at 8, M22 at 3

---

### `ear/h3/morphology/information/entropy.py`

**Purpose**: Implement M20 Shannon entropy with 16-bin histogram.

**Primary Docs**:
- `Docs/H3/Morphology/Information.md` -- Information category morph formula
- `Docs/H3/Contracts/MorphComputer.md` -- Section 4: M20 specification

**Related Docs**:
- `Docs/H3/Morphology/MorphScaling.md` -- M20 scale = 3.0, max raw ~log2(16) = 4.0

**Depends On**: Nothing (pure function, torch only).

**Exports**:
- `m20_entropy(window, weights)` -> `(B,)`

**Key Constraints**:
- 16-bin histogram of values in window
- Shannon entropy: `-sum(p * log2(p))` where p = bin probabilities
- Max theoretical value: log2(16) = 4.0 bits (uniform distribution)
- Min window = 4. Unsigned. Returns 0 for constant input.

**Verification Checklist**:
- [ ] Returns 0.0 for constant window
- [ ] Returns ~4.0 for uniformly distributed values (before downstream scaling)
- [ ] 16 bins used for histogram
- [ ] Min window guard at 4

---

### `ear/h3/morphology/symmetry/__init__.py`

**Purpose**: Re-export symmetry morph sub-module.

**Exports**: Functions from `features.py`.

---

### `ear/h3/morphology/symmetry/features.py`

**Purpose**: Implement symmetry/shape morphs: M16 curvature, M19 stability, M23 time-reversal symmetry.

**Primary Docs**:
- `Docs/H3/Morphology/Symmetry.md` -- Symmetry category morph formulas
- `Docs/H3/Contracts/MorphComputer.md` -- Section 4: M16, M19, M23 specifications

**Related Docs**:
- `Docs/H3/Morphology/MorphScaling.md` -- M16 signed, M19 unsigned, M23 signed
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 5.1: morph table

**Depends On**: Nothing (pure functions, torch only).

**Exports**:
- `m16_curvature(window, weights)` -> `(B,)` -- `mean(abs(diff(diff(x))))`
- `m19_stability(window, weights)` -> `(B,)` -- `1 / (1 + std(x))`
- `m23_symmetry(window, weights)` -> `(B,)` -- forward/backward correlation

**Key Constraints**:
- M16: curvature = `mean(|diff(diff(x))|)`. **Signed** per MorphScaling.md. Min window = 3.
- M19: stability = `1 / (1 + std(x))`. Unsigned. Min window = 2. Range (0, 1]. Returns 1.0 for constant input.
- M23: time-reversal symmetry = Pearson correlation between first half and reversed second half. **Signed**. Min window = 4. Range [-1, 1].

**Verification Checklist**:
- [ ] M16 returns 0 for linear window (zero curvature)
- [ ] M19 returns 1.0 for constant window
- [ ] M23 returns 1.0 for palindromic window
- [ ] M23 returns -1.0 for anti-symmetric window
- [ ] Min window guards: M16 at 3, M19 at 2, M23 at 4

---

### `ear/h3/morphology/scaling.py`

**Purpose**: Apply MORPH_SCALE normalization to raw morph outputs, dispatching between signed and unsigned formulas.

**Primary Docs**:
- `Docs/H3/Morphology/MorphScaling.md` -- normalization formulas, signed vs unsigned dispatch

**Related Docs**:
- `Docs/H3/Contracts/MorphComputer.md` -- Section 7: normalization not in MorphComputer
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 5.3: MORPH_SCALE values

**Depends On**:
- `ear/h3/constants/scaling.py` (MORPH_SCALE, normalize_unsigned, normalize_signed)
- `ear/h3/constants/morphs.py` (SIGNED_MORPHS)

**Exports**:
- `normalize_morph(raw, morph_idx)` -> normalized value in [0, 1]

**Key Constraints**:
- Dispatches to signed or unsigned formula based on `morph_idx in SIGNED_MORPHS`
- Signed morphs: zero maps to 0.5
- All outputs clamped to [0, 1]
- This is called by the pipeline executor, NOT by MorphComputer

**Verification Checklist**:
- [ ] Signed morph (M8, raw=0) -> 0.5
- [ ] Unsigned morph (M1, raw=0.5) -> 0.5
- [ ] Extreme values clamped to [0, 1]
- [ ] Correct dispatch for all 24 morphs

---

### `ear/h3/morphology/computer.py`

**Purpose**: MorphComputer dispatch table mapping morph indices 0-23 to their computation functions.

**Primary Docs**:
- `Docs/H3/Contracts/MorphComputer.md` -- dispatch table structure, compute() interface, edge cases

**Related Docs**:
- `Docs/H3/Morphology/00-INDEX.md` -- morph category overview
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 5: complete morph table

**Depends On**:
- `ear/h3/morphology/distribution/central.py` (m0, m1, m3)
- `ear/h3/morphology/distribution/spread.py` (m2, m5)
- `ear/h3/morphology/distribution/shape.py` (m4, m6, m7)
- `ear/h3/morphology/dynamics/derivatives.py` (m8-m13)
- `ear/h3/morphology/dynamics/smoothness.py` (m15)
- `ear/h3/morphology/dynamics/trend.py` (m18, m21)
- `ear/h3/morphology/rhythm/periodicity.py` (m14, m17, m22)
- `ear/h3/morphology/information/entropy.py` (m20)
- `ear/h3/morphology/symmetry/features.py` (m16, m19, m23)

**Exports**:
- `MorphComputer` (class)
  - `compute(window, weights, morph_idx)` -> `(B,)` tensor
  - Internal `_dispatch` dict mapping 0-23 to functions

**Key Constraints**:
- Interface: `compute(window: (B, win_len), weights: (win_len,), morph_idx: int) -> (B,)`
- Dispatch table must cover all 24 indices (0 through 23) with no gaps
- Raw output NOT normalized here (normalization is in scaling.py)
- Edge case handling: returns safe defaults for below-minimum windows (zeros or ones)
- Stateless: no mutable state, no parameters

**Verification Checklist**:
- [ ] Dispatch table has exactly 24 entries
- [ ] `compute(window, weights, 0)` returns weighted mean
- [ ] `compute(window, weights, 23)` returns symmetry
- [ ] Invalid morph_idx raises KeyError or ValueError
- [ ] All morph functions accessible via dispatch

---

## P2-H3.4 -- Demand

### `ear/h3/demand/__init__.py`

**Purpose**: Re-export demand-related classes.

**Exports**: `DemandTree`, `EventHorizon`, `aggregate_demands`.

---

### `ear/h3/demand/demand_tree.py`

**Purpose**: DemandTree groups flat 4-tuple demand sets by horizon for attention weight reuse.

**Primary Docs**:
- `Docs/H3/Contracts/DemandTree.md` -- build() interface, grouping semantics, invariants

**Related Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 9: demand aggregation
- `Docs/H3/Pipeline/ExecutionModel.md` -- Phase 2: demand tree construction
- `Docs/H3/Registry/DemandAddressSpace.md` -- 4-tuple system, sparsity analysis

**Depends On**:
- `ear/h3/constants/horizons.py` (N_HORIZONS for validation)
- `ear/h3/constants/morphs.py` (N_MORPHS for validation)
- `ear/h3/constants/laws.py` (N_LAWS for validation)

**Exports**:
- `DemandTree` (class)
  - `build(demand)` -> `Dict[int, Set[Tuple[int, int, int]]]` (static method)
  - `summary(demand)` -> `str` (static method)
  - `unique_horizons()` -> sorted list of horizon indices
  - `tuples_at(horizon)` -> set of (r3_idx, morph, law) triples

**Key Constraints**:
- Input: `Set[Tuple[int,int,int,int]]` -- `{(r3_idx, horizon, morph, law), ...}`
- Output: `{horizon: {(r3_idx, morph, law), ...}}` -- grouped by horizon
- Deduplication is inherent (set semantics)
- Empty demand -> empty tree
- Validation: r3_idx in [0, 127], horizon in [0, 31], morph in [0, 23], law in [0, 2]
- Horizon is primary key because attention weights depend only on horizon

**Verification Checklist**:
- [ ] `build(set())` returns `{}`
- [ ] 3 tuples sharing horizon 4 produce 1 key with 3 entries
- [ ] Duplicate 4-tuples produce single entry (set dedup)
- [ ] Output keys are horizon indices; values are 3-tuples (r3, morph, law)
- [ ] Validation rejects out-of-range indices

---

### `ear/h3/demand/event_horizon.py`

**Purpose**: EventHorizon maps horizon index to physical attributes (frames, ms, seconds, band).

**Primary Docs**:
- `Docs/H3/Contracts/EventHorizon.md` -- constructor, properties, usage pattern

**Related Docs**:
- `Docs/H3/Registry/HorizonCatalog.md` -- complete 32-horizon table
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 4: horizon table

**Depends On**:
- `ear/h3/constants/horizons.py` (HORIZON_FRAMES, HORIZON_MS, BAND_ASSIGNMENTS, N_HORIZONS)

**Exports**:
- `EventHorizon` (class)
  - `__init__(index: int)` -- asserts 0 <= index < 32
  - Properties: `frames` (int), `ms` (float), `seconds` (float), `band` (str)
  - `__repr__()` -> formatted string

**Key Constraints**:
- Pure lookup wrapper; no mutable state
- Raises AssertionError for out-of-range index
- `frames` = `HORIZON_FRAMES[index]`
- `ms` = `HORIZON_MS[index]`
- `seconds` = `ms / 1000.0`
- `band` = `BAND_ASSIGNMENTS[index]`

**Verification Checklist**:
- [ ] `EventHorizon(0).frames` = 1
- [ ] `EventHorizon(31).frames` = 168999
- [ ] `EventHorizon(31).ms` = 981000
- [ ] `EventHorizon(8).band` = "meso"
- [ ] Out-of-range index raises AssertionError

---

### `ear/h3/demand/aggregator.py`

**Purpose**: Aggregate H3DemandSpec tuples from multiple C3 models, deduplicate, and build DemandTree.

**Primary Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 9: demand aggregation pipeline
- `Docs/H3/Registry/DemandAddressSpace.md` -- sparsity analysis, per-unit demand

**Related Docs**:
- `Docs/H3/Demand/SPU-H3-DEMAND.md` through `Docs/H3/Demand/RPU-H3-DEMAND.md` -- per-unit demand
- `Docs/H3/Pipeline/ExecutionModel.md` -- Phase 1: demand collection

**Depends On**:
- `contracts/dataclasses/demand_spec.py` (H3DemandSpec)
- `ear/h3/demand/demand_tree.py` (DemandTree)

**Exports**:
- `aggregate_demands(models)` -> `DemandTree` -- collects from all models, deduplicates, builds tree
- `demand_statistics(demand_set)` -> dict with counts per band, per morph category, total

**Key Constraints**:
- Collects `h3_demand` from each model's property
- Converts H3DemandSpec to 4-tuple via `.as_tuple()`
- Deduplication: same 4-tuple from multiple models computed once
- Expected ~8,600 unique tuples from 96 models
- Returns DemandTree ready for executor

**Verification Checklist**:
- [ ] Deduplication: 2 models demanding same tuple -> 1 entry in tree
- [ ] Empty model list -> empty tree
- [ ] Statistics include per-band counts
- [ ] All H3DemandSpec instances converted via as_tuple()

---

## P2-H3.5 -- Bands

### `ear/h3/bands/__init__.py`

**Purpose**: Re-export band metadata modules.

**Exports**: `MicroBand`, `MesoBand`, `MacroBand`, `UltraBand`, `get_band`.

---

### `ear/h3/bands/micro.py`

**Purpose**: Micro band metadata (H0-H7, 5.8ms-250ms, sensory/sub-beat).

**Primary Docs**:
- `Docs/H3/Bands/Micro/00-INDEX.md` -- Micro band overview
- `Docs/H3/Bands/Micro/H0-H5-SubBeat.md` -- H0-H5 sub-beat horizons
- `Docs/H3/Bands/Micro/H6-H7-BeatSubdivision.md` -- H6-H7 beat subdivision horizons

**Related Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 4.1: Micro band table

**Depends On**:
- `ear/h3/constants/horizons.py` (HORIZON_MS, HORIZON_FRAMES)

**Exports**:
- `MicroBand` (class with metadata: name, horizon_range, musical_character, neuroscience_basis per horizon)

**Key Constraints**:
- Horizons H0-H7 (indices 0-7)
- Duration range: 5.8 ms to 250 ms
- Frame range: 1 to 43
- Musical scale: onset detection through beat subdivision
- Primary mechanisms: PPC (H0, H3, H6), ASA (H3, H6)

**Verification Checklist**:
- [ ] Contains metadata for exactly H0-H7
- [ ] Duration and frame values match architecture doc
- [ ] Musical character descriptions from band docs

---

### `ear/h3/bands/meso.py`

**Purpose**: Meso band metadata (H8-H15, 300ms-800ms, beat/phrase).

**Primary Docs**:
- `Docs/H3/Bands/Meso/00-INDEX.md` -- Meso band overview
- `Docs/H3/Bands/Meso/H8-H11-BeatPeriod.md` -- H8-H11 beat period horizons
- `Docs/H3/Bands/Meso/H12-H15-Phrase.md` -- H12-H15 phrase-level horizons

**Related Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 4.1: Meso band table

**Depends On**:
- `ear/h3/constants/horizons.py` (HORIZON_MS, HORIZON_FRAMES)

**Exports**:
- `MesoBand` (class with metadata)

**Key Constraints**:
- Horizons H8-H15 (indices 8-15)
- Duration range: 300 ms to 800 ms
- Frame range: 52 to 138
- Musical scale: fast beat (200 BPM) through slow tempo (half-note)
- Primary mechanisms: BEP (H6, H9, H11), TPC (H12)

**Verification Checklist**:
- [ ] Contains metadata for exactly H8-H15
- [ ] Duration and frame values match architecture doc
- [ ] Covers preferred tempo zone (100-170 BPM)

---

### `ear/h3/bands/macro.py`

**Purpose**: Macro band metadata (H16-H23, 1s-25s, section/passage).

**Primary Docs**:
- `Docs/H3/Bands/Macro/00-INDEX.md` -- Macro band overview
- `Docs/H3/Bands/Macro/H16-H17-Measure.md` -- H16-H17 measure-level horizons
- `Docs/H3/Bands/Macro/H18-H23-Section.md` -- H18-H23 section-level horizons

**Related Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 4.1: Macro band table

**Depends On**:
- `ear/h3/constants/horizons.py` (HORIZON_MS, HORIZON_FRAMES)

**Exports**:
- `MacroBand` (class with metadata)

**Key Constraints**:
- Horizons H16-H23 (indices 16-23)
- Duration range: 1,000 ms to 25,000 ms
- Frame range: 172 to 4,307
- Musical scale: measure through multi-section span
- Dominates overall demand (~46% of tuples)
- Primary mechanisms: TMH (H16, H18, H20, H22), SYN (H16, H18), C0P (H18, H19, H20)

**Verification Checklist**:
- [ ] Contains metadata for exactly H16-H23
- [ ] Duration and frame values match architecture doc
- [ ] H18 (2s) flagged as most frequently demanded macro horizon

---

### `ear/h3/bands/ultra.py`

**Purpose**: Ultra band metadata (H24-H31, 36s-981s, movement/full work).

**Primary Docs**:
- `Docs/H3/Bands/Ultra/00-INDEX.md` -- Ultra band overview
- `Docs/H3/Bands/Ultra/H24-H28-Movement.md` -- H24-H28 movement horizons
- `Docs/H3/Bands/Ultra/H29-H31-Piece.md` -- H29-H31 full-work horizons

**Related Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 4.1: Ultra band table
- `Docs/H3/Pipeline/WarmUp.md` -- Ultra band warm-up concerns

**Depends On**:
- `ear/h3/constants/horizons.py` (HORIZON_MS, HORIZON_FRAMES)

**Exports**:
- `UltraBand` (class with metadata)

**Key Constraints**:
- Horizons H24-H31 (indices 24-31)
- Duration range: 36,000 ms to 981,000 ms (~16 minutes)
- Frame range: 6,202 to 168,999
- Musical scale: movement through full work
- Sparingly used; primarily by MEM mechanism
- Audio shorter than 2 minutes cannot fully warm Ultra horizons

**Verification Checklist**:
- [ ] Contains metadata for exactly H24-H31
- [ ] Duration and frame values match architecture doc
- [ ] Warm-up warning metadata included

---

## P2-H3.6 -- Pipeline

### `ear/h3/pipeline/__init__.py`

**Purpose**: Re-export pipeline components.

**Exports**: `H3Executor`, `WarmUpHandler`.

---

### `ear/h3/pipeline/executor.py`

**Purpose**: Implement the 7-phase H3 execution loop that processes demands horizon-by-horizon.

**Primary Docs**:
- `Docs/H3/Pipeline/ExecutionModel.md` -- 7 execution phases, data flow, complexity analysis
- `Docs/H3/Contracts/H3Extractor.md` -- Sections 4-5: execution flow and _compute_morph_series

**Related Docs**:
- `Docs/H3/Pipeline/SparsityStrategy.md` -- why only ~2.9% computed
- `Docs/H3/Pipeline/Performance.md` -- cost model and optimization
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 12.4: execution flow pseudocode

**Depends On**:
- `ear/h3/demand/demand_tree.py` (DemandTree)
- `ear/h3/demand/event_horizon.py` (EventHorizon)
- `ear/h3/attention/kernel.py` (AttentionKernel)
- `ear/h3/attention/memory.py` (MemoryWindow)
- `ear/h3/attention/prediction.py` (PredictionWindow)
- `ear/h3/attention/integration.py` (IntegrationWindow)
- `ear/h3/morphology/computer.py` (MorphComputer)
- `ear/h3/morphology/scaling.py` (normalize_morph)
- `ear/h3/pipeline/warmup.py` (WarmUpHandler)

**Exports**:
- `H3Executor` (class)
  - `execute(r3_tensor, demand_tree)` -> `Dict[Tuple[int,int,int,int], Tensor]`

**Key Constraints**:
- 7-phase loop per ExecutionModel.md:
  1. Demand collection (already done by aggregator)
  2. DemandTree construction (already done)
  3. Horizon loop: iterate sorted unique horizons
  4. Window selection: dispatch to L0/L1/L2 window by law
  5. Attention weighting: compute once per horizon, truncate/renormalize per frame
  6. Morph computation: dispatch via MorphComputer
  7. Result packing: store in sparse dict
- Attention weights computed ONCE per horizon, reused across all tuples
- Weight truncation at boundaries: `w = weights[:win_len]; w = w / w.sum().clamp(min=1e-8)`
- Output: `Dict[(r3_idx, h, m, l)] -> Tensor(B, T)`, all values in [0, 1]
- Per-tuple loop: for each t in [0, T), select window, truncate weights, compute morph, normalize

**Verification Checklist**:
- [ ] Iterates horizons in sorted order
- [ ] Attention weights computed once per horizon
- [ ] Law dispatch: L0->MemoryWindow, L1->PredictionWindow, L2->IntegrationWindow
- [ ] Weight renormalization after truncation: `w / w.sum().clamp(min=1e-8)`
- [ ] normalize_morph applied to raw output
- [ ] Output dict keys are 4-tuples, values are (B, T) tensors
- [ ] All output values in [0, 1]

---

### `ear/h3/pipeline/warmup.py`

**Purpose**: Handle warm-up effects at sequence boundaries where attention windows are incomplete.

**Primary Docs**:
- `Docs/H3/Pipeline/WarmUp.md` -- per-law warm-up patterns, duration by band, recommendations

**Related Docs**:
- `Docs/H3/Pipeline/ExecutionModel.md` -- Phase 4-5: window selection and truncation
- `Docs/H3/Contracts/AttentionKernel.md` -- Section 7: normalization deferred to caller

**Depends On**:
- `ear/h3/constants/horizons.py` (HORIZON_FRAMES)
- `ear/h3/constants/laws.py` (law constants)

**Exports**:
- `WarmUpHandler` (class)
  - `warmup_frames(horizon, law)` -> int (number of warm-up frames)
  - `is_warmed(t, horizon, law, T)` -> bool
  - `warmup_fraction(horizon, T)` -> float (fraction of sequence in warm-up)

**Key Constraints**:
- L0 warm-up: first n_frames frames
- L1 warm-up: last n_frames frames
- L2 warm-up: first and last n_frames//2 frames
- No explicit warm-up flag in output (consumers must check)
- Ultra band may never fully warm for short audio
- Zero substitution policy for below-min-window frames

**Verification Checklist**:
- [ ] L0 warm-up at start: `warmup_frames(h, L0)` = HORIZON_FRAMES[h]
- [ ] L1 warm-up at end: `warmup_frames(h, L1)` = HORIZON_FRAMES[h]
- [ ] L2 warm-up at both ends: `warmup_frames(h, L2)` = HORIZON_FRAMES[h] // 2
- [ ] Warm-up fraction correct for various audio lengths

---

## P2-H3.7 -- Orchestrator

### `ear/h3/extractor.py`

**Purpose**: H3Extractor -- top-level orchestrator and sole entry point for H3 temporal context extraction.

**Primary Docs**:
- `Docs/H3/Contracts/H3Extractor.md` -- constructor, extract() method, execution flow, dependencies

**Related Docs**:
- `Docs/H3/H3-TEMPORAL-ARCHITECTURE.md` -- Section 12: code architecture overview
- `Docs/H3/Pipeline/ExecutionModel.md` -- 7-phase pipeline
- `Docs/H3/Pipeline/SparsityStrategy.md` -- sparsity rationale

**Depends On**:
- `ear/h3/demand/aggregator.py` (aggregate_demands)
- `ear/h3/demand/demand_tree.py` (DemandTree)
- `ear/h3/pipeline/executor.py` (H3Executor)
- `ear/h3/morphology/computer.py` (MorphComputer)

**Exports**:
- `H3Extractor` (class)
  - `__init__(config)` -- stores config, instantiates MorphComputer and H3Executor
  - `extract(r3, demand)` -> `Dict[Tuple[int,int,int,int], Tensor]`

**Key Constraints**:
- Input: R3 tensor `(B, T, 128)`, demand set (set of 4-tuples or list of H3DemandSpec)
- Output: sparse dict `{(r3_idx, horizon, morph, law): (B, T)}` with exactly one entry per demanded tuple
- Orchestration: builds DemandTree, delegates to H3Executor
- No GPU allocation at construction time
- Stateless between calls (no frame-to-frame state)
- R3 values in [0, 1] assumed; H3 output values in [0, 1]
- Frame rate inherited from R3: 172.27 Hz

**Verification Checklist**:
- [ ] `extract()` returns dict with one entry per demanded tuple
- [ ] Output tensor shapes are (B, T) matching input R3 tensor
- [ ] Empty demand produces empty dict
- [ ] Duplicate demands in input produce single computation
- [ ] All output values in [0, 1]
- [ ] No GPU allocation at construction

---

### `ear/h3/__init__.py`

**Purpose**: Package init; re-export H3Extractor and key types.

**Exports**:
- `H3Extractor`
- `DemandTree`
- `EventHorizon`
- `MorphComputer`
- `AttentionKernel`

**No primary docs** -- pure re-export module.

---

## Verification Gate G2-H3

After completing all P2-H3 files, run the following verification:

```python
# G2-H3 Verification Script

import torch
from Musical_Intelligence.ear.h3 import (
    H3Extractor, DemandTree, EventHorizon, MorphComputer, AttentionKernel
)
from Musical_Intelligence.ear.h3.constants import (
    HORIZON_MS, HORIZON_FRAMES, BAND_ASSIGNMENTS,
    MORPH_NAMES, MORPH_CATEGORIES, SIGNED_MORPHS, MORPH_SCALE,
    LAW_NAMES, ATTENTION_DECAY, FRAME_RATE,
    N_HORIZONS, N_MORPHS, N_LAWS
)

# --- G2-H3.1: Constants integrity ---
assert N_HORIZONS == 32, f"Expected 32 horizons, got {N_HORIZONS}"
assert N_MORPHS == 24, f"Expected 24 morphs, got {N_MORPHS}"
assert N_LAWS == 3, f"Expected 3 laws, got {N_LAWS}"
assert len(HORIZON_MS) == 32
assert len(HORIZON_FRAMES) == 32
assert len(MORPH_NAMES) == 24
assert len(MORPH_SCALE) == 24
assert len(LAW_NAMES) == 3
assert HORIZON_FRAMES[0] == 1, "H0 should be 1 frame"
assert HORIZON_FRAMES[31] == 168999, "H31 should be 168,999 frames"
assert HORIZON_MS[0] == 5.8, "H0 should be 5.8 ms"
assert HORIZON_MS[31] == 981000, "H31 should be 981,000 ms"
assert ATTENTION_DECAY == 3.0
assert FRAME_RATE == 172.27
assert SIGNED_MORPHS == frozenset({6, 8, 9, 11, 12, 16, 18, 23})
print("G2-H3.1 PASSED: Constants integrity verified")

# --- G2-H3.2: Band assignments ---
assert all(BAND_ASSIGNMENTS[i] == "micro" for i in range(8))
assert all(BAND_ASSIGNMENTS[i] == "meso" for i in range(8, 16))
assert all(BAND_ASSIGNMENTS[i] == "macro" for i in range(16, 24))
assert all(BAND_ASSIGNMENTS[i] == "ultra" for i in range(24, 32))
print("G2-H3.2 PASSED: Band assignments correct")

# --- G2-H3.3: EventHorizon ---
eh0 = EventHorizon(0)
assert eh0.frames == 1
assert eh0.ms == 5.8
eh31 = EventHorizon(31)
assert eh31.frames == 168999
try:
    EventHorizon(32)
    assert False, "Should raise for index 32"
except (AssertionError, ValueError):
    pass
print("G2-H3.3 PASSED: EventHorizon lookups correct")

# --- G2-H3.4: AttentionKernel ---
kernel = AttentionKernel()
w1 = kernel.compute_weights(1)
assert w1.shape == (1,), f"Expected shape (1,), got {w1.shape}"
assert torch.isclose(w1[0], torch.tensor(1.0))
w100 = kernel.compute_weights(100)
assert w100.shape == (100,)
assert torch.isclose(w100[-1], torch.tensor(1.0), atol=1e-6)
assert abs(w100[0].item() - 0.0498) < 0.01, "Boundary weight should be ~5%"
assert all(w100[i] <= w100[i+1] for i in range(99)), "Weights must be monotonically increasing"
print("G2-H3.4 PASSED: AttentionKernel properties verified")

# --- G2-H3.5: MorphComputer ---
mc = MorphComputer()
window = torch.rand(2, 10)  # B=2, win_len=10
weights = torch.ones(10) / 10.0  # uniform weights
for m_idx in range(24):
    result = mc.compute(window, weights, m_idx)
    assert result.shape == (2,), f"Morph {m_idx}: expected (2,), got {result.shape}"
print("G2-H3.5 PASSED: MorphComputer dispatches all 24 morphs")

# --- G2-H3.6: DemandTree ---
demand = {(0, 4, 0, 0), (0, 4, 2, 0), (5, 10, 8, 1)}
tree = DemandTree.build(demand)
assert 4 in tree, "Horizon 4 should be in tree"
assert 10 in tree, "Horizon 10 should be in tree"
assert len(tree[4]) == 2, "Horizon 4 should have 2 entries"
assert len(tree[10]) == 1, "Horizon 10 should have 1 entry"
assert DemandTree.build(set()) == {}
print("G2-H3.6 PASSED: DemandTree grouping correct")

# --- G2-H3.7: H3Extractor end-to-end ---
extractor = H3Extractor()
B, T, D = 2, 100, 128
r3 = torch.rand(B, T, D)
demand = {
    (0, 6, 0, 0),   # roughness, H6 200ms, weighted_mean, memory
    (7, 6, 8, 0),   # amplitude, H6 200ms, velocity, memory
    (0, 16, 14, 2),  # roughness, H16 1s, periodicity, integration
}
h3_output = extractor.extract(r3, demand)
assert isinstance(h3_output, dict), "H3 output should be a dict"
assert len(h3_output) == 3, f"Expected 3 entries, got {len(h3_output)}"
for key, tensor in h3_output.items():
    assert isinstance(key, tuple) and len(key) == 4, f"Key should be 4-tuple: {key}"
    assert tensor.shape == (B, T), f"Value shape should be ({B},{T}), got {tensor.shape}"
    assert tensor.min() >= 0.0 and tensor.max() <= 1.0, f"Values should be in [0,1]: [{tensor.min()}, {tensor.max()}]"
print("G2-H3.7 PASSED: H3Extractor produces sparse dict with correct shapes and ranges")

# --- G2-H3.8: Sparsity check ---
# With only 3 demanded tuples, verify exactly 3 output entries
assert len(h3_output) == len(demand), "Output entries should match demand count"
print("G2-H3.8 PASSED: Sparsity -- output entries equal demand count")

print("\n===== G2-H3 GATE PASSED: All H3 verifications successful =====")
```

### G2-H3 Gate Criteria Summary

| Check | Criterion | Automated |
|-------|-----------|:---------:|
| G2-H3.1 | All constants match doc values (32H, 24M, 3L, MORPH_SCALE, ATTENTION_DECAY) | Yes |
| G2-H3.2 | Band assignments: 8 per band, correct ordering | Yes |
| G2-H3.3 | EventHorizon lookups match horizon tables | Yes |
| G2-H3.4 | AttentionKernel: peak=1.0, boundary~5%, monotonic increasing | Yes |
| G2-H3.5 | MorphComputer dispatches all 24 morphs, correct output shape | Yes |
| G2-H3.6 | DemandTree groups by horizon, deduplicates, handles empty | Yes |
| G2-H3.7 | H3Extractor `extract()` returns `Dict[4-tuple, (B,T)]` in [0,1] | Yes |
| G2-H3.8 | Output sparsity: entries == demanded tuples | Yes |

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
 |         |
 |         +-- depends on: attention, morphology, demand
 |
 +---> ear/h3/extractor.py (H3Extractor)                            [P2-H3.7]
            |
            +-- depends on: pipeline, demand
```

All sub-phases P2-H3.1 through P2-H3.5 can be implemented in parallel (they share only constants). P2-H3.6 requires P2-H3.1 through P2-H3.3. P2-H3.7 requires P2-H3.6.
