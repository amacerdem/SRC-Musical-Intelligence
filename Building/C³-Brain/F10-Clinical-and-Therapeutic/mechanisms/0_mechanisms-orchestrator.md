# F10 Mechanism Orchestrator -- Clinical & Therapeutic

**Function**: F10 Clinical & Therapeutic (META-LAYER)
**Models covered**: 10/10 -- 0 IMPLEMENTED + 10 PENDING
**Total F10 mechanism output**: 119D (12+11+10+10+11+11+11+11+10+12)
**Beliefs**: 0 (meta-layer -- evidence only, feeds INTO F1-F9)
**H3 demands**: 167 tuples (all pending)
**Architecture**: 3 clinical domains -- no inter-domain depth ordering

---

## IMPORTANT: Cross-Reference Architecture

F10 has NO dedicated unit. 9/10 models have their mechanism layer docs in their **primary
function directories**, NOT duplicated here. Only DSP (the sole F10-primary model) has its
mechanism docs in this directory. This orchestrator provides F10-specific summaries and
cross-references to the canonical mechanism documentation.

| Model | Primary Function | Mechanism Docs Location |
|-------|-----------------|------------------------|
| **MMP** | F4 Memory Systems | `F4-Memory-Systems/mechanisms/mmp/` |
| **RASN** | F4 Memory Systems | `F4-Memory-Systems/mechanisms/rasn/` |
| **RIRI** | F4 Memory Systems | `F4-Memory-Systems/mechanisms/riri/` |
| **VRIAP** | F4 Memory Systems | `F4-Memory-Systems/mechanisms/vriap/` |
| **GSSM** | F7 Motor & Timing | `F7-Motor-and-Timing/mechanisms/gssm/` |
| **VRMSME** | F7 Motor & Timing | `F7-Motor-and-Timing/mechanisms/vrmsme/` |
| **CLAM** | F5 Emotion & Valence | `F5-Emotion-and-Valence/mechanisms/clam/` |
| **MAD** | F5 Emotion & Valence | `F5-Emotion-and-Valence/mechanisms/mad/` |
| **TAR** | F5 Emotion & Valence | `F5-Emotion-and-Valence/mechanisms/tar/` |
| **DSP** | F10 Clinical (THIS DIR) | `F10-Clinical-and-Therapeutic/mechanisms/dsp/` (NEW -- pending layer docs) |

---

## Model Pipeline

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
             |
             v
 [Neurodegeneration]
   MMP    (12D, IMU-alpha)   <- music memory preservation
 [Motor Rehabilitation]
   RASN   (11D, IMU-beta)    <- rhythmic auditory stimulation neuroplasticity
   RIRI   (10D, IMU-beta)    <- rhythm-induced rehabilitation integration
   GSSM   (11D, MPU-alpha)   <- gait-sound synchronization model
   VRMSME (11D, MPU-beta)    <- VR-music sensorimotor enhancement
 [Pain & Affect]
   VRIAP  (10D, IMU-beta)    <- VR-integrated analgesic processing
   CLAM   (11D, ARU-beta)    <- closed-loop affect modulation
   MAD    (11D, ARU-beta)    <- musical anhedonia dissociation
   TAR    (10D, ARU-gamma)   <- therapeutic auditory resonance
   DSP    (12D, NDU-beta)    <- deviance salience processing
             |
             v
   Evidence -> F1-F9 observe() (unidirectional, no return)
```

F10 models organize into **3 clinical domains** rather than a unified depth-ordered DAG.
Within each domain, within-unit tier ordering applies (alpha -> beta -> gamma).
Cross-domain models do NOT depend on each other. All evidence flows unidirectionally
out to F1-F9 observe() -- there is no return path.

---
---

# MMP -- Music Memory Preservation

**Model**: IMU-alpha-MMP
**Type**: Mechanism -- reads MEAMN memory outputs + R3/H3
**Tier**: alpha (>90% confidence)
**Output**: 12D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F10 Role**: Neurodegeneration domain -- Alzheimer's music memory preservation

> **Canonical docs**: `F4-Memory-Systems/mechanisms/mmp/`

---

## 1. Identity

MMP models the preserved musical memory pathway in Alzheimer's disease and related dementias. Musical memories are uniquely spared because they rely on SMA and cerebellum rather than hippocampal circuits degraded by neurodegeneration. Jacobsen 2015: PET/MRI shows musical memory regions have minimal amyloid/tau deposition. Baird 2018: music recognition preserved in moderate-severe AD (d=1.2 vs verbal).

## 2. Evidence Route

MMP -> F4.autobiographical_retrieval (preservation context)

MMP provides evidence of memory preservation capacity -- how much the hippocampal bypass pathway is engaged, how strong procedural music memory signals are. This modulates F4's autobiographical retrieval belief by providing a clinical context signal: in healthy listeners the preservation signal is near-maximal; in simulated neurodegenerative states it varies with the degree of sparing.

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 12D |
| H3 tuples | 21 |
| Unit | IMU |
| Tier | alpha |
| Primary Fn | F4 |
| Evidence target | F4.autobiographical_retrieval |

---
---

# RASN -- Rhythmic Auditory Stimulation Neuroplasticity

**Model**: IMU-beta-RASN
**Type**: Mechanism -- reads MMP, MEAMN outputs + R3/H3
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F10 Role**: Motor Rehabilitation domain -- RAS-driven gait entrainment plasticity

> **Canonical docs**: `F4-Memory-Systems/mechanisms/rasn/`

---

## 1. Identity

RASN models the neuroplastic changes driven by rhythmic auditory stimulation (RAS) in stroke and Parkinson's rehabilitation. Tempo-locked auditory cues entrain basal ganglia-cerebellar-premotor circuits, improving gait cadence, stride length, and symmetry. Thaut 2015: meta-analysis shows RAS improves gait velocity by 0.17 m/s (d=0.85) in stroke. Dalla Bella 2017: mobile RAS reduces step variability in PD.

## 2. Evidence Route

RASN -> F7.period_entrainment (RAS plasticity)

RASN provides evidence of rhythmic stimulation neuroplasticity -- how strongly the auditory-motor coupling pathway responds to rhythmic structure. This modulates F7's period entrainment belief by adding a clinical plasticity context: the degree to which entrainment reflects therapeutic adaptation vs baseline coupling.

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 11D |
| H3 tuples | 28 |
| Unit | IMU |
| Tier | beta |
| Primary Fn | F4 |
| Evidence target | F7.period_entrainment |

---
---

# RIRI -- Rhythm-Induced Rehabilitation Integration

**Model**: IMU-beta-RIRI
**Type**: Mechanism -- reads MMP, MEAMN outputs + R3/H3
**Tier**: beta (70-90% confidence)
**Output**: 10D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F10 Role**: Motor Rehabilitation domain -- multi-modal rhythmic rehabilitation synergy

> **Canonical docs**: `F4-Memory-Systems/mechanisms/riri/`

---

## 1. Identity

RIRI models the synergistic integration of rhythmic cues across multiple motor rehabilitation modalities. While RASN focuses on gait, RIRI captures how rhythm-induced entrainment generalizes across upper limb, speech, and whole-body coordination. Multi-modal rhythmic integration produces greater rehabilitation gains than single-modality approaches.

## 2. Evidence Route

RIRI -> F7 Motor (multi-modal synergy)

RIRI provides evidence of cross-modality motor synergy -- how rhythmic structure simultaneously entrains multiple motor systems. This feeds F7 motor beliefs with a clinical integration signal indicating the breadth of rhythmic engagement.

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 10D |
| H3 tuples | 16 |
| Unit | IMU |
| Tier | beta |
| Primary Fn | F4 |
| Evidence target | F7 Motor |

---
---

# VRIAP -- VR-Integrated Analgesic Processing

**Model**: IMU-beta-VRIAP
**Type**: Mechanism -- reads MMP, MEAMN outputs + R3/H3
**Tier**: beta (70-90% confidence)
**Output**: 10D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F10 Role**: Pain & Affect domain -- VR + music analgesia via descending pain modulation

> **Canonical docs**: `F4-Memory-Systems/mechanisms/vriap/`

---

## 1. Identity

VRIAP models the analgesic processing pathway activated by combined VR and music stimulation. Music-induced analgesia operates through descending pain modulation (PAG -> rostral ventromedial medulla) and attentional diversion (prefrontal -> ACC). VR adds immersive distraction. Roy 2008: music reduces pain ratings by 1.2 points (VAS). Garza-Villarreal 2014: music analgesia engages PAG + insula.

## 2. Evidence Route

VRIAP -> F5 Emotion (pain modulation valence)

VRIAP provides evidence of music-driven pain modulation -- the degree to which affective processing shifts from nociceptive to hedonic valence. This feeds F5 emotion beliefs with a clinical analgesia context signal.

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 10D |
| H3 tuples | 18 |
| Unit | IMU |
| Tier | beta |
| Primary Fn | F4 |
| Evidence target | F5 Emotion |

---
---

# GSSM -- Gait-Sound Synchronization Model

**Model**: MPU-alpha-GSSM
**Type**: Mechanism -- reads PEOM motor outputs + R3/H3
**Tier**: alpha (>90% confidence)
**Output**: 11D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F10 Role**: Motor Rehabilitation domain -- tempo-locked gait entrainment

> **Canonical docs**: `F7-Motor-and-Timing/mechanisms/gssm/`

---

## 1. Identity

GSSM models the synchronization between musical tempo and gait parameters. Tempo-locked auditory cues entrain step timing via the basal ganglia-cerebellar-premotor loop. GSSM captures the degree of gait-sound coupling, step variability, and cadence stability. Dalla Bella 2017: mobile cueing reduces step variability by 30% in PD. Leman 2013: spontaneous gait-music synchronization at preferred tempo.

## 2. Evidence Route

GSSM -> F7.period_entrainment (gait variability)

GSSM provides evidence of gait-sound coupling strength -- how precisely footfall timing locks to musical beat. This modulates F7's period entrainment belief with a clinical gait context: step regularity and temporal precision in motor rehabilitation.

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 11D |
| H3 tuples | 12 |
| Unit | MPU |
| Tier | alpha |
| Primary Fn | F7 |
| Evidence target | F7.period_entrainment |

---
---

# VRMSME -- VR-Music Sensorimotor Enhancement

**Model**: MPU-beta-VRMSME
**Type**: Mechanism -- reads GSSM, PEOM outputs + R3/H3
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F10 Role**: Motor Rehabilitation domain -- VR-music combined motor enhancement

> **Canonical docs**: `F7-Motor-and-Timing/mechanisms/vrmsme/`

---

## 1. Identity

VRMSME models the enhanced sensorimotor rehabilitation gains when VR and music stimulation are combined. The visual-auditory-motor integration in VR-music rehabilitation produces greater plasticity than either modality alone, likely through enhanced attentional engagement and multi-sensory prediction error amplification.

## 2. Evidence Route

VRMSME -> F7 Motor (VR-music enhancement)

VRMSME provides evidence of VR-music synergistic motor enhancement -- the degree to which combined stimulation exceeds single-modality motor gains. This feeds F7 motor beliefs with a clinical VR-enhancement context signal.

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 11D |
| H3 tuples | 12 |
| Unit | MPU |
| Tier | beta |
| Primary Fn | F7 |
| Evidence target | F7 Motor |

---
---

# CLAM -- Closed-Loop Affect Modulation

**Model**: ARU-beta-CLAM
**Type**: Mechanism -- reads SRP affect outputs + R3/H3
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F10 Role**: Pain & Affect domain -- EEG-music BCI for real-time affect regulation

> **Canonical docs**: `F5-Emotion-and-Valence/mechanisms/clam/`

---

## 1. Identity

CLAM models the closed-loop brain-computer interface pathway for affect modulation through music. EEG-derived affective state estimates drive real-time music parameter adaptation (tempo, mode, timbre) to steer emotional trajectory. Daly 2016: BCI-music reduces anxiety by 0.8 SD in clinical populations. Ramirez 2015: EEG-music neurofeedback improves emotional regulation in depression.

## 2. Evidence Route

CLAM -> F5 Emotion (closed-loop affect)

CLAM provides evidence of closed-loop affect regulation capability -- how strongly the music-brain feedback loop modulates emotional state. This feeds F5 emotion beliefs with a clinical BCI context signal indicating the degree of affect controllability.

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 11D |
| H3 tuples | 12 |
| Unit | ARU |
| Tier | beta |
| Primary Fn | F5 |
| Evidence target | F5 Emotion |

---
---

# MAD -- Musical Anhedonia Dissociation

**Model**: ARU-beta-MAD
**Type**: Mechanism -- reads SRP, DAED reward outputs + R3/H3
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F10 Role**: Pain & Affect domain -- reward circuit lesion patterns in musical anhedonia

> **Canonical docs**: `F5-Emotion-and-Valence/mechanisms/mad/`

---

## 1. Identity

MAD models the dissociation between general hedonic capacity and music-specific anhedonia. Specific musical anhedonia reflects selective disconnection of NAcc-auditory cortex white matter tracts while general reward processing remains intact. Mas-Herrero 2014: Barcelona Music Reward Questionnaire (BMRQ) identifies 3-5% prevalence. Martinez-Molina 2016: reduced NAcc-STG structural connectivity in musical anhedonia.

## 2. Evidence Route

MAD -> F6 Reward (anhedonia lesion)

MAD provides evidence of reward circuit integrity for music -- the degree to which the NAcc-auditory cortex pathway is functionally connected. This feeds F6 reward beliefs with a clinical anhedonia context: in intact listeners the signal is maximal; in musical anhedonia it attenuates music-specific reward.

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 11D |
| H3 tuples | 9 |
| Unit | ARU |
| Tier | beta |
| Primary Fn | F5 |
| Evidence target | F6 Reward |

---
---

# TAR -- Therapeutic Auditory Resonance

**Model**: ARU-gamma-TAR
**Type**: Mechanism -- reads CLAM, MAD, SRP outputs + R3/H3
**Tier**: gamma (50-70% confidence)
**Output**: 10D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F10 Role**: Pain & Affect domain -- therapeutic resonance across emotion and reward

> **Canonical docs**: `F5-Emotion-and-Valence/mechanisms/tar/`

---

## 1. Identity

TAR models the therapeutic resonance phenomenon -- the point at which musical stimulation achieves maximal therapeutic impact through convergent activation of emotion and reward pathways. TAR is the highest-tier (gamma) ARU model in F10, reading from both CLAM (affect modulation) and MAD (reward integrity) to estimate overall therapeutic potential.

## 2. Evidence Route

TAR -> F5/F6 (therapeutic resonance)

TAR provides evidence of therapeutic resonance capacity -- the combined emotion-reward optimization state. This feeds both F5 emotion and F6 reward beliefs with a clinical therapeutic context indicating the degree to which music achieves therapeutic resonance.

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 10D |
| H3 tuples | 21 |
| Unit | ARU |
| Tier | gamma |
| Primary Fn | F5 |
| Evidence target | F5/F6 |

---
---

# DSP -- Deviance Salience Processing

**Model**: NDU-beta-DSP
**Type**: Mechanism -- reads MPG outputs + R3/H3
**Tier**: beta (70-90% confidence)
**Output**: 12D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F10 Role**: Pain & Affect domain -- deviance detection in clinical contexts (F10-PRIMARY)

> **Mechanism docs**: `F10-Clinical-and-Therapeutic/mechanisms/dsp/` (NEW -- pending layer docs)

---

## 1. Identity

DSP is the **only F10-primary model** -- the only model whose mechanism docs reside in this directory rather than in F4/F5/F7. DSP models deviance salience processing in clinical populations: how unexpected auditory events capture attention differently in altered neural states (e.g., disorders of consciousness, coma, minimally conscious state). MMN (mismatch negativity) amplitude and latency serve as clinical biomarkers for consciousness level and recovery prognosis.

## 2. Evidence Route

DSP -> F3 Attention (deviance in clinical context)

DSP provides evidence of clinical deviance processing -- the degree to which the auditory system detects and responds to unexpected events under altered consciousness. This feeds F3 attention beliefs with a clinical context signal: deviance detection capacity as a function of neural integrity.

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 12D |
| H3 tuples | 18 |
| Unit | NDU |
| Tier | beta |
| Primary Fn | F10 |
| Evidence target | F3 Attention |

## 4. Pending

DSP layer docs (e_layer.md, m_layer.md, p_layer.md, f_layer.md) are NOT YET CREATED.
They will be authored in `F10-Clinical-and-Therapeutic/mechanisms/dsp/` when DSP
mechanism design is finalized.

---
---

## Summary Statistics

### Output Dimensions by Model

| Model | Unit | Tier | D | H3 | Primary Fn | Evidence Target |
|-------|------|------|---|-----|-----------|-----------------|
| MMP | IMU | alpha | 12 | 21 | F4 | F4 Memory |
| RASN | IMU | beta | 11 | 28 | F4 | F7 Motor |
| RIRI | IMU | beta | 10 | 16 | F4 | F7 Motor |
| VRIAP | IMU | beta | 10 | 18 | F4 | F5 Emotion |
| GSSM | MPU | alpha | 11 | 12 | F7 | F7 Motor |
| VRMSME | MPU | beta | 11 | 12 | F7 | F7 Motor |
| CLAM | ARU | beta | 11 | 12 | F5 | F5 Emotion |
| MAD | ARU | beta | 11 | 9 | F5 | F6 Reward |
| TAR | ARU | gamma | 10 | 21 | F5 | F5/F6 |
| DSP | NDU | beta | 12 | 18 | F10 | F3 Attention |
| **TOTAL** | | | **119** | **167** | | |

### Tier Gradient

| Tier | Count | Avg D | Avg H3 |
|------|-------|-------|--------|
| alpha | 2 | 11.5 | 16.5 |
| beta | 7 | 10.9 | 16.1 |
| gamma | 1 | 10.0 | 21.0 |

F10 is dominated by beta-tier models (7/10), reflecting the moderate confidence level
of clinical music neuroscience evidence. Two alpha models (MMP, GSSM) have the strongest
evidence bases. TAR is the sole gamma model.

### Clinical Domain Distribution

| Domain | Models | Total D | Total H3 |
|--------|--------|---------|----------|
| Neurodegeneration | MMP | 12 | 21 |
| Motor Rehabilitation | RASN, RIRI, GSSM, VRMSME | 43 | 68 |
| Pain & Affect | VRIAP, CLAM, MAD, TAR, DSP | 64 | 78 |

Motor Rehabilitation and Pain & Affect dominate (9/10 models combined), reflecting the
breadth of music therapy evidence in these domains. Neurodegeneration has only 1 model
(MMP) but with the strongest evidence base (alpha tier, Jacobsen 2015).

### Unit Distribution

| Unit | Count | Models |
|------|-------|--------|
| IMU (Integrative Memory Unit) | 4 | MMP, RASN, RIRI, VRIAP |
| MPU (Motor Processing Unit) | 2 | GSSM, VRMSME |
| ARU (Affective Response Unit) | 3 | CLAM, MAD, TAR |
| NDU (Neural Dynamics Unit) | 1 | DSP |

### Evidence Target Distribution

| Target Function | Models | Count |
|-----------------|--------|-------|
| F3 Attention | DSP | 1 |
| F4 Memory | MMP | 1 |
| F5 Emotion | VRIAP, CLAM, TAR | 3 |
| F5/F6 | TAR | (shared) |
| F6 Reward | MAD, TAR | 2 |
| F7 Motor | RASN, RIRI, GSSM, VRMSME | 4 |

F7 Motor receives the most F10 evidence (4 models), consistent with motor rehabilitation
being the most evidence-rich domain in clinical music neuroscience. F5 Emotion follows (3 models),
then F6 Reward (2), F4 Memory (1), and F3 Attention (1).

### H3 Demand Distribution

| Model | H3 | Domain |
|-------|-----|--------|
| RASN | 28 | Motor Rehab |
| MMP | 21 | Neurodegeneration |
| TAR | 21 | Pain & Affect |
| DSP | 18 | Pain & Affect |
| VRIAP | 18 | Pain & Affect |
| RIRI | 16 | Motor Rehab |
| GSSM | 12 | Motor Rehab |
| VRMSME | 12 | Motor Rehab |
| CLAM | 12 | Pain & Affect |
| MAD | 9 | Pain & Affect |
| **TOTAL** | **167** | |

RASN has the highest H3 demand (28), driven by multi-scale temporal tracking for RAS
neuroplasticity. MAD is most compact (9), consistent with its focused reward-lesion architecture.
