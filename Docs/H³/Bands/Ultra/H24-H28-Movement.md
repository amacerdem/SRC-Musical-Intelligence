# H24-H28: Movement-Level Horizons

**Band**: Ultra (lower)
**Horizons**: H24-H28
**Duration**: 36,000ms - 414,000ms
**Frames**: 6,202-71,319
**Musical scale**: Exposition to full movement (~36s to ~7min)
**Neural correlate**: Infra-slow oscillations (<0.1 Hz), long-term memory retrieval
**Updated**: 2026-02-13

---

## Overview

H24-H28 span the movement-level region of the ultra band, covering durations from about 36 seconds (a short exposition or song introduction) to about 7 minutes (a full movement or complete pop song). Only the MEM mechanism extends into this range, and only at H25 (60s). The primary consumer is IMU, which uses these horizons for form-level processing.

These horizons are characterized by extreme sparsity: few models demand them, few morphs produce meaningful values, and the computational cost of maintaining frame buffers at these scales is substantial.

---

## Per-Horizon Detail

| Horizon | Duration | Frames | Musical Scale | Mechanisms | Units |
|---------|----------|:------:|---------------|------------|-------|
| **H24** | 36,000ms | 6,202 | Exposition (~36s) | -- | IMU |
| **H25** | 60,000ms | 10,336 | 1 minute | MEM | IMU |
| **H26** | 120,000ms | 20,672 | 2 minutes | -- | IMU |
| **H27** | 200,000ms | 34,453 | ~3.3 minutes | -- | IMU |
| **H28** | 414,000ms | 71,319 | ~7 minutes | -- | IMU |

### H24: Exposition (36,000ms, 6,202 frames)

At 36 seconds, H24 captures a short formal section: a classical exposition, a pop verse-chorus cycle, or a jazz head. No dedicated mechanism -- IMU uses this for interpolation between H23 (25s) and H25 (60s).

**Musical examples at this timescale**:
- Pop: Full verse + chorus cycle
- Classical: Sonata exposition (fast movements)
- Jazz: First chorus of a standard

### H25: One Minute (60,000ms, 10,336 frames)

The only mechanism-bearing ultra horizon:

| Mechanism | Role at H25 | Horizon Range |
|-----------|-------------|:-------------:|
| **MEM** | Longest memory encoding window | H18, H20, H22, **H25** |

MEM at H25 represents the system's longest explicit memory encoding span. At 1 minute, the system can encode representations of complete musical sections (verse-chorus-verse, ABA form, rondo episodes). This is MEM's final horizon -- beyond H25, the system must rely on hierarchical aggregation of shorter-horizon memories rather than direct encoding.

**Musical examples at this timescale**:
- Pop: Two verse-chorus cycles
- Classical: Complete slow-movement theme and development
- Jazz: Complete head + one solo chorus

### H26: Two Minutes (120,000ms, 20,672 frames)

At 2 minutes, H26 captures extended formal units: a pop song through its bridge, a classical development section, or two jazz solo choruses. No dedicated mechanism -- IMU interpolates from H25.

### H27: Three Minutes (200,000ms, 34,453 frames)

At ~3.3 minutes, H27 approximates the length of a typical pop single or a classical aria. This is the median length of popular music tracks, making it a natural reference point for "song-length" processing.

### H28: Seven Minutes (414,000ms, 71,319 frames)

At ~7 minutes, H28 captures a full movement of moderate-length classical works, a complete jazz performance, or an extended pop/rock track. This is the practical upper limit for single-movement processing.

**Computational note**: H28 requires 71,319 frames in its buffer. At 128D float32, this is 71,319 x 128 x 4 = ~35 MB per batch element for the raw feature buffer alone.

---

## Morph Relevance

| Morph | Name | H24-H28 Relevance | Notes |
|-------|------|:------------------:|-------|
| M1 | mean | **Meaningful** | Average feature level over movement |
| M2 | std | Marginal | Variability is dominated by section-level contrasts |
| M5 | range | Marginal | Captures extreme values but high noise |
| M18 | trend | **Meaningful** | Overall trajectory of movement (e.g., darkening of timbre across a symphony movement) |
| M19 | stability | **Meaningful** | Consistency across movement (stylistic uniformity) |
| M20 | entropy | Marginal | Distribution complexity, but bin count at these scales is unstable |
| M8 | velocity | Not meaningful | Instantaneous dynamics averaged away |
| M14 | periodicity | Not meaningful | Section-level periodicity is structural, not statistical |

**Practical morph set at H24-H28**: {M1, M18, M19} with optional {M2, M5, M20}

The restriction to three core morphs dramatically reduces computational cost: instead of 24 morph computations per feature, only 3-6 are needed.

---

## Demand Sparsity

The ultra band is extremely sparse. Estimated demand at H24-H28:

| Horizon | Estimated Models | Estimated Tuples | % of System Total |
|---------|:----------------:|:----------------:|:-----------------:|
| H24 | ~5 | ~120 | ~1.4% |
| H25 | ~8 | ~200 | ~2.3% |
| H26 | ~4 | ~80 | ~0.9% |
| H27 | ~3 | ~50 | ~0.6% |
| H28 | ~2 | ~30 | ~0.3% |
| **Total** | | **~480** | **~5.6%** |

Only IMU's form-level models (approximately 5-8 of its 15 models) use these horizons. The demand is concentrated at H25 (MEM) and diminishes rapidly at longer horizons.

---

## Computational Cost Considerations

### Buffer Requirements

| Horizon | Frames | Buffer Size (128D float32) | Per-Batch (B=32) |
|---------|:------:|:--------------------------:|:-----------------:|
| H24 | 6,202 | 3.1 MB | 99 MB |
| H25 | 10,336 | 5.2 MB | 165 MB |
| H26 | 20,672 | 10.3 MB | 331 MB |
| H27 | 34,453 | 17.2 MB | 551 MB |
| H28 | 71,319 | 35.7 MB | 1.1 GB |

**H28 at B=32 requires 1.1 GB** for raw feature buffers alone. This is the primary computational bottleneck of the ultra band and motivates aggressive sparsity strategies:

1. **Demand-driven allocation**: Only allocate buffers for features actually demanded at each horizon
2. **Reduced morph set**: Compute only M1, M18, M19 (not all 24)
3. **Downsampled buffers**: Store every Nth frame rather than every frame (acceptable given that only trend/mean/stability are computed)
4. **Lazy evaluation**: Do not pre-compute ultra-band buffers; only allocate when a model first requests them

### Update Rate

Ultra-band morphs should be updated infrequently:

| Horizon | Recommended Update | Updates per Track (3min) |
|---------|:------------------:|:------------------------:|
| H24 | Every 6,202 frames (~36s) | ~5 |
| H25 | Every 10,336 frames (~60s) | ~3 |
| H26 | Every 20,672 frames (~120s) | ~1 |
| H27 | Every 34,453 frames (~200s) | ~1 (if track is long enough) |
| H28 | Every 71,319 frames (~414s) | 0 (track too short) |

For typical 3-minute tracks, H27-H28 never accumulate a full window. The system should emit partial-window morphs with a confidence flag indicating incomplete data.

---

## Neuroscience Basis

### Infra-Slow Oscillations (<0.1 Hz)

Neural activity at ultra-band timescales corresponds to infra-slow fluctuations (ISFs) observed in resting-state fMRI and EEG. These oscillations modulate:

- **Default mode network activity**: Self-referential processing during music listening
- **Attentional state**: Sustained attention and mind-wandering cycles during long performances
- **Autonomic responses**: Heart rate variability, skin conductance linked to emotional arcs

### Long-Term Memory Retrieval

At movement timescales, the brain retrieves previously encoded musical memories to compare current experience with expectations. This involves:

- **Hippocampal replay**: Pattern completion of previously heard sections
- **Prefrontal evaluation**: Abstract form-level comparison (is this a recapitulation? a development?)
- **Temporal tagging**: Hippocampal time-cells mark the temporal position within the movement

### Form-Level Processing

The ability to perceive large-scale musical form (sonata, rondo, verse-chorus-bridge) likely involves:
- Hierarchical compression: Section-level representations compressed into form-level schemas
- Expectation generation: Predicting formal structure from genre knowledge
- Surprise detection: Registering deviations from expected form

**Research gap**: Very few empirical studies have directly measured neural activity during form-level perception at these timescales. Most evidence comes from behavioral studies (form recognition tasks) rather than neural imaging.

---

## Cross-References

| Document | Location |
|----------|----------|
| Band index | [00-INDEX.md](00-INDEX.md) |
| Section (H18-H23) | [../Macro/H18-H23-Section.md](../Macro/H18-H23-Section.md) |
| Piece (H29-H31) | [H29-H31-Piece.md](H29-H31-Piece.md) |
| MEM mechanism | [../../../C³/Mechanisms/MEM.md](../../../C³/Mechanisms/MEM.md) |
| IMU demand | [../../Demand/IMU-H3-DEMAND.md](../../Demand/IMU-H3-DEMAND.md) |
