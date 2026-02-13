# TPC — Timbre Processing Chain

| Field | Value |
|-------|-------|
| NAME | TPC |
| FULL_NAME | Timbre Processing Chain |
| CIRCUIT | Perceptual (hearing & pattern recognition) |
| OUTPUT_DIM | 30 |
| HORIZONS | H6 (200 ms), H12 (525 ms), H16 (1 s) |

## Description

The Timbre Processing Chain decomposes incoming audio into perceptual timbre dimensions and tracks their temporal evolution across beat-to-phrase timescales. Timbre — the quality distinguishing sounds of equal pitch and loudness — is a multi-dimensional percept that cannot be reduced to a single acoustic feature. TPC models how the auditory cortex constructs a stable timbre representation from spectral and temporal envelope cues.

## 3x10D Sub-Section Structure

| Dims | Horizon | Computes |
|------|---------|----------|
| 0-9 | H6 (200 ms) | Attack/onset timbre: fast-varying spectral features during sound onset. Critical for instrument identification (Grey 1977). Spectral centroid, spectral flux, attack sharpness — "brightness" and "bite". |
| 10-19 | H12 (525 ms) | Sustain timbre: spectral information over the sustain portion of notes. Steady-state spectral shape, formant structure, harmonic-to-noise ratio defining instrument "body" and "warmth". McAdams et al.'s (1995) spectral centroid and spectral irregularity dimensions. |
| 20-29 | H16 (1 s) | Timbral trajectory: how timbre evolves over a full beat or note group. Vibrato, tremolo, gradual spectral modulations contributing to timbral expressiveness. Timbral transitions between events — critical for auditory stream formation (Bregman 1990). |

## H3 Demand

### R3 Feature Inputs

| R3 Domain | Indices | Features | Consuming Units |
|-----------|---------|----------|-----------------|
| C: Timbre | [12]-[20] | spectral_centroid, spectral_spread, spectral_rolloff, spectral_flatness, spectral_crest, brightness_kuttruff, mfcc_vector | SPU (all 3), PCU (HTP, MAA) |
| A: Consonance | [0]-[6] | harmonicity, roughness, consonance_dissonance, periodicity | SPU (STAI, MIAA), PCU (HTP, UDP, MAA) |
| B: Energy | [7]-[11] | onset_strength, loudness, velocity_A | STU (TPIO), PCU (HTP, MAA) |
| D: Change | [21]-[24] | spectral_flux, delta_loudness | STU (TPIO), PCU (UDP) |
| E: Interactions | [25]-[48] | Spectral interaction terms | SPU (STAI), PCU (HTP, UDP, MAA) |

Domain C (Timbre) is the primary input — all TPC-consuming models require spectral shape features. Domain A provides harmonic context for timbral analysis. Domains B, D, E serve supplementary roles for temporal gating and cross-domain coupling.

### Per-Horizon Morph Profile

| Horizon | Morphs | Rationale |
|---------|--------|-----------|
| H6 (200 ms, 34 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity) | Attack/onset timbre — fast spectral features during onset; velocity captures timbral change rate |
| H12 (525 ms, 90 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M14 (periodicity), M18 (trend) | Sustain timbre — steady-state spectral shape; periodicity detects vibrato; trend tracks spectral drift |
| H16 (1 s, 172 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M14 (periodicity), M18 (trend) | Timbral trajectory — full note/beat evolution; trend and periodicity capture timbral expressiveness |

### Law Distribution

| Law | Units | Models | Rationale |
|-----|-------|:------:|-----------|
| L0 (Memory) | STU, PCU | 2 | Causal beat tracking (STU) and maintaining timbral priors (PCU) |
| L1 (Prediction) | PCU | 2 | Forward timbral prediction for predictive coding hierarchy |
| L2 (Integration) | SPU, PCU | 5 | Bidirectional spectral template matching — bottom-up extraction meets top-down pattern completion |

L2 (Integration) dominates, reflecting the bidirectional nature of timbre processing — spectral templates constrain bottom-up analysis while new input updates templates.

### Demand Estimate

| Source Unit | Models | Est. Tuples |
|-------------|:------:|:-----------:|
| SPU | 3 | ~135 |
| PCU | 3 | ~80 |
| STU (TPIO) | 1 | ~50 |
| **Total (deduplicated)** | **7** | **~180** |

## Models Using This Mechanism

### SPU (Spectral Processing Unit)
- **STAI** — Spectral Timbre Analysis & Integration
- **TSCP** — Temporal-Spectral Coupling Processor
- **MIAA** — Multi-scale Integration & Auditory Attention

### STU (Sensorimotor Timing Unit)
- **TPIO** — Temporal Pattern Integration and Output

### PCU (Predictive Coding Unit)
- **IGFE** — Information Gain and Feature Extraction
- **HTP** — Hierarchical Temporal Prediction
- **PSH** — Predictive Sensory Hierarchy

## Neuroscientific Basis

- McAdams et al. (1995): Perceptual dimensions of timbre — attack time, spectral centroid, spectral flux.
- Grey (1977): Multidimensional scaling of musical timbre — spectral envelope and temporal envelope.
- Bregman (1990): Auditory Scene Analysis — timbral similarity as a primary grouping cue.
- Alluri & Toiviainen (2010): Neural correlates of timbre processing in bilateral superior temporal cortex.
- Giordano et al. (2013): Cortical representation of timbre in Heschl's gyrus and planum temporale.

## Code Reference

`mi_beta/brain/mechanisms/tpc.py`
