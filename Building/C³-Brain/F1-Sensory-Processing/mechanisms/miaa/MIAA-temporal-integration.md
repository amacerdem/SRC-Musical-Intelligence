# MIAA M-Layer — Temporal Integration (2D)

**Layer**: Memory (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: weighted sum / product (no sigmoid)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|------------------|
| 3 | M0:activation_function | [0, 1] | Composite AC activation. 0.60×E0 + 0.40×E2. Combines general imagery (BA22) and A1-specific modulation. |
| 4 | M1:familiarity_effect | [0, 1] | Familiarity enhancement magnitude. E1 × E0. Product ensures both familiarity and base activation must be present. |

---

## Design Rationale

The M-layer performs two simple composite operations:

1. **Activation Function (M0)**: Weighted sum of imagery activation (E0, weight 0.60) and A1 modulation (E2, weight 0.40). The 60/40 split reflects that general BA22 imagery activation is more universal than the A1-specific instrumental modulation (which depends on content type).

2. **Familiarity Effect (M1)**: Multiplicative gating — familiarity enhancement (E1) is scaled by base imagery activation (E0). This ensures that familiarity only matters when there's active imagery. Without imagery (E0≈0), even strong familiarity produces no effect.

---

## H³ Dependencies

None. M-layer uses only E-layer outputs.

---

## Range Analysis

- M0 = 0.60×sigmoid + 0.40×sigmoid → [0, 1] ✓
- M1 = sigmoid × sigmoid → [0, 1] ✓

No clamping needed; both outputs are naturally bounded.

---

## Scientific Foundation

- **Kraemer 2005**: Familiar + instrumental = highest activation; unfamiliar + lyrics = minimal
- The composite structure mirrors the 2×2 factorial design (familiar/unfamiliar × instrumental/lyrics)

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/miaa/temporal_integration.py`
