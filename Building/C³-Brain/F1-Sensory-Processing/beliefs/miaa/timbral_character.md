# timbral_character — Core Belief

**Category**: Core (full Bayesian PE cycle)
**Function**: F1 (Sensory Processing)
**Mechanism**: MIAA (Musical Imagery Auditory Activation)
**τ**: 0.5 (moderate — timbre character changes slowly)

---

## Definition

> "I recognize this timbre / warm vs bright."

## Observe Formula

```
observe = 0.50 × P0:melody_retrieval
        + 0.30 × E0:imagery_activation
        + 0.20 × M1:familiarity_effect
```

| Source Dim | MIAA Index | Weight | Rationale |
|-----------|-----------|--------|-----------|
| P0:melody_retrieval | 5 | 0.50 | Primary template retrieval signal |
| E0:imagery_activation | 0 | 0.30 | AC activation drives timbre processing |
| M1:familiarity_effect | 4 | 0.20 | Familiar timbres are recognized more strongly |

Weights sum to 1.0.

## Predict Formula

```
predict = τ × prev + (1 − τ) × baseline
        + 0.04 × tonalness_mean
        + 0.03 × spectral_auto_mean
        + 0.03 × imagery_recognition
```

| Source | H³ Tuple / Context | Weight | Rationale |
|--------|-------------------|--------|-----------|
| tonalness_mean | (14, 5, 1, 0) | 0.04 | Slow-changing tonal quality → timbre continuity |
| spectral_auto_mean | (17, 8, 1, 0) | 0.03 | Timbral periodicity proxy |
| imagery_recognition | context belief | 0.03 | Forward-looking recognition context |

---

## Dependency Chain

```
R³/H³ → MIAA (Depth 0, Relay) → timbral_character
```

No upstream mechanism dependency. MIAA reads R³/H³ directly.

---

## Downstream Consumers

- F2 (Prediction/HTP): Timbre character feeds harmonic prediction context
- F3 (Salience): Strong timbre recognition = salient event
- F6 (Reward): PE from timbral_character feeds reward formula
- F4 (Memory): Timbre character → recurrence tracking

## Implementation

File: `Musical_Intelligence/brain/functions/f1/beliefs/miaa/timbral_character.py`
