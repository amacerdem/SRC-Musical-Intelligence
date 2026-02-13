from __future__ import annotations

from typing import Tuple

R3_DIM: int = 128

R3_FEATURE_NAMES: Tuple[str, ...] = (
    # Group A: Consonance [0:7] -- 7D
    "roughness",                     # 0
    "sethares_dissonance",           # 1
    "helmholtz_kang",                # 2
    "stumpf_fusion",                 # 3
    "sensory_pleasantness",          # 4
    "inharmonicity",                 # 5
    "harmonic_deviation",            # 6
    # Group B: Energy [7:12] -- 5D
    "amplitude",                     # 7
    "velocity_A",                    # 8
    "acceleration_A",                # 9
    "loudness",                      # 10
    "onset_strength",                # 11
    # Group C: Timbre [12:21] -- 9D
    "warmth",                        # 12
    "sharpness",                     # 13
    "tonalness",                     # 14
    "clarity",                       # 15
    "spectral_smoothness",           # 16
    "spectral_autocorrelation",      # 17
    "tristimulus1",                  # 18
    "tristimulus2",                  # 19
    "tristimulus3",                  # 20
    # Group D: Change [21:25] -- 4D
    "spectral_flux",                 # 21
    "distribution_entropy",          # 22
    "distribution_flatness",         # 23
    "distribution_concentration",    # 24
    # Group E: Interactions [25:49] -- 24D
    "x_l0l5_0",                      # 25
    "x_l0l5_1",                      # 26
    "x_l0l5_2",                      # 27
    "x_l0l5_3",                      # 28
    "x_l0l5_4",                      # 29
    "x_l0l5_5",                      # 30
    "x_l0l5_6",                      # 31
    "x_l0l5_7",                      # 32
    "x_l4l5_0",                      # 33
    "x_l4l5_1",                      # 34
    "x_l4l5_2",                      # 35
    "x_l4l5_3",                      # 36
    "x_l4l5_4",                      # 37
    "x_l4l5_5",                      # 38
    "x_l4l5_6",                      # 39
    "x_l4l5_7",                      # 40
    "x_l5l7_0",                      # 41
    "x_l5l7_1",                      # 42
    "x_l5l7_2",                      # 43
    "x_l5l7_3",                      # 44
    "x_l5l7_4",                      # 45
    "x_l5l7_5",                      # 46
    "x_l5l7_6",                      # 47
    "x_l5l7_7",                      # 48
    # Group F: Pitch & Chroma [49:65] -- 16D
    "chroma_C",                      # 49
    "chroma_Db",                     # 50
    "chroma_D",                      # 51
    "chroma_Eb",                     # 52
    "chroma_E",                      # 53
    "chroma_F",                      # 54
    "chroma_Gb",                     # 55
    "chroma_G",                      # 56
    "chroma_Ab",                     # 57
    "chroma_A",                      # 58
    "chroma_Bb",                     # 59
    "chroma_B",                      # 60
    "pitch_height",                  # 61
    "pitch_class_entropy",           # 62
    "pitch_salience",                # 63
    "inharmonicity_index",           # 64
    # Group G: Rhythm & Groove [65:75] -- 10D
    "tempo_estimate",                # 65
    "beat_strength",                 # 66
    "pulse_clarity",                 # 67
    "syncopation_index",             # 68
    "metricality_index",             # 69
    "isochrony_nPVI",                # 70
    "groove_index",                  # 71
    "event_density",                 # 72
    "tempo_stability",               # 73
    "rhythmic_regularity",           # 74
    # Group H: Harmony & Tonality [75:87] -- 12D
    "key_clarity",                   # 75
    "tonnetz_fifth_x",               # 76
    "tonnetz_fifth_y",               # 77
    "tonnetz_minor_x",               # 78
    "tonnetz_minor_y",               # 79
    "tonnetz_major_x",               # 80
    "tonnetz_major_y",               # 81
    "voice_leading_distance",        # 82
    "harmonic_change",               # 83
    "tonal_stability",               # 84
    "diatonicity",                   # 85
    "syntactic_irregularity",        # 86
    # Group I: Information & Surprise [87:94] -- 7D
    "melodic_entropy",               # 87
    "harmonic_entropy",              # 88
    "rhythmic_information_content",  # 89
    "spectral_surprise",             # 90
    "information_rate",              # 91
    "predictive_entropy",            # 92
    "tonal_ambiguity",               # 93
    # Group J: Timbre Extended [94:114] -- 20D
    "mfcc_1",                        # 94
    "mfcc_2",                        # 95
    "mfcc_3",                        # 96
    "mfcc_4",                        # 97
    "mfcc_5",                        # 98
    "mfcc_6",                        # 99
    "mfcc_7",                        # 100
    "mfcc_8",                        # 101
    "mfcc_9",                        # 102
    "mfcc_10",                       # 103
    "mfcc_11",                       # 104
    "mfcc_12",                       # 105
    "mfcc_13",                       # 106
    "spectral_contrast_1",           # 107
    "spectral_contrast_2",           # 108
    "spectral_contrast_3",           # 109
    "spectral_contrast_4",           # 110
    "spectral_contrast_5",           # 111
    "spectral_contrast_6",           # 112
    "spectral_contrast_7",           # 113
    # Group K: Modulation & Psychoacoustic [114:128] -- 14D
    "modulation_0_5Hz",              # 114
    "modulation_1Hz",                # 115
    "modulation_2Hz",                # 116
    "modulation_4Hz",                # 117
    "modulation_8Hz",                # 118
    "modulation_16Hz",               # 119
    "modulation_centroid",           # 120
    "modulation_bandwidth",          # 121
    "sharpness_zwicker",             # 122
    "fluctuation_strength",          # 123
    "loudness_a_weighted",           # 124
    "alpha_ratio",                   # 125
    "hammarberg_index",              # 126
    "spectral_slope_0_500",          # 127
)

assert len(R3_FEATURE_NAMES) == R3_DIM
assert len(set(R3_FEATURE_NAMES)) == R3_DIM
