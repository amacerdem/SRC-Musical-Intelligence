# H3 Benchmark Plan

> Version 2.0.0 | Updated 2026-02-13

## 1. Overview

This document defines the benchmark methodology for measuring H3 engine performance (latency, throughput, memory) and accuracy (morph correctness, attention kernel fidelity, law enforcement). Benchmarks run on standardized hardware and input configurations to produce reproducible, comparable results across development iterations.

All benchmarks target the H3Extractor pipeline end-to-end: from R3 tensor input through DemandTree grouping, attention weight computation, morph evaluation, and sparse output assembly. Individual components (attention kernel, morph functions, DemandTree construction) are also benchmarked in isolation to identify bottlenecks.

---

## 2. Hardware Configuration

### 2.1 Reference Hardware

| Component | Specification |
|-----------|--------------|
| Processor | Apple M-series (M1/M2/M3) |
| GPU backend | MPS (Metal Performance Shaders) |
| Memory | >= 16 GB unified memory |
| Storage | SSD (NVMe) for dataset I/O |
| OS | macOS 14+ (Sonoma) |

### 2.2 Execution Modes

| Mode | Backend | Purpose |
|------|---------|---------|
| MPS | `torch.device("mps")` | Primary benchmark mode. All tensors on Metal GPU. |
| CPU | `torch.device("cpu")` | Compatibility baseline and regression detection. |

MPS benchmarks are the reference numbers. CPU benchmarks serve as a lower bound and compatibility check. All reported metrics include the execution mode.

---

## 3. Input Configurations

| Config | Description | R3 Shape | Duration | Total Frames |
|--------|-------------|----------|----------|:------------:|
| Micro | 5-second clip | (1, 862, 128) | 5 s | 862 |
| Standard | 30-second clip | (1, 5168, 128) | 30 s | 5,168 |
| Long | 3-minute clip | (1, 31036, 128) | 180 s | 31,036 |
| Ultra | 16-minute piece | (1, 165414, 128) | 960 s | 165,414 |
| Batch | 8x standard clips | (8, 5168, 128) | 30 s x 8 | 41,344 |

Frame count derived from `duration * 172.27 Hz` (rounded to nearest integer). All inputs are synthetic R3 tensors with values drawn from `Uniform(0, 1)` to avoid NaN paths during benchmarking. Real audio inputs are used separately for accuracy benchmarks (Section 5).

---

## 4. Performance Benchmarks

### 4.1 Latency Benchmarks

**Per-frame latency**: Time to compute all demanded H3 tuples for a single frame, averaged over 1000 frames from the middle of the Standard config sequence (avoiding warm-up boundary effects).

| Metric | Target (MPS) | Target (CPU) |
|--------|:------------:|:------------:|
| Mean per-frame latency (full demand, 8,610 tuples) | < 5 ms | < 20 ms |
| Mean per-frame latency (v1-only demand, 5,210 tuples) | < 3 ms | < 12 ms |
| P99 per-frame latency | < 2x mean | < 2x mean |

**Breakdown dimensions**:

- Per-horizon latency: individual timing for each of 32 horizons.
- Per-band latency: aggregated Micro / Meso / Macro / Ultra.
- Per-morph latency: averaged across all horizons and features for each of 24 morphs.
- Per-law latency: L0 vs L1 vs L2 overhead comparison (should be near-identical).

### 4.2 Throughput Benchmarks

**Frames per second**: Total output frames produced divided by wall-clock time for end-to-end extraction.

| Config | Target FPS (MPS) | Real-Time Ratio | Notes |
|--------|:-----------------:|:---------------:|-------|
| Micro | > 300 | > 1.74x | Small sequence, setup overhead visible |
| Standard | > 200 | > 1.16x | Primary benchmark target |
| Long | > 180 | > 1.04x | Memory pressure begins |
| Ultra | > 100 | > 0.58x | Sub-real-time acceptable for Ultra-band cost |
| Batch | > 250 per item | > 1.45x | GPU parallelism benefit |

For each config, report: fps, real-time ratio, bottleneck horizon (the horizon consuming the most wall time), and bottleneck band.

### 4.3 Memory Benchmarks

**Peak GPU memory**: Maximum allocated GPU memory during full extraction.

| Config | Target Peak Memory |
|--------|:------------------:|
| Micro | < 100 MB |
| Standard | < 500 MB |
| Long | < 2 GB |
| Ultra | < 6 GB |
| Batch | < 4 GB |

**Tracked allocations**:

| Component | Measurement |
|-----------|-------------|
| R3 input tensor | `B * T * 128 * 4` bytes |
| Attention weights cache | Sum of all horizon weight vectors (fixed ~760 KB) |
| Morph output buffer | `num_tuples * T * 4` bytes |
| DemandTree overhead | Python dict + horizon groupings (CPU-side) |
| Working memory (windows) | Largest materialized window per horizon |

---

## 5. Accuracy Benchmarks

### 5.1 Morph Accuracy

Compare MorphComputer output for each of the 24 morphs against a NumPy reference implementation operating on the same windowed, weighted input.

**Synthetic test signals** (per feature channel):

| Signal | Description | Purpose |
|--------|-------------|---------|
| Constant | `x(t) = 0.5` | Zero variance: test M2(std), M5(range), M8(velocity) edge cases |
| Sine | `x(t) = 0.5 + 0.4*sin(2*pi*f*t)` | Known periodicity for M14, known shape for M6/M7 |
| Ramp | `x(t) = t / T` | Known trend for M18, known velocity for M8 |
| Noise | `x(t) ~ Uniform(0,1)` | Expected M20(entropy) near maximum, M19(stability) near minimum |
| Impulse | `x(t) = delta(t - T/2)` | Edge case for M22(peaks), M5(range) |
| Step | `x(t) = 0 for t < T/2, 1 otherwise` | Discontinuity test for M15(smoothness), M21(zero_crossings) |

**Accuracy metrics per morph**:

| Metric | Target |
|--------|:------:|
| Max absolute error vs NumPy reference | < 1e-5 |
| Mean absolute error vs NumPy reference | < 1e-7 |
| Pearson correlation vs NumPy reference | > 0.999999 |

### 5.2 Attention Kernel Accuracy

Compare `compute_attention_weights(h)` output against the analytical formula `A(dt) = exp(-3|dt|/H)` computed in float64.

| Metric | Target |
|--------|:------:|
| Max absolute error | < 1e-7 |
| Boundary weight accuracy (H >= 8) | Within 0.01% of analytical ~4.98% |
| Weight normalization (sum to 1.0) | Residual < 1e-6 |

Test across all 32 horizons. Flag any horizon where float32 precision degrades beyond target.

### 5.3 Law Correctness

Verify temporal direction enforcement for each law:

| Law | Verification | Test Signal |
|-----|-------------|-------------|
| L0 (Memory) | Output at frame `t` depends only on frames `[t-H+1, t]` | Ascending ramp: L0 mean < 0.5 at midpoint |
| L1 (Prediction) | Output at frame `t` depends only on frames `[t, t+H-1]` | Ascending ramp: L1 mean > 0.5 at midpoint |
| L2 (Integration) | Output at frame `t` depends on frames `[t-H/2, t+H/2]` | Ascending ramp: L2 mean = 0.5 at midpoint |

Additional checks:
- L0 output != L1 output for any asymmetric signal. If equal, flag as error.
- L2 output is symmetric: reversing the input time axis yields the same output (reversed).
- All three laws produce identical output on a constant signal.

---

## 6. Scaling Analysis

### 6.1 Demand Scaling

Measure throughput as the demand set size varies, holding input config at Standard.

| Demand Size | Description |
|:-----------:|-------------|
| 100 | Minimal demand (single model equivalent) |
| 500 | Small unit demand |
| 1,000 | Medium unit demand |
| 5,000 | Approximate v1 total demand |
| 8,610 | Full v2 demand |

Plot: throughput (fps) vs demand size. Expected behavior: near-linear degradation due to horizon-keyed grouping (tuples sharing a horizon share the attention weight computation).

### 6.2 Horizon Scaling

Measure per-horizon morph computation cost as window size increases, using a fixed single morph (M0: value) and single law (L0) across all 32 horizons.

| Metric | Expected Behavior |
|--------|-------------------|
| Latency vs horizon index | Monotonically increasing, sub-linear with unfold optimization |
| Memory vs horizon index | Linear in `n_frames_h` |
| Crossover point | Identify horizon where GPU becomes faster than CPU |

Plot: per-tuple latency vs `n_frames_h` (1 to 169,043) on log-log scale.

### 6.3 Batch Scaling

Measure throughput per item as batch size varies, holding input config at Standard.

| Batch Size | Total Frames |
|:----------:|:------------:|
| 1 | 5,168 |
| 2 | 10,336 |
| 4 | 20,672 |
| 8 | 41,344 |
| 16 | 82,688 |

Plot: throughput per item vs batch size. Expected: improvement up to GPU saturation point, then plateau or slight degradation due to memory bandwidth.

---

## 7. Benchmark Reporting

### 7.1 Output Format

Results are stored in `benchmarks/h3/` (to be created during Phase 5 implementation).

```
benchmarks/h3/
|-- results/
|   |-- latency_{timestamp}.json
|   |-- throughput_{timestamp}.json
|   |-- memory_{timestamp}.json
|   |-- accuracy_{timestamp}.json
|   |-- scaling_{timestamp}.json
|-- plots/
|   |-- throughput_vs_demand.html
|   |-- latency_vs_horizon.html
|   |-- batch_scaling.html
```

### 7.2 JSON Metadata

Every result file includes:

```json
{
  "metadata": {
    "hardware": "Apple M3 Pro, 18GB",
    "backend": "mps",
    "torch_version": "2.x.x",
    "git_commit": "abc1234",
    "date": "2026-xx-xx",
    "demand_set": "v2_full_8610",
    "input_config": "Standard"
  },
  "results": { ... }
}
```

### 7.3 Visualization

Scaling analysis plots use Plotly for interactive HTML charts. Summary tables are generated as Markdown for inclusion in CI reports.

---

## 8. Cross-References

| Related Document | Location |
|-----------------|----------|
| Performance characteristics | [../Pipeline/Performance.md](../Pipeline/Performance.md) |
| Sparsity strategy | [../Pipeline/SparsityStrategy.md](../Pipeline/SparsityStrategy.md) |
| Execution model | [../Pipeline/ExecutionModel.md](../Pipeline/ExecutionModel.md) |
| Warm-up behavior | [../Pipeline/WarmUp.md](../Pipeline/WarmUp.md) |
| Acceptance criteria | [AcceptanceCriteria.md](AcceptanceCriteria.md) |
| Morph quality tiers | [../Standards/MorphQualityTiers.md](../Standards/MorphQualityTiers.md) |
| Temporal resolution standards | [../Standards/TemporalResolutionStandards.md](../Standards/TemporalResolutionStandards.md) |
| MorphComputer contract | [../Contracts/MorphComputer.md](../Contracts/MorphComputer.md) |
| AttentionKernel contract | [../Contracts/AttentionKernel.md](../Contracts/AttentionKernel.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |
| H3 code | `mi_beta/ear/h3/` |

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial benchmark plan (Phase 4H) |
