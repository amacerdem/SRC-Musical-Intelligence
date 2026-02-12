# R³ Gap Log — ASU (Auditory Salience Unit)

**Created**: 2026-02-13
**Unit**: ASU (Auditory Salience)
**Chat**: Chat 2 (BATCH 4)

---

## Gaps Found During C³ Revision

### SNEM (ASU-α1) — Selective Neural Entrainment Model

| Gap ID | Proposed R³ Feature | Source Paper | Evidence | Priority |
|--------|---------------------|-------------|----------|----------|
| ASU-G01 | `neural_entrainment_intensity` (ITPC measure) | Ding et al. 2025 | ITPC η²=0.14 across 1-12 Hz; measures phase coherence of entrainment | Medium — currently captured indirectly via BEP mechanism |
| ASU-G02 | `phase_locking_value` (inter-region PLV) | Yang et al. 2025 | PLV=0.76 frontal-parietal at fast tempo; measures auditory-motor coupling | Low — connectivity metric, not spectral feature |

**Notes:**
- SNEM's current R³ input mapping (~15D from Energy, Change, Interactions) is well-supported by literature
- The ITPC and PLV measures are neural response metrics, not acoustic/spectral features — they are better modeled as output dimensions rather than R³ inputs
- No strong evidence for missing R³ INPUT dimensions for SNEM

### IACM (ASU-α2) — Inharmonicity-Attention Capture Model

| Gap ID | Proposed R³ Feature | Source Paper | Evidence | Priority |
|--------|---------------------|-------------|----------|----------|
| ASU-G03 | `high_gamma_power_stg` (70-150 Hz power in STG) | Foo et al. 2016 | Dissonant chords → enhanced high gamma, p<0.001, 91% electrodes in STG | Low — neural response metric, not acoustic feature |
| ASU-G04 | `inharmonicity_index` (explicit inharmonicity measure) | Basinski 2025 | ApproxEntropy harmonic=0.02 vs inharmonic=0.19; currently approximated from tonalness+spectral_flatness | Medium — current R³ lacks direct inharmonicity measure; proxy via R³[14] tonalness + R³[16] spectral_flatness |

**Notes:**
- IACM's R³ mapping (~14D from Consonance, Energy, Timbre, Change, Interactions) is adequate
- The most notable gap is the lack of a direct `inharmonicity_index` in R³ — currently approximated by combining tonalness and spectral_flatness, which is reasonable but not exact
- The high gamma power measure is a neural response, not an acoustic feature — belongs in C³ output space

### CSG (ASU-α3) — Consonance-Salience Gradient

| Gap ID | Proposed R³ Feature | Source Paper | Evidence | Priority |
|--------|---------------------|-------------|----------|----------|
| ASU-G05 | `consonance_gradient` (continuous consonance level) | Fishman et al., Bravo 2017 | Phase-locked activity graded by consonance-dissonance; d=5.16 for salience | Low — adequately represented by R³[4] sensory_pleasantness + R³[0] roughness |

**Notes:**
- CSG's R³ mapping (~16D) is well-supported
- The consonance gradient is adequately represented by existing R³ features (roughness, sethares, sensory_pleasantness)
- New brain regions identified: amygdala, vmPFC, ventral striatum — extend the salience network beyond ACC/AI
