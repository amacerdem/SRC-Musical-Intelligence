# C³ Brain Regions -- Subcortical

> **Code**: `mi_beta/brain/regions/subcortical.py`
> **Count**: 9 regions
> **Total Evidence**: 163 citations
> **Brodmann Areas**: None (subcortical structures lack BA designations)

## MNI Coordinate Sources

Coordinates are derived from published atlases and studies:
- Harvard-Oxford Subcortical Structural Atlas (Desikan 2006)
- Neurosynth meta-analytic peaks (Yarkoni 2011)
- Salimpoor et al. 2011, 2013 (reward circuitry)
- Koelsch 2014 (music-evoked emotion model)
- Blood & Zatorre 2001 (chills and autonomic)
- Grahn & Rowe 2009 (putamen and timing)
- Trost et al. 2012 (amygdala and emotion)

---

## Region Table

| Name | Abbreviation | Hemisphere | MNI (x, y, z) | Brodmann Area | Function | Evidence Count |
|------|-------------|------------|----------------|---------------|----------|----------------|
| Ventral Tegmental Area | VTA | bilateral | (0, -16, -8) | -- | Dopaminergic source nucleus; generates reward prediction error signals during unexpected harmonic progressions and timbral changes | 18 |
| Nucleus Accumbens | NAcc | bilateral | (10, 12, -8) | -- | Consummatory reward hub; integrates dopaminergic and opioidergic signals for peak musical pleasure (Salimpoor 2011, r=0.84) | 24 |
| Caudate Nucleus | caudate | bilateral | (12, 10, 10) | -- | Anticipatory reward; dopamine release peaks 10-15s before consummatory pleasure reflecting prediction-based 'wanting' (Salimpoor 2011, r=0.71) | 19 |
| Amygdala | amygdala | bilateral | (24, -4, -18) | -- | Emotional valence tagging; responds to dissonance, tension, and affective salience in musical stimuli (Koelsch 2014) | 31 |
| Hippocampus | hippocampus | bilateral | (28, -22, -12) | -- | Musical memory encoding and retrieval; familiarity detection, episodic associations, and statistical learning of musical structure (Janata 2009, Watanabe 2008) | 22 |
| Putamen | putamen | bilateral | (26, 4, 2) | -- | Beat-based motor timing; entrainment to regular rhythmic structures via basal ganglia-cortical loops (Grahn & Rowe 2009, d=0.67) | 16 |
| Thalamus (Medial Geniculate Body) | MGB | bilateral | (14, -24, -2) | -- | Primary auditory relay; gates ascending spectrotemporal information to cortex with attentional modulation (Suga 2008, Winer 2005) | 11 |
| Hypothalamus | hypothalamus | bilateral | (0, -4, -8) | -- | Autonomic regulation; mediates physiological responses (heart rate, chills, skin conductance) to emotionally powerful music (Blood & Zatorre 2001) | 9 |
| Insula | insula | bilateral | (36, 16, 0) | -- | Interoceptive awareness; integrates bodily arousal signals with emotional context for conscious musical feeling states (Craig 2009, Koelsch 2014) | 14 |

---

## Functional Groupings

### Mesolimbic Reward Circuit
- **VTA** -- dopaminergic cell bodies, reward prediction error source
- **NAcc** -- consummatory pleasure, DA/opioid integration
- **caudate** -- anticipatory reward, prediction-based wanting

### Emotional Processing
- **amygdala** -- valence tagging, affective salience (highest evidence count: 31)
- **insula** -- interoceptive awareness, conscious feeling states
- **hypothalamus** -- autonomic regulation (chills, heart rate, SCR)

### Memory
- **hippocampus** -- familiarity detection, episodic musical memory

### Sensory Relay / Timing
- **MGB** (thalamus) -- auditory gateway to cortex
- **putamen** -- beat-based timing via basal ganglia loops

---

## Temporal Dissociation: Caudate vs NAcc

A critical finding from Salimpoor et al. 2011:
- **Caudate** DA peaks **10-15 seconds BEFORE** the pleasure moment (anticipatory)
- **NAcc** DA peaks **AT** the pleasure moment (consummatory)
- This temporal dissociation maps directly onto Berridge's wanting/liking framework

---

## Code Export

```python
from mi_beta.brain.regions import VTA, NACC, CAUDATE, AMYGDALA, HIPPOCAMPUS, PUTAMEN, THALAMUS_MGB, HYPOTHALAMUS, INSULA
from mi_beta.brain.regions.subcortical import ALL_SUBCORTICAL  # Tuple of all 9
```
