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

To be populated in Phase 6. Will declare demands for stability, trend, entropy, and periodicity morphs on multiple R3 features at H16/H18/H20/H22 to track context at each hierarchical level.

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
