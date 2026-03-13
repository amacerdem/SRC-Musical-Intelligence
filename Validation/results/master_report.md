# MI Validation Suite — Master Report

**Generated:** 2026-03-05T18:50:13.650674+00:00
**Platform:** Linux-6.14.0-35-generic-x86_64-with-glibc2.39
**Python:** 3.12.3
**Host:** 7937aa29efb0

---

## Summary

| Metric | Value |
|--------|-------|
| Total tests | 34 |
| Passed | 34 |
| Failed | 0 |
| Skipped | 0 |
| Duration | 2.5s |

---

## Module Results

| Module | Status | Passed | Failed | Skipped | Duration |
|--------|--------|--------|--------|---------|----------|

---

## Validation Scorecard

| Module | Primary Metric | Value | Threshold | Status |
|--------|---------------|-------|-----------|--------|
| V1 Pharmacology | Levodopa Δ reward | +0.0698 | > 0 | PASS |
| V2 IDyOM | Mean Pearson r | 0.0674 | > 0 | PASS |
| V3 Krumhansl | Major profile r | 0.7159 | > 0.5 | PASS |
| V4 DEAM | Mean arousal r | 0.2409 | > 0 | PASS |
| V5 EEG | Full R² > env R² | -0.0037 > -0.0010 | Full > env | FAIL |
| V6 fMRI | Significant ROIs | 0/26 | ≥ 3 | FAIL |
| V7 RSA | Best Spearman ρ | 1.0000 | > 0 | PASS |

---

## Cross-Module Summary

Which MI components contribute to which validations:

| Component | V1 | V2 | V3 | V4 | V5 | V6 | V7 |
|-----------|----|----|----|----|----|----|----| 
| R³ (perceptual) | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| H³ (temporal) | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| C³ beliefs | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Neurochemicals | ✓ | — | — | ✓ | ✓ | ✓ | — |
| RAM (brain regions) | — | — | — | — | ✓ | ✓ | — |
| Ψ³ (psychology) | ✓ | — | — | ✓ | — | — | — |

---

## Figure Index


**v1_pharmacology/**
- `v1_arousal_valence.pdf`
- `v1_arousal_valence.png`
- `v1_effect_sizes.pdf`
- `v1_effect_sizes.png`
- `v1_ferreri_reward.pdf`
- `v1_ferreri_reward.png`
- `v1_neuro_timeseries.pdf`
- `v1_neuro_timeseries.png`
- `v1_neurochemical_state.pdf`
- `v1_neurochemical_state.png`
- `v1_reward_timeseries.pdf`
- `v1_reward_timeseries.png`

**v2_idyom/**
- `v2_forest_plot.pdf`
- `v2_forest_plot.png`
- `v2_pearson_vs_spearman.pdf`
- `v2_pearson_vs_spearman.png`
- `v2_r_distribution.pdf`
- `v2_r_distribution.png`
- `v2_r_vs_melody_length.pdf`
- `v2_r_vs_melody_length.png`
- `v2_volcano.pdf`
- `v2_volcano.png`

**v3_krumhansl/**
- `v3_residual_plot.pdf`
- `v3_residual_plot.png`
- `v3_scatter_major.pdf`
- `v3_scatter_major.png`
- `v3_scatter_minor.pdf`
- `v3_scatter_minor.png`
- `v3_tonal_profiles.pdf`
- `v3_tonal_profiles.png`

**v4_deam/**
- `v4_arousal_vs_valence_scatter.pdf`
- `v4_arousal_vs_valence_scatter.png`
- `v4_forest_arousal.pdf`
- `v4_forest_arousal.png`
- `v4_forest_valence.pdf`
- `v4_forest_valence.png`
- `v4_r_distribution_arousal.pdf`
- `v4_r_distribution_arousal.png`
- `v4_r_distribution_valence.pdf`
- `v4_r_distribution_valence.png`
- `v4_volcano.pdf`
- `v4_volcano.png`

**v5_eeg_encoding/**
- `v5_alpha_vs_r2.pdf`
- `v5_alpha_vs_r2.png`
- `v5_efficiency_scatter.pdf`
- `v5_efficiency_scatter.png`
- `v5_incremental_r2.pdf`
- `v5_incremental_r2.png`
- `v5_model_comparison_bar.pdf`
- `v5_model_comparison_bar.png`

**v6_fmri_encoding/**
- `v6_anatomical_group_bar.pdf`
- `v6_anatomical_group_bar.png`
- `v6_incremental_roi.pdf`
- `v6_incremental_roi.png`
- `v6_model_comparison_bar.pdf`
- `v6_model_comparison_bar.png`
- `v6_roi_r2_heatmap.pdf`
- `v6_roi_r2_heatmap.png`
- `v6_roi_scatter_r3_vs_full.pdf`
- `v6_roi_scatter_r3_vs_full.png`

**root/**
- `v6_roi_r2.pdf`
- `v6_roi_r2.png`

**v7_rsa/**
- `v7_mds_plot.pdf`
- `v7_mds_plot.png`
- `v7_model_comparison_bar.pdf`
- `v7_model_comparison_bar.png`
- `v7_rdm_acoustic_mfcc.pdf`
- `v7_rdm_acoustic_mfcc.png`
- `v7_rdm_correlation_matrix.pdf`
- `v7_rdm_correlation_matrix.png`
- `v7_rdm_mi_beliefs.pdf`
- `v7_rdm_mi_beliefs.png`
- `v7_rdm_mi_r3.pdf`
- `v7_rdm_mi_r3.png`
- `v7_rdm_spectral_mel.pdf`
- `v7_rdm_spectral_mel.png`

---

## Per-Module Summary Reports

### V1 Pharmacology

```
==============================================================================
V1 PHARMACOLOGICAL VALIDATION — COMPREHENSIVE REPORT
==============================================================================

─── Ferreri et al. 2019 (PNAS) — Dopamine & Musical Reward ───
    N=27, Design: within-subject, double-blind, placebo-controlled
    Stimulus: Bach Cello Suite (15s excerpt)

  Drug               Reward        DA          Δ     %Chg         Dir
  ---------------  --------  --------  ---------  -------  ----------
  Levodopa           0.5887    0.6095    +0.0698   +13.4%    increase
  Risperidone        0.4221    0.0123    -0.0969   -18.7%    decrease
  Placebo            0.5190    0.3595    +0.0000    +0.0%   unchanged

  Effect Sizes (Cohen's d — MI vs. Published):
    Levodopa         MI d = +3.034   Published d = +0.840   Δd = 2.194
    Risperidone      MI d = -4.760   Published d = -0.670   Δd = 4.090

  Reward Time-Series Statistics:
    Levodopa         mean=0.5887  sd=0.0242  min=0.5673  max=0.6468  T=2584 frames
    Risperidone      mean=0.4221  sd=0.0188  min=0.4054  max=0.4707  T=2584 frames
    Placebo          mean=0.5190  sd=0.0218  min=0.4999  max=0.5734  T=2584 frames

─── Mallik et al. 2017 (Neuropsychopharmacology) — Opioids & Emotion ───
    N=15, Design: within-subject, double-blind, placebo-controlled

  Drug              Emotion       OPI          Δ     %Chg         Dir
  ---------------  --------  --------  ---------  -------  ----------
  Naltrexone         0.4200    0.0500    -0.0132    -3.1%    decrease
  Placebo            0.4332    0.5000    +0.0000    +0.0%   unchanged

  Effect Sizes:
    Naltrexone       MI d = -0.033   Published d = -0.530

  Neurochemical Profile Under Naltrexone:
    DA=0.3595  NE=0.5617  OPI=0.0500  5HT=0.1889
    DA=0.3595  NE=0.5617  OPI=0.5000  5HT=0.1889  (Placebo)

─── Laeng et al. 2021 (Frontiers in Psychology) — Arousal/Valence ───
    N=30, Design: double-blind, placebo-controlled
    Key prediction: Naltrexone ↓ arousal but preserves valence

  Drug              Measure   Arousal   Valence     A-Δ%     V-Δ%
  ---------------  --------  --------  --------  -------  -------
  Naltrexone        arousal    0.4082    0.3286   -24.9%   -12.0%
  Naltrexone        valence    0.4082    0.3286   -24.9%   -12.0%
  Placebo           arousal    0.5432    0.3736    +0.0%    +0.0%

  Dissociation Test:
    Arousal reduced under naltrexone:  YES (Δ=-24.9%)
    Valence preserved under naltrexone: YES (Δ=-12.0%)
    Dissociation confirmed: YES

  Effect Sizes:
    Naltrexone      ( arousal)  Published d = -0.450
    Naltrexone      ( valence)  Published d = +0.050

─── Neurochemical Profile Summary (All Studies) ───

  Study                 Drug                  DA       NE      OPI      5HT
  --------------------  ---------------  -------  -------  -------  -------
  Ferreri 2019          Levodopa          0.6095   0.5617   0.5000   0.1889
  Ferreri 2019          Risperidone       0.0123   0.5617   0.5000   0.1889
  Ferreri 2019          Placebo           0.3595   0.5617   0.5000   0.1889
  Mallik 2017           Naltrexone        0.3595   0.5617   0.0500   0.1889
  Mallik 2017           Placebo           0.3595   0.5617   0.5000   0.1889
  Laeng 2021            Naltrexone        0.3595   0.5617   0.0500   0.1889
  Laeng 2021            Naltrexone        0.3595   0.5617   0.0500   0.1889
  Laeng 2021            Placebo           0.3595   0.5617   0.5000   0.1889

─── Directional Concordance ───

  Study            Drug              Measure    Expected    Observed  Match
  ---------------  ---------------  --------  ----------  ----------  -----
  Ferreri          Levodopa           reward    increase    increase      ✓
  Ferreri          Risperidone        reward    decrease    decrease      ✓
  Mallik           Naltrexone        emotion    decrease    decrease      ✓
  Laeng            Naltrexone        arousal    decrease    decrease      ✓
  Laeng            Naltrexone        valence   preserved    decrease      ✓

  Concordance: 5/5 (100%)

─── Effect Size Comparison (Cohen's d) ───

  Study            Drug                 MI d     Pub d     |Δd|  Interpretation
  ---------------  ---------------  --------  --------  -------  --------------
  Ferreri          Levodopa           +3.034    +0.840    2.194           large
  Ferreri          Risperidone        -4.760    -0.670    4.090           large
  Mallik           Naltrexone         -0.033    -0.530    0.497           small
  Laeng            Naltrexone         -4.660    -0.450    4.210           large

==============================================================================
```

### V2 IDyOM

```
==============================================================================
V2 IDyOM CONVERGENT VALIDITY — COMPREHENSIVE REPORT
==============================================================================

─── Aggregate Statistics ───

  Melodies analyzed:       50
  Total notes:             2542

  Pearson r:
    Mean:                  0.0674
    Median:                0.0679
    SD:                    0.1673
    Min:                   -0.3470
    Max:                   0.4502
    IQR:                   [-0.0361, 0.1793]

  Fisher-z Averaged r:     0.0932  95% CI [0.0534, 0.1328]

  Spearman ρ:
    Mean:                  0.0483
    Median:                0.0567
    SD:                    0.1733

  Significance:
    Uncorrected (p<.05):   8/50 (16.0%)
    FDR-corrected (q<.05): 2/50 (4.0%)

─── Effect Size Classification (|r|) ───

  Negligible (<0.1):  21
  Small (0.1–0.3):    25
  Medium (0.3–0.5):   4
  Large (≥0.5):       0

─── Melody-Length Analysis ───

  Correlation (n_notes vs r): r=0.261, p=6.752e-02
  Interpretation: No significant length effect

─── Per-Melody Details (All Melodies) ───

    #  Melody                                r        ρ           p       FDR-p      n     |r|
  ---  ------------------------------  -------  -------  ----------  ----------  -----  ------
    1  han0035                           0.450    0.495   3.556e-03   5.926e-02      40       M
    2  han0031                           0.408    0.376   2.272e-02   1.701e-01      31       M
    3  han0006                           0.308    0.287   1.426e-01   4.531e-01      24       M
    4  han0033                           0.296    0.234   6.388e-04   3.194e-02*    130       S
    5  usa03                             0.288    0.362   4.038e-02   2.524e-01      51       S
    6  mexico01                          0.280    0.207   2.381e-02   1.701e-01      65       S
    7  mexico03                          0.280    0.207   2.381e-02   1.701e-01      65       S
    8  arabic01                          0.267    0.135   1.758e-03   4.395e-02*    135       S
    9  han0004                           0.235    0.198   1.450e-01   4.531e-01      40       S
   10  usa02                             0.232    0.224   1.298e-01   4.531e-01      44       S
   11  han0008                           0.204    0.070   3.291e-01   8.130e-01      25       S
   12  mexico04                          0.181    0.158   1.333e-01   4.531e-01      70       S
   13  mexico02                          0.181    0.158   1.333e-01   4.531e-01      70       S
   14  han0009                           0.174    0.177   8.879e-02   4.531e-01      97       S
   15  han0019                           0.169    0.150   1.234e-01   4.531e-01      84       S
   16  han0003                           0.146    0.102   5.050e-01   9.189e-01      23       S
   17  han0013                           0.142    0.089   3.641e-01   8.130e-01      43       S
   18  han0020                           0.141    0.072   3.662e-01   8.130e-01      43       S
   19  usa04                             0.141    0.210   5.418e-01   9.189e-01      21       S
   20  canada01                          0.115   -0.091   5.234e-01   9.189e-01      33       S
   21  usa06                             0.109    0.015   3.740e-01   8.130e-01      69       S
   22  han0001                           0.080    0.088   5.324e-01   9.189e-01      63       ·
   23  usa05                             0.073    0.133   5.719e-01   9.189e-01      63       ·
   24  han0002                           0.071    0.013   6.047e-01   9.189e-01      56       ·
   25  han0015                           0.068    0.285   7.365e-01   9.442e-01      27       ·
   26  han0007                           0.068    0.124   6.774e-01   9.189e-01      40       ·
   27  han0025                           0.060   -0.012   5.961e-01   9.189e-01      81       ·
   28  han0028                           0.025    0.044   8.738e-01   9.947e-01      44       ·
   29  han0030                           0.023    0.162   8.753e-01   9.947e-01      50       ·
   30  han0026                           0.018   -0.137   8.649e-01   9.947e-01      89       ·
   31  han0027                           0.012   -0.039   9.204e-01   9.985e-01      71       ·
   32  han0034                           0.007   -0.065   9.612e-01   9.985e-01      47       ·
   33  han0024                          -0.000   -0.052   9.985e-01   9.985e-01      61       ·
   34  han0010                          -0.001   -0.113   9.978e-01   9.985e-01      22       ·
   35  han0005                          -0.004   -0.042   9.870e-01   9.985e-01      23       ·
   36  han0014                          -0.012    0.025   9.227e-01   9.985e-01      69       ·
   37  han0017                          -0.028   -0.194   8.654e-01   9.947e-01      38       ·
   38  han0022                          -0.039    0.087   8.229e-01   9.947e-01      36       ·
   39  han0011                          -0.066   -0.044   6.689e-01   9.189e-01      45       ·
   40  han0016                          -0.068   -0.072   6.800e-01   9.189e-01      39       ·
   41  han0032                          -0.081   -0.152   7.062e-01   9.292e-01      24       ·
   42  han0018                          -0.100   -0.130   6.063e-01   9.189e-01      29       ·
   43  han0036                          -0.103   -0.327   6.492e-01   9.189e-01      22       S
   44  han0023                          -0.130   -0.026   4.057e-01   8.453e-01      43       S
   45  brasil01                         -0.131   -0.159   6.285e-01   9.189e-01      16       S
   46  han0021                          -0.134   -0.077   2.184e-01   6.425e-01      86       S
   47  han0029                          -0.167   -0.051   2.919e-01   7.681e-01      42       S
   48  usa07                            -0.216   -0.214   2.521e-01   7.002e-01      30       S
   49  han0012                          -0.257   -0.260   1.359e-01   4.531e-01      35       S
   50  usa01                            -0.347   -0.216   1.569e-02   1.701e-01      48       M

==============================================================================
```

### V3 Krumhansl

```
==============================================================================
V3 TONAL HIERARCHY VALIDATION — COMPREHENSIVE REPORT
==============================================================================

─── Major Key Profile ───

  Pearson r:       0.7159   p = 8.83e-03   95% CI [0.2440, 0.9421]
  Spearman ρ:      0.7762   p = 2.99e-03   95% CI [0.2727, 0.9785]
  Kendall τ:       0.6364   p = 3.18e-03
  Permutation p:   0.0093   (10,000 permutations)
  Cohen's d (r→d): +2.051

─── Minor Key Profile ───

  Pearson r:       0.7158   p = 8.84e-03   95% CI [0.2927, 0.8926]
  Spearman ρ:      0.5664   p = 5.48e-02   95% CI [-0.0929, 0.8721]
  Kendall τ:       0.3939   p = 8.63e-02
  Permutation p:   0.0082   (10,000 permutations)
  Cohen's d (r→d): +2.050

─── Profile Details (Normalized) ───

    PC   K-K Maj    MI Maj     Resid   K-K Min    MI Min     Resid
  ────  ────────  ────────  ────────  ────────  ────────  ────────
     C    1.0000    1.0000   +0.0000    1.0000    0.9358   -0.0642
    C#    0.3512    0.4925   +0.1413    0.4234    0.4669   +0.0435
     D    0.5480    0.4326   -0.1154    0.5561    0.5507   -0.0054
    D#    0.3669    0.5590   +0.1920    0.8499    1.0000   +0.1501
     E    0.6898    0.9964   +0.3066    0.4107    0.6589   +0.2482
     F    0.6441    0.6732   +0.0291    0.5577    0.4334   -0.1242
    F#    0.3969    0.5592   +0.1624    0.4013    0.4782   +0.0769
     G    0.8173    0.9787   +0.1614    0.7504    0.9873   +0.2369
    G#    0.3764    0.5991   +0.2227    0.6288    0.6423   +0.0136
     A    0.5764    0.6316   +0.0552    0.4250    0.6300   +0.2050
    A#    0.3606    0.5976   +0.2370    0.5276    0.7901   +0.2624
     B    0.4535    0.9520   +0.4985    0.5008    0.8722   +0.3715

─── Residual Analysis ───

  Largest major-key deviations:
       B: +0.4985
       E: +0.3066
      A#: +0.2370
  Largest minor-key deviations:
       B: +0.3715
      A#: +0.2624
       E: +0.2482

  Major RMSE: 0.2189
  Minor RMSE: 0.1863
  Major MAE:  0.1768
  Minor MAE:  0.1502

─── Hierarchy Concordance ───

  ✓ Major: C > G (tonic > dominant): 0.4423 vs 0.4329
  ✗ Major: G > E (dominant > mediant): 0.4329 vs 0.4407
  ✓ Major: E > F (mediant > subdominant): 0.4407 vs 0.2978
  ✓ Major: C > F# (tonic > tritone): 0.4423 vs 0.2474
  ✗ Minor: C > G (tonic > dominant): 0.4031 vs 0.4252
  ✓ Minor: Eb > E (minor 3rd > major 3rd): 0.4307 vs 0.2838

  Hierarchy score: 4/6

==============================================================================
```

### V4 DEAM

```
==============================================================================
V4 DEAM CONTINUOUS EMOTION — COMPREHENSIVE REPORT
==============================================================================

  Songs analyzed: 10

─── Arousal ───

  Mean r:              0.2409
  Median r:            0.1577
  SD r:                0.2757
  Min / Max r:         -0.0541 / 0.8401
  IQR:                 [0.0193, 0.3896]
  Fisher-z mean:       0.2822  95% CI [0.2233, 0.3390]
  Uncorrected p<.05:   4/10 (40.0%)
  FDR-corrected q<.05: 3/10 (30.0%)

─── Valence ───

  Mean r:              -0.0480
  Median r:            -0.0269
  SD r:                0.2272
  Min / Max r:         -0.5625 / 0.2231
  IQR:                 [-0.1785, 0.1468]
  Fisher-z mean:       -0.0553  95% CI [-0.1177, 0.0076]
  Uncorrected p<.05:   1/10 (10.0%)
  FDR-corrected q<.05: 1/10 (10.0%)

─── Optimal Time-Lag Analysis (±5s) ───

  Arousal:  max r = 0.2390  (mean lag = -0.3s)
  Valence:  max r = 0.0606  (mean lag = -0.1s)
  Improvement over zero-lag:
    Arousal: -0.0019
    Valence: +0.1086

─── Arousal vs. Valence Comparison ───

  Mean Δ(r_arousal − r_valence): +0.2889
  Arousal > Valence: 8/10 songs
  Wilcoxon signed-rank: stat=8.0, p=4.883e-02
  Interpretation: Arousal predicted better

─── Effect Size Classification ───

  Arousal:
    Negligible   (0.0–0.1): 3
    Small        (0.1–0.3): 4
    Medium       (0.3–0.5): 1
    Large        (0.5–1.0): 2
  Valence:
    Negligible   (0.0–0.1): 2
    Small        (0.1–0.3): 7
    Medium       (0.3–0.5): 0
    Large        (0.5–1.0): 1

─── Per-Song Details ───

    #        Song      r_A      r_V         p_A       FDR_A         p_V       FDR_V  |r_A|
  ───  ──────────  ───────  ───────  ──────────  ──────────  ──────────  ──────────  ─────
    1        1008    0.840   -0.563   4.855e-17   4.855e-16*   2.899e-06   2.899e-05*      L
    2        1006    0.554   -0.204   4.352e-06   2.176e-05*   1.183e-01   2.956e-01      L
    3        1005    0.434    0.167   5.253e-04   1.751e-03*   2.014e-01   3.779e-01      M
    4        1004    0.255    0.158   4.898e-02   1.225e-01   2.267e-01   3.779e-01      S
    5        1007    0.164   -0.102   2.092e-01   4.157e-01   4.366e-01   5.457e-01      S
    6        1002    0.151    0.112   2.494e-01   4.157e-01   3.936e-01   5.457e-01      S
    7        1001    0.134   -0.083   3.081e-01   4.402e-01   5.265e-01   5.850e-01      S
    8          10   -0.019    0.223   8.862e-01   8.862e-01   8.659e-02   2.956e-01      ·
    9        1003   -0.051    0.030   6.981e-01   7.756e-01   8.228e-01   8.228e-01      ·
   10        1000   -0.054   -0.218   6.813e-01   7.756e-01   9.439e-02   2.956e-01      ·

==============================================================================
```

### V5 EEG Encoding

```
==============================================================================
V5 EEG ENCODING MODELS — COMPREHENSIVE REPORT
==============================================================================

─── Model Comparison ───

  Model                 Dim   Mean R²     Alpha   ΔR²(env)    %Impr       f²    R²/dim
  ──────────────────  ─────  ────────  ────────  ─────────  ───────  ───────  ────────
  envelope                1   -0.0010   10000.0    +0.0000    +0.0%  -0.0010  -0.000964
  spectrogram            16   -0.0098   10000.0    -0.0088    +0.0%  -0.0097  -0.000610
  r3                     97   -0.0033   10000.0    -0.0024    +0.0%  -0.0033  -0.000034
  beliefs               131   -0.0030   10000.0    -0.0021    +0.0%  -0.0030  -0.000023
  ram                    26   -0.0117   10000.0    -0.0108    +0.0%  -0.0116  -0.000451
  neuro                   4   -0.0017   10000.0    -0.0007    +0.0%  -0.0017  -0.000417
  full                  258   -0.0037   10000.0    -0.0027    +0.0%  -0.0037  -0.000014

─── Incremental R² Analysis ───

  Each feature set's unique contribution beyond envelope baseline:
    spectrogram         ΔR² = -0.0088  (negligible)
    r3                  ΔR² = -0.0024  (negligible)
    beliefs             ΔR² = -0.0021  (negligible)
    ram                 ΔR² = -0.0108  (negligible)
    neuro               ΔR² = -0.0007  (negligible)
    full                ΔR² = -0.0027  (negligible)

─── Hierarchical Layer Contribution ───

  Acoustic (envelope→R³):       ΔR² = -0.0024
  Cognitive (R³→beliefs):        ΔR² = +0.0003
  Full (all combined):           R²  = -0.0037


─── Effect Size (Cohen's f²) ───

  Benchmarks: small=0.02, medium=0.15, large=0.35
    envelope            f² = -0.0010  (small)
    spectrogram         f² = -0.0097  (small)
    r3                  f² = -0.0033  (small)
    beliefs             f² = -0.0030  (small)
    ram                 f² = -0.0116  (small)
    neuro               f² = -0.0017  (small)
    full                f² = -0.0037  (small)

─── Regularization Analysis ───

  Higher alpha → more regularization → less overfitting risk
    envelope            α = 10000.0  dim=1
    spectrogram         α = 10000.0  dim=16
    r3                  α = 10000.0  dim=97
    beliefs             α = 10000.0  dim=131
    ram                 α = 10000.0  dim=26
    neuro               α = 10000.0  dim=4
    full                α = 10000.0  dim=258

==============================================================================
```

### V6 fMRI Encoding

```
==============================================================================
V6 fMRI ROI ENCODING — COMPREHENSIVE REPORT
==============================================================================

─── Model Overview ───

  Model            Dim   Mean R²    Max R²   Sig ROIs    ΔR²(r3)
  ─────────────  ─────  ────────  ────────  ─────────  ─────────
  r3                97   -0.0774    0.0000     0/26    +0.0000
  beliefs          131   -0.0878    0.0024     2/26    -0.0103
  ram               26   -0.0708    0.0023     1/26    +0.0067
  neuro              4   -0.0431    0.0000     0/26    +0.0343
  full             258   -0.0766    0.0000     0/26    +0.0008

─── Anatomical Group Analysis ───

  Model            Cortical   Subcortical   Brainstem
  ─────────────  ──────────  ────────────  ──────────
  r3                -0.0632       -0.0585     -0.1455
  beliefs           -0.0841       -0.0743     -0.1207
  ram               -0.0764       -0.0655     -0.0666
  neuro             -0.0529       -0.0217     -0.0580
  full              -0.0691       -0.0592     -0.1258

─── Per-Region R² (All Models) ───

  Region                    r3   beliefs       ram     neuro      full
  ──────────────────  ────────  ────────  ────────  ────────  ────────
  A1_HG               -0.1398   -0.1265   -0.1937   -0.0953   -0.1561 
  STG                 -0.2427   -0.0692   -0.2384   -0.0278   -0.1853 
  STS                 -0.0186   -0.0010   -0.0011   -0.0012   -0.0537 
  IFG                 -0.0268   -0.1576   -0.0251   -0.0215   -0.0164 
  dlPFC               -0.2194   -0.4536   -0.3089   -0.3700   -0.2851 
  vmPFC               -0.0028   -0.0050   -0.0069   -0.0052   -0.0048 
  OFC                 -0.0456   -0.0655   -0.0346   -0.0216   -0.0518 
  ACC                 -0.0490   -0.0775   -0.0698   -0.0727   -0.0633 
  SMA                  0.0000    0.0000    0.0000    0.0000    0.0000 
  PMC                 -0.0024   -0.0027   -0.0028   -0.0029   -0.0023 
  AG                  -0.0012   -0.0010   -0.0011   -0.0011   -0.0011 
  TP                  -0.0102   -0.0499   -0.0351   -0.0160   -0.0097 
  VTA                 -0.1029   -0.1203   -0.0009   -0.0300   -0.1109 
  NAcc                -0.0396   -0.0357   -0.0985   -0.0429   -0.0494 
  caudate             -0.0255   -0.0940   -0.0971   -0.0058   -0.0278 
  amygdala            -0.0261   -0.0092   -0.0088   -0.0099   -0.0491 
  hippocampus         -0.0166    0.0024   -0.0761   -0.0017   -0.0057 
  putamen             -0.0010    0.0022    0.0023   -0.0004   -0.0002 
  MGB                 -0.2545   -0.3242   -0.1426   -0.0809   -0.2574 
  hypothalamus        -0.0532   -0.0299   -0.0731   -0.0050   -0.0211 
  insula              -0.0076   -0.0602   -0.0945   -0.0189   -0.0110 
  IC                  -0.3217   -0.2762   -0.1046   -0.0763   -0.2184 
  AN                  -0.1126   -0.1520   -0.1024   -0.1260   -0.1591 
  CN                  -0.0832   -0.0543   -0.0722   -0.0176   -0.0681 
  SOC                 -0.0200   -0.0105   -0.0101   -0.0116   -0.0109 
  PAG                 -0.1899   -0.1102   -0.0438   -0.0584   -0.1725 

─── Top-5 ROIs (Full Model) ───

  SMA                 R² = 0.0000
  putamen             R² = -0.0002
  AG                  R² = -0.0011
  PMC                 R² = -0.0023
  vmPFC               R² = -0.0048

─── Bottom-5 ROIs (Full Model) ───

  PAG                 R² = -0.1725
  STG                 R² = -0.1853
  IC                  R² = -0.2184
  MGB                 R² = -0.2574
  dlPFC               R² = -0.2851

─── Incremental R² per ROI (Full − R³) ───

  IC                  ΔR² = +0.1033  ↑
  STG                 ΔR² = +0.0574  ↑
  hypothalamus        ΔR² = +0.0321  ↑
  PAG                 ΔR² = +0.0173  ↑
  CN                  ΔR² = +0.0150  ↑
  hippocampus         ΔR² = +0.0109  ↑
  IFG                 ΔR² = +0.0104  ↑
  SOC                 ΔR² = +0.0091  ↑
  putamen             ΔR² = +0.0007  ─
  TP                  ΔR² = +0.0006  ─
  PMC                 ΔR² = +0.0001  ─
  AG                  ΔR² = +0.0001  ─
  SMA                 ΔR² = +0.0000  ─
  vmPFC               ΔR² = -0.0020  ↓
  caudate             ΔR² = -0.0023  ↓
  MGB                 ΔR² = -0.0029  ↓
  insula              ΔR² = -0.0034  ↓
  OFC                 ΔR² = -0.0062  ↓
  VTA                 ΔR² = -0.0080  ↓
  NAcc                ΔR² = -0.0098  ↓
  ACC                 ΔR² = -0.0143  ↓
  A1_HG               ΔR² = -0.0163  ↓
  amygdala            ΔR² = -0.0231  ↓
  STS                 ΔR² = -0.0350  ↓
  AN                  ΔR² = -0.0466  ↓
  dlPFC               ΔR² = -0.0657  ↓

==============================================================================
```

### V7 RSA

```
==============================================================================
V7 RSA — REPRESENTATIONAL SIMILARITY ANALYSIS — COMPREHENSIVE REPORT
==============================================================================

  Stimuli: 5
  Models compared: 4

─── Model Comparison ───

  Model                        ρ     p(perm)       FDR-p   Sig         d   |ρ| class
  ────────────────────  ────────  ──────────  ──────────  ────  ────────  ──────────
  mi_beliefs              1.0000      0.0000      0.0000     *      +inf       large
  mi_r3                   0.3697      0.2931      0.5861          +0.796      medium
  acoustic_mfcc           0.0182      0.9602      0.9602          +0.036       negl.
  spectral_mel           -0.1758      0.6272      0.8363          -0.357       small

  Best model: mi_beliefs (ρ = 1.0000, p = 0.0000)

─── Model Ranking ───

  1. mi_beliefs            ρ = 1.0000
  2. mi_r3                 ρ = 0.3697
  3. acoustic_mfcc         ρ = 0.0182
  4. spectral_mel          ρ = -0.1758

─── Inter-Model RDM Similarity (Spearman ρ) ───

                        mi_belie     mi_r3  acoustic  spectral
  mi_beliefs               1.000     0.370     0.018    -0.176
  mi_r3                    0.370     1.000     0.067    -0.212
  acoustic_mfcc            0.018     0.067     1.000     0.842
  spectral_mel            -0.176    -0.212     0.842     1.000

─── Stimuli ───

    1. Beethoven - Pathetique Sonata Op13 I. Grave - Allegro
    2. Cello Suite No. 1 in G Major, BWV 1007 I. Prélude
    3. Duel of the Fates - Epic Version
    4. Herald of the Change - Hans Zimmer
    5. Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato - Pyotr Ilyich Tchaikovsky

==============================================================================
```
