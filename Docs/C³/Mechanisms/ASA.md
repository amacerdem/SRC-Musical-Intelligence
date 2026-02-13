# ASA — Auditory Scene Analysis

| Field | Value |
|-------|-------|
| NAME | ASA |
| FULL_NAME | Auditory Scene Analysis |
| CIRCUIT | Salience (attention, novelty, & arousal gating) |
| OUTPUT_DIM | 30 |
| HORIZONS | H3 (23.2 ms), H6 (200 ms), H9 (350 ms) |

## Description

Auditory Scene Analysis models the brain's ability to decompose complex acoustic mixtures into perceptually distinct auditory "streams" or "objects". In music, this corresponds to following individual instruments or voices within a polyphonic texture. Grounded in Bregman's (1990) framework, ASA distinguishes primitive grouping (bottom-up: harmonicity, onset synchrony, spectral proximity) from schema-based grouping (top-down: learned templates).

## 3x10D Sub-Section Structure

| Dims | Horizon | Computes |
|------|---------|----------|
| 0-9 | H3 (23.2 ms) | Gamma-rate micro-segregation: onset synchrony and spectral co-modulation determining whether simultaneous partials belong to the same or different sources. Earliest cortical processing in primary auditory cortex (A1). |
| 10-19 | H6 (200 ms) | Event-level stream formation: sequential grouping via pitch proximity, timbral similarity, temporal regularity. "Old-plus-new" heuristic for parsing events as continuations of existing streams. |
| 20-29 | H9 (350 ms) | Stream stabilisation: streams persisting >300 ms become perceptually stable. Outputs reflect stream count, distinctiveness, relative salience, segregation confidence, and attentional modulation. |

## H3 Demand

### R3 Feature Inputs

| R3 Domain | Indices | Features | Consuming Units |
|-----------|---------|----------|-----------------|
| B: Energy | [7]-[11] | onset_strength, loudness, rms_energy, velocity_A, velocity_D | ASU (all 9), NDU (EDNR, ONI), ARU (CMAT), RPU (SSPS) |
| C: Timbre | [12]-[20] | spectral_centroid, spectral_spread, spectral_flatness, mfcc_vector, brightness_kuttruff | ASU (7), NDU (SDD, SDDP), ARU (CMAT), RPU (SSPS), PCU (IGFE) |
| D: Change | [21]-[24] | spectral_flux, delta_loudness, onset_density | ASU (4), NDU (all 9) |
| E: Interactions | [25]-[48] | Cross-domain coupling terms | NDU (7), ARU (CMAT), RPU (SSPS) |
| A: Consonance | [0]-[6] | harmonicity, consonance_dissonance | ASU (IACM, CSG), NDU (SDD, SLEE), RPU (SSPS) |

Domains B (Energy) and D (Change) are the most broadly consumed — salience and novelty detection both require energy transients and spectral change. Domain C (Timbre) serves stream segregation via timbral similarity. Domain E provides cross-domain coupling for novelty contextualisation.

### Per-Horizon Morph Profile

| Horizon | Morphs | Rationale |
|---------|--------|-----------|
| H3 (23.2 ms, 4 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M9 (acceleration), M11 (peak), M12 (trough), M15 (contrast) | Gamma-rate micro-segregation — onset synchrony and spectral co-modulation; acceleration and peak/trough detect transient onsets |
| H6 (200 ms, 34 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M9 (acceleration), M11 (peak), M12 (trough), M15 (contrast) | Event-level stream formation — sequential grouping via pitch proximity, timbral similarity; contrast measures peak-to-trough salience ratio |
| H9 (350 ms, 60 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M11 (peak), M15 (contrast) | Stream stabilisation — streams >300 ms become perceptually stable; reduced morph set reflects consolidated segregation output |

ASU alpha models use the full 8-morph suite at all horizons. Beta models reduce to 6 morphs (drop M9, M12). Gamma models use 5 morphs (M0, M1, M2, M8, M11), reflecting progressive salience abstraction.

### Law Distribution

| Law | Units | Models | Rationale |
|-----|-------|:------:|-----------|
| L1 (Prediction) | NDU, RPU | 10 | Novelty detection requires forward prediction — stimulus is novel only relative to expectation |
| L2 (Integration) | ASU, ARU, PCU | 11 | Salience is time-symmetric — prominence is measured against both past and future context |

L2 (Integration) and L1 (Prediction) split ASA demand roughly evenly. ASU uses L2 exclusively — salience integrates bidirectional context. NDU uses L1 exclusively — novelty is defined as prediction error. ARU and PCU use L2 for bidirectional processing.

### Demand Estimate

| Source Unit | Models | Est. Tuples |
|-------------|:------:|:-----------:|
| ASU | 9 | ~360 |
| NDU | 9 | ~120 |
| ARU (CMAT) | 1 | ~15 |
| RPU (SSPS) | 1 | ~15 |
| PCU (IGFE) | 1 | ~10 |
| **Total (deduplicated)** | **21** | **~450** |

ASA is the second-highest mechanism by model count (21 models), with ASU contributing 80% of the tuple demand.

## Models Using This Mechanism

### ASU (Auditory Salience Unit)
- **SNEM** — Salience-Novelty Encoding Model
- **IACM** — Involuntary Attention Capture Model
- **CSG** — Cortical Salience Gating
- **SDl** — Salience-Driven Listening
- **STANM** — Salience-Triggered Attentional Network Model
- **BARM** — Bottom-up Attention and Response Model
- **AACM** — Auditory Attention Control Model
- **PWSM** — Prediction-Weighted Salience Model
- **DGTP** — Dynamic Gain and Threshold Processing

### ARU (Affective Resonance Unit)
- **AAC** — Amygdala-Auditory Cortex

### NDU (Novelty Detection Unit)
- **MPG** — Mismatch and Prediction Gating
- **CDMR** — Change Detection and Memory Refresh
- **ONI** — Oddball and Novelty Integration
- **EDNR** — Event-Driven Novelty Response
- **DSP** — Deviance-Sensitive Processing
- **SDD** — Spectral Deviation Detection
- **SDDP** — Stimulus-Driven Deviance Processing
- **ECT** — Error Correction and Tracking
- **SLEE** — Statistical Learning and Expectation Engine

### RPU (Regulatory Processing Unit)
- **SSPS** — Sensory-Stimulation Processing System

### PCU (Predictive Coding Unit)
- **MAA** — Multi-scale Attentional Allocation

## Neuroscientific Basis

- Bregman (1990): Auditory Scene Analysis — primitive and schema-based grouping.
- Darwin (1997): Auditory grouping — harmonicity, onset synchrony, and co-modulation as primary grouping cues.
- van Noorden (1975): Temporal coherence boundary — streams stabilise after ~300 ms.
- Snyder & Alain (2007): Neural correlates of auditory stream segregation; object-related negativity (ORN).
- Micheyl et al. (2007): Buildup of stream segregation over time in primary auditory cortex.
- Cusack (2005): fMRI evidence for intraparietal sulcus involvement in attentional stream selection.

## Code Reference

`mi_beta/brain/mechanisms/asa.py`
