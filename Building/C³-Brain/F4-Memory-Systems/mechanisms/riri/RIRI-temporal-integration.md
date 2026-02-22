# RIRI M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid / geometric mean

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:integration_synergy | [0, 1] | Multi-modal integration synergy index. Geometric mean of entrainment x integration x recovery: synergy = (f01 * f02 * f03) ^ (1/3). The geometric mean ensures all three components must contribute -- if any pathway fails, overall integration collapses. Models the empirical finding that multi-modal > unimodal. Jiao 2025: multi-modal synergy enhances outcomes. |
| 4 | M1:temporal_coherence | [0, 1] | Cross-modal temporal coherence. sigma(0.5 * entrainment_stability + 0.5 * onset_periodicity). Measures how tightly all modality channels maintain phase-locked timing. High coherence = effective rehabilitation. Ross & Balasubramaniam 2022: cerebellar forward models for predictive timing. |

---

## Design Rationale

1. **Integration Synergy (M0)**: The core computational output -- captures the multiplicative benefit of combining RAS + VR + robotics. Using the geometric mean (cube root of product) ensures that all three E-layer signals must be present for high synergy. If entrainment is strong but sensorimotor integration is zero, synergy collapses to zero. This models the empirical finding that synchronized multi-modal stimulation outperforms any single modality.

2. **Temporal Coherence (M1)**: Measures the degree to which all modality channels maintain phase-locked timing. Uses entrainment stability (H16, x_l0l5 stability) and onset periodicity (H6). High temporal coherence means the RAS master clock is effectively synchronizing VR and haptic channels. This is the prerequisite for integration synergy.

---

## Mathematical Formulation

```
Integration_Synergy(t) = (Entrainment(t) * SensorimotorInteg(t) * Recovery(t)) ^ (1/3)

  Entrainment = f01 (E-layer output)
  SensorimotorInteg = f02 (E-layer output)
  Recovery = f03 (E-layer output)

Temporal_Coherence(t) = sigma(0.5 * stability + 0.5 * onset_periodicity)
  coefficients: |0.50| + |0.50| = 1.00 <= 1.0

Key property: Geometric mean ensures ALL components must contribute.
  If any f_i = 0, synergy = 0 (system-level failure)
  If all f_i = 1, synergy = 1 (maximum integration)
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (25, 16, 19, 0) | x_l0l5[0] stability H16 L0 | Entrainment stability over 1s |
| (11, 6, 14, 2) | onset_strength periodicity H6 L2 | Rhythmic regularity at beat level |

M-layer primarily computes from E-layer outputs rather than reading many new H3 tuples directly.

---

## Scientific Foundation

- **Jiao 2025**: Multi-modal synergy (music therapy + entrainment + multisensory) enhances outcomes (review)
- **Ross & Balasubramaniam 2022**: Cerebellar forward models for predictive timing (review)
- **Liuzzi et al. 2025**: Multimodal orchestral therapy engages fronto-striatal, cerebellar networks (framework)
- **Liang et al. 2025**: Music + VR convergent activation exceeds unimodal (fNIRS, N=26)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/riri/temporal_integration.py`
