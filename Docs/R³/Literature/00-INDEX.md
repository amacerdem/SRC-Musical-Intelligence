# R3 Literature Index

> **Scope**: Literature references supporting the R3 spectral architecture (128D)
> **Sources**: R3-DSP-SURVEY-THEORY.md Section 7, R3-DSP-SURVEY-TOOLS.md Section 8
> **Created**: 2026-02-13

---

## Directory Contents

| File | Description |
|------|-------------|
| [R3-LITERATURE.md](R3-LITERATURE.md) | Complete 128-feature literature cross-reference: feature index, name, primary paper, DSP reference, local file |

## Literature Subdirectory (r3/)

The local literature files are stored in `Literature/r3/` organized by category:

| Subdirectory | Files | Category |
|-------------|:-----:|----------|
| `psychoacoustics/` | 11 | Plomp-Levelt, Sethares, Helmholtz, JI, neural correlates |
| `dsp-and-ml/` | 4 | CNN genre classification, spectral contrast, modulation, microtonal AMT |
| `spectral-music/` | 7 | Anderson, Grisey, Fineberg, spectral composition theory |
| `computational-music-theory/` | 65 | Tymoczko, Neo-Riemannian, Balzano, Lewin, Hook |
| `music-theory-analysis/` | 34 | Consonance models, geometry, neurodynamics, affect |
| **Total** | **121** | |

## Key References by Domain

### Consonance (Group A)
- Plomp & Levelt (1965) -- critical band roughness
- Sethares (1993) -- timbre-dependent dissonance
- Vassilakis (2005) -- 3-factor roughness model
- Harrison & Pearce (2020) -- composite consonance model
- Pressnitzer & McAdams (2000) -- critical bandwidth review

### Pitch (Group F)
- Shepard (1964) -- octave equivalence / chroma
- Krumhansl (1990) -- cognitive foundations of pitch
- Parncutt (1989/2019) -- virtual pitch salience
- Terhardt (1979) -- harmonicity and periodicity

### Rhythm (Group G)
- Witek et al. (2014) -- syncopation and groove
- Grahn & Brett (2007) -- metrical hierarchy
- Madison (2006) / Janata (2012) -- groove features
- Ravignani (2021) -- rhythmic regularity (nPVI)

### Harmony (Group H)
- Krumhansl & Kessler (1982) -- tonal hierarchy / key profiles
- Harte (2006) -- 6D Tonnetz from chroma
- Tymoczko -- geometry of music / voice-leading
- Lerdahl (2001) -- tonal pitch space / harmonic tension

### Information (Group I)
- Pearce (2005/2018) -- IDyOM / statistical learning
- Gold (2019) -- melodic/harmonic entropy
- Cheung (2019) -- prediction error and reward
- Shannon (1948) -- information theory foundations

### Timbre Extended (Group J)
- Jiang et al. (2002) -- spectral contrast
- Krimphoff et al. (1994) -- spectral irregularity
- Chi, Ru & Shamma (2005) -- modulation spectrum

### Modulation & Psychoacoustic (Group K)
- Zwicker & Fastl (1999) -- psychoacoustics textbook
- ISO 532-1 (2017) -- Zwicker loudness
- ISO 226 (2003) -- equal-loudness contours
- DIN 45692 -- sharpness
- Stevens (1957) -- power law of loudness

## Cross-References

- Feature definitions: `Docs/R3/upgrade_beta/R3-CROSSREF.md` Section 4
- Unit mappings: `Docs/R3/Mappings/`
- DSP theory survey: `Docs/R3/upgrade_beta/R3-DSP-SURVEY-THEORY.md`
- DSP tools survey: `Docs/R3/upgrade_beta/R3-DSP-SURVEY-TOOLS.md`
