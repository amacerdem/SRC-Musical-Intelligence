# H6-H7: Beat Subdivision Horizons

**Band**: Micro (upper boundary)
**Horizons**: H6-H7
**Duration**: 200ms - 250ms
**Frames**: 34-43
**Musical scale**: 16th note @75BPM to 8th note @120BPM
**Neural correlate**: Gamma-to-beta transition, pre-attentive grouping
**Updated**: 2026-02-13

---

## Overview

H6-H7 form the upper boundary of the Micro band and the transition zone into beat-level processing. This is where sensory feature extraction begins to interface with rhythmic and structural mechanisms. H6 (200ms) is the single most mechanism-dense horizon in the entire H3 system, with five mechanisms converging: PPC, TPC, BEP, ASA, and AED.

The 200-250ms range corresponds to the shortest intervals at which listeners reliably perceive rhythmic grouping. Below 200ms, perception is dominated by sensory attributes (timbre, onset sharpness); above 250ms, beat entrainment becomes the dominant processing mode.

---

## Per-Horizon Detail

| Horizon | Duration | Frames | BPM Equivalent | Mechanisms | Units |
|---------|----------|:------:|----------------|------------|-------|
| **H6** | 200ms | 34 | 16th @75, 32nd @150 | PPC, TPC, BEP, ASA, AED | SPU, ASU, NDU, STU, MPU, ARU |
| **H7** | 250ms | 43 | 8th @120, 16th @60 | -- | SPU |

### H6: Mechanism Convergence Point (200ms, 34 frames)

H6 is the most important single horizon in the Micro band and arguably in the entire system. Five mechanisms use it:

| Mechanism | Role at H6 | Horizon Range |
|-----------|-----------|:-------------:|
| **PPC** | Longest micro-band pitch tracking | H0, H3, **H6** |
| **TPC** | Shortest temporal pattern window | **H6**, H12, H16 |
| **BEP** | Shortest beat entrainment window | **H6**, H9, H11 |
| **ASA** | Longest micro-band scene analysis | H3, **H6**, H9 |
| **AED** | Short-scale event detection | **H6**, H16 |

This convergence reflects the perceptual significance of the ~200ms timescale: it is the shortest window where beat-level, pattern-level, and event-level processing can all operate with sufficient temporal context.

**Unit consumers at H6**: SPU (PPC, TPC), ASU (ASA), NDU (ASA), STU (BEP), MPU (BEP), ARU (AED)

### H7: Beat Subdivision (250ms, 43 frames)

H7 provides slightly longer context than H6 but currently has no dedicated mechanism assignments. It serves as an interpolation point for SPU's PPC processing, bridging between H6 (200ms) and H8 (300ms). At 250ms, this horizon corresponds to eighth notes at 120 BPM -- one of the most common subdivision levels in popular music.

---

## Morph Relevance

With 34-43 frames, H6-H7 support a broader set of morphs than H0-H5:

| Morph | Name | H6 (34fr) | H7 (43fr) | Notes |
|-------|------|:---------:|:---------:|-------|
| M0 | value | Y | Y | Instantaneous |
| M1 | mean | Y | Y | Stable with 34+ frames |
| M2 | std | Y | Y | Meaningful spread |
| M3 | median | Y | Y | |
| M4 | max | Y | Y | |
| M5 | range | Y | Y | |
| M6 | skewness | * | Y | Marginal at 34 frames |
| M7 | kurtosis | * | * | Still marginal |
| M8 | velocity | Y | Y | First difference reliable |
| M9 | acceleration | Y | Y | Second difference reliable |
| M10 | smoothness | Y | Y | |
| M14 | periodicity | * | * | Marginal -- need 2+ periods |
| M18 | trend | Y | Y | Linear trend detectable |
| M20 | entropy | * | * | Marginal bin count |

**Y** = reliable, **\*** = marginal (interpret with caution)

**Key transition**: H6-H7 is where the morph palette begins expanding from the limited micro set (M0, M1, M8) toward the full meso set. However, periodicity (M14) and entropy (M20) remain unreliable because they require longer windows to accumulate sufficient statistical samples.

---

## R3 Features Commonly Tracked

H6-H7 demands span the full Energy subspace and extend into Change features:

| R3 Index | Feature | Mechanisms Using It | Rationale |
|:--------:|---------|:-------------------:|-----------|
| [7] | velocity_A | PPC, BEP | Attack velocity at beat subdivision scale |
| [8] | velocity_D | PPC, BEP | Decay velocity |
| [9] | velocity_S | BEP | Sustain level |
| [10] | spectral_flux | TPC, AED | Spectral change for event boundary detection |
| [11] | onset_strength | ASA, AED | Onset salience for grouping and event detection |
| [0] | roughness_total | PPC | Sensory dissonance within subdivision window |
| [21] | spectral_change | TPC | Change rate at subdivision timescale |

### R3 v2 Candidates

| R3 Index | Feature | Candidate Mechanism | Rationale |
|:--------:|---------|:-------------------:|-----------|
| [72] | event_density | AED | Events per unit time at subdivision scale |
| [66] | beat_strength | BEP | Beat salience at fastest metrical level |
| [122] | sharpness | ASA, PPC | Psychoacoustic sharpness for stream segregation |
| [65] | tempo_estimate | BEP | Local tempo at subdivision resolution |

---

## The H6 Convergence Phenomenon

H6's five-mechanism convergence is not coincidental. It reflects a fundamental property of auditory cognition: the ~200ms timescale is where multiple processing streams converge before diverging into specialized pathways.

**Bottom-up convergence**: PPC (pitch), ASA (scene analysis), and AED (event detection) complete their micro-band processing at H6, producing refined representations.

**Top-down divergence**: TPC (temporal patterns) and BEP (beat entrainment) begin their processing at H6, consuming the refined micro-band outputs and extending into meso/macro timescales.

This makes H6 the architectural pivot between sensory processing and cognitive processing in the H3 system.

---

## Neuroscience Basis

### Gamma-to-Beta Transition

The 200-250ms range corresponds to the neural transition from gamma-band (>30 Hz) to beta-band (<30 Hz) oscillatory processing:

- **Below 200ms**: Gamma oscillations dominate, reflecting sensory feature binding
- **200-250ms**: Beta oscillations begin to emerge, reflecting predictive motor engagement
- **Above 250ms**: Beta-theta coupling drives beat entrainment

### Pre-Attentive Grouping

The mismatch negativity (MMN) response, a marker of pre-attentive auditory change detection, operates on a timescale of ~150-250ms. H6-H7 captures this processing window, aligning with AED's event detection function.

### Motor System Engagement

At ~200ms, the earliest motor cortex responses to rhythmic stimuli appear. This aligns with BEP's entry at H6 -- the shortest horizon at which the motor system can begin to entrain to auditory patterns.

---

## Computation Notes

### Buffer Requirements

| Horizon | Frames | Buffer Size (128D float32) |
|---------|:------:|:--------------------------:|
| H6 | 34 | 17 KB |
| H7 | 43 | 22 KB |

Buffer requirements remain modest. The main computational consideration at H6 is the number of concurrent mechanism computations (5 mechanisms), which may require careful scheduling to avoid redundant R3 feature reads.

### Mechanism Scheduling at H6

Because five mechanisms share H6, the H3 engine can optimize by computing the H6 attention-weighted window once and distributing it to all five mechanisms. This is a key optimization target for the pipeline.

---

## Cross-References

| Document | Location |
|----------|----------|
| Sub-beat horizons (H0-H5) | [H0-H5-SubBeat.md](H0-H5-SubBeat.md) |
| Band index | [00-INDEX.md](00-INDEX.md) |
| Beat period (H8-H11) | [../Meso/H8-H11-BeatPeriod.md](../Meso/H8-H11-BeatPeriod.md) |
| PPC mechanism | [../../../C³/Mechanisms/PPC.md](../../../C³/Mechanisms/PPC.md) |
| TPC mechanism | [../../../C³/Mechanisms/TPC.md](../../../C³/Mechanisms/TPC.md) |
| BEP mechanism | [../../../C³/Mechanisms/BEP.md](../../../C³/Mechanisms/BEP.md) |
| ASA mechanism | [../../../C³/Mechanisms/ASA.md](../../../C³/Mechanisms/ASA.md) |
| AED mechanism | [../../../C³/Mechanisms/AED.md](../../../C³/Mechanisms/AED.md) |
