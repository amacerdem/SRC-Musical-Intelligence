# SYN — Syntactic Processing

| Field | Value |
|-------|-------|
| NAME | SYN |
| FULL_NAME | Syntactic Processing |
| CIRCUIT | Mnemonic (memory consolidation & familiarity) |
| OUTPUT_DIM | 30 |
| HORIZONS | H12 (525 ms), H16 (1 s), H18 (2 s) |

## Description

Syntactic Processing models how the brain parses musical structure according to implicit grammatical rules — the "syntax" of music. Musical syntax encompasses harmonic progressions, phrase structure, voice-leading conventions, and hierarchical grouping rules that listeners internalise through exposure. Violations produce distinctive neural signatures (ERAN, P600) analogous to those in language processing. The primary neural substrate is the inferior frontal gyrus (IFG, Broca's area homologue), with interaction from posterior superior temporal gyrus (pSTG) for hierarchical structure building.

## 3x10D Sub-Section Structure

| Dims | Horizon | Computes |
|------|---------|----------|
| 0-9 | H12 (525 ms) | Beat-level harmonic syntax: chord-to-chord transitions and local harmonic violations. Individual chord timescale (~250-700 ms per chord). ERAN response to unexpected chords peaking at ~200 ms (Koelsch et al. 2000). |
| 10-19 | H16 (1 s) | Phrase-level syntax: phrase-level harmonic trajectories, cadential progressions, tonal closure, phrase-internal syntactic coherence. Detection of expected patterns (e.g., ii-V-I cadence). |
| 20-29 | H18 (2 s) | Hierarchical grouping: higher-order syntactic structure — how phrases group into periods, hierarchical tonal relationships spanning multiple phrases. GTTM grouping rules (Lerdahl & Jackendoff 1983). |

## H3 Demand

To be populated in Phase 6. Will declare demands for consonance group R3 features (stumpf_fusion, harmonicity, roughness) at H12/H16/H18 to measure harmonic transition surprise and syntactic coherence.

## Models Using This Mechanism

### IMU (Integrative Memory Unit)
- **MSPBA** — Musical Syntax Processing — Broca's Area

## Neuroscientific Basis

- Patel (2003): Shared Syntactic Integration Resource Hypothesis (SSIRH) — music and language share syntactic processing resources in IFG.
- Koelsch et al. (2000): ERAN response to unexpected chords, localised to IFG and anterior STG.
- Lerdahl & Jackendoff (1983): A Generative Theory of Tonal Music (GTTM) — hierarchical grouping and prolongational reduction.
- Maess et al. (2001): MEG evidence for early musical syntax processing in Broca's area (BA44/45).
- Tillmann et al. (2003): Musical structure processing activates bilateral network including IFG, STG, and premotor cortex.

## Code Reference

`mi_beta/brain/mechanisms/syn.py`
