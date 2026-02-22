# ETAM M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [4:6]
**Scope**: internal
**Activation**: sigmoid
**Model**: ETAM (STU-B4, Entrainment Tempo & Attention Modulation, 11D, beta-tier 70-90%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 4 | M0:attention_gain | [0, 1] | 0.60 * (f01 + f02 + f03) / 3. Attention-modulated tracking gain, averaging the three temporal windows into a unified gain signal. Effect size d=0.60 from Hausfeld 2021. The weighted average across windows captures the full cascade of attentional processing. |
| 5 | M1:entrainment_index | [0, 1] | sigma(0.5*energy_period + 0.5*bar_period). Beat entrainment strength — how strongly internal oscillations synchronize to the external rhythm. Combines energy periodicity at beat level with coupling periodicity at bar level. Doelling & Poeppel 2015: entrainment index predicts musical tracking. |

---

## Design Rationale

1. **Attention Gain (M0)**: Integrates the three temporal windows (early E0, middle E1, late E2) into a single gain factor. The 0.60 scaling reflects the empirical effect size from Hausfeld 2021 — attentional modulation produces a consistent d=0.60 enhancement. This is the "how much attention is being deployed" signal, independent of what is being attended.

2. **Entrainment Index (M1)**: Measures the synchronization strength between internal neural oscillations and external musical rhythm. Energy periodicity captures beat-level entrainment (is the energy pattern periodic?), while bar-level coupling periodicity captures hierarchical entrainment (is there meter-level structure?). Equal weights reflect the finding that beat and bar entrainment contribute equally to overall synchronization.

---

## Mathematical Formulation

```
attention_gain = 0.60 * (E0 + E1 + E2) / 3

Parameters:
  0.60 = scaling factor (Hausfeld 2021 effect size d=0.60)
  Equal window weights = 1/3 each (three delay windows contribute equally)

entrainment_index = sigma(0.5 * energy_periodicity + 0.5 * bar_periodicity)

H3 inputs:
  energy_periodicity = (22, 11, 14, 2)  energy_change periodicity H11 L2
  bar_periodicity    = (25, 16, 14, 2)  x_l0l5 periodicity H16 L2
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (22, 11, 14, 2) | energy_change periodicity H11 L2 | M1: beat-level periodicity in energy |
| (25, 16, 14, 2) | x_l0l5 periodicity H16 L2 | M1: bar-level periodicity in coupling |

M0 (attention_gain) has no direct H3 dependencies — it integrates E-layer outputs only.

---

## Scientific Foundation

- **Hausfeld et al. 2021**: Attentional modulation d=0.60-0.68 across three delay windows (fMRI, N=14)
- **Doelling & Poeppel 2015**: Neural entrainment to musical rhythm predicts tracking accuracy (MEG)
- **Aparicio-Terres et al. 2025**: Tempo modulates entrainment — 1.65 Hz > 2.85 Hz for coupling strength

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/etam/temporal_integration.py`
