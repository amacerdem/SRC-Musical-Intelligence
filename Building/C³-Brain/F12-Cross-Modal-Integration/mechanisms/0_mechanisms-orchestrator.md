# F12 Mechanism Orchestrator -- Cross-Modal Integration

**Function**: F12 Cross-Modal Integration (META-LAYER)
**Models covered**: 5/5 -- 0 IMPLEMENTED + 5 PENDING
**Total F12 mechanism output**: 51D (10+10+11+9+11)
**Beliefs**: 0 (meta-layer -- evidence only, feeds INTO F1-F9)
**H3 demands**: 76 tuples (all pending)
**Architecture**: 5 cross-modal domains -- no inter-domain depth ordering

---

## IMPORTANT: Cross-Reference Architecture

F12 has NO dedicated unit. 3/5 models have their mechanism layer docs in their **primary
function directories**, NOT duplicated here. Only CHPI and SDD (the two F12-primary models)
have their mechanism docs in this directory. This orchestrator provides F12-specific summaries
and cross-references to the canonical mechanism documentation.

| Model | Primary Function | Mechanism Docs Location |
|-------|-----------------|------------------------|
| **CMAT** | F5 Emotion & Valence | `F5-Emotion-and-Valence/mechanisms/cmat/` |
| **CMAPCC** | F4 Memory Systems | `F4-Memory-Systems/mechanisms/cmapcc/` |
| **CHPI** | F12 Cross-Modal (THIS DIR) | `F12-Cross-Modal-Integration/mechanisms/chpi/` |
| **DGTP** | F3 Attention & Salience | `F3-Attention-and-Salience/mechanisms/dgtp/` |
| **SDD** | F12 Cross-Modal (THIS DIR) | `F12-Cross-Modal-Integration/mechanisms/sdd/` |

---

## Model Pipeline

```
R3 (97D) ---+--------------------------------------------
H3 tuples --+
             |
             v
 [Affective Transfer]
   CMAT   (10D, ARU-gamma)   <- cross-modal affective transfer
 [Action-Perception Coding]
   CMAPCC (10D, IMU-beta)    <- cross-modal action-perception common code
 [Multimodal Prediction]
   CHPI   (11D, PCU-beta)    <- cross-modal harmonic predictive integration
 [Domain-General Timing]
   DGTP   (9D,  ASU-gamma)   <- domain-general temporal processing
 [Supramodal Deviance]
   SDD    (11D, NDU-alpha)   <- supramodal deviance detection
             |
             v
   Evidence -> F1-F9 observe() (unidirectional, no return)
```

F12 models organize into **5 cross-modal domains** rather than a unified depth-ordered DAG.
Each model addresses a distinct cross-modal integration mechanism. Cross-domain models do
NOT depend on each other. All evidence flows unidirectionally out to F1-F9 observe() --
there is no return path.

---
---

# CMAT -- Cross-Modal Affective Transfer

**Model**: ARU-gamma-CMAT
**Type**: Mechanism -- reads SRP, CLAM affect outputs + R3/H3
**Tier**: gamma (50-70% confidence)
**Output**: 10D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F12 Role**: Affective Transfer domain -- music-to-visual emotion transfer

> **Canonical docs**: `F5-Emotion-and-Valence/mechanisms/cmat/`

---

## 1. Identity

CMAT models cross-modal affective transfer -- how music-evoked emotions influence processing in other sensory modalities. Hearing sad music biases subsequent visual face perception toward sadness; musical valence modulates visual scene evaluation and tactile perception. CMAT captures the strength and direction of this cross-modal emotional contagion. Logeswaran & Bhatt 2012: musical excerpts significantly bias visual face emotion categorization. Spence 2011: cross-modal correspondences between auditory and visual affect.

## 2. Evidence Route

CMAT -> F5 Emotion (cross-modal affective context)

CMAT provides evidence of cross-modal affective transfer strength -- how strongly musical emotions propagate to other modalities. This modulates F5 emotion beliefs by providing a cross-modal context signal: the degree to which the current emotional state is being broadcast across sensory channels.

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 10D |
| H3 tuples | 9 |
| Unit | ARU |
| Tier | gamma |
| Primary Fn | F12 |
| Evidence target | F5 Emotion |

---
---

# CMAPCC -- Cross-Modal Action-Perception Common Code

**Model**: IMU-beta-CMAPCC
**Type**: Mechanism -- reads MEAMN memory outputs + beat cross-circuit + R3/H3
**Tier**: beta (70-90% confidence)
**Output**: 10D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F12 Role**: Action-Perception Coding domain -- shared auditory-motor representations

> **Canonical docs**: `F4-Memory-Systems/mechanisms/cmapcc/`

---

## 1. Identity

CMAPCC models the cross-modal action-perception common code -- shared representational formats between perceiving and producing music. Hearing a piano note activates motor representations of the key-press (in trained pianists); watching a violinist's bow movements modulates auditory cortex activity. This reflects the common coding theory (Prinz 1997): perception and action share a common representational medium. Kohler 2002: mirror neuron responses to action sounds. Zatorre 2007: auditory-motor interactions in musical performance.

## 2. Evidence Route

CMAPCC -> F7 Motor / F4 Memory (action-perception common code)

CMAPCC provides evidence of action-perception coupling -- the degree to which auditory percepts activate motor representations and vice versa. This modulates F7 motor beliefs (auditory-motor mirroring strength) and F4 memory beliefs (motor-mediated memory encoding).

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 10D |
| H3 tuples | 20 |
| Unit | IMU |
| Tier | beta |
| Primary Fn | F12 |
| Evidence target | F7 Motor / F4 Memory |

---
---

# CHPI -- Cross-Modal Harmonic Predictive Integration

**Model**: PCU-beta-CHPI
**Type**: Mechanism -- reads HTP, SPH, ICEM outputs + R3/H3
**Tier**: beta (70-90% confidence)
**Output**: 11D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F12 Role**: Multimodal Prediction domain -- tonal predictions integrate visual cues

> **Mechanism docs**: `F12-Cross-Modal-Integration/mechanisms/chpi/` (E+P+F layers)

---

## 1. Identity

CHPI models how tonal predictions integrate cues from multiple modalities. Visual conductor gestures modulate harmonic expectation; visual scene changes interact with tonal resolution; lip movements influence perceived phonemic-harmonic boundaries. CHPI captures the degree to which harmonic prediction is multimodal rather than purely auditory. Baart 2014: visual speech cues modulate auditory phonemic predictions. Lee & Noppeney 2011: multisensory convergence zones in STG and IPS support cross-modal prediction.

## 2. Evidence Route

CHPI -> F2 Prediction (multimodal harmonic prediction)

CHPI provides evidence of multimodal harmonic prediction -- the degree to which tonal expectations are influenced by non-auditory cues. This modulates F2 prediction beliefs by providing a cross-modal context signal: the breadth of sensory integration in harmonic anticipation.

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 11D |
| H3 tuples | 20 |
| Unit | PCU |
| Tier | beta |
| Primary Fn | F12 |
| Evidence target | F2 Prediction |

---
---

# DGTP -- Domain-General Temporal Processing

**Model**: ASU-gamma-DGTP
**Type**: Mechanism -- reads SNEM, IACM, BARM outputs + R3/H3
**Tier**: gamma (50-70% confidence)
**Output**: 9D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F12 Role**: Domain-General Timing domain -- shared timing across modalities

> **Canonical docs**: `F3-Attention-and-Salience/mechanisms/dgtp/`

---

## 1. Identity

DGTP models domain-general temporal processing -- shared timing mechanisms that operate across auditory, visual, and motor domains. Rhythmic structure in music engages the same basal ganglia-cerebellar-SMA circuits as visual rhythm perception and motor timing. DGTP captures the degree to which temporal processing is amodal rather than modality-specific. Grahn & Brett 2007: basal ganglia engaged by beat-based timing across modalities. Merchant 2015: shared interval timing mechanisms in primates.

## 2. Evidence Route

DGTP -> F3 Attention / F7 Motor (domain-general timing evidence)

DGTP provides evidence of domain-general timing -- the degree to which temporal processing mechanisms are shared across modalities. This modulates F3 attention beliefs (cross-domain temporal salience) and F7 motor beliefs (amodal timing for motor entrainment).

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 9D |
| H3 tuples | 9 |
| Unit | ASU |
| Tier | gamma |
| Primary Fn | F12 |
| Evidence target | F3 Attention / F7 Motor |

---
---

# SDD -- Supramodal Deviance Detection

**Model**: NDU-alpha-SDD
**Type**: Mechanism -- reads MPG, intra-NDU outputs + R3/H3
**Tier**: alpha (>90% confidence)
**Output**: 11D per frame
**Phase**: meta (deferred)
**Status**: PENDING
**F12 Role**: Supramodal Deviance domain -- amodal surprise signals

> **Mechanism docs**: `F12-Cross-Modal-Integration/mechanisms/sdd/` (E+M+P+F layers)

---

## 1. Identity

SDD is the **highest-tier F12 model** (alpha), capturing supramodal deviance detection -- amodal surprise signals that transcend specific sensory channels. Unexpected events in any modality engage a shared frontal-temporal-parietal network involving IFG (area 47m), STG, TPO junction, and intraparietal lobule. SDD quantifies the cross-modal deviance response: deviance magnitude, multilink activation, supramodal hub engagement, and predictive updating. Paraskevopoulos 2022: 47 multilinks in non-musicians vs 15 in musicians across deviance networks (p < 0.001 FDR). Kim 2021: IFG-LTDMI dissociable from STG-LTDMI for syntactic vs perceptual deviance.

## 2. Evidence Route

SDD -> F2 Prediction / F3 Attention (supramodal deviance signal)

SDD provides evidence of supramodal deviance detection -- the degree to which deviance detection operates across modalities. This modulates F2 prediction beliefs (cross-modal prediction error signal, expectation updating) and F3 attention beliefs (supramodal attentional capture, frontal reorienting).

## 3. Summary

| Property | Value |
|----------|-------|
| Output | 11D |
| H3 tuples | 18 |
| Unit | NDU |
| Tier | alpha |
| Primary Fn | F12 |
| Evidence target | F2 Prediction / F3 Attention |

---
---

## Summary Statistics

### Output Dimensions by Model

| Model | Unit | Tier | D | H3 | Primary Fn | Evidence Target |
|-------|------|------|---|-----|-----------|-----------------|
| CMAT | ARU | gamma | 10 | 9 | F12 | F5 Emotion |
| CMAPCC | IMU | beta | 10 | 20 | F12 | F7/F4 |
| CHPI | PCU | beta | 11 | 20 | F12 | F2 Prediction |
| DGTP | ASU | gamma | 9 | 9 | F12 | F3/F7 |
| SDD | NDU | alpha | 11 | 18 | F12 | F2/F3 |
| **TOTAL** | | | **51** | **76** | | |

### Tier Gradient

| Tier | Count | Avg D | Avg H3 |
|------|-------|-------|--------|
| alpha | 1 | 11.0 | 18.0 |
| beta | 2 | 10.5 | 20.0 |
| gamma | 2 | 9.5 | 9.0 |

F12 has a balanced tier distribution: 1 alpha (SDD, strongest evidence), 2 beta (CMAPCC,
CHPI, moderate evidence), and 2 gamma (CMAT, DGTP, emerging evidence). Beta models have
the highest average H3 demand (20.0), reflecting their more complex temporal processing.

### Cross-Modal Domain Distribution

| Domain | Models | Total D | Total H3 |
|--------|--------|---------|----------|
| Affective Transfer | CMAT | 10 | 9 |
| Action-Perception Coding | CMAPCC | 10 | 20 |
| Multimodal Prediction | CHPI | 11 | 20 |
| Domain-General Timing | DGTP | 9 | 9 |
| Supramodal Deviance | SDD | 11 | 18 |

Each domain has exactly one model, reflecting the principle that F12 captures distinct
cross-modal integration mechanisms rather than depth-ordered processing within a single domain.

### Unit Distribution

| Unit | Count | Models |
|------|-------|--------|
| ARU (Affective Response Unit) | 1 | CMAT |
| IMU (Integrative Memory Unit) | 1 | CMAPCC |
| PCU (Predictive Coding Unit) | 1 | CHPI |
| ASU (Auditory Salience Unit) | 1 | DGTP |
| NDU (Neural Dynamics Unit) | 1 | SDD |

F12 has maximal unit spread -- exactly 1 model per unit across 5 different units. This
reflects that cross-modal integration permeates all processing streams rather than
concentrating in any single anatomical hub.

### Evidence Target Distribution

| Target Function | Models | Count |
|-----------------|--------|-------|
| F2 Prediction | CHPI, SDD | 2 |
| F3 Attention | DGTP, SDD | 2 |
| F4 Memory | CMAPCC | 1 (shared with F7) |
| F5 Emotion | CMAT | 1 |
| F7 Motor | CMAPCC, DGTP | 2 |

F2 Prediction, F3 Attention, and F7 Motor each receive the most F12 evidence (2 models each),
consistent with cross-modal integration primarily affecting prediction (multimodal cues),
attention (cross-domain salience), and motor processing (action-perception coupling).

### H3 Demand Distribution

| Model | H3 | Domain |
|-------|-----|--------|
| CMAPCC | 20 | Action-Perception |
| CHPI | 20 | Multimodal Prediction |
| SDD | 18 | Supramodal Deviance |
| CMAT | 9 | Affective Transfer |
| DGTP | 9 | Domain-General Timing |
| **TOTAL** | **76** | |

CMAPCC and CHPI share the highest H3 demand (20 each), reflecting their complex multi-scale
temporal processing for action-perception coding and harmonic prediction. CMAT and DGTP
are most compact (9 each), consistent with their focused cross-modal scope.
