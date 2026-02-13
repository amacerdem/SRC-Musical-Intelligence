# CPD — Chills & Peak Detection

| Field | Value |
|-------|-------|
| NAME | CPD |
| FULL_NAME | Chills & Peak Detection |
| CIRCUIT | Mesolimbic (reward & pleasure) |
| OUTPUT_DIM | 30 |
| HORIZONS | H9 (350 ms), H16 (1 s), H18 (2 s) |

## Description

Chills & Peak Detection identifies moments of intense autonomic arousal during music listening — the "goosebumps" or "frisson" response. These are brief, involuntary physiological events characterised by piloerection, skin conductance spikes, and subjective reports of intense pleasure. CPD operates across three timescales spanning the autonomic nervous system's response dynamics.

## 3x10D Sub-Section Structure

| Dims | Horizon | Computes |
|------|---------|----------|
| 0-9 | H9 (350 ms) | Fast ANS detection: initial sympathetic response onset. Detects acoustic trigger features (sudden dynamic change, harmonic shift, timbral novelty) that initiate the autonomic cascade. |
| 10-19 | H16 (1 s) | Beat-level integration: timescale at which conscious awareness of the frisson event emerges. Corresponds to the psychological present (Poppel 2009) and typical beat duration. |
| 20-29 | H18 (2 s) | Phrase-level context: broader musical context determining whether an acoustic event is surprising enough to trigger chills. Expectation violation (Huron 2006) requires sufficient temporal window for prediction establishment. |

## H3 Demand

### R3 Feature Inputs

| R3 Domain | Indices | Features | Consuming Units |
|-----------|---------|----------|-----------------|
| B: Energy | [7]-[11] | loudness, velocity_A, velocity_D, onset_strength | ARU (SRP, AAC, PUPF, MAD via P5), RPU (MORMR, IUCP) |
| D: Change | [21]-[24] | spectral_flux, delta_loudness | ARU (all 4 via P5), RPU (IUCP) |
| C: Timbre | [12]-[20] | spectral_centroid, spectral_spread, brightness_kuttruff | ARU (SRP, AAC, MAD via P1), RPU (MORMR) |
| A: Consonance | [0]-[6] | harmonicity, roughness, consonance_dissonance | ARU (SRP, AAC, MAD via P1), RPU (MORMR, IUCP) |
| E: Interactions | [25]-[48] | Cross-domain coupling terms | ARU (SRP, AAC via P3), RPU (MORMR, IUCP) |

CPD's R3 inputs reflect the acoustic triggers of chills: sudden loudness increase (B: velocity_A), harmonic shift (A: consonance_dissonance), and timbral novelty (C: spectral_centroid change). ARU accesses features via pathways (P1, P3, P5); RPU accesses directly.

### Per-Horizon Morph Profile

| Horizon | Morphs | Rationale |
|---------|--------|-----------|
| H9 (350 ms, 60 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M9 (acceleration), M11 (peak) | Fast ANS detection — sympathetic onset response; velocity and acceleration capture sudden dynamic changes that trigger chills; peak detects local maxima in autonomic arousal |
| H16 (1 s, 172 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M11 (peak) | Beat-level integration — conscious awareness of frisson; peak detection at the psychological present timescale |
| H18 (2 s, 345 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity) | Phrase-level context — expectation violation requires sufficient temporal window for prediction establishment; reduced morph set reflects contextual role |

The morph profile narrows from H9 to H18, reflecting the shift from rapid autonomic detection (rich dynamics suite) to slower contextual expectation (statistical summary).

### Law Distribution

| Law | Units | Models | Rationale |
|-----|-------|:------:|-----------|
| L0 (Memory) | RPU | 1 | Comparing current arousal to stored chills templates |
| L1 (Prediction) | RPU | 1 | Anticipating peak moments — expectation violation drives chills |
| L2 (Integration) | ARU, RPU | 5 | Bidirectional processing — chills emerge from integrating sensory surprise with affective appraisal |

L2 (Integration) dominates — all 4 ARU models use L2. Chills detection is inherently bidirectional: the autonomic response depends on both the preceding context (build-up) and following resolution.

### Demand Estimate

| Source Unit | Models | Est. Tuples |
|-------------|:------:|:-----------:|
| ARU (SRP, AAC, PUPF, MAD) | 4 | ~80 |
| RPU (MORMR, IUCP) | 2 | ~40 |
| **Total (deduplicated)** | **6** | **~120** |

## Models Using This Mechanism

### ARU (Affective Resonance Unit)
- **SRP** — Striatal Reward Pathway
- **AAC** — Amygdala-Auditory Cortex
- **PUPF** — Pleasure-Unpleasure Processing Framework
- **MAD** — Musical Affect Dynamics

### RPU (Regulatory Processing Unit)
- **DAED** — Dynamic Autonomic Emotion Dynamics
- **RPEM** — Regulatory Processing of Emotional Music

## Neuroscientific Basis

- Blood & Zatorre (2001): PET study showing dopamine release during musical chills, with involvement of NAcc, VTA, and insula.
- Salimpoor et al. (2009): Psychophysiological correlates of music-evoked chills including SCR, heart rate, and respiration changes.
- Grewe et al. (2007): Acoustic features predicting chills include sudden dynamic increases, entry of new voices, and harmonic changes.
- Huron (2006): Sweet Anticipation — expectation violation as a driver of strong emotional responses in music.

## Code Reference

`mi_beta/brain/mechanisms/cpd.py`
