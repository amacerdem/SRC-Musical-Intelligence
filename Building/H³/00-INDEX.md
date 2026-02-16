# H³ Architecture Research & Corrections

**Date**: 2026-02-16
**Context**: Deep analysis of H³ temporal morphology system against auditory
neuroscience, speech processing, and predictive coding literature.

---

## Documents

| Document | Contents |
|----------|----------|
| [H3-TRW-MAPPING.md](H3-TRW-MAPPING.md) | H³ horizon ↔ Temporal Receptive Window mapping with empirical corrections. Region-by-region validation against Norman-Haignere 2022 (intracranial), Lerner 2011 (fMRI scrambling), Giraud & Poeppel 2012 (oscillations). Corrected table, gap analysis, oscillatory correspondence. **16 references.** |
| [H3-TEMPORAL-LAWS.md](H3-TEMPORAL-LAWS.md) | L0/L1/L2 neuroscientific basis. Laminar cortical evidence (superficial→error, deep→prediction), oscillatory signatures (gamma→L0, beta→L1, theta→L2), hippocampal forward/reverse replay, Temporal Context Model asymmetry (~2:1 forward bias), feedforward vs. recurrent processing phases. **29 references.** |
| [H3-EMPF-LAYERS.md](H3-EMPF-LAYERS.md) | E/M/P/F layer validation. Friston's generalized coordinates, mPFC past/future cells (Howard 2024), Tarder-Stoll 2024 bidirectional hierarchical coding, temporal asymmetry (memory > prediction at every level), proposed sequential execution. **14 references.** |
| [H3-ARCHITECTURE-CRITIQUE.md](H3-ARCHITECTURE-CRITIQUE.md) | Five specific issues with proposed fixes: horizon mapping corrections, missing intermediate horizons (H5/H20/H22), flat-to-stratum execution migration, R³ re-reading elimination, phased layer computation. MI's novel contribution identified. **10 prioritized actions.** |
| [H3-MUSIC-CROSSREF.md](H3-MUSIC-CROSSREF.md) | **Music/sound/perception cross-reference.** Validates all 5 speech/language findings against music-specific evidence from Literature/c3 (34 papers) and web research (~25 additional). TRW hierarchy confirmed for music, E/M/P/F validated by IDyOM + dopamine dissociation, L0/L1/L2 confirmed by hippocampal replay + laminar architecture. Music-specific additions: motor coupling, hemispheric lateralization, beta predictive bounce, dual neurochemistry. **59 music-specific references.** |

---

## Key Findings

### Validated (H³ gets right) — Now confirmed for BOTH speech AND music
- H6 = 200ms is EXACT: domain-general boundary (Norman-Haignere 2022 used natural sounds incl. music)
- H24 = 36s matches paragraph/movement-level processing (Lerner 2011 + Janata 2009 MEAM)
- E/M/P/F at every level: supported by Tarder-Stoll 2024, Howard 2024, IDyOM LTM/STM, Salimpoor caudate/NAcc
- L0/L1/L2 maps to: laminar architecture + hippocampal replay + dopamine dissociation
- H³ is a novel synthesis: validated by Vuust et al. 2022 (no equivalent framework in music neuroscience)
- Time-yoked horizons validated: Norman-Haignere 2024 preprint shows ~5% deviation with tempo change

### Corrections Needed
- H3 = 23ms: A1 onset grain, not full TRW (~70ms). Add H5 ≈ 70ms
- H18 = 2s: Maps to anterior STS (phrase), NOT IFG (sentence ~8s)
- H24 = 36s: Maps to PCC/precuneus, NOT mPFC (mPFC = minutes)
- Gap H18→H24: Add H20 (~5s) and H22 (~15s) for IFG
- Hierarchy is continuous gradient, not discrete steps (except at 200ms)
- Memory > Prediction asymmetry: ~2:1 to 5:1 at every level

### Architectural Issues
- 47/96 models re-read same R³ consonance indices (should use upstream outputs)
- Flat execution ignores temporal hierarchy (should use stratum-based order)
- E/M/P/F computed simultaneously (should be sequential: E→M→P→F)
- No cross-model prediction error loop (fundamental to predictive coding)

---

## Total References

**~90 unique papers** cited across all documents:

### Speech/Language (59 papers, from first 4 documents)
- 6 intracranial EEG studies (Norman-Haignere, Regev, Nourski, Cusinato, Canolty, Foo)
- 8 fMRI studies (Lerner, Hasson, Yeshurun, Simony, Chien, Overath, Lawrence, Kok)
- 5 foundational theoretical papers (Rao & Ballard, Friston, Clark, Keller, Kiebel)
- 4 hippocampal replay studies (Diba, Pfeiffer, Ambrose, Olafsdottir)
- 3 oscillatory framework papers (Giraud & Poeppel, Poeppel, Lisman & Jensen)
- 2 temporal context model papers (Howard & Kahana, Polyn)
- 2 mPFC timing papers (Howard 2024, Tarder-Stoll 2024)

### Music/Sound/Perception (59 papers, from H3-MUSIC-CROSSREF.md)
- 12 consonance/dissonance studies (Fishman, Bidelman, Foo, Tabas, Crespo-Bojorque, Wagner, etc.)
- 8 prediction/expectation studies (Egermann/IDyOM, Cheung, Gold, Mencke, Chabin, Harding, etc.)
- 8 memory/reward studies (Salimpoor, Janata, Mohebi, Martínez-Molina, Putkinen, etc.)
- 6 temporal hierarchy studies (Potes/ECoG, Samiee, Bonetti, Ye, Saadatmehr, etc.)
- 5 timbre studies (Pantev, Halpern, Bellmann, Sturm, Alluri)
- 8 oscillatory/TRW studies (Fujioka, Doelling, Gnanateja, Norman-Haignere, Albouy, etc.)
- 12 additional (Koelsch, Patel, Vuust, Zatorre, Patterson, Billig, Asilador, etc.)

---

## Relationship to Other Building Documents

- **Building/README.md**: Build system for 96 C³ models — H³ findings affect
  model build specifications (h3_demand, brain_regions, compute structure)
- **Docs/C³/C3-ARCHITECTURE.md**: System architecture — stratum execution
  proposal would modify the 5-phase execution model
- **Musical_Intelligence/ear/h3/**: H³ implementation code — horizon additions
  and new execution order would require code changes
