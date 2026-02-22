# HCMC P-Layer — Cognitive Present (3D)

**Layer**: Present Processing (P)
**Indices**: [5:8]
**Scope**: exported (kernel relay)
**Activation**: clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:binding_state | [0, 1] | Current hippocampal binding activation. Aggregation of encoding state from E-layer fast binding. Reflects the real-time "am I encoding this now" signal. Fernandez-Rubio et al. 2022: left hippocampus activated at 4th tone of memorized tonal sequences. |
| 6 | P1:segmentation_state | [0, 1] | Current episodic segmentation state. flux x entropy aggregation -- high values indicate an event boundary is being processed. Zacks et al. 2007: event perception boundaries. |
| 7 | P2:storage_state | [0, 1] | Current cortical storage activation. retrieval_dynamics x x_l5l7 -- reflects ongoing hippocampal-to-cortical transfer. Sikka et al. 2015: age-related hippocampal-to-cortical shift for musical semantic memory. |

---

## Design Rationale

1. **Binding State (P0)**: The summary "present-moment" signal for hippocampal encoding. This is the primary relay output that the kernel scheduler reads. It reflects whether the hippocampus is actively binding incoming musical features into a new episodic trace. High binding state occurs during novel or salient musical moments.

2. **Segmentation State (P1)**: Indicates whether the current frame is at or near an episodic boundary. Combines spectral flux (change magnitude) with entropy (unpredictability). Event boundaries are moments where the hippocampus closes one episodic segment and opens another.

3. **Storage State (P2)**: Reflects the degree to which cortical networks (mPFC, PCC) are actively receiving consolidated traces from the hippocampus. Uses consonance-timbre interactions as the cortical template signal. High storage state indicates active consolidation into long-term memory.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports for HCMC:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `binding_state` | P0 [5] | Familiarity belief: encoding component |
| `segmentation_state` | P1 [6] | Salience mixer: boundary detection |
| `storage_state` | P2 [7] | Familiarity belief: consolidation component |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (7, 20, 5, 0) | amplitude range H20 L0 | Energy dynamic range for binding activation |
| (10, 24, 3, 0) | loudness std H24 L0 | Salience variability over 36s for storage |
| (5, 24, 22, 0) | harmonicity autocorrelation H24 L0 | Harmonic repetition detection for storage |

P-layer primarily aggregates E+M outputs rather than reading many new H3 tuples directly.

---

## Brain Regions

| Region | MNI Coordinates | P-Layer Role |
|--------|-----------------|--------------|
| Hippocampus | +/-20, -24, -12 | P0: binding activation source |
| Entorhinal Cortex | +/-24, -12, -24 | P0: sensory input gateway |
| mPFC | 0, 52, 12 | P2: cortical storage target |
| PCC / Cingulate | 0, -52, 26 | P2: episodic recollection |

---

## Scientific Foundation

- **Fernandez-Rubio et al. 2022**: Tonal sequence recognition activates hippocampus + cingulate (MEG, N=71, MCS p<0.001)
- **Zacks et al. 2007**: Event segmentation theory -- boundaries trigger encoding (behavioral + fMRI)
- **Sikka et al. 2015**: Age-related shift from hippocampus to cortex for musical semantic memory (fMRI, N=40)
- **Billig et al. 2022**: Hippocampal auditory processing via EC-DG-CA3-CA1 trisynaptic pathway (review)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/hcmc/cognitive_present.py`
