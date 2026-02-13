# Alpha Tier -- Foundational Models

**Tier Symbol**: alpha
**Evidence Standard**: >90% confidence, k >= 10 studies, direct replication evidence
**Count**: 27 models (3 per unit x 9 units)

---

## Definition

Alpha-tier models represent the mechanistic foundation of the C3 architecture. Each alpha model is grounded in direct neural evidence with high replication rates: a minimum of 10 independent studies (k >= 10) with pooled effect sizes establishing causal or strong correlational relationships between acoustic features and specific neural processes.

Alpha models satisfy the strictest evidence criteria in the C3 meta-analysis framework:

| Criterion | Requirement |
|-----------|------------|
| Confidence range | >90% (typically 0.90--0.98) |
| Study count | k >= 10 independent studies |
| Effect sizes | Pooled d or r reported with confidence intervals |
| Replication | Direct replication across labs and paradigms |
| Neural evidence | fMRI, PET, EEG/MEG with source localization, or lesion studies |
| Falsifiability | At least one explicit falsification criterion declared |

---

## Characteristics of Alpha Models

1. **Higher output dimensionality**: Alpha models typically produce 11--19D per frame (vs. 10D for beta/gamma), reflecting richer feature extraction justified by stronger evidence.
2. **Direct neural mappings**: Each dimension corresponds to a well-characterized neural process with known anatomical substrate.
3. **Mature literature**: The phenomena modeled by alpha models have been studied for decades with converging methods (behavioral, neuroimaging, computational).
4. **Stable under revision**: Alpha models are unlikely to require fundamental restructuring, though parameter refinement continues.

---

## Alpha Models by Unit

### SPU -- Spectral Processing Unit (perceptual circuit)

| ID | Acronym | Full Name | Output | Doc |
|----|---------|-----------|--------|-----|
| SPU-a1 | BCH | Brainstem Consonance Hierarchy | 12D | [BCH.md](../Models/SPU-a1-BCH/BCH.md) |
| SPU-a2 | PSCL | Pitch Salience Cortical Localization | 12D | [PSCL.md](../Models/SPU-a2-PSCL/PSCL.md) |
| SPU-a3 | PCCR | Pitch Chroma Cortical Representation | 11D | [PCCR.md](../Models/SPU-a3-PCCR/PCCR.md) |

### STU -- Sensorimotor Timing Unit (sensorimotor circuit)

| ID | Acronym | Full Name | Output | Doc |
|----|---------|-----------|--------|-----|
| STU-a1 | HMCE | Hierarchical Musical Context Encoding | 13D | [HMCE.md](../Models/STU-a1-HMCE/HMCE.md) |
| STU-a2 | AMSC | Auditory-Motor Stream Coupling | 12D | [AMSC.md](../Models/STU-a2-AMSC/AMSC.md) |
| STU-a3 | MDNS | Melody Decoding from Neural Signals | 12D | [MDNS.md](../Models/STU-a3-MDNS/MDNS.md) |

### IMU -- Integrative Memory Unit (mnemonic circuit)

| ID | Acronym | Full Name | Output | Doc |
|----|---------|-----------|--------|-----|
| IMU-a1 | MEAMN | Music-Evoked Autobiographical Memory Network | 12D | [MEAMN.md](../Models/IMU-a1-MEAMN/MEAMN.md) |
| IMU-a2 | PNH | Pythagorean Neural Hierarchy | 11D | [PNH.md](../Models/IMU-a2-PNH/PNH.md) |
| IMU-a3 | MMP | Musical Mnemonic Preservation | 12D | [MMP.md](../Models/IMU-a3-MMP/MMP.md) |

### ARU -- Affective Resonance Unit (mesolimbic circuit)

| ID | Acronym | Full Name | Output | Doc |
|----|---------|-----------|--------|-----|
| ARU-a1 | SRP | Striatal Reward Pathway | 19D | [SRP.md](../Models/ARU-a1-SRP/SRP.md) |
| ARU-a2 | AAC | Autonomic-Affective Coupling | 14D | [AAC.md](../Models/ARU-a2-AAC/AAC.md) |
| ARU-a3 | VMM | Valence-Mode Mapping | 12D | [VMM.md](../Models/ARU-a3-VMM/VMM.md) |

### ASU -- Auditory Salience Unit (salience circuit)

| ID | Acronym | Full Name | Output | Doc |
|----|---------|-----------|--------|-----|
| ASU-a1 | SNEM | Selective Neural Entrainment Model | 12D | [SNEM.md](../Models/ASU-a1-SNEM/SNEM.md) |
| ASU-a2 | IACM | Inharmonicity-Attention Capture Model | 11D | [IACM.md](../Models/ASU-a2-IACM/IACM.md) |
| ASU-a3 | CSG | Consonance-Salience Gradient | 12D | [CSG.md](../Models/ASU-a3-CSG/CSG.md) |

### NDU -- Novelty Detection Unit (salience circuit)

| ID | Acronym | Full Name | Output | Doc |
|----|---------|-----------|--------|-----|
| NDU-a1 | MPG | Melodic Processing Gradient | 12D | [MPG.md](../Models/NDU-a1-MPG/MPG.md) |
| NDU-a2 | SDD | Supramodal Deviance Detection | 11D | [SDD.md](../Models/NDU-a2-SDD/SDD.md) |
| NDU-a3 | EDNR | Expertise-Dependent Network Reorganization | 11D | [EDNR.md](../Models/NDU-a3-EDNR/EDNR.md) |

### MPU -- Motor Planning Unit (sensorimotor circuit)

| ID | Acronym | Full Name | Output | Doc |
|----|---------|-----------|--------|-----|
| MPU-a1 | PEOM | Period Entrainment Optimization Model | 12D | [PEOM.md](../Models/MPU-a1-PEOM/PEOM.md) |
| MPU-a2 | MSR | Musician Sensorimotor Reorganization | 11D | [MSR.md](../Models/MPU-a2-MSR/MSR.md) |
| MPU-a3 | GSSM | Gait-Synchronized Stimulation Model | 11D | [GSSM.md](../Models/MPU-a3-GSSM/GSSM.md) |

### PCU -- Predictive Coding Unit (mnemonic circuit)

| ID | Acronym | Full Name | Output | Doc |
|----|---------|-----------|--------|-----|
| PCU-a1 | HTP | Hierarchical Temporal Prediction | 12D | [HTP.md](../Models/PCU-a1-HTP/HTP.md) |
| PCU-a2 | SPH | Spatiotemporal Prediction Hierarchy | 11D | [SPH.md](../Models/PCU-a2-SPH/SPH.md) |
| PCU-a3 | ICEM | Information Content Emotion Model | 11D | [ICEM.md](../Models/PCU-a3-ICEM/ICEM.md) |

### RPU -- Reward Processing Unit (mesolimbic circuit)

| ID | Acronym | Full Name | Output | Doc |
|----|---------|-----------|--------|-----|
| RPU-a1 | DAED | Dopamine Anticipation-Experience Dissociation | 12D | [DAED.md](../Models/RPU-a1-DAED/DAED.md) |
| RPU-a2 | MORMR | mu-Opioid Receptor Music Reward | 11D | [MORMR.md](../Models/RPU-a2-MORMR/MORMR.md) |
| RPU-a3 | RPEM | Reward Prediction Error in Music | 11D | [RPEM.md](../Models/RPU-a3-RPEM/RPEM.md) |

---

## Distribution Summary

| Property | Value |
|----------|-------|
| Total alpha models | 27 |
| Models per unit | 3 (uniform across all 9 units) |
| Total output dimensions | 327D |
| Output range per model | 11D -- 19D |
| Median output per model | 12D |

### By Circuit

| Circuit | Alpha Models | Total Alpha Output |
|---------|-------------|-------------------|
| Mesolimbic | 6 (ARU: 3, RPU: 3) | 79D |
| Perceptual | 3 (SPU: 3) | 35D |
| Sensorimotor | 6 (STU: 3, MPU: 3) | 71D |
| Mnemonic | 6 (IMU: 3, PCU: 3) | 69D |
| Salience | 6 (ASU: 3, NDU: 3) | 69D |

---

## Evidence Standards

To qualify for alpha tier, a model's `ModelMetadata` must satisfy:

```python
@dataclass(frozen=True)
class ModelMetadata:
    evidence_tier: str = "alpha"          # Must be "alpha"
    confidence_range: Tuple[float, float]  # Both bounds > 0.90
    paper_count: int                       # >= 10
    falsification_criteria: Tuple[str, ...]  # At least one criterion
```

Alpha models are periodically audited against the literature. If replication failures reduce the effective paper count below 10 or confidence below 90%, a model is downgraded to beta tier.

---

## Cross-References

- **Beta Tier**: [Beta.md](Beta.md) -- integrative models (70--90% confidence)
- **Gamma Tier**: [Gamma.md](Gamma.md) -- theoretical models (<70% confidence)
- **Models Index**: [Models/00-INDEX.md](../Models/00-INDEX.md)
- **Circuits**: [Circuits/00-INDEX.md](../Circuits/00-INDEX.md)
