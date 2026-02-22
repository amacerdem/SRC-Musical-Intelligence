# STANM E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:temporal_attention | [0, 1] | Speech-directed temporal attention. f13 = sigma(0.35*temporal_period_1s + 0.30*tempo_velocity_500ms). Haiduk 2024: left auditory cortex preferentially processes temporal structure (fMRI, p<0.001). |
| 1 | E1:spectral_attention | [0, 1] | Melody-directed spectral attention. f14 = sigma(0.35*tonalness_mean_1s + 0.30*tonalness_value). Zatorre 2022: right auditory cortex preferentially processes spectral/pitch structure (L/R dissociation). |
| 2 | E2:network_topology | [0, 1] | Local network clustering. f15 = sigma(0.35*energy_var_500ms + 0.30*coupling_entropy). Jin 2024: spectrotemporal attention networks show distinct clustering topologies (eta2p=0.526). |

---

## Design Rationale

1. **Temporal Attention (E0)**: Tracks the allocation of attentional resources to temporal structure — rhythm, meter, and speech prosody. Uses spectral_flux periodicity at 1s horizon for sustained temporal regularity and spectral_change velocity at 500ms for tempo dynamics. This captures the left-hemisphere-dominant temporal processing stream.

2. **Spectral Attention (E1)**: Tracks attention to spectral/pitch structure — melody, harmony, and timbre. Uses tonalness mean at 1s horizon for sustained tonal content and instantaneous tonalness value. This captures the right-hemisphere-dominant spectral processing stream. The L/R dissociation is a foundational finding in auditory neuroscience.

3. **Network Topology (E2)**: Captures the local clustering structure of the attention network. Uses energy variability at 500ms and motor-auditory coupling entropy. High local clustering indicates that nearby processing nodes are tightly interconnected, enabling efficient local computation.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 16, 14, 2) | spectral_flux periodicity H16 L2 | Temporal periodicity at 1s — main temporal attention signal |
| (21, 8, 8, 0) | spectral_change velocity H8 L0 | Tempo velocity at 500ms — temporal dynamics |
| (14, 3, 0, 2) | tonalness value H3 L2 | Instantaneous tonalness at 100ms — spectral attention |
| (14, 16, 1, 2) | tonalness mean H16 L2 | Sustained tonalness mean at 1s — spectral stability |
| (22, 8, 2, 0) | energy_change std H8 L0 | Energy variability at 500ms — network topology |
| (25, 3, 20, 2) | x_l0l5[0] entropy H3 L2 | Coupling entropy at 100ms — local clustering |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [10] | spectral_flux | E0: temporal onset detection |
| [14] | tonalness | E1: spectral/pitch content |
| [21] | spectral_change | E0: tempo dynamics source |
| [22] | energy_change | E2: energy variability source |
| [25:33] | x_l0l5 | E2: motor-auditory coupling features |

---

## Scientific Foundation

- **Haiduk et al. 2024**: Left AC preferentially processes temporal structure (fMRI, p<0.001)
- **Zatorre et al. 2022**: L/R dissociation — left temporal, right spectral (review)
- **Jin et al. 2024**: Spectrotemporal network topology with distinct clustering (eta2p=0.526)
- **Norman-Haignere et al. 2022**: iEEG confirms frequency-selective attention in AC (F=104.71)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/stanm/extraction.py`
