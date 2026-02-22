# CSG P-Layer — Cognitive Present (3D)

**Layer**: Present (P)
**Indices**: [6:9]
**Scope**: hybrid
**Activation**: sigmoid (P0, P2), tanh (P1)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 6 | P0:salience_network | [0, 1] | Attention-gated salience. sigma(0.30*M0 + 0.25*spectral_auto_h3 + 0.25*loudness_h3 + 0.20*energy_vel). Koelsch 2006: dissonant -> amygdala/hippocampus; consonant -> AI/HG/NAc. |
| 7 | P1:affective_evaluation | [-1, 1] | Salience-weighted valence (tanh). tanh(0.50*E2 + 0.30*(pleas_h3-roughness_mean) + 0.20*spectral_flux_vel). Kim 2017: vmPFC/NAc valence integration. |
| 8 | P2:sensory_load | [0, 1] | Processing demand. sigma(0.30*ambiguity + 0.25*sethares_vel + 0.25*spectral_auto_h8 + 0.20*loudness_mean_1s). Bravo 2017: intermediate dissonance -> increased HG load. |

---

## Design Rationale

Three present-processing dimensions:

1. **Salience Network (P0)**: Attention-gated integration of M-layer salience response with multi-scale sensory evidence. Spectral autocorrelation (100ms) captures cross-band salience coupling — how different frequency bands contribute to unified percept. Loudness provides intensity-driven salience, energy velocity captures dynamic change. This is the primary output consumed by the consonance_salience_gradient belief.

2. **Affective Evaluation (P1)**: Uses **tanh** for [-1, 1] valence range. Inherits E2's consonance-valence mapping, adds the consonance-minus-roughness contrast (how far current pleasantness exceeds roughness context), and spectral flux velocity for timbral change-driven affect. Kim 2017 localizes this to vmPFC/NAc interaction.

3. **Sensory Load (P2)**: Processing demand from intermediate dissonance. Ambiguity captures the inverted-U; dissonance velocity (sethares at 500ms) adds the dynamics of dissonance change; spectral autocorrelation at medium term (500ms) provides structural complexity. Sustained loudness adds sustained intensity load.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (17, 3, 0, 2) | spectral_autocorrelation value H3 L2 | Cross-band salience coupling at 100ms |
| (10, 3, 0, 2) | loudness value H3 L2 | Intensity for salience |
| (22, 3, 8, 0) | energy_change velocity H3 L0 | Energy dynamics |
| (4, 3, 0, 2) | sensory_pleasantness value H3 L2 | Consonance (reused) |
| (0, 3, 1, 2) | roughness mean H3 L2 | Dissonance context (reused) |
| (21, 4, 8, 0) | spectral_flux velocity H4 L0 | Spectral change dynamics |
| (1, 8, 8, 0) | sethares_dissonance velocity H8 L0 | Dissonance velocity at 500ms |
| (17, 8, 0, 2) | spectral_autocorrelation value H8 L2 | Medium-term coupling |
| (10, 16, 1, 2) | loudness mean H16 L2 | Sustained intensity |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 4 | sensory_pleasantness | P1: consonance for ambiguity computation |

---

## Scientific Foundation

- **Koelsch 2006**: Dissonant -> amygdala/hippocampus; consonant -> AI/HG/ventral striatum (fMRI, N=11)
- **Kim 2017**: vmPFC/NAc interaction for spectral-temporal reward integration; dissonance -> decreased STG/insula BOLD
- **Bravo 2017**: Intermediate dissonance -> increased HG processing load (d=1.9)

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/csg/cognitive_present.py`
