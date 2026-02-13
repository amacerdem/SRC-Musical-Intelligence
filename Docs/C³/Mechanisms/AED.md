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

### R3 Feature Inputs

| R3 Domain | Indices | Features | Consuming Units |
|-----------|---------|----------|-----------------|
| B: Energy | [7]-[11] | onset_strength, loudness, velocity_A, velocity_D, rms_energy | ARU (all 10 via P5), RPU (all 6), PCU (WMED, CHPI) |
| A: Consonance | [0]-[6] | harmonicity, consonance_dissonance, periodicity | ARU (6 via P1), RPU (8), PCU (CHPI) |
| D: Change | [21]-[24] | spectral_flux, delta_loudness | ARU (4 via P5), RPU (DAED, RPEM, IUCP, IOTMS), PCU (WMED) |
| E: Interactions | [25]-[48] | Cross-domain coupling terms | ARU (6 via P3), RPU (9), PCU (WMED, CHPI) |
| C: Timbre | [12]-[20] | spectral_centroid, brightness_kuttruff | ARU (7 via P1), RPU (MORMR, MCCN, MEAMR, SSRI, LDAC, SSPS), PCU (CHPI) |

Domain B (Energy) is the universal input — affective entrainment fundamentally couples emotional response to acoustic energy fluctuations. ARU accesses R3 features indirectly via pathways (P1 from SPU, P3 from IMU, P5 from STU). RPU and PCU access R3 directly.

### Per-Horizon Morph Profile

| Horizon | Morphs | Rationale |
|---------|--------|-----------|
| H6 (200 ms, 34 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M19 (stability) | Beat-level entrainment — instantaneous coupling between energy fluctuations and expected beat grid; stability measures phase-locking quality |
| H16 (1 s, 172 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M18 (trend), M19 (stability) | Bar-level dynamics — entrainment stability and groove quality over the bar; trend captures emotional arc trajectory |

The bimodal horizon profile (H6 + H16) captures AED's distinctive dual-timescale architecture: immediate affective response (Micro) and structural emotional arc (Macro).

### Law Distribution

| Law | Units | Models | Rationale |
|-----|-------|:------:|-----------|
| L0 (Memory) | RPU, PCU | 4 | Comparing current affective state to stored reward templates |
| L1 (Prediction) | RPU, PCU | 4 | Anticipatory dopaminergic responses — predicting affective outcomes |
| L2 (Integration) | ARU, RPU, PCU | 14 | Bidirectional affective processing — emotion integrates sensory evidence with appraisal and expectation |

L2 (Integration) dominates — all 10 ARU models use L2, reflecting the bidirectional nature of affective resonance. RPU distributes across all three laws (wanting vs liking). PCU uses all three for predictive coding of affect.

### Demand Estimate

| Source Unit | Models | Est. Tuples |
|-------------|:------:|:-----------:|
| ARU | 10 | ~200 |
| RPU | 6 | ~90 |
| PCU (WMED, CHPI) | 2 | ~40 |
| **Total (deduplicated)** | **18** | **~350** |

AED is the highest-demand mechanism by model count in any single unit (10/10 ARU models), with the characteristic bimodal H6+H16 footprint appearing universally across all 18 consuming models.

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
