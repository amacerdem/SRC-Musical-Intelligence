# H3 Morphology -- Rhythm (M14, M17, M22)

**Version**: 2.0.0
**Category**: Rhythm
**Morphs**: 3 (M14, M17, M22)
**Purpose**: Periodicity, dominant cycle, and event density descriptors for rhythmic feature analysis
**Code reference**: `mi_beta.ear.h3.morph.MorphComputer.compute_M14`, `compute_M17`, `compute_M22`
**Updated**: 2026-02-13

---

## Overview

Rhythm morphs detect and characterize periodic and quasi-periodic structure in R3 features over time. They answer questions about temporal regularity: *Is this feature repeating? How often? How many events occur?* These three morphs work together to provide a compact rhythmic profile -- periodicity strength, dominant period, and event count.

Rhythm morphs are among the most horizon-sensitive in the system. At Micro band (H0-H5), windows are too short to capture meaningful periodic patterns. Reliable rhythm analysis requires Meso horizons (H8+) where multiple beat cycles fit within the window. M14 and M17 ideally need 8+ frames for meaningful autocorrelation, making H5 the practical minimum.

---

## Category Summary

| Index | Name | Min Window | Output Range | Signed | MORPH_SCALE |
|:-----:|------|:----------:|:------------:|:------:|:-----------:|
| M14 | periodicity | 4 | [0, 1] | No | 1.0 |
| M17 | shape_period | 4 | [0, +inf) | No | 100.0 |
| M22 | peaks | 3 | [0, N-2] | No | 10.0 |

---

## M14: periodicity

**Formula**:
```
M14(x) = max(autocorrelation(x)[lag > 0])
```

Where autocorrelation is the normalized autocorrelation function:
```
R(k) = sum((x(t) - mean) * (x(t+k) - mean)) / sum((x(t) - mean)^2)
```

The maximum is taken over all positive lags within the window.

**Computational method**: For windows larger than ~32 frames, autocorrelation is efficiently computed via FFT:
```
R(k) = ifft(|fft(x - mean)|^2) / R(0)
```

For shorter windows, direct computation is used.

**Properties**:
- **Output range**: [0, 1] (autocorrelation is normalized; 1.0 = perfect periodicity)
- **Min window**: 4 frames (technical minimum; practical minimum is 8+ frames)
- **Signed**: No
- **MORPH_SCALE**: 1.0 (already in [0, 1])

**Musical interpretation**: The strength of the dominant periodic pattern in the feature. High periodicity (near 1.0) means the feature is highly regular -- think of a steady drum beat producing periodic energy fluctuations, or a regular tremolo producing periodic amplitude modulation. Low periodicity (near 0.0) means the feature evolves aperiodically -- rubato passages, free-time sections, or noisy signals.

**Horizon sensitivity**:

| Horizon Band | Reliability | What Periodicity Detects |
|-------------|:----------:|-------------------------|
| Micro (H0-H5) | Unreliable | Too few frames; autocorrelation peaks are noise artifacts |
| Micro (H6-H7) | Marginal | Can detect very fast sub-beat oscillation (e.g., tremolo at H6) |
| Meso (H8-H15) | Good | Beat-level periodicity: is there a regular pulse? |
| Macro (H16-H23) | Excellent | Section-level periodicity: are phrases repeating? |
| Ultra (H24+) | Good | Movement-level periodicity: large-scale structural repetition |

**Common use cases**:
- BEP: Beat periodicity strength at H9-H12 -- core input for beat entrainment
- TMH: Phrase-level repetition detection at H18-H22
- STU: Structural periodicity for form analysis (verse-chorus alternation at Macro horizons)
- MPU: Motor entrainment strength -- high periodicity enables strong motor coupling

**Relationship to M17 (shape_period)**: M14 measures *how periodic* the feature is (strength); M17 measures *at what period* it repeats (dominant cycle duration). Together they answer "Is it periodic?" and "If so, how fast?"

---

## M17: shape_period

**Formula**:
```
M17(x) = mean zero-crossing interval of velocity signal
```

Computed as:
1. Compute velocity: `v(t) = x(t) - x(t-1)`
2. Identify zero crossings of v (where v changes sign)
3. Compute the mean interval (in frames) between consecutive zero crossings
4. Double the result (a full cycle has two zero crossings)

**Properties**:
- **Output range**: [0, +inf) -- output is in frames
- **Min window**: 4 frames (need at least 2 velocity values and 1 zero crossing)
- **Signed**: No
- **MORPH_SCALE**: 100.0 (divides by 100 to normalize; assumes periods up to ~100 frames map to [0, 1])

**Musical interpretation**: The dominant oscillation period of the feature, expressed as a fraction of the MORPH_SCALE reference. At Meso horizons on energy features, shape_period captures the effective beat period -- the time between successive energy peaks. At Macro horizons, shape_period captures phrase length or harmonic rhythm period.

**Horizon sensitivity**:

| Horizon Band | Reliability | Practical Notes |
|-------------|:----------:|-----------------|
| Micro (H0-H5) | Unreliable | Too few samples; often returns 0 or degenerate values |
| Micro (H6-H7) | Marginal | Can detect fast oscillations but resolution is poor |
| Meso (H8-H15) | Good | Captures beat-level period; best when window contains 2+ full cycles |
| Macro (H16-H23) | Excellent | Captures phrase/section period; many cycles available |
| Ultra (H24+) | Good | Large-scale structural period |

**MORPH_SCALE note**: Unlike most morphs whose raw output naturally spans a bounded range, M17 outputs a frame count. The MORPH_SCALE value of 100.0 means that periods up to 100 frames (~580 ms, roughly matching a 103 BPM beat) map to [0, 1]. Periods longer than 100 frames are clamped to 1.0. This scaling is preliminary and subject to recalibration in Phase 5.

**Common use cases**:
- BEP: Beat period estimation at Meso horizons -- core input for tempo tracking
- TMH: Phrase period estimation at Macro horizons for hierarchical form analysis
- SYN: Temporal synchronization -- matching periods across different R3 features

**Relationship to M14 (periodicity)**: M14 gives the strength of periodicity (how regular); M17 gives the period (how fast). A high M14 with M17 = 60 frames (~350 ms) indicates a strong, regular beat at about 170 BPM.

---

## M22: peaks

**Formula**:
```
M22(x) = count of local maxima in window
```

A frame `x(t)` is a local maximum if `x(t) > x(t-1)` and `x(t) > x(t+1)`.

**Properties**:
- **Output range**: [0, N-2] (first and last frames cannot be local maxima)
- **Min window**: 3 frames (need at least 3 values to detect a peak)
- **Signed**: No
- **MORPH_SCALE**: 10.0 (count-valued; `raw / 10.0` normalizes typical range to [0, 1])

**Musical interpretation**: Event density -- how many distinct peak events occur within the window. High peak count indicates a rhythmically dense passage with many transient events (e.g., rapid drum rolls, dense ornamentation). Low peak count indicates sparse events (e.g., sustained tones, long notes). At Meso horizons on energy features, peaks approximately counts the number of note onsets within a beat period. At Macro horizons, peaks on energy features counts the number of accent events within a section.

**Horizon sensitivity**:

| Horizon Band | Reliability | Practical Notes |
|-------------|:----------:|-----------------|
| Micro (H0-H2) | Unreliable | Too few frames to identify meaningful peaks |
| Micro (H3-H7) | Valid | Counts sub-beat events (onsets, transients) |
| Meso (H8-H15) | Good | Counts beat-level events (note onsets per beat) |
| Macro (H16-H23) | Excellent | Counts section-level events (phrases, accents) |
| Ultra (H24+) | Good | Counts movement-level events (sections, climaxes) |

**Common use cases**:
- AED: Arousal detection via event density at H6 and H16
- CPD: Change point detection -- sudden shift in peak density signals a structural boundary
- BEP: Rhythmic density measurement for entrainment complexity

**Relationship to M21 (zero_crossings)**: Peaks count local maxima; zero_crossings count mean-crossings. For a sinusoidal signal, peaks per window = zero_crossings / 2. For more complex signals, the relationship varies. Peaks are more sensitive to transient events; zero_crossings provide a smoother oscillation measure.

---

## Rhythm Morph Interactions

The three rhythm morphs provide complementary information:

```
M14 (periodicity):  "Is it periodic?"        strength [0,1]
M17 (shape_period): "At what period?"         duration (frames)
M22 (peaks):        "How many events?"        count [0,N-2]
```

**Typical combinations**:

| M14 | M17 | M22 | Musical Interpretation |
|:---:|:---:|:---:|----------------------|
| High | Consistent | Moderate | Regular rhythmic pattern (steady beat) |
| High | Consistent | High | Fast, regular pattern (subdivided beat, tremolo) |
| Low | Inconsistent | High | Dense but irregular events (free rhythm, noise) |
| Low | Inconsistent | Low | Sparse, aperiodic events (rubato, sustained tones) |
| High | Consistent | Low | Slow, regular pulsation (half notes, slow tempo) |

---

## Cross-References

| Related Document | Location |
|-----------------|----------|
| Morph catalog (compact reference) | [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md) |
| MORPH_SCALE calibration | [MorphScaling.md](MorphScaling.md) |
| H3 architecture (morph axis) | [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) |
| Morphology index | [00-INDEX.md](00-INDEX.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |
| Beat entrainment (BEP) mechanism | [../../C3/Mechanisms/BEP.md](../../C3/Mechanisms/BEP.md) |
| MorphComputer implementation | `mi_beta/ear/h3/morph.py` |
