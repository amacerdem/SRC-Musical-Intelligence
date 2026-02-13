# C³ Brain Regions -- Brainstem

> **Code**: `mi_beta/brain/regions/brainstem.py`
> **Count**: 5 regions
> **Total Evidence**: 35 citations
> **Brodmann Areas**: None (brainstem structures lack BA designations)
> **Spatial Note**: Brainstem structures are small and deep; MNI coordinates carry higher spatial uncertainty (+/- 2-3 mm) than cortical regions.

## MNI Coordinate Sources

Coordinates are derived from:
- Harvard Ascending Arousal Network Atlas (Edlow 2012)
- Coffey et al. 2016 (frequency-following response in IC)
- Chandrasekaran & Kraus 2010 (auditory brainstem encoding)
- Thompson & Bhatt 2017 (brainstem auditory pathway atlas)
- Blood & Zatorre 2001 (PAG activation during chills)

---

## Region Table

| Name | Abbreviation | Hemisphere | MNI (x, y, z) | Brodmann Area | Function | Evidence Count |
|------|-------------|------------|----------------|---------------|----------|----------------|
| Inferior Colliculus | IC | bilateral | (0, -34, -8) | -- | Midbrain auditory relay; generates frequency-following response (FFR) for subcortical pitch encoding of musical sounds (Coffey 2016, Chandrasekaran & Kraus 2010) | 12 |
| Auditory Nerve | AN | bilateral | (8, -26, -24) | -- | Peripheral auditory encoding; phase-locked spike trains carry spectrotemporal information from cochlea to brainstem (Heil & Peterson 2015) | 6 |
| Cochlear Nucleus | CN | bilateral | (10, -38, -32) | -- | First central auditory processing station; parallel spectral and temporal feature extraction via specialised cell types (Young & Oertel 2004) | 5 |
| Superior Olivary Complex | SOC | bilateral | (6, -34, -24) | -- | First binaural processing stage; computes interaural time and level differences for spatial hearing and auditory scene analysis (Grothe 2010) | 4 |
| Periaqueductal Gray | PAG | bilateral | (0, -30, -10) | -- | Autonomic and emotional regulation; mediates chills, piloerection, and respiratory changes during peak musical moments (Blood & Zatorre 2001, Goldstein 1983) | 8 |

---

## Ascending Auditory Pathway

The brainstem regions form the ascending auditory pathway, processing sound from cochlea to cortex:

```
Cochlea
  |
  v
AN (Auditory Nerve) -- phase-locked spike trains, spectrotemporal encoding
  |
  v
CN (Cochlear Nucleus) -- first central relay, parallel spectral/temporal extraction
  |                       (AVCN: onset detection, PVCN/DCN: spectral shaping)
  v
SOC (Superior Olivary Complex) -- first binaural convergence
  |                               (MSO: interaural time, LSO: interaural level)
  v
IC (Inferior Colliculus) -- obligatory midbrain relay, FFR generation
  |                          (subcortical pitch encoding)
  v
MGB (Thalamus) -> Cortex
```

### PAG: Parallel Emotional Pathway

The Periaqueductal Gray is not part of the ascending auditory pathway but plays a critical role in musical experience:
- Surrounds the cerebral aqueduct in the midbrain
- Mediates autonomic emotional responses: chills, piloerection, respiratory changes
- Activated during peak musical moments (Blood & Zatorre 2001)
- Also involved in emotional vocalisation and pain modulation

---

## Cochlear Nucleus Subdivisions

The CN contains three functionally distinct subdivisions:
- **AVCN** (Anteroventral): Onset cells for transient detection, bushy cells for temporal preservation
- **PVCN** (Posteroventral): Choppers for periodicity, octopus cells for broadband onset
- **DCN** (Dorsal): Spectral notch detection, adaptive filtering

---

## Code Export

```python
from mi_beta.brain.regions import IC, AN, CN, SOC, PAG
from mi_beta.brain.regions.brainstem import ALL_BRAINSTEM  # Tuple of all 5
```
