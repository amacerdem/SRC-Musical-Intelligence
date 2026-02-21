# Region Activation Map (RAM)

Non-computational 26D brain region activation.
Visualization ve HYBRID layer için spatial output.
Belief'leri veya reward'ı ETKİLEMEZ.

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

## Region Link Table

### BCH (SPU) — Brainstem Consonance
| Output | Region | Weight |
|--------|--------|--------|
| hierarchy | IC | 0.85 |
| consonance_signal | MGB | 0.6, STG | 0.4 |

### HMCE (STU) — Temporal Context
| Output | Region | Weight |
|--------|--------|--------|
| a1_encoding | A1_HG | 0.85 |
| stg_encoding | STG | 0.80 |
| mtg_encoding | STS | 0.75 |
| context_prediction | hippocampus | 0.50 |
| structure_predict | IFG | 0.60 |

### SNEM (ASU) — Neural Entrainment
| Output | Region | Weight |
|--------|--------|--------|
| beat_locked_activity | SMA | 0.80 |
| entrainment_strength | putamen | 0.85 |
| selective_gain | ACC | 0.50 |
| beat_onset_pred | PMC | 0.60 |

### MEAMN (IMU) — Autobiographical Memory
| Output | Region | Weight |
|--------|--------|--------|
| memory_state | hippocampus | 0.90 |
| emotional_color | amygdala | 0.80 |
| nostalgia_link | AG | 0.60, STG | 0.80 |
| self_referential_pred | vmPFC | 0.85 |

### DAED (RPU) — Dopamine Dissociation
| Output | Region | Weight |
|--------|--------|--------|
| wanting_index | amygdala | 0.60, hippocampus | 0.40 |
| liking_index | putamen | 0.60, OFC | 0.70 |
| caudate_activation | caudate | 0.85 |
| nacc_activation | NAcc | 0.85 |

### MPG (NDU) — Melodic Processing
| Output | Region | Weight |
|--------|--------|--------|
| onset_state | STG | 0.60 |
| contour_state | STG | 0.70 |

### SRP (ARU) — Striatal Reward
| Output | Region | Weight |
|--------|--------|--------|
| wanting | caudate | 0.70 |
| liking | NAcc | 0.80 |
| tension | IFG | 0.60 |

### PEOM (MPU) — Motor Entrainment
| Output | Region | Weight |
|--------|--------|--------|
| period_lock_strength | STG | 0.60 |
| next_beat_pred | SMA | 0.70 |

### HTP (PCU) — Hierarchical Prediction
| Output | Region | Weight |
|--------|--------|--------|
| sensory_match | A1_HG | 0.90 |
| pitch_prediction | STG | 0.85 |
| abstract_prediction | STG | 0.80 |
| abstract_future_500ms | ACC | 0.60 |

## Convergence Hub: STG

4 relay feeds into STG: BCH, MEAMN, MPG, PEOM, HTP.
Highest connectivity in the network.
