# PNH H-Layer — Extraction (3D)

**Layer**: Harmonic Encoding (H)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | H0:f04_ratio | [0, 1] | Pythagorean ratio complexity encoding. sigma(0.75 * (roughness + inharmonicity) / 2). Low = simple ratio (consonant), High = complex ratio (dissonant). Bidelman & Krishnan 2009: brainstem FFR responses follow Pythagorean hierarchy; NPS ordering matches music theory (r >= 0.81). |
| 1 | H1:f05_conflict | [0, 1] | Conflict monitoring response (IFG/ACC). sigma(0.70 * pred_error * x_l0l5.mean * roughness). Dissonant intervals produce stronger activation than consonant. Kim et al. 2021: R-IFG to L-IFG connectivity for syntactic irregularity (p=0.024 FDR). |
| 2 | H2:f06_expertise | [0, 1] | Training-dependent encoding modulation. sigma(0.60 * familiarity * (1-sethares) * training). Musicians: 5 ROIs (L-IFG, L-STG, L-MFG, L-IPL, ACC). Non-musicians: 1 ROI (R-IFG only). Crespo-Bojorque et al. 2018: consonance-context MMN in all; dissonance-context MMN only in musicians. |

---

## Design Rationale

1. **Ratio Complexity (H0)**: The core encoding feature of the Pythagorean hierarchy. Measures the complexity of the current frequency ratio by combining roughness (critical-band beating) and inharmonicity (deviation from harmonic series). Simple ratios like octaves (2:1) produce low values; complex ratios like tritones (45:32) produce high values. This proxy tracks log2(n*d) because roughness is proportional to ratio complexity (Plomp & Levelt 1965).

2. **Conflict Monitoring (H1)**: Tracks IFG/ACC activation during dissonant intervals. Conflict arises when current interval violates the stored template hierarchy — complex ratios generate prediction error that activates conflict monitoring regions. Uses the energy-consonance interaction (x_l0l5) as pitch-dissonance coupling signal.

3. **Expertise Modulation (H2)**: Captures the training-dependent expansion of Pythagorean encoding. Musical training expands the cortical representation from 1 ROI (R-IFG) to 5 ROIs. Uses familiarity and inverse-sethares as proxies for trained template matching. This is fundamentally a plasticity/learning feature.

---

## H3 Dependencies (H-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 10, 0, 2) | roughness value H10 L2 | Current dissonance at chord level (400ms) |
| (0, 14, 1, 0) | roughness mean H14 L0 | Average dissonance over progression (700ms) |
| (5, 10, 0, 2) | inharmonicity value H10 L2 | Current ratio complexity (400ms) |
| (5, 14, 1, 0) | inharmonicity mean H14 L0 | Average complexity over progression (700ms) |
| (3, 10, 0, 2) | stumpf_fusion value H10 L2 | Current tonal fusion (400ms) |
| (10, 10, 0, 2) | loudness value H10 L2 | Attention weight (400ms) |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | H0+H1: sensory dissonance proportional to ratio complexity |
| [1] | sethares_dissonance | H2: timbre-dependent dissonance for expertise |
| [5] | inharmonicity | H0: ratio complexity proxy |
| [6] | harmonic_deviation | H0: error from ideal harmonics |
| [14] | tonalness | H2: harmonic-to-noise ratio purity |
| [25:33] | x_l0l5 | H1: pitch-roughness coupling for conflict |

---

## Scientific Foundation

- **Bidelman & Krishnan 2009**: Brainstem FFR responses follow Pythagorean hierarchy; NPS correlation r >= 0.81 (brainstem FFR, N=10)
- **Crespo-Bojorque et al. 2018**: Consonance-context MMN in all; dissonance-context MMN only in musicians (EEG oddball, N=32)
- **Kim et al. 2021**: R-IFG to L-IFG connectivity for syntactic irregularity (MEG connectivity, N=19, p=0.024 FDR)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/pnh/extraction.py`
