# BARM M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:veridical_perception | [0, 1] | Combined veridical beat perception. sigma(0.5*f11 + 0.5*f12). alpha*BAT + beta*Exposure. Grahn & Brett 2007: veridical perception = alignment accuracy + synchronization ability. |
| 4 | M1:regularization_effect | [0, 1] | Regularization magnitude. sigma(0.5*f10 + 0.5*(1-f11)). Regularization strength scales inversely with alignment ability — low-BAT individuals show stronger regularization. Rathcke 2024: perceptual regularization exceeds production regularization. |

---

## Design Rationale

1. **Veridical Perception (M0)**: Integrates beat alignment (f11) and sync benefit (f12) into a unified "how accurately does this listener perceive the beat?" score. The alpha*BAT + beta*Exposure formulation reflects that veridical perception depends on both innate ability and exposure history. High values indicate accurate, non-regularized perception.

2. **Regularization Effect (M1)**: Quantifies the magnitude of perceptual regularization — the tendency to hear irregular rhythms as more regular than they are. Uses (1-f11) because regularization is strongest when alignment ability is weakest. This is the key individual-difference modulator for the BARM model.

---

## Mathematical Formulation

```
Veridical_Perception = sigma(alpha * BAT_score + beta * Sync_Benefit)

Parameters:
  alpha = 0.5 (alignment weight)
  beta  = 0.5 (sync benefit weight)

Regularization_Effect = sigma(gamma * Reg_Tendency + delta * (1 - BAT_score))

Parameters:
  gamma = 0.5 (tendency weight)
  delta = 0.5 (inverse-ability weight)

Constraint: Veridical + Regularization ~ 1 (approximately complementary)
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 3, 0, 2) | spectral_flux value H3 L2 | Instantaneous onset at 100ms — beat tracking |
| (7, 3, 0, 2) | amplitude value H3 L2 | Beat amplitude at 100ms — strength modulation |
| (22, 8, 8, 0) | energy_change velocity H8 L0 | Energy velocity at 500ms — regularization dynamics |
| (25, 8, 0, 2) | x_l0l5[0] value H8 L2 | Coupling value at 500ms — motor integration |

---

## Scientific Foundation

- **Grahn & Brett 2007**: Veridical perception correlates with SMA activation (fMRI, N=27)
- **Rathcke et al. 2024**: Regularization > production regularization, ER>19 threshold (N=87)
- **Lazzari et al. 2025**: TMS over dPMC disrupts beat alignment (OR=22.16), confirming motor-perception link
- **Niarchou et al. 2022**: Genetic basis for individual differences (GWAS, N=606k, h²=0.13-0.16)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/barm/temporal_integration.py`
