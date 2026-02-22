# NEWMD M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [4:6]
**Scope**: internal
**Activation**: sigmoid
**Model**: STU-γ2 (Neural Entrainment-Working Memory Dissociation, 10D, γ-tier <70%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 4 | M0:paradox_magnitude | [0, 1] | Paradox signal: strong entrainment + low flexibility. M0 = f01*(1-f03). When entrainment is high but flexibility is low, the paradox is maximal — the system is "locked in" without adaptability. Sares 2023: paradoxical negative beta for entrainment. |
| 5 | M1:dual_route_balance | [0, 1] | Balance between dual routes. M1 = sigma(0.50*f01 + 0.50*f02). 0.5=equal engagement of both routes; 0=entrainment-only; 1=WM-only. Sares 2023: routes are independent but can be jointly engaged. |

---

## Design Rationale

1. **Paradox Magnitude (M0)**: The mathematical signature of the Sares 2023 paradox. Strong automatic entrainment (f01 high) combined with low flexibility (f03 low, so 1-f03 high) produces a large paradox signal. This captures the state where the listener is tightly locked to the beat but cannot adapt to tempo changes — the hallmark of "entrainment without benefit."

2. **Dual Route Balance (M1)**: A summary signal indicating which processing route dominates. Equal weighting (0.50/0.50) reflects the finding that entrainment and WM are independent predictors of similar magnitude but opposite sign. Values near 0.5 indicate balanced dual-route engagement; extreme values indicate one route dominating.

---

## Mathematical Formulation

```
Paradox Magnitude:
  M0 = f01 * (1 - f03)

  where:
    f01 = entrainment_strength (E0)
    f03 = flexibility_cost (E2)

  High M0 when: strong entrainment AND rigid (inflexible)
  Low M0 when: weak entrainment OR flexible

Dual Route Balance:
  M1 = sigma(0.50 * f01 + 0.50 * f02)

  where:
    f01 = entrainment_strength (E0)
    f02 = wm_capacity (E1)

  M1 ~ 0.5 when both routes equally engaged
  M1 ~ 0   when neither route active
  M1 ~ 1   when both routes saturated
```

---

## H3 Dependencies (M-Layer)

M-layer is purely computational from E-layer outputs. No direct H3 reads.

Indirect dependencies via E-layer:
| E-Layer Source | Feature | Purpose |
|---------------|---------|---------|
| E0 (f01) | entrainment_strength | Both M0 and M1 |
| E1 (f02) | wm_capacity | M1 balance |
| E2 (f03) | flexibility_cost | M0 paradox |

---

## Scientific Foundation

- **Sares et al. 2023**: The paradoxical finding — SS-EP (entrainment proxy) has negative beta for performance while WM capacity has positive beta. N=48, independent routes.
- **Noboa et al. 2025**: Exact replication with R²=0.316 confirms dual-route model.
- **Zanto et al. 2022**: RCT (d=0.52) supporting separable temporal attention mechanisms.
- **Scartozzi et al. 2024**: Cross-validation (beta r=0.42, N=57) of independent routes.

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/newmd/temporal_integration.py` (pending)
