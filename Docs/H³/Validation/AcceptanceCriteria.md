# H3 Acceptance Criteria

> Version 2.0.0 | Updated 2026-02-13

---

## 1. Overview

This document defines pass/fail criteria for H3 outputs across morphs, horizons, and laws. These criteria serve as the acceptance gate during Phase 5 (code implementation) and Phase 6 (formula revision). A compliant H3 implementation must pass all criteria in Sections 2-6 before deployment. Performance criteria (Section 7) are targets, not hard gates, and may be relaxed with documented justification.

All criteria assume inputs are valid R3 feature tensors of shape `(B, T, 128)` with values in [0, 1] and frame rate 172.27 Hz.

---

## 2. Output Range Criteria

Universal invariants that must hold for every H3 output, regardless of morph, horizon, or law.

| ID | Criterion | Requirement | Rationale |
|:--:|-----------|------------|-----------|
| ORC-1 | Value range | All outputs in [0, 1] | MORPH_SCALE normalization guarantee via `clamp()` |
| ORC-2 | NaN freedom | No NaN values in output | Edge case handling in MorphComputer (eps guards) |
| ORC-3 | Inf freedom | No +/-Inf values in output | Clamping in normalization prevents unbounded output |
| ORC-4 | Batch consistency | Same input produces same output | Deterministic computation (no stochastic components) |
| ORC-5 | Law distinctness | L0 != L1 for non-symmetric, non-constant inputs | Causal vs anticipatory windows see different data |
| ORC-6 | Dtype consistency | All outputs are float32 | Tensor dtype contract |
| ORC-7 | Shape consistency | Output shape = (B, T) for each tuple | Per-tuple temporal output matches input length |

**Test procedure**: Generate 1000 random R3 tensors (uniform [0,1], shape (1, 1000, 128)). Compute all ~8,610 demanded tuples. Verify ORC-1 through ORC-7 on every output tensor.

---

## 3. Per-Morph Acceptance Tests

Synthetic test inputs with expected output behavior. Each test uses a single R3 feature (r3_idx=0) at a reference horizon (H10, 86 frames, Meso band) under L0 (Memory) unless otherwise noted.

| ID | Morph | Test Input | Expected Behavior | Tolerance |
|:--:|-------|-----------|-------------------|:---------:|
| MA-01 | M0 (value) | Linear ramp [0 -> 1] | Output = attention-weighted latest value, close to 1.0 | +/- 0.05 |
| MA-02 | M1 (mean) | Constant 0.5 | Output = 0.5 | +/- 0.01 |
| MA-03 | M1 (mean) | Uniform noise [0, 1] | Output in [0.4, 0.6] | statistical |
| MA-04 | M2 (std) | Constant 0.5 | Output = 0.0 | exact |
| MA-05 | M2 (std) | Uniform noise [0, 1] | Output = 0.289 * 4.0 = 1.0 (clamped) | +/- 0.1 |
| MA-06 | M3 (median) | Ramp [0 -> 1] | Output near 0.5 | +/- 0.1 |
| MA-07 | M4 (max) | Ramp [0 -> 1] | Output = 1.0 | exact |
| MA-08 | M5 (range) | Constant | Output = 0.0 | exact |
| MA-09 | M5 (range) | Ramp [0 -> 1] | Output = 1.0 * 2.0 = 1.0 (clamped) | +/- 0.05 |
| MA-10 | M6 (skewness) | Symmetric distribution | Output near 0.5 (zero skew + bias) | +/- 0.05 |
| MA-11 | M6 (skewness) | Right-skewed | Output > 0.5 | directional |
| MA-12 | M7 (kurtosis) | Gaussian-distributed | Output near 0.5 (normal kurtosis + bias) | +/- 0.1 |
| MA-13 | M8 (velocity) | Constant | Output = 0.5 (zero velocity + bias) | +/- 0.01 |
| MA-14 | M8 (velocity) | Linear ramp up | Output > 0.5 (positive velocity) | directional |
| MA-15 | M8 (velocity) | Linear ramp down | Output < 0.5 (negative velocity) | directional |
| MA-16 | M11 (acceleration) | Constant | Output = 0.5 (zero accel + bias) | +/- 0.01 |
| MA-17 | M11 (acceleration) | Quadratic (concave up) | Output > 0.5 (positive acceleration) | directional |
| MA-18 | M14 (periodicity) | Sine wave, period = H10 | Output near 1.0 (strong periodicity) | +/- 0.15 |
| MA-19 | M14 (periodicity) | White noise | Output near 0.0 (no periodicity) | +/- 0.1 |
| MA-20 | M15 (smoothness) | Constant | Output = 0.0 (perfectly smooth) | exact |
| MA-21 | M15 (smoothness) | White noise | Output > 0.0 (rough) | directional |
| MA-22 | M18 (trend) | Ascending ramp | Output > 0.5 (positive trend) | directional |
| MA-23 | M18 (trend) | Descending ramp | Output < 0.5 (negative trend) | directional |
| MA-24 | M18 (trend) | Constant | Output = 0.5 (zero trend + bias) | +/- 0.01 |
| MA-25 | M19 (stability) | Constant | Output near 1.0 (maximum stability) | +/- 0.05 |
| MA-26 | M19 (stability) | White noise | Output < 0.5 (low stability) | directional |
| MA-27 | M20 (entropy) | Constant | Output = 0.0 (zero entropy) | exact |
| MA-28 | M20 (entropy) | Uniform noise | Output > 0.3 (high entropy) | directional |
| MA-29 | M21 (zero_crossings) | Constant 0.5 | Output = 0.0 (no crossings) | exact |
| MA-30 | M22 (peaks) | Sine wave | Output > 0.0 (periodic peaks) | directional |
| MA-31 | M23 (symmetry) | Time-symmetric signal | Output near 0.5 + 0.5 = 1.0 | +/- 0.1 |
| MA-32 | M23 (symmetry) | Strongly asymmetric | Output < 0.5 | directional |

**Tolerance types**:
- `exact`: Must match within floating-point epsilon (1e-6).
- `+/- X`: Absolute deviation from expected value must be less than X.
- `directional`: Output must satisfy the inequality (greater or less than threshold).
- `statistical`: Must hold in expectation over multiple random seeds (95% of trials).

---

## 4. Law Symmetry Tests

These tests verify that the three laws produce correct directional relationships.

| ID | Test | Condition | Expected Result |
|:--:|------|-----------|-----------------|
| LS-01 | L2 symmetry | Time-symmetric input (e.g., palindrome signal) | L2 output = L0 output (both see same distribution) |
| LS-02 | L0 vs L1 asymmetry | Ascending ramp input | L0 != L1 (causal window sees lower values; anticipatory sees higher) |
| LS-03 | L0/L1 mirror | Ascending ramp under L0 vs descending ramp under L0 | Outputs are symmetric around bias (for signed morphs) |
| LS-04 | L1 on ascending = L0 on descending | Same signal, reversed | M1(ramp, L1) should approximate M1(reversed_ramp, L0) |
| LS-05 | L2 on constant | Constant input | L2 = L0 = L1 (all windows see the same constant) |
| LS-06 | Law independence | Arbitrary non-trivial input | L0, L1, L2 produce three distinct outputs |

**Test horizon**: H10 (86 frames, Meso). **Test morph**: M1 (mean) for LS-01 through LS-05; all morphs for LS-06.

**Tolerance**: LS-01 and LS-05 require exact match (within 1e-6). LS-02 and LS-06 require strict inequality. LS-03 and LS-04 require match within +/- 0.05.

---

## 5. Horizon Scaling Tests

These tests verify that morph outputs exhibit scale-appropriate behavior across horizons.

| ID | Test | Morph | Horizons | Expected Behavior |
|:--:|------|-------|----------|-------------------|
| HS-01 | Local vs global mean | M1 | H6 vs H18 | H6 tracks local fluctuations; H18 is smoother. Variance of M1(H6) over time > variance of M1(H18) over time. |
| HS-02 | Local vs global std | M2 | H6 vs H18 | H6 captures local variability; H18 captures section-level variability. Different magnitudes. |
| HS-03 | Periodicity detection | M14 | H3, H9, H18 | Sine wave at 2 Hz (beat rate): M14(H9) should be highest (window spans multiple 500ms cycles). M14(H3) too short; M14(H18) window too long relative to cycle. |
| HS-04 | Trend resolution | M18 | H6 vs H18 | H6 captures note-level trends; H18 captures section-level trends. For a signal with fast local trends but flat global trend: M18(H6) deviates from 0.5; M18(H18) stays near 0.5. |
| HS-05 | Entropy scaling | M20 | H6 vs H18 | Longer windows have more diverse histograms. M20(H18) >= M20(H6) for stationary noise input. |
| HS-06 | Stability scaling | M19 | H6 vs H18 | Longer windows smooth out fluctuations. M19(H18) > M19(H6) for stationary input. |

**Input**: 60-second synthetic signal at 172.27 Hz = 10,336 frames. Signal: sine wave (2 Hz) + slow envelope (0.1 Hz) + Gaussian noise (sigma=0.05).

---

## 6. Attention Kernel Tests

These tests verify the exponential decay kernel `A(dt) = exp(-3|dt|/H)`.

| ID | Test | Expected Result | Tolerance |
|:--:|------|-----------------|:---------:|
| AK-01 | Kernel sum | 0 < sum(A) < H for all horizons H | exact |
| AK-02 | Monotonic decay | A(dt) >= A(dt+1) for all dt >= 0 | exact |
| AK-03 | Center weight | A(0) = 1.0 | exact (1e-8) |
| AK-04 | Boundary weight | A(H) = exp(-3) = 0.04979 | +/- 1e-4 |
| AK-05 | Symmetry (L2) | A(-dt) = A(dt) for all dt | exact (1e-8) |
| AK-06 | Causality (L0) | A(dt) = 0 for dt > 0 (future frames) | exact |
| AK-07 | Anticipation (L1) | A(dt) = 0 for dt < 0 (past frames) | exact |
| AK-08 | Feature independence | Kernel weights are identical for all r3_idx values | exact |
| AK-09 | Morph independence | Kernel weights are identical for all morph values | exact |
| AK-10 | Horizon scaling | Kernel width scales linearly with H | Sum(A) for H_a / Sum(A) for H_b = H_a / H_b +/- 5% |

**Test procedure**: Compute kernel for all 32 horizons. Verify AK-01 through AK-10. For AK-08 and AK-09, verify by comparing kernel arrays across 10 randomly chosen r3_idx and morph values.

---

## 7. Performance Acceptance

| ID | Metric | Threshold | Measured At | Notes |
|:--:|--------|-----------|------------|-------|
| PA-01 | Per-frame latency | < 5 ms | 96-model aggregate demand (~8,610 tuples), batch=1 | Micro-band tuples dominate cost |
| PA-02 | Memory footprint | < 500 MB | Full demand set, batch=1 | Sparse storage; 97% of 294,912 space is unused |
| PA-03 | Output sparsity | > 97% zeros | Full 294,912 theoretical space | Confirmed by DemandTree occupancy (~2.9%) |
| PA-04 | Startup time | < 2 s | DemandTree construction + kernel precomputation | One-time cost at model load |
| PA-05 | Warm-up latency | = max(HORIZON_FRAMES[h]) frames | Per demand set | L0 needs H frames of history before first valid output |
| PA-06 | GPU utilization | > 60% | Batch=8, 96-model demand | Target for GPU-accelerated pipeline |

**Measurement conditions**: Intel/Apple Silicon CPU, single-threaded baseline. GPU targets assume CUDA or MPS backend. All measurements on 60-second audio at 44.1 kHz sample rate.

---

## 8. Regression Test Suite

### 8.1 Synthetic Test Corpus

Five synthetic audio signals covering the primary acoustic conditions:

| Signal | Description | Duration | Key Properties |
|--------|------------|:--------:|----------------|
| S1: Silence | All zeros | 30 s | Tests zero-input handling, NaN-freedom |
| S2: Sine wave | 440 Hz pure tone | 30 s | Tests periodicity detection, constant spectral features |
| S3: White noise | Gaussian, sigma=0.1 | 30 s | Tests statistical morph convergence, entropy |
| S4: Speech | Male speech excerpt | 60 s | Tests natural dynamics, pauses, transients |
| S5: Music | Piano + drums excerpt | 60 s | Tests full complexity: harmony, rhythm, dynamics |

### 8.2 Golden Reference

- Computed once from a known-good H3 implementation (validated against Sections 2-6 above).
- Stored as test fixtures: one `.npz` file per signal, containing all demanded tuple outputs.
- Reference includes: R3 features (input), H3 outputs (expected), and DemandTree specification (demand).
- File format: `test/fixtures/h3_golden_{signal_id}.npz`.

### 8.3 Regression Threshold

| Metric | Threshold | Application |
|--------|:---------:|-------------|
| Max absolute difference | < 1e-6 | Per-element comparison against golden reference |
| Mean absolute difference | < 1e-8 | Aggregate comparison per tuple |
| Output shape match | exact | Tensor dimensions must match reference |
| Demand coverage | 100% | All demanded tuples must be present in output |

### 8.4 Regression Test Execution

For each signal in the corpus:

1. Load R3 features from fixture.
2. Compute all demanded H3 tuples using the implementation under test.
3. Compare each output tensor element-wise against the golden reference.
4. Report: pass/fail per tuple, worst-case absolute error, mean absolute error.
5. Overall pass requires: all tuples pass, all ORC criteria (Section 2) hold.

**Trigger**: Regression tests run on every commit that modifies files in `mi_beta/ear/h3/` or `mi_beta/core/constants.py`.

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| Quality tier framework | [../Standards/MorphQualityTiers.md](../Standards/MorphQualityTiers.md) |
| Temporal resolution standards | [../Standards/TemporalResolutionStandards.md](../Standards/TemporalResolutionStandards.md) |
| Benchmark plan | [BenchmarkPlan.md](BenchmarkPlan.md) |
| Performance characteristics | [../Pipeline/Performance.md](../Pipeline/Performance.md) |
| H3Extractor contract | [../Contracts/H3Extractor.md](../Contracts/H3Extractor.md) |
| MorphComputer contract | [../Contracts/MorphComputer.md](../Contracts/MorphComputer.md) |
| AttentionKernel contract | [../Contracts/AttentionKernel.md](../Contracts/AttentionKernel.md) |
| DemandTree contract | [../Contracts/DemandTree.md](../Contracts/DemandTree.md) |
| H3 code | `mi_beta/ear/h3/` |

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial acceptance criteria (Phase 4H) |
