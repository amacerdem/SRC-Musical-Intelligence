# H3 Law L0 -- Memory (Past --> Present)

**Version**: 2.0.0
**Law index**: 0
**Direction**: Causal (backward-looking)
**Window**: `[max(0, t-n+1), t+1)`
**Kernel**: `A(dt) = exp(-3|t-t'|/H)` for `t'` in `[t-n+1, t]`
**Causality**: Fully causal -- no future frames required
**Latency**: 0 frames (real-time capable)
**Code reference**: `mi_beta.ear.h3.attention.AttentionKernel`, law=0
**Updated**: 2026-02-13

---

## Overview

L0 (Memory) is the causal temporal law. It places the attention window entirely in the past, looking backward from the current frame `t`. The exponential kernel peaks at the present moment (weight = 1.0) and decays into the past, reaching ~5% at the oldest frame in the window. L0 captures how a feature has behaved recently -- the accumulated sensory impression fading with time.

L0 is the only law that requires no future information. This makes it uniquely suited for real-time processing, where future frames are not yet available.

---

## Window Definition

```
Window: [max(0, t - n + 1),  t + 1)
```

Where:
- `t` = current frame index
- `n` = horizon frame count (from `HORIZON_FRAMES[horizon]`)
- `T` = total frames in the signal

The window includes `n` frames: from `t - n + 1` through `t` (inclusive). The `max(0, ...)` clamp handles the track start boundary -- when `t < n - 1`, the window is truncated at frame 0.

```python
# L0 window selection
window = range(max(0, t - n + 1), t + 1)
```

---

## Kernel Formula

```
A(dt) = exp(-3 * |t - t'| / H)    for t' in [t-n+1, t]
```

| Position | dt = |t - t'| | Weight A(dt) | Role |
|----------|:---:|:--------:|------|
| Current frame (t' = t) | 0 | 1.000 | Peak -- full attention on the present |
| Half-life (t' = t - 0.231H) | 0.231H | 0.500 | Half of peak attention |
| Midpoint (t' = t - H/2) | H/2 | 0.223 | ~22% of peak |
| Window edge (t' = t - n + 1) | ~H | 0.050 | ~5% of peak -- fading boundary |

The kernel is **not renormalized** after boundary clamping. At track start, edge frames naturally receive less total attention weight.

---

## Kernel Visualization

For horizon H = 10 frames, centered at frame t = 15:

```
Weight
1.00 |                                        *  <- t=15 (current, peak)
     |                                     *
0.67 |                                  *
     |                               *
     |                            *
0.37 |                         *
     |                      *
     |                   *
     |                *
0.05 |  *  *  *  *  *                            <- oldest frames (~5%)
     +--|--|--|--|--|--|--|--|--|--|--> frame
       6  7  8  9 10 11 12 13 14 15
       <------- past ----------->  now

Direction of decay: past <--- exponential --- present
```

```
L0 Memory window at t=15, H=10:
Frame:   6    7    8    9   10   11   12   13   14  [15]
Weight: .05  .07  .10  .14  .20  .27  .37  .50  .67 1.00
         <---------- exponential decay ----------   peak
```

---

## Properties

| Property | Value |
|----------|-------|
| Causality | Fully causal -- only past and present frames |
| Future frames used | 0 |
| Real-time latency | 0 frames (zero lookahead) |
| Peak weight | 1.0 at current frame t |
| Edge weight | exp(-3) = 0.0498 at oldest frame |
| Half-life | 0.231 * H frames from present |
| Effective width | ~67% of H (region where A > 0.5) |
| Boundary handling | Left-clamped at frame 0 (no renormalization) |

---

## Neuroscience Basis

L0 models the exponential decay of auditory sensory memory:

- **Echoic memory** (Cowan, 1984): Auditory short-term memory traces decay exponentially over hundreds of milliseconds. Recent sounds are vivid; older sounds fade. L0's kernel directly mirrors this decay profile.
- **Sensory memory traces in auditory cortex**: Neurons in primary auditory cortex (A1) maintain decaying representations of recent stimuli. The temporal response function of these neurons is well-approximated by exponential decay (Ulanovsky et al., 2004).
- **Exponential forgetting curves**: The memory literature consistently finds exponential (or near-exponential) decay of sensory traces (Wixted, 2004). L0 embeds this universal finding directly into temporal feature extraction.
- **Causal constraint**: Biological memory is inherently causal -- the brain cannot remember the future. L0 respects this constraint, making it the most biologically faithful of the three laws.

---

## Musical Role

L0 answers the question: **"How has this feature behaved recently?"**

It captures the accumulated sensory impression -- what the listener has heard and how it fades from perceptual salience. Specific musical functions include:

- **Detecting departures from recent baseline**: By comparing the current value to the L0-weighted recent history (e.g., M0 value vs M1 mean), models detect when a feature suddenly changes relative to what was recently established.
- **Tracking feature trajectories**: L0 morphs like M8 (velocity) and M18 (trend) capture the direction and rate of recent change, enabling detection of crescendos, accelerandos, and timbral shifts.
- **Maintaining sensory continuity**: The exponential weighting ensures that abrupt transients are captured (high weight at present) while sustained patterns accumulate influence over the window.

---

## Primary Unit Users

| Unit | Role of L0 | Key Morphs at L0 | Primary Horizons |
|------|-----------|-------------------|------------------|
| **IMU** | Memory integration (primary) | M0, M1, M2, M18 | H18-H25 (Macro-Ultra) |
| **STU** | Tonal memory / key tracking | M0, M1, M19 | H16-H22 (Macro) |
| **MPU** | Beat tracking from recent onsets | M0, M8, M14 | H6-H11 (Micro-Meso) |
| **NDU** | Recent history for novelty baseline | M0, M1, M2 | H3-H6 (Micro) |
| **PCU** | Pitch trajectory memory | M0, M8, M18 | H6-H16 (Micro-Macro) |
| **ARU** | Arousal memory trace | M0, M2, M18 | H6-H16 (Micro-Macro) |
| **RPU** | Rhythm pattern memory | M0, M14, M22 | H9-H16 (Meso-Macro) |
| **SPU** | Spectral memory trace | M0, M1, M2 | H6-H16 (Micro-Macro) |

---

## Usage by Unit

| Unit | Uses L0? | Rationale |
|------|:--------:|-----------|
| SPU | Yes | Spectral memory traces for feature stability assessment |
| STU | Yes | Tonal memory -- recent key/chord history for harmonic tracking |
| IMU | Yes | Primary memory-centric unit -- past traces drive emotional memory |
| ASU | **No** | Scene analysis uses only balanced integration (L2) |
| NDU | Yes | Recent history provides the baseline against which novelty is measured |
| MPU | Yes | Beat tracking relies on recent onset patterns |
| PCU | Yes | Pitch trajectory estimation from recent pitch history |
| ARU | Yes | Arousal tracking from recent energy/dynamic history |
| RPU | Yes | Rhythm pattern recognition from recent rhythmic events |

**Coverage**: 8 of 9 units. Only ASU omits L0, relying exclusively on L2 for balanced scene analysis.

---

## Real-Time Advantage

L0 is the only fully causal law. In real-time audio processing:

| Law | Lookahead Required | Real-Time Status |
|-----|:------------------:|:----------------:|
| **L0** | **0 frames** | **Fully real-time** |
| L1 | n frames (full horizon) | Requires buffering |
| L2 | n/2 frames (half horizon) | Requires partial buffering |

For real-time applications, models that depend exclusively on L0 can operate with zero additional latency beyond the R3 frame computation. Models using L1 or L2 require frame buffering equal to the horizon duration (L1) or half the horizon duration (L2).

---

## Horizon Interaction

L0 operates meaningfully at all horizon scales:

| Band | Horizons | L0 Captures | Example |
|------|----------|-------------|---------|
| **Micro** | H0-H7 | Onset history, attack decay, recent transients | "Did loudness spike in the last 200ms?" |
| **Meso** | H8-H15 | Beat-level accumulation, short-term rhythmic patterns | "What is the average energy over the last beat period?" |
| **Macro** | H16-H23 | Section-level trajectory, harmonic progression memory | "Is pitch trending upward over the last 2 seconds?" |
| **Ultra** | H24-H28 | Movement-scale memory, long-term feature accumulation | "What is the timbral character of the piece so far?" |

At micro horizons, L0 acts as a short-term sensory buffer. At macro horizons, it acts as a long-term memory trace capturing the overall trajectory of musical evolution.

---

## Relationship to L1 and L2

L0 provides the **memory perspective** that complements the other two laws:

- **L0 vs L1**: NDU (novelty detection) compares L0 morphs (what happened) with L1 morphs (what was expected) to compute prediction error. A large divergence between L0 and L1 signals surprise or novelty.
- **L0 vs L2**: IMU uses both L0 (pure memory trace) and L2 (balanced context) to distinguish between what has been heard (L0) and the overall perceptual character of the present moment (L2).
- **L0 uniqueness**: L0 is the only law that can provide a strictly causal feature history. Neither L1 nor L2 can answer the question "what has happened so far?" without contamination from future frames.

---

## Code Path

```
mi_beta/ear/h3/attention.py    -- compute_attention_weights(window, t, n_frames)
mi_beta/ear/h3/__init__.py     -- H3Extractor selects law=0 window
mi_beta/core/constants.py      -- LAW_NAMES[0] = "memory", ATTENTION_DECAY = 3.0
```

---

**Parent index**: [00-INDEX.md](00-INDEX.md)
**Registry**: [../Registry/LawCatalog.md](../Registry/LawCatalog.md)
**Attention kernel contract**: [../Contracts/AttentionKernel.md](../Contracts/AttentionKernel.md)
**H3 architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
