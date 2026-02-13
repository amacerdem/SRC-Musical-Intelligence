# H16-H17: Measure-Level Horizons

**Band**: Macro (lower boundary)
**Horizons**: H16-H17
**Duration**: 1,000ms - 1,500ms
**Frames**: 172-259
**Musical scale**: Full measure at moderate-to-fast tempi
**Neural correlate**: Delta oscillations (~1 Hz), auditory cortex temporal receptive fields
**Updated**: 2026-02-13

---

## Overview

H16-H17 form the lower boundary of the Macro band, bridging phrase-level processing into section-level cognition. H16 (1,000ms) is the most mechanism-dense macro horizon, with five mechanisms converging -- mirroring H6's role as the micro-band convergence point. Together, H6 and H16 form the two architectural pillars of the H3 system.

At 1-1.5 seconds, these horizons capture complete musical measures at moderate tempi, enabling the system to process harmonic progressions, metrical hierarchies, and structural boundaries at the measure level.

---

## Per-Horizon Detail

| Horizon | Duration | Frames | Musical Scale | Mechanisms | Units |
|---------|----------|:------:|---------------|------------|-------|
| **H16** | 1,000ms | 172 | 1 bar @240BPM, 1 bar @120BPM (2/4) | TMH, TPC, SYN, AED, CPD | ARU, STU, SPU, NDU, RPU |
| **H17** | 1,500ms | 259 | 1 bar @160BPM | -- | IMU, STU |

### H16: Macro Convergence Point (1,000ms, 172 frames)

H16 is the most mechanism-dense macro horizon, with five mechanisms:

| Mechanism | Role at H16 | Horizon Range |
|-----------|-------------|:-------------:|
| **TMH** | Entry point for temporal memory hierarchy | **H16**, H18, H20, H22 |
| **TPC** | Longest temporal pattern window | H6, H12, **H16** |
| **SYN** | Measure-level syntactic processing | H12, **H16**, H18 |
| **AED** | Macro-scale event detection | H6, **H16** |
| **CPD** | Measure-level change-point detection | H9, **H16**, H18 |

**Convergence significance**: Just as H6 serves as the pivot between sensory and cognitive processing, H16 serves as the pivot between beat/phrase processing and section/form processing. Mechanisms completing their upward span (TPC, AED) meet mechanisms beginning their downward span (TMH) at this horizon.

**Unit consumers at H16**: ARU (AED, CPD), STU (TMH, SYN), SPU (TPC), NDU (TMH), RPU (CPD, TMH)

### H17: Extended Measure (1,500ms, 259 frames)

At 1,500ms, H17 captures a full measure at 160 BPM (4/4) or a measure-and-a-half at slower tempi. No dedicated mechanism at this horizon, but IMU and STU use it for interpolation between H16 and H18. The 259-frame window provides strong statistical foundation for all morphs.

---

## Musical Timing Equivalents

| Horizon | Duration | As 4/4 Bar | As 3/4 Bar | Tempo Range |
|---------|----------|:----------:|:----------:|:-----------:|
| H16 | 1,000ms | @240 BPM | @180 BPM | Fast |
| H16 | 1,000ms | Half bar @120 | 1 bar @180 | Moderate-fast |
| H17 | 1,500ms | @160 BPM | @120 BPM | Moderate |
| H17 | 1,500ms | 3/4 bar @120 | 1 bar @120 | Moderate |

**Key insight**: H16 at 1s corresponds to the boundary of echoic memory duration -- the auditory system's short-term buffer for unprocessed sound. Processing at H16 and beyond increasingly relies on encoded representations rather than raw sensory traces.

---

## The H6-H16 Symmetry

H6 and H16 share a structural symmetry in the H3 architecture:

| Property | H6 (200ms) | H16 (1,000ms) |
|----------|:----------:|:--------------:|
| Mechanism count | 5 | 5 |
| Band position | Micro upper boundary | Macro lower boundary |
| Upward-completing | PPC, ASA | TPC, AED |
| Downward-beginning | TPC, BEP | TMH, SYN, CPD |
| Shared mechanism | AED (both) | AED (both) |
| Ratio to next convergence | 5x (200ms to 1,000ms) | -- |

AED uniquely operates at both convergence points (H6 and H16), detecting events at both micro and macro scales. This dual-scale event detection allows the system to identify both onset-level and section-level structural boundaries.

---

## R3 Features Commonly Tracked

At measure timescales, Interactions features become prominent:

| R3 Index | Feature | Mechanism | Rationale |
|:--------:|---------|:---------:|-----------|
| [25] | consonance_motion | SYN, TMH | Harmonic consonance trajectory over measure |
| [26] | energy_consonance | SYN | Energy-consonance coupling |
| [27:49] | (various interactions) | TMH, SYN | Cross-feature interactions at measure scale |
| [10] | spectral_flux | AED, CPD | Spectral change for boundary detection |
| [21] | spectral_change | CPD | Change rate at measure boundaries |

### R3 v2 Candidates

| R3 Index | Feature | Candidate Mechanism | Rationale |
|:--------:|---------|:-------------------:|-----------|
| [84] | tonal_stability | SYN | Key stability within measure |
| [91] | information_rate | TMH | Information density at measure rate |
| [114:128] | modulation features | TMH, SYN | Modulation patterns across measure |

Modulation features (v2 indices 114-128) are expected to be strongly demanded at H16-H17 because modulation perception requires at least one measure of context to establish tonal reference.

---

## Neuroscience Basis

### Delta Oscillations (~1 Hz)

The ~1s period of H16 aligns with cortical delta oscillations, which are implicated in:
- **Measure-level temporal prediction**: Delta phase tracks measure boundaries in rhythmic music
- **Hierarchical metrical structure**: Delta oscillations nest within slower infra-slow rhythms, creating a neural hierarchy paralleling the H3 band hierarchy
- **Attention modulation**: Delta phase gates sensory processing, enhancing perception at expected measure-level events

### Auditory Cortex Temporal Receptive Fields

Norman-Haignere (2022) characterized temporal receptive fields (TRFs) in auditory cortex, finding that higher-order auditory areas integrate information over windows of 1-10s. H16-H17 sit at the lower boundary of these TRFs, marking the transition from sensory to cognitive temporal integration.

### Memory Encoding Initiation

At the 1-1.5s timescale, the hippocampal encoding system begins to engage. Golesorkhi (2021) showed that temporal integration windows in hippocampus and medial prefrontal cortex match delta-range oscillations, supporting the assignment of TMH (temporal memory hierarchy) entry at H16.

---

## Computation Notes

### Buffer Requirements

| Horizon | Frames | Buffer Size (128D float32) |
|---------|:------:|:--------------------------:|
| H16 | 172 | 86 KB |
| H17 | 259 | 130 KB |

Buffer requirements start becoming non-trivial at macro scale. At H16, maintaining a rolling buffer of 172 frames across 128 features requires 86 KB per batch element.

### Mechanism Scheduling at H16

Five mechanisms share H16, creating a scheduling optimization opportunity similar to H6. The H3 engine should compute the H16 attention-weighted window once and distribute to all five mechanisms.

### Update Rate

At H16 (1,000ms), the morph computation can be updated less frequently than at micro horizons. A reasonable strategy is to compute H16 morphs every 172 frames (once per horizon window) rather than every frame, reducing computation by 172x relative to frame-rate updates.

---

## Cross-References

| Document | Location |
|----------|----------|
| Band index | [00-INDEX.md](00-INDEX.md) |
| Phrase (H12-H15) | [../Meso/H12-H15-Phrase.md](../Meso/H12-H15-Phrase.md) |
| Section (H18-H23) | [H18-H23-Section.md](H18-H23-Section.md) |
| TMH mechanism | [../../../C³/Mechanisms/TMH.md](../../../C³/Mechanisms/TMH.md) |
| TPC mechanism | [../../../C³/Mechanisms/TPC.md](../../../C³/Mechanisms/TPC.md) |
| SYN mechanism | [../../../C³/Mechanisms/SYN.md](../../../C³/Mechanisms/SYN.md) |
| AED mechanism | [../../../C³/Mechanisms/AED.md](../../../C³/Mechanisms/AED.md) |
| CPD mechanism | [../../../C³/Mechanisms/CPD.md](../../../C³/Mechanisms/CPD.md) |
