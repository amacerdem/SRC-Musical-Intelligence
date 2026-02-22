# memory_preservation — Appraisal Belief (MMP)

**Category**: Appraisal (observe-only)
**Owner**: MMP (IMU-a3)

---

## Definition

"Musical memories preserved despite disease." Tracks the degree of musical memory preservation, comparing semantic musical memory (preserved) vs. episodic musical memory (impaired in AD). This is a clinical meta-layer output reflecting the relative sparing of music-specific cortical pathways. High values indicate strong cortically-mediated musical memory with minimal hippocampal dependency.

---

## Observation Formula

```
# Direct read from MMP C-layer:
memory_preservation = MMP.preservation_idx[C0]  # index [9]

# Formula: cortical_strength / (cortical_strength + episodic_strength + epsilon)
# Cortical features (warmth, tonalness, tristimulus): hippocampal dep = 0.1
# Episodic features (entropy, x_l0l5): hippocampal dep = 0.8
# At maximum atrophy: cortical retains 90%, episodic retains only 20%
```

No prediction -- observe-only appraisal. The value is directly consumed as a clinical metric indicating the overall preservation state of musical memory pathways.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| MMP C0 | preservation_idx [9] | Primary preservation metric |
| MMP C2 | hippocampal_indep [11] | Cortical independence score (context) |
| MMP R0 | f07_preserved [0] | Preserved memory index (R-layer) |
| H3 | (3, 24, 19, 0) | stumpf_fusion stability H24 L0 -- binding stability (36s) |
| H3 | (18, 24, 1, 0) | tristimulus1 mean H24 L0 -- timbre stability (36s) |
| H3 | (10, 24, 3, 0) | loudness std H24 L0 -- arousal variability (36s) |

---

## Kernel Usage

The memory_preservation appraisal feeds the clinical meta-layer (F10):

```python
# Clinical output:
# preservation_idx screens which patients benefit most from music therapy
# High preservation + low general memory = strong music therapy candidate
```

This provides the key clinical signal distinguishing preserved semantic musical memory from impaired episodic memory. It directly informs treatment planning and patient screening for music-based interventions.

---

## Scientific Foundation

- **Jacobsen et al. 2015**: SMA/pre-SMA and ACC show least cortical atrophy in AD; musical memory regions spared (fMRI+VBM, N=32)
- **Dominguez et al. 2025**: Episodic vs semantic distinction -- semantic musical memory preserved while episodic degrades in AD
- **Espinosa et al. 2025**: Active musicians show increased GM in AD-resistant regions (VBM, N=61, p<0.0001)
- **Luxton et al. 2025**: Level 1 evidence -- cognitive stimulation therapy improves QoL (SMD=0.25, p=0.003) (systematic review+meta-analysis, 324 studies)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/mmp/` (pending)
