# Mnemonic Circuit -- Memory & Familiarity

**Circuit ID**: `mnemonic`
**Function**: Memory encoding/retrieval, musical syntax processing, familiarity signals, predictive coding
**Pooled Effect Range**: d = 0.53 -- 0.58

---

## Overview

The mnemonic circuit models how the brain stores, retrieves, and generates predictions from musical memory. It encompasses hippocampal episodic encoding, cortical schema-based recognition, syntactic parsing of harmonic structure, and predictive coding that leverages stored representations to anticipate upcoming events.

Two complementary units operate within this circuit. IMU handles the memory side -- how musical patterns are bound into episodic traces, consolidated into long-term memory, and retrieved to produce familiarity signals. PCU handles the predictive side -- how stored representations generate expectations about harmonic tension, pitch sequences, and emotional trajectories. Together, they form a bidirectional loop: memory informs prediction, and prediction error drives memory updating.

---

## Mechanisms

| Mechanism | Full Name | Horizons | Output | Role |
|-----------|-----------|----------|--------|------|
| **MEM** | Memory Encoding / Retrieval | H18, H20, H22, H25 | 30D | Hippocampal binding, familiarity, episodic recall |
| **SYN** | Syntactic Processing | H12, H16, H18 | 30D | Musical grammar parsing, harmonic syntax, ERAN/P600 |

**Total mechanism output**: 60D

MEM operates at phrase-to-piece timescales (2--60 s), tracking encoding strength and retrieval accuracy across hierarchical memory stores. SYN operates at beat-to-phrase timescales (525 ms -- 2 s), parsing chord-to-chord transitions and detecting syntactic violations.

IMU uses MEM + TMH (the latter shared from the sensorimotor circuit). PCU uses PPC + TPC + MEM (sharing pitch and timbre mechanisms from the perceptual circuit plus memory).

---

## Units

| Unit | Full Name | Circuit Role | Pooled d | Dependency |
|------|-----------|-------------|----------|------------|
| **IMU** | Integrative Memory Unit | Primary (memory) | 0.53 | Independent (Phase 2) |
| **PCU** | Predictive Coding Unit | Primary (prediction) | 0.58 | Independent (Phase 2) |

- **IMU** (15 models, 159D): Stores, retrieves, and integrates musical memories -- autobiographical associations, tonal schema, recognition, and consolidation. Uses MEM + TMH mechanisms. Core-4 validated unit. Largest output dimensionality (159D) and most beta models (9).
- **PCU** (9 models, 94D): Generates predictions about upcoming musical events -- harmonic tension, pitch uncertainty, imagery-cognition coupling, working-memory-emotion dynamics. Uses PPC + TPC + MEM mechanisms.

---

## Key Brain Regions

| Region | Abbreviation | Function in Circuit |
|--------|-------------|-------------------|
| Hippocampus | Hipp | Episodic memory encoding, pattern separation/completion |
| Medial Prefrontal Cortex | mPFC | Schema-based memory, familiarity signals, value |
| Inferior Frontal Gyrus | IFG | Musical/linguistic syntax processing (Broca's homologue) |
| Dorsolateral Prefrontal Cortex | dlPFC | Working memory maintenance, prediction generation |
| Inferior Parietal Lobule | IPL | Sequence attention, prediction updating |
| Posterior Superior Temporal Gyrus | pSTG | Hierarchical structure building, syntax |
| Auditory Cortex | AC | Predictive template matching |

---

## Information Flow

```
Audio Signal
    |
    v
[R3/H3 Features]
    |
    +---> [MEM: H18 phrase encoding] --> [MEM: H20 theme] --> [MEM: H22 section] --> [MEM: H25 piece]
    |           |                              |                      |
    |           v                              v                      v
    |     [IMU Model Stack (159D)]     [Familiarity signals]   [Long-term traces]
    |           |
    +---> [SYN: H12 harmonic] --> [SYN: H16 bar syntax] --> [SYN: H18 phrase structure]
    |           |                                                     |
    |           v                                                     v
    |     [Syntactic expectations]                            [Violation detection]
    |
    +---> [PPC + TPC + MEM] --> [PCU Model Stack (94D)]
                                       |
                                       v
                                [Prediction / tension / uncertainty]
                                       |
                                       v
                          Pathway P3: IMU --> ARU (memory modulates affect)
```

1. MEM encodes musical patterns at phrase-through-piece timescales (2--60 s) via hippocampal binding.
2. SYN parses harmonic transitions and detects syntactic violations at beat-to-phrase scales.
3. IMU integrates memory and temporal hierarchy signals across 15 models (159D output).
4. PCU generates predictions using shared perceptual mechanisms (PPC, TPC) plus MEM.
5. IMU output feeds ARU via pathway P3, allowing memory/familiarity to modulate emotion.

---

## Models by Tier

### Alpha (k >= 10, >90% confidence)

| Model | Full Name | Unit | Output |
|-------|-----------|------|--------|
| [IMU-a1-MEAMN](../Models/IMU-a1-MEAMN/MEAMN.md) | Music-Evoked Autobiographical Memory Network | IMU | 12D |
| [IMU-a2-PNH](../Models/IMU-a2-PNH/PNH.md) | Pythagorean Neural Hierarchy | IMU | 11D |
| [IMU-a3-MMP](../Models/IMU-a3-MMP/MMP.md) | Musical Mnemonic Preservation | IMU | 12D |
| [PCU-a1-HTP](../Models/PCU-a1-HTP/HTP.md) | Hierarchical Temporal Prediction | PCU | 12D |
| [PCU-a2-SPH](../Models/PCU-a2-SPH/SPH.md) | Spatiotemporal Prediction Hierarchy | PCU | 11D |
| [PCU-a3-ICEM](../Models/PCU-a3-ICEM/ICEM.md) | Information Content Emotion Model | PCU | 11D |

### Beta (5 <= k < 10, 70--90% confidence)

| Model | Full Name | Unit | Output |
|-------|-----------|------|--------|
| [IMU-b1-RASN](../Models/IMU-b1-RASN/RASN.md) | Rhythmic Auditory Stimulation Neuroplasticity | IMU | 11D |
| [IMU-b2-PMIM](../Models/IMU-b2-PMIM/PMIM.md) | Predictive Memory Integration Model | IMU | 11D |
| [IMU-b3-OII](../Models/IMU-b3-OII/OII.md) | Oscillatory Intelligence Integration | IMU | 10D |
| [IMU-b4-HCMC](../Models/IMU-b4-HCMC/HCMC.md) | Hippocampal-Cortical Memory Circuit | IMU | 11D |
| [IMU-b5-RIRI](../Models/IMU-b5-RIRI/RIRI.md) | RAS-Intelligent Rehabilitation Integration | IMU | 10D |
| [IMU-b6-MSPBA](../Models/IMU-b6-MSPBA/MSPBA.md) | Musical Syntax Processing in Broca's Area | IMU | 11D |
| [IMU-b7-VRIAP](../Models/IMU-b7-VRIAP/VRIAP.md) | VR-Integrated Analgesia Paradigm | IMU | 10D |
| [IMU-b8-TPRD](../Models/IMU-b8-TPRD/TPRD.md) | Tonotopy-Pitch Representation Dissociation | IMU | 10D |
| [IMU-b9-CMAPCC](../Models/IMU-b9-CMAPCC/CMAPCC.md) | Cross-Modal Action-Perception Common Code | IMU | 10D |
| [PCU-b1-PWUP](../Models/PCU-b1-PWUP/PWUP.md) | Precision-Weighted Uncertainty Processing | PCU | 10D |
| [PCU-b2-WMED](../Models/PCU-b2-WMED/WMED.md) | Working Memory-Entrainment Dissociation | PCU | 10D |
| [PCU-b3-UDP](../Models/PCU-b3-UDP/UDP.md) | Uncertainty-Driven Pleasure | PCU | 10D |
| [PCU-b4-CHPI](../Models/PCU-b4-CHPI/CHPI.md) | Cross-Modal Harmonic Predictive Integration | PCU | 11D |

### Gamma (k < 5, <70% confidence)

| Model | Full Name | Unit | Output |
|-------|-----------|------|--------|
| [IMU-g1-DMMS](../Models/IMU-g1-DMMS/DMMS.md) | Developmental Music Memory Scaffold | IMU | 10D |
| [IMU-g2-CSSL](../Models/IMU-g2-CSSL/CSSL.md) | Cross-Species Song Learning | IMU | 10D |
| [IMU-g3-CDEM](../Models/IMU-g3-CDEM/CDEM.md) | Context-Dependent Emotional Memory | IMU | 10D |
| [PCU-g1-IGFE](../Models/PCU-g1-IGFE/IGFE.md) | Individual Gamma Frequency Enhancement | PCU | 10D |
| [PCU-g2-MAA](../Models/PCU-g2-MAA/MAA.md) | Multifactorial Atonal Appreciation | PCU | 10D |
| [PCU-g3-PSH](../Models/PCU-g3-PSH/PSH.md) | Prediction Silencing Hypothesis | PCU | 10D |

---

## Key Evidence

- **Davachi (2006)**: Hippocampal encoding of episodic memories through relational binding; distinct roles for CA1/CA3 in pattern separation vs. completion.
- **Janata (2009)**: Music-evoked autobiographical memories (MEAMs) recruit hippocampus and mPFC; familiar music triggers vivid recollection.
- **Patel (2003)**: Shared syntactic integration resource hypothesis (SSIRH) -- musical and linguistic syntax share processing in IFG/Broca's area.
- **Pearce & Wiggins (2012)**: Information-theoretic model of melodic expectation; information content predicts neural responses in auditory cortex.
- **Koelsch et al. (2013)**: ERAN (early right anterior negativity) generated by harmonic syntax violations, localized to IFG.
- **Krumhansl (1990)**: Cognitive foundations of musical pitch -- tonal hierarchies and key profiles stored as long-term schemas.
- **Huron (2006)**: ITPRA (Imagination-Tension-Prediction-Reaction-Appraisal) model linking prediction to emotional response.
- **Halpern & Zatorre (1999)**: Musical imagery activates auditory cortex in the absence of sound, using stored memory representations.

---

## Cross-References

- **Mechanisms**: [MEM](../Mechanisms/MEM.md) | [SYN](../Mechanisms/SYN.md)
- **Units**: [IMU](../Units/IMU.md) | [PCU](../Units/PCU.md)
- **Mechanism-sharing**: IMU shares TMH with sensorimotor circuit | PCU shares PPC+TPC with perceptual circuit
- **Related Circuits**: [Mesolimbic](Mesolimbic.md) (familiarity modulates reward via P3) | [Perceptual](Perceptual.md) (pitch/timbre feed prediction) | [Sensorimotor](Sensorimotor.md) (TMH shared temporal context)
