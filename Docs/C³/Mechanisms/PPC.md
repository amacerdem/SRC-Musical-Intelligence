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

To be populated in Phase 6. Will declare demands for consonance group R3 features (harmonic_ratio, stumpf_fusion, f0_salience) at H0, H3, and H6 across memory and integration laws.

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
