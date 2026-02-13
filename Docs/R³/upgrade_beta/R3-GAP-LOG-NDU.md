# R³ Gap Log — NDU (Novelty Detection Unit)

**Created**: 2026-02-13
**Unit**: NDU (Novelty Detection)
**Models**: #48-#56

---

## Gaps Found During C³ Revision

### GAP-NDU-001: Syntactic Irregularity Level
- **Source**: Kim et al. 2021 (MEG effective connectivity, n=19)
- **Proposed**: r3:X27.syntactic_irregularity_level
- **Evidence**: IFG-LTDMI enhanced for most irregular condition F(2,36)=6.526, p=0.024; dissociable from perceptual ambiguity
- **NDU Models**: SDD, CDMR
- **Current R³ Coverage**: No dimension captures degree of harmonic syntax violation
- **Recommendation**: Consider adding a syntactic regularity feature to R³ interactions group

### GAP-NDU-002: Perceptual Ambiguity Level
- **Source**: Kim et al. 2021 (MEG effective connectivity, n=19)
- **Proposed**: r3:X28.perceptual_ambiguity_level
- **Evidence**: STG-LTDMI enhanced for most ambiguous F(2,36)=12.373, p<0.001; dissociable from syntactic irregularity
- **NDU Models**: SDD
- **Current R³ Coverage**: No dimension captures auditory perceptual ambiguity
- **Recommendation**: May be derivable from existing spectral features rather than new dimension

### GAP-NDU-003: Cortical Entrainment Index
- **Source**: Bridwell et al. 2017 (EEG, n=13)
- **Proposed**: r3:X23.cortical_entrainment_index
- **Evidence**: MMN-entrainment correlation r=0.65, p=0.015; neural tracking scales with regularity
- **NDU Models**: CDMR, SLEE
- **Current R³ Coverage**: Partially covered by onset_strength periodicity but lacks entrainment specificity
- **Recommendation**: May be an H³-level feature rather than R³

### GAP-NDU-004: Perceived Musical Roundness
- **Source**: Wöhrle et al. 2024 (MEG, n=30)
- **Proposed**: r3:X26.perceived_musical_roundness
- **Evidence**: CHORD3 effect η²p=0.592 (behavioral), η²p=0.101 (N1m), η²p=0.095 (expertise interaction)
- **NDU Models**: CDMR, EDNR
- **Current R³ Coverage**: Partially covered by consonance group but lacks gestalt chord quality
- **Recommendation**: Investigate whether existing consonance features can derive this

### GAP-NDU-005: Spectral Flux as Primary Novelty Feature
- **Source**: Weineck et al. 2022 (EEG, neural synchronization study)
- **Evidence**: Spectral flux is the STRONGEST predictor of neural synchronization, subsumes amplitude envelope + onset strength + beat times; TRF latency 102-211ms
- **NDU Models**: ALL (especially MPG)
- **Current R³ Coverage**: spectral_flux [R³ idx 10] EXISTS but its primacy for novelty detection is not reflected in model weighting
- **Recommendation**: NDU models should weight spectral_flux more heavily; current R³ coverage is adequate but model formulas may underweight it
