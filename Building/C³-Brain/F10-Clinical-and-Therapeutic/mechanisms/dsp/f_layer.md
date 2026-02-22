# DSP — Forecast

**Model**: Developmental Singing Plasticity
**Unit**: NDU
**Function**: F10 Clinical & Therapeutic
**Tier**: beta
**Layer**: F — Forecast
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 9 | ac_maturation | Auditory cortex development prediction. Forecasts trajectory of auditory cortex maturation based on cumulative plasticity, current vocal learning state, and onset variability trends. Partanen 2022: singing intervention group exceeded full-term baseline in oddball paradigm (F(2,27)=4.019, p=0.030, eta^2=0.229) — over-normalization effect demonstrates AC maturation can surpass typical development with quality singing exposure. Kaminska 2025: age-dependent gamma increase and leftward lateralization track AC maturation trajectory. |
| 10 | speech_transfer | Language region transfer prediction. Predicts generalization from singing-driven auditory plasticity to speech perception, based on pitch change dynamics and session memory. Partanen 2022: singing group males showed enhanced MMR for vowel duration deviants (p=0.001), demonstrating transfer from singing to speech-relevant phonemic processing. Nguyen 2023: early musical social communication scaffolds later language development. |
| 11 | mmr_enhancement | Deviance detection future state. Predicts expected mismatch response enhancement at upcoming time steps, combining contour entropy, vocal periodicity, and onset variability. Higher values predict stronger future MMR — the core clinical outcome of singing intervention. Partanen 2022: intervention group achieved over-normalization in oddball (eta^2=0.229). Yu 2015: MMN plasticity reflects auditory regularity learning over time. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 16 | 10 | 3 | M2 (std) | L2 (bidi) | Onset variability at 100ms for maturation trend |
| 17 | 23 | 3 | M0 (value) | L2 (bidi) | Pitch change at 100ms for speech transfer |

---

## Computation

The F-layer generates predictions about developmental outcomes of singing intervention:

1. **AC maturation** (idx 9): Predicts auditory cortex developmental trajectory from cumulative plasticity (M-layer), vocal learning state (P-layer), and onset variability at 100ms (H3). The onset variability morph (M2, standard deviation) captures the diversity of acoustic onsets in the singing stimulus — varied onset patterns drive broader auditory cortex tuning. Under the over-normalization finding (Partanen 2022), this prediction can exceed typical developmental trajectories when singing quality is sustained, reflecting the remarkable plasticity of preterm auditory cortex that enables intervention groups to surpass full-term baselines. Kaminska 2025's age-dependent gamma increase provides the neural substrate for this maturation trajectory.

2. **Speech transfer** (idx 10): Predicts generalization of singing-driven plasticity to speech perception using pitch change at 100ms (H3) and session memory (M-layer). Pitch change dynamics during singing share acoustic features with speech prosody — melodic contours in infant-directed singing parallel the exaggerated pitch contours of infant-directed speech. When singing sessions are melodically rich (high session memory) and pitch dynamics are active, the model predicts stronger transfer to speech-relevant auditory processing. Partanen 2022 confirmed this transfer: singing group males showed enhanced MMR specifically for vowel duration deviants, a speech-relevant acoustic feature.

3. **MMR enhancement** (idx 11): Predicts the expected future magnitude of mismatch response enhancement. Combines contour entropy and vocal periodicity from E-layer (f03 plasticity index components) with onset variability (H3) to extrapolate the trajectory of deviance detection improvement. This is the primary clinical outcome prediction — will the current singing intervention lead to enhanced MMR at follow-up? The prediction integrates both the quality of current stimulation (entropy, periodicity) and the temporal dynamics of onset patterns (variability as a driver of neural tuning breadth). sigma(0.50 * contour_entropy_125ms + 0.50 * vocal_periodicity_100ms) forms the base, modulated by onset variability trend.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f03_plasticity_index | Base plasticity signal for MMR enhancement prediction |
| M-layer | cumulative_plasticity | Accumulated exposure for AC maturation trajectory |
| M-layer | session_memory | Session richness for speech transfer prediction |
| P-layer | vocal_learning | Current encoding state for maturation prediction |
| R3 [10] | spectral_flux | Onset variability for maturation and MMR predictions |
| R3 [23] | pitch_change | Pitch dynamics for speech transfer prediction |
| H3 | 2 tuples (see above) | Onset variability and pitch change at 100ms |
