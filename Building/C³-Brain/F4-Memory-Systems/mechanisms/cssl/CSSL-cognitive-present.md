# CSSL P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [5:7]
**Scope**: internal
**Activation**: clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:entrainment_state | [0, 1] | Current motor-auditory entrainment level. Aggregation of encoding state for rhythm. Reflects how tightly the motor-auditory loop is currently coupled. Barchet et al. 2024: music-specific ~2 Hz beat entrainment timescale; finger-tapping optimal at 2 Hz for music. |
| 6 | P1:template_match | [0, 1] | Current song template match quality. familiarity_proxy * x_l5l7.mean. High when current music closely matches a stored song template. Eliades et al. 2024: dual vocal suppression timescales in marmoset auditory cortex (r=0.46, N=3285 units). |

---

## Design Rationale

1. **Entrainment State (P0)**: The present-moment motor-auditory coupling signal. This aggregates the encoding state to reflect real-time rhythmic entrainment. When this signal is high, the listener's motor system is tightly locked to the musical beat — the same mechanism that songbirds use for vocal practice (matching output to auditory template through basal ganglia gating).

2. **Template Match (P1)**: The present-moment template recognition signal. This is the product of familiarity and the consonance-timbre interaction (x_l5l7). High template match means the current spectrotemporal pattern is being successfully compared against stored song templates in the auditory cortex, analogous to the HVC template matching in songbirds.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (11, 20, 17, 0) | onset_strength periodicity H20 L0 | Beat regularity over 5s for entrainment |
| (12, 16, 0, 2) | warmth value H16 L2 | Current voice quality for template matching |
| (7, 20, 3, 0) | amplitude std H20 L0 | Energy variability = dynamic range for entrainment |

P-layer primarily aggregates E+M outputs rather than introducing many new H3 tuples.

---

## Brain Regions

| Region | MNI Coordinates | P-Layer Role |
|--------|-----------------|-------------|
| Basal ganglia (putamen/caudate) | +/-24, 2, 4 | P0: real-time motor-auditory loop gating |
| Auditory cortex (STG/A1) | +/-60, -32, 8 | P1: online template comparison |
| Premotor cortex / SMA | +/-44, 0, 48 | P0: motor output for vocal production, beat timing |

---

## Scientific Foundation

- **Barchet et al. 2024**: Speech and music recruit partially distinct rhythmic timing mechanisms; ~2 Hz music beat entrainment (behavioral)
- **Eliades et al. 2024**: Dual vocal suppression timescales (phasic + tonic) in marmoset auditory cortex (single-neuron, N=3285 units, r=0.46)
- **Loui et al. 2017**: Auditory-reward white matter connectivity predicts musical reward (DTI, N=47)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/cssl/cognitive_present.py`
