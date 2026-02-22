# MEAMN E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f01_retrieval | [0, 1] | Autobiographical retrieval activation. Hippocampus + mPFC + PCC hub. f01 = sigma(0.80 * x_l0l5.mean * retrieval * stumpf). Janata 2009: dorsal MPFC (BA 8/9) tracks tonal space movement during autobiographically salient songs (t(9)=5.784, p<0.0003). |
| 1 | E1:f02_nostalgia | [0, 1] | Nostalgia response intensity. Hippocampus + STG melodic trace. f02 = sigma(0.70 * x_l5l7.mean * familiarity). Sakakibara 2025: acoustic similarity alone triggers nostalgia (eta_p^2=0.636). |
| 2 | E2:f03_emotion | [0, 1] | Emotional memory coloring. Amygdala affective tagging. f03 = sigma(0.60 * (1-roughness) * loudness * arousal). Context-dependent study 2021: multimodal integration in STS and hippocampus (d=0.17, p<0.0001). |

---

## Design Rationale

1. **Autobiographical Retrieval (E0)**: The primary MEAMN extraction feature. Measures how strongly current music activates autobiographical memory retrieval via the hippocampus-mPFC-PCC hub. Uses x_l0l5 (energy-consonance interaction) as the memory binding signal, modulated by stumpf fusion for coherence. Primary basis: Janata 2009 fMRI showing dorsal MPFC parametrically tracks autobiographical salience.

2. **Nostalgia Response (E1)**: Tracks the intensity of nostalgia evoked by familiar musical patterns. Uses x_l5l7 (consonance-timbre interaction) as the warmth-familiarity signal. Timbre warmth combined with tonal consonance creates the characteristic "this feels like home" nostalgia response. Sakakibara 2025 confirms acoustic features alone can trigger nostalgia.

3. **Emotional Coloring (E2)**: Measures the affective tag strength applied to retrieved memories. Uses the inverse of roughness (consonance = pleasant valence) combined with loudness (arousal correlate) to compute the emotional intensity of memory encoding. Supported by context-dependent memory studies showing amygdala-STS integration.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 16, 1, 2) | stumpf_fusion mean H16 L2 | Binding stability at 1s |
| (3, 20, 1, 2) | stumpf_fusion mean H20 L2 | Binding over 5s consolidation |
| (12, 16, 0, 2) | warmth value H16 L2 | Current timbre warmth |
| (12, 20, 1, 0) | warmth mean H20 L0 | Sustained warmth = nostalgia |
| (0, 16, 0, 2) | roughness value H16 L2 | Current dissonance |
| (0, 20, 18, 0) | roughness trend H20 L0 | Dissonance trajectory |
| (10, 16, 0, 2) | loudness value H16 L2 | Current arousal |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E2: valence proxy (inverse) |
| [3] | stumpf_fusion | E0: binding integrity |
| [10] | loudness | E2: arousal correlate |
| [12] | warmth | E1: nostalgia trigger |
| [25:33] | x_l0l5 | E0: memory retrieval binding |
| [41:49] | x_l5l7 | E1: nostalgia warmth signal |

---

## Scientific Foundation

- **Janata 2009**: Dorsal MPFC (BA 8/9) parametrically tracks autobiographical salience (fMRI 3T, N=13, t(9)=5.784, p<0.0003)
- **Sakakibara et al. 2025**: Nostalgia Brain-Music Interface — acoustic similarity triggers nostalgia (EEG, N=33, eta_p^2=0.636)
- **Context-dependent study 2021**: Multimodal integration in STS and hippocampus (fMRI, N=84, d=0.17, p<0.0001)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/meamn/extraction.py`
