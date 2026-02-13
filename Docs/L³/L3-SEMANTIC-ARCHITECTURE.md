# L3 Semantic Architecture -- Definitive Design Document

**Version**: 2.1.0
**Updated**: 2026-02-13
**Status**: Canonical specification for L3 semantic interpretation layer
**Companion**: [H3-TEMPORAL-ARCHITECTURE.md](../H3/H3-TEMPORAL-ARCHITECTURE.md), [R3-SPECTRAL-ARCHITECTURE.md](../R3/R3-SPECTRAL-ARCHITECTURE.md)

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Pipeline Position](#2-pipeline-position)
3. [The 8 Semantic Groups](#3-the-8-semantic-groups)
4. [Group 1: Alpha -- Computation (6D)](#4-group-1-alpha----computation-6d)
5. [Group 2: Beta -- Neuroscience (14D)](#5-group-2-beta----neuroscience-14d)
6. [Group 3: Gamma -- Psychology (13D)](#6-group-3-gamma----psychology-13d)
7. [Group 4: Delta -- Validation (12D)](#7-group-4-delta----validation-12d)
8. [Group 5: Epsilon -- Learning (19D, STATEFUL)](#8-group-5-epsilon----learning-19d-stateful)
9. [Group 6: Zeta -- Polarity (12D)](#9-group-6-zeta----polarity-12d)
10. [Group 7: Eta -- Vocabulary (12D)](#10-group-7-eta----vocabulary-12d)
11. [Group 8: Theta -- Narrative (16D)](#11-group-8-theta----narrative-16d)
12. [Computation Phases and Dependency Graph](#12-computation-phases-and-dependency-graph)
13. [Unique Characteristics](#13-unique-characteristics)
14. [Key Constants](#14-key-constants)
15. [Code Architecture](#15-code-architecture)
16. [References](#16-references)
17. [Cross-References](#17-cross-references)

---

## 1. Design Philosophy

A number is not knowledge. When a C3 model emits `da_caudate = 0.73`, that floating-point value carries no intrinsic meaning. It becomes knowledge only when placed in context: *What computation produced it? Which brain region does it represent? What psychological state does it imply? How could an experimenter verify it? How does the listener learn from it? Which semantic direction does it point? What word describes it? How does it fit into a narrative?*

L3 -- the Lexical LOGOS Lattice -- provides eight layers of context, one for each of these epistemological questions. It is the semantic interpretation layer of MI: the stage where raw neural computation acquires scientific, psychological, and linguistic meaning.

Four principles govern L3's design:

### 1.1 Epistemological Grounding

Every L3 dimension answers a specific scientific question. The eight groups form an epistemological ladder, ascending from computational transparency to narrative description:

```
Level 8  theta  HOW to describe   -- narrative structure for language generation
Level 7  eta    WHAT word         -- 64-gradation vocabulary quantization
Level 6  zeta   WHICH direction   -- 12 bipolar semantic axes
Level 5  epsilon HOW listener learns -- online learning dynamics (STATEFUL)
Level 4  delta  HOW to test       -- measurable physiological/neural/behavioral targets
Level 3  gamma  WHAT it means     -- psychological constructs (reward, emotion, chills)
Level 2  beta   WHERE in brain    -- brain region activations, neurotransmitters, circuits
Level 1  alpha  HOW computed      -- pathway attribution, certainty, directionality
```

No dimension exists without a formula and a citation. This is not aspirational -- it is an architectural constraint enforced in code.

### 1.2 Zero Learned Parameters

L3 contains no trainable weights. Every dimension is computed from a fixed, citable formula applied to the Brain output. This makes L3 fully transparent: given the same Brain output, L3 always produces the same interpretation. The formulas can be audited, reproduced, and challenged by domain experts.

### 1.3 Cascaded Dependency

The eight groups are not independent. Learning dynamics (epsilon) feed into polarity axes (zeta), which feed into vocabulary (eta). Narrative (theta) reads both learning and polarity. This creates a principled information flow: raw computation becomes psychological meaning becomes bipolar direction becomes human-readable language.

### 1.4 Graceful Degradation

In mi_beta, the Brain's dimensionality varies by which units and models are active. L3 handles missing dimensions through `_safe_get_dim()` fallbacks: any Brain dimension that is not present defaults to 0.5 (neutral). This means L3 never crashes on partial Brain output -- it degrades gracefully, producing neutral interpretations for missing signals.

---

## 2. Pipeline Position

```
Audio Signal (44,100 Hz)
    |
    v
Cochlea (128-mel spectrogram, B x 128 x T @ 172.27 Hz)
    |
    v
+================================================================+
|              R3 Spectral Extractor (128D)                       |
|   Groups A-K: Consonance, Energy, Timbre, Change, Interactions, |
|   Pitch, Rhythm, Harmony, Information, TimbreExt, Modulation    |
+================================================================+
    |
    v
R3 Output: (B, T, 128) -- dense spectral tensor, [0,1] range
    |
    v
+================================================================+
|              H3 Temporal Morphology Layer (sparse)              |
|   ~8,600 4-tuples from 96 C3 models                            |
+================================================================+
    |
    v
+================================================================+
|              C3 Brain (96 models, 9 units)                      |
|   BEP+ASA mechanisms, E/M/P/F output layers                    |
+================================================================+
    |
    v
BrainOutput: (B, T, 1006) -- full perceptual representation
    |
    v
+================================================================+
|              L3 Semantic Interpretation (104D)                  |
|                                                                 |
|   Input:  BrainOutput tensor (B, T, D)                         |
|   Output: L3Output tensor (B, T, 104)                          |
|                                                                 |
|   Phase 1:  alpha(6) + beta(14) + gamma(13) + delta(12)       |
|   Phase 1b: epsilon(19)                  [STATEFUL]            |
|   Phase 2a: zeta(12)    <-- epsilon                            |
|   Phase 2b: eta(12)     <-- zeta                               |
|   Phase 2c: theta(16)   <-- epsilon + zeta                     |
+================================================================+
    |
    v
L3Output: (B, T, 104) -- 8 semantic groups concatenated
    |
    v
MI-space (downstream applications: search, recommendation, NLG)
```

L3 is a **semantic transformer**: it takes dense perceptual representations from the Brain and produces interpretable, citable, linguistically grounded descriptions. The output dimensionality is fixed at 104 in the reference specification, though mi_beta allows alpha and beta to auto-configure to the active model set.

**Key invariants**:
- L3 reads BrainOutput; it never reads R3, H3, or raw audio directly
- L3 output range is `[0, 1]` for all groups except zeta `[-1, +1]`
- L3 contains zero learned parameters -- every dimension has a formula
- Epsilon is the only stateful group; it must be reset between audio files
- Frame rate is inherited through the pipeline: 172.27 Hz (5.8 ms/frame)

---

## 3. The 8 Semantic Groups

### 3.1 Overview Table

| # | Symbol | Name | Dim | Range | Phase | Stateful | Epistemological Question |
|:-:|:------:|------|:---:|:-----:|:-----:|:--------:|--------------------------|
| 1 | alpha | Computation | 6 | [0,1] | 1 | No | HOW was this computed? |
| 2 | beta | Neuroscience | 14 | [0,1] | 1 | No | WHERE in the brain? |
| 3 | gamma | Psychology | 13 | [0,1] | 1 | No | WHAT does it mean subjectively? |
| 4 | delta | Validation | 12 | [0,1] | 1 | No | HOW to test empirically? |
| 5 | epsilon | Learning | 19 | [0,1] | 1b | **Yes** | HOW does the listener learn? |
| 6 | zeta | Polarity | 12 | [-1,+1] | 2a | No | WHICH direction? |
| 7 | eta | Vocabulary | 12 | [0,1] | 2b | No | WHAT word describes this? |
| 8 | theta | Narrative | 16 | [0,1] | 2c | No | HOW to describe in language? |
| | | **Total** | **104** | | | | |

### 3.2 Index Ranges

```
Dimension:  0    6    20   33   45   64   76   88   104
            |    |    |    |    |    |    |    |    |
Group:      [alpha][beta ][gamma][delta][epsilon][zeta][eta ][theta]
            6D    14D   13D   12D   19D      12D  12D  16D
```

### 3.3 Audience Map

| Group | Primary Audience | What They Get |
|-------|-----------------|---------------|
| alpha | Engineers | Computational attribution, confidence metrics |
| beta | Neuroscientists | Brain region activations, neurotransmitter levels, circuit states |
| gamma | Psychologists | Reward, emotion, aesthetics, chills |
| delta | Experimenters | Predicted physiological, neural, behavioral measurements |
| epsilon | Information theorists | Surprise, entropy, prediction errors, learning dynamics |
| zeta | Semanticists | Bipolar axes with named poles |
| eta | Linguists, lay users | Human-readable vocabulary terms at 64 gradations |
| theta | Narrative researchers | Subject-predicate-modifier-connector structure |

---

## 4. Group 1: Alpha -- Computation (6D)

**Level**: 1 -- HOW was this computed?
**Index range**: [0:6]
**Phase**: 1 (Independent)
**Code**: `mi_beta/language/groups/alpha.py` (98 lines)
**Scientific basis**: White-box attribution, Bayesian precision

### 4.1 Purpose

Alpha provides computational transparency. It answers: which processing pathways contributed to the current output, how confident is the computation, and what is its net direction?

### 4.2 Dimension Table

| Local | Name | Range | Formula | Source |
|:-----:|------|:-----:|---------|--------|
| alpha0 | `shared_attribution` | [0,1] | mean(Brain[shared_pathway]) | Pathway mean |
| alpha1 | `reward_attribution` | [0,1] | mean(Brain[reward_pathway]) | Pathway mean |
| alpha2 | `affect_attribution` | [0,1] | mean(Brain[affect_pathway]) | Pathway mean |
| alpha3 | `autonomic_attribution` | [0,1] | mean(Brain[autonomic_pathway]) | Pathway mean |
| alpha4 | `computation_certainty` | [0,1] | 1 / (1 + Var(Brain)) | Bayesian precision |
| alpha5 | `bipolar_activation` | [0,1] | (mean(Brain) - 0.5) * 2 * 0.5 + 0.5 | Signed summary |

### 4.3 Formulas

**Per-unit attribution** (mi_beta: per active unit):
```
attribution_u = mean(BrainOutput.get_unit(u), dim=-1)    for each active unit u
```

**Computation certainty** (inverse variance = Bayesian precision):
```
certainty = 1 / (1 + Var(BrainOutput.tensor, dim=-1))
```

**Bipolar activation** (net direction of Brain output):
```
bipolar = (mean(BrainOutput.tensor, dim=-1) - 0.5) * 2.0
bipolar_rescaled = bipolar * 0.5 + 0.5     # remap [-1,+1] -> [0,1]
```

### 4.4 Variable Dimensionality (mi_beta)

In mi_beta, alpha auto-configures to the active unit set:
- **Doc spec**: 4 pathway attributions + 2 globals = 6D
- **mi_beta**: N_active_units + 2 (e.g., 9 units + 2 = 11D)

Alpha auto-configures on first call by inspecting `brain_output.unit_outputs.keys()`.

---

## 5. Group 2: Beta -- Neuroscience (14D)

**Level**: 2 -- WHERE in the brain?
**Index range**: [6:20]
**Phase**: 1 (Independent)
**Code**: `mi_beta/language/groups/beta.py` (123 lines)
**Scientific basis**: Salimpoor 2011, Blood & Zatorre 2001, Howe 2013, Kim 2021, Koelsch 2006

### 5.1 Purpose

Beta maps Brain model outputs to brain region activations, neurotransmitter dynamics, and circuit states. It answers: which brain structures would be active if a human were experiencing this musical moment?

### 5.2 Dimension Table

#### Brain Regions (8D)

| Local | Name | Region | MNI Coordinates | Citation |
|:-----:|------|--------|:--------------:|----------|
| beta0 | `nacc_activation` | Nucleus Accumbens | (10, 12, -8) | Salimpoor 2011 |
| beta1 | `caudate_activation` | Caudate Nucleus | (12, 10, 14) | Salimpoor 2011 |
| beta2 | `vta_activation` | Ventral Tegmental Area | (0, -16, -10) | Howe 2013 |
| beta3 | `sn_activation` | Substantia Nigra | (8, -18, -12) | Howe 2013 |
| beta4 | `stg_activation` | Superior Temporal Gyrus | (58, -22, 8) | Kim 2021 |
| beta5 | `ifg_activation` | Inferior Frontal Gyrus | (-48, 16, 20) | Fong 2020 |
| beta6 | `amygdala_activation` | Amygdala | (24, -4, -18) | Koelsch 2006 |
| beta7 | `hippocampus_activation` | Hippocampus | (28, -18, -14) | Sachs 2025 |

#### Neurotransmitter Dynamics (3D)

| Local | Name | System | Formula | Citation |
|:-----:|------|--------|---------|----------|
| beta8 | `dopamine_level` | Striatal DA | (NAcc + Caudate) / 2 | Salimpoor 2011 |
| beta9 | `opioid_level` | Endogenous opioid proxy | liking pathway activation | Blood & Zatorre 2001 |
| beta10 | `da_opioid_interaction` | DA x Opioid | dopamine * opioid | Berridge 2003 |

#### Circuit States (3D)

| Local | Name | Circuit | Formula | Citation |
|:-----:|------|---------|---------|----------|
| beta11 | `anticipation_circuit` | Caudate -> DA ramp | caudate_activation (wanting) | Salimpoor 2011 |
| beta12 | `consummation_circuit` | NAcc -> DA burst | nacc_activation (liking) | Salimpoor 2011 |
| beta13 | `learning_circuit` | VTA -> RPE | abs(prediction_error) | Fong 2020 |

### 5.3 Variable Dimensionality (mi_beta)

In mi_beta, beta auto-configures to the set of unique brain regions declared by active models:
- **Doc spec**: 8 regions + 3 neurotransmitters + 3 circuits = 14D
- **mi_beta**: N_unique_regions (auto-discovered from model BrainRegion declarations)

Beta auto-configures from the ModelRegistry, collecting all unique `brain_regions.abbreviation` values from active models.

---

## 6. Group 3: Gamma -- Psychology (13D)

**Level**: 3 -- WHAT does it mean subjectively?
**Index range**: [20:33]
**Phase**: 1 (Independent)
**Code**: `mi_beta/language/groups/gamma.py` (134 lines)
**Scientific basis**: Salimpoor 2011, Berridge 2003, Huron 2006, Russell 1980, Blood & Zatorre 2001

### 6.1 Purpose

Gamma maps Brain outputs to psychological constructs that capture subjective musical experience: reward, emotion, aesthetics, and chills. It answers: what does a listener feel?

### 6.2 Dimension Table

#### Reward (3D)

| Local | Name | Range | Formula | Citation |
|:-----:|------|:-----:|---------|----------|
| gamma0 | `reward_intensity` | [0,1] | pleasure | Salimpoor 2011 |
| gamma1 | `reward_type` | [0,1] | (liking - wanting) * 0.5 + 0.5 | Berridge 2003 |
| gamma2 | `reward_phase` | [0,1] | (da_nacc - da_caudate) * 0.5 + 0.5 | Salimpoor 2011 |

**Interpretation**: gamma1 near 0 = wanting-dominant (anticipation); near 1 = liking-dominant (consummation). gamma2 near 0 = anticipation phase (caudate > NAcc); near 1 = consummation phase (NAcc > caudate).

#### ITPRA (2D)

| Local | Name | Range | Formula | Citation |
|:-----:|------|:-----:|---------|----------|
| gamma3 | `itpra_tension_resolution` | [0,1] | (1 - tension) * harmonic_context | Huron 2006 |
| gamma4 | `itpra_surprise_evaluation` | [0,1] | abs(prediction_error) * emotional_arc | Huron 2006 |

**Interpretation**: gamma3 captures the tension-resolution trajectory of Huron's ITPRA model. gamma4 captures the surprise-evaluation pathway.

#### Aesthetics (3D)

| Local | Name | Range | Formula | Citation |
|:-----:|------|:-----:|---------|----------|
| gamma5 | `beauty` | [0,1] | beauty (direct from Brain) | Blood & Zatorre 2001 |
| gamma6 | `sublime` | [0,1] | pleasure * arousal | Konecni 2005 |
| gamma7 | `groove` | [0,1] | arousal * harmonic_context | Janata 2012 |

**Interpretation**: Beauty is opioid-mediated hedonic pleasure. Sublime is the intersection of peak pleasure and peak arousal -- awe, transcendence. Groove is motor-harmonic coupling -- the pleasure of synchronized movement.

#### Emotion (2D)

| Local | Name | Range | Formula | Citation |
|:-----:|------|:-----:|---------|----------|
| gamma8 | `valence` | [0,1] | valence (direct from Brain) | Russell 1980 |
| gamma9 | `arousal` | [0,1] | arousal (direct from Brain) | Yang 2025 |

**Interpretation**: These two dimensions define the circumplex model of affect (Russell 1980). Valence is the positive/negative axis; arousal is the activation/deactivation axis.

#### Chills (3D)

| Local | Name | Range | Formula | Citation |
|:-----:|------|:-----:|---------|----------|
| gamma10 | `chill_probability` | [0,1] | scr * (1 - hr) | de Fleurian & Pearce 2021 |
| gamma11 | `chill_intensity` | [0,1] | chills_intensity (direct) | Sloboda 1991, Guhn 2007 |
| gamma12 | `chill_phase` | [0,1] | sigmoid(chills_intensity - tension) | Grewe 2009 |

**Interpretation**: Chills are autonomic nervous system signatures. Probability combines skin conductance response with heart rate deceleration. Phase distinguishes buildup (pre-chill tension > chills) from peak/afterglow (chills > tension).

---

## 7. Group 4: Delta -- Validation (12D)

**Level**: 4 -- HOW to test empirically?
**Index range**: [33:45]
**Phase**: 1 (Independent)
**Code**: `mi_beta/language/groups/delta.py` (112 lines)
**Scientific basis**: de Fleurian & Pearce 2021, Salimpoor 2011/2013, Schubert 2004

### 7.1 Purpose

Delta generates testable predictions. Each dimension corresponds to a measurable physiological, neural, or behavioral signal that an experimenter could record and compare against L3's output. Delta makes L3 falsifiable.

### 7.2 Dimension Table

#### Physiological (4D)

| Local | Name | Measurement | Formula | Citation | Effect Size |
|:-----:|------|------------|---------|----------|:-----------:|
| delta0 | `skin_conductance` | SCR (microsiemens) | scr (direct) | de Fleurian & Pearce 2021 | d=0.85 |
| delta1 | `heart_rate` | HR change (BPM) | hr (direct) | Thayer 2009 | -- |
| delta2 | `pupil_diameter` | Pupil dilation (mm) | arousal * abs(prediction_error) | Laeng 2012 | -- |
| delta3 | `piloerection` | Goosebump probability | chills_intensity (direct) | Sloboda 1991 | -- |

#### Neural (3D)

| Local | Name | Measurement | Formula | Citation | Correlation |
|:-----:|------|------------|---------|----------|:-----------:|
| delta4 | `fmri_nacc_bold` | NAcc BOLD signal | da_nacc (direct) | Salimpoor 2011 | r=0.84 |
| delta5 | `fmri_caudate_bold` | Caudate BOLD signal | da_caudate (direct) | Salimpoor 2011 | r=0.71 |
| delta6 | `eeg_frontal_alpha` | Frontal alpha suppression | 1 - pleasure | Sammler 2007 | -- |

#### Behavioral (2D)

| Local | Name | Measurement | Formula | Citation |
|:-----:|------|------------|---------|----------|
| delta7 | `willingness_to_pay` | Auction price ($0-$2) | pleasure | Salimpoor 2013 |
| delta8 | `button_press_rating` | Continuous pleasure rating | pleasure | Schubert 2004 |

#### Temporal (3D)

| Local | Name | Prediction | Formula | Citation |
|:-----:|------|-----------|---------|----------|
| delta9 | `wanting_leads_liking` | Caudate precedes NAcc | sigmoid(da_caudate - da_nacc) | Salimpoor 2011 |
| delta10 | `rpe_latency` | RPE magnitude predicts latency | abs(prediction_error) | Fong 2020 |
| delta11 | `refractory_state` | Inter-chill cooldown | 1 - chills_intensity | Grewe 2009 |

---

## 8. Group 5: Epsilon -- Learning (19D, STATEFUL)

**Level**: 5 -- HOW does the listener learn?
**Index range**: [45:64]
**Phase**: 1b (Stateful)
**Code**: `mi_beta/language/groups/epsilon.py` (336 lines)
**Scientific basis**: Pearce 2005, Shannon 1948, Friston 2010, Schmidhuber 2009, Huron 2006

### 8.1 Purpose

Epsilon models how a listener acquires expectations during music listening. It tracks surprise, entropy, prediction errors at multiple timescales, precision, information dynamics, and maps these to Huron's ITPRA theory and reward/aesthetic constructs. Epsilon is the only stateful group -- it maintains running statistics that accumulate across frames.

### 8.2 Dimension Table

#### Surprise and Entropy (2D)

| Local | Name | Range | Formula | Citation |
|:-----:|------|:-----:|---------|----------|
| eps0 | `surprise` | [0,1] | -log2(P(state|prev_state)) / log2(N_states) | Pearce 2005 (IDyOM) |
| eps1 | `entropy` | [0,1] | -sum(P * log2(P)) / log2(N_states) | Shannon 1948 |

**Mechanism**: 8-state Markov chain. Pleasure is quantized to bins 0-7. Transition counts accumulate online (Laplace-smoothed). Surprise is the negative log-probability of the observed transition; entropy is the uncertainty of the current state's transition distribution.

#### Prediction Errors (3D)

| Local | Name | Range | Timescale | Formula | Citation |
|:-----:|------|:-----:|:---------:|---------|----------|
| eps2 | `pe_short` | [0,1] | ~58ms | tanh((x - EMA_short) / sigma_short) * 0.5 + 0.5 | Koelsch 2019 |
| eps3 | `pe_medium` | [0,1] | ~580ms | tanh((x - EMA_medium) / sigma_medium) * 0.5 + 0.5 | Koelsch 2019 |
| eps4 | `pe_long` | [0,1] | ~5.8s | tanh((x - EMA_long) / sigma_long) * 0.5 + 0.5 | Koelsch 2019 |

**Mechanism**: Three exponential moving average (EMA) trackers at different timescales. Each prediction error is the deviation from the EMA, normalized by the running standard deviation, passed through tanh, and remapped to [0,1].

#### Precision (2D)

| Local | Name | Range | Formula | Citation |
|:-----:|------|:-----:|---------|----------|
| eps5 | `precision_short` | [0,1] | 1 / (1 + Var_short) | Friston 2010 |
| eps6 | `precision_long` | [0,1] | 1 / (1 + Var_long) | Friston 2010 |

**Mechanism**: Inverse variance (Bayesian precision). High precision means the signal is stable and predictions are confident; low precision means high uncertainty.

#### Information Dynamics (3D)

| Local | Name | Range | Formula | Citation |
|:-----:|------|:-----:|---------|----------|
| eps7 | `bayesian_surprise` | [0,1] | sigmoid(abs(PE_medium) * precision_long * 5) | Itti & Baldi 2009 |
| eps8 | `information_rate` | [0,1] | entropy * (1 - autocorrelation) | Dubnov 2008 |
| eps9 | `compression_progress` | [0,1] | sigmoid((entropy_old - entropy_new) * 5) | Schmidhuber 2009 |

**Mechanism**: Bayesian surprise quantifies belief update magnitude. Information rate captures the flow of novel information (entropy discounted by self-correlation). Compression progress -- Schmidhuber's "curiosity" signal -- measures whether the model's internal entropy is decreasing (learning) via a ring buffer split into old and new halves.

#### Interaction (1D)

| Local | Name | Range | Formula | Citation |
|:-----:|------|:-----:|---------|----------|
| eps10 | `entropy_x_surprise` | [0,1] | entropy * surprise | Cheung et al. 2019 |

**Interpretation**: The sweet spot for musical pleasure: high surprise in a high-entropy (uncertain) context. This interaction term predicts chill ratings better than either component alone (Cheung et al. 2019).

#### ITPRA Mapping (5D)

| Local | Name | ITPRA Stage | Formula | Citation |
|:-----:|------|:-----------:|---------|----------|
| eps11 | `imagination` | I (Imagination) | EMA_long (pleasure baseline) | Huron 2006 |
| eps12 | `tension_uncertainty` | T (Tension) | entropy (= state uncertainty) | Huron 2006 |
| eps13 | `prediction_reward` | P (Prediction) | exp(-abs(PE) / sigma_medium) | Huron 2006 |
| eps14 | `reaction_magnitude` | R (Reaction) | abs(PE_medium) * precision_long | Huron 2006 |
| eps15 | `appraisal_learning` | A (Appraisal) | compression_progress | Huron 2006 |

**Interpretation**: Huron's ITPRA theory describes five stages of response to musical events: Imagination (pre-stimulus expectation), Tension (uncertainty during anticipation), Prediction (reward for correct prediction), Reaction (magnitude of surprise response), Appraisal (post-hoc evaluation and learning). Epsilon maps each stage to a computable formula.

#### Reward and Aesthetics (3D)

| Local | Name | Range | Formula | Citation |
|:-----:|------|:-----:|---------|----------|
| eps16 | `reward_pe` | [0,1] | tanh(x - EMA_medium) * 0.5 + 0.5 | Gold et al. 2019 |
| eps17 | `wundt_position` | [0,1] | 4 * surprise * (1 - surprise) | Berlyne 1971 |
| eps18 | `familiarity` | [0,1] | log1p(state_visits) / log1p(total_visits) | Zajonc 1968 |

**Interpretation**: Reward PE is the hedonic prediction error. Wundt position implements the inverted-U curve (Berlyne's optimal arousal): maximal at surprise=0.5, zero at both extremes. Familiarity grows with exposure -- the mere exposure effect (Zajonc 1968).

### 8.3 State Architecture

Epsilon maintains the following state between frames:

```
State Component               Shape          Update Rule
---                           ---            ---
EMA accumulators (3 scales)   (B, 2) x 3    alpha * x + (1 - alpha) * EMA
EMA variance (3 scales)       (B, 2) x 3    alpha * (x - EMA)^2 + (1 - alpha) * Var
Welford online mean/M2        (B, 2) x 2    Welford's algorithm (numerically stable)
Welford count                 scalar         +1 per frame
Markov transition matrix      (B, 8, 8)     count[prev][curr] += 1 (Laplace init)
Previous state                (B,)           current quantized pleasure bin
Previous pleasure             (B,)           pleasure at t-1
Ring buffer                   (B, 50)        circular write for compression progress
Buffer index / count          scalar x 2     modular index, min(count+1, 50)
```

**Reset protocol**: `epsilon.reset()` clears all state. Must be called between audio files. The L3Orchestrator exposes `orchestrator.reset()` which delegates to epsilon.

### 8.4 EMA Timescale Correspondence

```
Timescale     alpha     1/alpha   Duration       Musical Scale
---           ---       ---       ---            ---
Short         0.1       ~10       ~58 ms         Single onset / attack
Medium        0.01      ~100      ~580 ms        One beat at 103 BPM
Long          0.001     ~1000     ~5.8 s         Musical phrase / passage
```

---

## 9. Group 6: Zeta -- Polarity (12D)

**Level**: 6 -- WHICH direction?
**Index range**: [64:76]
**Phase**: 2a (reads epsilon output)
**Code**: `mi_beta/language/groups/zeta.py` (145 lines)
**Scientific basis**: Osgood 1957 (Semantic Differential), Russell 1980 (Circumplex)

### 9.1 Purpose

Zeta maps the Brain's unipolar [0,1] activations and epsilon's learning dynamics onto 12 bipolar semantic axes. Each axis has named negative and positive poles, creating a human-interpretable semantic space.

### 9.2 The 12 Bipolar Axes

| Local | Axis | Negative Pole | Positive Pole | Source | Citation |
|:-----:|------|:-------------:|:-------------:|--------|----------|
| zeta0 | valence | sad | joyful | Brain: valence | Russell 1980 |
| zeta1 | arousal | calm | excited | Brain: arousal | Yang 2025 |
| zeta2 | tension | relaxed | tense | Brain: tension | Huron 2006 |
| zeta3 | power | delicate | powerful | Brain: arousal (proxy) | Osgood 1957 |
| zeta4 | wanting | satiated | craving | Brain: wanting | Berridge 2003 |
| zeta5 | liking | displeasure | satisfaction | Brain: liking | Berridge 2003 |
| zeta6 | novelty | familiar | novel | Epsilon: surprise | Berlyne 1971 |
| zeta7 | complexity | simple | complex | Epsilon: entropy | Berlyne 1971 |
| zeta8 | beauty | discordant | harmonious | Brain: beauty | Blood & Zatorre 2001 |
| zeta9 | groove | rigid | flowing | Brain: arousal * harmonic_ctx | Janata 2012 |
| zeta10 | stability | chaotic | stable | Epsilon: precision_long | Friston 2010 |
| zeta11 | engagement | detached | absorbed | Brain: pleasure * arousal | Csikszentmihalyi 1990 |

### 9.3 Conversion Formula

All Brain dimensions are in [0,1]. The polarity transform is:

```
polarity = 2 * brain_value - 1        # maps [0,1] -> [-1,+1]
```

For epsilon-derived axes (novelty, complexity, stability), the epsilon output tensor is indexed directly:

```
novelty    = 2 * epsilon[..., 0] - 1    # surprise -> novelty polarity
complexity = 2 * epsilon[..., 1] - 1    # entropy -> complexity polarity
stability  = 2 * epsilon[..., 6] - 1    # precision_long -> stability polarity
```

### 9.4 Axis Grouping

```
Reward Axes (6D):     valence, arousal, tension, power, wanting, liking
                      |--- from Brain dimensions directly ---|

Learning Axes (3D):   novelty, complexity, stability
                      |--- from epsilon output ---|

Aesthetic Axes (3D):  beauty, groove, engagement
                      |--- from Brain (beauty, arousal*harmonic_ctx, pleasure*arousal) ---|
```

### 9.5 Output Range

Zeta is the **only** L3 group with output in [-1, +1]. All other groups output in [0, 1]. The output is clamped: `tensor.clamp(-1, 1)`.

---

## 10. Group 7: Eta -- Vocabulary (12D)

**Level**: 7 -- WHAT word describes this?
**Index range**: [76:88]
**Phase**: 2b (reads zeta output)
**Code**: `mi_beta/language/groups/eta.py` (176 lines)
**Scientific basis**: Rosch 1975 (Prototype Theory), Trier 1931 (Semantic Field Theory), Weber 1834 (JND)

### 10.1 Purpose

Eta quantizes the continuous polarity axes from zeta into a 64-gradation vocabulary system. Each axis is divided into 8 intensity bands, each with 8 sub-gradations, yielding 64 discrete levels. Each band has a human-readable term.

### 10.2 The 64-Gradation System

```
Polarity:  -1.0                    0.0                    +1.0
            |--------|--------|--------|--------|--------|--------|--------|--------|
Band:       0        1        2        3        4        5        6        7
Gradations: [0..7]   [8..15]  [16..23] [24..31] [32..39] [40..47] [48..55] [56..63]

Step size:  1/64 = 1.5625%  (below human JND of ~3%)
Bits/axis:  6 (log2(64) = 6)
Total bits: 12 axes * 6 bits = 72 bits
```

### 10.3 Band Terms (96 unique terms: 12 axes x 8 bands)

| Axis | Band 0 | Band 1 | Band 2 | Band 3 | Band 4 | Band 5 | Band 6 | Band 7 |
|------|--------|--------|--------|--------|--------|--------|--------|--------|
| valence | devastating | melancholic | wistful | subdued | neutral | content | happy | euphoric |
| arousal | comatose | lethargic | drowsy | calm | neutral | alert | energized | explosive |
| tension | dissolved | slack | easy | mild | neutral | taut | strained | crushing |
| power | whisper | fragile | gentle | moderate | neutral | strong | forceful | overwhelming |
| wanting | fulfilled | content | settled | mild | neutral | interested | eager | desperate |
| liking | aversive | unpleasant | bland | indifferent | neutral | pleasant | delightful | ecstatic |
| novelty | habitual | routine | known | expected | neutral | fresh | surprising | shocking |
| complexity | trivial | basic | clear | moderate | neutral | elaborate | intricate | labyrinthine |
| beauty | harsh | grating | rough | plain | neutral | pleasing | beautiful | sublime |
| groove | mechanical | stiff | stilted | measured | neutral | swinging | grooving | transcendent |
| stability | turbulent | erratic | unsteady | wavering | neutral | steady | anchored | immovable |
| engagement | oblivious | indifferent | distracted | aware | neutral | attentive | immersed | entranced |

### 10.4 Quantization Formula

```python
# Polarity [-1,+1] -> normalized [0,1]
normalized = (polarity + 1.0) * 0.5

# Normalized [0,1] -> gradation index [0,63]
gradation = round(normalized * 63).clamp(0, 63)

# Gradation [0,63] -> band index [0,7]
band = gradation // 8

# Output tensor: normalized gradation back to [0,1]
output = gradation / 63
```

### 10.5 JND Rationale

The 64-gradation system provides a step size of 1/64 = 1.5625%. Human perceptual Just Noticeable Difference (JND) for most psychophysical dimensions is approximately 3% (Weber's law). With 64 gradations, adjacent levels are below the JND threshold -- meaning we never lose perceptually meaningful resolution. The 8-band structure groups these fine gradations into linguistically distinct categories.

### 10.6 The `get_terms()` Method

Eta provides a `get_terms(zeta_output)` method that returns human-readable vocabulary labels:

```python
terms = eta_group.get_terms(zeta_output)
# Returns: [
#   [{"axis": "valence", "band_index": 6, "term": "happy"}, ...],
#   [{"axis": "arousal", "band_index": 5, "term": "alert"}, ...],
#   ...
# ]
```

This method is for downstream natural language generation. The tensor output of eta provides the quantized values; `get_terms()` provides the words.

---

## 11. Group 8: Theta -- Narrative (16D)

**Level**: 8 -- HOW to describe in language?
**Index range**: [88:104]
**Phase**: 2c (reads epsilon + zeta output)
**Code**: `mi_beta/language/groups/theta.py` (155 lines)
**Scientific basis**: Schubert 2004, Sloboda 1991, Gabrielsson 2001, Huron 2006

### 11.1 Purpose

Theta generates sentence-level narrative structure for describing musical moments. It decomposes a musical moment into four linguistic roles: Subject (WHICH aspect dominates), Predicate (WHAT is happening), Modifier (HOW it is happening), and Connector (TEMPORAL relation to what came before).

### 11.2 Dimension Table

#### Subject (4D) -- WHICH aspect dominates

| Local | Name | Meaning | Formula | Citation |
|:-----:|------|---------|---------|----------|
| theta0 | `reward_salience` | Reward/pleasure dominates | softmax(pleasure, T=3.0) | Salimpoor 2011 |
| theta1 | `tension_salience` | Tension/conflict dominates | softmax(tension, T=3.0) | Huron 2006 |
| theta2 | `motion_salience` | Movement/energy dominates | softmax(arousal, T=3.0) | Yang 2025 |
| theta3 | `beauty_salience` | Beauty/harmony dominates | softmax(beauty, T=3.0) | Blood & Zatorre 2001 |

**Mechanism**: Softmax competition at temperature 3.0 over [pleasure, tension, arousal, beauty]. The softmax temperature of 3.0 creates moderate competition -- one subject typically dominates but others can contribute.

```
subject = softmax([pleasure, tension, arousal, beauty] * 3.0, dim=-1)
```

#### Predicate (4D) -- WHAT is happening

| Local | Name | Meaning | Formula | Citation |
|:-----:|------|---------|---------|----------|
| theta4 | `rising` | Subject is increasing | clamp(pe_short - 0.5, min=0) * 2 | Schubert 2004 |
| theta5 | `peaking` | Subject is at climax | pleasure * arousal | Sloboda 1991 |
| theta6 | `falling` | Subject is decreasing | clamp(0.5 - pe_short, min=0) * 2 | Schubert 2004 |
| theta7 | `stable` | Subject is holding steady | 1 - (rising + falling + peaking) | Meyer 1956 |

**Mechanism**: Predicate is derived from epsilon's short-term prediction error. Positive PE (pe_short > 0.5) means rising; negative PE (pe_short < 0.5) means falling. Peaking is the conjunction of high pleasure and high arousal. Stable is the complement.

#### Modifier (4D) -- HOW it is happening

| Local | Name | Meaning | Source | Citation |
|:-----:|------|---------|--------|----------|
| theta8 | `intensity` | How strongly | arousal | Gabrielsson 2001 |
| theta9 | `certainty` | How confidently | epsilon: precision_short | Friston 2010 |
| theta10 | `novelty` | How surprisingly | epsilon: surprise | Berlyne 1971 |
| theta11 | `speed` | How quickly | sigmoid(abs(prediction_error) * 3) | Fong 2020 |

#### Connector (4D) -- TEMPORAL relation

| Local | Name | Meaning | Formula | Citation |
|:-----:|------|---------|---------|----------|
| theta12 | `continuing` | Same thread continues | 1 / (1 + abs(val_pol) + abs(ten_pol)) | Halliday & Hasan 1976 |
| theta13 | `contrasting` | Opposing element | (abs(val_pol) + abs(ten_pol)) * 0.5 | Almen 2008 |
| theta14 | `resolving` | Tension resolves | clamp(-ten_pol, min=0) | Huron 2006 |
| theta15 | `transitioning` | Moving to new section | 1 - (continuing + contrasting + resolving) | Caplin 1998 |

**Mechanism**: Connectors are derived from zeta polarity axes (valence and tension). Low polarity magnitude = continuation. High polarity magnitude = contrast. Negative tension polarity (tension relaxing) = resolution. The remainder = transition.

### 11.3 Narrative Generation Example

Given theta output at a frame:
```
Subject:   [0.08, 0.12, 0.15, 0.65]  -- beauty dominates
Predicate: [0.72, 0.31, 0.02, 0.05]  -- rising
Modifier:  [0.40, 0.80, 0.30, 0.55]  -- certain, moderate intensity
Connector: [0.15, 0.60, 0.20, 0.05]  -- contrasting
```

Natural language: *"In contrast to the preceding section, beauty is rising with moderate intensity and high certainty."*

---

## 12. Computation Phases and Dependency Graph

### 12.1 Phase Definitions

```
Phase 1   (Independent):  alpha, beta, gamma, delta
                          Read only BrainOutput. No mutual dependencies.
                          Can be computed in parallel.

Phase 1b  (Stateful):    epsilon
                          Reads only BrainOutput. Maintains state.
                          Must execute sequentially (frame-by-frame).

Phase 2a  (Dependent):   zeta
                          Reads epsilon output (learning axes).
                          No other L3 group dependencies.

Phase 2b  (Dependent):   eta
                          Reads zeta output (quantizes polarity).
                          No other L3 group dependencies.

Phase 2c  (Dependent):   theta
                          Reads epsilon + zeta output.
                          Must wait for both Phase 1b and Phase 2a.
```

### 12.2 Dependency DAG

```
BrainOutput
    |
    +---> alpha (6D)   ----+
    |                      |
    +---> beta (14D)   ----+
    |                      |
    +---> gamma (13D)  ----+--> [concatenate Phase 1 outputs]
    |                      |
    +---> delta (12D)  ----+
    |
    +---> epsilon (19D) ---+--> [Phase 1b complete]
                |          |
                |          +---> zeta (12D) ---+--> [Phase 2a complete]
                |                   |          |
                |                   |          +---> eta (12D) -- [Phase 2b]
                |                   |
                +-------+-----------+
                        |
                        +---> theta (16D) ------- [Phase 2c complete]

Final: cat(alpha, beta, gamma, delta, epsilon, zeta, eta, theta) -> (B, T, 104)
```

### 12.3 Orchestrator Execution Sequence

The L3Orchestrator executes groups in strict dependency order:

```python
# Phase 1: Independent (could be parallel)
alpha_out  = alpha.compute(brain_output)
beta_out   = beta.compute(brain_output)
gamma_out  = gamma.compute(brain_output)
delta_out  = delta.compute(brain_output)

# Phase 1b: Stateful
epsilon_out = epsilon.compute(brain_output)

# Phase 2a: Dependent on epsilon
zeta_out = zeta.compute(brain_output, epsilon_output=epsilon_out.tensor)

# Phase 2b: Dependent on zeta
eta_out = eta.compute(brain_output, zeta_output=zeta_out.tensor)

# Phase 2c: Dependent on epsilon + zeta
theta_out = theta.compute(brain_output, epsilon_output=epsilon_out.tensor,
                          zeta_output=zeta_out.tensor)

# Concatenate
combined = cat([alpha, beta, gamma, delta, epsilon, zeta, eta, theta], dim=-1)
```

---

## 13. Unique Characteristics

L3 differs from R3, H3, and C3 in several fundamental ways:

### 13.1 Stateful Computation (Epsilon Only)

R3, H3, and C3 are stateless -- given the same input at time t, they always produce the same output regardless of history. Epsilon breaks this invariant: its output at time t depends on all frames 0..t-1. This statefulness is essential for modeling learning, prediction, and surprise, which are inherently temporal phenomena.

The statefulness is carefully contained: only epsilon is stateful, and its state is explicitly managed through the reset protocol.

### 13.2 Linguistic Output Pipeline

L3 contains a three-stage linguistic pipeline unique in the MI architecture:

```
epsilon (learning dynamics)
    |
    v
zeta (bipolar polarity axes, [-1,+1])
    |
    v
eta (64-gradation vocabulary, human-readable terms)
    |
    (+ epsilon + zeta)
    v
theta (narrative structure: subject-predicate-modifier-connector)
```

This pipeline transforms numerical computation into linguistic structure, enabling natural language generation about musical experience.

### 13.3 64-Gradation Vocabulary System

The eta group implements a perceptually grounded vocabulary system:
- 12 semantic axes x 8 intensity bands = 96 unique terms
- 64 gradations per axis (below JND threshold)
- 6 bits per axis, 72 bits total
- Each term is a psycholinguistic prototype (Rosch 1975)

No other MI layer produces linguistic output.

### 13.4 Variable Dimensionality (mi_beta)

In mi_beta, alpha and beta auto-configure their output dimensionality:
- Alpha: N_active_units + 2 (vs fixed 6D in spec)
- Beta: N_unique_regions (vs fixed 14D in spec)

This means L3's total output dimensionality can vary. The L3Orchestrator computes `total_dim` dynamically.

### 13.5 Zero Learned Parameters

L3 is pure formula. Every dimension is computed from a known equation with citable provenance. There are no weights to train, no gradients to compute, no loss functions to optimize. This makes L3:
- **Transparent**: every output can be traced to a formula
- **Reproducible**: given the same input, always the same output (except epsilon state)
- **Auditable**: domain experts can verify each formula against its citation
- **Interpretable**: every dimension has a human-readable scientific meaning

### 13.6 Epistemological Grounding

Every L3 dimension answers a specific scientific question. This is not a post-hoc labeling of arbitrary features -- it is the architectural design principle. The eight groups were chosen to span the epistemological space relevant to musical experience.

---

## 14. Key Constants

### 14.1 Architectural Constants

| Constant | Value | Source |
|----------|:-----:|--------|
| Total dimensions | 104 | 6+14+13+12+19+12+12+16 |
| Frame rate | 172.27 Hz | Inherited from R3 (hop_length=256, sr=44100) |
| Frame duration | 5.8 ms | 1 / 172.27 |
| Number of groups | 8 | alpha through theta |
| Number of phases | 5 | 1, 1b, 2a, 2b, 2c |

### 14.2 Epsilon State Constants

| Constant | Value | Meaning |
|----------|:-----:|---------|
| ALPHA_SHORT | 0.1 | EMA decay: ~10 frames (~58 ms) |
| ALPHA_MEDIUM | 0.01 | EMA decay: ~100 frames (~580 ms) |
| ALPHA_LONG | 0.001 | EMA decay: ~1000 frames (~5.8 s) |
| N_STATES | 8 | Markov transition matrix quantization bins (0-7) |
| BUFFER_SIZE | 50 | Ring buffer for compression progress |
| D_TRACK | 2 | Tracked signals: pleasure + arousal |
| EPS | 1e-8 | Numerical stability epsilon |

### 14.3 Eta/Vocabulary Constants

| Constant | Value | Meaning |
|----------|:-----:|---------|
| N_GRADATIONS | 64 | Total discrete levels per axis |
| N_BANDS | 8 | Intensity bands per axis |
| GRADATIONS_PER_BAND | 8 | Sub-gradations within each band |
| Step size | 1/64 = 1.5625% | Below human JND (~3%) |
| Total terms | 96 | 12 axes x 8 bands |
| Bits per axis | 6 | log2(64) = 6 |

### 14.4 Theta Constants

| Constant | Value | Meaning |
|----------|:-----:|---------|
| Softmax temperature | 3.0 | Subject selection competition strength |

---

## 15. Code Architecture

### 15.1 File Structure

```
mi_beta/
|-- language/
|   |-- __init__.py              L3 package: exports L3Orchestrator
|   |-- groups/
|   |   |-- __init__.py          L3Orchestrator: phase-ordered computation
|   |   |-- alpha.py             AlphaGroup: computation semantics (variable D)
|   |   |-- beta.py              BetaGroup: neuroscience semantics (variable D)
|   |   |-- gamma.py             GammaGroup: psychology semantics (13D)
|   |   |-- delta.py             DeltaGroup: validation semantics (12D)
|   |   |-- epsilon.py           EpsilonGroup: learning dynamics (19D, STATEFUL)
|   |   |-- zeta.py              ZetaGroup: polarity (12D, [-1,+1])
|   |   |-- eta.py               EtaGroup: vocabulary (12D, 64-gradation)
|   |   |-- theta.py             ThetaGroup: narrative (16D)
|   |
|   |-- adapters/
|       |-- __init__.py          Adapter registry
|       |-- _base_adapter.py     BaseModelSemanticAdapter ABC
|       |-- aru_adapter.py       ARU unit adapter
|       |-- asu_adapter.py       ASU unit adapter
|       |-- imu_adapter.py       IMU unit adapter
|       |-- mpu_adapter.py       MPU unit adapter
|       |-- ndu_adapter.py       NDU unit adapter
|       |-- pcu_adapter.py       PCU unit adapter
|       |-- rpu_adapter.py       RPU unit adapter
|       |-- spu_adapter.py       SPU unit adapter
|       |-- stu_adapter.py       STU unit adapter
|
|-- contracts/
|   |-- base_semantic_group.py   BaseSemanticGroup ABC (LEVEL, GROUP_NAME, compute())
|
|-- core/
    |-- types.py                 BrainOutput, L3Output, SemanticGroupOutput
```

**Total**: 21 files in `mi_beta/language/`

### 15.2 Module Responsibilities

#### `language/__init__.py` -- Package Entry Point

Exports `L3Orchestrator`. Single line of functional code:
```python
from .groups import L3Orchestrator
```

#### `language/groups/__init__.py` -- L3Orchestrator (141 lines)

The orchestrator that coordinates all 8 groups:
- Instantiates groups in an `OrderedDict` (alpha through theta)
- `compute(brain_output)`: executes groups in phase order, concatenates outputs
- `reset()`: delegates to epsilon for state cleanup
- `total_dim`: property that sums all group OUTPUT_DIMs

#### `language/groups/alpha.py` -- AlphaGroup (98 lines)

Computation semantics with variable dimensionality:
- Auto-configures from BrainOutput unit structure on first call
- Per-unit attribution via mean activation
- Computation certainty via inverse variance
- Bipolar activation via centered mean

#### `language/groups/beta.py` -- BetaGroup (123 lines)

Neuroscience semantics with variable dimensionality:
- Auto-configures from ModelRegistry brain region declarations
- Per-region activation via mean of contributing model outputs
- Falls back to placeholder dimension if no regions configured

#### `language/groups/gamma.py` -- GammaGroup (134 lines)

Psychology semantics (fixed 13D):
- Reward: intensity, type (wanting vs liking), phase (anticipation vs consummation)
- ITPRA: tension-resolution arc, surprise-evaluation pathway
- Aesthetics: beauty, sublime (pleasure x arousal), groove (arousal x harmony)
- Emotion: valence, arousal (circumplex model)
- Chills: probability, intensity, phase

#### `language/groups/delta.py` -- DeltaGroup (112 lines)

Validation semantics (fixed 12D):
- Physiological: SCR, HR, pupil dilation, piloerection
- Neural: NAcc BOLD, Caudate BOLD, frontal alpha suppression
- Behavioral: willingness to pay, button-press rating
- Temporal: wanting-leads-liking, RPE latency, refractory state

#### `language/groups/epsilon.py` -- EpsilonGroup (336 lines)

Learning dynamics (fixed 19D, STATEFUL):
- The largest and most complex group
- Frame-by-frame loop with online state accumulation
- 8-state Markov model, 3-timescale EMA, Welford variance, ring buffer
- Maps to ITPRA theory and reward/aesthetic constructs
- Requires `reset()` between audio files

#### `language/groups/zeta.py` -- ZetaGroup (145 lines)

Polarity axes (fixed 12D, [-1,+1]):
- 12 named bipolar axes with negative/positive poles
- Reads epsilon output for learning-derived axes (novelty, complexity, stability)
- 2x-1 transform from [0,1] to [-1,+1]
- Only group with output range [-1,+1]

#### `language/groups/eta.py` -- EtaGroup (176 lines)

Vocabulary quantization (fixed 12D, [0,1]):
- 64-gradation quantization of zeta polarity
- 96 human-readable terms (12 axes x 8 bands)
- `get_terms()` method for downstream NLG
- Tensor output is the normalized gradation index

#### `language/groups/theta.py` -- ThetaGroup (155 lines)

Narrative structure (fixed 16D):
- Subject: softmax competition (pleasure, tension, arousal, beauty)
- Predicate: rising/peaking/falling/stable from epsilon PE
- Modifier: intensity, certainty, novelty, speed
- Connector: continuing/contrasting/resolving/transitioning from zeta polarity

### 15.3 Contract Interface

All groups implement `BaseSemanticGroup` (defined in `mi_beta/contracts/base_semantic_group.py`):

```python
class BaseSemanticGroup(ABC):
    LEVEL: int                    # epistemological level (1-8)
    GROUP_NAME: str               # lowercase name ("alpha", "beta", ...)
    OUTPUT_DIM: int               # number of output dimensions

    @property
    @abstractmethod
    def dimension_names(self) -> List[str]:
        """Return ordered list of dimension names."""
        ...

    @abstractmethod
    def compute(self, brain_output: Any, **kwargs: Any) -> SemanticGroupOutput:
        """Compute semantic group from BrainOutput."""
        ...
```

### 15.4 Data Types

```python
@dataclass
class SemanticGroupOutput:
    group_name: str                   # "alpha", "beta", ...
    level: int                        # 1-8
    tensor: Tensor                    # (B, T, group_dim)
    dimension_names: Tuple[str, ...]  # names for each dim

@dataclass
class L3Output:
    model_name: str                   # "Brain"
    groups: Dict[str, SemanticGroupOutput]
    tensor: Tensor                    # (B, T, total_dim) concatenated
```

### 15.5 Execution Flow

```
Application code
    |
    v
orchestrator = L3Orchestrator(registry=registry)
    |
    v
l3_output = orchestrator.compute(brain_output)
    |
    +-- Phase 1: alpha.compute(brain_output)       -> (B, T, 6)
    +-- Phase 1: beta.compute(brain_output)        -> (B, T, 14)
    +-- Phase 1: gamma.compute(brain_output)       -> (B, T, 13)
    +-- Phase 1: delta.compute(brain_output)       -> (B, T, 12)
    |
    +-- Phase 1b: epsilon.compute(brain_output)    -> (B, T, 19)
    |                  |
    +-- Phase 2a: zeta.compute(brain_output,
    |                  epsilon_output=eps.tensor)   -> (B, T, 12)
    |                  |
    +-- Phase 2b: eta.compute(brain_output,
    |                  zeta_output=zeta.tensor)     -> (B, T, 12)
    |
    +-- Phase 2c: theta.compute(brain_output,
                       epsilon_output=eps.tensor,
                       zeta_output=zeta.tensor)     -> (B, T, 16)
    |
    v
torch.cat([alpha, beta, gamma, delta, epsilon,
           zeta, eta, theta], dim=-1)               -> (B, T, 104)
    |
    v
L3Output(model_name="Brain", groups={...}, tensor=combined)
```

---

## 16. References

### 16.1 Core Citations

| # | Citation | Used In | Contribution |
|:-:|----------|---------|-------------|
| 1 | Salimpoor, V.N. et al. (2011). Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262. | beta, gamma, delta, theta | NAcc/Caudate BOLD correlation with pleasure; wanting-leads-liking temporal ordering |
| 2 | Blood, A.J. & Zatorre, R.J. (2001). Intensely pleasurable responses to music correlate with activity in brain regions implicated in reward and emotion. *PNAS*, 98(20), 11818-11823. | beta, gamma, zeta | Opioid-mediated hedonic response; beauty dimension |
| 3 | Berridge, K.C. (2003). Pleasures of the brain. *Brain and Cognition*, 52(1), 106-128. | gamma, zeta | Wanting vs liking dissociation; dopamine-opioid interaction |
| 4 | Huron, D. (2006). *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press. | gamma, epsilon, theta | ITPRA theory: Imagination, Tension, Prediction, Reaction, Appraisal |
| 5 | Russell, J.A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*, 39(6), 1161-1178. | gamma, zeta | Valence-arousal circumplex model |
| 6 | Pearce, M.T. (2005). *The Construction and Evaluation of Statistical Models of Melodic Structure in Music Perception and Composition*. PhD thesis, City University London. | epsilon | IDyOM: Information Dynamics of Music; Markov-based surprise and entropy |
| 7 | Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138. | epsilon, zeta, theta | Precision-weighted prediction errors; free-energy minimization |
| 8 | Schmidhuber, J. (2009). Simple algorithmic theory of subjective beauty, novelty, surprise, interestingness, attention, curiosity, creativity, art, science, music, jokes. *JMLR*, 185-200. | epsilon | Compression progress as intrinsic reward |
| 9 | Osgood, C.E., Suci, G.J., & Tannenbaum, P.H. (1957). *The Measurement of Meaning*. University of Illinois Press. | zeta | Semantic Differential Theory; evaluation-potency-activity |
| 10 | Rosch, E. (1975). Cognitive representations of semantic categories. *Journal of Experimental Psychology: General*, 104(3), 192-233. | eta | Prototype Theory; categorical perception of vocabulary terms |

### 16.2 Additional Citations

| # | Citation | Used In | Contribution |
|:-:|----------|---------|-------------|
| 11 | Shannon, C.E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379-423. | epsilon | Information entropy formula |
| 12 | Koelsch, S. (2019). *Music and the Brain*. In Oxford Handbook of Music Psychology. | epsilon | Multi-timescale prediction error hierarchy |
| 13 | Itti, L. & Baldi, P. (2009). Bayesian surprise attracts human attention. *Vision Research*, 49(10), 1295-1306. | epsilon | Bayesian surprise: KL divergence of belief update |
| 14 | Dubnov, S. (2008). Musical information dynamics as models of auditory anticipation. In *Machine Audition*, 371-397. | epsilon | Information rate in music perception |
| 15 | Cheung, V.K.M. et al. (2019). Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092. | epsilon | Entropy x surprise interaction predicts pleasure |
| 16 | Berlyne, D.E. (1971). *Aesthetics and Psychobiology*. Appleton-Century-Crofts. | epsilon, zeta | Inverted-U (Wundt curve); novelty-complexity aesthetics |
| 17 | Zajonc, R.B. (1968). Attitudinal effects of mere exposure. *Journal of Personality and Social Psychology*, 9(2, Pt.2), 1-27. | epsilon | Mere exposure effect; familiarity accumulation |
| 18 | Gold, B.P. et al. (2019). Musical reward prediction errors engage the nucleus accumbens and motivate learning. *PNAS*, 116(8), 3310-3315. | epsilon | Reward prediction error in musical context |
| 19 | de Fleurian, R. & Pearce, M.T. (2021). Chills in music: A systematic review. *Psychological Bulletin*, 147(9), 890-920. | gamma, delta | SCR as chill predictor; effect size d=0.85 |
| 20 | Sloboda, J.A. (1991). Music structure and emotional response. *Psychology of Music*, 19(2), 110-120. | gamma, delta, theta | Chills, piloerection, peaking |
| 21 | Grewe, O. et al. (2009). Chills in different sensory domains. *Music Perception*, 27(1), 37-50. | gamma, delta | Chill phase (buildup/peak/afterglow); refractory period |
| 22 | Schubert, E. (2004). Modeling perceived emotion with continuous musical features. *Music Perception*, 21(4), 561-585. | delta, theta | Continuous pleasure rating; rising/falling dynamics |
| 23 | Salimpoor, V.N. et al. (2013). Interactions between the nucleus accumbens and auditory cortices predict music reward value. *Science*, 340(6129), 216-219. | delta | Willingness-to-pay auction paradigm |
| 24 | Sammler, D. et al. (2007). Music and emotion: electrophysiological correlates. *Psychophysiology*, 44(2), 293-304. | delta | EEG frontal alpha suppression |
| 25 | Thayer, J.F. et al. (2009). Heart rate variability, prefrontal neural function, and cognitive performance. *Annals of Behavioral Medicine*, 37(2), 141-153. | delta | Heart rate as emotional arousal index |
| 26 | Laeng, B. et al. (2012). Pupillometry: a window to the preconscious? *Perspectives on Psychological Science*, 7(1), 18-27. | delta | Pupil dilation tracks cognitive load and arousal |
| 27 | Fong, C.Y. et al. (2020). The influence of musical training on prediction error processing. *NeuroImage*, 222, 117252. | delta, theta | RPE latency; IFG activation |
| 28 | Janata, P. et al. (2012). Sensorimotor coupling in music and the psychology of the groove. *Journal of Experimental Psychology: General*, 141(1), 54-75. | gamma, zeta | Groove: motor-harmonic coupling pleasure |
| 29 | Konecni, V.J. (2005). The aesthetic trinity: awe, being moved, thrills. *Bulletin of Psychology and the Arts*, 5(2), 27-44. | gamma | Sublime: awe and transcendence |
| 30 | Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience*. Harper & Row. | zeta | Engagement/absorption; flow state |
| 31 | Gabrielsson, A. (2001). Emotions in strong experiences with music. In *Music and Emotion*, 431-449. | theta | Intensity of musical experience |
| 32 | Meyer, L.B. (1956). *Emotion and Meaning in Music*. University of Chicago Press. | theta | Stability in musical expectation |
| 33 | Halliday, M.A.K. & Hasan, R. (1976). *Cohesion in English*. Longman. | theta | Textual connectors: continuation |
| 34 | Almen, B. (2008). *A Theory of Musical Narrative*. Indiana University Press. | theta | Musical contrast and opposition |
| 35 | Caplin, W.E. (1998). *Classical Form*. Oxford University Press. | theta | Formal transitions in musical structure |
| 36 | Howe, M.W. et al. (2013). Prolonged dopamine signalling in striatum signals proximity and value of distant rewards. *Nature*, 500, 575-579. | beta | VTA/SN dopamine signaling |
| 37 | Kim, S.G. et al. (2021). Decoding musical training from dynamic processing of musical features in the brain. *Scientific Reports*, 11, 2024. | beta | STG in auditory processing |
| 38 | Koelsch, S. (2006). Significance of Broca's area and ventral premotor cortex for music-syntactic processing. *Cortex*, 42(4), 518-520. | beta | Amygdala in musical emotion |
| 39 | Sachs, M.E. et al. (2025). The hippocampus and music: a comprehensive review. *Trends in Cognitive Sciences*. | beta | Hippocampus in musical memory |

---

## 17. Cross-References

### 17.1 L3 Documentation Tree

| Document | Path | Content |
|----------|------|---------|
| Master index | [L3/00-INDEX.md](00-INDEX.md) | Directory structure, summary tables |
| **This document** | [L3/L3-SEMANTIC-ARCHITECTURE.md](L3-SEMANTIC-ARCHITECTURE.md) | Definitive architecture spec |
| Dimension catalog | [L3/Registry/DimensionCatalog.md](Registry/DimensionCatalog.md) | All 104 dimensions with full metadata |
| Group map | [L3/Registry/GroupMap.md](Registry/GroupMap.md) | Group index ranges and dependencies |
| Naming conventions | [L3/Registry/NamingConventions.md](Registry/NamingConventions.md) | Dimension naming rules |
| Extension guide | [L3/EXTENSION-GUIDE.md](EXTENSION-GUIDE.md) | How to add new groups or dimensions |
| Changelog | [L3/CHANGELOG.md](CHANGELOG.md) | Version history |

### 17.2 Epistemology Documents

| Document | Path | Level |
|----------|------|:-----:|
| Computation | [L3/Epistemology/Computation.md](Epistemology/Computation.md) | 1 (alpha) |
| Neuroscience | [L3/Epistemology/Neuroscience.md](Epistemology/Neuroscience.md) | 2 (beta) |
| Psychology | [L3/Epistemology/Psychology.md](Epistemology/Psychology.md) | 3 (gamma) |
| Validation | [L3/Epistemology/Validation.md](Epistemology/Validation.md) | 4 (delta) |
| Learning | [L3/Epistemology/Learning.md](Epistemology/Learning.md) | 5 (epsilon) |
| Polarity | [L3/Epistemology/Polarity.md](Epistemology/Polarity.md) | 6 (zeta) |
| Vocabulary | [L3/Epistemology/Vocabulary.md](Epistemology/Vocabulary.md) | 7 (eta) |
| Narrative | [L3/Epistemology/Narrative.md](Epistemology/Narrative.md) | 8 (theta) |

### 17.3 Group Detail Documents

| Document | Path | Group |
|----------|------|:-----:|
| Alpha detail | [L3/Groups/Independent/Alpha.md](Groups/Independent/Alpha.md) | alpha |
| Beta detail | [L3/Groups/Independent/Beta.md](Groups/Independent/Beta.md) | beta |
| Gamma detail | [L3/Groups/Independent/Gamma.md](Groups/Independent/Gamma.md) | gamma |
| Delta detail | [L3/Groups/Independent/Delta.md](Groups/Independent/Delta.md) | delta |
| Epsilon detail | [L3/Groups/Independent/Epsilon.md](Groups/Independent/Epsilon.md) | epsilon |
| Zeta detail | [L3/Groups/Dependent/Zeta.md](Groups/Dependent/Zeta.md) | zeta |
| Eta detail | [L3/Groups/Dependent/Eta.md](Groups/Dependent/Eta.md) | eta |
| Theta detail | [L3/Groups/Dependent/Theta.md](Groups/Dependent/Theta.md) | theta |

### 17.4 Pipeline Documents

| Document | Path | Content |
|----------|------|---------|
| R3 spectral architecture | [R3/R3-SPECTRAL-ARCHITECTURE.md](../R3/R3-SPECTRAL-ARCHITECTURE.md) | 128D spectral space |
| H3 temporal architecture | [H3/H3-TEMPORAL-ARCHITECTURE.md](../H3/H3-TEMPORAL-ARCHITECTURE.md) | Temporal morphology layer |
| C3 brain architecture | [C3/C3-ARCHITECTURE.md](../C3/C3-ARCHITECTURE.md) | 96-model brain |
| C3 output space | [C3/Matrices/Output-Space.md](../C3/Matrices/Output-Space.md) | 1006D brain output |

### 17.5 Code References

| Component | Code Path | Role |
|-----------|-----------|------|
| L3 package | `mi_beta/language/__init__.py` | Package entry point |
| L3 orchestrator | `mi_beta/language/groups/__init__.py` | Phase-ordered group execution |
| Alpha group | `mi_beta/language/groups/alpha.py` | Computation semantics |
| Beta group | `mi_beta/language/groups/beta.py` | Neuroscience semantics |
| Gamma group | `mi_beta/language/groups/gamma.py` | Psychology semantics |
| Delta group | `mi_beta/language/groups/delta.py` | Validation semantics |
| Epsilon group | `mi_beta/language/groups/epsilon.py` | Learning dynamics (STATEFUL) |
| Zeta group | `mi_beta/language/groups/zeta.py` | Polarity axes |
| Eta group | `mi_beta/language/groups/eta.py` | Vocabulary quantization |
| Theta group | `mi_beta/language/groups/theta.py` | Narrative structure |
| Base contract | `mi_beta/contracts/base_semantic_group.py` | BaseSemanticGroup ABC |
| Adapter base | `mi_beta/language/adapters/_base_adapter.py` | Per-unit adapter ABC |
| Unit adapters | `mi_beta/language/adapters/{unit}_adapter.py` | 9 unit-specific adapters |
| Core types | `mi_beta/core/types.py` | BrainOutput, L3Output, SemanticGroupOutput |

---

## Appendix A: Quick Reference Card

```
L3 = Lexical LOGOS Lattice (Semantic Interpretation Layer)
    Input:  BrainOutput tensor (B, T, D) from C3
    Output: L3Output tensor (B, T, 104)  -- 8 groups concatenated

Properties: Zero learned parameters. Every dimension has a formula and citation.
            Stateful computation (epsilon only). Must reset between audio files.

Groups:
  alpha   [0:6]    6D  Computation    HOW computed        Phase 1    [0,1]
  beta    [6:20]  14D  Neuroscience   WHERE in brain      Phase 1    [0,1]
  gamma  [20:33]  13D  Psychology     WHAT it means       Phase 1    [0,1]
  delta  [33:45]  12D  Validation     HOW to test         Phase 1    [0,1]
  epsilon[45:64]  19D  Learning       HOW listener learns Phase 1b   [0,1]  STATEFUL
  zeta   [64:76]  12D  Polarity       WHICH direction     Phase 2a  [-1,+1]
  eta    [76:88]  12D  Vocabulary     WHAT word           Phase 2b   [0,1]
  theta  [88:104] 16D  Narrative      HOW to describe     Phase 2c   [0,1]

Dependency Chain:
  BrainOutput -> {alpha, beta, gamma, delta} (parallel)
  BrainOutput -> epsilon (stateful, sequential)
  epsilon -> zeta -> eta
  epsilon + zeta -> theta

Epsilon State:
  EMA accumulators:      3 timescales (short ~58ms, medium ~580ms, long ~5.8s)
  Markov transition:     8x8 matrix (Laplace-smoothed)
  Welford variance:      online mean/M2
  Ring buffer:           size 50 (compression progress)
  Reset:                 orchestrator.reset() between audio files

Vocabulary (eta):
  64 gradations = 8 bands x 8 sub-gradations
  Step size: 1/64 = 1.5625% (below JND ~3%)
  96 terms: 12 axes x 8 bands
  6 bits/axis, 72 bits total

Code: mi_beta/language/ (21 files)
      mi_beta/contracts/base_semantic_group.py
      mi_beta/core/types.py
```
