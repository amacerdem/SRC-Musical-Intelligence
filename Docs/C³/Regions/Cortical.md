# C³ Brain Regions -- Cortical

> **Code**: `mi_beta/brain/regions/cortical.py`
> **Count**: 12 regions
> **Total Evidence**: 198 citations
> **Brodmann Areas**: All cortical regions have BA designations

## MNI Coordinate Sources

Coordinates are derived from published meta-analyses and atlases:
- Zatorre et al. 2002 (auditory cortex specialization)
- Koelsch 2011, 2014 (music syntax and emotion)
- Grahn & Rowe 2009, 2013 (motor timing)
- Janata 2009 (tonality-tracking in mPFC)
- Levitin & Menon 2003 (musical structure)
- Alluri et al. 2012 (timbral feature mapping)
- Patterson et al. 2002 (pitch centre in HG)
- Sammler et al. 2013 (music syntax in IFG)

---

## Region Table

| Name | Abbreviation | Hemisphere | MNI (x, y, z) | Brodmann Area | Function | Evidence Count |
|------|-------------|------------|----------------|---------------|----------|----------------|
| Primary Auditory Cortex (Heschl's Gyrus) | A1/HG | bilateral | (48, -18, 8) | BA 41 | Tonotopic frequency analysis; first cortical stage of spectral decomposition with rightward lateralisation for pitch, leftward for temporal fine structure (Zatorre 2002, Patterson 2002) | 42 |
| Superior Temporal Gyrus | STG | bilateral | (58, -22, 4) | BA 22 | Auditory association cortex; processes melody, harmony, and timbre through spectrotemporal pattern recognition (Griffiths & Warren 2002, Alluri 2012) | 38 |
| Superior Temporal Sulcus | STS | bilateral | (54, -32, 4) | BA 21 | Multimodal stream integration; voice/music discrimination, audiovisual binding, and communicative intent processing (Belin 2000, Peretz & Coltheart 2003) | 15 |
| Inferior Frontal Gyrus (Broca's Area) | IFG | R | (48, 18, 8) | BA 44 | Musical syntax processing; generates ERAN for unexpected harmonic events, hierarchical sequence parsing (Koelsch 2011, Sammler 2013) | 27 |
| Dorsolateral Prefrontal Cortex | dlPFC | bilateral | (42, 32, 30) | BA 46 | Working memory and executive control; maintains tonal context for expectation comparison and planning (Zatorre 1994, Owen 2005) | 13 |
| Ventromedial Prefrontal Cortex | vmPFC | bilateral | (2, 46, -10) | BA 10 | Subjective value computation; integrates reward with contextual evaluation, tracks tonality and musical autobiography (Janata 2009, Blood & Zatorre 2001) | 17 |
| Orbitofrontal Cortex | OFC | bilateral | (28, 34, -16) | BA 11 | Reward valuation and hedonic judgement; computes the conscious aesthetic value of musical stimuli (Blood & Zatorre 2001, Salimpoor 2013) | 15 |
| Anterior Cingulate Cortex | ACC | bilateral | (2, 30, 28) | BA 32 | Conflict monitoring and prediction error signalling; detects harmonic violations and unexpected musical events (Koelsch 2014, Menon 2015) | 12 |
| Supplementary Motor Area | SMA | bilateral | (2, -2, 56) | BA 6 | Internal timing and motor planning; encodes beat-level metric structure even during passive listening (Grahn & Rowe 2009, 2013, d=0.67) | 21 |
| Premotor Cortex | PMC | bilateral | (46, 0, 48) | BA 6 | Auditory-motor coupling and motor planning; mediates rhythm entrainment and sensorimotor synchronisation (Chen 2008, Zatorre 2007) | 14 |
| Angular Gyrus | AG | bilateral | (48, -60, 30) | BA 39 | Cross-modal integration; binds auditory, visual, and somatosensory streams for holistic musical experience (Seghier 2013, Koelsch 2014) | 8 |
| Temporal Pole | TP | bilateral | (42, 12, -32) | BA 38 | Semantic memory hub; stores abstract musical knowledge, genre schemas, and conceptual associations (Patterson 2007, Peretz & Coltheart 2003) | 7 |

---

## Functional Groupings

### Auditory Processing Chain
- **A1/HG** (BA 41) -> **STG** (BA 22) -> **STS** (BA 21)
- Ascending complexity: tonotopic -> spectrotemporal patterns -> multimodal integration

### Frontal Executive / Syntax
- **IFG** (BA 44) -- musical syntax and sequence parsing
- **dlPFC** (BA 46) -- tonal working memory

### Reward / Valuation
- **vmPFC** (BA 10) -- subjective value, tonality tracking
- **OFC** (BA 11) -- hedonic judgement, aesthetic value

### Motor / Timing
- **SMA** (BA 6) -- internal metric structure, beat encoding
- **PMC** (BA 6) -- auditory-motor coupling, rhythm entrainment

### Monitoring / Integration
- **ACC** (BA 32) -- conflict monitoring, prediction error
- **AG** (BA 39) -- cross-modal binding
- **TP** (BA 38) -- semantic memory, musical knowledge

---

## Lateralisation Notes

Most cortical regions are listed as bilateral, with notable exceptions:
- **IFG** is specified as **right-lateralised** for musical syntax processing (left IFG handles linguistic syntax)
- **A1/HG** shows rightward lateralisation for spectral/pitch processing and leftward for temporal resolution
- **dlPFC** shows left lateralisation for verbal working memory, right for tonal/spatial

---

## Code Export

```python
from mi_beta.brain.regions import A1_HG, STG, STS, IFG, DLPFC, VMPFC, OFC, ACC, SMA, PMC, ANGULAR_GYRUS, TEMPORAL_POLE
from mi_beta.brain.regions.cortical import ALL_CORTICAL  # Tuple of all 12
```
