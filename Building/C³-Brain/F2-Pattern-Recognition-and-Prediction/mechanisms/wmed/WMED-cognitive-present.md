# WMED P-Layer — Cognitive Present (3D)

**Layer**: Cognitive Present (P)
**Indices**: [4:7]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 4 | P0:entrainment_level | [0, 1] | Current automatic entrainment activation. Real-time SS-EP strength reflecting how strongly the auditory cortex is locked to beat frequencies. High values indicate strong automatic motor coupling. Maps to fronto-central (Fz/FCz/Cz) SS-EP maximum (Noboa 2025, Ding 2025, Bridwell 2017). |
| 5 | P1:wm_activation | [0, 1] | Current WM engagement level. Real-time working memory contribution reflecting cognitive control load. High values indicate strong controlled processing. Maps to DLPFC (Noboa 2025), left medial frontal and parahippocampal cortex (Lu 2022). |
| 6 | P2:paradox_strength | [0, 1] | Current entrainment paradox strength. Product of high entrainment × low accuracy. When entrainment is strong but tapping is poor, the paradox is active. Noboa 2025: stronger SS-EP → worse tapping (p=0.015). Formula: entrainment × (1 − tapping_accuracy). |

---

## Design Rationale

1. **Entrainment Level (P0)**: Real-time automatic route activation. Aggregated from E-layer entrainment signals. Maps to the automatic SS-EP pathway via auditory cortex → motor coupling.

2. **WM Activation (P1)**: Real-time controlled route activation. Aggregated from E-layer WM signals. Maps to the cognitive control pathway via DLPFC → motor planning.

3. **Paradox Strength (P2)**: The key WMED insight — over-entrainment impairs motor accuracy. When entrainment is high but accuracy is low, the paradox is maximally expressed.

---

## H³ Demands

No additional unique H³ demands. Reuses E-layer tuples.

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No unique H³ demands; reuses E-layer tuples |

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | E0:entrainment_strength | Entrainment for level tracking |
| E-layer | E1:wm_contribution | WM for activation tracking |
| E-layer | E2:tapping_accuracy | Accuracy for paradox detection |
