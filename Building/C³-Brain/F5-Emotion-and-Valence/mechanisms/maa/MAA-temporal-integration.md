# MAA — Temporal Integration (0D)

**Layer**: Mathematical Model (M)
**Indices**: (none — MAA has no dedicated M-layer)
**Scope**: internal
**Activation**: N/A

---

## Output Dimensions

MAA does not define a separate mathematical / temporal-integration layer. The model uses a 3-layer structure (E, P, F) rather than the 4-layer structure (E, M, P, F) used by some other mechanisms.

The temporal integration function is embedded within the E-layer's appreciation composite (E3:f04_appreciation_composite), which multiplicatively integrates the three factors:

```
f04 = sigma(0.35 * f01 * f02 + 0.35 * f03)

where:
  f01 = complexity_tolerance (entropy-based)
  f02 = familiarity_index (trend + periodicity-based)
  f03 = framing_effect (tonalness + change-based)
```

This follows the Mencke 2019 multifactorial model: `Appreciation = f(Complexity x Tolerance x Framing x Exposure)`.

---

## Design Rationale

1. **No Separate M-Layer**: MAA's mathematical integration is lightweight compared to models that require explicit temporal dynamics (e.g., MEAMN's retrieval function and recall probability). The three-factor model is fully captured by the E-layer formulas. The interaction term (f01 * f02) within f04 provides the essential multiplicative binding between complexity tolerance and familiarity.

2. **Temporal Dynamics via H3**: The temporal integration that would otherwise require an M-layer is delegated to the H3 temporal features. The 1s entropy and trend tuples (H16) provide the medium-term temporal context, and the 500ms mean tuples (H8) provide short-term dynamics. This sparse H3 demand (14 tuples) replaces what would otherwise be an explicit temporal integration layer.

3. **Appreciation = Interaction, Not Summation**: The critical design choice is the multiplicative interaction (f01 * f02) rather than additive combination. This captures the finding from Cheung 2019 that the uncertainty x surprise interaction term is essential — neither factor alone predicts pleasure. The saddle-shaped pleasure surface requires multiplication.

---

## H3 Dependencies (Temporal Integration)

No additional H3 tuples beyond those consumed by the E-layer. The temporal integration function reuses:

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (41, 16, 18, 0) | x_l5l7[0] trend H16 L0 | Familiarity trajectory over 1s |
| (4, 16, 20, 0) | sensory_pleasantness entropy H16 L0 | Complexity trajectory over 1s |
| (41, 16, 20, 0) | x_l5l7[0] entropy H16 L0 | Coupling complexity trajectory over 1s |

---

## Scientific Foundation

- **Mencke et al. 2019**: Multifactorial appreciation model: openness x framing x exposure interact multiplicatively (MIR corpus, N=100 excerpts, d=3.0 key clarity)
- **Cheung et al. 2019**: Saddle-shaped pleasure surface; interaction term essential beyond main effects (fMRI, N=39+40, R2_marginal=0.476)
- **Gold et al. 2019**: IC x entropy quadratic interaction on liking replicated across experiments (behavioral + IDyOM, N=43+27, p<0.05)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/maa/temporal_integration.py`

Note: This file implements a pass-through that delegates to E-layer outputs. No independent computation.
