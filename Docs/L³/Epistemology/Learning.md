# L³ Epistemology — Learning

**Level**: 5 (ε)
**Question**: HOW does the listener learn?
**Audience**: Information theorists, computational musicologists
**Version**: 2.1.0
**Updated**: 2026-02-13

---

## Overview

The Learning group is the most complex epistemological level and the **only stateful group** in L³. While α-δ treat each frame independently, ε accumulates knowledge across time — tracking what the listener has heard, what they expect, and how those expectations evolve.

Epsilon produces 19 dimensions across 7 subcategories: Surprise & Entropy (2), Prediction Errors (3), Precision (2), Information Dynamics (3), Interaction (1), ITPRA Mapping (5), and Reward & Aesthetics (3).

---

## Why Statefulness Is Necessary

Music is fundamentally temporal. A chord that surprises on first hearing becomes expected after repetition. A melody that bores a naive listener may delight an experienced one. These phenomena cannot be captured by stateless computation — they require memory.

ε maintains internal state (EMA accumulators, transition matrices, entropy history) that updates at every frame. This makes ε the only group that produces different output for the same input depending on what came before. The architectural consequence is that ε must be computed in Phase 1b (after the independent groups but before the dependent groups that consume its output).

---

## Predictive Coding Framework

The theoretical backbone of ε is Friston's (2010) **free energy principle**: the brain is a prediction machine that continuously generates expectations about incoming sensory data, then updates those expectations when they are violated. Musical pleasure arises partly from this process — the interplay between prediction and surprise.

ε implements predictive coding through three mechanisms:
1. **Expectation formation** via exponential moving averages (EMA)
2. **Prediction error** as the difference between expected and observed
3. **Precision-weighting** to modulate the influence of prediction errors

---

## Statistical Learning (EMA at 3 Timescales)

The listener forms expectations at three temporal scales, each implemented as an EMA with a different smoothing parameter:

| Timescale | α (smoothing) | Time Constant | Musical Parallel | Citation |
|-----------|:-------------:|:-------------:|-----------------|----------|
| Short | 0.1 | ~58ms | Note-to-note transitions | Koelsch 2019 |
| Medium | 0.01 | ~580ms | Phrase-level patterns | Koelsch 2019 |
| Long | 0.001 | ~5.8s | Section-level structure | Koelsch 2019 |

Each EMA tracks a running estimate of the Brain's output. The prediction error at each timescale is the absolute difference between the EMA and the current observation.

This multi-scale approach follows IDyOM (Pearce 2005), which models auditory expectations using multiple statistical models at different temporal granularities. The key insight from Pearce is that listeners simultaneously track local and global regularities — a surprising note within an expected phrase is processed differently from an expected note within a surprising phrase.

---

## Prediction Errors (3D)

| Local | Name | Timescale | Formula | Citation |
|:-----:|------|-----------|---------|----------|
| ε2 | `pe_short` | ~58ms | \|obs - EMA_short\| | Koelsch 2019 |
| ε3 | `pe_medium` | ~580ms | \|obs - EMA_medium\| | Koelsch 2019 |
| ε4 | `pe_long` | ~5.8s | \|obs - EMA_long\| | Koelsch 2019 |

Prediction error is the fundamental currency of learning. Large PE means the model was surprised; small PE means the event was expected. The three timescales allow ε to distinguish between local surprise (an unexpected note) and global surprise (an unexpected section change).

---

## Precision (2D)

| Local | Name | Formula | Citation |
|:-----:|------|---------|----------|
| ε5 | `precision_short` | 1 / (1 + Var_short) | Friston 2010 |
| ε6 | `precision_long` | 1 / (1 + Var_long) | Friston 2010 |

Precision is the inverse of variance — a measure of how reliable the prediction errors are. When the environment is stable (low variance), precision is high and prediction errors carry more weight. When the environment is chaotic (high variance), precision drops and prediction errors are discounted.

This directly implements Friston's (2010) precision-weighting: the brain does not treat all prediction errors equally. It weights them by the estimated reliability of the context.

---

## Information-Theoretic Measures (3D)

### Shannon Entropy (ε1)

```
entropy = -sum(p * log(p)) / log(N)
```

Normalized Shannon entropy over the 8-state Markov model. High entropy means the listener cannot predict which state comes next (maximum uncertainty). Low entropy means the music is predictable.

### Bayesian Surprise (ε7)

```
bayesian_surprise = σ(|PE_med| × precision_long × 5)
```

Itti & Baldi (2009) defined Bayesian surprise as the KL divergence between prior and posterior beliefs after observing data. ε7 approximates this: large prediction error combined with high precision (the model was confident but wrong) produces maximum surprise.

### Information Rate (ε8)

```
information_rate = entropy × (1 - autocorrelation)
```

Dubnov (2008) proposed information rate as a measure of musical interest — how much new information the signal provides per unit time. High entropy alone is not enough (random noise has high entropy but is not interesting). Information rate also requires low autocorrelation (the information must be genuinely new, not repetitive).

### Compression Progress (ε9)

```
compression_progress = σ((H_old - H_new) × 5)
```

Schmidhuber (2009) argued that the intrinsic reward of learning is **compression progress** — the reduction in the model's entropy over time. When the listener discovers a pattern that reduces uncertainty, compression progress is positive. This is the "aha!" moment formalized as information theory.

---

## Surprise (ε0) and the Markov Model

ε0 (`surprise`) is the negative log probability of the current state transition under an 8-state Markov model:

```
surprise = -log(P(state_t | state_{t-1}))
```

The 8 quantized states partition the Brain's output into discrete categories. The Markov transition matrix is updated online as the listener encounters new transitions, implementing statistical learning. Initially, all transitions are equally likely (uniform prior). Over time, the matrix concentrates on observed transitions, reducing surprise for repeated patterns.

This design is inspired by IDyOM (Pearce 2005), which uses variable-order Markov models to predict melodic sequences. ε simplifies this to a first-order model over quantized Brain states, trading expressive power for computational efficiency.

---

## Interaction: Entropy x Surprise (ε10)

```
entropy_x_surprise = entropy × surprise
```

Cheung et al. (2019) found that musical pleasure peaks when surprise is high but uncertainty (entropy) is also high — that is, when the listener is in a state of genuine not-knowing and then receives a surprising event. The product of entropy and surprise captures this interaction.

This explains why the same surprise has different hedonic impact depending on context: a surprising chord in a predictable passage (low entropy) is less pleasurable than the same surprise in an uncertain passage (high entropy).

---

## ITPRA Mapping (5D)

ε maps the learning dynamics onto Huron's (2006) five-stage expectation framework:

| Local | ITPRA Stage | Source | Description |
|:-----:|:-----------:|--------|-------------|
| ε11 | Imagination (I) | EMA_long | Long-term expectation = what the listener imagines will happen |
| ε12 | Tension (T) | entropy | Uncertainty = how tense the listener is about what comes next |
| ε13 | Prediction (P) | 1 - surprise | Accuracy = how correct the prediction was |
| ε14 | Reaction (R) | \|PE_short\| | Fast response = immediate reaction to the event |
| ε15 | Appraisal (A) | compression_progress | Slow evaluation = did the listener learn something? |

This mapping makes the connection between information theory and music psychology explicit. Huron's framework was originally qualitative; ε provides quantitative formulas for each stage.

---

## Reward & Aesthetics (3D)

### Reward Prediction Error (ε16)

```
reward_pe = σ(pleasure_observed - pleasure_expected)
```

Gold et al. (2019) showed that reward prediction error — not absolute reward — drives dopamine release during music. ε16 captures the difference between how rewarding a moment is and how rewarding the listener expected it to be.

### Wundt Inverted-U (ε17)

```
wundt_position = 4 × surprise × (1 - surprise)
```

Berlyne (1971) proposed that aesthetic pleasure follows an inverted-U relationship with complexity: too simple is boring, too complex is overwhelming, and optimal complexity is maximally pleasurable. The Wundt curve formalizes this. ε17 computes the listener's position on this curve using surprise as a proxy for complexity.

The formula `4x(1-x)` maps [0,1] onto an inverted parabola peaking at x = 0.5. Moderate surprise is maximally aesthetic.

### Familiarity (ε18)

```
familiarity = log(transition_count) / log(total_transitions)
```

Zajonc's (1968) **mere exposure effect** holds that familiarity breeds liking (up to a point). ε18 tracks how familiar the current musical state is by counting how often this transition has been observed relative to total transitions. Familiarity accumulates over time — a genuinely stateful quantity.

---

## Key Citations

- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138.
- Pearce, M.T. (2005). *The Construction and Evaluation of Statistical Models of Melodic Structure in Music Perception and Composition*. PhD thesis, City University London.
- Schmidhuber, J. (2009). Simple algorithmic theory of subjective beauty, novelty, surprise, interestingness, attention, curiosity, creativity, art, science, music, jokes. *JAGI*, 1(1), 41-53.
- Itti, L. & Baldi, P. (2009). Bayesian surprise attracts human attention. *Vision Research*, 49(10), 1295-1306.
- Dubnov, S. (2008). Unified view of prediction and repetition structure in audio signals with application to interest in music. *IEEE TASLP*, 16(2), 515-525.
- Cheung, V.K.M., Harrison, P.M.C., Meyer, L., Pearce, M.T., Haynes, J.D., & Koelsch, S. (2019). Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. *Current Biology*, 29(23), 4084-4092.
- Gold, B.P., Pearce, M.T., Mas-Herrero, E., Dagher, A., & Bhagwati, R. (2019). Predictability and uncertainty in the pleasure of music. *Current Biology*, 29(23), 4084-4092.
- Koelsch, S., Vuust, P., & Friston, K. (2019). Predictive processes and the peculiar case of music. *Trends in Cognitive Sciences*, 23(1), 63-77.
- Huron, D. (2006). *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press.
- Berlyne, D.E. (1971). *Aesthetics and Psychobiology*. Appleton-Century-Crofts.
- Zajonc, R.B. (1968). Attitudinal effects of mere exposure. *JPSP Monograph Supplement*, 9(2), 1-27.
- Shannon, C.E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27, 379-423.

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [Groups/Independent/Epsilon.md](../Groups/Independent/Epsilon.md) for implementation details | [Registry/DimensionCatalog.md](../Registry/DimensionCatalog.md) for dimension metadata | [Pipeline/StateManagement.md](../Pipeline/StateManagement.md) for state lifecycle
