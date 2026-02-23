# F12 -- Cross-Modal Integration

**Function**: F12 Cross-Modal Integration
**Type**: META-LAYER -- evidence-only, NO beliefs, NO relay
**Models**: 5 total (all cross-unit: NDU 1, IMU 1, PCU 1, ASU 1, ARU 1) + 0 secondary
**Beliefs**: 0 (meta-layer -- evidence feeds INTO F1-F9 observe())
**Total output**: 51D (CMAT 10D + CMAPCC 10D + CHPI 11D + DGTP 9D + SDD 11D)
**H3 demands**: 76 tuples total (CMAT 9, CMAPCC 20, CHPI 20, DGTP 9, SDD 18)
**Phase**: meta (deferred -- evidence-only)
**Relay**: NONE -- F12 is a meta-layer with no dedicated relay
**Implemented**: no F12 mechanism models yet

---

## 1. What F12 Does

F12 processes the CROSS-MODAL INTEGRATION dimension of music cognition -- how auditory musical processing interacts with other sensory modalities (vision, movement, touch) and how information transfers across modal boundaries. It captures cross-modal affective transfer (music-to-visual emotion), action-perception common coding (auditory-motor mirroring), cross-modal harmonic prediction (multimodal tonal integration), domain-general temporal processing (shared timing across modalities), and supramodal deviance detection (amodal surprise signals).

F12 is a **META-LAYER** -- it has **NO beliefs** and **NO relay**. All 5 models produce evidence that feeds unidirectionally INTO F1-F9 observe() via cross-function signal routes. This architecture reflects that cross-modal integration is not a separate cognitive process but rather a contextual modulation of the same F1-F9 machinery: how emotion crosses modal boundaries (F5), how prediction integrates multimodal cues (F2), how attention operates across domains (F3), and how motor-perception coupling creates common codes (F7).

F12 has **NO dedicated unit**. Its 5 models are uniquely distributed one-per-unit across 5 different units: ARU (Affective Response Unit, 1 model), IMU (Integrative Memory Unit, 1 model), PCU (Predictive Coding Unit, 1 model), ASU (Auditory Salience Unit, 1 model), and NDU (Neural Dynamics Unit, 1 model). This maximal unit spread reflects that cross-modal integration permeates all processing streams rather than concentrating in any single anatomical hub.

### Cross-Modal Domains

1. **Affective Transfer**: CMAT (cross-modal affective transfer, music-to-visual)
2. **Action-Perception Coding**: CMAPCC (cross-modal action-perception common code)
3. **Multimodal Prediction**: CHPI (cross-modal harmonic predictive integration)
4. **Domain-General Timing**: DGTP (domain-general temporal processing)
5. **Supramodal Deviance**: SDD (supramodal deviance detection)

### Key Neuroscience Circuits

- **Cross-Modal Affect**: Amygdala + STS + insula -> emotion transfers from music to visual/tactile domains (Logeswaran & Bhatt 2012, Spence 2011)
- **Action-Perception Common Code**: Mirror neuron system + SMA + parietal -> shared representations for musical action observation and execution (Kohler 2002, Zatorre 2007)
- **Multimodal Harmonic Prediction**: STG + IPS + prefrontal -> tonal predictions integrate visual cues via multisensory convergence zones (Baart 2014, Lee & Noppeney 2011)
- **Domain-General Timing**: Basal ganglia + cerebellum + SMA -> shared temporal processing across auditory, visual, and motor domains (Grahn & Brett 2007, Merchant 2015)
- **Supramodal Deviance**: Frontal + temporal + parietal network -> amodal mismatch detection transcending specific sensory channels (Downar 2000, Escera 2014)

```
Audio -> R3 (97D) ---+--------------------------------------------
H3 tuples -----------+
                     |
                     v
 [Affective]         CMAT   (10D, ARU-g)    <- cross-modal affective transfer
 [Action-Perception] CMAPCC (10D, IMU-b)    <- action-perception common code
 [Prediction]        CHPI   (11D, PCU-b)    <- cross-modal harmonic prediction
 [Timing]            DGTP   (9D,  ASU-g)    <- domain-general temporal processing
 [Deviance]          SDD    (11D, NDU-a)    <- supramodal deviance detection
                     |
                     v
         Evidence -> F1-F9 observe() (unidirectional)
```

---

## 2. Complete Model Inventory

| # | Model | Unit | Tier | Output | H3 | Primary Fn | Status |
|---|-------|------|------|--------|-----|-----------|--------|
| 1 | **CMAT** | ARU | g | 10D | 9 | F12 | pending |
| 2 | **CMAPCC** | IMU | b | 10D | 20 | F12 | pending |
| 3 | **CHPI** | PCU | b | 11D | 20 | F12 | pending |
| 4 | **DGTP** | ASU | g | 9D | 9 | F12 | pending |
| 5 | **SDD** | NDU | a | 11D | 18 | F12 | pending |

3/5 models have mechanism layer docs in their primary function directories:
- **CMAT**: `F5-Emotion-and-Valence/mechanisms/cmat/`
- **DGTP**: `F3-Attention-and-Salience/mechanisms/dgtp/`
- **SDD**: mechanism docs co-located with NDU in F2 prediction pipeline (cross-ref)

2/5 models are F12-primary with docs in this directory:
- **CHPI**: `F12-Cross-Modal-Integration/mechanisms/chpi/` (NEW -- pending layer docs)
- **SDD**: `F12-Cross-Modal-Integration/mechanisms/sdd/` (NEW -- pending layer docs)

---

## 3. Meta-Layer Architecture -- NO Beliefs

F12 is fundamentally different from F1-F9. It has **0 beliefs**, **0 Core**, **0 Appraisal**, **0 Anticipation**. There is no Bayesian update cycle, no precision engine, no prediction error tracking.

Instead, F12 models produce **evidence signals** that feed INTO F1-F9 observe() unidirectionally:

```
F12 Models -> F1-F9 Evidence Routes:
CMAT   -> F5 Emotion                      (cross-modal affective context)
CMAPCC -> F7 Motor / F4 Memory            (action-perception common code)
CHPI   -> F2 Prediction                   (multimodal harmonic prediction)
DGTP   -> F3 Attention / F7 Motor         (domain-general timing evidence)
SDD    -> F2 Prediction / F3 Attention    (supramodal deviance signal)
```

This evidence-only architecture means:
- No tau values (no Core beliefs)
- No precision tracking (no PE history)
- No relay wrapper (no kernel integration)
- No phase in the scheduler (meta-layer)
- All computation is deferred to the receiving F1-F9 beliefs

---

## 4. Dependency Graph

```
                R3 (97D) + H3
                    |
    +---+---+---+---+---+
    v   v   v   v   v
  CMAT CMAPCC CHPI DGTP SDD
  10D  10D   11D  9D   11D
  ARU  IMU   PCU  ASU  NDU
    |   |     |    |    |
    v   v     v    v    v
   F5  F7    F2   F3   F2
       F4         F7   F3
        Evidence -> F1-F9 observe()
```

### Key Dependencies

| Model | Reads From |
|-------|-----------|
| CMAT (ARU-g) | R3/H3 + upstream SRP, CLAM, TAR outputs (ARU) |
| CMAPCC (IMU-b) | R3/H3 + upstream MEAMN memory outputs (IMU) + beat cross-circuit |
| CHPI (PCU-b) | R3/H3 + upstream HTP, SPH, ICEM outputs (PCU) |
| DGTP (ASU-g) | R3/H3 + upstream SNEM, IACM, BARM outputs (ASU) |
| SDD (NDU-a) | R3/H3 + intra NDU feeds to CDMR, EDNR, SLEE |

### Cross-Function Evidence Flow

F12 models feed evidence into F1-F9 unidirectionally:
- **F2 Prediction**: CHPI multimodal harmonic prediction, SDD supramodal deviance
- **F3 Attention**: DGTP domain-general timing, SDD supramodal deviance
- **F4 Memory**: CMAPCC action-perception common code (motor-memory bridge)
- **F5 Emotion**: CMAT cross-modal affective transfer
- **F7 Motor**: CMAPCC action-perception common code, DGTP cross-domain timing

---

## 5. Unit Architecture

### ARU -- Affective Response Unit (1 F12 model)

ARU contributes 1 model to F12: CMAT (cross-modal affective transfer, gamma). CMAT captures how music-evoked emotions transfer to other sensory domains -- music heard as "sad" biases subsequent visual face perception toward sadness. This provides F5 emotion beliefs with a cross-modal affective context signal.

```
ARU models in F12:  CMAT (g)
                    cross-modal
                    affective
                    transfer
```

### IMU -- Integrative Memory Unit (1 F12 model)

IMU contributes 1 model to F12: CMAPCC (cross-modal action-perception common code, beta). CMAPCC models the shared representational format between perceiving and producing music -- hearing a piano note activates motor representations of key-press. This reflects the common coding theory (Prinz 1997) applied to music.

```
IMU models in F12:  CMAPCC (b)
                    action-perception
                    common code
```

### PCU -- Predictive Coding Unit (1 F12 model)

PCU contributes 1 model to F12: CHPI (cross-modal harmonic predictive integration, beta). CHPI models how tonal predictions integrate cues from multiple modalities -- visual conductor gestures modulate harmonic expectation, visual scene changes interact with tonal resolution. CHPI has the highest H3 demand tied with CMAPCC (20 tuples each).

```
PCU models in F12:  CHPI (b)
                    cross-modal
                    harmonic
                    prediction
```

### ASU -- Auditory Salience Unit (1 F12 model)

ASU contributes 1 model to F12: DGTP (domain-general temporal processing, gamma). DGTP captures shared timing mechanisms that operate across auditory, visual, and motor domains -- rhythmic structure in music engages the same basal ganglia-cerebellar circuits as visual rhythm and motor timing.

```
ASU models in F12:  DGTP (g)
                    domain-general
                    temporal
                    processing
```

### NDU -- Neural Dynamics Unit (1 F12 model)

NDU contributes 1 model to F12: SDD (supramodal deviance detection, alpha). SDD is the highest-tier F12 model, capturing amodal surprise signals that transcend specific sensory channels. Unexpected events in any modality engage a shared frontal-temporal-parietal network -- SDD provides evidence of this supramodal deviance response to F2/F3.

```
NDU models in F12:  SDD (a)
                    supramodal
                    deviance
                    detection
```

---

## 6. Documentation Structure

```
F12-Cross-Modal-Integration/
+-- 0_F12-orchestrator.md                  <- this file
+-- collections.md                         <- full model inventory
+-- mechanisms/
    +-- 0_mechanisms-orchestrator.md       <- cross-references + CHPI/SDD summary
    +-- chpi/                             <- CHPI mechanism layer docs (NEW, pending)
    +-- sdd/                              <- SDD mechanism layer docs (NEW, pending)
```

**NOTE**: F12 has NO beliefs directory -- meta-layers have 0 beliefs.
3/5 models have their mechanism docs in their primary unit function directories:
- CMAT: `F5-Emotion-and-Valence/mechanisms/cmat/`
- CMAPCC: `F4-Memory-Systems/mechanisms/cmapcc/`
- DGTP: `F3-Attention-and-Salience/mechanisms/dgtp/`

2/5 models have mechanism docs in this directory:
- CHPI: `F12-Cross-Modal-Integration/mechanisms/chpi/`
- SDD: `F12-Cross-Modal-Integration/mechanisms/sdd/`

**0 models implemented.** Pending: 1 a (SDD) + 2 b (CMAPCC, CHPI) + 2 g (CMAT, DGTP) -- 76 H3 tuples total.
