# AED — Affective Entrainment Dynamics

| Field | Value |
|-------|-------|
| NAME | AED |
| FULL_NAME | Affective Entrainment Dynamics |
| CIRCUIT | Mesolimbic (reward & pleasure) |
| OUTPUT_DIM | 30 |
| HORIZONS | H6 (200 ms), H16 (1 s) |

## Description

Affective Entrainment Dynamics captures the phenomenon whereby musical beat structure modulates emotional engagement through the mesolimbic dopaminergic pathway. AED quantifies how strongly a listener's affective state "locks" onto periodic rhythmic patterns — a process mediated by the ventral tegmental area (VTA) and its projections to the nucleus accumbens (NAcc).

## 3x10D Sub-Section Structure

| Dims | Horizon | Computes |
|------|---------|----------|
| 0-9 | H6 (200 ms) | Beat-level entrainment: instantaneous coupling between acoustic energy fluctuations and expected beat grid. Syncopation and microtiming prediction errors driving dopaminergic responses. |
| 10-19 | H16 (1 s) | Bar-level dynamics: entrainment stability and groove quality at the bar/measure level. Metric hierarchy engagement and groove sensation emergence. |
| 20-29 | (combined) | Cross-horizon interaction: beat-level prediction error magnitude, entrainment strength, groove index, affective valence modulation. |

## H3 Demand

To be populated in Phase 6. Will declare demands for energy, onset strength, and periodicity features at H6 and H16 across memory, prediction, and integration laws.

## Models Using This Mechanism

### ARU (Affective Resonance Unit)
- **SRP** — Striatal Reward Pathway
- **AAC** — Amygdala-Auditory Cortex
- **VMM** — Ventral-Medial Mapping
- **PUPF** — Pleasure-Unpleasure Processing Framework
- **MAD** — Musical Affect Dynamics
- **CLAM** — Cortical-Limbic Affect Model
- **TAR** — Thalamo-Amygdalar Routing
- **DAP** — Dopaminergic Anticipation Pathway
- **CMAT** — Cortico-Mesolimbic Affect Transduction
- **NEMAC** — Neuroendocrine Modulation of Affective Coding

### RPU (Regulatory Processing Unit)
- **DAED** — Dynamic Autonomic Emotion Dynamics
- **RPEM** — Regulatory Processing of Emotional Music
- **MORMR** — Model of Reward Modulation and Regulation
- **MCCN** — Motor-Cortical Coupling Network
- **MEAMR** — Memory-Emotion Associative Modulation and Regulation
- **LDAC** — Limbic-Driven Autonomic Control

### PCU (Predictive Coding Unit)
- **ICEM** — Interoceptive-Cognitive Emotion Model
- **WMED** — Working Memory for Emotion Dynamics

## Neuroscientific Basis

- Salimpoor et al. (2011): Dopamine release in NAcc/caudate during music listening correlates with anticipation and peak pleasure.
- Vuust et al. (2018): Predictive coding model of beat-based processing showing reward prediction error generation at mesolimbic sites.
- Witek et al. (2014): Syncopation and groove recruit mesolimbic reward circuitry, with medium syncopation yielding peak pleasure.

## Code Reference

`mi_beta/brain/mechanisms/aed.py`
