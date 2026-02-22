# PNH H-Layer — Extraction (3D)

**Layer**: Harmonic (H)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | H0:ratio_encoding | [0, 1] | Pythagorean complexity proxy. sigma(0.75*(roughness_h10 + inharm_h10)/2). Low = simple ratio (consonant), High = complex ratio (dissonant). Bidelman & Krishnan 2009: log2(n*d) predicts FFR. |
| 1 | H1:conflict_response | [0, 1] | IFG/ACC conflict monitoring. sigma(0.70*energy_cons_coupling*roughness_h10). Dissonant > consonant activation. Kim 2021: R-IFG->L-IFG connectivity for syntactic irregularity. |
| 2 | H2:expertise_mod | [0, 1] | Training-dependent encoding modulation. sigma(0.60*stumpf_h10*(1-sethares)). Fusion * low-dissonance = musician sensitivity. Crespo-Bojorque 2018: musicians show pattern in more ROIs. |

---

## Design Rationale

Three features encoding the Pythagorean ratio complexity hierarchy:

1. **Ratio Encoding (H0)**: Average of roughness and inharmonicity at chord level (H10) captures the log2(n*d) complexity. Simple intervals (unison, octave, fifth) have low values; complex intervals (tritone, minor second) have high values. Alpha=0.75 scales the sigmoid input.

2. **Conflict Response (H1)**: Energy-consonance coupling (velocity_D * roughness, replacing dissolved x_l0l5) times chord-level roughness captures IFG/ACC activation for dissonant stimuli. Beta=0.70 controls conflict sensitivity.

3. **Expertise Modulation (H2)**: Tonal fusion (Stumpf) gated by low dissonance (1-Sethares). Musicians show this pattern in 5 ROIs; non-musicians in 1 ROI only. Gamma=0.60 weights the training effect.

---

## H3 Dependencies (H-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 10, 0, 2) | roughness value H10 L2 | Current dissonance at chord level |
| (5, 10, 0, 2) | inharmonicity value H10 L2 | Current ratio complexity |
| (3, 10, 0, 2) | stumpf value H10 L2 | Current tonal fusion |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 0 | roughness | Sensory dissonance (ratio complexity proxy) |
| 1 | sethares | Timbre-dependent dissonance (expertise gating) |
| 5 | inharmonicity | Ratio complexity proxy |
| 8 | velocity_D | Loudness — replaces dissolved x_l0l5 energy coupling |

Note: Model doc references `x_l0l5[25:33]` (dissolved E:Interactions group). Replaced with inline `velocity_D * roughness` energy-consonance coupling. Model doc `[10] loudness` corrected to `[8] velocity_D` (97D naming).

---

## Scientific Foundation

- **Bidelman & Krishnan 2009**: FFR responses follow Pythagorean hierarchy; NPS ordering matches music theory
- **Kim 2021**: R-IFG->L-IFG connectivity for syntactic irregularity (p=0.024 FDR)
- **Crespo-Bojorque 2018**: Musicians show consonance pattern in 5 vs 1 ROI

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/pnh/extraction.py`
