# L³ — Brain Semantic Space (104D)

> Musical Intelligence (MI) v2.0.0 — 2026-02-12
> The interpretation layer: giving meaning to computation.
> Scope: Unified MusicalBrain (26D) → 8 semantic groups → 104D total.
> Replaces: [L³-SRP-SEMANTIC-SPACE.md](L³-SRP-SEMANTIC-SPACE.md), [L³-AAC-SEMANTIC-SPACE.md](L³-AAC-SEMANTIC-SPACE.md), [L³-VMM-SEMANTIC-SPACE.md](L³-VMM-SEMANTIC-SPACE.md)

---

## 1. Overview

L³ (Lexical LOGOS Lattice) is MI's **semantic interpretation layer**. It
answers the question: "What does this computation MEAN?"

The unified MusicalBrain produces **26 dimensions per frame** across five
internal pathways (Shared State, Reward, Affect, Autonomic, Integration).
These are numbers. By themselves, they say nothing about brain regions,
subjective experience, or how to test them. L³ provides **eight interpretation
groups** (alpha through theta) that give the 26D computation its scientific,
psychological, and linguistic meaning.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     L³ BRAIN SEMANTIC SPACE (104D)                      │
│                                                                        │
│  Input: MusicalBrain (26D)                                             │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  Shared(4D) Reward(9D) Affect(6D) Autonomic(5D) Integ(2D)  │       │
│  └──────────────────────────────────────────────────────────────┘       │
│                              ↓                                         │
│  ┌─── Phase 1: Independent ────────────────────────────────────┐       │
│  │  α  Computation    HOW was this computed?             6D    │       │
│  │  β  Neuroscience   WHERE in the brain?               14D   │       │
│  │  γ  Psychology     WHAT does it mean subjectively?   13D   │       │
│  │  δ  Validation     HOW to test empirically?          12D   │       │
│  │  ε  Learning       HOW does the listener learn?      19D   │       │
│  └─────────────────────────────────────────────────────────────┘       │
│                              ↓                                         │
│  ┌─── Phase 2: Dependent (ε→ζ→η, ε+ζ→θ) ─────────────────────┐       │
│  │  ζ  Polarity       WHICH direction? [-1,+1]          12D   │       │
│  │  η  Vocabulary     WHAT word describes this?         12D   │       │
│  │  θ  Narrative      HOW to describe in language?      16D   │       │
│  └─────────────────────────────────────────────────────────────┘       │
│                                                                        │
│  TOTAL: 6+14+13+12+19+12+12+16 = 104D per frame                       │
│  Zero learned parameters. Every dimension has a citation.              │
└──────────────────────────────────────────────────────────────────────────┘
```

### Why L³ Exists

A number is not knowledge. `da_caudate = 0.73` means nothing without context.
L³ provides **eight layers of context** — one for each epistemological question
a scientist, psychologist, or listener might ask:

| Layer | Question | Audience |
|-------|----------|----------|
| α | HOW was this computed? | Engineers, system designers |
| β | WHERE in the brain? | Neuroscientists |
| γ | WHAT does it mean subjectively? | Psychologists |
| δ | HOW to test empirically? | Experimenters |
| ε | HOW does the listener learn? | Information theorists |
| ζ | WHICH direction? | Semanticists |
| η | WHAT word describes this? | Linguists, lay users |
| θ | HOW to describe in language? | Narrative researchers, NLG |

### Architecture

All eight groups inherit from `BaseSemanticGroup`, which defines:

```python
class BaseSemanticGroup(ABC):
    LEVEL: int           # 1-8
    GROUP_NAME: str      # "alpha", "beta", etc.
    DISPLAY_NAME: str    # "α", "β", etc.
    OUTPUT_DIM: int      # dimensionality

    def compute(self, brain_output, **kwargs) -> SemanticGroupOutput
    def dimension_names -> List[str]
```

The orchestrator `BrainSemantics` (total_dim=104) manages dependency ordering
and calls `reset()` on stateful groups between audio files.

---

## 2. The 8-Level Epistemological Framework

The eight semantic groups form an **epistemological ladder** — each level answers
a progressively deeper question about the same 26D Brain computation.

```
Level 1  α: HOW was this computed?          ← Pathway attribution
Level 2  β: WHERE in the brain?             ← Neural localization
Level 3  γ: WHAT does it mean?              ← Subjective experience
Level 4  δ: HOW to test it?                 ← Empirical validation
Level 5  ε: HOW does the listener learn?    ← Online statistics (STATEFUL)
                    ↓
Level 6  ζ: WHICH direction?                ← Bipolar polarity [-1,+1]
                    ↓
Level 7  η: WHAT word describes this?       ← Vocabulary (64-gradation)
                    ↓
Level 8  θ: HOW to describe in language?    ← Narrative sentence structure
```

Levels 1-5 read only `brain_output` (Phase 1, independent).
Levels 6-8 form a dependency chain (Phase 2):

- **ζ** reads `epsilon_output` to derive learning-based polarity axes
- **η** reads `zeta_output` to quantize polarity into vocabulary terms
- **θ** reads `epsilon_output` + `zeta_output` to construct narrative

---

## 3. Computation Phases

### Phase 1 — Independent Groups

All five Phase 1 groups read only `brain_output` (26D). They can be computed
in any order (the current implementation runs them sequentially for
simplicity, but they have no mutual dependencies).

```python
# Phase 1: α, β, γ, δ (stateless, independent)
for name in ("alpha", "beta", "gamma", "delta"):
    out = groups[name].compute(brain_output)

# Phase 1b: ε (stateful, but reads only brain_output)
eps_out = groups["epsilon"].compute(brain_output)
```

**Epsilon** is placed in Phase 1b because it reads only `brain_output`, but it
is stateful: it maintains EMA accumulators, Markov transition counts, Welford
statistics, and a ring buffer across frames.

### Phase 2 — Dependent Groups

Phase 2 groups form a strict dependency chain:

```python
# Phase 2a: ζ (needs ε output)
zeta_out = groups["zeta"].compute(brain_output, epsilon_output=eps_out.tensor)

# Phase 2b: η (needs ζ output)
eta_out = groups["eta"].compute(brain_output, zeta_output=zeta_out.tensor)

# Phase 2c: θ (needs ε + ζ output)
theta_out = groups["theta"].compute(
    brain_output,
    epsilon_output=eps_out.tensor,
    zeta_output=zeta_out.tensor,
)
```

### Dependency Graph

```
brain_output ─────────┬──→ α (6D)
                      ├──→ β (14D)
                      ├──→ γ (13D)
                      ├──→ δ (12D)
                      ├──→ ε (19D) ──┬──→ ζ (12D) ──┬──→ η (12D)
                      │              │               │
                      │              └──────┬────────┘
                      │                     ↓
                      └─────────────────→ θ (16D)
```

Final assembly:

```python
combined = torch.cat([α, β, γ, δ, ε, ζ, η, θ], dim=-1)  # (B, T, 104)
```

---

## 4. Detailed Group Specifications

### 4.1 Alpha (α) — Computation Semantics (6D)

**Level 1: HOW was this computed?**

Traces each Brain dimension back to its computational source pathway.
Provides pathway attribution, computation certainty (Bayesian precision),
and net bipolar activation direction.

| Index | Name | Range | Description | Source |
|-------|------|-------|-------------|--------|
| α0 | `shared_attribution` | [0, 1] | Mean activation of the Shared State pathway (4D) | White-box attribution |
| α1 | `reward_attribution` | [0, 1] | Mean activation of the Reward pathway (9D) | White-box attribution |
| α2 | `affect_attribution` | [0, 1] | Mean activation of the Affect pathway (6D) | White-box attribution |
| α3 | `autonomic_attribution` | [0, 1] | Mean activation of the Autonomic pathway (5D) | White-box attribution |
| α4 | `computation_certainty` | [0, 1] | Inverse output variance: 1/(1+Var(26D)) | Bayesian precision |
| α5 | `bipolar_activation` | [-1, 1] | Net direction: 0.5*(prediction_error + f03_valence) | Signed summary |

**Formulas:**

```
α0 = mean(shared_pathway)          # mean of Brain[0:4]
α1 = mean(reward_pathway)          # mean of Brain[4:13]
α2 = mean(affect_pathway)          # mean of Brain[13:19]
α3 = mean(autonomic_pathway)       # mean of Brain[19:24]
α4 = 1 / (1 + Var(Brain[0:26]))   # inverse variance = certainty
α5 = 0.5 * (prediction_error + f03_valence)  # net signed direction
```

---

### 4.2 Beta (β) — Neuroscience Semantics (14D)

**Level 2: WHERE in the brain?**

Maps Brain dimensions to brain regions, neurotransmitter dynamics, and
neural circuit states. Output clamped to [0, 1].

#### Brain Regions (8D)

| Index | Name | Range | Region | Citation |
|-------|------|-------|--------|----------|
| β0 | `nacc_activation` | [0, 1] | Nucleus Accumbens (ventral striatum) | Salimpoor 2011 |
| β1 | `caudate_activation` | [0, 1] | Caudate Nucleus (dorsal striatum) | Salimpoor 2011 |
| β2 | `vta_activation` | [0, 1] | Ventral Tegmental Area (midbrain) | Howe 2013 |
| β3 | `sn_activation` | [0, 1] | Substantia Nigra (midbrain proxy) | Howe 2013 |
| β4 | `stg_activation` | [0, 1] | Superior Temporal Gyrus (auditory cortex) | Kim 2021 |
| β5 | `ifg_activation` | [0, 1] | Inferior Frontal Gyrus (prediction) | Fong 2020 |
| β6 | `amygdala_activation` | [0, 1] | Amygdala (salience/emotion) | Koelsch 2006 |
| β7 | `hippocampus_activation` | [0, 1] | Hippocampus (memory encoding) | Sachs 2025 |

#### Neurotransmitter Dynamics (3D)

| Index | Name | Range | System | Citation |
|-------|------|-------|--------|----------|
| β8 | `dopamine_level` | [0, 1] | Striatal DA: (NAcc + Caudate)/2 | Salimpoor 2011 |
| β9 | `opioid_level` | [0, 1] | Endogenous opioid proxy | Blood & Zatorre 2001 |
| β10 | `da_opioid_interaction` | [0, 1] | DA * Opioid interaction term | Berridge 2003 |

#### Circuit States (3D)

| Index | Name | Range | Circuit | Citation |
|-------|------|-------|---------|----------|
| β11 | `anticipation_circuit` | [0, 1] | Caudate → DA ramp (wanting) | Salimpoor 2011 |
| β12 | `consummation_circuit` | [0, 1] | NAcc → DA burst (liking) | Salimpoor 2011 |
| β13 | `learning_circuit` | [0, 1] | VTA → RPE (|prediction_error|) | Fong 2020 |

**Key mappings:**

```
β0 = da_nacc                                          # direct
β1 = da_caudate                                       # direct
β2 = reward_forecast                                  # VTA = ramping DA
β3 = reward_forecast * 0.5                            # shared midbrain proxy
β4 = harmonic_context                                 # STG: harmony processing
β5 = σ(|prediction_error|)                            # IFG: prediction violation
β6 = σ(|prediction_error| * tension)                  # amygdala: salience gating
β7 = emotional_arc                                    # hippocampus: memory encoding
β8 = (β0 + β1) * 0.5                                 # DA level
β9 = opioid_proxy                                     # direct
β10 = β8 * β9                                         # interaction
```

---

### 4.3 Gamma (γ) — Psychology Semantics (13D)

**Level 3: WHAT does it mean subjectively?**

Maps Brain dimensions to psychological constructs: reward dynamics, ITPRA,
aesthetics, emotion, and chills. Output clamped to [0, 1].

#### Reward (3D)

| Index | Name | Range | Description | Citation |
|-------|------|-------|-------------|----------|
| γ0 | `reward_intensity` | [0, 1] | Overall reward signal = pleasure | Salimpoor 2011 |
| γ1 | `reward_type` | [0, 1] | Wanting-dominant (0) vs liking-dominant (1) | Berridge 2003 |
| γ2 | `reward_phase` | [0, 1] | Anticipation (0) vs consummation (1) | Salimpoor 2011 |

#### ITPRA (2D)

| Index | Name | Range | Description | Citation |
|-------|------|-------|-------------|----------|
| γ3 | `itpra_tension_resolution` | [0, 1] | (1-tension) * harmonic_context | Huron 2006 |
| γ4 | `itpra_surprise_evaluation` | [0, 1] | |prediction_error| * emotional_arc | Huron 2006 |

#### Aesthetics (3D)

| Index | Name | Range | Description | Citation |
|-------|------|-------|-------------|----------|
| γ5 | `beauty` | [0, 1] | Opioid-mediated hedonic pleasure (direct from Brain) | Blood & Zatorre 2001 |
| γ6 | `sublime` | [0, 1] | Awe/transcendence: pleasure * arousal | Konecni 2005 |
| γ7 | `groove` | [0, 1] | Motor-harmonic coupling: arousal * harmonic_context | Janata 2012 |

#### Emotion (2D)

| Index | Name | Range | Description | Citation |
|-------|------|-------|-------------|----------|
| γ8 | `valence` | [0, 1] | Positive/negative affect: (f03_valence+1)/2 | Russell 1980 |
| γ9 | `arousal` | [0, 1] | Activation level (direct from Brain) | Yang 2025 |

#### Chills (3D)

| Index | Name | Range | Description | Citation |
|-------|------|-------|-------------|----------|
| γ10 | `chill_probability` | [0, 1] | ANS chill signature: SCR * (1-HR) | de Fleurian & Pearce 2021 |
| γ11 | `chill_intensity` | [0, 1] | Integrated chill strength (direct from Brain) | Sloboda 1991, Guhn 2007 |
| γ12 | `chill_phase` | [0, 1] | Buildup/peak/afterglow: sigma(chills - tension) | Grewe 2009 |

---

### 4.4 Delta (δ) — Validation Semantics (12D)

**Level 4: HOW to test empirically?**

Maps Brain dimensions to measurable physiological, neural, and behavioral
signals. Each dimension represents a **testable prediction**. Output clamped
to [0, 1].

#### Physiological (4D)

| Index | Name | Range | Measure | Citation |
|-------|------|-------|---------|----------|
| δ0 | `skin_conductance` | [0, 1] | Expected SCR signal | de Fleurian & Pearce 2021, d=0.85 |
| δ1 | `heart_rate` | [0, 1] | Expected HR change | Thayer 2009 |
| δ2 | `pupil_diameter` | [0, 1] | Expected pupil dilation: arousal * |PE| | Laeng 2012 |
| δ3 | `piloerection` | [0, 1] | Expected goosebump probability | Sloboda 1991 |

#### Neural (3D)

| Index | Name | Range | Measure | Citation |
|-------|------|-------|---------|----------|
| δ4 | `fmri_nacc_bold` | [0, 1] | Expected NAcc BOLD signal | Salimpoor 2011, r=0.84 |
| δ5 | `fmri_caudate_bold` | [0, 1] | Expected Caudate BOLD signal | Salimpoor 2011, r=0.71 |
| δ6 | `eeg_frontal_alpha` | [0, 1] | Expected alpha suppression: 1-pleasure | Sammler 2007 |

#### Behavioral (2D)

| Index | Name | Range | Measure | Citation |
|-------|------|-------|---------|----------|
| δ7 | `willingness_to_pay` | [0, 1] | Salimpoor 2013 auction paradigm | Salimpoor 2013 |
| δ8 | `button_press_rating` | [0, 1] | Continuous pleasure rating | Schubert 2004 |

#### Temporal Constraints (3D)

| Index | Name | Range | Constraint | Citation |
|-------|------|-------|------------|----------|
| δ9 | `wanting_leads_liking` | [0, 1] | sigma(da_caudate - da_nacc): temporal ordering | Salimpoor 2011 |
| δ10 | `rpe_latency` | [0, 1] | |prediction_error|: PE magnitude | Fong 2020 |
| δ11 | `refractory_state` | [0, 1] | 1 - chills_intensity: inter-chill cooldown | Grewe 2009 |

---

### 4.5 Epsilon (ε) — Learning Dynamics (19D, STATEFUL)

**Level 5: HOW does the listener learn from the music over time?**

The **only stateful group** in L³. Epsilon maintains online statistics across
frames and must be **reset between audio files** via `BrainSemantics.reset()`.

See [Section 5](#5-epsilon-deep-dive--stateful-learning-dynamics) for the full
deep dive into epsilon's internal state machinery.

#### Surprise and Entropy (2D)

| Index | Name | Range | Description | Citation |
|-------|------|-------|-------------|----------|
| ε0 | `surprise` | [0, 1] | Transition surprisal from 8-state Markov model | Pearce 2005 (IDyOM) |
| ε1 | `entropy` | [0, 1] | State uncertainty: normalized Shannon entropy | Shannon 1948 |

#### Prediction Errors (3D)

| Index | Name | Range | Description | Citation |
|-------|------|-------|-------------|----------|
| ε2 | `pe_short` | [0, 1] | Short-term PE: tanh((x - EMA_short) / sigma_short) | Koelsch 2019 |
| ε3 | `pe_medium` | [0, 1] | Medium-term PE: tanh((x - EMA_medium) / sigma_medium) | Koelsch 2019 |
| ε4 | `pe_long` | [0, 1] | Long-term PE: tanh((x - EMA_long) / sigma_long) | Koelsch 2019 |

#### Precision (2D)

| Index | Name | Range | Description | Citation |
|-------|------|-------|-------------|----------|
| ε5 | `precision_short` | [0, 1] | Short-term confidence: 1/(1+Var_short) | Friston 2010 |
| ε6 | `precision_long` | [0, 1] | Long-term confidence: 1/(1+Var_long) | Friston 2010 |

#### Information Dynamics (3D)

| Index | Name | Range | Description | Citation |
|-------|------|-------|-------------|----------|
| ε7 | `bayesian_surprise` | [0, 1] | Belief update: sigma(|PE_medium| * precision_long * 5) | Itti & Baldi 2009 |
| ε8 | `information_rate` | [0, 1] | Mutual info past-present: entropy * (1 - autocorr) | Dubnov 2008 |
| ε9 | `compression_progress` | [0, 1] | Learning as reward: sigma((old_entropy - new_entropy) * 5) | Schmidhuber 2009 |

#### Interaction (1D)

| Index | Name | Range | Description | Citation |
|-------|------|-------|-------------|----------|
| ε10 | `entropy_x_surprise` | [0, 1] | Pleasure predictor: entropy * surprise | Cheung et al. 2019 |

#### ITPRA Mapping (5D)

| Index | Name | Range | ITPRA | Description | Citation |
|-------|------|-------|-------|-------------|----------|
| ε11 | `imagination` | [0, 1] | I | Long-term pleasure baseline: EMA_long[0] | Huron 2006 |
| ε12 | `tension_uncertainty` | [0, 1] | T | Entropy as tension source | Huron 2006 |
| ε13 | `prediction_reward` | [0, 1] | P | Reward for correct prediction: exp(-|PE|/sigma) | Huron 2006 |
| ε14 | `reaction_magnitude` | [0, 1] | R | Surprise magnitude: |PE| * precision_long | Huron 2006 |
| ε15 | `appraisal_learning` | [0, 1] | A | Compression progress (alias) | Huron 2006 |

#### Reward and Aesthetics (3D)

| Index | Name | Range | Description | Citation |
|-------|------|-------|-------------|----------|
| ε16 | `reward_pe` | [0, 1] | Reward prediction error: tanh(x - EMA_medium) | Gold et al. 2019 |
| ε17 | `wundt_position` | [0, 1] | Inverted-U: 4 * surprise * (1 - surprise) | Berlyne 1971 |
| ε18 | `familiarity` | [0, 1] | Exposure accumulation: log(transitions) / log(total) | Zajonc 1968 |

---

### 4.6 Zeta (ζ) — Polarity (12D, Bipolar)

**Level 6: WHICH direction?**

Maps Brain and epsilon outputs to 12 **bipolar semantic axes** in [-1, +1].
Each axis has named negative and positive poles following the Semantic
Differential Theory (Osgood et al. 1957) and the Circumplex Model of Affect
(Russell 1980).

| Index | Name | Neg Pole | Pos Pole | Range | Source | Citation |
|-------|------|----------|----------|-------|--------|----------|
| ζ0 | `valence` | sad | joyful | [-1, +1] | f03_valence (already bipolar) | Russell 1980 |
| ζ1 | `arousal` | calm | excited | [-1, +1] | 2*arousal - 1 | Yang 2025 |
| ζ2 | `tension` | relaxed | tense | [-1, +1] | 2*tension - 1 | Huron 2006 |
| ζ3 | `power` | delicate | powerful | [-1, +1] | 2*ans_composite - 1 | Osgood 1957 |
| ζ4 | `wanting` | satiated | craving | [-1, +1] | 2*wanting - 1 | Berridge 2003 |
| ζ5 | `liking` | displeasure | satisfaction | [-1, +1] | 2*liking - 1 | Berridge 2003 |
| ζ6 | `novelty` | familiar | novel | [-1, +1] | 2*epsilon[0] - 1 (surprise) | Berlyne 1971 |
| ζ7 | `complexity` | simple | complex | [-1, +1] | 2*epsilon[1] - 1 (entropy) | Berlyne 1971 |
| ζ8 | `beauty` | discordant | harmonious | [-1, +1] | 2*beauty - 1 | Blood & Zatorre 2001 |
| ζ9 | `groove` | rigid | flowing | [-1, +1] | 2*(harmonic_context * arousal) - 1 | Janata 2012 |
| ζ10 | `stability` | chaotic | stable | [-1, +1] | 2*epsilon[6] - 1 (precision_long) | Friston 2010 |
| ζ11 | `engagement` | detached | absorbed | [-1, +1] | 2*(pleasure * arousal) - 1 | Csikszentmihalyi 1990 |

**Axis grouping:**

- **Reward Axes** (ζ0-ζ5): Derived directly from Brain reward/affect dimensions
- **Learning Axes** (ζ6-ζ7, ζ10): Derived from epsilon output (surprise, entropy, precision)
- **Aesthetic Axes** (ζ8-ζ9, ζ11): Derived from Brain integration/interaction terms

---

### 4.7 Eta (η) — Vocabulary (12D, 64-Gradation)

**Level 7: WHAT word describes this?**

Quantizes each polarity axis from [-1, +1] into one of **64 discrete
gradation levels**, organized into **8 intensity bands** of 8 levels each.
The tensor output is the normalized gradation index (continuous [0, 1]);
the `get_terms()` method returns human-readable labels.

| Index | Name | Range | Gradation | Quantization |
|-------|------|-------|-----------|--------------|
| η0 | `valence_vocab` | [0, 1] | 64 levels | round((ζ0+1)/2 * 63) / 63 |
| η1 | `arousal_vocab` | [0, 1] | 64 levels | round((ζ1+1)/2 * 63) / 63 |
| η2 | `tension_vocab` | [0, 1] | 64 levels | round((ζ2+1)/2 * 63) / 63 |
| η3 | `power_vocab` | [0, 1] | 64 levels | round((ζ3+1)/2 * 63) / 63 |
| η4 | `wanting_vocab` | [0, 1] | 64 levels | round((ζ4+1)/2 * 63) / 63 |
| η5 | `liking_vocab` | [0, 1] | 64 levels | round((ζ5+1)/2 * 63) / 63 |
| η6 | `novelty_vocab` | [0, 1] | 64 levels | round((ζ6+1)/2 * 63) / 63 |
| η7 | `complexity_vocab` | [0, 1] | 64 levels | round((ζ7+1)/2 * 63) / 63 |
| η8 | `beauty_vocab` | [0, 1] | 64 levels | round((ζ8+1)/2 * 63) / 63 |
| η9 | `groove_vocab` | [0, 1] | 64 levels | round((ζ9+1)/2 * 63) / 63 |
| η10 | `stability_vocab` | [0, 1] | 64 levels | round((ζ10+1)/2 * 63) / 63 |
| η11 | `engagement_vocab` | [0, 1] | 64 levels | round((ζ11+1)/2 * 63) / 63 |

**64-gradation design rationale:**

- 8 intensity bands x 8 gradations per band = 64 levels
- Step size: 1/64 = 1.56% — below human JND (~3%) threshold (Weber 1834, Stevens 1957)
- 6 bits per axis — total 72 bits for 12 axes
- Based on Prototype Theory (Rosch 1975) and Semantic Field Theory (Trier 1931, Lyons 1977)

See [Section 6](#6-zeta--eta--theta-pipeline) for the complete vocabulary
term catalog.

---

### 4.8 Theta (θ) — Narrative (16D)

**Level 8: HOW to describe this in language?**

Constructs a **sentence-level linguistic structure** for generating natural
language descriptions of musical moments. Organized as a four-slot sentence:
Subject + Predicate + Modifier + Connector.

#### Subject (4D) — WHICH aspect dominates

| Index | Name | Range | Slot | Citation |
|-------|------|-------|------|----------|
| θ0 | `reward_salience` | [0, 1] | Reward/pleasure dominates | Salimpoor 2011 |
| θ1 | `tension_salience` | [0, 1] | Tension/conflict dominates | Huron 2006 |
| θ2 | `motion_salience` | [0, 1] | Movement/energy dominates | Yang 2025 |
| θ3 | `beauty_salience` | [0, 1] | Beauty/harmony dominates | Blood & Zatorre 2001 |

Subject is computed via **softmax competition** (temperature=3.0) over
pleasure, tension, arousal, and beauty from the Brain output.

#### Predicate (4D) — WHAT is happening

| Index | Name | Range | Slot | Citation |
|-------|------|-------|------|----------|
| θ4 | `rising` | [0, 1] | The subject is increasing | Schubert 2004 |
| θ5 | `peaking` | [0, 1] | The subject is at climax | Sloboda 1991 |
| θ6 | `falling` | [0, 1] | The subject is decreasing | Schubert 2004 |
| θ7 | `stable` | [0, 1] | The subject is holding steady | Meyer 1956 |

Predicate is derived from epsilon's short-term prediction error:
- `rising = clamp(pe_short - 0.5, min=0) * 2`
- `falling = clamp(0.5 - pe_short, min=0) * 2`
- `peaking = clamp(pleasure * arousal, 0, 1)`
- `stable = clamp(1 - rising - falling - peaking, min=0)`

#### Modifier (4D) — HOW it is happening

| Index | Name | Range | Slot | Citation |
|-------|------|-------|------|----------|
| θ8 | `intensity` | [0, 1] | How strongly (= arousal) | Gabrielsson 2001 |
| θ9 | `certainty` | [0, 1] | How confidently (= ε precision_short) | Friston 2010 |
| θ10 | `novelty` | [0, 1] | How surprisingly (= ε surprise) | Berlyne 1971 |
| θ11 | `speed` | [0, 1] | How quickly: sigma(|prediction_error| * 3) | Fong 2020 |

#### Connector (4D) — TEMPORAL relation

| Index | Name | Range | Slot | Citation |
|-------|------|-------|------|----------|
| θ12 | `continuing` | [0, 1] | Same thread continues | Halliday & Hasan 1976 |
| θ13 | `contrasting` | [0, 1] | Opposing element introduced | Almen 2008 |
| θ14 | `resolving` | [0, 1] | Tension/conflict resolves | Huron 2006 |
| θ15 | `transitioning` | [0, 1] | Moving to new section | Caplin 1998 |

Connector is derived from zeta polarity:
- `continuing = 1 / (1 + |valence_pol| + |tension_pol|)`
- `contrasting = (|valence_pol| + |tension_pol|) / 2`
- `resolving = clamp(-tension_pol, min=0)`
- `transitioning = clamp(1 - continuing - contrasting - resolving, min=0)`

---

## 5. Epsilon Deep Dive — Stateful Learning Dynamics

Epsilon is the **only stateful group** in L³. While all other groups perform
stateless transformations of the 26D Brain output, epsilon maintains **online
statistics** that accumulate over the duration of an audio file. This state
captures how the listener's internal model adapts to the music in real time.

### 5.1 Internal State Components

```
EpsilonGroup
├── EMA accumulators (3 timescales × 2D = 6 tensors)
│   ├── _ema_short    (B, 2)   α=0.1    ~58ms     ~10 frames
│   ├── _ema_medium   (B, 2)   α=0.01   ~580ms    ~100 frames
│   └── _ema_long     (B, 2)   α=0.001  ~5.8s     ~1000 frames
│
├── EMA variance (3 timescales × 2D = 6 tensors)
│   ├── _var_short    (B, 2)
│   ├── _var_medium   (B, 2)
│   └── _var_long     (B, 2)
│
├── Welford online statistics (global)
│   ├── _welford_count  int
│   ├── _welford_mean   (B, 2)
│   └── _welford_m2     (B, 2)
│
├── Markov transition model (8-state)
│   ├── _prev_state           (B,)          int64
│   └── _transition_counts    (B, 8, 8)     float
│
├── Ring buffer (compression progress)
│   ├── _buffer       (B, 50)
│   ├── _buffer_idx   int
│   └── _buffer_count int
│
└── Previous frame cache
    └── _prev_pleasure  (B,)
```

**Tracked features:** Two dimensions from BrainOutput are tracked at each
frame: `pleasure` (D9) and `arousal` (D0). These form the 2D tracked vector.

### 5.2 Online EMA (Short / Medium / Long)

Exponential Moving Averages at three timescales capture the listener's
expectations at different temporal horizons:

```
EMA_t = α * x_t + (1 - α) * EMA_{t-1}
Var_t = α * (x_t - EMA_t)² + (1 - α) * Var_{t-1}
```

| Timescale | Alpha | Effective Window | Musical Correlate |
|-----------|-------|-----------------|-------------------|
| Short | 0.1 | ~10 frames (~58ms) | Beat-level events |
| Medium | 0.01 | ~100 frames (~580ms) | Bar-level patterns |
| Long | 0.001 | ~1000 frames (~5.8s) | Phrase-level trajectories |

Prediction errors are computed as **z-scored deviations** from each EMA,
normalized via tanh and shifted to [0, 1]:

```
PE_timescale = tanh((x - EMA_timescale) / (sqrt(Var_timescale) + eps)) * 0.5 + 0.5
```

Precision is the **inverse variance** at each timescale:

```
precision = 1 / (1 + Var_timescale)
```

### 5.3 Markov Transition Model (8-State)

The pleasure signal is quantized into 8 states (bins 0-7). An 8x8 transition
count matrix accumulates observed state transitions over time:

```
state_t = floor(pleasure * 7).clamp(0, 7)
transition_counts[prev_state, state_t] += 1
```

From this matrix, two key quantities are derived:

- **Surprise** (ε0): Negative log probability of the observed transition,
  normalized by log2(8):

  ```
  surprise = -log2(P(state_t | prev_state)) / log2(8)
  ```

- **Entropy** (ε1): Shannon entropy of the current state's transition
  distribution, normalized by log2(8):

  ```
  entropy = -sum(p * log2(p)) / log2(8)
  ```

The transition count matrix is initialized with uniform counts (1.0) to
provide a Laplace prior, ensuring no zero probabilities at startup.

### 5.4 Welford Global Variance

Welford's online algorithm tracks the **global variance** of the tracked
features across the entire file:

```
count += 1
delta1 = x - mean
mean = mean + delta1 / count
delta2 = x - mean
M2 = M2 + delta1 * delta2
```

This is used for the **familiarity** dimension (ε18): the ratio of local
transition counts to global exposure provides a normalized measure of how
often the current state has been visited.

### 5.5 Ring Buffer for Compression Progress

A ring buffer of size 50 stores recent pleasure values. When the buffer is
full, it is split into two halves (old and new), and the entropy of each half
is compared:

```
compression_progress = sigma((entropy_old - entropy_new) * 5)
```

When the new half has lower entropy than the old half, the listener's internal
model is successfully **compressing** the signal — the Schmidhuber (2009)
definition of learning as reward.

### 5.6 ITPRA Mapping

Epsilon provides a complete mapping to Huron's (2006) ITPRA framework:

| Component | Epsilon Dimension | Formula |
|-----------|-------------------|---------|
| **I** — Imagination | ε11 | EMA_long[pleasure] — long-term pleasure baseline |
| **T** — Tension | ε12 | entropy — uncertainty as tension source |
| **P** — Prediction | ε13 | exp(-|PE_medium| / sigma_medium) — reward for accuracy |
| **R** — Reaction | ε14 | clamp(|PE_medium| * precision_long, 0, 1) — surprise magnitude |
| **A** — Appraisal | ε15 | compression_progress — learning as cognitive appraisal |

### 5.7 Wundt Inverted-U

The Wundt curve (Berlyne 1971) models the inverted-U relationship between
stimulus complexity (here: surprise) and hedonic value:

```
wundt_position = 4 * surprise * (1 - surprise)
```

This parabola peaks at surprise = 0.5, capturing the sweet spot between
boredom (low surprise) and anxiety (high surprise).

### 5.8 Reset Protocol

**Epsilon state MUST be reset between audio files.** The `reset()` method
clears all internal accumulators:

```python
def reset(self) -> None:
    """Clear all internal state. Call between audio files."""
    self._state_initialized = False

# Called via orchestrator:
brain_semantics.reset()  # → calls epsilon.reset()
```

On the next `compute()` call after reset, state is lazily re-initialized for
the new batch size.

---

## 6. Zeta → Eta → Theta Pipeline

The Phase 2 groups form a **linguistic interpretation pipeline**: polarity
axes are quantized into vocabulary terms, which are then structured into
narrative sentences.

### 6.1 Polarity Mapping (ζ)

Each Brain [0, 1] dimension is mapped to [-1, +1] via `2x - 1`. The
exception is `f03_valence`, which is already bipolar [-1, +1] in the Brain
output.

Learning-derived axes (ζ6, ζ7, ζ10) read from specific epsilon output indices:

| Axis | Epsilon Index | Epsilon Dimension |
|------|---------------|-------------------|
| ζ6 novelty | ε[0] | surprise |
| ζ7 complexity | ε[1] | entropy |
| ζ10 stability | ε[6] | precision_long |

### 6.2 Vocabulary Quantization (η)

Each polarity value is quantized from [-1, +1] to one of 64 discrete levels:

```
normalized = (polarity + 1) / 2               # → [0, 1]
grad_index = round(normalized * 63)            # → [0, 63]
band_index = grad_index // 8                   # → [0, 7]
```

The 8 bands map to 8 intensity-graded terms per axis. Total vocabulary:
**12 axes x 8 bands = 96 unique terms**.

#### Complete Vocabulary Catalog

| Axis | Band 0 | Band 1 | Band 2 | Band 3 | Band 4 | Band 5 | Band 6 | Band 7 |
|------|--------|--------|--------|--------|--------|--------|--------|--------|
| **valence** | devastating | melancholic | wistful | subdued | neutral | content | happy | euphoric |
| **arousal** | comatose | lethargic | drowsy | calm | neutral | alert | energized | explosive |
| **tension** | dissolved | slack | easy | mild | neutral | taut | strained | crushing |
| **power** | whisper | fragile | gentle | moderate | neutral | strong | forceful | overwhelming |
| **wanting** | fulfilled | content | settled | mild | neutral | interested | eager | desperate |
| **liking** | aversive | unpleasant | bland | indifferent | neutral | pleasant | delightful | ecstatic |
| **novelty** | habitual | routine | known | expected | neutral | fresh | surprising | shocking |
| **complexity** | trivial | basic | clear | moderate | neutral | elaborate | intricate | labyrinthine |
| **beauty** | harsh | grating | rough | plain | neutral | pleasing | beautiful | sublime |
| **groove** | mechanical | stiff | stilted | measured | neutral | swinging | grooving | transcendent |
| **stability** | turbulent | erratic | unsteady | wavering | neutral | steady | anchored | immovable |
| **engagement** | oblivious | indifferent | distracted | aware | neutral | attentive | immersed | entranced |

### 6.3 Narrative Sentence Structure (θ)

Theta constructs a four-slot sentence template from epsilon and zeta:

```
[Subject] + [Predicate] + [Modifier] + [Connector]
```

**Example generated sentence (conceptual):**

> "Reward [subject=0.65] is rising [predicate=0.8] intensely [modifier=0.7],
> continuing [connector=0.6] the current thread."

Each slot is a probability distribution over its 4 options (via softmax or
normalization), allowing soft blending. The dominant term in each slot can be
selected via argmax for discrete sentence generation.

**Slot derivation summary:**

| Slot | Source | Mechanism |
|------|--------|-----------|
| Subject | Brain (pleasure, tension, arousal, beauty) | softmax(x * 3.0) |
| Predicate | epsilon (pe_short) | threshold-based classification |
| Modifier | Brain (arousal, prediction_error) + epsilon (precision, surprise) | direct mapping |
| Connector | zeta (valence polarity, tension polarity) | algebraic combination |

---

## 7. Summary Table — All 104 Dimensions

| # | Group | Index | Name | Range | Description |
|---|-------|-------|------|-------|-------------|
| 0 | α | α0 | `shared_attribution` | [0, 1] | Shared pathway mean activation |
| 1 | α | α1 | `reward_attribution` | [0, 1] | Reward pathway mean activation |
| 2 | α | α2 | `affect_attribution` | [0, 1] | Affect pathway mean activation |
| 3 | α | α3 | `autonomic_attribution` | [0, 1] | Autonomic pathway mean activation |
| 4 | α | α4 | `computation_certainty` | [0, 1] | Inverse output variance |
| 5 | α | α5 | `bipolar_activation` | [-1, 1] | Net signed direction |
| 6 | β | β0 | `nacc_activation` | [0, 1] | NAcc activation |
| 7 | β | β1 | `caudate_activation` | [0, 1] | Caudate activation |
| 8 | β | β2 | `vta_activation` | [0, 1] | VTA activation |
| 9 | β | β3 | `sn_activation` | [0, 1] | Substantia Nigra activation |
| 10 | β | β4 | `stg_activation` | [0, 1] | STG activation |
| 11 | β | β5 | `ifg_activation` | [0, 1] | IFG activation |
| 12 | β | β6 | `amygdala_activation` | [0, 1] | Amygdala activation |
| 13 | β | β7 | `hippocampus_activation` | [0, 1] | Hippocampus activation |
| 14 | β | β8 | `dopamine_level` | [0, 1] | Striatal DA level |
| 15 | β | β9 | `opioid_level` | [0, 1] | Opioid proxy level |
| 16 | β | β10 | `da_opioid_interaction` | [0, 1] | DA x Opioid interaction |
| 17 | β | β11 | `anticipation_circuit` | [0, 1] | Caudate DA ramp |
| 18 | β | β12 | `consummation_circuit` | [0, 1] | NAcc DA burst |
| 19 | β | β13 | `learning_circuit` | [0, 1] | VTA RPE |
| 20 | γ | γ0 | `reward_intensity` | [0, 1] | Overall reward = pleasure |
| 21 | γ | γ1 | `reward_type` | [0, 1] | Wanting(0) vs Liking(1) |
| 22 | γ | γ2 | `reward_phase` | [0, 1] | Anticipation(0) vs Consummation(1) |
| 23 | γ | γ3 | `itpra_tension_resolution` | [0, 1] | Tension-resolution arc |
| 24 | γ | γ4 | `itpra_surprise_evaluation` | [0, 1] | Surprise-appraisal arc |
| 25 | γ | γ5 | `beauty` | [0, 1] | Opioid-mediated pleasure |
| 26 | γ | γ6 | `sublime` | [0, 1] | Awe/transcendence |
| 27 | γ | γ7 | `groove` | [0, 1] | Motor-harmonic coupling |
| 28 | γ | γ8 | `valence` | [0, 1] | Positive/negative affect |
| 29 | γ | γ9 | `arousal` | [0, 1] | Activation level |
| 30 | γ | γ10 | `chill_probability` | [0, 1] | ANS chill signature |
| 31 | γ | γ11 | `chill_intensity` | [0, 1] | Integrated chill strength |
| 32 | γ | γ12 | `chill_phase` | [0, 1] | Buildup/peak/afterglow |
| 33 | δ | δ0 | `skin_conductance` | [0, 1] | Expected SCR |
| 34 | δ | δ1 | `heart_rate` | [0, 1] | Expected HR change |
| 35 | δ | δ2 | `pupil_diameter` | [0, 1] | Expected pupil dilation |
| 36 | δ | δ3 | `piloerection` | [0, 1] | Expected goosebump prob |
| 37 | δ | δ4 | `fmri_nacc_bold` | [0, 1] | Expected NAcc BOLD |
| 38 | δ | δ5 | `fmri_caudate_bold` | [0, 1] | Expected Caudate BOLD |
| 39 | δ | δ6 | `eeg_frontal_alpha` | [0, 1] | Expected alpha suppression |
| 40 | δ | δ7 | `willingness_to_pay` | [0, 1] | Auction willingness |
| 41 | δ | δ8 | `button_press_rating` | [0, 1] | Continuous rating |
| 42 | δ | δ9 | `wanting_leads_liking` | [0, 1] | Temporal ordering |
| 43 | δ | δ10 | `rpe_latency` | [0, 1] | PE magnitude |
| 44 | δ | δ11 | `refractory_state` | [0, 1] | Inter-chill cooldown |
| 45 | ε | ε0 | `surprise` | [0, 1] | Transition surprisal |
| 46 | ε | ε1 | `entropy` | [0, 1] | State uncertainty |
| 47 | ε | ε2 | `pe_short` | [0, 1] | Short-term PE (~58ms) |
| 48 | ε | ε3 | `pe_medium` | [0, 1] | Medium-term PE (~580ms) |
| 49 | ε | ε4 | `pe_long` | [0, 1] | Long-term PE (~5.8s) |
| 50 | ε | ε5 | `precision_short` | [0, 1] | Short-term confidence |
| 51 | ε | ε6 | `precision_long` | [0, 1] | Long-term confidence |
| 52 | ε | ε7 | `bayesian_surprise` | [0, 1] | Belief update magnitude |
| 53 | ε | ε8 | `information_rate` | [0, 1] | Mutual info past-present |
| 54 | ε | ε9 | `compression_progress` | [0, 1] | Learning as reward |
| 55 | ε | ε10 | `entropy_x_surprise` | [0, 1] | Pleasure predictor |
| 56 | ε | ε11 | `imagination` | [0, 1] | ITPRA-I: long-term baseline |
| 57 | ε | ε12 | `tension_uncertainty` | [0, 1] | ITPRA-T: entropy as tension |
| 58 | ε | ε13 | `prediction_reward` | [0, 1] | ITPRA-P: accuracy reward |
| 59 | ε | ε14 | `reaction_magnitude` | [0, 1] | ITPRA-R: surprise magnitude |
| 60 | ε | ε15 | `appraisal_learning` | [0, 1] | ITPRA-A: compression |
| 61 | ε | ε16 | `reward_pe` | [0, 1] | Reward prediction error |
| 62 | ε | ε17 | `wundt_position` | [0, 1] | Inverted-U optimum |
| 63 | ε | ε18 | `familiarity` | [0, 1] | Exposure accumulation |
| 64 | ζ | ζ0 | `valence` | [-1, +1] | sad - joyful |
| 65 | ζ | ζ1 | `arousal` | [-1, +1] | calm - excited |
| 66 | ζ | ζ2 | `tension` | [-1, +1] | relaxed - tense |
| 67 | ζ | ζ3 | `power` | [-1, +1] | delicate - powerful |
| 68 | ζ | ζ4 | `wanting` | [-1, +1] | satiated - craving |
| 69 | ζ | ζ5 | `liking` | [-1, +1] | displeasure - satisfaction |
| 70 | ζ | ζ6 | `novelty` | [-1, +1] | familiar - novel |
| 71 | ζ | ζ7 | `complexity` | [-1, +1] | simple - complex |
| 72 | ζ | ζ8 | `beauty` | [-1, +1] | discordant - harmonious |
| 73 | ζ | ζ9 | `groove` | [-1, +1] | rigid - flowing |
| 74 | ζ | ζ10 | `stability` | [-1, +1] | chaotic - stable |
| 75 | ζ | ζ11 | `engagement` | [-1, +1] | detached - absorbed |
| 76 | η | η0 | `valence_vocab` | [0, 1] | 64-gradation valence |
| 77 | η | η1 | `arousal_vocab` | [0, 1] | 64-gradation arousal |
| 78 | η | η2 | `tension_vocab` | [0, 1] | 64-gradation tension |
| 79 | η | η3 | `power_vocab` | [0, 1] | 64-gradation power |
| 80 | η | η4 | `wanting_vocab` | [0, 1] | 64-gradation wanting |
| 81 | η | η5 | `liking_vocab` | [0, 1] | 64-gradation liking |
| 82 | η | η6 | `novelty_vocab` | [0, 1] | 64-gradation novelty |
| 83 | η | η7 | `complexity_vocab` | [0, 1] | 64-gradation complexity |
| 84 | η | η8 | `beauty_vocab` | [0, 1] | 64-gradation beauty |
| 85 | η | η9 | `groove_vocab` | [0, 1] | 64-gradation groove |
| 86 | η | η10 | `stability_vocab` | [0, 1] | 64-gradation stability |
| 87 | η | η11 | `engagement_vocab` | [0, 1] | 64-gradation engagement |
| 88 | θ | θ0 | `reward_salience` | [0, 1] | Subject: reward dominates |
| 89 | θ | θ1 | `tension_salience` | [0, 1] | Subject: tension dominates |
| 90 | θ | θ2 | `motion_salience` | [0, 1] | Subject: motion dominates |
| 91 | θ | θ3 | `beauty_salience` | [0, 1] | Subject: beauty dominates |
| 92 | θ | θ4 | `rising` | [0, 1] | Predicate: increasing |
| 93 | θ | θ5 | `peaking` | [0, 1] | Predicate: at climax |
| 94 | θ | θ6 | `falling` | [0, 1] | Predicate: decreasing |
| 95 | θ | θ7 | `stable` | [0, 1] | Predicate: holding steady |
| 96 | θ | θ8 | `intensity` | [0, 1] | Modifier: how strongly |
| 97 | θ | θ9 | `certainty` | [0, 1] | Modifier: how confidently |
| 98 | θ | θ10 | `novelty` | [0, 1] | Modifier: how surprisingly |
| 99 | θ | θ11 | `speed` | [0, 1] | Modifier: how quickly |
| 100 | θ | θ12 | `continuing` | [0, 1] | Connector: same thread |
| 101 | θ | θ13 | `contrasting` | [0, 1] | Connector: opposition |
| 102 | θ | θ14 | `resolving` | [0, 1] | Connector: resolution |
| 103 | θ | θ15 | `transitioning` | [0, 1] | Connector: new section |

---

## 8. References

### Reward and Dopamine

- **Salimpoor, V. N. et al. (2011)**. Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14(2), 257-262. [r_NAcc=0.84, r_Caudate=0.71]
- **Salimpoor, V. N. et al. (2013)**. Interactions between the nucleus accumbens and auditory cortices predict music reward value. *Science*, 340(6129), 216-219.
- **Blood, A. J. & Zatorre, R. J. (2001)**. Intensely pleasurable responses to music correlate with activity in brain regions implicated in reward and emotion. *PNAS*, 98(20), 11818-11823.
- **Berridge, K. C. (2003)**. Pleasures of the brain. *Brain and Cognition*, 52(1), 106-128.
- **Howe, M. W. et al. (2013)**. Prolonged dopamine signalling in striatum signals proximity and value of distant rewards. *Nature*, 500, 575-579.

### Affect and Emotion

- **Russell, J. A. (1980)**. A circumplex model of affect. *Journal of Personality and Social Psychology*, 39(6), 1161-1178.
- **Fritz, T. et al. (2009)**. Universal recognition of three basic emotions in music. *Current Biology*, 19(7), 573-576. [F(2,39)=15.48]
- **Koelsch, S. et al. (2006)**. Investigating emotion with music: An fMRI study. *Human Brain Mapping*, 27(3), 239-250. [t=5.1]
- **Mitterschiffthaler, M. T. et al. (2007)**. A functional MRI study of happy and sad affective states induced by classical music. *Human Brain Mapping*, 28(11), 1150-1162.
- **Konecni, V. J. (2005)**. The aesthetic trinity: Awe, being moved, thrills. *Bulletin of Psychology and the Arts*, 5(2), 27-44.

### Autonomic and Chills

- **de Fleurian, R. & Pearce, M. T. (2021)**. Chills in music: A systematic review. *Psychological Bulletin*, 147(9), 890-920. [k=116, d=0.85]
- **Sloboda, J. A. (1991)**. Music structure and emotional response. *Psychology of Music*, 19(2), 110-120.
- **Guhn, M. et al. (2007)**. Experiencing chills in response to music. *Psychology of Music*, 35(1), 91-110.
- **Grewe, O. et al. (2009)**. The chill parameter. *Music Perception*, 27(1), 61-74.
- **Thayer, J. F. et al. (2009)**. Heart rate variability, prefrontal neural function, and cognitive performance. *Annals of Behavioral Medicine*, 37(2), 141-153.

### Information Theory and Learning

- **Shannon, C. E. (1948)**. A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379-423.
- **Pearce, M. T. (2005)**. The construction and evaluation of statistical models of melodic structure in music perception and composition. PhD Thesis, City University London. [IDyOM]
- **Friston, K. (2010)**. The free-energy principle: A unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138.
- **Itti, L. & Baldi, P. (2009)**. Bayesian surprise attracts human attention. *Vision Research*, 49(10), 1295-1306.
- **Dubnov, S. (2008)**. A unified view of prediction and repetition structure in audio signals with application to interest point detection. *IEEE Transactions on Audio, Speech, and Language Processing*, 16(2), 327-337.
- **Schmidhuber, J. (2009)**. Simple algorithmic theory of subjective beauty, novelty, surprise, interestingness, attention, curiosity, creativity, art, science, music, jokes. *JAGI*, 1, 1-32.
- **Cheung, V. K. M. et al. (2019)**. Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092.
- **Gold, B. P. et al. (2019)**. Musical reward prediction errors engage the nucleus accumbens and motivate learning. *PNAS*, 116(8), 3310-3315.
- **Koelsch, S. et al. (2019)**. Predictive processes and the peculiar case of music. *Trends in Cognitive Sciences*, 23(1), 63-77.

### ITPRA and Expectation

- **Huron, D. (2006)**. *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press.
- **Meyer, L. B. (1956)**. *Emotion and Meaning in Music*. University of Chicago Press.

### Aesthetics and Flow

- **Berlyne, D. E. (1971)**. *Aesthetics and Psychobiology*. Appleton-Century-Crofts.
- **Zajonc, R. B. (1968)**. Attitudinal effects of mere exposure. *Journal of Personality and Social Psychology*, 9(2), 1-27.
- **Janata, P. et al. (2012)**. Sensorimotor coupling in music and the psychology of the groove. *Journal of Experimental Psychology: General*, 141(1), 54-75.
- **Csikszentmihalyi, M. (1990)**. *Flow: The Psychology of Optimal Experience*. Harper & Row.

### Neuroscience (General)

- **Fong, C. Y. et al. (2020)**. Bayesian surprise in reward prediction error signaling. *eLife*, 9, e59834.
- **Kim, S. G. et al. (2021)**. Musical anticipation involves the motor cortex. *NeuroImage*, 234, 117988.
- **Sachs, M. E. et al. (2025)**. The neuroscience of music-evoked emotions. *Annual Review of Psychology*.
- **Yang, J. et al. (2025)**. Neural arousal patterns during continuous music listening. *Nature Human Behaviour*.
- **Ding, N. et al. (2025)**. Hierarchical temporal processing of musical structure. *Cerebral Cortex*.
- **Sammler, D. et al. (2007)**. Music and emotion: Electrophysiological correlates. *Psychophysiology*, 44(2), 293-304.
- **Laeng, B. et al. (2012)**. Pupillary responses to emotional music. *Cognition & Emotion*, 26(4), 589-606.

### Semantics and Linguistics

- **Osgood, C. E. et al. (1957)**. *The Measurement of Meaning*. University of Illinois Press.
- **Rosch, E. (1975)**. Cognitive representations of semantic categories. *Journal of Experimental Psychology: General*, 104(3), 192-233.
- **Halliday, M. A. K. & Hasan, R. (1976)**. *Cohesion in English*. Longman.
- **Caplin, W. E. (1998)**. *Classical Form*. Oxford University Press.
- **Almen, B. (2008)**. *A Theory of Musical Narrative*. Indiana University Press.
- **Schubert, E. (2004)**. Modeling perceived emotion with continuous musical features. *Music Perception*, 21(4), 561-585.
- **Gabrielsson, A. (2001)**. Emotions in strong experiences with music. In P. N. Juslin & J. A. Sloboda (Eds.), *Music and Emotion*. Oxford University Press.
- **Stevens, S. S. (1957)**. On the psychophysical law. *Psychological Review*, 64(3), 153-181.

### Music Theory and Analysis

- **Brattico, E. et al. (2011)**. The neuroaesthetics of music. *Psychology of Aesthetics, Creativity, and the Arts*, 5(1), 2-19.
- **Ferreri, L. et al. (2019)**. Dopamine modulates the reward experiences elicited by music. *PNAS*, 116(9), 3793-3798.
- **Peng, H. et al. (2022)**. Co-activation of autonomic nervous system during music-evoked chills. *Psychophysiology*, 59(6), e14020.
- **Fancourt, A. et al. (2020)**. Dynamics of emotional responses to music. *Music Perception*, 37(4), 317-332.

---

## Navigation

- Back to: [00-INDEX.md](../General/00-INDEX.md)
- See also: [Architecture/representation-space.md](../Architecture/representation-space.md)
- Replaces: [L³-SRP-SEMANTIC-SPACE.md](L³-SRP-SEMANTIC-SPACE.md) | [L³-AAC-SEMANTIC-SPACE.md](L³-AAC-SEMANTIC-SPACE.md) | [L³-VMM-SEMANTIC-SPACE.md](L³-VMM-SEMANTIC-SPACE.md)

---

*v2.0.0 — 2026-02-12 — Unified Brain Semantic Space (104D)*
