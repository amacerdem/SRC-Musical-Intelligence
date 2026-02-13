# R3 v2 Experimental Benchmark Plan

**Phase**: 3C -- Validation Documentation
**Source**: R3-V2-DESIGN.md Section 7, R3-CROSSREF.md Section 7.2

---

## 1. Overview

Six features in R3 v2 require experimental validation because their mel-domain approximations
have uncertain quality relative to established reference methods. Each benchmark defines a
dataset, baseline method, evaluation metric, success threshold, and fallback plan.

---

## 2. Benchmark Specifications

### Test 1: Mel-Based Chroma [49:60] -- Key Detection Accuracy

**Priority**: CRITICAL (H, I groups depend on chroma quality)

| Parameter | Value |
|-----------|-------|
| **Feature** | chroma_C .. chroma_B [49:60] (12D) |
| **Baseline** | librosa.chroma_cqt (CQT-based chroma, gold standard for key detection) |
| **Dataset** | GTZAN (1000 tracks x 30s, 10 genres); Hainsworth key dataset (100 tracks with key annotations) |
| **Metric** | Key detection accuracy = correct key / total tracks |
| **Threshold** | >= 85% accuracy (CQT-based typically achieves ~90%) |
| **Dependency** | F group implementation complete |
| **Estimated duration** | 1 day |

**Test procedure**:
1. Compute mel-based chroma via Gaussian soft-assignment (sigma=0.5 semitone)
2. Apply Krumhansl-Schmuckler key detection (24 key profiles)
3. Compute CQT-based chroma via librosa.chroma_cqt on same audio
4. Apply identical key detection to CQT chroma
5. Compare both against ground truth key annotations
6. Error analysis: identify which keys show largest deviation (expected: low register issues)

**Fallback plan**:
- If accuracy < 85%: tune sigma parameter (grid search 0.3 to 1.0)
- If still insufficient: switch to CQT approach (Option B from R3-CROSSREF.md Decision 1), cost +2ms/frame

---

### Test 2: Melodic Entropy [87] -- IDyOM IC Correlation

**Priority**: MEDIUM (IDyOM data preparation required)

| Parameter | Value |
|-----------|-------|
| **Feature** | melodic_entropy [87] |
| **Baseline** | IDyOM melodic Information Content (gold standard for melodic expectation) |
| **Dataset** | Essen Folksong Collection (6000+ monophonic melodies, MIDI format) |
| **Metric** | Pearson correlation (r) at note-level IC values |
| **Threshold** | r >= 0.7 |
| **Dependency** | I group implementation + Essen dataset prepared as audio |
| **Estimated duration** | 2 days (includes MIDI-to-audio synthesis) |

**Test procedure**:
1. Synthesize MIDI to audio (piano timbre, 44.1 kHz)
2. Compute mel spectrogram, then chroma transition entropy [87]
3. Run IDyOM on original MIDI, extract note-level IC values
4. Align frame-level R3 output to note boundaries (average within each note)
5. Compute Pearson correlation between R3 melodic_entropy and IDyOM IC

**Fallback plan**:
- If r < 0.7: increase transition matrix from 12x12 bigram to 24x24 (octave-aware)
- If still insufficient: extend warm-up from tau=2.0s to tau=4.0s
- Last resort: redefine [87] as "melodic_change_rate" (simpler, always valid)

---

### Test 3: Harmonic Entropy [88] -- Chord Analysis Correlation

**Priority**: MEDIUM (Billboard dataset required)

| Parameter | Value |
|-----------|-------|
| **Feature** | harmonic_entropy [88] |
| **Baseline** | Expert harmonic analysis -- chord change surprise ratings |
| **Dataset** | Billboard dataset (740 tracks with chord annotations) |
| **Metric** | Pearson correlation (r) at chord boundary positions |
| **Threshold** | r >= 0.6 |
| **Dependency** | I group implementation + Billboard chord annotations |
| **Estimated duration** | 1 day |

**Test procedure**:
1. Compute audio -> mel -> chroma -> KL divergence (harmonic_entropy)
2. Extract chord boundary positions from Billboard annotations
3. Compute ground truth surprise: inverse of chord bigram probability in dataset
4. Average frame-level harmonic_entropy within each chord boundary window
5. Compute Pearson correlation

**Fallback plan**:
- If r < 0.6: tune running average tau parameter (1.0s to 4.0s grid search)
- If still insufficient: add chord template matching layer
- Last resort: redefine [88] as "chroma_novelty" (cosine distance from running average)

---

### Test 4: Syncopation Index [68] -- Behavioral Rating Correlation

**Priority**: HIGH (groove and metricality features depend on syncopation quality)

| Parameter | Value |
|-----------|-------|
| **Feature** | syncopation_index [68] |
| **Baseline** | Witek 2014 syncopation degree ratings (behavioral) |
| **Dataset** | Witek corpus (50 drum patterns, rated by participants) |
| **Metric** | Spearman correlation (rho) at pattern level |
| **Threshold** | rho >= 0.7 |
| **Dependency** | G group implementation |
| **Estimated duration** | 1 day |

**Test procedure**:
1. Drum pattern audio -> mel -> onset detection (B[11] threshold=0.3)
2. Onset peaks + tempo_lag -> metrical grid construction (4 hierarchical levels)
3. Apply LHL syncopation formula: sum of metrical weight differences
4. Compute mean syncopation per pattern
5. Compute Spearman correlation with Witek behavioral ratings

**Fallback plan**:
- If rho < 0.7: increase metrical grid resolution from 4 to 8 levels
- If still insufficient: tune onset threshold; improve beat tracking
- Last resort: replace LHL with simplified off-beat energy ratio

---

### Test 5: Groove Index [71] -- Behavioral Groove Ratings

**Priority**: LOW (behavioral groove data is limited)

| Parameter | Value |
|-----------|-------|
| **Feature** | groove_index [71] |
| **Baseline** | Madison 2006 / Janata 2012 groove ratings |
| **Dataset** | Groove MIDI Dataset (1150 MIDI patterns) + Madison groove clips |
| **Metric** | Pearson correlation (r) at clip level |
| **Threshold** | r >= 0.5 |
| **Dependency** | G group implementation + Groove MIDI Dataset |
| **Estimated duration** | 1 day |

**Test procedure**:
1. MIDI -> audio synthesis -> mel -> groove_index computation
2. Compute mean groove_index per clip
3. Correlate with behavioral groove ratings

**Fallback plan**:
- If r < 0.5: optimize composite weights (syncopation, bass, clarity) via grid search
- If still insufficient: use random forest to find best feature combination from G group
- Last resort: redefine [71] as "rhythmic_complexity" (simpler, non-behavioral target)

---

### Test 6: Inharmonicity Index [64] -- essentia Comparison

**Priority**: MEDIUM (independent feature, no downstream dependencies)

| Parameter | Value |
|-----------|-------|
| **Feature** | inharmonicity_index [64] |
| **Baseline** | essentia Inharmonicity (raw audio spectral peak analysis) |
| **Dataset** | NSynth dataset (300k notes, diverse instruments) |
| **Metric** | Pearson correlation (r) at note level |
| **Threshold** | r >= 0.8 |
| **Dependency** | F group implementation |
| **Estimated duration** | 0.5 day |

**Test procedure**:
1. NSynth audio -> mel -> mel-based inharmonicity (K=8 harmonics, argmax f0)
2. NSynth audio -> essentia Inharmonicity (raw audio spectral peaks, ground truth)
3. Per-note average for both methods
4. Compute Pearson correlation

**Fallback plan**:
- If r < 0.8: increase harmonic template from K=8 to K=16 harmonics
- If still insufficient: add parabolic interpolation for mel peak detection
- Last resort: redefine [64] as "spectral_peakiness" (peak/mean energy ratio)

---

## 3. Test Execution Timeline

| Order | Test | Priority | Dependencies | Duration |
|:-----:|------|:--------:|-------------|:--------:|
| 1 | Test 1 (Chroma) | Critical | F group code | 1 day |
| 2 | Test 4 (Syncopation) | High | G group code | 1 day |
| 3 | Test 6 (Inharmonicity) | Medium | F group code | 0.5 day |
| 4 | Test 2 (Melodic entropy) | Medium | I group + Essen dataset | 2 days |
| 5 | Test 3 (Harmonic entropy) | Medium | I group + Billboard dataset | 1 day |
| 6 | Test 5 (Groove) | Low | G group + Groove dataset | 1 day |

**Total estimated duration**: 6.5 days (sequential). Tests 1+6 and 4 can run in parallel (share no dataset dependencies), reducing critical path to ~5 days.

---

## 4. CI Integration Plan

Each benchmark test will be implemented as a pytest test file:

| Test | Test file location | Marker |
|------|-------------------|--------|
| Test 1 | `tests/ear/r3/test_benchmark_chroma.py` | `@pytest.mark.benchmark` |
| Test 2 | `tests/ear/r3/test_benchmark_melodic_entropy.py` | `@pytest.mark.benchmark` |
| Test 3 | `tests/ear/r3/test_benchmark_harmonic_entropy.py` | `@pytest.mark.benchmark` |
| Test 4 | `tests/ear/r3/test_benchmark_syncopation.py` | `@pytest.mark.benchmark` |
| Test 5 | `tests/ear/r3/test_benchmark_groove.py` | `@pytest.mark.benchmark` |
| Test 6 | `tests/ear/r3/test_benchmark_inharmonicity.py` | `@pytest.mark.benchmark` |

Benchmark tests are excluded from the default test suite (`pytest -m "not benchmark"`) due to
large dataset requirements. They run in a dedicated CI stage (Phase 6.6) with dataset access.

---

## 5. Success Matrix

| Outcome | Action |
|---------|--------|
| All 6 tests pass | Proceed to Phase 6.7 integration |
| Critical test (1) fails | Block: apply fallback, re-test before proceeding |
| High test (4) fails | Apply fallback; proceed with caution |
| Medium/Low tests fail | Apply fallback or redefine feature; note in QualityTiers.md |

---

*Source: R3-V2-DESIGN.md Section 7.1-7.2, R3-CROSSREF.md Section 7.2*
