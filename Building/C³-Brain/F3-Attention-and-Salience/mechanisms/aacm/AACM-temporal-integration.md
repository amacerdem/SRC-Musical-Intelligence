# AACM M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:aesthetic_engagement | [0, 1] | Composite aesthetic engagement level. f(Consonance, Attention). Integrates consonance state with attentional capture to produce an overall engagement index. Sarasso 2019: consonance modulates N1/P2 which in turn modulates sustained engagement. |
| 4 | M1:rt_appreciation | [0, 1] | Reaction-time derived appreciation index. sigma(0.5*f18_savoring + 0.5*pleasant_value). Combines the behavioral RT slowing with the hedonic signal to estimate ongoing appreciation. Kim 2019: vmPFC activation (T=6.852) during aesthetic appreciation. |

---

## Design Rationale

1. **Aesthetic Engagement (M0)**: The core integration model — combines consonance-driven attention (E0) with the broader attentional state. This is the summary signal for "how engaged is the listener aesthetically?" High values mean both consonance is favorable and attention is captured. Feeds the P-layer for present-state estimation and the Appraisal belief `aesthetic_engagement`.

2. **RT Appreciation (M1)**: A behavioral proxy for ongoing appreciation. Reaction-time slowing (E2:savoring_effect) is combined equally with the pleasant value to form an appreciation estimate. This bridges the neural (ERP) and behavioral (RT) domains. Feeds the Appraisal belief `savoring_effect`.

---

## Mathematical Formulation

```
aesthetic_engagement = f(Consonance, Attention)
  = sigma(w_cons * consonance_state + w_att * attentional_engage)

rt_appreciation = sigma(0.5 * f18_savoring + 0.5 * pleasant_value)

Parameters:
  w_cons, w_att determined by consonance-attention coupling
  f18 = E2:savoring_effect (multiplicative attention * inhibition + velocity + integration)
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 3, 0, 2) | pleasant value H3 L2 | Pleasantness at 100ms — hedonic input to appreciation |
| (8, 3, 0, 2) | loudness value H3 L2 | Perceptual loudness at 100ms — engagement strength |
| (8, 3, 2, 2) | loudness std H3 L2 | Loudness variability 100ms — dynamic range |

M-layer primarily integrates E-layer outputs rather than reading many new H3 tuples directly.

---

## Scientific Foundation

- **Sarasso 2019**: Consonance modulates ERP amplitudes proportional to aesthetic preference (eta2p=0.685)
- **Kim 2019**: vmPFC activation during aesthetic judgments (fMRI, T=6.852)
- **Foo 2016**: RT slowing as behavioral marker of aesthetic appreciation

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/aacm/temporal_integration.py`
