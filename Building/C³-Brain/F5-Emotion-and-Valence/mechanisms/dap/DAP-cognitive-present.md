# DAP P-Layer — Cognitive Present (3D)

**Layer**: Present Processing (P)
**Indices**: [5:8]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:current_affect | [0, 1] | Current affective response strength to music. current_affect = sigma(0.5 * response + 0.5 * R3.sensory_pleasantness[4]). Modulated by developmental history — enriched individuals show stronger real-time affective responses. Trehub 2003: innate musicality provides developmental baseline for affective response. |
| 6 | P1:familiarity_warmth | [0, 1] | Familiarity-warmth link strength. familiarity_warmth = sigma(exposure * (1.0 - R3.distribution_entropy[22]) * 2.0). Strength of learned associations between familiar musical patterns and affective warmth. High exposure + low entropy (predictable) = strong warmth association. Nguyen 2023: early ID singing establishes familiarity-warmth bonds. |
| 7 | P2:learning_rate | [0, 1] | Current affect-learning rate. learning_rate = plasticity * sigma(arousal_dynamics * 2.0). Decreases with age as plasticity decays. High during critical period — captures how quickly new music-affect associations form. Trainor 2012: enhanced learning rate during critical period. |

---

## Design Rationale

1. **Current Affect (P0)**: The present-moment affective response strength. Averages the internal response signal (from H3 affect dynamics) with the external hedonic quality (R3 sensory pleasantness). This weighted combination ensures the output reflects both the developmental history (response strength depends on enrichment) and the current acoustic quality.

2. **Familiarity-Warmth (P1)**: The strength of the learned association between musical familiarity and affective warmth. Computed as exposure history multiplied by musical predictability (1 - entropy). This captures the "mere exposure" effect — repeated exposure to predictable musical patterns builds warm affective associations, and this building process is stronger during the critical period.

3. **Learning Rate (P2)**: The current rate at which new music-affect associations can be formed. Gated by plasticity coefficient (from D-layer) and modulated by current arousal dynamics. High arousal states facilitate learning even in low-plasticity conditions, but the plasticity gate ensures that the overall learning rate declines with maturation.

---

## Kernel Relay Export

P-layer outputs feed the kernel relay for cross-function integration:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `current_affect` | P0 [5] | Emotion: developmental modulation of affective response |
| `familiarity_warmth` | P1 [6] | Familiarity: developmental warmth-familiarity binding |
| `learning_rate` | P2 [7] | Learning: plasticity-dependent affect acquisition rate |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Current hedonic quality |
| (22, 16, 20, 2) | entropy entropy H16 L2 | Predictability for familiarity estimation |
| (10, 16, 8, 0) | loudness velocity H16 L0 | Arousal dynamics for learning rate |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [4] | sensory_pleasantness | P0: direct hedonic signal |
| [10] | loudness | P2: arousal dynamics for learning modulation |
| [22] | distribution_entropy | P1: predictability for familiarity-warmth link |

---

## Scientific Foundation

- **Trehub 2003**: Developmental origins of musicality — innate predispositions shape affective response baseline (review, Nature Neuroscience, 6(7), 669-673)
- **Nguyen et al. 2023**: Infant-directed singing establishes familiarity-warmth bonds through co-regulation (review, Developmental Cognitive Neuroscience, 63, 101279)
- **Trainor & Unrau 2012**: Enhanced learning rate during critical period — musical training before age 7 produces lasting effects (review, Springer Handbook)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/dap/cognitive_present.py`
