# MEAMN M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:meam_retrieval | [0, 1] | MEAM Retrieval function. f(Familiarity * EmotionalIntensity * SelfRelevance). Expanded: retrieval * familiarity * emotional_intensity. Janata 2009: music-evoked autobiographical memories emerge from intersection of familiar musical structure and personal history. |
| 4 | M1:p_recall | [0, 1] | P(recall given music). sigma(beta_0 + beta_1*Familiarity + beta_2*Arousal + beta_3*Valence). Familiarity from familiarity_proxy, Arousal from R3.loudness, Valence from 1-roughness. Derks-Dijkman 2024: 28/37 studies show musical mnemonic benefit. |

---

## Design Rationale

1. **MEAM Retrieval (M0)**: The core computational model of music-evoked autobiographical memory. Combines three factors: familiarity (how well-known the music is), emotional intensity (arousal x valence), and self-relevance (hippocampal binding strength). This triple-product captures the finding that MEAMs require all three components to emerge — familiar music without emotional significance does not trigger autobiographical recall.

2. **Recall Probability (M1)**: A logistic regression model predicting the probability of autobiographical memory recall given current musical input. Uses familiarity, arousal (loudness), and valence (1-roughness) as predictors. Based on the behavioral finding (Janata et al. 2007) that 30-80% of familiar songs trigger MEAMs, with trigger rate modulated by these three factors.

---

## Mathematical Formulation

```
MEAM_Retrieval(music) = f(Familiarity * EmotionalIntensity * SelfRelevance)

P(recall | music) = sigma(beta_0 + beta_1*Familiarity + beta_2*Arousal + beta_3*Valence)

where:
  Familiarity   = familiarity_proxy.mean()  [derived from entropy, warmth]
  EmotionalInt. = |Valence| * Arousal       [from R3 + affect dynamics]
  SelfRelevance = retrieval_dynamics.mean()  [hippocampal binding]
  Arousal       = sigma(R3.loudness[10] * R3.amplitude[7])
  Valence       = 1 - R3.roughness[0]       [consonance = pleasant]

Temporal dynamics:
  dMEAM/dt = alpha * (Current_Music - MEAM) + beta * dFamiliarity/dt
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Current pleasantness |
| (4, 20, 18, 0) | sensory_pleasantness trend H20 L0 | Pleasantness trajectory |
| (10, 20, 1, 0) | loudness mean H20 L0 | Average arousal over 5s |
| (22, 16, 0, 2) | entropy value H16 L2 | Current unpredictability |
| (22, 20, 1, 0) | entropy mean H20 L0 | Average complexity over 5s |
| (7, 16, 8, 0) | amplitude velocity H16 L0 | Energy change rate |

---

## Scientific Foundation

- **Janata 2009**: mPFC as retrieval hub; retrieval_dynamics + familiarity binding (fMRI 3T, N=13, t(9)=5.784)
- **Janata et al. 2007**: 30-80% MEAM trigger rate with popular music; reminiscence bump ages 10-30 (behavioral, N~300)
- **Derks-Dijkman et al. 2024**: 28/37 studies show musical mnemonics improve memory (systematic review, 37 studies)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/meamn/temporal_integration.py`
