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

To be populated in Phase 6. Will declare demands for timbre group R3 features (spectral_centroid, spectral_irregularity, spectral_flux, harmonic_ratio) at H6, H12, and H16.

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
