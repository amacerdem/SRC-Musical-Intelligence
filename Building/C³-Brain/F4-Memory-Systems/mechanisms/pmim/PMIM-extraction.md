# PMIM P-Layer — Prediction Features (3D)

**Layer**: Prediction (P)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | P0:f13_eran | [0, 1] | ERAN response: long-term syntax violation. IFG (Broca's area) activation. f13 = sigma(0.30 * entropy * harmony.mean * x_l5l7.mean). Max argument = 0.30. Koelsch 2000: ERAN elicited by Neapolitan sixth chords, peak 150-180ms, right-frontal maximum (EEG N=24, p<0.001). |
| 1 | P1:f14_mmn | [0, 1] | MMN response: short-term deviance detection. STG + IFG echoic mismatch. f14 = sigma(0.30 * flux * pred_error.mean * x_l0l5.mean). Max argument = 0.30. Wagner et al. 2018: MMN for harmonic interval deviants; consonance-dissonance asymmetry (EEG N=15). |
| 2 | P2:f15_pred_error | [0, 1] | Combined prediction error signal. IFG shared generator output. f15 = sigma(0.40 * pred_error.mean * (roughness + inharmonicity) / 2). Max argument = 0.40. Bonetti et al. 2024: hierarchical PE from auditory cortex to hippocampus to ACC (MEG N=83, p<0.001). |

---

## Design Rationale

1. **ERAN Response (P0)**: Captures long-term syntax violation — the "wrong chord in context" signal. ERAN requires stored harmonic rules (long-term memory) against which current input is compared. Uses entropy as unpredictability proxy, harmonic context from synthesis, and consonance-timbre interactions (x_l5l7) as high-level syntax template. The key insight: ERAN is memory-based prediction, not simple acoustic deviance.

2. **MMN Response (P1)**: Captures short-term deviance detection — the "that sound was different" signal. MMN operates on echoic memory (~10s window), comparing current input against recently established regularities. Uses spectral flux as change magnitude, prediction error from synthesis, and energy-consonance interactions (x_l0l5) as low-level sensory comparison substrate.

3. **Combined Prediction Error (P2)**: The integrated PE signal from shared IFG generators. Both ERAN and MMN converge on inferior fronto-lateral cortex. This combined signal weights PE by dissonance (roughness + inharmonicity average) — prediction violations in dissonant contexts produce larger error signals. This is the signal that drives downstream memory updating.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 10, 0, 2) | roughness value H10 L2 | Current dissonance at chord level (400ms) |
| (0, 14, 1, 0) | roughness mean H14 L0 | Average dissonance over progression (700ms) |
| (5, 10, 0, 2) | inharmonicity value H10 L2 | Current ratio deviation at chord level |
| (5, 14, 8, 0) | inharmonicity velocity H14 L0 | Rate of complexity change over progression |
| (22, 10, 0, 2) | entropy value H10 L2 | Current unpredictability at chord level |
| (21, 10, 0, 2) | spectral_flux value H10 L2 | Current change magnitude at chord level |
| (21, 14, 8, 0) | spectral_flux velocity H14 L0 | Acceleration of change over progression |
| (11, 10, 0, 2) | onset_strength value H10 L2 | Onset salience for MMN triggering |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | P2: sensory dissonance for PE weighting |
| [5] | inharmonicity | P2: harmonic template deviation |
| [21] | spectral_flux | P1: change detection (MMN basis) |
| [22] | entropy | P0: syntactic unpredictability (ERAN basis) |
| [25:33] | x_l0l5 | P1: sensory-level prediction coupling (MMN) |
| [41:49] | x_l5l7 | P0: high-level syntactic prediction (ERAN) |

---

## Scientific Foundation

- **Koelsch et al. 2000**: EEG N=24, ERAN elicited by Neapolitan sixth chords, peak 150-180ms, right-frontal (p<0.001)
- **Koelsch 2009**: Review, ERAN generators in inferior BA 44 bilateral; ERAN based on long-term stored rules vs MMN on-line regularity; shared predictive processes
- **Wagner et al. 2018**: EEG N=15, MMN for harmonic interval deviants; consonance-dissonance asymmetry
- **Bonetti et al. 2024**: MEG N=83, hierarchical PE: auditory cortex to hippocampus to ACC/MCC (p<0.001)
- **Garrido et al. 2009**: DCM/fMRI N=16, hierarchical predictive coding explains MMN; forward PE + backward predictions

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/pmim/extraction.py`
