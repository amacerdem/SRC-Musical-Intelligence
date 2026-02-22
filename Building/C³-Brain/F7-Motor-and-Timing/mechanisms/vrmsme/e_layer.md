# VRMSME — Extraction

**Model**: VR Music Stimulation Motor Enhancement
**Unit**: MPU-β3
**Function**: F7 Motor & Timing
**Tier**: β (Bridging)
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f16_music_enhancement | VRMS motor enhancement superiority over VRAO/VRMI. f16 = σ(0.40 * coupling_period_1s + 0.30 * music_period_1s + 0.30 * music_onset_100ms). Captures the unique motor-enhancing effect of VR music stimulation: music adds a dimension to VR that observation and imagery cannot replicate. Liang et al. 2025: VRMS > VRAO in bilateral PM&SMA connectivity (RS1, LPMSMA, RPMSMA p<.01 FDR). Range [0, 1]. |
| 1 | f17_bilateral_activation | Bilateral sensorimotor activation (S1/PM/SMA/M1). f17 = σ(0.40 * sensorimotor_period_1s + 0.30 * sensorimotor_period_500ms + 0.30 * sensorimotor_100ms). The bilateral activation pattern that distinguishes VRMS from VRMI. Liang et al. 2025: VRMS > VRMI in bilateral M1 activation (RM1, LM1 p<.05 HBT). Range [0, 1]. |
| 2 | f18_network_connectivity | PM-DLPFC-M1 interaction network strength. f18 = σ(0.35 * f16 * f17 + 0.35 * loudness_entropy_100ms + 0.30 * binding_variability_100ms). Captures the heterogeneous functional connectivity pattern unique to VRMS. The interaction term (f16 * f17) requires both music enhancement AND bilateral activation for strong network connectivity. Liang et al. 2025: VRMS shows strongest PM-DLPFC-M1 heterogeneous FC (RDLPFC-LPMSMA, RPMSMA-RM1 p<.01 FDR). Range [0, 1]. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 3 | M0 (value) | L2 (bidi) | Music onset at 100ms — fast auditory detection |
| 1 | 10 | 16 | M14 (periodicity) | L2 (bidi) | Music periodicity 1s — sustained auditory regularity |
| 2 | 11 | 3 | M0 (value) | L2 (bidi) | Beat strength 100ms — motor timing marker |
| 3 | 11 | 16 | M14 (periodicity) | L2 (bidi) | Onset periodicity 1s — beat regularity |
| 4 | 25 | 3 | M0 (value) | L2 (bidi) | VR-motor coupling 100ms — fast multi-modal link |
| 5 | 25 | 3 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 100ms — fast coupling regularity |
| 6 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s — sustained coupling regularity |
| 7 | 33 | 3 | M0 (value) | L2 (bidi) | Sensorimotor binding 100ms — fast action-perception link |
| 8 | 33 | 3 | M2 (std) | L2 (bidi) | Binding variability 100ms — sensorimotor stability |
| 9 | 33 | 8 | M14 (periodicity) | L2 (bidi) | Sensorimotor period 500ms — mid-scale binding |
| 10 | 33 | 16 | M14 (periodicity) | L2 (bidi) | Sensorimotor period 1s — sustained binding regularity |
| 11 | 8 | 3 | M20 (entropy) | L2 (bidi) | Loudness entropy 100ms — auditory complexity |

---

## Computation

The E-layer extracts three explicit features capturing the core effects of VR music stimulation on the sensorimotor network.

**f16 (music_enhancement)** is the VR music stimulation advantage signal. It combines multi-modal coupling periodicity at 1s (sustained VR-music-motor coupling), music periodicity at 1s (sustained auditory regularity), and music onset at 100ms (immediate onset detection). This captures the unique contribution of music to VR motor stimulation: periodic auditory-motor coupling at sustained timescales produces stronger motor enhancement than observation or imagery alone.

**f17 (bilateral_activation)** captures the bilateral sensorimotor activation pattern. It combines sensorimotor binding periodicity at three timescales: 1s (sustained bilateral activation), 500ms (mid-range activation), and 100ms (fast action-perception binding). This multi-scale combination reflects the VRMS finding that bilateral M1 activation — measured via homotopic brain connectivity — is stronger with music stimulation.

**f18 (network_connectivity)** captures the PM-DLPFC-M1 heterogeneous connectivity network. The interaction term (f16 * f17) is critical: both music enhancement AND bilateral activation must be present for strong network connectivity, reflecting the finding that the PM-DLPFC-M1 network is uniquely activated in VRMS (not VRAO or VRMI). Loudness entropy adds auditory complexity and binding variability adds sensorimotor stability as modulators.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³[10] spectral_flux | Music onset detection | VR audio synchronization anchor |
| R³[11] onset_strength | Beat marker strength | Motor timing markers for VR entrainment |
| R³[8] loudness | Perceptual intensity | Loudness entropy for auditory complexity |
| R³[25] x_l0l5[0] | Multi-modal coupling | VR-audio-motor coupling pathway |
| R³[33] x_l4l5[0] | Sensorimotor binding | Action-perception link for bilateral activation |
| H³ (12 tuples) | Multi-scale temporal dynamics | Fast (100ms) to sustained (1s) multi-modal binding |
