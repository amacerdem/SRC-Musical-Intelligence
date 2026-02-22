# HCMC M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid / clamp

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:consolidation_str | [0, 1] | Hippocampal-to-cortical transfer strength. f(Encoding_Strength x Pattern_Stability) x stumpf_fusion. McClelland et al. 1995: complementary learning systems -- fast hippocampal + slow cortical. Buzsaki 2015: sharp-wave ripples drive hippocampal-cortical transfer. |
| 4 | M1:encoding_rate | [0, 1] | Rate of new episodic trace formation. sigma(0.35 * flux + 0.35 * onset_str + 0.30 * loudness). Event-driven: high flux and onsets trigger stronger encoding. Squire & Alvarez 1995: hippocampal-cortical consolidation rate. |

---

## Design Rationale

1. **Consolidation Strength (M0)**: The core computational model for hippocampal-cortical memory transfer. Combines encoding strength (from E-layer binding) with pattern stability (how consistent the harmonic signal is over time), gated by tonal fusion (stumpf). This models the empirical finding that coherent musical patterns consolidate more effectively than noisy ones.

2. **Encoding Rate (M1)**: An event-driven measure of how rapidly new episodic traces are being formed. High spectral flux (event boundaries) and strong onsets drive faster encoding, modulated by loudness as an arousal correlate. This captures the finding that event-rich musical passages create more distinct memory traces per unit time.

---

## Mathematical Formulation

```
Consolidation(music) = f(Encoding_Strength x Pattern_Stability x Time)

Encoding_Strength = encoding_state.mean() x binding_coherence
Pattern_Stability = familiarity_proxy.mean() x (1 - entropy)
binding_coherence = R3.stumpf_fusion[3] x mean(R3.x_l0l5[25:33])

consolidation_str = (Encoding_Strength x Pattern_Stability x stumpf).clamp(0, 1)

encoding_rate = sigma(0.35 * flux + 0.35 * onset_str + 0.30 * loudness)
  coefficients: |0.35| + |0.35| + |0.30| = 1.00 <= 1.0

Temporal dynamics:
  dConsolidation/dt = alpha * (Encoding - Consolidation) + beta * Pattern_Stability
  where alpha = hippocampal replay rate, beta = cortical integration rate
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 20, 1, 0) | stumpf_fusion mean H20 L0 | Binding stability over 5s consolidation window |
| (3, 24, 19, 0) | stumpf_fusion stability H24 L0 | Long-term binding stability over 36s |
| (22, 20, 13, 0) | entropy entropy H20 L0 | Entropy of entropy over 5s (pattern regularity) |
| (22, 24, 19, 0) | entropy stability H24 L0 | Pattern stability over 36s |
| (21, 20, 5, 0) | spectral_flux range H20 L0 | Flux dynamic range over 5s |
| (11, 20, 5, 0) | onset_strength range H20 L0 | Onset dynamic range over 5s |
| (10, 20, 1, 0) | loudness mean H20 L0 | Average salience over 5s |

---

## Scientific Foundation

- **McClelland et al. 1995**: Complementary learning systems -- fast hippocampal + slow cortical integration (computational)
- **Squire & Alvarez 1995**: Hippocampal-cortical consolidation theory (review/lesion)
- **Buzsaki 2015**: Sharp-wave ripples drive hippocampal-cortical transfer (review)
- **Liu et al. 2024**: Memory replay events trigger heightened hippocampal and mPFC activation (EEG-fMRI, N=33)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/hcmc/temporal_integration.py`
