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

To be populated in Phase 6. Will declare demands for timbre group R3 features (spectral_centroid, spectral_flux, harmonic_ratio) and energy features at H3/H6/H9 to compute grouping cues and stream segregation signals.

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
