# Social Synchrony Reward

**Source**: RPU-β4-SSRI (Social Synchrony Reward Integration)
**Unit**: RPU (Reward Processing Unit)
**Tier**: β (Integrative)
**Score**: 9/10 — Multi-timescale state dynamics with social PE

---

## Scientific Basis

- Social music-making endorphin release literature
- Group synchronization → pain threshold elevation
- Dunbar social bonding hypothesis

## Mechanism

Social music synchronization amplifies individual reward via a social gain factor.
Three timescales: immediate coordination, endorphin accumulation (30s), social bonding (120s).

### Formula

```
R_social = R_individual × (1 + κ · Synchrony_Quality)

Social Prediction Error:
  SPE(t) = Coordination_Actual(t) - E[Coordination(t)]

Endorphin dynamics:
  dβ-endorphin/dt = τ_endo^(-1) · (Sustained_Synchrony - Current_Endorphin)
  τ_endo = 30.0s

Social bonding:
  dBond/dt = τ_bond^(-1) · (Endorphin × SharedAffect - Current_Bond)
  τ_bond = 120.0s

Group flow:
  Flow_Group = α·Entrainment × β·SharedAffect × γ·Challenge_Skill_Balance
  α=0.40, β=0.35, γ=0.25

Parameters:
  κ_social = 0.60 (social gain)
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| R_individual | Individual reward signal | Base hedonic response |
| Synchrony_Quality | Motor synchronization | Coordination quality |
| Coordination_Actual | Current sync state | Real-time coordination |
| SharedAffect | Group emotional state | Shared emotional response |
| Challenge_Skill_Balance | Csikszentmihalyi balance | Flow prerequisite |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| R_social | [0, R_ind × 1.6] | Socially amplified reward |
| SPE | unbounded | Social prediction error |
| β-endorphin | [0, 1] | Endorphin accumulation (30s) |
| Bond | [0, 1] | Social bonding (120s) |
| Flow_Group | [0, 1] | Group flow state |

## Why 9/10

- Three distinct timescales (immediate, 30s, 120s) — real multi-scale dynamics
- Social gain multiplicative (κ=0.60) — not additive
- Endorphin and bonding have differential equations with validated τ
- Social PE extends classical RPE to coordination domain
- Group flow via multiplicative gate (all three factors needed)
- Currently acoustic-proxy only, but mechanism is fully specified
