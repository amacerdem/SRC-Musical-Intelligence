# Region-Atlas -- Brain Region Usage Across All Models

> **Scope**: 94 models across 9 units
> **Brain Regions**: 26 total (12 cortical, 9 subcortical, 5 brainstem)
> **Data Source**: Model `brain_regions` properties in `mi_beta/brain/units/*/models/*.py`, region definitions in `mi_beta/brain/regions/`
> **Last Updated**: 2026-02-13

---

## Region Inventory

### Cortical Regions (12)

| Abbr | Full Name | MNI (x, y, z) | BA | Primary Function |
|------|-----------|----------------|-----|-----------------|
| A1/HG | Primary Auditory Cortex (Heschl's Gyrus) | (48, -18, 8) | 41 | Tonotopic frequency analysis |
| STG | Superior Temporal Gyrus | (58, -22, 4) | 22 | Auditory association, melody, harmony, timbre |
| STS | Superior Temporal Sulcus | (54, -32, 4) | 21 | Multimodal integration, voice/music |
| IFG | Inferior Frontal Gyrus (Broca's Area) | (48, 18, 8) | 44 | Musical syntax, ERAN, sequence parsing |
| dlPFC | Dorsolateral Prefrontal Cortex | (42, 32, 30) | 46 | Working memory, executive control |
| vmPFC | Ventromedial Prefrontal Cortex | (2, 46, -10) | 10 | Subjective value, tonality tracking |
| OFC | Orbitofrontal Cortex | (28, 34, -16) | 11 | Reward valuation, hedonic judgement |
| ACC | Anterior Cingulate Cortex | (2, 30, 28) | 32 | Conflict monitoring, prediction error |
| SMA | Supplementary Motor Area | (2, -2, 56) | 6 | Internal timing, beat encoding |
| PMC | Premotor Cortex | (46, 0, 48) | 6 | Auditory-motor coupling, rhythm entrainment |
| AG | Angular Gyrus | (48, -60, 30) | 39 | Cross-modal integration |
| TP | Temporal Pole | (42, 12, -32) | 38 | Semantic memory, genre schemas |

### Subcortical Regions (9)

| Abbr | Full Name | MNI (x, y, z) | Primary Function |
|------|-----------|----------------|-----------------|
| VTA | Ventral Tegmental Area | (0, -16, -8) | Dopaminergic source, reward prediction error |
| NAcc | Nucleus Accumbens | (10, 12, -8) | Consummatory reward, DA/opioid integration |
| Caudate | Caudate Nucleus | (12, 10, 10) | Anticipatory reward, prediction-based wanting |
| Amygdala | Amygdala | (24, -4, -18) | Emotional valence tagging, affective salience |
| Hippocampus | Hippocampus | (28, -22, -12) | Musical memory, familiarity, statistical learning |
| Putamen | Putamen | (26, 4, 2) | Beat-based motor timing, basal ganglia loops |
| MGB | Medial Geniculate Body (Thalamus) | (14, -24, -2) | Primary auditory relay to cortex |
| Hypothalamus | Hypothalamus | (0, -4, -8) | Autonomic regulation (chills, HR, SCR) |
| Insula | Insula | (36, 16, 0) | Interoceptive awareness, bodily arousal |

### Brainstem Regions (5)

| Abbr | Full Name | MNI (x, y, z) | Primary Function |
|------|-----------|----------------|-----------------|
| IC | Inferior Colliculus | (0, -34, -8) | FFR generation, subcortical pitch encoding |
| AN | Auditory Nerve | (8, -26, -24) | Phase-locked spike trains from cochlea |
| CN | Cochlear Nucleus | (10, -38, -32) | First central auditory relay, feature extraction |
| SOC | Superior Olivary Complex | (6, -34, -24) | Binaural processing, spatial hearing |
| PAG | Periaqueductal Gray | (0, -30, -10) | Autonomic emotion, chills, piloerection |

---

## Unit-by-Region Usage Matrix

The matrix below shows which units use which brain regions. An "X" indicates that one or more models within the unit declare that region in their `brain_regions` property. Numbers in parentheses indicate how many models within the unit reference the region.

### Cortical Regions

| Region | SPU | STU | IMU | ASU | NDU | MPU | PCU | ARU | RPU | Total Models |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:-----------:|
| A1/HG | X(7) | X(8) | X(2) | . | . | . | X(3) | . | . | ~20 |
| STG | X(3) | X(9) | X(3) | X(5) | X(5) | . | X(4) | X(2) | . | ~31 |
| STS | . | X(2) | X(3) | X(2) | . | . | . | . | . | ~7 |
| IFG | . | . | X(3) | . | X(4) | . | . | . | . | ~7 |
| dlPFC | . | . | X(2) | . | . | . | X(2) | X(3) | X(2) | ~9 |
| vmPFC | . | . | X(4) | . | . | . | . | X(3) | X(3) | ~10 |
| OFC | . | . | . | . | . | . | . | X(3) | X(4) | ~7 |
| ACC | . | X(2) | . | X(5) | X(5) | . | X(3) | X(2) | . | ~17 |
| SMA | . | X(9) | . | . | . | X(8) | X(2) | . | . | ~19 |
| PMC | . | X(5) | . | . | . | X(7) | . | . | . | ~12 |
| AG | . | . | X(2) | . | . | . | X(1) | . | . | ~3 |
| TP | . | . | X(3) | . | . | . | . | . | . | ~3 |

### Subcortical Regions

| Region | SPU | STU | IMU | ASU | NDU | MPU | PCU | ARU | RPU | Total Models |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:-----------:|
| VTA | . | . | . | . | . | . | . | X(5) | X(4) | ~9 |
| NAcc | . | . | . | . | . | . | . | X(7) | X(5) | ~12 |
| Caudate | . | . | . | . | . | . | . | X(5) | X(5) | ~10 |
| Amygdala | . | . | X(5) | X(2) | . | . | X(1) | X(5) | . | ~13 |
| Hippocampus | . | . | X(12) | . | . | . | X(3) | X(2) | . | ~17 |
| Putamen | . | X(6) | . | . | . | X(7) | . | . | . | ~13 |
| MGB | X(2) | X(2) | . | . | . | . | . | . | . | ~4 |
| Hypothalamus | . | . | . | . | . | . | . | X(3) | X(2) | ~5 |
| Insula | . | . | . | X(6) | X(2) | . | . | X(3) | X(2) | ~13 |

### Brainstem Regions

| Region | SPU | STU | IMU | ASU | NDU | MPU | PCU | ARU | RPU | Total Models |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:-----------:|
| IC | X(4) | . | . | . | . | . | . | . | . | ~4 |
| AN | X(3) | . | . | . | . | . | . | . | . | ~3 |
| CN | X(3) | . | . | . | . | . | . | . | . | ~3 |
| SOC | X(1) | . | . | X(1) | . | . | . | . | . | ~2 |
| PAG | . | . | . | . | . | . | . | X(3) | X(2) | ~5 |

---

## Region Usage Heatmap

```
            SPU  STU  IMU  ASU  NDU  MPU  PCU  ARU  RPU
           +----+----+----+----+----+----+----+----+----+
  A1/HG    | XX | XX |  x |    |    |    |  X |    |    |  Cortical
  STG      |  X | XX |  X |  X |  X |    |  X |  x |    |
  STS      |    |  x |  X |  x |    |    |    |    |    |
  IFG      |    |    |  X |    |  X |    |    |    |    |
  dlPFC    |    |    |  x |    |    |    |  x |  X |  x |
  vmPFC    |    |    |  X |    |    |    |    |  X |  X |
  OFC      |    |    |    |    |    |    |    |  X |  X |
  ACC      |    |  x |    |  X |  X |    |  X |  x |    |
  SMA      |    | XX |    |    |    | XX |  x |    |    |
  PMC      |    |  X |    |    |    | XX |    |    |    |
  AG       |    |    |  x |    |    |    |  x |    |    |
  TP       |    |    |  X |    |    |    |    |    |    |
           +----+----+----+----+----+----+----+----+----+
  VTA      |    |    |    |    |    |    |    |  X |  X |  Subcortical
  NAcc     |    |    |    |    |    |    |    | XX |  X |
  Caudate  |    |    |    |    |    |    |    |  X |  X |
  Amygdala |    |    |  X |  x |    |    |  x |  X |    |
  Hippoc.  |    |    | XX |    |    |    |  X |  x |    |
  Putamen  |    |  X |    |    |    | XX |    |    |    |
  MGB      |  x |  x |    |    |    |    |    |    |    |
  Hypothal.|    |    |    |    |    |    |    |  X |  x |
  Insula   |    |    |    |  X |  x |    |    |  X |  x |
           +----+----+----+----+----+----+----+----+----+
  IC       |  X |    |    |    |    |    |    |    |    |  Brainstem
  AN       |  X |    |    |    |    |    |    |    |    |
  CN       |  X |    |    |    |    |    |    |    |    |
  SOC      |  x |    |    |  x |    |    |    |    |    |
  PAG      |    |    |    |    |    |    |    |  X |  x |
           +----+----+----+----+----+----+----+----+----+

Legend:  XX = dominant (>60% of models)  X = substantial (30-60%)
        x = minor (<30%)               (blank) = not used
```

---

## Top 10 Most-Referenced Regions

| Rank | Region | Abbr | Type | Models | Units | Evidence Citations |
|------|--------|------|------|--------|-------|--------------------|
| 1 | Superior Temporal Gyrus | STG | Cortical | ~31 | 7 units | 38 |
| 2 | Primary Auditory Cortex | A1/HG | Cortical | ~20 | 4 units | 42 |
| 3 | Supplementary Motor Area | SMA | Cortical | ~19 | 3 units | 21 |
| 4 | Anterior Cingulate Cortex | ACC | Cortical | ~17 | 5 units | 12 |
| 5 | Hippocampus | Hippocampus | Subcortical | ~17 | 3 units | 22 |
| 6 | Amygdala | Amygdala | Subcortical | ~13 | 4 units | 31 |
| 7 | Putamen | Putamen | Subcortical | ~13 | 2 units | 16 |
| 8 | Insula | Insula | Subcortical | ~13 | 4 units | 14 |
| 9 | Nucleus Accumbens | NAcc | Subcortical | ~12 | 2 units | 24 |
| 10 | Premotor Cortex | PMC | Cortical | ~12 | 2 units | 14 |

**STG is the most-referenced region** -- used by 7 of 9 units. This reflects its role as the primary auditory association cortex, processing melody, harmony, and timbre.

---

## Region Dominance by Unit

Each unit has a characteristic "neural signature" -- a set of regions that define its anatomical substrate:

| Unit | Dominant Regions | Circuit | Anatomical Profile |
|------|-----------------|---------|-------------------|
| **SPU** | A1/HG, IC, AN, CN | Perceptual | Ascending auditory pathway: brainstem -> primary cortex |
| **STU** | A1/HG, STG, SMA, Putamen | Sensorimotor | Auditory-motor loop: temporal cortex <-> basal ganglia <-> motor cortex |
| **IMU** | Hippocampus, vmPFC, STG, IFG, TP | Mnemonic | Memory circuit: hippocampus -> prefrontal -> temporal association |
| **ASU** | ACC, Insula, STG | Salience | Salience network: anterior insula <-> ACC <-> temporal cortex |
| **NDU** | STG, ACC, IFG | Salience | Deviance detection: temporal cortex -> frontal monitoring |
| **MPU** | SMA, PMC, Putamen | Sensorimotor | Motor circuit: premotor -> SMA -> basal ganglia |
| **PCU** | A1/HG, STG, ACC, Hippocampus | Mnemonic | Prediction hierarchy: sensory -> memory -> monitoring |
| **ARU** | NAcc, VTA, Amygdala, vmPFC, OFC | Mesolimbic | Reward circuit: VTA -> striatum -> prefrontal |
| **RPU** | NAcc, Caudate, VTA, OFC, vmPFC | Mesolimbic | Reward computation: striatum -> prefrontal valuation |

---

## Functional Pathways Through Regions

The declared cross-unit pathways (P1--P5) can be traced through their anatomical substrates:

| Pathway | Route | Source Regions | Target Regions | Neural Pathway |
|---------|-------|---------------|---------------|----------------|
| P1 | SPU -> ARU | A1/HG, IC | NAcc, VTA | Ascending auditory -> mesolimbic reward |
| P2 | STU -> STU | SMA, STG | SMA, Putamen | Auditory-motor loop (internal) |
| P3 | IMU -> ARU | Hippocampus, vmPFC | Amygdala, NAcc | Memory -> affect (Papez circuit analog) |
| P4 | STU -> STU | STG, A1/HG | STG, A1/HG | Context -> prediction (internal) |
| P5 | STU -> ARU | SMA, Putamen | VTA, NAcc | Motor/tempo -> emotion (groove -> reward) |

---

## Region Type Distribution

| Region Type | Count | Total Evidence | Avg Evidence/Region | Units Using |
|-------------|-------|----------------|---------------------|-------------|
| Cortical | 12 | 198 | 16.5 | All 9 |
| Subcortical | 9 | 163 | 18.1 | 7 of 9 (not SPU, not NDU exclusively) |
| Brainstem | 5 | 35 | 7.0 | 2 (SPU primarily, ASU marginally) |

### By Circuit

| Circuit | Primary Regions | Secondary Regions |
|---------|----------------|-------------------|
| Perceptual | A1/HG, STG, IC, AN, CN, SOC | MGB |
| Sensorimotor | SMA, PMC, Putamen | STG, A1/HG, Cerebellum (implied) |
| Mnemonic | Hippocampus, vmPFC, dlPFC | IFG, TP, AG |
| Mesolimbic | NAcc, VTA, Caudate, OFC | vmPFC, Amygdala, Hypothalamus |
| Salience | ACC, Insula, STG | IFG, Amygdala |

---

## Lateralization Notes

Most regions are specified as bilateral in the model declarations, with notable exceptions:

- **IFG**: Right-lateralized for musical syntax (left for language)
- **A1/HG**: Right hemisphere preference for pitch; left for temporal resolution
- **dlPFC**: Right for tonal working memory; left for verbal
- **Hippocampus**: Bilateral but left-dominant for sequential/temporal memory
- **Amygdala**: Bilateral but right-dominant for negative valence

---

## MNI Coordinate Summary for Top Regions

| Region | MNI (x, y, z) | Spatial Uncertainty | Source Atlas |
|--------|----------------|--------------------|--------------|
| STG | (58, -22, 4) | +/- 5mm | Griffiths & Warren 2002 |
| A1/HG | (48, -18, 8) | +/- 3mm | Patterson 2002 |
| SMA | (2, -2, 56) | +/- 4mm | Grahn & Rowe 2009 |
| ACC | (2, 30, 28) | +/- 4mm | Koelsch 2014 |
| Hippocampus | (28, -22, -12) | +/- 3mm | Harvard-Oxford Atlas |
| NAcc | (10, 12, -8) | +/- 2mm | Salimpoor 2011 |
| VTA | (0, -16, -8) | +/- 3mm | Harvard AAR Atlas |
| Amygdala | (24, -4, -18) | +/- 3mm | Trost 2012 |
| Putamen | (26, 4, 2) | +/- 3mm | Grahn & Rowe 2009 |
| IC | (0, -34, -8) | +/- 2mm | Coffey 2016 |

---

## Cross-References

- **Region Definitions**: [Regions/Cortical.md](../Regions/Cortical.md), [Subcortical.md](../Regions/Subcortical.md), [Brainstem.md](../Regions/Brainstem.md)
- **Unit Docs**: [Units/](../Units/) -- model rosters and pathway declarations
- **Mechanism Map**: [Mechanism-Map.md](Mechanism-Map.md) -- mechanisms group models that share regional substrates
- **Code**: `mi_beta/brain/regions/cortical.py`, `subcortical.py`, `brainstem.py`
