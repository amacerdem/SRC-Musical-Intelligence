# DAP E-Layer — Extraction (1D)

**Layer**: Extraction (E)
**Indices**: [0:1]
**Scope**: internal
**Activation**: clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f12_dev_sensitiv | [0, 1] | Age-dependent plasticity coefficient. f12 = plasticity * exposure. Product of current neural plasticity (inverse of maturation) and musical enrichment history. High during critical period (ages 0-5) with rich musical environment. Trainor 2012: musical training before age 7 yields enhanced auditory processing. |

---

## Design Rationale

1. **Developmental Sensitivity (E0)**: The single extraction feature captures the overall developmental sensitivity to musical affect. It is the product of two signals: plasticity (how malleable the auditory-limbic connections currently are) and exposure (how much musical enrichment has been received). This multiplicative gate ensures that sensitivity is high only when both plasticity is available AND enrichment is present — plasticity without exposure produces no lasting effect, and exposure after critical period closure has diminished impact. Based on general neurodevelopmental principles (Trainor 2012) and preterm infant response patterns (Scholkmann 2024).

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Current hedonic response strength — maturation marker |
| (0, 16, 0, 2) | roughness value H16 L2 | Consonance discrimination — developmental marker |
| (10, 16, 0, 2) | loudness value H16 L2 | Arousal response baseline — maturation index |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | Consonance learning marker — discrimination ability |
| [4] | sensory_pleasantness | Hedonic response strength — enrichment indicator |
| [10] | loudness | Arousal response baseline — developmental maturation |
| [14] | tonalness | Tonal template strength — learned pattern depth |

---

## Scientific Foundation

- **Trainor & Unrau 2012**: Musical training before age 7 yields enhanced auditory processing and pitch discrimination (review, Springer Handbook)
- **Scholkmann et al. 2024**: 2 distinct response patterns in preterm infants; sex differences in StO2 response to music (fNIRS, N=17)
- **Trehub 2003**: Developmental origins of musicality — innate predispositions for musical processing (review, Nature Neuroscience)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/dap/extraction.py`
