# AMSS E-Layer — Extraction (5D)

**Layer**: Extraction (E)
**Indices**: [0:5]
**Scope**: internal
**Activation**: sigmoid
**Model**: AMSS (STU-B1, Attention-Modulated Stream Segregation, 11D, beta-tier 70-90%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:onset_tracking | [0, 1] | Onset-driven envelope tracking. sigma(envelope * attention) at 150-220ms window. Envelope following response modulated by attentional state. Bellier 2023: STRF-based onset encoding in primary auditory cortex. |
| 1 | E1:harmonic_segregation | [0, 1] | Harmonic template matching for stream separation. Tonalness-driven — harmonically rich sounds form coherent streams. Mesgarani & Chang 2012: neural segregation follows harmonic structure in STG. |
| 2 | E2:spectral_stream | [0, 1] | Spectral stream boundary detection. Spectral centroid + spectral change drive stream formation along the frequency axis. Mischler 2025: iEEG shows spectral stream boundaries in HG. |
| 3 | E3:temporal_stream | [0, 1] | Temporal stream continuity tracking. Beat-locked temporal patterns maintain stream coherence over time. Hausfeld 2021: temporal regularity sustains stream percept (d=0.60). |
| 4 | E4:attention_gate | [0, 1] | Attention-modulated processing gate. Attended > unattended envelope tracking — selective amplification of the attended stream. Basinski 2025: ORN F(2,170)=31.38 for attended vs. unattended. |

---

## Design Rationale

1. **Onset Tracking (E0)**: Tracks how envelope onsets are captured under attentional modulation. The 150-220ms window corresponds to the early auditory processing latency where N1/P2 responses reflect onset encoding. Attention amplifies envelope tracking for the selected stream.

2. **Harmonic Segregation (E1)**: Uses tonalness to drive harmonic template matching. Harmonically coherent partials are grouped into a single stream — the fundamental principle of auditory scene analysis. Higher tonalness means stronger harmonic grouping.

3. **Spectral Stream (E2)**: Detects boundaries between spectral streams using spectral centroid position and spectral change rate. When spectral centroid jumps, a new stream boundary is inferred. This is the frequency-domain component of segregation.

4. **Temporal Stream (E3)**: Tracks continuity within streams over time. Beat-locked patterns maintain temporal coherence — a stream that follows a regular temporal pattern is more easily maintained. This is the time-domain component of segregation.

5. **Attention Gate (E4)**: The selective attention mechanism. Attended streams receive amplified processing (larger envelope tracking response), while unattended streams are suppressed. This gate modulates all downstream processing — the ORN (Object-Related Negativity) reflects the cost of segregation.

---

## H3 Dependencies (E-Layer)

The AMSS E-layer draws from 16 H3 tuples total (full model). E-layer specific tuples focus on onset, harmonic, spectral, and temporal features at early processing horizons.

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (7, *, *, *) | amplitude morphologies | Envelope tracking for onset detection |
| (8, *, *, *) | loudness morphologies | Loudness-weighted envelope following |
| (10, *, *, *) | spectral_flux morphologies | Spectral change detection for stream boundaries |
| (11, *, *, *) | onset_strength morphologies | Onset event detection |
| (14, *, *, *) | tonalness morphologies | Harmonic template matching strength |
| (15, *, *, *) | spectral_centroid morphologies | Spectral stream position |
| (21, *, *, *) | spectral_change morphologies | Stream boundary velocity |
| (25:33, *, *, *) | x_l0l5 morphologies | Cross-domain coupling for attention gate |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [7] | amplitude | E0: envelope onset tracking |
| [8] | loudness | E0: perceptual loudness weighting |
| [10] | spectral_flux | E2: spectral change for stream boundaries |
| [11] | onset_strength | E0: event onset detection |
| [14] | tonalness | E1: harmonic template matching |
| [15] | spectral_centroid | E2: spectral stream position |
| [21] | spectral_change | E2: spectral stream boundary velocity |
| [25:33] | x_l0l5 | E3+E4: cross-domain coupling patterns |

---

## Scientific Foundation

- **Basinski et al. 2025**: ORN amplitude F(2,170)=31.38 — attention modulates stream segregation cost (EEG)
- **Hausfeld et al. 2021**: Attentional modulation of streaming d=0.60, 3T fMRI, N=14
- **Wikman et al. 2025**: fMRI evidence for attention-dependent stream segregation in auditory cortex
- **Mischler et al. 2025**: iEEG reveals spectral stream boundaries in high-gamma band
- **Bellier et al. 2023**: STRF-based onset encoding in primary auditory cortex
- **Mesgarani & Chang 2012**: Selective cortical representation of attended speaker in multi-talker scenes (ECoG)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/amss/extraction.py`
