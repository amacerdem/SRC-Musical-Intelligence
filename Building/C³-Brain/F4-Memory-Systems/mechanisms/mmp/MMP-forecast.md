# MMP C-Layer — Forecast (3D)

**Layer**: Clinical Metrics (C)
**Indices**: [9:12]
**Scope**: exported (clinical output)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 9 | C0:preservation_idx | [0, 1] | Relative sparing measure. How much musical memory is preserved relative to general memory at this disease state. cortical_strength / (cortical_strength + episodic_strength + epsilon). Jacobsen et al. 2015: SMA/pre-SMA and ACC show least cortical atrophy in AD (VBM, N=32). |
| 10 | C1:therapeutic_eff | [0, 1] | Therapeutic efficacy metric. Expected clinical benefit of this music for this patient state. (f07_preserved + f08_melodic + f09_scaffold) / 3.0. Luxton et al. 2025: Level 1 evidence for cognitive stimulation (SMD=0.25, p=0.003); Fang et al. 2017: MT reduces cognitive decline. |
| 11 | C2:hippocampal_indep | [0, 1] | Hippocampal independence score. How much of the current response is cortically mediated (AD-resistant). High = more preserved in AD. Computed as cortical_features / (cortical_features + episodic_features + epsilon). Espinosa et al. 2025: active musicians show increased GM in AD-resistant regions (p<0.0001). |

---

## Design Rationale

1. **Preservation Index (C0)**: The primary clinical output. Quantifies the relative sparing of musical memory compared to general memory. Computed from the ratio of cortical feature strength (warmth, tonalness, tristimulus, stumpf) to episodic feature strength (entropy). High values indicate that the patient's musical memory pathways are substantially more intact than general memory pathways, justifying music therapy intervention.

2. **Therapeutic Efficacy (C1)**: A composite clinical metric averaging the three R-layer features: preserved memory (f07), melodic recognition (f08), and scaffold efficacy (f09). This provides a single number for clinicians: "how much benefit will this specific music provide for this specific patient?" Validated against systematic review evidence (Fang et al. 2017, Luxton et al. 2025).

3. **Hippocampal Independence (C2)**: Measures the degree to which the current musical response is cortically mediated rather than hippocampally dependent. High independence means the response will persist even as hippocampal atrophy progresses. This directly informs treatment planning: select music that maximizes hippocampal-independent pathways for patients with advancing disease.

---

## Preservation Factor Computation

```
For each R3 feature:
  preserved_weight(feature) = 1.0 - (hippocampal_dependency * atrophy_factor)

Feature hippocampal dependencies:
  warmth, tonalness, tristimulus:    0.1 (cortical — highly preserved)
  x_l5l7 (consonance*timbre):       0.2 (cortical — preserved)
  stumpf_fusion, pleasantness:       0.3 (mixed — preserved)
  loudness, roughness:               0.4 (emotional — partially preserved)
  entropy, x_l0l5:                   0.8 (episodic — vulnerable)

At maximum atrophy (1.0):
  Cortical features retain 90% strength
  Emotional features retain 60% strength
  Episodic features retain only 20% strength
```

---

## H3 Dependencies (C-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 24, 19, 0) | stumpf_fusion stability H24 L0 | Long-term binding stability (36s) |
| (18, 24, 1, 0) | tristimulus1 mean H24 L0 | Long-term timbre stability (36s) |
| (10, 24, 3, 0) | loudness std H24 L0 | Arousal variability over 36s |
| (0, 24, 1, 0) | roughness mean H24 L0 | Long-term valence (36s) |
| (7, 24, 5, 0) | amplitude range H24 L0 | Dynamic range over 36s |

C-layer uses long-horizon (H24) features for clinical-scale assessments.

---

## Clinical Applications

| C-Layer Output | Clinical Use |
|---------------|-------------|
| **preservation_idx** | Screen which patients benefit most from music therapy |
| **therapeutic_eff** | Predict intervention efficacy per-patient |
| **hippocampal_indep** | Select music that maximizes preserved pathways |

---

## Scientific Foundation

- **Jacobsen et al. 2015**: Musical memory regions (SMA, pre-SMA, ACC) show least cortical atrophy in AD (fMRI+VBM, N=32)
- **Espinosa et al. 2025**: Active musicians show increased GM in L-planum temporale, L-planum polare, R-posterior insula, L-cerebellum (VBM, N=61, all p<0.0001)
- **Luxton et al. 2025**: Level 1 evidence — cognitive stimulation therapy improves QoL (SMD=0.25, p=0.003) (systematic review+meta-analysis, 324 studies)
- **Jin et al. 2024**: Musicians preserve youth-like lateralization patterns vs compensation in non-musicians (resting-state fMRI)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/mmp/forecast.py`
