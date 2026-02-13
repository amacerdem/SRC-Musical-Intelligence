# H3 Registry -- Law Catalog

**Version**: 2.0.0
**Count**: 3 laws (L0-L2)
**Code reference**: `mi_beta.core.constants.LAW_NAMES`
**Implementation**: `mi_beta.ear.h3.attention.AttentionKernel`
**Updated**: 2026-02-13

---

## Complete Law Table

| Index | Name | Direction | Window Selection | Kernel Formula |
|:-----:|------|-----------|-----------------|----------------|
| L0 | Memory | Past --> Present | `[max(0, t-n+1), t+1)` | Causal exponential decay from present into past |
| L1 | Prediction | Present --> Future | `[t, min(T, t+n))` | Anticipatory exponential projection forward from present |
| L2 | Integration | Bidirectional | `[max(0, t-half), min(T, t+n-half))` | Symmetric exponential centered on present |

**Notation**: `t` = current frame, `n` = horizon frame count, `T` = total frames, `half` = `n // 2`

**Shared kernel base**: `A(dt) = exp(-3|dt| / H)` where `H` = horizon frame count and `dt` = distance from center point. The three laws differ in which frames are included in the window and where the kernel is centered.

---

## Detailed Descriptions

### L0 -- Memory (Past --> Present)

**Window**: From `max(0, t - n + 1)` to `t + 1` (inclusive of current frame, looking backward)

**Kernel**: Causal exponential decay. The current frame `t` receives the highest weight; past frames decay exponentially as they recede:

```
A(dt) = exp(-3 * |t - t'| / H)    for t' in [t-n+1, t]
```

**Neuroscience basis**: Models echoic memory and sensory memory traces in auditory cortex. Recent information is weighted most strongly, matching the exponential decay of auditory short-term memory (Cowan, 1984). The causal constraint ensures that only information available at time `t` contributes, appropriate for real-time processing.

**Musical role**: How does this feature's recent history look from the present moment? Captures the accumulated sensory impression -- what has been heard and how it fades. Critical for tracking feature trajectories, detecting changes from recent baselines, and maintaining continuity.

**Primary users**: IMU (memory integration), STU (tonal memory), MPU (beat tracking from recent onsets)

---

### L1 -- Prediction (Present --> Future)

**Window**: From `t` to `min(T, t + n)` (inclusive of current frame, looking forward)

**Kernel**: Anticipatory exponential projection. The current frame `t` receives the highest weight; future frames decay exponentially:

```
A(dt) = exp(-3 * |t' - t| / H)    for t' in [t, t+n-1]
```

**Neuroscience basis**: Models predictive coding and anticipatory attention. The brain constantly generates predictions about upcoming auditory events (Friston, 2005; Clark, 2013). Forward-looking temporal morphs capture the trajectory that the feature is expected to follow, weighted by prediction confidence (which decreases with temporal distance).

**Musical role**: Where is this feature heading? Captures anticipatory structure -- what is expected to happen next. Critical for beat prediction, harmonic expectation, and phrase-boundary anticipation.

**Primary users**: NDU (novelty from prediction violation), MPU (beat prediction), PCU (pitch prediction)

**Note**: L1 requires access to future frames. During real-time processing, L1 morphs introduce latency equal to the horizon duration. In offline analysis, full future context is available.

---

### L2 -- Integration (Bidirectional)

**Window**: From `max(0, t - half)` to `min(T, t + n - half)` where `half = n // 2` (centered on present)

**Kernel**: Symmetric exponential centered on the current frame. Both past and future frames contribute equally:

```
A(dt) = exp(-3 * |t' - t| / H)    for t' in [t-half, t+n-half-1]
```

**Neuroscience basis**: Models the temporal integration window of auditory perception, where both recent memory and immediate anticipation contribute to the percept at time `t` (Poeppel, 2003). Corresponds to the "perceptual present" -- the temporal window within which events are fused into a unified experience.

**Musical role**: What is the overall character of this feature around the present moment? Captures the balanced temporal context -- a holistic view combining memory and anticipation. Critical for steady-state feature characterization, tonal stability assessment, and contextual normalization.

**Primary users**: SPU (spectral integration), ASU (scene analysis over balanced context), ARU (arousal from full context)

---

## Usage by Unit

Each unit uses a specific subset of laws reflecting its temporal processing needs:

| Unit | L0 (Memory) | L1 (Prediction) | L2 (Integration) | Rationale |
|------|:-----------:|:----------------:|:-----------------:|-----------|
| **SPU** | Yes | -- | Yes | Spectral processing: memory traces + integrated percept |
| **STU** | Yes | Yes | Yes | Tonal analysis: full temporal perspective needed |
| **IMU** | Yes | -- | Yes | Memory-centric: past traces + integrated context |
| **ASU** | -- | -- | Yes | Scene analysis: balanced integration only |
| **NDU** | Yes | Yes | Yes | Novelty: compare past (L0) with prediction (L1) + context (L2) |
| **MPU** | Yes | Yes | -- | Beat tracking: past pattern + forward prediction |
| **PCU** | Yes | Yes | Yes | Pitch: full temporal perspective for chroma tracking |
| **ARU** | Yes | Yes | Yes | Arousal: full temporal perspective for dynamic response |
| **RPU** | Yes | Yes | Yes | Rhythm: full temporal perspective for pattern analysis |

### Summary

| Law | Unit Count | Usage Frequency |
|-----|:----------:|----------------|
| L0 (Memory) | 8 of 9 | Most common (all except ASU) |
| L1 (Prediction) | 6 of 9 | Common (STU, NDU, MPU, PCU, ARU, RPU) |
| L2 (Integration) | 8 of 9 | Most common (all except MPU) |

---

## Kernel Visualization

For a horizon of H = 10 frames, centered at frame t = 15:

```
L0 Memory (past -> present):
Frame:   6   7   8   9  10  11  12  13  14  [15]
Weight: .05 .07 .10 .14 .20 .27 .37 .50 .67 1.0
         <---- exponential decay ----        peak

L1 Prediction (present -> future):
Frame: [15] 16  17  18  19  20  21  22  23  24
Weight: 1.0 .67 .50 .37 .27 .20 .14 .10 .07 .05
        peak        ---- exponential decay ---->

L2 Integration (bidirectional):
Frame:  11  12  13  14  [15] 16  17  18  19  20
Weight: .22 .30 .41 .55 1.0  .55 .41 .30 .22 .16
        <-- decay --    peak    -- decay -->
```

---

## Implementation Notes

- The decay constant `3` in `exp(-3|dt|/H)` means the kernel reaches ~5% of peak at the window edge (e^-3 = 0.0498). This provides effective localization while maintaining non-zero weight across the full window.
- All three laws share the same kernel shape; they differ only in window placement relative to `t`.
- Window boundary clamping (`max(0, ...)`, `min(T, ...)`) handles edge effects at track start/end. The kernel is **not** renormalized after clamping -- edge frames naturally have lower total attention weight.
- L1 and L2 introduce latency in real-time applications (up to `n` and `n/2` frames respectively). For real-time use, only L0 is fully causal.

---

**Parent index**: [00-INDEX.md](00-INDEX.md)
**Registry index**: [00-INDEX.md](00-INDEX.md)
