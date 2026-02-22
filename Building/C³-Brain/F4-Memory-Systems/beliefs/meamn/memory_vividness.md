# memory_vividness — Appraisal Belief (MEAMN)

**Category**: Appraisal (observe-only)
**Owner**: MEAMN (IMU-α1)

---

## Definition

"Memory vividness high/low." Interaction of retrieval strength and emotional intensity. Tracks how vivid and detailed the currently retrieved autobiographical memory is — from faint recognition ("I've heard this before") to full multisensory re-experiencing ("I can see the room, smell the air"). Computed as the product of retrieval activation and emotional color, reflecting the finding that vivid MEAMs require both strong retrieval and emotional engagement.

---

## Observation Formula

```
# Interaction of E-layer retrieval and P-layer emotional color:
memory_vividness = MEAMN.f01_retrieval[E0] × MEAMN.emotional_color[P1]
                 # index [0] × index [6]

# f01_retrieval = sigma(0.80 × x_l0l5.mean × retrieval × stumpf)
# emotional_color = arousal × (1 - roughness)
```

No prediction — observe-only appraisal. The multiplicative interaction captures the key finding from Belfi et al. (2016): memory vividness is not simply retrieval strength, but the product of retrieval and emotional intensity. A strongly retrieved but emotionally neutral memory will have low vividness; a weakly retrieved but emotional memory will also have low vividness.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| MEAMN E0 | f01_retrieval [0] | Hippocampal retrieval strength |
| MEAMN P1 | emotional_color [6] | Affective tag intensity |
| R³ [25:33] | x_l0l5 | Energy-consonance binding (upstream of E0) |
| R³ [0] | roughness | Valence proxy for emotional_color |
| R³ [10] | loudness | Arousal correlate for emotional_color |

---

## Kernel Usage

The memory_vividness appraisal feeds multiple downstream systems:

```python
# Available in BeliefStore for downstream consumers:
# - F6 Reward: vivid memories amplify hedonic signal
# - Precision engine: memory_vividness contributes 0.1 weight to pi_obs
#   (from autobiographical_retrieval precision formula)
# - F5 Emotion: vividness gates emotional re-experiencing intensity
```

The precision contribution is documented in the autobiographical_retrieval observe formula: `+ MEAMN: 0.3×(memory×nostalgia) + 0.2×self_ref + 0.1×vividness`.

---

## Scientific Foundation

- **Belfi et al. 2016**: Music-evoked autobiographical memories are more vivid than word-cued memories; vividness correlates with both familiarity and emotional intensity (behavioral, N=31)
- **Janata 2009**: Imagery vividness strong vs weak autobiographical (t(9)=5.784, p<0.0003); vividness tracks mPFC activation (fMRI 3T, N=13)
- **Sakakibara et al. 2025**: Nostalgia enhances memory vividness (eta_p^2=0.541); acoustic triggers sufficient for vivid recall (EEG, N=33)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/meamn_relay.py`
