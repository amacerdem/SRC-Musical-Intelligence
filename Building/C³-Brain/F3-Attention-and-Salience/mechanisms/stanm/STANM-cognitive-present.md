# STANM P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [6:8]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 6 | P0:temporal_alloc | [0, 1] | Temporal attention allocation. sigma(...+0.5*temporal_period_1s). Real-time measure of how much processing resource is directed to temporal/rhythmic structure. Haiduk 2024: left AC activation scales with temporal attention demand (fMRI, p<0.001). |
| 7 | P1:spectral_alloc | [0, 1] | Spectral attention allocation. sigma(...+0.5*tonalness_mean_1s). Real-time measure of how much processing resource is directed to spectral/pitch structure. Norman-Haignere 2022: iEEG frequency-selective responses in right AC (F=104.71). |

---

## Design Rationale

1. **Temporal Allocation (P0)**: The present-moment temporal attention signal. Captures how much of the auditory processing pipeline is currently allocated to temporal features (rhythm, meter, speech prosody). Uses the 1s temporal periodicity to ensure allocation reflects sustained temporal structure rather than transient events. Feeds downstream to salience computation and F3 attention modulation.

2. **Spectral Allocation (P1)**: The present-moment spectral attention signal. Captures how much processing is allocated to spectral features (melody, harmony, timbre). Uses the 1s tonalness mean for stability. Together with P0, these two signals define the attentional "mode" — temporal vs spectral emphasis. Their relative balance corresponds to the M-layer lateralization.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `temporal_alloc` | P0 [6] | Attention modulation: temporal processing weight |
| `spectral_alloc` | P1 [7] | Attention modulation: spectral processing weight |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 16, 14, 2) | spectral_flux periodicity H16 L2 | Temporal periodicity at 1s — allocation anchor |
| (14, 16, 1, 2) | tonalness mean H16 L2 | Sustained tonalness at 1s — spectral allocation anchor |
| (10, 4, 14, 2) | spectral_flux periodicity H4 L2 | Beat periodicity at 125ms — fast temporal modulation |
| (8, 3, 0, 2) | loudness value H3 L2 | Perceptual loudness — baseline activation |

---

## Scientific Foundation

- **Haiduk et al. 2024**: Left AC activation scales with temporal attention demand (fMRI, p<0.001)
- **Norman-Haignere et al. 2022**: Frequency-selective attention responses in AC (iEEG, F=104.71)
- **Zatorre et al. 2022**: Temporal vs spectral allocation maps to L/R hemispheres (review)
- **Kim et al. 2019**: Attention allocation predicts processing efficiency (T=6.852)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/stanm/cognitive_present.py`
