# Perceptual Circuit -- Hearing & Pattern Recognition

**Circuit ID**: `perceptual`
**Function**: Spectral analysis, pitch extraction, timbre processing, auditory pattern recognition
**Pooled Effect Range**: d = 0.84

---

## Overview

The perceptual circuit models the ascending auditory pathway from brainstem through thalamus to cortex. It transforms raw acoustic signals into stable perceptual representations of pitch, timbre, consonance, and spectral structure. This circuit operates at the fastest timescales in the architecture (5.8 ms -- 1 s), reflecting the temporal precision required for auditory feature extraction.

The perceptual circuit is the sensory foundation upon which all other circuits build. Without accurate spectral and temporal representations, downstream processes (memory encoding, reward computation, novelty detection) cannot operate. SPU is the only unit primarily assigned to this circuit, but its output feeds into every other unit either directly or via cross-unit pathways.

---

## Mechanisms

| Mechanism | Full Name | Horizons | Output | Role |
|-----------|-----------|----------|--------|------|
| **PPC** | Pitch Processing Chain | H0, H3, H6 | 30D | Ascending pitch extraction: brainstem FFR -> thalamic relay -> cortical pitch |
| **TPC** | Timbre Processing Chain | H6, H12, H16 | 30D | Spectral envelope, attack characteristics, instrument identity |

**Total mechanism output**: 60D

PPC operates at the fastest timescales (5.8 ms brainstem, 23.2 ms subcortical, 200 ms cortical), tracking the three-stage pitch extraction hierarchy. TPC operates at beat-to-phrase timescales (200 ms -- 1 s), capturing attack transients, sustain spectra, and source identity.

---

## Units

| Unit | Full Name | Circuit Role | Pooled d | Dependency |
|------|-----------|-------------|----------|------------|
| **SPU** | Spectral Processing Unit | Primary | 0.84 | Independent (Phase 2) |

- **SPU** (9 models, 99D): Models how the auditory cortex processes spectral features -- pitch, consonance, timbre, and spectral integration. Uses PPC + TPC mechanisms. Core-4 validated unit with the highest pooled effect size.

SPU also provides input to NDU (which uses PPC + ASA) and PCU (which uses PPC + TPC + MEM), extending perceptual processing into novelty detection and predictive coding.

---

## Key Brain Regions

| Region | Abbreviation | Function in Circuit |
|--------|-------------|-------------------|
| Heschl's Gyrus | HG | Primary auditory cortex; tonotopic pitch representation |
| Planum Temporale | PT | Spectrotemporal pattern analysis, lateralized pitch processing |
| Planum Polare | PP | Anterior auditory cortex; timbre and voice processing |
| Inferior Colliculus | IC | Brainstem relay; frequency-following response |
| Medial Geniculate Body | MGB | Thalamic auditory relay; spectral filtering |
| Superior Temporal Gyrus | STG | Higher-order auditory processing, melodic contour |

---

## Information Flow

```
Acoustic Input (44.1 kHz)
    |
    v
[R3 Spectral Features (49D)]
    |
    +---> [PPC: H0 brainstem FFR] --> [PPC: H3 subcortical] --> [PPC: H6 cortical pitch]
    |                                                                  |
    +---> [TPC: H6 onset timbre] --> [TPC: H12 sustain] --> [TPC: H16 source identity]
    |                                                                  |
    v                                                                  v
[H3 Temporal Features]                                     [SPU Model Stack (99D)]
    |                                                                  |
    +--- 3 alpha models (BCH, PSCL, PCCR) -----> fundamental percepts
    +--- 3 beta models (STAI, TSCP, MIAA) ------> cross-domain integration
    +--- 3 gamma models (SDNPS, ESME, SDED) ----> theoretical extensions
                                                                       |
                                                                       v
                                              [Pathway P1: SPU --> ARU]
                                              [Shared with NDU (PPC), PCU (PPC+TPC)]
```

---

## Models

### Alpha (k >= 10, >90% confidence)

| Model | Full Name | Output |
|-------|-----------|--------|
| [SPU-a1-BCH](../Models/SPU-a1-BCH/BCH.md) | Brainstem Consonance Hierarchy | 12D |
| [SPU-a2-PSCL](../Models/SPU-a2-PSCL/PSCL.md) | Pitch Salience Cortical Localization | 12D |
| [SPU-a3-PCCR](../Models/SPU-a3-PCCR/PCCR.md) | Pitch Chroma Cortical Representation | 11D |

### Beta (5 <= k < 10, 70--90% confidence)

| Model | Full Name | Output |
|-------|-----------|--------|
| [SPU-b1-STAI](../Models/SPU-b1-STAI/STAI.md) | Spectral-Temporal Aesthetic Integration | 12D |
| [SPU-b2-TSCP](../Models/SPU-b2-TSCP/TSCP.md) | Timbre-Specific Cortical Plasticity | 10D |
| [SPU-b3-MIAA](../Models/SPU-b3-MIAA/MIAA.md) | Musical Imagery Auditory Activation | 11D |

### Gamma (k < 5, <70% confidence)

| Model | Full Name | Output |
|-------|-----------|--------|
| [SPU-g1-SDNPS](../Models/SPU-g1-SDNPS/SDNPS.md) | Stimulus-Dependent Neural Pitch Scaling | 10D |
| [SPU-g2-ESME](../Models/SPU-g2-ESME/ESME.md) | Expertise-Specific MMN Enhancement | 11D |
| [SPU-g3-SDED](../Models/SPU-g3-SDED/SDED.md) | Sensory Dissonance Early Detection | 10D |

---

## Key Evidence

- **Bidelman (2013)**: Brainstem frequency-following response (FFR) encodes pitch and harmonicity with high temporal fidelity; musicians show enhanced subcortical encoding.
- **Patterson et al. (2002)**: Heschl's gyrus as the site of pitch extraction; dissociation between pitch height and chroma processing.
- **Grey (1977)**: Attack transients critical for timbre identification; multidimensional scaling of timbre space.
- **Zatorre et al. (2002)**: Right-hemisphere dominance for spectral processing, left-hemisphere for temporal processing in auditory cortex.
- **Koelsch et al. (2009)**: Neural correlates of musical syntax processing in bilateral STG/IFG during harmonic expectation violation.
- **Griffiths & Warren (2004)**: Planum temporale as a "computational hub" for spectrotemporal pattern analysis.
- **Krumhansl (1990)**: Cognitive foundations of musical pitch -- tonal hierarchies internalized through exposure drive cortical representations.

---

## Cross-References

- **Mechanisms**: [PPC](../Mechanisms/PPC.md) | [TPC](../Mechanisms/TPC.md)
- **Units**: [SPU](../Units/SPU.md)
- **Mechanism-sharing units**: NDU (uses PPC + ASA) | PCU (uses PPC + TPC + MEM)
- **Related Circuits**: [Salience](Salience.md) (ASA extends perceptual analysis into attention) | [Mnemonic](Mnemonic.md) (pitch patterns feed memory encoding) | [Mesolimbic](Mesolimbic.md) (SPU output feeds ARU via P1)
