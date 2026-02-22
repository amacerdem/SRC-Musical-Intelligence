# MAD F-Layer — Forecast (2D)

**Layer**: Forecast (F)
**Indices**: [9:11]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 9 | F0:recovery_potential | [0, 1] | Reward pathway recovery potential. recovery = connectivity * affect_entropy. Requires both residual connectivity (some FA) AND affective variability (some reward-driven modulation). Predicts neuroplasticity potential for therapeutic intervention. Belfi & Loui 2020: proposed model for music reward restoration. |
| 10 | F1:anhedonia_prob | [0, 1] | Overall disconnection likelihood (diagnostic composite). sigma(0.4 * f10_anhedonia + 0.3 * dissociation_idx + 0.3 * (1.0 - stg_nacc_connect)). Weighted combination of all markers: anhedonia severity (40%), dissociation pattern (30%), connectivity deficit (30%). Clinical diagnostic output. |

---

## Design Rationale

1. **Recovery Potential (F0)**: A forward-looking clinical dimension that estimates the potential for therapeutic intervention to restore music reward. Computed as the product of residual connectivity and affect entropy. Both factors are necessary: some residual white matter integrity (connectivity > 0) provides the structural substrate for neuroplasticity, and some affective variability (entropy > 0) indicates the reward system is not completely abolished. A patient with zero connectivity has no pathway to recover; a patient with some connectivity but zero affect entropy may need stronger intervention. This dimension supports clinical decision-making for music-based neurofeedback (via CLAM) and pharmacological intervention.

2. **Anhedonia Probability (F1)**: The comprehensive diagnostic output — a single number estimating the probability of musical anhedonia. Weighted combination of three orthogonal markers: the anhedonia marker from extraction (40% weight, sigmoid-based FA estimate), the dissociation index (30% weight, music vs general reward gap), and the inverse of connectivity (30% weight, structural deficit). The sigmoid activation ensures a probabilistic output suitable for clinical thresholding. This is MAD's primary diagnostic export to the F10 (Clinical) meta-layer.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 11, 2, 0) | sensory_pleasantness std H11 L0 | Reward variability over 500ms for recovery estimation |
| (10, 16, 20, 0) | loudness entropy H16 L0 | Affect entropy over 1s for recovery potential |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [4] | sensory_pleasantness | F0: residual hedonic variability |
| [22] | distribution_entropy | F0: information content (preserved perception marker) |
| [21] | spectral_flux | F1: change detection (preserved) for diagnostic baseline |

---

## Scientific Foundation

- **Belfi & Loui 2020**: Musical anhedonia model — proposed framework for music reward restoration and neuroplasticity potential (review)
- **Loui et al. 2017**: White matter correlates of musical anhedonia — FA as structural biomarker (DTI + behavioral, N=17, d=-5.89)
- **Martinez-Molina et al. 2016**: NAcc-STG connectivity predicts music reward capacity (fMRI + DTI, N=45, r=0.61)
- **Jin et al. 2025**: Congenital amusia: lower music reward across all 5 BMRQ subscales; altered minor-key emotion (behavioral, N=88, significant)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/mad/forecast.py`
