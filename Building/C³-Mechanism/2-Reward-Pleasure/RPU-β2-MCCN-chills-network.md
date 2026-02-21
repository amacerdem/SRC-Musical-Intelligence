# Chills Network (Theta Contrast)

**Source**: RPU-β2-MCCN (Musical Chills Circuit Network)
**Unit**: RPU (Reward Processing Unit)
**Tier**: β (Integrative)
**Score**: 7/10 — State-dependent peak pleasure detection

---

## Scientific Basis

- Musical chills: peak pleasure moments with physiological markers
- Theta contrast: prefrontal increase + central decrease during chills
- Network: OFC, Insula, SMA, STG convergence

## Mechanism

Musical chills arise from peak pleasure combined with a specific theta-band
contrast pattern: prefrontal theta increases while central theta decreases.

### Formula

```
Chills_Magnitude = α·PeakPleasure + β·ThetaContrast + γ·ArousalIndex

ThetaContrast = Theta_Prefrontal_increase - Theta_Central_decrease

Parameters: α=1.0, β=0.8, γ=0.7

Temporal dynamics:
  dChills/dt = τ^(-1) · (Target_Magnitude - Current_Chills)
  τ = 3.0s
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| PeakPleasure | Reward signal | Current pleasure level |
| ThetaContrast | Theta-band activity | Prefrontal - central theta |
| ArousalIndex | Autonomic response | Current arousal level |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| chills_magnitude | [0, 1] | Chills intensity |
| theta_contrast | continuous | Prefrontal vs central theta |

## Why 7/10

- Theta contrast is a specific neural signature (not generic weighted avg)
- Subtraction operation (prefrontal - central) is a real mechanism
- τ=3.0s dynamics for chills persistence
- Multi-region convergence (OFC + Insula + SMA + STG)
- But PeakPleasure and ThetaContrast need upstream definitions
