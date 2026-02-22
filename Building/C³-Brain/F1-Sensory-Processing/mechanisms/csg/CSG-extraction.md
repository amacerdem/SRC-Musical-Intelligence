# CSG E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid (E0, E1), tanh (E2)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:salience_activation | [0, 1] | ACC/AI activation driven by dissonance. sigma(0.40*dissonance + 0.35*roughness_h0 + 0.25*loudness_entropy). Bravo 2017: strong dissonance -> ACC/bilateral AI, d=5.16. |
| 1 | E1:sensory_evidence | [0, 1] | Heschl's gyrus intermediate processing load. sigma(0.40*ambiguity + 0.35*sethares_h3 + 0.25*roughness_std). Bravo 2017: intermediate dissonance -> HG, d=1.9. |
| 2 | E2:consonance_valence | [-1, 1] | Consonance-valence mapping (tanh). tanh(0.50*pleas_vel + 0.50*pleas_mean_1s). Bravo 2017: linear consonance-valence trend, d=3.31. |

---

## Design Rationale

Three features model the consonance-salience gradient at the extraction level:

1. **Salience Activation (E0)**: Dissonance drives ACC/anterior insula activation — the core salience network. Roughness provides the brainstem-level sensory evidence, loudness entropy adds unpredictability-driven salience. Weights follow Bravo 2017's d=5.16 effect size for strong dissonance.

2. **Sensory Evidence (E1)**: Captures the inverted-U pattern where intermediate dissonance produces maximum Heschl's gyrus processing demand. Ambiguity (1 - |consonance - 0.5| * 2) peaks at intermediate levels. Sethares dissonance and roughness variability add spectral evidence.

3. **Consonance Valence (E2)**: Uses **tanh** activation for [-1, 1] valence mapping. Pleasantness velocity captures moment-by-moment valence change rate; sustained pleasantness (1s) provides the tonic context. Bravo 2017 confirmed linear consonance-valence relationship (d=3.31).

### Derived Signals

- `dissonance = 1.0 - pleas_h3` (from H3 pleasantness)
- `ambiguity = 1.0 - |pleas_h3 - 0.5| * 2` (peaks at intermediate consonance)

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 0, 0, 2) | roughness value H0 L2 | Instant roughness at brainstem timescale |
| (4, 3, 0, 2) | sensory_pleasantness value H3 L2 | Consonance proxy (also derives dissonance/ambiguity) |
| (10, 3, 13, 2) | loudness entropy H3 L2 | Salience unpredictability |
| (1, 3, 0, 2) | sethares_dissonance value H3 L2 | Psychoacoustic dissonance confirmation |
| (0, 3, 2, 2) | roughness std H3 L2 | Roughness variability — sensory evidence |
| (4, 3, 8, 2) | sensory_pleasantness velocity H3 L2 | Pleasantness change rate |
| (4, 16, 1, 2) | sensory_pleasantness mean H16 L2 | Sustained pleasantness over 1s |

## R3 Dependencies

None — E-layer uses only H3 features.

---

## Scientific Foundation

- **Bravo 2017**: Strong dissonance -> ACC/bilateral AI (d=5.16, fMRI N=12); intermediate dissonance -> HG (d=1.9); linear consonance-valence trend (d=3.31, p<0.01)
- **Fishman 2001**: Phase-locked A1 activity graded by consonance-dissonance
- **Cheung 2019**: Uncertainty (entropy) modulates salience response

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/csg/extraction.py`
