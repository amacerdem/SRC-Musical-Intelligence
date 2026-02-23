# MDNS E-Layer — Extraction (4D)

**Layer**: E (Extraction)
**Dimensions**: 4D (indices 0–3 of MDNS 12D output)
**Input**: R³ direct + H³ tuples
**Character**: Melody decoding features — note-onset tracking, pitch decoding, perception-imagery overlap

---

## Overview

The E-layer extracts 4 melody decoding features from R³ and H³ inputs. These capture the brain's ability to decode melodies from neural signals at both the note-onset and pitch levels, plus the shared representation between perception and imagery. Evidence base: Di Liberto et al. 2021 (EEG maxCorr TRF, n=21), Bellier et al. 2023 (iEEG, r²=0.429), Kraemer et al. 2005 (fMRI, PAC imagery).

---

## E0: Note-Onset Tracking (f01_note_tracking)

**Range**: [0, 1]
**Brain region**: Bilateral STG (phase-locking to note onsets)
**Question answered**: "How well does the brain track note boundaries in this music?"

### Formula

```python
flux_val = H3[(10, 6, 0, 0)]    # spectral_flux value at H6 (200ms)
onset_val = H3[(11, 6, 0, 0)]   # onset_strength value at H6 (200ms)
f01_note_tracking = σ(0.80 * flux_val * onset_val)
```

### R³ / H³ Inputs

| Source | Index/Tuple | Feature | Role |
|--------|-------------|---------|------|
| H³ | (10, 6, 0, 0) | spectral_flux, value, H6, L0 | Note onset envelope correlate |
| H³ | (11, 6, 0, 0) | onset_strength, value, H6, L0 | Event onset precision |

### Logic

The product of spectral flux and onset strength at the beat-entrainment horizon (200ms) captures note boundary detection. The α=0.80 coefficient reflects the study's effect size (d=0.80). Di Liberto 2021: maxCorr method achieves F(1,20)=80.6, p=1.9e-08 for note-onset decoding.

### Evidence
- Di Liberto et al. 2021: Note-onset tracking F(1,20)=80.6, p=1.9e-08 (EEG, n=21)
- Weineck et al. 2022: Spectral flux > amplitude envelope for neural sync, η²=0.55 (EEG, n=37)

---

## E1: Pitch Decoding (f02_pitch_decoding)

**Range**: [0, 1]
**Brain region**: Heschl's Gyrus / Planum Temporale (pitch extraction)
**Question answered**: "How accurately can individual melody pitches be decoded?"

### Formula

```python
tonal_val = H3[(14, 8, 0, 2)]     # tonalness value at H8 (300ms), bidirectional
autocorr_val = H3[(17, 8, 0, 2)]  # spectral_autocorrelation value at H8, bidi
helm_mean = H3[(2, 8, 1, 0)]      # helmholtz_kang mean at H8
f02_pitch_decoding = σ(0.85 * tonal_val * autocorr_val * helm_mean)
```

### R³ / H³ Inputs

| Source | Index/Tuple | Feature | Role |
|--------|-------------|---------|------|
| H³ | (14, 8, 0, 2) | tonalness, value, H8, L2 | Pitch clarity at motif scale |
| H³ | (17, 8, 0, 2) | spectral_autocorrelation, value, H8, L2 | Harmonic periodicity |
| H³ | (2, 8, 1, 0) | helmholtz_kang, mean, H8, L0 | Interval quality context |

### Logic

Triple product of tonal clarity, harmonic periodicity, and interval quality at the motif horizon (300ms). The β=0.85 coefficient reflects strong pitch decoding confidence. 20/21 participants showed significant pitch decoding at ≥4.8s segments. Sub-1 Hz EEG carries pitch information: F(1,20)=369.8, p=2.3e-14.

### Evidence
- Di Liberto et al. 2021: Pitch decoded in 20/21 participants, F(1,20)=142.3 (method)
- Di Liberto et al. 2021: Sub-1 Hz pitch encoding, F(1,20)=369.8, p=2.3e-14

---

## E2: Perception-Imagery Overlap (f03_percept_imag)

**Range**: [0, 1]
**Brain region**: Secondary Auditory Cortex (BA22) — shared substrate
**Question answered**: "How strongly does the imagined melody match the perceived representation?"

### Formula

```python
f03_percept_imag = σ(0.80 * (f01_note_tracking + f02_pitch_decoding) / 2)
```

### Dependencies

| Source | Feature | Role |
|--------|---------|------|
| E0 | f01_note_tracking | Onset tracking quality |
| E1 | f02_pitch_decoding | Pitch decoding quality |

### Logic

Averages note-onset and pitch decoding as a proxy for shared neural code quality. The γ=0.80 coefficient reflects that imagery decoding is reduced vs perception (F(1,20)=6.0, p=0.02 condition effect). Kraemer 2005 confirms PAC activation during instrumental imagery: F(1,14)=22.55, p<0.0005.

### Evidence
- Di Liberto et al. 2021: Imagery decoding possible but reduced, F(1,20)=6.0, p=0.02
- Kraemer et al. 2005: PAC imagery activation, F(1,14)=22.55, p<0.0005 (fMRI, n=15)
- Halpern et al. 2004: Secondary AC activated for both perception and imagery

---

## E3: Decoding Accuracy (f04_decoding_acc)

**Range**: [0, ~0.80]
**Brain region**: Bilateral STG → cortex (TRF decoding chain)
**Question answered**: "What is the overall individual-level decoding precision?"

### Formula

```python
f04_decoding_acc = 0.80 * (f01_note_tracking + f02_pitch_decoding + f03_percept_imag) / 3
```

### Dependencies

| Source | Feature | Role |
|--------|---------|------|
| E0 | f01_note_tracking | Onset component |
| E1 | f02_pitch_decoding | Pitch component |
| E2 | f03_percept_imag | Imagery overlap component |

### Logic

Average of all three E-layer features, scaled by the study's effect size d=0.80. Models individual-level decoding precision. Not a standalone belief — this is a validation metric that feeds M-layer and downstream integration.

### Evidence
- Di Liberto et al. 2021: Individual trial + individual participant decoding, d=0.80
- Bellier et al. 2023: Music reconstructed from ECoG, r²=0.429, 36/38 songs identified

---

## Layer Summary

| Idx | Name | Range | Key Inputs | Downstream |
|-----|------|-------|------------|------------|
| E0 | f01_note_tracking | [0, 1] | H³ flux+onset at H6 | M-layer, P-layer |
| E1 | f02_pitch_decoding | [0, 1] | H³ tonal+autocorr+helm at H8 | M-layer, P-layer |
| E2 | f03_percept_imag | [0, 1] | E0+E1 averaged | F-layer, → TPIO |
| E3 | f04_decoding_acc | [0, ~0.80] | E0+E1+E2 averaged×0.80 | F-layer, → IMU.MEAMN |

**Total E-layer H³ tuples**: 5 (of MDNS's 18 total)
