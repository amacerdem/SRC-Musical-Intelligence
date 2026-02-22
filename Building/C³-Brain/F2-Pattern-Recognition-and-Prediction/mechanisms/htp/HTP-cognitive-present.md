# HTP P-Layer — Cognitive Present (3D)

**Layer**: Present (P)
**Indices**: [7:10]
**Scope**: hybrid
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | P0:sensory_match | [0, 1] | Low-level prediction match. sigma(0.40*M2 + 0.30*amplitude_H3 + 0.30*onset_H0). Forseth 2020: HG timing prediction + PT content. Persists post-stimulus as PE. |
| 8 | P1:pitch_prediction | [0, 1] | Mid-level pitch template match. sigma(0.40*M1 + 0.30*sharpness_H3 + 0.30*spectral_auto_H3). Planum temporale high-gamma for content prediction. |
| 9 | P2:abstract_prediction | [0, 1] | High-level abstract pattern match. sigma(0.40*M0 + 0.30*tonal_stability_H8 + 0.30*trist_mean). Bonetti 2024: hippocampus/cingulate sequence recognition. Silenced post-stimulus when correct. |

---

## Design Rationale

Post-stimulus silencing asymmetry (de Vries & Wurm 2023):
- **P2 (abstract)**: Silenced when prediction is correct — "explained away"
- **P0 (sensory)**: Persists regardless — prediction error signal

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (7, 3, 0, 2) | amplitude value H3 L2 | 100ms amplitude context |
| (11, 0, 0, 2) | onset_strength value H0 L2 | Instant onset |
| (13, 3, 0, 2) | sharpness value H3 L2 | Brightness at 100ms |
| (17, 3, 0, 2) | spectral_auto value H3 L2 | Cross-band coupling (reused) |
| (60, 8, 0, 0) | tonal_stability value H8 L0 | 500ms structure (reused) |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 18:21 | tristimulus1-3 | P2: abstract harmonic balance (reused) |

## Implementation

File: `Musical_Intelligence/brain/functions/f2/mechanisms/htp/cognitive_present.py`
