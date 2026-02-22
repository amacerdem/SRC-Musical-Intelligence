# CSG M-Layer — Temporal Integration (3D)

**Layer**: Memory (M)
**Indices**: [3:6]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:salience_response | [0, 1] | Graded salience network response. sigma(0.50*E0 + 0.30*E1 + 0.20*roughness_mean_1s). Bravo 2017: graded ACC/AI -> HG -> baseline across levels. |
| 4 | M1:rt_valence_judgment | [0, 1] | Inverted-U RT function for valence judgments. sigma(0.40*ambiguity + 0.30*E1 + 0.30*centroid_h3). Bravo 2017: RT_intermediate=6792ms > RT_consonant=4333ms. |
| 5 | M2:aesthetic_appreciation | [0, 1] | Consonance preference index. sigma(0.40*consonance + 0.30*pleas_mean_1s + 0.30*warmth). Sarasso 2019: consonant > dissonant, d=2.008. |

---

## Design Rationale

Three temporal integration signals:

1. **Salience Response (M0)**: Integrates E-layer salience activation (E0) and sensory evidence (E1) with long-range roughness context (1s). E0 dominates (50%) because the salience gradient is the model's core computation. The 1s roughness context (H16) prevents momentary spikes from dominating.

2. **RT Valence Judgment (M1)**: Models the behavioral finding from Bravo 2017 that intermediate dissonance produces the longest reaction times (6792ms vs 4333ms for consonant). The ambiguity signal captures this inverted-U: ambiguity peaks at intermediate consonance/dissonance levels. Spectral centroid adds brightness-based cognitive load.

3. **Aesthetic Appreciation (M2)**: Direct consonance-preference mapping per Sarasso 2019 (d=2.008). Consonance (pleasantness) is the primary driver (40%), with sustained pleasantness providing temporal context and warmth adding timbral quality. This feeds the F-layer's aesthetic prediction.

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 16, 1, 2) | roughness mean H16 L2 | Long-range roughness context over 1s |
| (9, 3, 0, 2) | spectral_centroid value H3 L2 | Brightness for RT cognitive load |
| (4, 16, 1, 2) | sensory_pleasantness mean H16 L2 | Sustained pleasantness (reused) |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 4 | sensory_pleasantness | M2: consonance proxy for aesthetic appreciation |
| 12 | warmth | M2: spectral envelope quality for aesthetics |

---

## Scientific Foundation

- **Bravo 2017**: Graded salience response across consonance levels; RT_intermediate=6792ms > RT_consonant=4333ms (N=45 behavioral)
- **Sarasso 2019**: Consonant > dissonant aesthetic appreciation (d=2.008, p<0.001, N=22)

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/csg/temporal_integration.py`
