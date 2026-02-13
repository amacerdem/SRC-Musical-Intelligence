# R3 v2 Acceptance Criteria

**Phase**: 3C -- Validation Documentation
**Source**: R3-V2-DESIGN.md Sections 2, 7; R3-CROSSREF.md Section 7

---

## 1. Universal Quality Gates

Every spectral group (A through K) must pass all six universal gates before acceptance
into the R3 v2 pipeline. Failure on any gate is a hard block.

### Gate 1: Output Shape

```
Requirement: group.compute(mel).shape == (B, T, group.OUTPUT_DIM)
```

| Group | Expected OUTPUT_DIM | Index Range |
|-------|:-------------------:|:-----------:|
| A: Consonance | 7 | [0:7] |
| B: Energy | 5 | [7:12] |
| C: Timbre | 9 | [12:21] |
| D: Change | 4 | [21:25] |
| E: Interactions | 24 | [25:49] |
| F: Pitch & Chroma | 16 | [49:65] |
| G: Rhythm & Groove | 10 | [65:75] |
| H: Harmony & Tonality | 12 | [75:87] |
| I: Information & Surprise | 7 | [87:94] |
| J: Timbre Extended | 20 | [94:114] |
| K: Modulation & Psychoacoustic | 14 | [114:128] |

The concatenated output must be exactly 128D: `torch.cat([A..K], dim=-1).shape == (B, T, 128)`.

### Gate 2: Value Range

```
Requirement: 0.0 <= output <= 1.0 for all features, all frames, all batches
```

- All features are specified to produce values in [0, 1].
- Tonnetz features [76:82] are internally [-1, 1] but mapped to [0, 1] via `(x + 1) / 2`.
- Test with diverse audio: silence, white noise, pure tone, polyphonic music, percussion.

### Gate 3: NaN/Inf Safety

```
Requirement: torch.isfinite(output).all() == True for all test inputs
```

Critical edge cases to test:
- Silent audio (all-zero mel): division-by-zero in normalization formulas
- Single-frame input (T=1): frame diff features must handle gracefully
- Extreme dynamic range: mel values near float32 limits
- Uniform spectrum: entropy features when p_k = 1/128 for all k

### Gate 4: Computation Budget

```
Requirement: group latency <= allocated budget (ms/frame on GPU batch B=8)
```

| Group | Budget (ms/frame) | Measurement Method |
|-------|:-----------------:|-------------------|
| A: Consonance | 0.5 | `torch.cuda.Event` start/end timing |
| B: Energy | 0.5 | Same |
| C: Timbre | 0.5 | Same |
| D: Change | 0.5 | Same |
| E: Interactions | 0.5 | Same |
| F: Pitch & Chroma | 2.0 | Same |
| G: Rhythm & Groove | 2.5 | Same |
| H: Harmony & Tonality | 2.0 | Same |
| I: Information & Surprise | 2.5 | Same |
| J: Timbre Extended | 1.0 | Same |
| K: Modulation & Psychoacoustic | 4.0 (amortized 1.0) | Average over 344 frames (1 hop cycle) |

Total pipeline budget: **< 5.8 ms/frame** (GPU parallel execution, 172.27 Hz frame rate).
With 3-stage DAG parallelism (R3-V2-DESIGN.md Section 1, Decision 5), target is ~4.0 ms/frame.

### Gate 5: Feature Name Registry

```
Requirement: group.FEATURE_NAMES matches FeatureCatalog entry for all features
```

- Each feature name must be unique across all 128 features.
- All names must be snake_case.
- Names must match the canonical list in R3-V2-DESIGN.md Section 2.
- Validation: `assert len(set(all_names)) == 128`

### Gate 6: Benchmark Pass (if applicable)

```
Requirement: Benchmark test passes at specified threshold (see BenchmarkPlan.md)
```

Only applies to features with assigned benchmarks:
- F: chroma [49:60] -- Test 1 (key detection >= 85%)
- F: inharmonicity_index [64] -- Test 6 (r >= 0.8 vs essentia)
- G: syncopation_index [68] -- Test 4 (rho >= 0.7 vs Witek)
- G: groove_index [71] -- Test 5 (r >= 0.5 vs behavioral)
- I: melodic_entropy [87] -- Test 2 (r >= 0.7 vs IDyOM)
- I: harmonic_entropy [88] -- Test 3 (r >= 0.6 vs Billboard)

---

## 2. Per-Group Specific Criteria

### Groups A-E (Existing, v1)

These groups are already implemented. Acceptance criteria for v2 are:
- **No behavioral change**: `v2_output[:, :, 0:49] == v1_output` (bitwise identical)
- **Index preservation**: feature at index `i` in v1 must remain at index `i` in v2
- Phase 6 formula changes have separate acceptance criteria (not in scope for v2 launch)

### Group F: Pitch & Chroma [49:65]

- Chroma [49:60] must L1-normalize to 1.0 per frame: `chroma.sum(dim=-1) == 1.0 +/- 1e-6`
- pitch_height [61] must correlate positively with mel spectral centroid (sanity check)
- inharmonicity_index [64] must produce higher values for piano (K=8) than for sine wave

### Group G: Rhythm & Groove [65:75]

- tempo_estimate [65] must be in [30, 300] BPM range (after denormalization)
- beat_strength [66] must correlate with onset_strength[11] peaks
- Metronome test: 120 BPM metronome -> tempo_estimate should converge to ~0.33 ([120-30]/[300-30])
- syncopation_index [68] must be 0.0 for on-beat-only patterns

### Group H: Harmony & Tonality [75:87]

- key_clarity [75] must be high (> 0.7) for single-key tonal music (Bach chorales)
- tonnetz [76:81] must form circular trajectories for chromatic scales
- voice_leading_distance [82] must be 0.0 for sustained chords (no chroma change)

### Group I: Information & Surprise [87:94]

- All features must respect warm-up: output = 0.0 for first `tau * frame_rate` = 344 frames
- After warm-up, melodic_entropy [87] must be higher for atonal music than tonal music
- spectral_surprise [90] must spike at sudden timbral changes

### Group J: Timbre Extended [94:114]

- MFCC [94:106] must correlate with librosa.feature.mfcc output (r > 0.95 per coefficient)
- spectral_contrast [107:113] must be higher for harmonic sounds than noise

### Group K: Modulation & Psychoacoustic [114:128]

- Modulation features [114:119] must show warm-up period (first 344 frames = 0.0)
- modulation_4Hz [117] must peak for tremolo at 4 Hz (synthesized test signal)
- sharpness_zwicker [122] must increase monotonically with high-frequency content

---

## 3. Regression Test Requirements

### Automated Regression Suite

```
tests/ear/r3/test_regression_v2.py
```

| Test | Description | Input | Expected |
|------|-------------|-------|----------|
| `test_output_shape` | Full pipeline output shape | Random mel (8, 128, 1000) | (8, 1000, 128) |
| `test_value_range` | All values in [0,1] | Diverse audio set (10 clips) | No values outside [0,1] |
| `test_nan_safety` | No NaN/Inf | Edge cases (silence, noise, DC) | All finite |
| `test_v1_preservation` | First 49D unchanged | Swan Lake mel (reference) | Bitwise match with v1 output |
| `test_feature_names` | 128 unique names | Registry freeze | len(set(names)) == 128 |
| `test_group_contiguity` | No gaps in index space | All groups | Boundaries contiguous 0-128 |
| `test_determinism` | Identical output for identical input | Same mel, 3 runs | Max diff < 1e-7 |

### Performance Regression

```
tests/ear/r3/test_performance_v2.py
```

| Test | Description | Input | Expected |
|------|-------------|-------|----------|
| `test_pipeline_latency` | Total extraction time | (8, 128, 10000) | < 5.8 ms/frame average |
| `test_stage1_latency` | Stage 1 groups (A,B,C,D,F,J,K) | (8, 128, 10000) | < 3.5 ms/frame |
| `test_stage2_latency` | Stage 2 groups (E,G,H) | (8, 128, 10000) | < 1.5 ms/frame |
| `test_stage3_latency` | Stage 3 groups (I) | (8, 128, 10000) | < 1.0 ms/frame |

---

## 4. Performance Envelope Tests

Validate R3 v2 under production conditions:

| Scenario | mel Shape | RT Requirement | Pass Criteria |
|----------|-----------|:--------------:|---------------|
| Single stream | (1, 128, T) | 1.0x RT | < 5.8 ms/frame |
| Batch 8 | (8, 128, T) | 1.0x RT per stream | < 5.8 ms/frame average |
| Long audio (10 min) | (1, 128, 103000) | Memory stable | No OOM; RSS < 4 GB |
| Short audio (1 s) | (1, 128, 172) | Correct warm-up | I, K groups handle partial windows |

---

## 5. Acceptance Sign-Off Checklist

Before R3 v2 is accepted into the main pipeline:

- [ ] All 6 universal gates pass for all 11 groups
- [ ] Per-group specific criteria verified
- [ ] Regression test suite passes (0 failures)
- [ ] Performance regression passes on target GPU (NVIDIA RTX 4090 or equivalent)
- [ ] Critical benchmark (Test 1: chroma) passes at >= 85% accuracy
- [ ] High-priority benchmark (Test 4: syncopation) passes or has documented fallback
- [ ] Feature names registered in `mi_beta/ear/r3/_registry.py`
- [ ] Group boundaries match `mi_beta/core/constants.py` definitions
- [ ] `R3_DIM == 128` assertion passes at registry freeze

---

*Source: R3-V2-DESIGN.md Sections 2, 7; R3-CROSSREF.md Section 7*
