# PPC — Pitch Processing Chain

| Field | Value |
|-------|-------|
| NAME | PPC |
| FULL_NAME | Pitch Processing Chain |
| CIRCUIT | Perceptual (hearing & pattern recognition) |
| OUTPUT_DIM | 30 |
| HORIZONS | H0 (5.8 ms), H3 (23.2 ms), H6 (200 ms) |

## Description

The Pitch Processing Chain models the ascending auditory pathway for pitch extraction — from brainstem frequency-following response through thalamic relay to cortical pitch analysis in Heschl's gyrus. This mechanism captures how raw spectral information is transformed into stable pitch percepts through hierarchical processing stages.

## 3x10D Sub-Section Structure

| Dims | Horizon | Computes |
|------|---------|----------|
| 0-9 | H0 (5.8 ms) | Brainstem frequency-following response (FFR): phase-locked neural responses to individual pitch periods. Faithful encoding of fundamental frequency and lower harmonics through temporal fine structure. Cochlear nucleus / inferior colliculus stage (Bidelman 2013). |
| 10-19 | H3 (23.2 ms) | Subcortical pitch encoding: integrates over ~1-2 pitch periods for typical musical frequencies. Autocorrelation-based pitch extraction in the medial geniculate body providing stable periodicity estimate (Patterson et al. 1992). |
| 20-29 | H6 (200 ms) | Cortical pitch processing: Heschl's gyrus and planum temporale integrate pitch over ~200 ms for stable pitch percept. Pitch height, pitch chroma, pitch salience, pitch interval, and contour (Patterson et al. 2002, Zatorre et al. 2002). |

## H3 Demand

### R3 Feature Inputs

| R3 Domain | Indices | Features | Consuming Units |
|-----------|---------|----------|-----------------|
| A: Consonance | [0]-[6] | harmonicity, roughness, roughness_total, consonance_dissonance, inharmonicity, periodicity, fundamental_freq | SPU, PCU, IMU, NDU |
| C: Timbre | [12]-[20] | spectral_centroid, spectral_spread, spectral_rolloff, brightness_kuttruff | PCU, IMU, NDU |
| B: Energy | [7]-[11] | onset_strength, loudness, rms_energy | IMU (CDEM) |
| D: Change | [21]-[24] | spectral_flux, delta_loudness | NDU (SDD) |
| E: Interactions | [25]-[48] | Cross-domain coupling terms | PCU (HTP, ICEM, PWUP), IMU (CDEM) |

Domain A (Consonance) is the universal input — all 12 PPC-consuming models require consonance features as the basis for pitch extraction. Domains C, B, D, E are supplementary, consumed by specific models in PCU, IMU, and NDU.

### Per-Horizon Morph Profile

| Horizon | Morphs | Rationale |
|---------|--------|-----------|
| H0 (5.8 ms, 1 frame) | M0 (value), M1 (mean) | Brainstem FFR — instantaneous phase-locked response; only point-estimate morphs are meaningful at single-frame resolution |
| H3 (23.2 ms, 4 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity) | Subcortical pitch encoding — 1-2 pitch periods for typical frequencies; variability and rate-of-change capture periodicity stability |
| H6 (200 ms, 34 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity) | Cortical pitch processing — 200 ms integration window in Heschl's gyrus; full first-order statistical suite for stable pitch percept |

### Law Distribution

| Law | Units | Models | Rationale |
|-----|-------|:------:|-----------|
| L0 (Memory) | PCU | 4 | Maintaining predictive priors for pitch from recent past |
| L1 (Prediction) | PCU, NDU | 5 | Generating forward pitch predictions; deviance detection requires predicted vs actual comparison |
| L2 (Integration) | SPU, PCU, IMU | 9 | Bidirectional spectral integration — bottom-up feature extraction meets top-down harmonic template matching |

L2 (Integration) is the dominant law (9 of 12 models), reflecting the bidirectional nature of pitch processing. SPU uses L2 exclusively. PCU distributes across all three laws for hierarchical predictive coding. NDU uses L1 for prediction error computation.

### Demand Estimate

| Source Unit | Models | Est. Tuples |
|-------------|:------:|:-----------:|
| SPU | 6 | ~180 |
| PCU | 4 | ~100 |
| NDU (SDD) | 1 | ~30 |
| IMU (CDEM) | 1 | ~20 |
| **Total (deduplicated)** | **12** | **~250** |

## Models Using This Mechanism

### SPU (Spectral Processing Unit)
- **BCH** — Brainstem-Cortical Hierarchy
- **PSCL** — Pitch-Space Consonance Lattice
- **PCCR** — Pitch-Class Circular Representation
- **SDNPS** — Spectral Decomposition and Neural Pitch Salience
- **ESME** — Envelope and Spectral Modulation Encoding
- **SDED** — Spectral Detail and Edge Detection

### PCU (Predictive Coding Unit)
- **SPH** — Sensory Prediction Hierarchy
- **HTP** — Hierarchical Temporal Prediction
- **PSH** — Predictive Sensory Hierarchy
- **PWUP** — Precision-Weighted Uncertainty Processor

### IMU (Integrative Memory Unit)
- **TPRD** — Tonal Pattern Recognition and Decoding

### NDU (Novelty Detection Unit)
- **SDD** — Spectral Deviation Detection

## Neuroscientific Basis

- Bidelman (2013): Subcortical sources of brainstem FFR predict cortical pitch processing.
- Patterson et al. (1992): Autocorrelation model of pitch perception; temporal integration windows.
- Patterson et al. (2002): fMRI localisation of pitch centre in lateral Heschl's gyrus.
- Zatorre et al. (2002): Cortical mechanisms for pitch perception — pitch height vs. pitch chroma.
- Plack et al. (2005): Pitch coding from periphery to cortex — hierarchical temporal processing model.

## Code Reference

`mi_beta/brain/mechanisms/ppc.py`
