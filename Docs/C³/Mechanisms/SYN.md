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

### R3 Feature Inputs

| R3 Domain | Indices | Features | Consuming Units |
|-----------|---------|----------|-----------------|
| A: Consonance | [0]-[6] | stumpf_fusion, harmonicity, roughness, consonance_dissonance | IMU (MSPBA) |
| D: Change | [21]-[24] | spectral_flux, harmonic_change | IMU (MSPBA) |
| E: Interactions | [25]-[48] | Consonance-energy cross terms | IMU (MSPBA) |

SYN has the most focused R3 input of any mechanism. Domain A (Consonance) is the primary driver — musical syntax is fundamentally about chord-level harmonic relationships. Stumpf fusion and harmonicity measure consonance quality, while roughness captures dissonance tension. Domain D provides change detection for harmonic transitions (ERAN-triggering events). Domain E captures consonance-energy interactions that modulate syntactic processing strength.

### Per-Horizon Morph Profile

| Horizon | Morphs | Rationale |
|---------|--------|-----------|
| H12 (525 ms, 90 frames) | M0 (value), M1 (mean), M2 (std), M18 (trend) | Beat-level harmonic syntax — individual chord transitions (~250-700 ms per chord); trend captures local harmonic trajectory within chords |
| H16 (1 s, 172 frames) | M0 (value), M1 (mean), M2 (std), M18 (trend) | Phrase-level syntax — cadential progressions and tonal closure; trend measures phrase-level harmonic direction (tension → resolution) |
| H18 (2 s, 345 frames) | M0 (value), M1 (mean), M2 (std), M18 (trend) | Hierarchical grouping — how phrases group into periods; trend captures higher-order tonal relationships spanning multiple phrases |

All three horizons share the same compact 4-morph profile. Trend (M18) is the signature morph — it captures the directionality of harmonic movement that defines syntactic expectation (tension building vs resolution).

### Law Distribution

| Law | Units | Models | Rationale |
|-----|-------|:------:|-----------|
| L0 (Memory) | IMU | 1 | Accumulating harmonic context from past chords to assess syntactic coherence |
| L2 (Integration) | IMU | 1 | Bidirectional processing for hierarchical grouping — current chord evaluated against both preceding and following harmonic context |

MSPBA uses both L0 and L2. L0 (Memory) serves the causal aspect of syntax processing — each chord is evaluated in the context of what preceded it (harmonic expectation). L2 (Integration) serves the hierarchical grouping rules (GTTM) that require bidirectional evaluation.

### Demand Estimate

| Source Unit | Models | Est. Tuples |
|-------------|:------:|:-----------:|
| IMU (MSPBA) | 1 | ~30 |
| **Total** | **1** | **~30** |

SYN has the smallest demand footprint of any mechanism — a single model (MSPBA) in a single unit (IMU). This reflects the highly specialised nature of musical syntax processing, concentrated in the Broca's area homologue.

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
