# TMH — Temporal Memory Hierarchy

| Field | Value |
|-------|-------|
| NAME | TMH |
| FULL_NAME | Temporal Memory Hierarchy |
| CIRCUIT | Sensorimotor (rhythm & movement) |
| OUTPUT_DIM | 30 |
| HORIZONS | H16 (1 s), H18 (2 s), H20 (5 s), H22 (15 s) |

## Description

The Temporal Memory Hierarchy encodes musical temporal context at multiple nested timescales, from individual bars through phrases to entire sections. TMH models how the brain maintains hierarchical temporal representations that enable perception of musical structure beyond the immediate present. Grounded in the theory that temporal processing is organised hierarchically, with different neural circuits maintaining representations at different timescales (Hasson et al. 2008).

## 3x10D Sub-Section Structure

| Dims | Horizon | Computes |
|------|---------|----------|
| 0-9 | H16 (1 s) | Bar-level memory: representation of current and immediately preceding bars. Bar-level repetition, variation, and metric regularity detection. Corresponds to the "perceptual present" (Poppel 2009). |
| 10-19 | H18 (2 s) + H20 (5 s) | Phrase-to-theme memory: phrase boundaries, cadential expectations, melodic/harmonic arcs (H18). Antecedent-consequent phrase relationships, thematic return, large-scale repetition (H20). Hippocampal episodic binding timescale. |
| 20-29 | H22 (15 s) | Section-level memory: context over entire sections (exposition, development, verse, chorus). Formal structure, large-scale key relationships, section boundaries. Prefrontal cortex for abstract structural representations (Sridharan et al. 2007). |

## H3 Demand

### R3 Feature Inputs

| R3 Domain | Indices | Features | Consuming Units |
|-----------|---------|----------|-----------------|
| B: Energy | [7]-[11] | onset_strength, loudness, rms_energy, velocity_A | STU (all 4), IMU (PMIM), RPU (RPEM) |
| D: Change | [21]-[24] | spectral_flux, delta_loudness, onset_density | STU (HMCE, EDTA, TMRM), IMU (PMIM, MSPBA), NDU (CDMR) |
| A: Consonance | [0]-[6] | harmonicity, periodicity, consonance_dissonance | IMU (MEAMN, PMIM), RPU (RPEM) |
| E: Interactions | [25]-[48] | Cross-domain coupling terms | IMU (PMIM, MSPBA), RPU (RPEM), NDU (CDMR) |

Domains B (Energy) and D (Change) are the core inputs — temporal memory hierarchy fundamentally tracks how energy and change patterns evolve across hierarchically nested timescales. Domain A provides harmonic structure for tonal memory levels.

### Per-Horizon Morph Profile

| Horizon | Morphs | Rationale |
|---------|--------|-----------|
| H16 (1 s, 172 frames) | M0 (value), M1 (mean), M2 (std), M14 (periodicity), M18 (trend), M21 (zero_crossings) | Bar-level memory — repetition and metric regularity detection; periodicity captures metric patterns; zero-crossings reflect energy oscillation within the perceptual present |
| H18 (2 s, 345 frames) | M0 (value), M1 (mean), M2 (std), M14 (periodicity), M18 (trend), M21 (zero_crossings) | Phrase-level memory — phrase boundaries and cadential expectations; trend captures melodic/harmonic arc trajectory |
| H20 (5 s, 861 frames) | M0 (value), M1 (mean), M14 (periodicity), M18 (trend) | Theme-level memory — thematic return recognition, large-scale repetition; reduced morph set reflects consolidated structural output |
| H22 (15 s, 2584 frames) | M0 (value), M1 (mean), M14 (periodicity), M18 (trend) | Section-level memory — formal structure, large-scale key relationships, section boundaries; periodicity and trend sufficient for abstract structural representation |

Periodicity (M14) and trend (M18) are the signature morphs of TMH — they capture the nested periodic structures and directional tendencies at each level of the temporal hierarchy.

### Law Distribution

| Law | Units | Models | Rationale |
|-----|-------|:------:|-----------|
| L0 (Memory) | STU, IMU, RPU | 6 | Causal temporal accumulation — hierarchy builds from past to present |
| L1 (Prediction) | STU, NDU | 3 | Tempo prediction (STU) and structural novelty detection (NDU) |
| L2 (Integration) | IMU | 2 | Bidirectional binding for cross-modal memory integration (MEAMN, PMIM) |

L0 (Memory) dominates — the temporal hierarchy is fundamentally about accumulating context from past events. L1 (Prediction) appears in STU models (HMCE, TMRM) for tempo anticipation and in NDU (CDMR) for structural novelty.

### Demand Estimate

| Source Unit | Models | Est. Tuples |
|-------------|:------:|:-----------:|
| STU (HMCE, AMSC, HGSIC, TMRM) | 4 | ~250 |
| IMU (MEAMN, PMIM) | 2 | ~80 |
| RPU (RPEM) | 1 | ~30 |
| NDU (CDMR) | 1 | ~20 |
| **Total (deduplicated)** | **8** | **~300** |

## Models Using This Mechanism

### STU (Sensorimotor Timing Unit)
- **HMCE** — Hierarchical Musical Context Encoding
- **AMSC** — Auditory-Motor Synchronisation Circuit
- **HGSIC** — Hierarchical Groove and Sensorimotor Integration Circuit
- **TMRM** — Temporal Memory and Rhythm Model

### IMU (Integrative Memory Unit)
- **MEAMN** — Memory Encoding and Maintenance Network
- **PMIM** — Predictive Memory Integration Model

### RPU (Regulatory Processing Unit)
- **MCCN** — Motor-Cortical Coupling Network

### NDU (Novelty Detection Unit)
- **CDMR** — Change Detection and Memory Refresh

## Neuroscientific Basis

- Hasson et al. (2008): Hierarchical temporal receptive windows — different cortical regions process information at different timescales.
- Poppel (2009): The "psychological present" of ~3 s as a temporal binding window.
- Davachi (2006): Hippocampal contributions to episodic memory through temporal context encoding.
- Sridharan et al. (2007): Neural dynamics of event segmentation — right fronto-insular cortex detecting temporal context boundaries.
- Jones & Boltz (1989): Dynamic attending theory — hierarchical oscillatory attention to multiple timescales.

## Code Reference

`mi_beta/brain/mechanisms/tmh.py`
