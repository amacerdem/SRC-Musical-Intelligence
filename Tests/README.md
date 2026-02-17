# Musical Intelligence -- Test Suite

> **Ozet (Turkish Summary):**
> Bu dizin, Musical Intelligence (MI) projesinin tam test altyapisini icerir.
> Birim testleri, entegrasyon testleri, performans olcumleri, dogrulama testleri
> ve deneysel senaryolar olmak uzere 5 kategori altinda organize edilmistir.
> Tum testler, Audio -> Cochlea(mel) -> R3(97D) -> H3(sparse) -> Brain(1006D)
> boru hattini kapsar. Temel performans referansi Swan Lake (30s) uzerinden
> olusturulmustur: toplam ~149 saniye (H3 darbogaziyla).

---

## Overview

The MI test suite validates the complete auditory-cognitive pipeline from raw
audio to the 1006-dimensional brain output tensor. Tests are organized into
five categories that together ensure correctness, performance, and scientific
validity of the system.

| Category       | Tool   | Focus                                       |
|----------------|--------|---------------------------------------------|
| **Unit**       | pytest | Individual components in isolation           |
| **Integration**| pytest | Cross-module data flow and shape contracts   |
| **Benchmarks** | python | Execution time and memory profiling          |
| **Validation** | python | Scientific invariants and output constraints |
| **Experiments**| python | Exploratory analyses and ablation studies    |

---

## Pipeline Architecture

```
                        Musical Intelligence Pipeline
  ======================================================================

  Audio (.wav/.mp3)
    |
    v
  +------------------+
  |     Cochlea       |   librosa / torchaudio
  |  (Mel Spectrogram)|   sr=44100, hop=256, n_mels=128
  +------------------+   Output: (B, 128, T)  ~172.27 Hz frame rate
    |
    v
  +------------------+
  |       R3          |   9 spectral groups (A-K)
  |  Spectral Extract |   2-stage DAG pipeline + normalization
  +------------------+   Output: (B, T, 97)  values in [0, 1]
    |
    +----------+
    |          |
    v          v
  +------------------+   +------------------+
  |       H3          |   |    Brain (C3)     |
  |  Temporal Morph   |   |  Cognitive Arch   |
  |  (sparse, on-     |   |  10 mechanisms    |
  |   demand)         |   |  9 units (96      |
  |  24 morphs x      |   |    models)        |
  |  32 horizons x    |   |  5 pathways       |
  |  3 laws           |   +------------------+
  +------------------+          |
    |                           |
    +----------+----------------+
               |
               v
          +------------------+
          |   Brain Output    |
          |   (B, T, 1006)   |
          +------------------+

  4-tuple address space: (r3_idx, horizon, morph, law)
  Theoretical H3 space: 97 x 32 x 24 x 3 = 223,488 features
  Sparse execution: only demanded tuples are computed
```

---

## Directory Structure

```
Tests/
|-- README.md               # This file
|-- conftest.py             # Pytest configuration, shared fixtures
|-- fixtures/
|   |-- __init__.py
|   `-- generators.py       # Synthetic data generators for all stages
|
|-- unit/                   # Isolated component tests (pytest)
|   |-- __init__.py
|   |-- test_r3_groups/     # Per-group R3 extraction tests
|   |-- test_r3_pipeline/   # R3 DAG, normalization, registry
|   |-- test_h3_morphs/     # Per-morph H3 computation tests
|   |-- test_h3_pipeline/   # H3 executor, demand tree, warmup
|   |-- test_mechanisms/    # Per-mechanism (10) tests
|   |-- test_models/        # Per-model (96) contract validation
|   `-- test_units/         # Per-unit (9) compute tests
|
|-- integration/            # Cross-module pipeline tests (pytest)
|   |-- __init__.py
|   |-- test_r3_to_h3.py   # R3 output feeds H3 extractor
|   |-- test_h3_to_brain.py # H3+R3 outputs feed BrainOrchestrator
|   |-- test_full_pipeline.py  # End-to-end audio -> 1006D
|   `-- test_demand_flow.py # Demand aggregation across models
|
|-- benchmarks/             # Performance profiling (python scripts)
|   |-- __init__.py
|   |-- bench_r3.py         # R3 extraction timing
|   |-- bench_h3.py         # H3 extraction timing (the bottleneck)
|   |-- bench_brain.py      # Brain forward pass timing
|   |-- bench_full.py       # Full pipeline timing
|   `-- bench_memory.py     # Peak memory usage per stage
|
|-- validation/             # Scientific invariant checks (python)
|   |-- __init__.py
|   |-- val_output_range.py # All outputs in [0, 1]
|   |-- val_r3_groups.py    # 9 groups sum to 97D
|   |-- val_h3_sparsity.py  # Only demanded tuples computed
|   |-- val_brain_dims.py   # 9 units sum to 1006D
|   `-- val_determinism.py  # Same input -> same output
|
|-- experiments/            # Exploratory analyses (python)
|   |-- __init__.py
|   |-- exp_genre_compare.py    # Cross-genre feature distributions
|   |-- exp_demand_coverage.py  # Which H3 tuples are actually used
|   |-- exp_unit_ablation.py    # Impact of disabling individual units
|   `-- exp_temporal_scales.py  # Feature behavior across horizons
|
`-- reports/                # Generated test reports (gitignored)
    |-- benchmark_results/
    `-- validation_logs/
```

---

## How to Run Tests

### Unit and Integration Tests (pytest)

```bash
# Run all pytest-based tests
pytest Tests/ -v

# Run only unit tests
pytest Tests/unit/ -v

# Run only integration tests
pytest Tests/integration/ -v

# Run with coverage
pytest Tests/ --cov=Musical_Intelligence --cov-report=html

# Run a specific test file
pytest Tests/unit/test_mechanisms/test_bep.py -v

# Run tests matching a keyword
pytest Tests/ -k "r3" -v
```

### Benchmarks (standalone python scripts)

```bash
# Full pipeline benchmark
python Tests/benchmarks/bench_full.py

# Individual stage benchmarks
python Tests/benchmarks/bench_r3.py
python Tests/benchmarks/bench_h3.py
python Tests/benchmarks/bench_brain.py

# Memory profiling
python Tests/benchmarks/bench_memory.py
```

### Validation (standalone python scripts)

```bash
# Run all validation checks
python Tests/validation/val_output_range.py
python Tests/validation/val_brain_dims.py
python Tests/validation/val_determinism.py
```

### Experiments (standalone python scripts)

```bash
# Exploratory analysis
python Tests/experiments/exp_demand_coverage.py
python Tests/experiments/exp_genre_compare.py
```

---

## Test Coverage Matrix

| Component              | Unit | Integration | Benchmark | Validation | Experiment |
|------------------------|:----:|:-----------:|:---------:|:----------:|:----------:|
| Cochlea (mel)          |      |     x       |     x     |            |            |
| R3 Groups (A-K)        |  x   |             |     x     |     x      |     x      |
| R3 Pipeline (DAG)      |  x   |     x       |     x     |     x      |            |
| R3 Registry            |  x   |             |           |     x      |            |
| H3 Morphs (24)         |  x   |             |     x     |     x      |     x      |
| H3 Horizons (32)       |  x   |     x       |     x     |            |     x      |
| H3 Laws (3)            |  x   |     x       |           |     x      |            |
| H3 DemandTree          |  x   |     x       |     x     |     x      |     x      |
| H3 Pipeline (7-phase)  |  x   |     x       |     x     |            |            |
| Mechanisms (10)        |  x   |             |     x     |     x      |            |
| Models (96)            |  x   |             |           |     x      |     x      |
| Units (9)              |  x   |     x       |     x     |     x      |     x      |
| Pathways (5)           |  x   |     x       |     x     |            |            |
| BrainOrchestrator      |      |     x       |     x     |     x      |     x      |
| Full Pipeline          |      |     x       |     x     |     x      |     x      |
| Output ranges [0,1]    |      |             |           |     x      |            |
| Determinism            |      |             |           |     x      |            |
| Shape contracts        |  x   |     x       |           |     x      |            |

---

## Performance Baseline

Reference results from **Swan Lake Suite, Op. 20a: I. Scene** (~30 seconds,
T=5168 frames at 172.27 Hz, single CPU, batch size 1):

| Stage    | Wall Time | Frames | ms/frame | Output Shape     | Notes                    |
|----------|-----------|--------|----------|------------------|--------------------------|
| Cochlea  | 1.7 s     | 5168   | 0.33     | (1, 128, 5168)   | librosa mel spectrogram  |
| R3       | 1.2 s     | 5168   | 0.23     | (1, 5168, 97)    | 9 groups, DAG pipeline   |
| H3       | 146 s     | 5168   | 28.25    | sparse dict      | Bottleneck stage         |
| Brain    | 0.16 s    | 5168   | 0.03     | (1, 5168, 1006)  | 10 mechs + 96 models     |
| **Total**| **149 s** | 5168   | 28.84    | (1, 5168, 1006)  | H3 dominates at 98%      |

**Key observations:**
- H3 temporal morphology is the clear bottleneck (98% of total time)
- Brain cognitive computation is remarkably fast at 0.16s for 96 models
- R3 spectral extraction benefits from the 3-stage DAG parallelism
- Cochlea mel extraction is I/O-bound (audio decoding + FFT)

**Target for optimization:** H3 execution can be accelerated via:
1. Horizon-level batching (compute all morphs for a horizon in one pass)
2. GPU acceleration of morph kernels
3. Demand pruning (eliminate redundant tuples)
4. Caching of shared intermediate windows

---

## Fixtures and Synthetic Data

The test suite uses synthetic data generators (`Tests/fixtures/generators.py`)
to create reproducible test inputs without requiring audio files. Key fixtures:

- **`synthetic_mel`**: Random mel spectrogram `(B, 128, T)` for R3 input
- **`synthetic_r3`**: Random R3 tensor `(B, T, 97)` for H3/Brain input
- **`synthetic_r3_v1`**: Random R3 v1 tensor `(B, T, 49)` for legacy Brain input
- **`synthetic_h3`**: Extracted H3 features from synthetic R3 with minimal demand
- **`brain_orchestrator`**: Pre-constructed `BrainOrchestrator` instance

For real-audio tests, place `.wav` files in the `Test-Audio/` directory at the
project root.

---

## Conventions

- **Markers**: Use `@pytest.mark.slow` for tests exceeding 10 seconds
- **Fixtures**: Session-scoped for expensive objects (extractors, orchestrator)
- **Assertions**: Always check tensor shapes, dtypes, and value ranges
- **Naming**: `test_{module}_{behavior}` for test functions
- **Imports**: Use absolute imports from `Musical_Intelligence.*`

---

## Requirements

- Python 3.10+
- PyTorch >= 2.0
- pytest >= 7.0
- librosa (for audio loading in integration tests)
- numpy
