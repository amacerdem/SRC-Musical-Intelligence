# memory_scaffold_pred — Anticipation Belief (MMP)

**Category**: Anticipation (prediction)
**Owner**: MMP (IMU-a3)

---

## Definition

"Music will help access locked memories." Predicts whether current music can serve as a cognitive scaffold -- a bridge to otherwise inaccessible memories and emotional states in cognitively impaired listeners. High values indicate that the music is successfully activating cortical back-channels to locked autobiographical and semantic memories.

---

## Observation Formula

```
# From MMP F-layer:
memory_scaffold_pred = MMP.scaffold_fc[F2]  # index [8]

# Formula: sigma(f09_scaffold * hippocampal_indep)
# where f09_scaffold = MMP R2 (retrieval * x_l5l7.mean * (1/entropy) * preservation_factor)
# hippocampal_indep = MMP C2 (cortical_features / (cortical + episodic + epsilon))
```

Anticipation beliefs are forward-looking predictions that generate PE when the predicted scaffold efficacy mismatches the observed therapeutic response.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| MMP F2 | scaffold_fc [8] | Cognitive scaffolding prediction |
| MMP R2 | f09_scaffold [2] | Memory scaffold efficacy (R-layer) |
| MMP C2 | hippocampal_indep [11] | Cortical independence score |
| H3 | (22, 24, 1, 0) | entropy mean H24 L0 -- predictability for scaffold trajectory |
| H3 | (16, 20, 1, 0) | spectral_smoothness mean H20 L0 -- timbral quality for recognition trajectory |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F10 Clinical | Therapeutic assessment -- session-level benefit prediction |
| F5 Emotion | Emotional scaffolding -- predicts emotional response to locked memory access |
| Precision engine | pi_pred estimation via scaffold prediction accuracy |

---

## Scientific Foundation

- **Derks-Dijkman et al. 2024**: 28/37 studies show musical mnemonic benefit; familiarity key contributor (systematic review, 37 studies)
- **Luxton et al. 2025**: Level 1 evidence -- cognitive stimulation therapy improves QoL (SMD=0.25, p=0.003) (systematic review+meta-analysis, 324 studies)
- **Fang et al. 2017**: Music therapy reduces cognitive decline in autobiographical/episodic memory (systematic mini-review, multiple RCTs)
- **El Haj et al. 2012**: Music-evoked autobiographical memories more specific and vivid than verbal-evoked in AD (behavioral, AD patients)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/mmp/` (pending)
