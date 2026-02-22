# CDEM M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:congruency_index | [0, 1] | Music-mood congruency estimation. sigma(0.50 * (1-roughness) * familiar + 0.50 * x_l5l7.mean * warmth). Congruent context = stronger encoding. Sachs 2025: within-context emotion correlation (r=0.303) > across-context (r=0.265, p=0.04). Sakakibara 2025: nostalgia enhances memory vividness (Cohen's r=0.88, N=33). |
| 4 | M1:context_recall_prob | [0, 1] | P(recall given context reinstated). sigma(0.35 * retrieval + 0.35 * familiar + 0.30 * (1-entropy)). Foundational encoding specificity principle. Godden & Baddeley 1975: ~40% better recall in same context (N=18). Billig 2022: hippocampal computational architecture for auditory context binding (review). |

---

## Design Rationale

1. **Congruency Index (M0)**: Quantifies how well the current music's emotional content matches the listening context. Uses two equally-weighted terms: consonance times familiarity (pleasant + recognized = congruent) and consonance-timbre interaction times warmth (familiar timbre warmth = matching context). High congruency means the music and context are emotionally aligned, which amplifies memory encoding.

2. **Context Recall Probability (M1)**: Estimates the probability that a memory trace will be successfully retrieved when the context is reinstated. Based on encoding specificity (Tulving & Thomson 1973). Retrieval state (0.35), familiarity (0.35), and low entropy (0.30) all contribute — memories encoded in simple, familiar, actively-retrieved contexts are the most context-retrievable.

---

## Mathematical Formulation

```
Congruency Index:
  congruency_index = sigma(0.50 * (1 - roughness[0]) * familiar
                         + 0.50 * x_l5l7.mean() * warmth[12])
  |0.50| + |0.50| = 1.00

Context Recall Probability:
  ctx_recall_prob = sigma(0.35 * retrieval + 0.35 * familiar + 0.30 * (1 - entropy[22]))
  |0.35| + |0.35| + |0.30| = 1.00
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 20, 1, 0) | stumpf_fusion mean H20 L0 | Binding over 5s context window |
| (4, 20, 18, 0) | sensory_pleasantness trend H20 L0 | Pleasantness trajectory for congruency |
| (0, 20, 18, 0) | roughness trend H20 L0 | Valence trajectory for congruency |
| (12, 20, 1, 0) | warmth mean H20 L0 | Sustained context warmth stability |
| (22, 20, 1, 0) | entropy mean H20 L0 | Average complexity over 5s |

---

## Scientific Foundation

- **Sachs et al. 2025**: Within-context emotion correlation > across-context (r=0.303 vs 0.265, p=0.04, fMRI, N=39)
- **Sakakibara et al. 2025**: Nostalgia Brain-Music Interface enhances memory vividness (EEG, N=33, Cohen's r=0.88)
- **Godden & Baddeley 1975**: Context-dependent memory: ~40% better recall in same context (behavioral, N=18)
- **Tulving & Thomson 1973**: Encoding specificity principle for context-dependent memory (theoretical framework)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/cdem/temporal_integration.py`
