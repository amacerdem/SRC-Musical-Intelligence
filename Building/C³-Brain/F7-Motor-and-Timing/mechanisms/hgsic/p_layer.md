# HGSIC — Cognitive Present

**Model**: Hierarchical Groove State Integration Circuit
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: β
**Layer**: P — Cognitive Present
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 5 | pstg_activation | pSTG current activation state. Measures real-time intensity tracking by posterior superior temporal gyrus high-gamma (70-170 Hz). Driven by amplitude × loudness at beat level (H6). Potes 2012: pSTG gamma tracks sound intensity at r = 0.49 (ECoG, N=8). Maps to pSTG. |
| 6 | motor_preparation | Premotor preparation state. Measures readiness of the motor system to entrain to the groove. Combines motor entrainment context with meter integration (f02). The 110ms delay from pSTG to premotor cortex means motor preparation reflects slightly delayed auditory state. Maps to dorsal precentral gyrus / premotor cortex. |
| 7 | onset_sync | Onset synchronization signal. Measures precision of beat-level event detection from spectral flux × onset strength at H6. High values indicate sharp, well-defined onsets that facilitate motor synchronization. Maps to the dorsal auditory-motor pathway onset detection circuit. |

---

## H³ Demands

No additional unique H³ demands beyond E/M layers. The P-layer reuses:
- amplitude value from (7, 6, M0, L0)
- loudness value from (8, 6, M0, L0)
- spectral_flux value from (10, 6, M0, L0)
- onset_strength value from (11, 6, M0, L0)

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No unique H³ demands; reuses E/M layer tuples |

---

## Computation

The P-layer computes the real-time state of the groove integration system:

1. **pSTG activation** (idx 5): Current auditory gamma state from amplitude × loudness at beat level. Higher when stimulus is strong and well-defined. Reflects the bottom-up intensity tracking that initiates the groove cascade. Formula: σ(0.5 × amp_val × loud_val).

2. **Motor preparation** (idx 6): Premotor readiness state from motor entrainment × meter context. Combines beat-level motor coupling with f02 meter integration, reflecting the 110ms-delayed motor response to auditory input. Higher when both auditory input is strong and metrical structure is clear.

3. **Onset synchronization** (idx 7): Beat-event detection precision from spectral flux × onset strength at H6. Sharp, clear onsets produce high values, enabling precise motor synchronization. Formula: σ(0.50 × flux_val × onset_val).

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01, f02 | Beat gamma and meter integration for motor preparation |
| M-layer | groove_index | Overall groove state context |
| R³ [7] | amplitude | Current stimulus strength |
| R³ [8] | loudness | Perceptual intensity |
| R³ [10] | spectral_flux | Onset detection |
| R³ [11] | onset_strength | Event boundary precision |
| H³ (shared) | Reuses E-layer tuples | Current-state features at H6 |
