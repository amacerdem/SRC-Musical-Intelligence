# PNH P-Layer — Cognitive Present (3D)

**Layer**: Present Processing (P)
**Indices**: [5:8]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:ratio_enc | [0, 1] | Current ratio encoding state. harmony.mean() — harmonic context summarizing current key/chord stability. Reflects how clearly the brain is encoding the current interval's position in the Pythagorean hierarchy. Tabas et al. 2019: consonant dyads produce earlier and larger POR in alHG (p<0.0001). |
| 6 | P1:conflict_mon | [0, 1] | Current conflict monitoring activation. pred_error.mean() — IFG/ACC signal representing the magnitude of conflict between heard interval and stored template. Kim et al. 2021: R-IFG to L-IFG connectivity for syntactic irregularity (p=0.024 FDR). |
| 7 | P2:consonance_pref | [0, 1] | Consonance-preference binding. struct_expect.mean() * (1-roughness). Links structural expectation with consonance to produce the preference signal. Sarasso et al. 2019: aesthetic appreciation of consonant intervals enhances attention (eta_p^2=0.685). |

---

## Design Rationale

1. **Ratio Encoding (P0)**: The present-moment encoding of harmonic context. Summarizes the current state of the Pythagorean hierarchy representation in the brain. High values indicate clear tonal context (strong key center), low values indicate ambiguous harmonic environment. Feeds downstream prediction and preference systems.

2. **Conflict Monitoring (P1)**: The real-time IFG/ACC conflict signal. Represents how much the current interval deviates from expected templates. High conflict (dissonant intervals in consonant context) drives attention allocation and prediction error. This is the primary signal for harmonic surprise detection.

3. **Consonance Preference (P2)**: The binding of structural expectation with perceptual consonance. This captures the aesthetic response — intervals that are both expected and consonant produce the highest preference. Unexpected consonance or expected dissonance produce intermediate values. This feeds the reward pathway for pleasure from harmonic resolution.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 18, 19, 0) | sensory_pleasantness stability H18 L0 | Consonance stability over phrase (2s) |
| (14, 10, 0, 2) | tonalness value H10 L2 | Ratio purity at chord level (400ms) |
| (17, 10, 14, 2) | spectral_autocorrelation periodicity H10 L2 | Harmonic regularity at chord level (400ms) |

---

## Scientific Foundation

- **Tabas et al. 2019**: Consonant dyads produce earlier (up to 36 ms) and larger POR in alHG (MEG+model, N=37, p<0.0001)
- **Kim et al. 2021**: IFG-LTDMI connectivity for syntactic irregularity; STG for perceptual ambiguity (MEG, N=19, p=0.024 FDR)
- **Sarasso et al. 2019**: Aesthetic appreciation of consonant intervals enhances attention and motor inhibition (EEG+behavioral, N=22, eta_p^2=0.685)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/pnh/cognitive_present.py`
