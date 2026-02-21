# Region Activation Map (RAM)

**Version**: v3.0.0 (Mechanism-based beliefs)

Non-computational 26D brain region activation.
Visualization ve HYBRID layer için spatial output.
Belief'leri veya reward'ı ETKİLEMEZ.

> RAM is driven by relay outputs (model-level), not by beliefs directly.
> The 131 mechanism-level beliefs (v3.0) do not change region link computation.
> Region links are organized by Function (v2.0) — the same relay models drive the same regions.

## 26 Brain Regions

### Cortical (0–11)
| Idx | Region | Role |
|-----|--------|------|
| 0 | A1_HG | Primary auditory cortex |
| 1 | STG | Superior temporal gyrus (convergence hub) |
| 2 | STS | Superior temporal sulcus |
| 3 | IFG | Inferior frontal gyrus |
| 4 | dlPFC | Dorsolateral prefrontal cortex |
| 5 | vmPFC | Ventromedial prefrontal cortex |
| 6 | OFC | Orbitofrontal cortex |
| 7 | ACC | Anterior cingulate cortex |
| 8 | SMA | Supplementary motor area |
| 9 | PMC | Premotor cortex |
| 10 | AG | Angular gyrus |
| 11 | TP | Temporal pole |

### Subcortical (12–20)
| Idx | Region | Role |
|-----|--------|------|
| 12 | VTA | Ventral tegmental area |
| 13 | NAcc | Nucleus accumbens |
| 14 | caudate | Caudate nucleus |
| 15 | amygdala | Amygdala |
| 16 | hippocampus | Hippocampus |
| 17 | putamen | Putamen |
| 18 | MGB | Medial geniculate body |
| 19 | hypothalamus | Hypothalamus |
| 20 | insula | Insula |

### Brainstem (21–25)
| Idx | Region | Role |
|-----|--------|------|
| 21 | IC | Inferior colliculus |
| 22 | AN | Auditory nerve |
| 23 | CN | Cochlear nucleus |
| 24 | SOC | Superior olivary complex |
| 25 | PAG | Periaqueductal gray |

## Assembly Pipeline

```
1. Accumulate: ram[region] += Σ(relay_output × link_weight)
2. ReLU: negative → 0
3. Z-normalize across time (T>1): (x − μ) / σ
4. Sigmoid: → [0, 1]
```

T=1 (single frame): z-norm skipped → sigmoid(ReLU(x)) ∈ [0.5, 1)

## Region Link Table (v2.0 — Function-Based)

As of v2.0, region links are organized by Function. Each Function's primary relay
model drives the region activations. Relay names preserved for backward compatibility.

### F1 Sensory Processing (primary relay: BCH)
| Output | Region | Weight | Relay |
|--------|--------|--------|-------|
| hierarchy | IC | 0.85 | BCH |
| consonance_signal | MGB | 0.60 | BCH |
| consonance_signal | STG | 0.40 | BCH |

### F2 Pattern Recognition & Prediction (primary relay: HTP)
| Output | Region | Weight | Relay |
|--------|--------|--------|-------|
| sensory_match | A1_HG | 0.90 | HTP |
| pitch_prediction | STG | 0.85 | HTP |
| abstract_prediction | STG | 0.80 | HTP |
| abstract_future_500ms | ACC | 0.60 | HTP |
| a1_encoding | A1_HG | 0.85 | HMCE |
| stg_encoding | STG | 0.80 | HMCE |
| mtg_encoding | STS | 0.75 | HMCE |
| context_prediction | hippocampus | 0.50 | HMCE |
| structure_predict | IFG | 0.60 | HMCE |

### F3 Attention & Salience (primary relay: SNEM)
| Output | Region | Weight | Relay |
|--------|--------|--------|-------|
| beat_locked_activity | SMA | 0.80 | SNEM |
| entrainment_strength | putamen | 0.85 | SNEM |
| selective_gain | ACC | 0.50 | SNEM |
| beat_onset_pred | PMC | 0.60 | SNEM |

### F4 Memory Systems (primary relay: MEAMN)
| Output | Region | Weight | Relay |
|--------|--------|--------|-------|
| memory_state | hippocampus | 0.90 | MEAMN |
| emotional_color | amygdala | 0.80 | MEAMN |
| nostalgia_link | AG | 0.60 | MEAMN |
| nostalgia_link | STG | 0.80 | MEAMN |
| self_referential_pred | vmPFC | 0.85 | MEAMN |

### F5 Emotion & Valence (primary relay: VMM)

> F5 has no kernel relay in v1.0. Region links pending implementation wave 3.
> Evidence from MEAMN.emotional_color (F4) provides indirect amygdala activation.

### F6 Reward & Motivation (primary relay: SRP)
| Output | Region | Weight | Relay |
|--------|--------|--------|-------|
| wanting | caudate | 0.70 | SRP |
| liking | NAcc | 0.80 | SRP |
| tension | IFG | 0.60 | SRP |
| wanting_index | amygdala | 0.60 | DAED |
| liking_index | putamen | 0.60 | DAED |
| liking_index | OFC | 0.70 | DAED |
| caudate_activation | caudate | 0.85 | DAED |
| nacc_activation | NAcc | 0.85 | DAED |

### F7 Motor & Timing (primary relay: PEOM)
| Output | Region | Weight | Relay |
|--------|--------|--------|-------|
| period_lock_strength | STG | 0.60 | PEOM |
| next_beat_pred | SMA | 0.70 | PEOM |
| onset_state | STG | 0.60 | MPG |
| contour_state | STG | 0.70 | MPG |

### F8 Learning, F9 Social

> F8/F9 have no kernel relay in v1.0. Region links pending implementation waves 4–5.
> F8 plasticity → potential links: A1_HG, STG (expertise-dependent cortical reorganization).
> F9 social → potential links: STS, ACC, vmPFC (social cognition network).

### F10–F12 Meta-Layers

> Meta-Layers produce no beliefs and drive no region activations.
> Their evidence contributes indirectly via F1–F9 observe() calls.

## Convergence Hubs

### STG — Superior Temporal Gyrus
5 relay feeds from 4 Functions: BCH(F1), HMCE(F2), HTP(F2), MPG(F7), PEOM(F7), MEAMN(F4).
Highest connectivity in the network. Convergence of sensory, temporal, and memory signals.

### NAcc — Nucleus Accumbens
2 relay feeds from F6: SRP(liking), DAED(nacc_activation).
Primary reward convergence point.

### Hippocampus
2 relay feeds: HMCE(F2, context), MEAMN(F4, memory), DAED(F6, wanting).
Memory-prediction-reward convergence.
