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

To be populated in Phase 6. Will declare demands for entropy, stability, periodicity, and trend morphs at H18/H20/H22/H25 to track novelty, repetition, and encoding strength.

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
