# Imagery Circuit -- Simulation & Prediction

**Circuit ID**: `imagery`
**Function**: Mental simulation, auditory imagery, predictive modeling, expectation generation

---

## Overview

The imagery circuit is defined in `CIRCUIT_NAMES` as the sixth functional neural pathway: "Simulation & Prediction." It represents the brain's capacity to generate internal auditory representations in the absence of external sound -- hearing music "in one's head" -- and to use these simulated representations to drive prediction, expectation, and emotional anticipation.

Unlike the other five circuits, the imagery circuit does not have a dedicated entry in the `CIRCUITS` tuple (which lists only the five circuits used for cross-unit pathway routing: perceptual, sensorimotor, mnemonic, mesolimbic, salience). The imagery function is instead distributed across units and mechanisms that contribute to simulation and prediction:

- **PCU** (Predictive Coding Unit) is the primary computational substrate, generating predictions about upcoming musical events through harmonic tension, uncertainty processing, and imagery-cognition coupling.
- **SPU** contributes via the MIAA (Musical Imagery Auditory Activation) model, which activates auditory cortex representations during imagery.
- **IMU** contributes via memory-based prediction -- familiar music enables vivid auditory imagery through stored templates.

---

## Mechanisms Contributing to Imagery

The imagery circuit draws on mechanisms from multiple other circuits rather than having dedicated mechanisms:

| Mechanism | Source Circuit | Contribution to Imagery |
|-----------|--------------|------------------------|
| **PPC** | Perceptual | Pitch templates for imagined sounds |
| **TPC** | Perceptual | Timbre templates for imagined instruments |
| **MEM** | Mnemonic | Stored representations enabling re-simulation |
| **SYN** | Mnemonic | Syntactic expectations generate predictive imagery |
| **C0P** | Mesolimbic | Cognitive projection of anticipated events |

PCU uses PPC + TPC + MEM (three mechanisms), making it the only unit that draws on three simultaneous mechanism streams. This reflects the integrative nature of imagery: simulating sound requires pitch templates (PPC), timbre templates (TPC), and memory of what was heard before (MEM).

---

## Primary Unit

| Unit | Full Name | Circuit Assignment | Pooled d | Dependency |
|------|-----------|-------------------|----------|------------|
| **PCU** | Predictive Coding Unit | mnemonic (code) / imagery (functional) | 0.58 | Independent (Phase 2) |

PCU is formally assigned to the `mnemonic` circuit in the codebase (for pathway routing purposes), but its functional role is most naturally described as imagery/simulation. Its 9 models generate predictions, process uncertainty, and simulate upcoming musical events.

---

## Key Brain Regions

| Region | Abbreviation | Function in Imagery |
|--------|-------------|-------------------|
| Auditory Cortex | AC | Activated during auditory imagery without external sound |
| Inferior Frontal Gyrus | IFG | Top-down control of imagery; prediction generation |
| Superior Temporal Sulcus | STS | Multimodal integration, voice/instrument imagery |
| Hippocampus | Hipp | Memory-based imagery; recollection-driven simulation |
| Dorsolateral Prefrontal Cortex | dlPFC | Working memory for maintaining imagined sequences |
| Supplementary Motor Area | SMA | Motor imagery of performance; rhythmic simulation |

---

## Information Flow

```
[Stored Memory (MEM)] --> [PCU: prediction generation]
         |                         |
         v                         v
[Familiar patterns] --> [Imagery templates] --> [Expected next events]
                              |
[PPC: pitch templates] ------+
[TPC: timbre templates] -----+
                              |
                              v
                    [PCU Model Stack (94D)]
                              |
                    +---------+---------+
                    |         |         |
                    v         v         v
            [HTP: tension] [SPH: space] [ICEM: emotion]
            [PWUP: uncertainty] [UDP: pleasure] [WMED: WM-emotion]
            [IGFE: gamma] [MAA: atonal] [PSH: silencing]
                              |
                              v
                    [Prediction / Expectation Signals]
```

1. Memory representations (MEM) provide the substrate for imagery -- you can only imagine what you have encountered.
2. Perceptual templates (PPC, TPC) structure the content of imagery in terms of pitch and timbre.
3. PCU models integrate these inputs to generate expectations about upcoming events.
4. Prediction errors (when reality deviates from imagery) propagate to reward (mesolimbic) and novelty (salience) circuits.

---

## Models

### Alpha (k >= 10, >90% confidence)

| Model | Full Name | Output |
|-------|-----------|--------|
| [PCU-a1-HTP](../Models/PCU-a1-HTP/HTP.md) | Hierarchical Temporal Prediction | 12D |
| [PCU-a2-SPH](../Models/PCU-a2-SPH/SPH.md) | Spatiotemporal Prediction Hierarchy | 11D |
| [PCU-a3-ICEM](../Models/PCU-a3-ICEM/ICEM.md) | Information Content Emotion Model | 11D |

### Beta (5 <= k < 10, 70--90% confidence)

| Model | Full Name | Output |
|-------|-----------|--------|
| [PCU-b1-PWUP](../Models/PCU-b1-PWUP/PWUP.md) | Precision-Weighted Uncertainty Processing | 10D |
| [PCU-b2-WMED](../Models/PCU-b2-WMED/WMED.md) | Working Memory-Entrainment Dissociation | 10D |
| [PCU-b3-UDP](../Models/PCU-b3-UDP/UDP.md) | Uncertainty-Driven Pleasure | 10D |
| [PCU-b4-CHPI](../Models/PCU-b4-CHPI/CHPI.md) | Cross-Modal Harmonic Predictive Integration | 11D |

### Gamma (k < 5, <70% confidence)

| Model | Full Name | Output |
|-------|-----------|--------|
| [PCU-g1-IGFE](../Models/PCU-g1-IGFE/IGFE.md) | Individual Gamma Frequency Enhancement | 10D |
| [PCU-g2-MAA](../Models/PCU-g2-MAA/MAA.md) | Multifactorial Atonal Appreciation | 10D |
| [PCU-g3-PSH](../Models/PCU-g3-PSH/PSH.md) | Prediction Silencing Hypothesis | 10D |

### Contributing Models from Other Units

| Model | Full Name | Unit | Relevance |
|-------|-----------|------|-----------|
| SPU-b3-MIAA | Musical Imagery Auditory Activation | SPU | Auditory cortex activation during imagery |
| IMU-b2-PMIM | Predictive Memory Integration Model | IMU | Memory-driven prediction |
| ARU-b1-PUPF | Pleasure-Uncertainty-Prediction Function | ARU | Affective consequences of prediction |

---

## Key Evidence

- **Halpern & Zatorre (1999)**: Auditory imagery activates secondary auditory cortex (not A1), demonstrating top-down activation of perceptual representations.
- **Huron (2006)**: ITPRA model -- Imagination phase precedes Tension, Prediction, Reaction, Appraisal; imagery is the first step in musical expectation.
- **Pearce & Wiggins (2012)**: IDyOM (Information Dynamics of Music) -- statistical model of melodic expectation predicts ERP responses and behavioral ratings.
- **Kosslyn et al. (2001)**: Mental imagery as "simulation" using the same neural circuits as perception; applies to auditory domain.
- **Zatorre & Halpern (2005)**: Review of auditory imagery -- shared neural substrates between perception and imagination in auditory cortex.
- **Koelsch et al. (2019)**: Predictive coding in music -- hierarchical generative models maintain predictions at multiple timescales.
- **Clark (2013)**: Predictive processing framework -- the brain as a prediction machine that minimizes surprise through generative models.

---

## Cross-References

- **Units**: [PCU](../Units/PCU.md) | [SPU](../Units/SPU.md) (MIAA model) | [IMU](../Units/IMU.md) (PMIM model)
- **Mechanisms**: [PPC](../Mechanisms/PPC.md) | [TPC](../Mechanisms/TPC.md) | [MEM](../Mechanisms/MEM.md) | [SYN](../Mechanisms/SYN.md)
- **Related Circuits**: [Mnemonic](Mnemonic.md) (PCU formally assigned here; memory enables imagery) | [Perceptual](Perceptual.md) (PPC+TPC provide imagery templates) | [Mesolimbic](Mesolimbic.md) (prediction error drives reward)

---

## Note on Circuit Architecture

The imagery circuit occupies a unique position in the C3 architecture. It is listed in `CIRCUIT_NAMES` (6 circuits) but not in `CIRCUITS` (5 circuits used for pathway routing). This reflects its nature as a *functional* rather than *structural* circuit: imagery is an emergent property of coordinated activity across perceptual, mnemonic, and mesolimbic systems, rather than a distinct anatomical pathway. The PCU is the closest single-unit embodiment of this function, but true auditory imagery requires the full network.
