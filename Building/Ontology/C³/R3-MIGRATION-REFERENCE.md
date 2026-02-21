# R³ Index Migration Reference (128D → 97D)

## Groups E (Interactions 24D) and I (Information 7D) are DISSOLVED.
## All other groups shift to close the gaps.

## Index Migration Rules

### Groups A,B,C,D [0:25) — NO CHANGE (shift = 0)
| New Index | Feature Name |
|-----------|-------------|
| 0 | roughness |
| 1 | sethares_dissonance |
| 2 | helmholtz_kang |
| 3 | stumpf_fusion |
| 4 | sensory_pleasantness |
| 5 | inharmonicity |
| 6 | harmonic_deviation |
| 7 | amplitude |
| 8 | velocity_A |
| 9 | acceleration_A |
| 10 | loudness |
| 11 | onset_strength |
| 12 | warmth |
| 13 | sharpness |
| 14 | tonalness |
| 15 | clarity |
| 16 | spectral_smoothness |
| 17 | spectral_autocorrelation |
| 18 | tristimulus1 |
| 19 | tristimulus2 |
| 20 | tristimulus3 |
| 21 | spectral_flux |
| 22 | distribution_entropy |
| 23 | distribution_flatness |
| 24 | distribution_concentration |

### Group E [25:49] — DISSOLVED → C³ input layer
These are cross-domain interaction products. Each model now computes them internally.
| Old Index | Old Feature Name | Migration |
|-----------|-----------------|-----------|
| 25 | amp_x_roughness | C³ input layer |
| 26 | amp_x_sethares | C³ input layer |
| 27 | amp_x_helmholtz | C³ input layer |
| 28 | amp_x_stumpf | C³ input layer |
| 29 | vel_x_roughness | C³ input layer |
| 30 | vel_x_sethares | C³ input layer |
| 31 | vel_x_helmholtz | C³ input layer |
| 32 | vel_x_stumpf | C³ input layer |
| 33 | flux_x_roughness | C³ input layer |
| 34 | flux_x_sethares | C³ input layer |
| 35 | flux_x_helmholtz | C³ input layer |
| 36 | flux_x_stumpf | C³ input layer |
| 37 | ent_x_roughness | C³ input layer |
| 38 | ent_x_sethares | C³ input layer |
| 39 | ent_x_helmholtz | C³ input layer |
| 40 | ent_x_stumpf | C³ input layer |
| 41 | rough_x_warmth | C³ input layer |
| 42 | rough_x_sharpness | C³ input layer |
| 43 | seth_x_warmth | C³ input layer |
| 44 | seth_x_sharpness | C³ input layer |
| 45 | helm_x_tonalness | C³ input layer |
| 46 | helm_x_clarity | C³ input layer |
| 47 | stumpf_x_smoothness | C³ input layer |
| 48 | stumpf_x_autocorr | C³ input layer |

### Group F [49:65] → [25:41] (shift = −24)
| Old Index | New Index | Feature Name |
|-----------|-----------|-------------|
| 49 | 25 | chroma_C |
| 50 | 26 | chroma_Db |
| 51 | 27 | chroma_D |
| 52 | 28 | chroma_Eb |
| 53 | 29 | chroma_E |
| 54 | 30 | chroma_F |
| 55 | 31 | chroma_Gb |
| 56 | 32 | chroma_G |
| 57 | 33 | chroma_Ab |
| 58 | 34 | chroma_A |
| 59 | 35 | chroma_Bb |
| 60 | 36 | chroma_B |
| 61 | 37 | pitch_height |
| 62 | 38 | pitch_class_entropy |
| 63 | 39 | pitch_salience |
| 64 | 40 | inharmonicity_index |

### Group G [65:75] → [41:51] (shift = −24)
| Old Index | New Index | Feature Name |
|-----------|-----------|-------------|
| 65 | 41 | tempo_estimate |
| 66 | 42 | beat_strength |
| 67 | 43 | pulse_clarity |
| 68 | 44 | syncopation_index |
| 69 | 45 | metricality_index |
| 70 | 46 | isochrony_nPVI |
| 71 | 47 | groove_index |
| 72 | 48 | event_density |
| 73 | 49 | tempo_stability |
| 74 | 50 | rhythmic_regularity |

### Group H [75:87] → [51:63] (shift = −24)
| Old Index | New Index | Feature Name |
|-----------|-----------|-------------|
| 75 | 51 | key_clarity |
| 76 | 52 | tonnetz_fifth_x |
| 77 | 53 | tonnetz_fifth_y |
| 78 | 54 | tonnetz_minor_x |
| 79 | 55 | tonnetz_minor_y |
| 80 | 56 | tonnetz_major_x |
| 81 | 57 | tonnetz_major_y |
| 82 | 58 | voice_leading_distance |
| 83 | 59 | harmonic_change |
| 84 | 60 | tonal_stability |
| 85 | 61 | diatonicity |
| 86 | 62 | syntactic_irregularity |

### Group I [87:94] → DISSOLVED
| Old Index | Old Feature Name | Migration |
|-----------|-----------------|-----------|
| 87 | melodic_entropy | C³ model internal (transition tracking) |
| 88 | harmonic_entropy | C³ model internal (harmonic expectation) |
| 89 | rhythmic_info_content | Removed (redundant with event_density [48]) |
| 90 | spectral_surprise | C³ model internal (prediction/surprise) |
| 91 | information_rate | H³ velocity morph of spectral_flux [21] |
| 92 | predictive_entropy | C³ model internal (prediction) |
| 93 | tonal_ambiguity | Removed (use 1 − key_clarity [51]) |

### Group J [94:114] → [63:83] (shift = −31)
| Old Index | New Index | Feature Name |
|-----------|-----------|-------------|
| 94 | 63 | mfcc_1 |
| 95 | 64 | mfcc_2 |
| 96 | 65 | mfcc_3 |
| 97 | 66 | mfcc_4 |
| 98 | 67 | mfcc_5 |
| 99 | 68 | mfcc_6 |
| 100 | 69 | mfcc_7 |
| 101 | 70 | mfcc_8 |
| 102 | 71 | mfcc_9 |
| 103 | 72 | mfcc_10 |
| 104 | 73 | mfcc_11 |
| 105 | 74 | mfcc_12 |
| 106 | 75 | mfcc_13 |
| 107 | 76 | spectral_contrast_1 |
| 108 | 77 | spectral_contrast_2 |
| 109 | 78 | spectral_contrast_3 |
| 110 | 79 | spectral_contrast_4 |
| 111 | 80 | spectral_contrast_5 |
| 112 | 81 | spectral_contrast_6 |
| 113 | 82 | spectral_contrast_7 |

### Group K [114:128] → [83:97] (shift = −31)
| Old Index | New Index | Feature Name |
|-----------|-----------|-------------|
| 114 | 83 | modulation_0_5Hz |
| 115 | 84 | modulation_1Hz |
| 116 | 85 | modulation_2Hz |
| 117 | 86 | modulation_4Hz |
| 118 | 87 | modulation_8Hz |
| 119 | 88 | modulation_16Hz |
| 120 | 89 | modulation_centroid |
| 121 | 90 | modulation_bandwidth |
| 122 | 91 | sharpness_zwicker |
| 123 | 92 | fluctuation_strength |
| 124 | 93 | loudness_a_weighted |
| 125 | 94 | alpha_ratio |
| 126 | 95 | hammarberg_index |
| 127 | 96 | spectral_slope_0_500 |

## Group Range Updates
| Group | Old Range | New Range |
|-------|-----------|-----------|
| A Consonance | [0:7] | [0:7] |
| B Energy | [7:12] | [7:12] |
| C Timbre | [12:21] | [12:21] |
| D Change | [21:25] | [21:25] |
| E Interactions | [25:49] | DISSOLVED |
| F Pitch/Chroma | [49:65] | [25:41] |
| G Rhythm/Groove | [65:75] | [41:51] |
| H Harmony/Tonality | [75:87] | [51:63] |
| I Information | [87:94] | DISSOLVED |
| J Timbre Extended | [94:114] | [63:83] |
| K Modulation/Psychoacoustic | [114:128] | [83:97] |

## H³ Horizon Durations (current frozen values)
| H# | Duration | Band |
|----|----------|------|
| H0 | 5.8ms | Micro |
| H1 | 11.6ms | Micro |
| H2 | 17.4ms | Micro |
| H3 | 23.2ms | Micro |
| H4 | 34.8ms | Micro |
| H5 | 46.4ms | Micro |
| H6 | 200ms | Micro |
| H7 | 250ms | Micro |
| H8 | 300ms | Meso |
| H9 | 350ms | Meso |
| H10 | 400ms | Meso |
| H11 | 450ms | Meso |
| H12 | 525ms | Meso |
| H13 | 600ms | Meso |
| H14 | 700ms | Meso |
| H15 | 800ms | Meso |
| H16 | 1s | Macro |
| H17 | 1.5s | Macro |
| H18 | 2s | Macro |
| H19 | 3s | Macro |
| H20 | 5s | Macro |
| H21 | 8s | Macro |
| H22 | 15s | Macro |
| H23 | 25s | Macro |
| H24 | 36s | Ultra |
| H25 | 60s | Ultra |
| H26 | 120s | Ultra |
| H27 | 200s | Ultra |
| H28 | 414s | Ultra |
| H29 | 600s | Ultra |
| H30 | 800s | Ultra |
| H31 | 981s | Ultra |

## H³ Theoretical Space
97 × 32 × 24 × 3 = 223,488 tuples (not 294,912)

## H³ Morphs (M0-M23) — NO CHANGE
M0=value, M1=mean, M2=std, M3=median, M4=max, M5=range,
M6=skewness, M7=kurtosis, M8=velocity, M9=velocity_mean,
M10=velocity_std, M11=acceleration, M12=acceleration_mean,
M13=acceleration_std, M14=periodicity, M15=smoothness,
M16=curvature, M17=shape_period, M18=trend, M19=stability,
M20=entropy, M21=zero_crossings, M22=peaks, M23=symmetry

## H³ Laws (L0-L2) — NO CHANGE
L0=memory (backward), L1=forward (prediction), L2=integration (bidirectional)
