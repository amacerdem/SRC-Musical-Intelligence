# H29-H31: Piece-Level Horizons

**Band**: Ultra (upper boundary)
**Horizons**: H29-H31
**Duration**: 600,000ms - 981,000ms
**Frames**: 103,359-168,999
**Musical scale**: 10 minutes to 16 minutes (full piece/act)
**Neural correlate**: Infra-slow oscillations, narrative-level processing
**Updated**: 2026-02-13

---

## Overview

H29-H31 represent the maximum temporal context in the H3 system. These horizons span 10-16 minutes, covering full musical pieces, opera scenes, or the first act of multi-movement works. This is the sparsest and least empirically grounded region of the temporal architecture.

**Current status**: No mechanism or unit assignments exist at H29-H31. Fewer than 10 models across the entire system are expected to use these horizons, even in the fully populated architecture. These horizons exist primarily as reserved capacity for future research into long-form musical cognition.

---

## Per-Horizon Detail

| Horizon | Duration | Frames | Musical Scale | Mechanisms | Units |
|---------|----------|:------:|---------------|------------|-------|
| **H29** | 600,000ms | 103,359 | 10 min (full sonata movement) | -- | -- |
| **H30** | 800,000ms | 137,812 | ~13 min (extended movement) | -- | -- |
| **H31** | 981,000ms | 168,999 | ~16 min (maximum system context) | -- | -- |

### H29: Ten Minutes (600,000ms, 103,359 frames)

At 10 minutes, H29 captures a complete sonata movement, a full jazz set piece, or a long pop/rock composition. This is approximately the length of a "typical" extended classical movement (e.g., Beethoven sonata first movement, Mozart concerto slow movement).

**Musical examples at this timescale**:
- Classical: Complete sonata-allegro movement
- Jazz: Extended performance with multiple solo choruses
- Progressive rock: Full suite (e.g., "Close to the Edge" side one)

### H30: Thirteen Minutes (800,000ms, 137,812 frames)

At ~13 minutes, H30 approaches the length of extended symphonic movements (Mahler adagios, Bruckner slow movements). Very few musical units smaller than a complete piece reach this duration.

### H31: System Maximum (981,000ms, 168,999 frames)

H31 at ~16 minutes represents the absolute upper boundary of the H3 system's temporal context. This horizon was chosen to accommodate:
- Extended symphonic movements (up to ~20 min, partially captured)
- Complete pop/rock albums sides (~16 min typical)
- Extended jazz performances

**Design decision**: The 981s (~16 min) upper limit was set as a practical compromise. Musical works longer than 16 minutes (symphonic movements >20 min, opera acts, full albums) require piece-level chunking strategies rather than single-window processing.

---

## Morph Relevance

At piece-level timescales, only the most basic aggregates are meaningful:

| Morph | Name | Relevance | Notes |
|-------|------|:---------:|-------|
| M1 | mean | **Meaningful** | Piece-level average (overall character) |
| M18 | trend | **Meaningful** | Overall arc of the piece (e.g., gradual brightening) |
| M19 | stability | **Meaningful** | Consistency of the piece (stylistic coherence) |
| M2 | std | Marginal | Overall contrast level |
| All others | -- | Not meaningful | Noise dominates signal at 10+ minutes |

**Practical morph set**: {M1, M18, M19} -- three morphs only.

---

## Demand Sparsity

H29-H31 are the emptiest horizons in the H3 system:

| Horizon | Estimated Models | Estimated Tuples | % of System Total |
|---------|:----------------:|:----------------:|:-----------------:|
| H29 | ~2 | ~20 | ~0.2% |
| H30 | ~1 | ~10 | ~0.1% |
| H31 | ~1 | ~5 | ~0.06% |
| **Total** | | **~35** | **~0.4%** |

Combined, H29-H31 account for fewer than 40 tuples out of ~8,600 system-wide. Most models that operate at ultra timescales terminate at H25 (MEM) or H28 (IMU interpolation).

---

## Computational Notes

### Buffer Requirements

| Horizon | Frames | Buffer Size (128D float32) | Per-Batch (B=32) |
|---------|:------:|:--------------------------:|:-----------------:|
| H29 | 103,359 | 51.7 MB | **1.6 GB** |
| H30 | 137,812 | 68.9 MB | **2.2 GB** |
| H31 | 168,999 | 84.5 MB | **2.7 GB** |

**H31 requires ~1 GB per batch element** for full morph computation over all 128 features. At B=32, this exceeds 2.7 GB -- a significant memory allocation.

### Memory Optimization Strategies

Given the extreme sparsity and limited morph palette, several optimization strategies should be applied:

1. **Feature-sparse buffers**: Only allocate buffers for the handful of features actually demanded (likely <10 features at these horizons), reducing memory by ~10x
2. **Downsampled storage**: Store every 100th frame (1.7 Hz effective rate) rather than every frame. For M1 (mean) and M19 (stability), this introduces negligible error. For M18 (trend), linear regression over downsampled points is equivalent to the full computation.
3. **Streaming statistics**: Compute M1 (mean) and M2 (std) using Welford's online algorithm, requiring O(1) storage per feature regardless of horizon length
4. **Lazy allocation**: Only allocate H29-H31 buffers if a model explicitly demands them, which fewer than 10 models ever will

With these optimizations, effective memory cost per batch element can be reduced from ~85 MB to under 1 MB.

### Piece-Length Constraints

Many musical inputs will be shorter than H29-H31 horizons:

| Track Length | H29 Coverage | H30 Coverage | H31 Coverage |
|:------------:|:------------:|:------------:|:------------:|
| 3 min | 30% | 23% | 18% |
| 5 min | 50% | 38% | 31% |
| 10 min | 100% | 77% | 61% |
| 16 min | 100% | 100% | 98% |

For tracks shorter than the horizon, the system should:
- Emit partial-window morphs with a completeness flag
- Weight M18 (trend) and M19 (stability) by the fraction of the window filled
- Never extrapolate beyond observed data

---

## Known Limitations

### Empirical Research Gap

Very few empirical studies have directly investigated temporal integration at 10+ minute timescales in music perception. Existing evidence is limited to:
- Behavioral studies of large-scale form recognition (e.g., can listeners identify sonata recapitulation?)
- Self-report emotional arc studies (e.g., continuous valence/arousal ratings over full pieces)
- Limited fMRI studies using long musical stimuli (typically <10 min due to scanner constraints)

**Implication**: The theoretical basis for H29-H31 is weaker than for shorter horizons. These horizons should be treated as speculative and subject to revision as empirical data accumulates.

### Piece-Level Chunking

For works longer than 16 minutes (the H31 limit), the system cannot capture the full piece in a single temporal window. Possible strategies for future development:

1. **Hierarchical chunking**: Process 16-minute chunks sequentially, building a higher-level representation from chunk-level summaries
2. **Movement-level memory**: Use MEM at H25 (60s) as the primary ultra-band encoding, and build piece-level representations by aggregating movement-level memories
3. **Attention-gated replay**: Process the full piece at shorter horizons (H20-H22) with periodic "replay" passes that revisit earlier sections

These strategies are deferred to future phases of development.

### Stationarity Assumption

All H3 morph computations assume local stationarity within the analysis window. At H29-H31, this assumption is strongly violated -- a 10-minute window may contain tempo changes, key changes, instrumentation changes, and formal transitions. Statistical morphs computed over such non-stationary signals should be interpreted with caution.

---

## Future Directions

1. **Empirical validation**: Partner with music cognition labs to study neural activity during extended listening (>10 min)
2. **Chunking strategies**: Develop and test piece-level chunking algorithms
3. **Adaptive horizons**: Consider making H29-H31 adaptive rather than fixed, adjusting to the actual piece length
4. **Cross-piece memory**: Extend the MEM mechanism to operate across pieces (album-level, concert-level), though this would require architectural changes beyond H3

---

## Cross-References

| Document | Location |
|----------|----------|
| Band index | [00-INDEX.md](00-INDEX.md) |
| Movement (H24-H28) | [H24-H28-Movement.md](H24-H28-Movement.md) |
| Section (H18-H23) | [../Macro/H18-H23-Section.md](../Macro/H18-H23-Section.md) |
| MEM mechanism | [../../../C³/Mechanisms/MEM.md](../../../C³/Mechanisms/MEM.md) |
| IMU demand | [../../Demand/IMU-H3-DEMAND.md](../../Demand/IMU-H3-DEMAND.md) |
| H3 master index | [../../00-INDEX.md](../../00-INDEX.md) |
