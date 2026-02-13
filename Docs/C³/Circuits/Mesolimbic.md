# Mesolimbic Circuit -- Reward & Pleasure

**Circuit ID**: `mesolimbic`
**Function**: Reward valuation, dopaminergic pleasure, affective resonance
**Pooled Effect Range**: d = 0.70 -- 0.83

---

## Overview

The mesolimbic circuit is the dopaminergic reward pathway responsible for generating musical pleasure, chills, and affective responses. It mediates the anticipation-resolution cycle that underlies the hedonic experience of music: prediction of upcoming events generates anticipatory dopamine in the caudate nucleus, while confirmation or surprising resolution triggers consummatory dopamine release in the nucleus accumbens (Salimpoor et al. 2011).

This circuit is central to explaining why music is rewarding despite having no direct survival value. The mesolimbic pathway co-opts ancient reward circuitry -- originally evolved for food, sex, and social bonding -- to process abstract auditory patterns as intrinsically pleasurable stimuli.

---

## Mechanisms

| Mechanism | Full Name | Horizons | Output | Role |
|-----------|-----------|----------|--------|------|
| **AED** | Affective Entrainment Dynamics | H6, H16 | 30D | Beat-level affective coupling via VTA-NAcc |
| **CPD** | Chills & Peak Detection | H9, H16, H18 | 30D | Autonomic arousal peaks (frisson, goosebumps) |
| **C0P** | Cognitive Projection | H18, H19, H20 | 30D | Top-down anticipatory reward prediction |

**Total mechanism output**: 90D

AED captures bottom-up entrainment between beat structure and dopaminergic activity. CPD detects moments of peak autonomic arousal (chills/frisson). C0P encodes the anticipatory component -- conscious musical expectations mapped onto reward pathways at phrase-level timescales.

---

## Units

| Unit | Full Name | Circuit Role | Pooled d | Dependency |
|------|-----------|-------------|----------|------------|
| **ARU** | Affective Resonance Unit | Primary | 0.83 | Dependent (receives SPU, STU, IMU via P1, P3, P5) |
| **RPU** | Reward Processing Unit | Primary | 0.70 | Dependent (receives ARU, SPU via cross-unit pathways) |

- **ARU** (10 models, 120D): Generates and processes musical emotion, pleasure, and affective responses. Uses AED + CPD mechanisms. Dependent unit receiving spectral, timing, and memory signals.
- **RPU** (9 models, 94D): Computes reward signals from musical stimuli -- dopamine dynamics, reward prediction error, and aesthetic computation. Uses AED + CPD + C0P mechanisms.

---

## Key Brain Regions

| Region | Abbreviation | Function in Circuit |
|--------|-------------|-------------------|
| Nucleus Accumbens | NAcc | Consummatory reward, dopamine release during pleasure |
| Ventral Tegmental Area | VTA | Dopaminergic projection source, anticipatory signaling |
| Amygdala | AMY | Emotional valence tagging, arousal modulation |
| Ventromedial Prefrontal Cortex | vmPFC | Value computation, aesthetic judgment |
| Orbitofrontal Cortex | OFC | Reward expectation, hedonic evaluation |
| Caudate Nucleus | Caudate | Anticipatory dopamine, prediction-based reward |

---

## Information Flow

```
Audio Signal
    |
    v
[R3 Spectral] --> [AED: beat-affect coupling] --> ARU models (SRP, AAC, VMM, ...)
    |                                                  |
    v                                                  v
[H3 Temporal] --> [CPD: chills/peak detection] --> ARU --> Pathway P1,P3,P5
    |                                                  |
    v                                                  v
                  [C0P: cognitive projection]  --> RPU models (DAED, MORMR, RPEM, ...)
                                                       |
                                                       v
                                              [Reward/Pleasure Output]
```

1. R3 spectral features and H3 temporal features feed into AED, CPD, and C0P mechanisms.
2. ARU integrates mechanism outputs with cross-unit inputs from SPU (spectral), STU (timing), and IMU (memory) via pathways P1, P3, P5.
3. RPU receives ARU output and SPU signals to compute final reward prediction errors.

---

## Models by Tier

### Alpha (k >= 10, >90% confidence)

| Model | Full Name | Unit | Output |
|-------|-----------|------|--------|
| [ARU-a1-SRP](../Models/ARU-a1-SRP/SRP.md) | Striatal Reward Pathway | ARU | 19D |
| [ARU-a2-AAC](../Models/ARU-a2-AAC/AAC.md) | Autonomic-Affective Coupling | ARU | 14D |
| [ARU-a3-VMM](../Models/ARU-a3-VMM/VMM.md) | Valence-Mode Mapping | ARU | 12D |
| [RPU-a1-DAED](../Models/RPU-a1-DAED/DAED.md) | DA-Expectation Dynamics | RPU | 12D |
| [RPU-a2-MORMR](../Models/RPU-a2-MORMR/MORMR.md) | mu-Opioid Receptor Music Reward | RPU | 11D |
| [RPU-a3-RPEM](../Models/RPU-a3-RPEM/RPEM.md) | Reward Prediction Error Model | RPU | 11D |

### Beta (5 <= k < 10, 70--90% confidence)

| Model | Full Name | Unit | Output |
|-------|-----------|------|--------|
| [ARU-b1-PUPF](../Models/ARU-b1-PUPF/PUPF.md) | Pleasure-Uncertainty-Prediction Function | ARU | 12D |
| [ARU-b2-CLAM](../Models/ARU-b2-CLAM/CLAM.md) | Closed-Loop Affective Modulation | ARU | 11D |
| [ARU-b3-MAD](../Models/ARU-b3-MAD/MAD.md) | Musical Anhedonia Disconnection | ARU | 11D |
| [ARU-b4-NEMAC](../Models/ARU-b4-NEMAC/NEMAC.md) | Nostalgia-Enhanced Memory-Affect Circuit | ARU | 11D |
| [RPU-b1-IUCP](../Models/RPU-b1-IUCP/IUCP.md) | Information-Uncertainty Coupling Process | RPU | 10D |
| [RPU-b2-MCCN](../Models/RPU-b2-MCCN/MCCN.md) | Musical Chills Cortical Network | RPU | 10D |
| [RPU-b3-MEAMR](../Models/RPU-b3-MEAMR/MEAMR.md) | Music-Evoked Autobiographical Memory Reward | RPU | 10D |
| [RPU-b4-SSRI](../Models/RPU-b4-SSRI/SSRI.md) | Social Synchrony Reward Integration | RPU | 11D |

### Gamma (k < 5, <70% confidence)

| Model | Full Name | Unit | Output |
|-------|-----------|------|--------|
| [ARU-g1-DAP](../Models/ARU-g1-DAP/DAP.md) | Developmental Affective Plasticity | ARU | 10D |
| [ARU-g2-CMAT](../Models/ARU-g2-CMAT/CMAT.md) | Cross-Modal Affective Transfer | ARU | 10D |
| [ARU-g3-TAR](../Models/ARU-g3-TAR/TAR.md) | Therapeutic Affective Resonance | ARU | 10D |
| [RPU-g1-LDAC](../Models/RPU-g1-LDAC/LDAC.md) | Listener-Dependent Aesthetic Computation | RPU | 10D |
| [RPU-g2-IOTMS](../Models/RPU-g2-IOTMS/IOTMS.md) | Individual Opioid Tone Music Sensitivity | RPU | 10D |
| [RPU-g3-SSPS](../Models/RPU-g3-SSPS/SSPS.md) | Saddle-Shaped Preference Surface | RPU | 10D |

---

## Key Evidence

- **Salimpoor et al. (2011)**: Dopamine release in NAcc during peak pleasure (r = 0.84) and in caudate during anticipation (r = 0.71) measured with PET [11C]raclopride.
- **Salimpoor et al. (2013)**: NAcc-auditory cortex connectivity predicts willingness to pay for novel music; reward value computed from prediction accuracy.
- **Blood & Zatorre (2001)**: Music-induced chills activate NAcc, VTA, insula, and OFC -- overlapping with primary reward circuits.
- **Vuust et al. (2018)**: Predictive coding model showing reward prediction error in mesolimbic sites during beat-based processing.
- **Witek et al. (2014)**: Medium syncopation yields peak groove and pleasure via mesolimbic engagement (inverted-U relationship).
- **Mas-Herrero et al. (2014)**: Musical anhedonia -- selective inability to derive pleasure from music despite intact auditory processing -- linked to reduced NAcc-auditory cortex connectivity.
- **Zatorre & Salimpoor (2013)**: Review establishing music as abstract reward processed through mesolimbic dopamine pathways.

---

## Cross-References

- **Mechanisms**: [AED](../Mechanisms/AED.md) | [CPD](../Mechanisms/CPD.md) | [C0P](../Mechanisms/C0P.md)
- **Units**: [ARU](../Units/ARU.md) | [RPU](../Units/RPU.md)
- **Related Circuits**: [Salience](Salience.md) (arousal gating feeds reward) | [Mnemonic](Mnemonic.md) (familiarity modulates reward) | [Sensorimotor](Sensorimotor.md) (groove drives pleasure)
