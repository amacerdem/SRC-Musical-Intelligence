# L³ Groups — Beta (Neuroscience Semantics)

**Version**: 2.1.0
**Symbol**: β
**Level**: 2
**Dimensions**: Variable (N_unique_regions)
**Phase**: 1 (Independent, Stateless)
**Output Range**: [0, 1]
**Code**: `mi_beta/language/groups/beta.py` (123 lines)
**Updated**: 2026-02-13

---

## Overview

Beta answers the question: **WHERE in the brain?**

Beta maps Brain model outputs to brain region activations using the `BrainRegion` declarations from each active model in the ModelRegistry. It produces one activation dimension per unique brain region, plus derived neurotransmitter and circuit state dimensions.

**Audience**: Neuroscientists, fMRI/EEG researchers, computational neuroscience.

---

## Dimensionality

Beta has **variable dimensionality** that depends on the number of unique brain regions declared across all active models:

- **mi_beta (current)**: N_unique_regions (auto-discovered from ModelRegistry)
- **mi v2 design spec (14D)**: 8D Brain Regions + 3D Neurotransmitter Dynamics + 3D Circuit States

### 3 Subcategories (v2 design spec)

| Subcategory | Dim | Dimensions |
|-------------|:---:|------------|
| Brain Regions | 8 | NAcc, Caudate, VTA, SN, STG, IFG, Amygdala, Hippocampus |
| Neurotransmitter Dynamics | 3 | DA proxy, Opioid proxy, DA x Opioid interaction |
| Circuit States | 3 | Anticipation, Consummation, Learning |

---

## Dimension Table (v2 Design Spec)

### Brain Regions (8D)

| Local Index | Name | Range | Formula | Citation |
|:-----------:|------|:-----:|---------|----------|
| 0 | `region_nacc` | [0,1] | Mean activation of NAcc-declaring models | Salimpoor et al. 2011 |
| 1 | `region_caudate` | [0,1] | Mean activation of Caudate-declaring models | Salimpoor et al. 2011 |
| 2 | `region_vta` | [0,1] | Mean activation of VTA-declaring models | Howe et al. 2013 |
| 3 | `region_sn` | [0,1] | Mean activation of SN-declaring models | Howe et al. 2013 |
| 4 | `region_stg` | [0,1] | Mean activation of STG-declaring models | Kim et al. 2021 |
| 5 | `region_ifg` | [0,1] | Mean activation of IFG-declaring models | Fong et al. 2020 |
| 6 | `region_amygdala` | [0,1] | Mean activation of Amygdala-declaring models | Koelsch et al. 2006 |
| 7 | `region_hippocampus` | [0,1] | Mean activation of Hippocampus-declaring models | Sachs et al. 2025 |

### Neurotransmitter Dynamics (3D)

| Local Index | Name | Range | Formula | Citation |
|:-----------:|------|:-----:|---------|----------|
| 8 | `da_proxy` | [0,1] | `(NAcc + Caudate) / 2` | Salimpoor et al. 2011 |
| 9 | `opioid_proxy` | [0,1] | Opioid-system activation proxy | Blood & Zatorre 2001 |
| 10 | `da_opioid_interaction` | [0,1] | `DA_proxy * Opioid_proxy` | Berridge & Kringelbach 2015 |

### Circuit States (3D)

| Local Index | Name | Range | Formula | Citation |
|:-----------:|------|:-----:|---------|----------|
| 11 | `anticipation` | [0,1] | Caudate DA ramp (wanting phase) | Salimpoor et al. 2011 |
| 12 | `consummation` | [0,1] | NAcc DA burst (liking phase) | Salimpoor et al. 2011 |
| 13 | `learning` | [0,1] | VTA RPE signal | Schultz 1997 |

---

## Formulas

### Per-Region Activation (mi_beta implementation)

```python
# For each unique brain region:
for unit_name, model_name in model_refs:
    model_tensor = brain_output.get_model(unit_name, model_name)
    activations.append(model_tensor.mean(dim=-1, keepdim=True))

# Average across all models declaring this region:
region_act = torch.stack(activations, dim=-1).mean(dim=-1)  # (B, T, 1)
```

Each region's activation is the mean of the mean activations of all models that declare that region in their `brain_regions` attribute. If no models declare a region, it defaults to 0.5.

### Neurotransmitter Dynamics (v2 design)

```python
DA_proxy = (NAcc + Caudate) / 2
Opioid_proxy = f(opioid_region_activations)  # from opioid-associated models
DA_Opioid_interaction = DA_proxy * Opioid_proxy
```

### Circuit States (v2 design)

```python
anticipation = caudate_DA_ramp      # Caudate → wanting/anticipation phase
consummation = nacc_DA_burst        # NAcc → liking/consummation phase
learning = vta_RPE                  # VTA → reward prediction error / learning
```

---

## Code Mapping

| Doc Concept | Code Variable | Location |
|-------------|---------------|----------|
| Region discovery | `_configure(registry)` scans `registry.active_models()` | beta.py:45-60 |
| Region map | `self._region_model_map: Dict[str, List[Tuple[str, str]]]` | beta.py:40 |
| Region names | `self._region_names = sorted(region_set.keys())` | beta.py:58 |
| Per-region activation | `model_tensor.mean(dim=-1, keepdim=True)` averaged across models | beta.py:104-110 |
| Fallback | `torch.full((B, T, 1), 0.5, ...)` when no models declare a region | beta.py:98 |
| Placeholder | `"no_region_placeholder"` when no regions found at all | beta.py:69 |
| Dimension names | `[f"region_{name.lower()}" for name in self._region_names]` | beta.py:70 |

---

## Auto-Configuration Protocol

Like Alpha, Beta has variable dimensionality:

1. `__init__(registry=None)` accepts an optional ModelRegistry
2. `_configure(registry)` iterates all active models, reads `brain_regions` attribute
3. Collects `region.abbreviation` for each BrainRegion, builds `_region_model_map`
4. Sorts region names alphabetically for deterministic ordering
5. `_output_dim = max(len(region_names), 1)` — minimum 1D placeholder

Each model can declare multiple brain regions, and each region can be declared by multiple models. Beta averages across all contributing models for each region.

---

## Brain Region Evidence

Each BrainRegion declaration in C³ carries:
- **MNI152 coordinates**: Standard neuroimaging space localization
- **evidence_count**: Number of supporting studies from the C³ meta-analysis database

This allows Beta activations to be directly compared against fMRI BOLD signals at known coordinates.

---

## Design Notes

- **Variable dimensionality**: Adapts to whatever models are registered and active
- **No learned parameters**: Pure averaging from model declarations
- **Graceful fallback**: Returns 0.5 placeholder when no models declare any region
- **Alphabetical ordering**: Region dimension names are sorted for deterministic output
- **All outputs clamped**: Final tensor passes through `.clamp(0, 1)`

---

## Parent / See Also

- **Parent**: [Independent/00-INDEX.md](00-INDEX.md)
- **Epistemology**: [Epistemology/Neuroscience.md](../../Epistemology/Neuroscience.md) — Level 2 theory
- **Registry**: [Registry/DimensionCatalog.md](../../Registry/DimensionCatalog.md) — global indices
- **C³ Brain Regions**: [C³/Matrices/Output-Space.md](../../../C³/Matrices/Output-Space.md) — source region declarations
- **Code**: `mi_beta/language/groups/beta.py`
