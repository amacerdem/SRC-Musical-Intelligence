# Psychometric Alignment

Alignment of L³ semantic dimensions with established psychometric instruments.

## Russell Circumplex Model (1980)

The two-dimensional affect space maps directly to L³ polarity axes:

| Circumplex Dim | L³ Axis | L³ Index |
|----------------|---------|----------|
| Valence | ζ.valence | ζ0 |
| Arousal | ζ.arousal | ζ1 |

Quadrant mapping:

| Quadrant | Valence | Arousal | L³ Vocabulary |
|----------|---------|---------|---------------|
| Q1: Excited-Happy | + | + | happy + energized |
| Q2: Distressed-Angry | − | + | melancholic + explosive |
| Q3: Sad-Depressed | − | − | devastating + comatose |
| Q4: Calm-Content | + | − | content + calm |

## Osgood Semantic Differential (EPA, 1957)

The three-factor model maps to L³:

| EPA Factor | L³ Axis | L³ Index | Interpretation |
|------------|---------|----------|----------------|
| Evaluation | ζ.valence | ζ0 | Good ↔ Bad → joyful ↔ sad |
| Potency | ζ.power | ζ3 | Strong ↔ Weak → powerful ↔ delicate |
| Activity | ζ.arousal | ζ1 | Active ↔ Passive → excited ↔ calm |

## GEMS — Geneva Emotional Music Scale (Zentner et al., 2008)

9-factor alignment:

| GEMS Factor | Primary L³ Axis | Secondary | Coverage |
|-------------|----------------|-----------|----------|
| Wonder | ζ.beauty | ζ.novelty | Full |
| Transcendence | γ.sublime | ζ.beauty | Full |
| Tenderness | ζ.valence (+) | ζ.power (−) | Partial |
| Nostalgia | ε.familiarity | ζ.valence | Partial |
| Peacefulness | ζ.tension (−) | ζ.arousal (−) | Full |
| Power | ζ.power (+) | ζ.arousal (+) | Full |
| Joyful Activation | ζ.valence (+) | ζ.arousal (+) | Full |
| Tension | ζ.tension (+) | ε.entropy | Full |
| Sadness | ζ.valence (−) | ζ.arousal (−) | Full |

Coverage: 9/9 GEMS factors have L³ representation. 7/9 fully covered.

## ITPRA Framework (Huron, 2006)

Direct implementation in ε group:

| ITPRA Stage | L³ Dimension | L³ Index | Formula |
|-------------|-------------|----------|---------|
| Imagination | ε.imagination | ε11 | Long-term EMA of pleasure |
| Tension | ε.tension_uncertainty | ε12 | Markov entropy |
| Prediction | ε.prediction_reward | ε13 | exp(−\|PE\| / σ) |
| Reaction | ε.reaction_magnitude | ε14 | \|PE\| × precision |
| Appraisal | ε.appraisal_learning | ε15 | Compression progress |

## Berridge Wanting/Liking Dissociation (2003)

Dual-process reward maps to both γ and ζ:

| Berridge Concept | L³ Group | Dimension | Mechanism |
|-----------------|----------|-----------|-----------|
| Wanting (incentive salience) | γ | reward_type (→0) | DA-mediated anticipation |
| Wanting (polarity) | ζ | wanting | satiated ↔ craving |
| Liking (hedonic impact) | γ | reward_type (→1) | Opioid-mediated pleasure |
| Liking (polarity) | ζ | liking | displeasure ↔ satisfaction |

## Berlyne Aesthetics — Wundt Curve (1971)

The inverted-U relationship between arousal and hedonic value is captured by:

- **ε.wundt_position** (ε17): `4 × surprise × (1 − surprise)`
- Peak pleasure at intermediate novelty/arousal (surprise ≈ 0.5)
- Maps Berlyne's "optimal arousal" theory to a continuous scalar
- Connects to the collative variables: novelty, complexity, surprise

## Self-Determination Theory (Deci & Ryan, 2000)

Indirect mapping:

| SDT Need | L³ Proxy | Rationale |
|----------|----------|-----------|
| Autonomy | ζ.power | Sense of agency/control |
| Competence | ζ.stability | Predictive success |
| Relatedness | ζ.engagement | Absorbed connection |

## Summary

| Framework | Year | Factors | L³ Coverage | Key Axes |
|-----------|------|---------|-------------|----------|
| Russell Circumplex | 1980 | 2 | 2/2 (100%) | ζ0, ζ1 |
| Osgood EPA | 1957 | 3 | 3/3 (100%) | ζ0, ζ1, ζ3 |
| GEMS | 2008 | 9 | 9/9 (100%) | ζ0-5, γ6, ε18 |
| ITPRA | 2006 | 5 | 5/5 (100%) | ε11-15 |
| Berridge | 2003 | 2 | 2/2 (100%) | γ1, ζ4-5 |
| Berlyne/Wundt | 1971 | 1 | 1/1 (100%) | ε17 |
| SDT | 2000 | 3 | 3/3 (indirect) | ζ3, ζ10, ζ11 |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
