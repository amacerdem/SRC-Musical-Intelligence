# L³ Dimension Catalog

**Scope**: Complete inventory of all 104 L³ semantic dimensions with global index, group, name, range, formula, and primary citation.

---

## α — Computation Semantics (6D) [0:6]

| Global | Local | Name | Range | Formula | Citation |
|:------:|:-----:|------|:-----:|---------|----------|
| 0 | α0 | `shared_attribution` | [0, 1] | mean(Brain[0:4]) | White-box attribution |
| 1 | α1 | `reward_attribution` | [0, 1] | mean(Brain[4:13]) | White-box attribution |
| 2 | α2 | `affect_attribution` | [0, 1] | mean(Brain[13:19]) | White-box attribution |
| 3 | α3 | `autonomic_attribution` | [0, 1] | mean(Brain[19:24]) | White-box attribution |
| 4 | α4 | `computation_certainty` | [0, 1] | 1 / (1 + Var(Brain[0:26])) | Bayesian precision |
| 5 | α5 | `bipolar_activation` | [-1, 1] | 0.5 * (prediction_error + f03_valence) | Signed summary |

## β — Neuroscience Semantics (14D) [6:20]

### Brain Regions (8D)

| Global | Local | Name | Range | Region | Citation |
|:------:|:-----:|------|:-----:|--------|----------|
| 6 | β0 | `nacc_activation` | [0, 1] | Nucleus Accumbens | Salimpoor 2011 |
| 7 | β1 | `caudate_activation` | [0, 1] | Caudate Nucleus | Salimpoor 2011 |
| 8 | β2 | `vta_activation` | [0, 1] | Ventral Tegmental Area | Howe 2013 |
| 9 | β3 | `sn_activation` | [0, 1] | Substantia Nigra | Howe 2013 |
| 10 | β4 | `stg_activation` | [0, 1] | Superior Temporal Gyrus | Kim 2021 |
| 11 | β5 | `ifg_activation` | [0, 1] | Inferior Frontal Gyrus | Fong 2020 |
| 12 | β6 | `amygdala_activation` | [0, 1] | Amygdala | Koelsch 2006 |
| 13 | β7 | `hippocampus_activation` | [0, 1] | Hippocampus | Sachs 2025 |

### Neurotransmitter Dynamics (3D)

| Global | Local | Name | Range | System | Citation |
|:------:|:-----:|------|:-----:|--------|----------|
| 14 | β8 | `dopamine_level` | [0, 1] | Striatal DA: (NAcc + Caudate) / 2 | Salimpoor 2011 |
| 15 | β9 | `opioid_level` | [0, 1] | Endogenous opioid proxy | Blood & Zatorre 2001 |
| 16 | β10 | `da_opioid_interaction` | [0, 1] | DA × Opioid interaction | Berridge 2003 |

### Circuit States (3D)

| Global | Local | Name | Range | Circuit | Citation |
|:------:|:-----:|------|:-----:|---------|----------|
| 17 | β11 | `anticipation_circuit` | [0, 1] | Caudate → DA ramp (wanting) | Salimpoor 2011 |
| 18 | β12 | `consummation_circuit` | [0, 1] | NAcc → DA burst (liking) | Salimpoor 2011 |
| 19 | β13 | `learning_circuit` | [0, 1] | VTA → RPE (\|prediction_error\|) | Fong 2020 |

## γ — Psychology Semantics (13D) [20:33]

### Reward (3D)

| Global | Local | Name | Range | Description | Citation |
|:------:|:-----:|------|:-----:|-------------|----------|
| 20 | γ0 | `reward_intensity` | [0, 1] | Overall reward = pleasure | Salimpoor 2011 |
| 21 | γ1 | `reward_type` | [0, 1] | Wanting(0) vs Liking(1) | Berridge 2003 |
| 22 | γ2 | `reward_phase` | [0, 1] | Anticipation(0) vs Consummation(1) | Salimpoor 2011 |

### ITPRA (2D)

| Global | Local | Name | Range | Description | Citation |
|:------:|:-----:|------|:-----:|-------------|----------|
| 23 | γ3 | `itpra_tension_resolution` | [0, 1] | (1 - tension) × harmonic_context | Huron 2006 |
| 24 | γ4 | `itpra_surprise_evaluation` | [0, 1] | \|prediction_error\| × emotional_arc | Huron 2006 |

### Aesthetics (3D)

| Global | Local | Name | Range | Description | Citation |
|:------:|:-----:|------|:-----:|-------------|----------|
| 25 | γ5 | `beauty` | [0, 1] | Opioid-mediated hedonic pleasure | Blood & Zatorre 2001 |
| 26 | γ6 | `sublime` | [0, 1] | Awe/transcendence: pleasure × arousal | Konecni 2005 |
| 27 | γ7 | `groove` | [0, 1] | Motor-harmonic coupling: arousal × harmonic_context | Janata 2012 |

### Emotion (2D)

| Global | Local | Name | Range | Description | Citation |
|:------:|:-----:|------|:-----:|-------------|----------|
| 28 | γ8 | `valence` | [0, 1] | Positive/negative affect: (f03_valence + 1) / 2 | Russell 1980 |
| 29 | γ9 | `arousal` | [0, 1] | Activation level | Yang 2025 |

### Chills (3D)

| Global | Local | Name | Range | Description | Citation |
|:------:|:-----:|------|:-----:|-------------|----------|
| 30 | γ10 | `chill_probability` | [0, 1] | ANS chill signature: SCR × (1 - HR) | de Fleurian & Pearce 2021 |
| 31 | γ11 | `chill_intensity` | [0, 1] | Integrated chill strength | Sloboda 1991 |
| 32 | γ12 | `chill_phase` | [0, 1] | Buildup/peak/afterglow: σ(chills - tension) | Grewe 2009 |

## δ — Validation Semantics (12D) [33:45]

### Physiological (4D)

| Global | Local | Name | Range | Measure | Citation |
|:------:|:-----:|------|:-----:|---------|----------|
| 33 | δ0 | `skin_conductance` | [0, 1] | Expected SCR signal | de Fleurian & Pearce 2021 |
| 34 | δ1 | `heart_rate` | [0, 1] | Expected HR change | Thayer 2009 |
| 35 | δ2 | `pupil_diameter` | [0, 1] | Expected pupil dilation: arousal × \|PE\| | Laeng 2012 |
| 36 | δ3 | `piloerection` | [0, 1] | Expected goosebump probability | Sloboda 1991 |

### Neural (3D)

| Global | Local | Name | Range | Measure | Citation |
|:------:|:-----:|------|:-----:|---------|----------|
| 37 | δ4 | `fmri_nacc_bold` | [0, 1] | Expected NAcc BOLD signal | Salimpoor 2011 |
| 38 | δ5 | `fmri_caudate_bold` | [0, 1] | Expected Caudate BOLD signal | Salimpoor 2011 |
| 39 | δ6 | `eeg_frontal_alpha` | [0, 1] | Expected alpha suppression: 1 - pleasure | Sammler 2007 |

### Behavioral (2D)

| Global | Local | Name | Range | Measure | Citation |
|:------:|:-----:|------|:-----:|---------|----------|
| 40 | δ7 | `willingness_to_pay` | [0, 1] | Salimpoor 2013 auction paradigm | Salimpoor 2013 |
| 41 | δ8 | `button_press_rating` | [0, 1] | Continuous pleasure rating | Schubert 2004 |

### Temporal Constraints (3D)

| Global | Local | Name | Range | Constraint | Citation |
|:------:|:-----:|------|:-----:|------------|----------|
| 42 | δ9 | `wanting_leads_liking` | [0, 1] | σ(da_caudate - da_nacc) | Salimpoor 2011 |
| 43 | δ10 | `rpe_latency` | [0, 1] | \|prediction_error\| | Fong 2020 |
| 44 | δ11 | `refractory_state` | [0, 1] | 1 - chills_intensity | Grewe 2009 |

## ε — Learning Dynamics (19D, STATEFUL) [45:64]

### Surprise & Entropy (2D)

| Global | Local | Name | Range | Description | Citation |
|:------:|:-----:|------|:-----:|-------------|----------|
| 45 | ε0 | `surprise` | [0, 1] | Transition surprisal (8-state Markov) | Pearce 2005 |
| 46 | ε1 | `entropy` | [0, 1] | State uncertainty: normalized Shannon entropy | Shannon 1948 |

### Prediction Errors (3D)

| Global | Local | Name | Range | Description | Citation |
|:------:|:-----:|------|:-----:|-------------|----------|
| 47 | ε2 | `pe_short` | [0, 1] | Short-term PE (~58ms, α=0.1) | Koelsch 2019 |
| 48 | ε3 | `pe_medium` | [0, 1] | Medium-term PE (~580ms, α=0.01) | Koelsch 2019 |
| 49 | ε4 | `pe_long` | [0, 1] | Long-term PE (~5.8s, α=0.001) | Koelsch 2019 |

### Precision (2D)

| Global | Local | Name | Range | Description | Citation |
|:------:|:-----:|------|:-----:|-------------|----------|
| 50 | ε5 | `precision_short` | [0, 1] | Short-term confidence: 1 / (1 + Var_short) | Friston 2010 |
| 51 | ε6 | `precision_long` | [0, 1] | Long-term confidence: 1 / (1 + Var_long) | Friston 2010 |

### Information Dynamics (3D)

| Global | Local | Name | Range | Description | Citation |
|:------:|:-----:|------|:-----:|-------------|----------|
| 52 | ε7 | `bayesian_surprise` | [0, 1] | Belief update: σ(\|PE_med\| × prec_long × 5) | Itti & Baldi 2009 |
| 53 | ε8 | `information_rate` | [0, 1] | Mutual info: entropy × (1 - autocorr) | Dubnov 2008 |
| 54 | ε9 | `compression_progress` | [0, 1] | Learning as reward: σ((H_old - H_new) × 5) | Schmidhuber 2009 |

### Interaction (1D)

| Global | Local | Name | Range | Description | Citation |
|:------:|:-----:|------|:-----:|-------------|----------|
| 55 | ε10 | `entropy_x_surprise` | [0, 1] | Pleasure predictor: entropy × surprise | Cheung et al. 2019 |

### ITPRA Mapping (5D)

| Global | Local | Name | Range | ITPRA | Citation |
|:------:|:-----:|------|:-----:|:-----:|----------|
| 56 | ε11 | `imagination` | [0, 1] | I | Huron 2006 |
| 57 | ε12 | `tension_uncertainty` | [0, 1] | T | Huron 2006 |
| 58 | ε13 | `prediction_reward` | [0, 1] | P | Huron 2006 |
| 59 | ε14 | `reaction_magnitude` | [0, 1] | R | Huron 2006 |
| 60 | ε15 | `appraisal_learning` | [0, 1] | A | Huron 2006 |

### Reward & Aesthetics (3D)

| Global | Local | Name | Range | Description | Citation |
|:------:|:-----:|------|:-----:|-------------|----------|
| 61 | ε16 | `reward_pe` | [0, 1] | Reward prediction error | Gold et al. 2019 |
| 62 | ε17 | `wundt_position` | [0, 1] | Inverted-U: 4 × surprise × (1 - surprise) | Berlyne 1971 |
| 63 | ε18 | `familiarity` | [0, 1] | Exposure accumulation: log(trans) / log(total) | Zajonc 1968 |

## ζ — Polarity (12D, Bipolar) [64:76]

| Global | Local | Name | Neg Pole | Pos Pole | Range | Source | Citation |
|:------:|:-----:|------|----------|----------|:-----:|--------|----------|
| 64 | ζ0 | `valence` | sad | joyful | [-1, +1] | f03_valence | Russell 1980 |
| 65 | ζ1 | `arousal` | calm | excited | [-1, +1] | 2 × arousal - 1 | Yang 2025 |
| 66 | ζ2 | `tension` | relaxed | tense | [-1, +1] | 2 × tension - 1 | Huron 2006 |
| 67 | ζ3 | `power` | delicate | powerful | [-1, +1] | 2 × ans_composite - 1 | Osgood 1957 |
| 68 | ζ4 | `wanting` | satiated | craving | [-1, +1] | 2 × wanting - 1 | Berridge 2003 |
| 69 | ζ5 | `liking` | displeasure | satisfaction | [-1, +1] | 2 × liking - 1 | Berridge 2003 |
| 70 | ζ6 | `novelty` | familiar | novel | [-1, +1] | 2 × ε[0] - 1 | Berlyne 1971 |
| 71 | ζ7 | `complexity` | simple | complex | [-1, +1] | 2 × ε[1] - 1 | Berlyne 1971 |
| 72 | ζ8 | `beauty` | discordant | harmonious | [-1, +1] | 2 × beauty - 1 | Blood & Zatorre 2001 |
| 73 | ζ9 | `groove` | rigid | flowing | [-1, +1] | 2 × (harm_ctx × arousal) - 1 | Janata 2012 |
| 74 | ζ10 | `stability` | chaotic | stable | [-1, +1] | 2 × ε[6] - 1 | Friston 2010 |
| 75 | ζ11 | `engagement` | detached | absorbed | [-1, +1] | 2 × (pleasure × arousal) - 1 | Csikszentmihalyi 1990 |

## η — Vocabulary (12D, 64-Gradation) [76:88]

| Global | Local | Name | Range | Quantization | Axis |
|:------:|:-----:|------|:-----:|-------------|------|
| 76 | η0 | `valence_vocab` | [0, 1] | round((ζ0+1)/2 × 63) / 63 | valence |
| 77 | η1 | `arousal_vocab` | [0, 1] | round((ζ1+1)/2 × 63) / 63 | arousal |
| 78 | η2 | `tension_vocab` | [0, 1] | round((ζ2+1)/2 × 63) / 63 | tension |
| 79 | η3 | `power_vocab` | [0, 1] | round((ζ3+1)/2 × 63) / 63 | power |
| 80 | η4 | `wanting_vocab` | [0, 1] | round((ζ4+1)/2 × 63) / 63 | wanting |
| 81 | η5 | `liking_vocab` | [0, 1] | round((ζ5+1)/2 × 63) / 63 | liking |
| 82 | η6 | `novelty_vocab` | [0, 1] | round((ζ6+1)/2 × 63) / 63 | novelty |
| 83 | η7 | `complexity_vocab` | [0, 1] | round((ζ7+1)/2 × 63) / 63 | complexity |
| 84 | η8 | `beauty_vocab` | [0, 1] | round((ζ8+1)/2 × 63) / 63 | beauty |
| 85 | η9 | `groove_vocab` | [0, 1] | round((ζ9+1)/2 × 63) / 63 | groove |
| 86 | η10 | `stability_vocab` | [0, 1] | round((ζ10+1)/2 × 63) / 63 | stability |
| 87 | η11 | `engagement_vocab` | [0, 1] | round((ζ11+1)/2 × 63) / 63 | engagement |

## θ — Narrative (16D) [88:104]

### Subject (4D)

| Global | Local | Name | Range | Slot | Citation |
|:------:|:-----:|------|:-----:|------|----------|
| 88 | θ0 | `reward_salience` | [0, 1] | Reward dominates | Salimpoor 2011 |
| 89 | θ1 | `tension_salience` | [0, 1] | Tension dominates | Huron 2006 |
| 90 | θ2 | `motion_salience` | [0, 1] | Motion dominates | Yang 2025 |
| 91 | θ3 | `beauty_salience` | [0, 1] | Beauty dominates | Blood & Zatorre 2001 |

### Predicate (4D)

| Global | Local | Name | Range | Slot | Citation |
|:------:|:-----:|------|:-----:|------|----------|
| 92 | θ4 | `rising` | [0, 1] | Increasing | Schubert 2004 |
| 93 | θ5 | `peaking` | [0, 1] | At climax | Sloboda 1991 |
| 94 | θ6 | `falling` | [0, 1] | Decreasing | Schubert 2004 |
| 95 | θ7 | `stable` | [0, 1] | Holding steady | Meyer 1956 |

### Modifier (4D)

| Global | Local | Name | Range | Slot | Citation |
|:------:|:-----:|------|:-----:|------|----------|
| 96 | θ8 | `intensity` | [0, 1] | How strongly | Gabrielsson 2001 |
| 97 | θ9 | `certainty` | [0, 1] | How confidently | Friston 2010 |
| 98 | θ10 | `novelty` | [0, 1] | How surprisingly | Berlyne 1971 |
| 99 | θ11 | `speed` | [0, 1] | How quickly | Fong 2020 |

### Connector (4D)

| Global | Local | Name | Range | Slot | Citation |
|:------:|:-----:|------|:-----:|------|----------|
| 100 | θ12 | `continuing` | [0, 1] | Same thread | Halliday & Hasan 1976 |
| 101 | θ13 | `contrasting` | [0, 1] | Opposition | Almen 2008 |
| 102 | θ14 | `resolving` | [0, 1] | Resolution | Huron 2006 |
| 103 | θ15 | `transitioning` | [0, 1] | New section | Caplin 1998 |

---

**Total**: 104 dimensions (6 + 14 + 13 + 12 + 19 + 12 + 12 + 16)
**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [GroupMap.md](GroupMap.md) for group-level overview
