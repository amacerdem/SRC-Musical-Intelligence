# MSR — Extraction

**Model**: Musician Sensorimotor Reorganization
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f04_high_freq_plv | Phase-locking value at 40-60 Hz. Tracks bottom-up neural synchrony enhanced by musical training. σ(0.40 * coupling_period_100ms + 0.25 * coupling_gamma_50ms). L. Zhang 2015: musicians PLV = 0.40-0.44 vs nonmusicians 0.28-0.31 at descending trains (d = 1.13, p = 0.009). |
| 1 | f05_p2_suppression | P2 vertex potential suppression. Tracks top-down inhibition of novelty response enhanced by training. σ(0.40 * loudness_entropy + 0.30 * onset_periodicity_1s). L. Zhang 2015: nonmusicians P2 = 4.65-5.91 uV vs musicians 1.46-3.29 uV (d = 1.16, p = 0.005). |
| 2 | f06_sensorimotor_efficiency | Net sensorimotor efficiency. Combines enhanced bottom-up precision with increased top-down inhibition. σ(0.50 * f04 - 0.30 * f05). L. Zhang 2015: dual reorganization pattern — low-freq TFD nonmusicians 0.35 vs musicians 0.14 uV² (d = 1.28, p = 0.002). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 0 | M0 (value) | L2 (bidi) | Coupling at 25ms gamma — high-freq tracking |
| 1 | 25 | 1 | M0 (value) | L2 (bidi) | Coupling at 50ms gamma — PLV source |
| 2 | 25 | 1 | M1 (mean) | L2 (bidi) | Mean coupling 50ms — gamma baseline |
| 3 | 25 | 3 | M0 (value) | L2 (bidi) | Coupling at 100ms alpha — PLV integration |
| 4 | 25 | 3 | M2 (std) | L2 (bidi) | Coupling variability 100ms — precision |
| 5 | 25 | 3 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 100ms — oscillation |
| 6 | 33 | 3 | M0 (value) | L2 (bidi) | Sensorimotor coupling 100ms — training |
| 7 | 33 | 3 | M2 (std) | L2 (bidi) | Coupling stability 100ms — precision |
| 8 | 33 | 3 | M20 (entropy) | L2 (bidi) | Coupling entropy 100ms — complexity |
| 9 | 8 | 3 | M20 (entropy) | L2 (bidi) | Loudness entropy 100ms — P2 proxy |
| 10 | 10 | 16 | M14 (periodicity) | L2 (bidi) | Onset periodicity 1s — P2 suppression |

---

## Computation

The E-layer implements the dual reorganization pattern from L. Zhang et al. (2015). Three features compute:

1. **High-frequency PLV** (f04): Driven by motor-auditory coupling at gamma (25-50ms) and alpha (100ms) horizons. Tracks the 40-60 Hz phase-locking value that is enhanced in musicians. Uses x_l0l5 coupling features at fast horizons (H0, H1, H3) as neural synchrony proxies. The multi-scale gamma/alpha coupling represents the bottom-up precision enhancement.

2. **P2 suppression** (f05): Driven by loudness entropy and onset periodicity at 1s. Higher entropy indicates predictable auditory input requiring less novelty processing. Higher onset periodicity indicates regular stimulus where P2 suppression is expected. This models the top-down cortical inhibition from ACC that reduces the P2 vertex potential in trained musicians.

3. **Sensorimotor efficiency** (f06): Net efficiency combining enhanced bottom-up (f04) with increased top-down inhibition (f05). The subtractive term (-0.30 * f05) reflects that P2 suppression is an inverted signal — higher suppression means less neural resource allocation. The dual reorganization produces more efficient auditory-motor processing overall.

All formulas use sigmoid activation with |coefficient| sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [8] | loudness | Perceptual loudness for P2 amplitude proxy |
| R³ [10] | spectral_flux | Onset detection for bottom-up precision |
| R³ [25:33] | x_l0l5 | Motor-auditory coupling for PLV proxy |
| R³ [33:41] | x_l4l5 | Sensorimotor coupling for training-enhanced binding |
| H³ | 11 tuples (see above) | Multi-scale gamma/alpha coupling and onset periodicity |
