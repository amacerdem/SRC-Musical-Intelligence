# MEM — Memory Encoding / Retrieval

| Field | Value |
|-------|-------|
| NAME | MEM |
| FULL_NAME | Memory Encoding / Retrieval |
| CIRCUIT | Mnemonic (memory consolidation & familiarity) |
| OUTPUT_DIM | 30 |
| HORIZONS | H18 (2 s), H20 (5 s), H22 (15 s), H25 (60 s) |

## Description

Memory Encoding / Retrieval models the hippocampal-cortical memory system as it operates during music listening. The mechanism captures two complementary processes: (1) encoding — how novel musical events and patterns are bound into episodic memory traces through hippocampal pattern separation; and (2) retrieval — how previously encountered musical patterns trigger memory reactivation, producing familiarity signals and recollection. The interplay generates the phenomenology of musical memory — recognition, prediction of what comes next, and emotional resonance of familiar music.

## 3x10D Sub-Section Structure

| Dims | Horizon | Computes |
|------|---------|----------|
| 0-9 | H18 (2 s) | Phrase-level encoding: encoding of individual melodic or harmonic phrases into short-term memory. Hippocampal binding of pitch sequences into episodic traces via relational binding (Davachi 2006). Encoding strength based on novelty, distinctiveness, emotional salience. |
| 10-19 | H20 (5 s) | Pattern matching: detection of pattern recurrence across multiple phrases. Thematic return recognition via cortical pattern completion driven by hippocampal reactivation (Henson 2003). Familiarity signal. |
| 20-29 | H22 (15 s) + H25 (60 s) | Context-dependent retrieval and long-term encoding: longer-range memory retrieval cued by musical context over ~15 s (section-level familiarity, recapitulation recognition), integrated with 60 s consolidation tracking modulated by emotional intensity and structural salience (LaBar & Cabeza 2006). |

## H3 Demand

### R3 Feature Inputs

| R3 Domain | Indices | Features | Consuming Units |
|-----------|---------|----------|-----------------|
| A: Consonance | [0]-[6] | harmonicity, roughness, consonance_dissonance, periodicity, fundamental_freq | IMU (11), PCU (HTP, ICEM, PSH), NDU (SLEE), RPU (LDAC) |
| B: Energy | [7]-[11] | onset_strength, loudness, rms_energy, velocity_A | IMU (9), ARU (NEMAC via P5), RPU (LDAC) |
| C: Timbre | [12]-[20] | spectral_centroid, mfcc_vector, spectral_contrast, brightness_kuttruff | IMU (8), PCU (PSH), RPU (LDAC) |
| D: Change | [21]-[24] | spectral_flux, onset_density, delta_loudness | IMU (5), NDU (SLEE) |
| E: Interactions | [25]-[48] | Cross-domain coupling terms | IMU (6), PCU (HTP, ICEM, PSH), NDU (SLEE), RPU (LDAC) |

MEM has the broadest R3 consumption of any mechanism — all five v1 domains are represented. Domain A (Consonance) is the most broadly consumed, reflecting the central role of harmonic structure in musical memory formation and retrieval.

### Per-Horizon Morph Profile

| Horizon | Morphs | Rationale |
|---------|--------|-----------|
| H18 (2 s, 345 frames) | M0 (value), M1 (mean), M2 (std), M3 (median), M4 (max), M5 (range), M18 (trend), M20 (entropy) | Phrase-level encoding — full statistical suite for characterising episodic traces; entropy measures information content driving encoding strength (Davachi 2006) |
| H20 (5 s, 861 frames) | M0 (value), M1 (mean), M2 (std), M3 (median), M5 (range), M18 (trend), M20 (entropy) | Pattern matching — thematic return recognition via cortical pattern completion; entropy and trend capture familiarity signal |
| H22 (15 s, 2584 frames) | M0 (value), M1 (mean), M2 (std), M18 (trend), M20 (entropy) | Section-level retrieval — context-dependent memory over ~15 s; reduced morph set reflects consolidated structural memory |
| H25 (60 s, 10336 frames) | M0 (value), M1 (mean), M18 (trend), M20 (entropy) | Long-term consolidation — 60 s window for movement/piece-level memory; minimal morph set for abstract encoding modulated by emotional intensity |

MEM has the richest statistical morph profile of any mechanism (8 distinct morphs including M3 median, M4 max, M5 range). Entropy (M20) is the signature morph — it appears at all four horizons, measuring information content that drives encoding strength and novelty detection.

### Law Distribution

| Law | Units | Models | Rationale |
|-----|-------|:------:|-----------|
| L0 (Memory) | IMU, ARU, RPU | 15 | Memory retrieval reconstructs past from stored traces — inherently causal |
| L1 (Prediction) | PCU, NDU | 4 | Generating predictions from memory to compute prediction error (PCU) and novelty (NDU) |
| L2 (Integration) | IMU, PCU, RPU | 5 | Bidirectional binding for cross-modal memory integration and memory-based prediction error |

L0 (Memory) is the dominant law — 15 of 19 consuming models use L0, reflecting MEM's core function of causal memory retrieval. L1 appears in PCU and NDU where memory serves prediction. L2 enables bidirectional memory binding in MEAMN and CDEM.

### Demand Estimate

| Source Unit | Models | Est. Tuples |
|-------------|:------:|:-----------:|
| IMU | 13 | ~500 |
| PCU (HTP, ICEM, PSH) | 3 | ~60 |
| NDU (SLEE) | 1 | ~15 |
| RPU (LDAC) | 1 | ~15 |
| ARU (NEMAC) | 1 | ~10 |
| **Total (deduplicated)** | **19** | **~600** |

MEM is the highest-demand mechanism by tuple count (~600), reflecting the centrality of memory encoding/retrieval in music cognition. IMU contributes 83% of the total demand.

## Models Using This Mechanism

### IMU (Integrative Memory Unit)
- **MEAMN** — Memory Encoding and Maintenance Network
- **PNH** — Parahippocampal Novelty Hub
- **MMP** — Medial-temporal Memory Processor
- **HCMC** — Hippocampal-Cortical Memory Circuit
- **OII** — Olfactory-Integrative Interface
- **CDEM** — Context-Dependent Episodic Memory
- **CSSL** — Cortical Statistical Sequence Learning
- **DMMS** — Distributed Memory and Matching System
- **RIRI** — Recognition, Integration, and Retrieval Interface
- **VRIAP** — Visual-Rhythmic Integration and Associative Processing
- **CMAPCC** — Cross-Modal Associative Processing in Cortical Circuits
- **RASN** — Rhythm and Associative Sequence Network
- **PMIM** — Predictive Memory Integration Model

### ARU (Affective Resonance Unit)
- **NEMAC** — Neuroendocrine Modulation of Affective Coding

### PCU (Predictive Coding Unit)
- **HTP** — Hierarchical Temporal Prediction
- **PSH** — Predictive Sensory Hierarchy
- **WMED** — Working Memory for Emotion Dynamics

### RPU (Regulatory Processing Unit)
- **MEAMR** — Memory-Emotion Associative Modulation and Regulation

### NDU (Novelty Detection Unit)
- **SLEE** — Statistical Learning and Expectation Engine

## Neuroscientific Basis

- Davachi (2006): Item-context binding in hippocampus during episodic memory formation.
- Henson (2003): Neural correlates of recognition memory — familiarity (perirhinal cortex) vs. recollection (hippocampus).
- LaBar & Cabeza (2006): Cognitive neuroscience of emotional memory — amygdala-hippocampal interaction enhancing encoding.
- Janata (2009): Music and the self — how familiar music activates mPFC and autobiographical memory networks.
- Schulkind et al. (1999): Long-term memory for popular music — precise memory for familiar tunes after decades.

## Code Reference

`mi_beta/brain/mechanisms/mem.py`
