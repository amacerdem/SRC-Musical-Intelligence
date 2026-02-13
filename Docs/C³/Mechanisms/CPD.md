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

To be populated in Phase 6. Will declare demands for loudness velocity, harmonic change, and timbral novelty at H9/H16/H18 to detect autonomic trigger features and expectation violation.

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
