from __future__ import annotations

from typing import Tuple

R3_DIM: int = 97

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
    # Group F: Pitch & Chroma [25:41] -- 16D
    "chroma_C",                      # 25
    "chroma_Db",                     # 26
    "chroma_D",                      # 27
    "chroma_Eb",                     # 28
    "chroma_E",                      # 29
    "chroma_F",                      # 30
    "chroma_Gb",                     # 31
    "chroma_G",                      # 32
    "chroma_Ab",                     # 33
    "chroma_A",                      # 34
    "chroma_Bb",                     # 35
    "chroma_B",                      # 36
    "pitch_height",                  # 37
    "pitch_class_entropy",           # 38
    "pitch_salience",                # 39
    "inharmonicity_index",           # 40
    # Group G: Rhythm & Groove [41:51] -- 10D
    "tempo_estimate",                # 41
    "beat_strength",                 # 42
    "pulse_clarity",                 # 43
    "syncopation_index",             # 44
    "metricality_index",             # 45
    "isochrony_nPVI",                # 46
    "groove_index",                  # 47
    "event_density",                 # 48
    "tempo_stability",               # 49
    "rhythmic_regularity",           # 50
    # Group H: Harmony & Tonality [51:63] -- 12D
    "key_clarity",                   # 51
    "tonnetz_fifth_x",               # 52
    "tonnetz_fifth_y",               # 53
    "tonnetz_minor_x",               # 54
    "tonnetz_minor_y",               # 55
    "tonnetz_major_x",               # 56
    "tonnetz_major_y",               # 57
    "voice_leading_distance",        # 58
    "harmonic_change",               # 59
    "tonal_stability",               # 60
    "diatonicity",                   # 61
    "syntactic_irregularity",        # 62
    # Group J: Timbre Extended [63:83] -- 20D
    "mfcc_1",                        # 63
    "mfcc_2",                        # 64
    "mfcc_3",                        # 65
    "mfcc_4",                        # 66
    "mfcc_5",                        # 67
    "mfcc_6",                        # 68
    "mfcc_7",                        # 69
    "mfcc_8",                        # 70
    "mfcc_9",                        # 71
    "mfcc_10",                       # 72
    "mfcc_11",                       # 73
    "mfcc_12",                       # 74
    "mfcc_13",                       # 75
    "spectral_contrast_1",           # 76
    "spectral_contrast_2",           # 77
    "spectral_contrast_3",           # 78
    "spectral_contrast_4",           # 79
    "spectral_contrast_5",           # 80
    "spectral_contrast_6",           # 81
    "spectral_contrast_7",           # 82
    # Group K: Modulation & Psychoacoustic [83:97] -- 14D
    "modulation_0_5Hz",              # 83
    "modulation_1Hz",                # 84
    "modulation_2Hz",                # 85
    "modulation_4Hz",                # 86
    "modulation_8Hz",                # 87
    "modulation_16Hz",               # 88
    "modulation_centroid",           # 89
    "modulation_bandwidth",          # 90
    "sharpness_zwicker",             # 91
    "fluctuation_strength",          # 92
    "loudness_a_weighted",           # 93
    "alpha_ratio",                   # 94
    "hammarberg_index",              # 95
    "spectral_slope_0_500",          # 96
)

assert len(R3_FEATURE_NAMES) == R3_DIM
assert len(set(R3_FEATURE_NAMES)) == R3_DIM
