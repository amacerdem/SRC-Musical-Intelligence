# SDED M-Layer — Temporal Integration (1D)

**Layer**: Memory (M)
**Indices**: [3:4]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:detection_function | [0, 1] | Combined detection function. sigma(0.60*E0 + 0.40*E1). Integrates roughness encoding with deviance magnitude. |

---

## Design Rationale

Single composite detection function combining two E-layer signals:

1. **Detection Function (M0)**: Weighted sum of early detection (E0, 0.60) and MMN deviation (E1, 0.40). The 60/40 split reflects that direct roughness encoding is the primary brainstem signal, while MMN-based deviance provides contextual modulation. Conservative sigmoid: max input ~1.0, output ~[0.50, 0.73].

---

## H3 Dependencies

None. M-layer uses only E-layer outputs.

---

## Range Analysis

- M0 = sigmoid(0.60*sigmoid + 0.40*sigmoid) -> [sigma(0), sigma(1.0)] = [0.50, 0.73]

No clamping needed; output is naturally bounded.

---

## Scientific Foundation

- **Bidelman 2013**: Brainstem encodes consonance hierarchy innately — detection is bottom-up
- **Fishman 2001**: A1 integrates roughness encoding at early cortical level

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/sded/temporal_integration.py`
