# PWUP P-Layer — Cognitive Present (3D)

**Layer**: Cognitive Present (P)
**Indices**: [4:7]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 4 | P0:tonal_precision_weight | [0, 1] | Current tonal precision weight. Direct pass-through of E0 tonal_precision as real-time weighting factor. High = tonal context active, PE fully weighted. Maps to IFG top-down precision modulation. |
| 5 | P1:rhythmic_precision_weight | [0, 1] | Current rhythmic precision weight. Direct pass-through of E1 rhythmic_precision as real-time weighting factor. High = regular rhythm active, temporal PE fully weighted. Maps to BG/SMA precision for timing. |
| 6 | P2:attenuated_pe | [0, 1] | Current precision-attenuated PE. Direct pass-through of E2 weighted_error as real-time PE magnitude. Represents the moment-by-moment precision-weighted prediction error signal sent to downstream models. |

---

## Design Rationale

1. **Tonal Precision Weight (P0)**: The current tonal precision level determines how strongly harmonic prediction errors are weighted. Real-time proxy for IFG precision estimation (Koelsch: ERAN generator).

2. **Rhythmic Precision Weight (P1)**: The current rhythmic precision level determines temporal PE weighting. Real-time proxy for BG beat-tracking precision.

3. **Attenuated PE (P2)**: The final precision-weighted PE that downstream models consume. This is the key PWUP output — PE that has been modulated by contextual uncertainty. Bravo 2017: heightened sensory cortical response under uncertainty in R Heschl's Gyrus.

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
| E-layer | E0:tonal_precision | Tonal weighting |
| E-layer | E1:rhythmic_precision | Rhythmic weighting |
| E-layer | E2:weighted_error | Precision-attenuated PE |
