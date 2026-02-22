# CSSL E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:rhythm_copying | [0, 1] | Motor-auditory rhythm entrainment strength. Basal ganglia / Area X motor loop. rhythm_copying = sigma(0.30 * x_l0l5.mean + 0.30 * onset_strength * encoding.mean + 0.30 * retrieval.mean). Burchardt et al. 2025: r=0.88 overall IOI beat correlation (N=54). |
| 1 | E1:melody_copying | [0, 1] | Melodic template matching strength. HVC / Auditory cortex pathway. melody_copying = sigma(0.35 * stumpf * tonalness + 0.35 * familiarity.mean + 0.30 * pitch_strength). Bolhuis & Moorman 2015: HVC-Broca neural homology for song timing. |
| 2 | E2:all_shared_binding | [0, 1] | Complete melody-rhythm binding. Hippocampal sequential binding. all_shared = sigma(0.40 * x_l5l7.mean * familiarity.mean + 0.30 * rhythm_copying + 0.30 * melody_copying). Burchardt et al. 2025: r=0.94 all-shared element correlation (p=0.01, N=54). |

---

## Design Rationale

1. **Rhythm Copying (E0)**: Tracks the motor-auditory entrainment that underlies rhythmic imitation in both songbirds and humans. Uses energy-consonance interaction (x_l0l5) as the motor-auditory coupling signal, onset strength for rhythm boundary detection, and retrieval for motor replay. The basal ganglia (Area X in songbirds) gates motor output against the auditory template.

2. **Melody Copying (E1)**: Tracks how accurately the melodic contour template is being matched. Stumpf fusion times tonalness captures tonal coherence (the "purity" of the melodic signal). Pitch strength provides clarity of the fundamental frequency. This maps to the HVC-auditory cortex pathway in songbirds.

3. **All-Shared Binding (E2)**: The integrative signal representing complete song template binding. This is the CSSL's core output — the r=0.94 "all-shared" correlation from Burchardt et al. 2025. It requires BOTH rhythm copying AND melody copying to be active (weighted 0.30 each), plus the consonance-timbre interaction (x_l5l7) as the unified song template signal.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 16, 1, 2) | stumpf_fusion mean H16 L2 | Binding stability at beat level for melody copying |
| (6, 16, 0, 2) | pitch_strength value H16 L2 | Current pitch clarity for melody template |
| (11, 16, 0, 2) | onset_strength value H16 L2 | Current rhythm boundary for beat segmentation |
| (14, 16, 0, 2) | tonalness value H16 L2 | Current tonal purity for melody matching |
| (22, 16, 0, 2) | entropy value H16 L2 | Current pattern complexity for template novelty |
| (12, 16, 0, 2) | warmth value H16 L2 | Current voice quality for song recognition |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E2: consonance component of binding |
| [1] | sethares_dissonance | Harmonic structure quality |
| [3] | stumpf_fusion | E1+E2: tonal fusion = binding strength |
| [5] | harmonicity | E1: harmonic-to-noise ratio = song purity |
| [6] | pitch_strength | E1: pitch clarity for melody template |
| [7] | amplitude | E0: vocal intensity / energy level |
| [11] | onset_strength | E0: rhythm boundary marker |
| [14] | tonalness | E1: tonal purity for melody matching |
| [22] | entropy | E2: pattern complexity / familiarity |
| [25:33] | x_l0l5 | E0: motor-auditory coupling for rhythm |
| [41:49] | x_l5l7 | E2: melody-timbre binding for song template |

---

## Brain Regions

| Region | MNI Coordinates | E-Layer Role |
|--------|-----------------|-------------|
| Auditory cortex (STG/A1) | +/-60, -32, 8 | E0+E1: spectrotemporal encoding, template storage |
| Basal ganglia (putamen/caudate) | +/-24, 2, 4 | E0: motor sequencing, vocal refinement, reward gating |
| Hippocampus | +/-20, -24, -12 | E2: sequential binding (rhythm + melody into song) |
| IFG / Broca's area | +/-48, 14, 8 | E1: song timing and sequencing, vocal learning control |

---

## Scientific Foundation

- **Burchardt, Varkevisser & Spierings 2025**: Zebra finch tutees copy melody and rhythm from tutors; r=0.94 all-shared, r=0.88 overall (N=54)
- **Bolhuis, Okanoya & Scharff 2010**: FoxP2, basal ganglia, auditory cortex homologies across species (review)
- **Bolhuis & Moorman 2015**: HVC-Broca's area, Area X-basal ganglia neural circuit homologies (review)
- **Jarvis 2004**: 7 homologous cerebral vocal nuclei for learned birdsong and human language (review)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/cssl/extraction.py`
