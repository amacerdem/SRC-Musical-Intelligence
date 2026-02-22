# CSSL M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:conservation_index | [0, 1] | Cross-species conservation strength. How "universal" the current musical pattern is. conservation = sigma(0.35 * stumpf + 0.35 * harmonicity + 0.30 * tonalness). Zhang et al. 2024: homologous auditory dorsal/ventral pathways across 3 primate species (dMRI, N=21). |
| 4 | M1:template_fidelity | [0, 1] | Song template match quality. sigma(0.50 * familiarity.mean + 0.30 * (1 - entropy) + 0.20 * stumpf). Lipkind et al. 2013: stepwise vocal combinatorial capacity parallels between songbirds and human infants. |

---

## Design Rationale

1. **Conservation Index (M0)**: Quantifies how "species-general" the current musical pattern is. Uses three features that are universal across vocal learning species: stumpf fusion (tonal coherence), harmonicity (harmonic-to-noise ratio = song purity), and tonalness (tonal vs noise). Patterns with high conservation index are the ones most likely to be shared across species — simple tonal patterns with clear harmonic structure.

2. **Template Fidelity (M1)**: Measures how closely the current music matches a stored song template. Familiarity is weighted highest (0.50) because template fidelity is fundamentally about recognition. Low entropy (0.30) indicates predictable patterns that match templates better. Stumpf fusion (0.20) provides tonal binding coherence. High fidelity means the current input is a close match to a learned template.

---

## Mathematical Formulation

```
Conservation Index:
  conservation_index = sigma(0.35 * stumpf[3] + 0.35 * harmonicity[5] + 0.30 * tonalness[14])
  |0.35| + |0.35| + |0.30| = 1.00

Template Fidelity:
  template_fidelity = sigma(0.50 * familiarity.mean + 0.30 * (1.0 - entropy[22]) + 0.20 * stumpf[3])
  |0.50| + |0.30| + |0.20| = 1.00
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 20, 1, 0) | stumpf_fusion mean H20 L0 | Binding stability over phrase window for conservation |
| (3, 24, 1, 0) | stumpf_fusion mean H24 L0 | Long-term binding context for template fidelity |
| (6, 20, 1, 0) | pitch_strength mean H20 L0 | Pitch stability over phrase for melody matching |
| (14, 20, 1, 0) | tonalness mean H20 L0 | Tonal stability over phrase for conservation |
| (22, 20, 1, 0) | entropy mean H20 L0 | Average complexity over 5s for fidelity |

---

## Scientific Foundation

- **Zhang et al. 2024**: Homologous auditory dorsal/ventral pathways across marmosets, macaques, and humans (dMRI, N=21, P<0.001)
- **Lipkind et al. 2013**: Stepwise vocal combinatorial capacity parallels between songbirds and human infants (cross-species behavioral)
- **Ravignani 2021**: Isochronous rhythms facilitate vocal learning by providing temporal scaffolding across species (theoretical)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/cssl/temporal_integration.py`
