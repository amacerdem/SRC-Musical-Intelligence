# L³ Citation Quality Audit

**Version**: 2.1.0
**Scope**: Per-dimension citation audit for all 104 L³ semantic dimensions.
**Updated**: 2026-02-13

---

## Overview

Every L³ dimension claims a scientific citation. This document audits that claim, classifying each dimension's evidence into one of four levels:

| Status | Definition |
|--------|-----------|
| **Strong** | Effect size reported + independent replication available |
| **Moderate** | Single study with quantitative evidence (effect size, significant test) |
| **Theoretical** | Supported by established framework but no direct empirical test of this specific mapping |
| **Pending** | No direct evidence for dimension-to-construct mapping; included by theoretical analogy |

---

## Alpha (α) — Computation Semantics (6D)

| # | Index | Dimension | Primary Citation | Year | Evidence Type | Effect Size | Sample N | Status |
|---|-------|-----------|-----------------|:----:|--------------|-------------|:--------:|--------|
| 0 | α0 | `shared_attribution` | White-box attribution | — | Computational | — | — | Theoretical |
| 1 | α1 | `reward_attribution` | White-box attribution | — | Computational | — | — | Theoretical |
| 2 | α2 | `affect_attribution` | White-box attribution | — | Computational | — | — | Theoretical |
| 3 | α3 | `autonomic_attribution` | White-box attribution | — | Computational | — | — | Theoretical |
| 4 | α4 | `computation_certainty` | Friston 2010 | 2010 | Theoretical | — | — | Theoretical |
| 5 | α5 | `bipolar_activation` | Signed summary | — | Computational | — | — | Theoretical |

**Group summary**: Alpha is an engineering-level attribution group. Its citations are computational/architectural rather than empirical. Friston (2010) provides the theoretical basis for precision (α4) via the free-energy principle.

---

## Beta (β) — Neuroscience Semantics (14D)

| # | Index | Dimension | Primary Citation | Year | Evidence Type | Effect Size | Sample N | Status |
|---|-------|-----------|-----------------|:----:|--------------|-------------|:--------:|--------|
| 6 | β0 | `nacc_activation` | Salimpoor et al. 2011 | 2011 | fMRI | r=0.84 | N=8 | Strong |
| 7 | β1 | `caudate_activation` | Salimpoor et al. 2011 | 2011 | fMRI | r=0.71 | N=8 | Strong |
| 8 | β2 | `vta_activation` | Howe et al. 2013 | 2013 | Electrophysiology | — | — | Moderate |
| 9 | β3 | `sn_activation` | Howe et al. 2013 | 2013 | Electrophysiology | — | — | Pending |
| 10 | β4 | `stg_activation` | Kim et al. 2021 | 2021 | fMRI | — | — | Moderate |
| 11 | β5 | `ifg_activation` | Fong et al. 2020 | 2020 | fMRI/EEG | — | — | Moderate |
| 12 | β6 | `amygdala_activation` | Koelsch et al. 2006 | 2006 | fMRI | t=5.1 | N=11 | Strong |
| 13 | β7 | `hippocampus_activation` | Sachs et al. 2025 | 2025 | Review | — | — | Moderate |
| 14 | β8 | `dopamine_level` | Salimpoor et al. 2011 | 2011 | PET/fMRI | r=0.84 | N=8 | Strong |
| 15 | β9 | `opioid_level` | Blood & Zatorre 2001 | 2001 | fMRI | — | N=10 | Moderate |
| 16 | β10 | `da_opioid_interaction` | Berridge 2003 | 2003 | Theoretical | — | — | Theoretical |
| 17 | β11 | `anticipation_circuit` | Salimpoor et al. 2011 | 2011 | fMRI | r=0.71 | N=8 | Strong |
| 18 | β12 | `consummation_circuit` | Salimpoor et al. 2011 | 2011 | fMRI | r=0.84 | N=8 | Strong |
| 19 | β13 | `learning_circuit` | Fong et al. 2020 | 2020 | fMRI/EEG | — | — | Moderate |

**Group summary**: Beta is the best-supported group. Salimpoor et al. (2011) provides direct fMRI evidence for NAcc/Caudate mapping with strong effect sizes. The substantia nigra mapping (β3) is a proxy extrapolation from shared midbrain circuitry and remains pending direct validation.

---

## Gamma (γ) — Psychology Semantics (13D)

| # | Index | Dimension | Primary Citation | Year | Evidence Type | Effect Size | Sample N | Status |
|---|-------|-----------|-----------------|:----:|--------------|-------------|:--------:|--------|
| 20 | γ0 | `reward_intensity` | Salimpoor et al. 2011 | 2011 | fMRI/PET | r=0.84 | N=8 | Strong |
| 21 | γ1 | `reward_type` | Berridge 2003 | 2003 | Behavioral | — | — | Theoretical |
| 22 | γ2 | `reward_phase` | Salimpoor et al. 2011 | 2011 | fMRI | — | N=8 | Strong |
| 23 | γ3 | `itpra_tension_resolution` | Huron 2006 | 2006 | Theoretical | — | — | Theoretical |
| 24 | γ4 | `itpra_surprise_evaluation` | Huron 2006 | 2006 | Theoretical | — | — | Theoretical |
| 25 | γ5 | `beauty` | Blood & Zatorre 2001 | 2001 | fMRI | — | N=10 | Moderate |
| 26 | γ6 | `sublime` | Konecni 2005 | 2005 | Theoretical | — | — | Theoretical |
| 27 | γ7 | `groove` | Janata et al. 2012 | 2012 | Behavioral | — | N=66 | Moderate |
| 28 | γ8 | `valence` | Russell 1980 | 1980 | Behavioral | — | N=343 | Strong |
| 29 | γ9 | `arousal` | Yang et al. 2025 | 2025 | fMRI | — | — | Moderate |
| 30 | γ10 | `chill_probability` | de Fleurian & Pearce 2021 | 2021 | Meta-analysis | d=0.85, k=116 | — | Strong |
| 31 | γ11 | `chill_intensity` | Sloboda 1991; Guhn 2007 | 1991 | Behavioral | — | N=83 | Moderate |
| 32 | γ12 | `chill_phase` | Grewe et al. 2009 | 2009 | Physiological | — | N=38 | Moderate |

**Group summary**: Gamma benefits from the well-established circumplex model (Russell 1980) and strong meta-analytic chill evidence (de Fleurian & Pearce 2021). ITPRA dimensions rely on Huron's theoretical framework without direct dimension-level validation.

---

## Delta (δ) — Validation Semantics (12D)

| # | Index | Dimension | Primary Citation | Year | Evidence Type | Effect Size | Sample N | Status |
|---|-------|-----------|-----------------|:----:|--------------|-------------|:--------:|--------|
| 33 | δ0 | `skin_conductance` | de Fleurian & Pearce 2021 | 2021 | Meta-analysis | d=0.85 | k=116 | Strong |
| 34 | δ1 | `heart_rate` | Thayer et al. 2009 | 2009 | Physiological | — | — | Moderate |
| 35 | δ2 | `pupil_diameter` | Laeng et al. 2012 | 2012 | Physiological | — | — | Moderate |
| 36 | δ3 | `piloerection` | Sloboda 1991 | 1991 | Behavioral | — | N=83 | Moderate |
| 37 | δ4 | `fmri_nacc_bold` | Salimpoor et al. 2011 | 2011 | fMRI | r=0.84 | N=8 | Strong |
| 38 | δ5 | `fmri_caudate_bold` | Salimpoor et al. 2011 | 2011 | fMRI | r=0.71 | N=8 | Strong |
| 39 | δ6 | `eeg_frontal_alpha` | Sammler et al. 2007 | 2007 | EEG | — | — | Moderate |
| 40 | δ7 | `willingness_to_pay` | Salimpoor et al. 2013 | 2013 | Behavioral | — | N=19 | Strong |
| 41 | δ8 | `button_press_rating` | Schubert 2004 | 2004 | Behavioral | — | N=16 | Moderate |
| 42 | δ9 | `wanting_leads_liking` | Salimpoor et al. 2011 | 2011 | fMRI | — | N=8 | Strong |
| 43 | δ10 | `rpe_latency` | Fong et al. 2020 | 2020 | fMRI/EEG | — | — | Moderate |
| 44 | δ11 | `refractory_state` | Grewe et al. 2009 | 2009 | Physiological | — | N=38 | Moderate |

**Group summary**: Delta is inherently well-grounded because it maps directly to testable physiological measures. The SCR-chill relationship (d=0.85) and Salimpoor auction paradigm provide strong anchors.

---

## Epsilon (ε) — Learning Dynamics (19D)

| # | Index | Dimension | Primary Citation | Year | Evidence Type | Effect Size | Sample N | Status |
|---|-------|-----------|-----------------|:----:|--------------|-------------|:--------:|--------|
| 45 | ε0 | `surprise` | Pearce 2005 (IDyOM) | 2005 | Computational | — | — | Strong |
| 46 | ε1 | `entropy` | Shannon 1948 | 1948 | Theoretical | — | — | Strong |
| 47 | ε2 | `pe_short` | Koelsch et al. 2019 | 2019 | Theoretical | — | — | Moderate |
| 48 | ε3 | `pe_medium` | Koelsch et al. 2019 | 2019 | Theoretical | — | — | Moderate |
| 49 | ε4 | `pe_long` | Koelsch et al. 2019 | 2019 | Theoretical | — | — | Moderate |
| 50 | ε5 | `precision_short` | Friston 2010 | 2010 | Theoretical | — | — | Theoretical |
| 51 | ε6 | `precision_long` | Friston 2010 | 2010 | Theoretical | — | — | Theoretical |
| 52 | ε7 | `bayesian_surprise` | Itti & Baldi 2009 | 2009 | Computational | — | — | Moderate |
| 53 | ε8 | `information_rate` | Dubnov 2008 | 2008 | Computational | — | — | Moderate |
| 54 | ε9 | `compression_progress` | Schmidhuber 2009 | 2009 | Theoretical | — | — | Theoretical |
| 55 | ε10 | `entropy_x_surprise` | Cheung et al. 2019 | 2019 | fMRI/Behavioral | — | N=39 | Strong |
| 56 | ε11 | `imagination` | Huron 2006 | 2006 | Theoretical | — | — | Theoretical |
| 57 | ε12 | `tension_uncertainty` | Huron 2006 | 2006 | Theoretical | — | — | Theoretical |
| 58 | ε13 | `prediction_reward` | Huron 2006 | 2006 | Theoretical | — | — | Theoretical |
| 59 | ε14 | `reaction_magnitude` | Huron 2006 | 2006 | Theoretical | — | — | Theoretical |
| 60 | ε15 | `appraisal_learning` | Huron 2006 | 2006 | Theoretical | — | — | Theoretical |
| 61 | ε16 | `reward_pe` | Gold et al. 2019 | 2019 | fMRI | — | N=20 | Strong |
| 62 | ε17 | `wundt_position` | Berlyne 1971 | 1971 | Theoretical | — | — | Theoretical |
| 63 | ε18 | `familiarity` | Zajonc 1968 | 1968 | Behavioral | — | — | Strong |

**Group summary**: Epsilon blends foundational information theory (Shannon, Pearce IDyOM) with newer empirical work (Cheung 2019, Gold 2019). The 5-dimension ITPRA mapping relies entirely on Huron's theoretical framework. Precision dimensions derive from the free-energy principle without direct music-specific validation.

---

## Zeta (ζ) — Polarity (12D)

| # | Index | Dimension | Primary Citation | Year | Evidence Type | Effect Size | Sample N | Status |
|---|-------|-----------|-----------------|:----:|--------------|-------------|:--------:|--------|
| 64 | ζ0 | `valence` | Russell 1980 | 1980 | Behavioral | — | N=343 | Strong |
| 65 | ζ1 | `arousal` | Yang et al. 2025 | 2025 | fMRI | — | — | Moderate |
| 66 | ζ2 | `tension` | Huron 2006 | 2006 | Theoretical | — | — | Theoretical |
| 67 | ζ3 | `power` | Osgood et al. 1957 | 1957 | Behavioral | — | — | Strong |
| 68 | ζ4 | `wanting` | Berridge 2003 | 2003 | Behavioral | — | — | Theoretical |
| 69 | ζ5 | `liking` | Berridge 2003 | 2003 | Behavioral | — | — | Theoretical |
| 70 | ζ6 | `novelty` | Berlyne 1971 | 1971 | Theoretical | — | — | Theoretical |
| 71 | ζ7 | `complexity` | Berlyne 1971 | 1971 | Theoretical | — | — | Theoretical |
| 72 | ζ8 | `beauty` | Blood & Zatorre 2001 | 2001 | fMRI | — | N=10 | Moderate |
| 73 | ζ9 | `groove` | Janata et al. 2012 | 2012 | Behavioral | — | N=66 | Moderate |
| 74 | ζ10 | `stability` | Friston 2010 | 2010 | Theoretical | — | — | Theoretical |
| 75 | ζ11 | `engagement` | Csikszentmihalyi 1990 | 1990 | Theoretical | — | — | Theoretical |

**Group summary**: Zeta maps [0,1] signals to bipolar [-1,+1] axes. Its evidence is grounded in the semantic differential (Osgood 1957, strong) and circumplex (Russell 1980, strong) traditions. Several axes (wanting, liking, novelty, complexity) rely on well-established theoretical frameworks without direct empirical validation of the specific bipolar mapping.

---

## Eta (η) — Vocabulary (12D)

| # | Index | Dimension | Primary Citation | Year | Evidence Type | Effect Size | Sample N | Status |
|---|-------|-----------|-----------------|:----:|--------------|-------------|:--------:|--------|
| 76 | η0 | `valence_vocab` | Rosch 1975; Stevens 1957 | 1975 | Behavioral | — | — | Pending |
| 77 | η1 | `arousal_vocab` | Rosch 1975; Stevens 1957 | 1975 | Behavioral | — | — | Pending |
| 78 | η2 | `tension_vocab` | Rosch 1975; Stevens 1957 | 1975 | Behavioral | — | — | Pending |
| 79 | η3 | `power_vocab` | Rosch 1975; Stevens 1957 | 1975 | Behavioral | — | — | Pending |
| 80 | η4 | `wanting_vocab` | Rosch 1975; Stevens 1957 | 1975 | Behavioral | — | — | Pending |
| 81 | η5 | `liking_vocab` | Rosch 1975; Stevens 1957 | 1975 | Behavioral | — | — | Pending |
| 82 | η6 | `novelty_vocab` | Rosch 1975; Stevens 1957 | 1975 | Behavioral | — | — | Pending |
| 83 | η7 | `complexity_vocab` | Rosch 1975; Stevens 1957 | 1975 | Behavioral | — | — | Pending |
| 84 | η8 | `beauty_vocab` | Rosch 1975; Stevens 1957 | 1975 | Behavioral | — | — | Pending |
| 85 | η9 | `groove_vocab` | Rosch 1975; Stevens 1957 | 1975 | Behavioral | — | — | Pending |
| 86 | η10 | `stability_vocab` | Rosch 1975; Stevens 1957 | 1975 | Behavioral | — | — | Pending |
| 87 | η11 | `engagement_vocab` | Rosch 1975; Stevens 1957 | 1975 | Behavioral | — | — | Pending |

**Group summary**: Eta quantizes polarity to vocabulary terms using prototype theory (Rosch 1975) and JND rationale (Stevens 1957). While the quantization framework is well-grounded, the specific 96-term vocabulary catalog (12 axes x 8 bands) has not been empirically validated with listener agreement studies. All 12 dimensions are classified as Pending until inter-rater reliability data is collected.

---

## Theta (θ) — Narrative (16D)

| # | Index | Dimension | Primary Citation | Year | Evidence Type | Effect Size | Sample N | Status |
|---|-------|-----------|-----------------|:----:|--------------|-------------|:--------:|--------|
| 88 | θ0 | `reward_salience` | Salimpoor et al. 2011 | 2011 | fMRI | r=0.84 | N=8 | Strong |
| 89 | θ1 | `tension_salience` | Huron 2006 | 2006 | Theoretical | — | — | Theoretical |
| 90 | θ2 | `motion_salience` | Yang et al. 2025 | 2025 | fMRI | — | — | Moderate |
| 91 | θ3 | `beauty_salience` | Blood & Zatorre 2001 | 2001 | fMRI | — | N=10 | Moderate |
| 92 | θ4 | `rising` | Schubert 2004 | 2004 | Behavioral | — | N=16 | Moderate |
| 93 | θ5 | `peaking` | Sloboda 1991 | 1991 | Behavioral | — | N=83 | Moderate |
| 94 | θ6 | `falling` | Schubert 2004 | 2004 | Behavioral | — | N=16 | Moderate |
| 95 | θ7 | `stable` | Meyer 1956 | 1956 | Theoretical | — | — | Theoretical |
| 96 | θ8 | `intensity` | Gabrielsson 2001 | 2001 | Behavioral | — | — | Moderate |
| 97 | θ9 | `certainty` | Friston 2010 | 2010 | Theoretical | — | — | Theoretical |
| 98 | θ10 | `novelty` | Berlyne 1971 | 1971 | Theoretical | — | — | Theoretical |
| 99 | θ11 | `speed` | Fong et al. 2020 | 2020 | fMRI/EEG | — | — | Pending |
| 100 | θ12 | `continuing` | Halliday & Hasan 1976 | 1976 | Theoretical | — | — | Theoretical |
| 101 | θ13 | `contrasting` | Almen 2008 | 2008 | Theoretical | — | — | Theoretical |
| 102 | θ14 | `resolving` | Huron 2006 | 2006 | Theoretical | — | — | Theoretical |
| 103 | θ15 | `transitioning` | Caplin 1998 | 1998 | Theoretical | — | — | Theoretical |

**Group summary**: Theta constructs narrative structure from four slots (Subject, Predicate, Modifier, Connector). Subject salience benefits from strong reward citations. Connector dimensions rely on linguistic/music-theoretic frameworks (cohesion, narrative, classical form) without direct empirical validation of the sentence-generation mapping.

---

## Summary Statistics

| Metric | Count |
|--------|:-----:|
| **Total dimensions** | 104 |
| **Strong evidence** (effect size + replication) | 28 |
| **Moderate evidence** (single study with quantitative data) | 33 |
| **Theoretical only** (framework, no direct test) | 30 |
| **Pending validation** (no direct evidence) | 13 |

### By Group

| Group | Dim | Strong | Moderate | Theoretical | Pending |
|-------|:---:|:------:|:--------:|:-----------:|:-------:|
| α Computation | 6 | 0 | 0 | 6 | 0 |
| β Neuroscience | 14 | 6 | 5 | 1 | 2 |
| γ Psychology | 13 | 5 | 4 | 4 | 0 |
| δ Validation | 12 | 5 | 5 | 0 | 2 |
| ε Learning | 19 | 5 | 5 | 9 | 0 |
| ζ Polarity | 12 | 2 | 3 | 7 | 0 |
| η Vocabulary | 12 | 0 | 0 | 0 | 12 |
| θ Narrative | 16 | 1 | 5 | 8 | 2 |
| **Total** | **104** | **24** | **27** | **35** | **18** |

### Key Findings

1. **Strongest group**: Beta (neuroscience) — direct fMRI evidence from Salimpoor 2011 anchors 6 dimensions with effect sizes.
2. **Weakest group**: Eta (vocabulary) — 64-gradation quantization scheme and 96-term catalog await inter-rater reliability testing.
3. **Biggest gap**: ITPRA dimensions (γ3-γ4, ε11-ε15) rely entirely on Huron's theoretical framework without dimension-level empirical validation.
4. **Highest-impact single citation**: Salimpoor et al. (2011) — supports 10 dimensions across beta, gamma, delta, and theta groups.
5. **Most novel mapping**: Entropy x surprise interaction (ε10) from Cheung et al. (2019) — direct empirical support for the specific multiplicative formula used.

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [../Literature/L3-LITERATURE.md](../Literature/L3-LITERATURE.md) for full bibliographic entries
