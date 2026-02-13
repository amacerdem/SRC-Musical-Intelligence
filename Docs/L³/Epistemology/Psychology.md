# L³ Epistemology — Psychology

**Level**: 3 (γ)
**Question**: WHAT does it mean subjectively?
**Audience**: Psychologists, music cognition researchers
**Version**: 2.1.0
**Updated**: 2026-02-13

---

## Overview

The Psychology group translates neural activity into subjective experience. Where β tells us which brain regions are active, γ tells us what the listener *feels*. This is the interpretive bridge between biology and phenomenology.

Gamma produces 13 dimensions across 5 subcategories: Reward (3), ITPRA (2), Aesthetics (3), Emotion (2), and Chills (3).

---

## Reward Psychology (3D)

### Intensity / Type / Phase Dissociation

Reward is not a single thing. Gamma's first three dimensions dissociate three orthogonal aspects:

| Local | Name | What it captures | Citation |
|:-----:|------|------------------|----------|
| γ0 | `reward_intensity` | HOW MUCH reward (overall magnitude) | Salimpoor et al. 2011 |
| γ1 | `reward_type` | WHAT KIND: wanting (0) vs liking (1) | Berridge 2003 |
| γ2 | `reward_phase` | WHEN: anticipation (0) vs consummation (1) | Salimpoor et al. 2011 |

Berridge (2003) demonstrated that wanting (incentive salience, dopaminergic) and liking (hedonic pleasure, opioidergic) are psychologically and neurally dissociable. A listener can intensely want to hear a passage again (high wanting) without experiencing peak pleasure in the moment (low liking), or vice versa.

The phase dimension (γ2) captures the temporal position within the reward cycle: anticipation builds before the rewarding moment, consummation occurs at and after it.

---

## ITPRA Theory (2D)

Huron's (2006) ITPRA framework describes five stages of expectation response:

- **I**magination: pre-event mental imagery
- **T**ension: uncertainty-driven arousal before the event
- **P**rediction: accuracy of the prediction (correct = positive, wrong = negative)
- **R**eaction: automatic fast response to the event
- **A**ppraisal: slower conscious evaluation

Gamma captures two composite ITPRA dimensions:

| Local | Name | Formula | Citation |
|:-----:|------|---------|----------|
| γ3 | `itpra_tension_resolution` | (1 - tension) * harmonic_context | Huron 2006 |
| γ4 | `itpra_surprise_evaluation` | \|prediction_error\| * emotional_arc | Huron 2006 |

Tension-resolution (γ3) captures the relief when uncertainty resolves into consonance. Surprise-evaluation (γ4) captures the magnitude and emotional impact of violated expectations. Together, they encode the core of Huron's framework as continuous signals.

---

## Musical Aesthetics (3D)

| Local | Name | Description | Citation |
|:-----:|------|-------------|----------|
| γ5 | `beauty` | Opioid-mediated hedonic pleasure — consonance, resolution, flow | Blood & Zatorre 2001 |
| γ6 | `sublime` | Awe and transcendence — pleasure * arousal | Konecni 2005 |
| γ7 | `groove` | Motor-entrainment coupling — arousal * harmonic_context | Janata et al. 2012 |

**Beauty** (γ5) is the classical aesthetic response — the pleasure of well-formed harmonic progressions, smooth voice leading, and melodic contour. It maps to opioid-mediated hedonic processing.

**Sublime** (γ6) is beauty amplified by arousal to the point of awe. Konecni (2005) argues that the sublime is phenomenologically distinct from beauty — it involves a sense of being overwhelmed that beauty alone does not produce.

**Groove** (γ7) is the urge to move with the music. Janata et al. (2012) showed that groove arises from the interaction of rhythmic clarity (motor entrainment) and harmonic richness. It is a uniquely musical aesthetic that has no obvious parallel in visual art.

---

## Circumplex Emotion (2D)

| Local | Name | Description | Citation |
|:-----:|------|-------------|----------|
| γ8 | `valence` | Positive/negative affect: (f03_valence + 1) / 2 | Russell 1980 |
| γ9 | `arousal` | Activation level: energy/intensity | Yang et al. 2025 |

Russell's (1980) **circumplex model of affect** holds that all emotional states can be located in a 2D space defined by valence (pleasant-unpleasant) and arousal (activated-deactivated). This is the most widely validated dimensional model of emotion in psychology.

γ8 and γ9 map the Brain's output onto this 2D space. Any frame of music can be characterized as, for example, high-valence/high-arousal (joyful excitement), low-valence/high-arousal (anxious tension), or high-valence/low-arousal (peaceful contentment).

---

## Musical Chills (3D)

| Local | Name | Description | Citation |
|:-----:|------|-------------|----------|
| γ10 | `chill_probability` | ANS chill signature: SCR * (1 - HR) | de Fleurian & Pearce 2021 |
| γ11 | `chill_intensity` | Integrated chill strength | Sloboda 1991 |
| γ12 | `chill_phase` | Buildup/peak/afterglow: sigma(chills - tension) | Grewe et al. 2009 |

Musical chills (frisson) are brief, intense pleasure responses marked by goosebumps, shivers, and autonomic nervous system changes. de Fleurian & Pearce (2021) meta-analyzed the chill literature and found a reliable ANS signature with effect size d = 0.85.

Gamma models chills as a three-phase process:
1. **Buildup** (γ12 low): tension accumulates as expectations become uncertain
2. **Peak** (γ12 mid): the chill occurs at the moment of resolution or surprise
3. **Afterglow** (γ12 high): post-chill relaxation and satisfaction

This three-phase structure explains why chills are not just spikes — they have temporal shape.

---

## Key Citations

- Berridge, K.C. (2003). Pleasures of the brain. *Brain and Cognition*, 52(1), 106-128.
- Huron, D. (2006). *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press.
- Blood, A.J. & Zatorre, R.J. (2001). Intensely pleasurable responses to music. *PNAS*, 98(20), 11818-11823.
- Russell, J.A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*, 39(6), 1161-1178.
- Janata, P., Tomic, S.T., & Haberman, J.M. (2012). Sensorimotor coupling in music and the psychology of the groove. *JEPHPP*, 38(1), 54-72.
- de Fleurian, R. & Pearce, M.T. (2021). Chills in music: A systematic review. *Psychological Bulletin*, 147(9), 890-920.
- Konecni, V.J. (2005). The aesthetic trinity: awe, being moved, thrills. *Bulletin of Psychology and the Arts*, 5(2), 27-44.
- Sloboda, J.A. (1991). Music structure and emotional response. *Psychology of Music*, 19, 110-120.
- Grewe, O., Kopiez, R., & Altenmuller, E. (2009). Chills as an indicator of individual emotional peaks. *Annals of the New York Academy of Sciences*, 1169, 351-354.

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [Groups/Independent/Gamma.md](../Groups/Independent/Gamma.md) for implementation details | [Registry/DimensionCatalog.md](../Registry/DimensionCatalog.md) for dimension metadata
