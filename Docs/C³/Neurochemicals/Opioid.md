# Endogenous Opioids (mu-opioid) -- Hedonic "Liking" and Consummatory Pleasure

> **Code**: `mi_beta/brain/neurochemicals/opioid.py`
> **NeurochemicalType**: `OPIOID`
> **Manager methods**: `write_opioid()`, `read_opioid()`, `opioid_keys`

## Overview

The mu-opioid system mediates the hedonic "liking" response -- the raw pleasurable sensation at the moment of musical consummation. This is dissociable from dopaminergic "wanting" (Berridge 2003):

| System | Function | Timing | Subjective |
|--------|----------|--------|------------|
| DA "wanting" | Motivational drive, anticipation, prediction error | Before pleasure peak | Desire, craving, approach |
| Opioid "liking" | Hedonic impact, conscious pleasure, "felt goodness" | At pleasure peak | Raw pleasure, satisfaction |

---

## Region Specifications (`OPIOID_REGIONS`)

| Region Key | Full Name | Is Hotspot | Hotspot Volume | Role | Citation |
|------------|-----------|-----------|----------------|------|----------|
| `nacc_shell` | Nucleus Accumbens Shell | Yes | 8.0 mm³ | Primary hedonic hotspot; mu-opioid stimulation amplifies consummatory pleasure reactions. Rostrodorsal medial shell is the most reliable site for hedonic enhancement | Pecina & Berridge 2005; Nummenmaa 2025 |
| `vp` | Ventral Pallidum | Yes | 6.0 mm³ | Second hedonic hotspot; VP posterior region amplifies hedonic 'liking' reactions, functionally linked to NAcc shell opioid output | Smith & Berridge 2007 |
| `parabrachial` | Parabrachial Nucleus | Yes | 3.0 mm³ | Brainstem hedonic hotspot; modulates basic sensory pleasure. Projects to NAcc shell and VP to coordinate hedonic evaluation | Berridge & Kringelbach 2015 |

---

## Hedonic Hotspots (`HEDONIC_HOTSPOTS`)

Hedonic hotspots are remarkably small circumscribed brain regions (typically < 10 mm³ in rodents, scaled to ~25 mm³ in humans) where mu-opioid receptor stimulation amplifies hedonic "liking" reactions. They form a distributed network where each hotspot can amplify liking independently, but their interaction produces maximal hedonic impact.

| Hotspot Name | Region Key | MNI Centroid (x, y, z) | Receptor | Effect | Mechanism | Citation |
|-------------|-----------|------------------------|----------|--------|-----------|----------|
| NAcc medial shell hotspot | `nacc_shell` | (8, 14, -6) | mu | Amplifies hedonic liking | mu-opioid agonist (DAMGO) in rostrodorsal medial shell doubles hedonic 'liking' reactions without changing 'wanting'; blocked by naloxone | Pecina & Berridge 2005 |
| Ventral pallidum posterior hotspot | `vp` | (-2, 0, -6) | mu | Amplifies hedonic liking | mu-opioid stimulation in posterior VP enhances hedonic reactions; lesions here produce anhedonia -- the only brain site where lesion abolishes both liking and wanting | Smith & Berridge 2007 |
| Parabrachial nucleus hotspot | `parabrachial` | (4, -32, -28) | mu | Modulates sensory hedonic tone | Opioid signalling in parabrachial nucleus modulates basic sensory pleasure; projects to NAcc shell to coordinate evaluation across modalities | Berridge & Kringelbach 2015 |

---

## Hotspot Network

```
Parabrachial (brainstem)
  |
  v  (ascending hedonic signal)
NAcc Shell (ventral striatum)
  |
  v  (opioid output)
Ventral Pallidum (basal forebrain)
  |
  v  (hedonic evaluation -> conscious pleasure)
Cortex (OFC, vmPFC)
```

Each hotspot amplifies "liking" independently, but the circuit produces maximal hedonic impact when all three are active. The VP posterior hotspot is unique: lesions there abolish BOTH liking and wanting -- the only brain site with this property.

---

## Interaction with Other Systems

- **Dopamine**: DA encodes "wanting" (anticipation, motivation); opioids encode "liking" (hedonic impact). Both converge in NAcc but operate via distinct receptor systems. DA can drive approach behavior without pleasure; opioids generate pleasure without necessarily driving approach.
- **Serotonin**: 5-HT modulates the background mood state that colours hedonic evaluation. Low 5-HT may reduce the capacity for opioid-mediated pleasure.
- **Norepinephrine**: NE-driven arousal amplifies the salience of hedonic moments, potentially enhancing opioid release at peak pleasure.

---

## Models That Write/Read Opioids

**Writers** (models that produce opioid signals):
- ARU models (SRP) -- write `opioid_proxy` for hedonic evaluation

**Readers** (models that consume opioid signals):
- ARU models (AAC, VMM) -- read opioid for affect and valence computation
- PCU models -- read opioid for imagery/emotion processing

---

## Key Papers

| Paper | Finding |
|-------|---------|
| Berridge 2003 | Wanting vs liking dissociation: DA for wanting, opioids for liking |
| Berridge & Kringelbach 2015 | Hedonic hotspot circuitry: NAcc shell, VP, parabrachial |
| Nummenmaa et al. 2025 | Music-evoked opioid release demonstrated via PET |
| Pecina & Berridge 2005 | NAcc shell hotspot mapping: DAMGO doubles liking reactions |
| Smith & Berridge 2007 | VP posterior hotspot: only site where lesion abolishes both liking and wanting |
