# ESME — Extraction

**Model**: Expertise-Specific MMN Enhancement
**Unit**: SPU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_pitch_mmn | Pitch MMN amplitude. Enhanced in singers and violinists. Pitch deviance detection strength weighted by consonance reference and onset context. f01 = σ(0.40 * abs(pitch_change_vel) + 0.30 * abs(helmholtz_diff) + 0.30 * onset_val). Koelsch et al. 1999: violinists show MMN to 0.75% pitch deviants in major chord triads; MMN absent in non-musicians. |
| 1 | f02_rhythm_mmn | Rhythm MMN amplitude. Enhanced in drummers and jazz musicians. Onset timing deviation weighted by spectral change velocity and temporal-spectral coupling. f02 = σ(0.40 * abs(onset_deviation) + 0.30 * spec_change_vel + 0.30 * x_l4l5_mean). Vuust et al. 2012: genre-specific gradient jazz > rock > pop > non-musicians for complex rhythmic deviants. Liao et al. 2024: percussionists recruit distinct NMR network. |
| 2 | f03_timbre_mmn | Timbre MMN amplitude. Enhanced for trained instrument timbre. Spectral envelope change weighted by tristimulus deviation across fundamental, mid, and high harmonics. f03 = σ(0.40 * timbre_change_std + 0.30 * tristimulus_deviation). Tervaniemi 2022 review: "sound parameters most important in performance evoke the largest MMN." |
| 3 | f04_expertise_enhancement | Expertise enhancement modulation. Domain-specific amplification of the strongest MMN channel. f04 = σ(α * max(f01, f02, f03)), where α is trainable. Criscuolo et al. 2022 ALE meta (k = 84, N = 3005): bilateral STG + L IFG (BA44) in musicians. Martins et al. 2022 constraint: no singer vs instrumentalist P2/P3 difference — clean 3-way dissociation is an oversimplification; the actual pattern is a gradient. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 2 | 0 | M0 (value) | L2 (bidi) | Consonance deviance baseline 25ms |
| 1 | 2 | 3 | M1 (mean) | L2 (bidi) | Consonance template 100ms |
| 2 | 23 | 3 | M8 (velocity) | L0 (fwd) | Pitch deviant detection velocity 100ms |
| 3 | 11 | 3 | M0 (value) | L0 (fwd) | Onset strength for rhythm deviance 100ms |
| 4 | 21 | 3 | M8 (velocity) | L0 (fwd) | Spectral deviance velocity 100ms |
| 5 | 33 | 8 | M0 (value) | L2 (bidi) | Temporal-spectral coupling 300ms |
| 6 | 18 | 2 | M0 (value) | L2 (bidi) | Tristimulus1 (F0 energy) instantaneous 17ms |
| 7 | 19 | 2 | M0 (value) | L2 (bidi) | Tristimulus2 (mid harmonics) instantaneous 17ms |
| 8 | 20 | 2 | M0 (value) | L2 (bidi) | Tristimulus3 (high harmonics) instantaneous 17ms |
| 9 | 24 | 8 | M3 (std) | L0 (fwd) | Timbre change magnitude 300ms |

---

## Computation

The E-layer extracts four explicit features that characterize domain-specific mismatch negativity responses and their expertise-dependent enhancement. The key insight is that MMN amplitude is enhanced in a domain-specific manner by musical training, following a gradient pattern rather than a clean dissociation (Tervaniemi 2022 review; Vuust et al. 2012).

All features use sigmoid activation with coefficient sums equal to 1.0 (saturation rule).

1. **f01** (pitch MMN): Computes pitch deviance detection from pitch change velocity at 100ms, helmholtz consonance difference (instantaneous minus template), and onset context. This captures the expertise effect demonstrated by Koelsch et al. 1999 where violinists detected 0.75% pitch deviants that non-musicians missed entirely.

2. **f02** (rhythm MMN): Computes onset timing deviation from onset strength at 100ms, spectral change velocity, and temporal-spectral coupling at 300ms. This captures the genre-specific gradient (Vuust et al. 2012) and the distinct percussionist NMR network (Liao et al. 2024).

3. **f03** (timbre MMN): Computes spectral envelope change from timbre change standard deviation at 300ms and tristimulus deviation (std across fundamental, mid, and high harmonic energies at 17ms). The tristimulus components at gamma-band resolution capture instantaneous spectral identity.

4. **f04** (expertise enhancement): Modulates the maximum across all three domain-specific MMNs by a trainable alpha parameter. This implements the gradient principle: all musicians show some general enhancement, but the strongest enhancement occurs in the trained domain.

H³ tuples span H0 (25ms) through H8 (300ms), using both L0 (forward) and L2 (bidirectional) laws. Gamma-band tristimulus features (H2, 17ms) capture instantaneous timbre identity; alpha-band features (H3, 100ms) capture deviance templates; delta-band features (H8, 300ms) capture sustained deviant magnitude.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³[0] roughness | Dissonance baseline | Normalizing pitch deviants |
| R³[2] helmholtz_kang | Consonance reference | Pitch deviance baseline and template |
| R³[11] onset_strength | Onset timing | Rhythm deviance detection |
| R³[12] warmth | Timbre baseline | Timbre deviance context |
| R³[14] tonalness | Pitch clarity | Harmonic-to-noise reference |
| R³[18:21] tristimulus | Harmonic energy distribution | Timbre identity for spectral envelope change |
| R³[21] spectral_change | Spectral flux | Spectral deviance velocity |
| R³[23] pitch_change | Pitch flux | Pitch deviance velocity |
| R³[33:41] x_l4l5 | Temporal-spectral coupling | Emergent deviance patterns |
| H³ (10 tuples) | Multi-scale temporal morphology | Deviance detection at gamma through delta timescales |
