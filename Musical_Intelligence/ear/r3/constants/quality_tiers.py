from __future__ import annotations

from enum import Enum
from typing import Dict


class QualityTier(Enum):
    P = "Proxy"
    A = "Approximate"
    S = "Standard"
    R = "Reference"


R3_QUALITY_TIERS: Dict[str, QualityTier] = {
    # Group A: Consonance [0:7] -- all Proxy
    "roughness":                    QualityTier.P,
    "sethares_dissonance":          QualityTier.P,
    "helmholtz_kang":               QualityTier.P,
    "stumpf_fusion":                QualityTier.P,
    "sensory_pleasantness":         QualityTier.P,
    "inharmonicity":                QualityTier.P,
    "harmonic_deviation":           QualityTier.P,
    # Group B: Energy [7:12]
    "amplitude":                    QualityTier.P,
    "velocity_A":                   QualityTier.A,
    "acceleration_A":               QualityTier.A,
    "loudness":                     QualityTier.P,
    "onset_strength":               QualityTier.S,
    # Group C: Timbre [12:21]
    "warmth":                       QualityTier.A,
    "sharpness":                    QualityTier.A,
    "tonalness":                    QualityTier.A,
    "clarity":                      QualityTier.A,
    "spectral_smoothness":          QualityTier.P,
    "spectral_autocorrelation":     QualityTier.P,
    "tristimulus1":                 QualityTier.A,
    "tristimulus2":                 QualityTier.A,
    "tristimulus3":                 QualityTier.A,
    # Group D: Change [21:25]
    "spectral_flux":                QualityTier.S,
    "distribution_entropy":         QualityTier.S,
    "distribution_flatness":        QualityTier.S,
    "distribution_concentration":   QualityTier.P,
    # Group E: Interactions [25:49] -- all Proxy
    "x_l0l5_0":                     QualityTier.P,
    "x_l0l5_1":                     QualityTier.P,
    "x_l0l5_2":                     QualityTier.P,
    "x_l0l5_3":                     QualityTier.P,
    "x_l0l5_4":                     QualityTier.P,
    "x_l0l5_5":                     QualityTier.P,
    "x_l0l5_6":                     QualityTier.P,
    "x_l0l5_7":                     QualityTier.P,
    "x_l4l5_0":                     QualityTier.P,
    "x_l4l5_1":                     QualityTier.P,
    "x_l4l5_2":                     QualityTier.P,
    "x_l4l5_3":                     QualityTier.P,
    "x_l4l5_4":                     QualityTier.P,
    "x_l4l5_5":                     QualityTier.P,
    "x_l4l5_6":                     QualityTier.P,
    "x_l4l5_7":                     QualityTier.P,
    "x_l5l7_0":                     QualityTier.P,
    "x_l5l7_1":                     QualityTier.P,
    "x_l5l7_2":                     QualityTier.P,
    "x_l5l7_3":                     QualityTier.P,
    "x_l5l7_4":                     QualityTier.P,
    "x_l5l7_5":                     QualityTier.P,
    "x_l5l7_6":                     QualityTier.P,
    "x_l5l7_7":                     QualityTier.P,
    # Group F: Pitch & Chroma [49:65]
    "chroma_C":                     QualityTier.A,
    "chroma_Db":                    QualityTier.A,
    "chroma_D":                     QualityTier.A,
    "chroma_Eb":                    QualityTier.A,
    "chroma_E":                     QualityTier.A,
    "chroma_F":                     QualityTier.A,
    "chroma_Gb":                    QualityTier.A,
    "chroma_G":                     QualityTier.A,
    "chroma_Ab":                    QualityTier.A,
    "chroma_A":                     QualityTier.A,
    "chroma_Bb":                    QualityTier.A,
    "chroma_B":                     QualityTier.A,
    "pitch_height":                 QualityTier.S,
    "pitch_class_entropy":          QualityTier.S,
    "pitch_salience":               QualityTier.A,
    "inharmonicity_index":          QualityTier.A,
    # Group G: Rhythm & Groove [65:75]
    "tempo_estimate":               QualityTier.A,
    "beat_strength":                QualityTier.A,
    "pulse_clarity":                QualityTier.A,
    "syncopation_index":            QualityTier.A,
    "metricality_index":            QualityTier.A,
    "isochrony_nPVI":               QualityTier.A,
    "groove_index":                 QualityTier.A,
    "event_density":                QualityTier.S,
    "tempo_stability":              QualityTier.A,
    "rhythmic_regularity":          QualityTier.A,
    # Group H: Harmony & Tonality [75:87]
    "key_clarity":                  QualityTier.A,
    "tonnetz_fifth_x":              QualityTier.S,
    "tonnetz_fifth_y":              QualityTier.S,
    "tonnetz_minor_x":              QualityTier.S,
    "tonnetz_minor_y":              QualityTier.S,
    "tonnetz_major_x":              QualityTier.S,
    "tonnetz_major_y":              QualityTier.S,
    "voice_leading_distance":       QualityTier.S,
    "harmonic_change":              QualityTier.S,
    "tonal_stability":              QualityTier.A,
    "diatonicity":                  QualityTier.A,
    "syntactic_irregularity":       QualityTier.A,
    # Group I: Information & Surprise [87:94]
    "melodic_entropy":              QualityTier.A,
    "harmonic_entropy":             QualityTier.A,
    "rhythmic_information_content": QualityTier.A,
    "spectral_surprise":            QualityTier.A,
    "information_rate":             QualityTier.S,
    "predictive_entropy":           QualityTier.A,
    "tonal_ambiguity":              QualityTier.A,
    # Group J: Timbre Extended [94:114]
    "mfcc_1":                       QualityTier.S,
    "mfcc_2":                       QualityTier.S,
    "mfcc_3":                       QualityTier.S,
    "mfcc_4":                       QualityTier.S,
    "mfcc_5":                       QualityTier.S,
    "mfcc_6":                       QualityTier.S,
    "mfcc_7":                       QualityTier.S,
    "mfcc_8":                       QualityTier.S,
    "mfcc_9":                       QualityTier.S,
    "mfcc_10":                      QualityTier.S,
    "mfcc_11":                      QualityTier.S,
    "mfcc_12":                      QualityTier.S,
    "mfcc_13":                      QualityTier.S,
    "spectral_contrast_1":          QualityTier.S,
    "spectral_contrast_2":          QualityTier.S,
    "spectral_contrast_3":          QualityTier.S,
    "spectral_contrast_4":          QualityTier.S,
    "spectral_contrast_5":          QualityTier.S,
    "spectral_contrast_6":          QualityTier.S,
    "spectral_contrast_7":          QualityTier.S,
    # Group K: Modulation & Psychoacoustic [114:128]
    "modulation_0_5Hz":             QualityTier.A,
    "modulation_1Hz":               QualityTier.A,
    "modulation_2Hz":               QualityTier.A,
    "modulation_4Hz":               QualityTier.A,
    "modulation_8Hz":               QualityTier.A,
    "modulation_16Hz":              QualityTier.A,
    "modulation_centroid":          QualityTier.S,
    "modulation_bandwidth":         QualityTier.S,
    "sharpness_zwicker":            QualityTier.R,
    "fluctuation_strength":         QualityTier.A,
    "loudness_a_weighted":          QualityTier.S,
    "alpha_ratio":                  QualityTier.S,
    "hammarberg_index":             QualityTier.S,
    "spectral_slope_0_500":         QualityTier.S,
}

assert len(R3_QUALITY_TIERS) == 128
_tier_counts = {t: sum(1 for v in R3_QUALITY_TIERS.values() if v is t) for t in QualityTier}
assert _tier_counts[QualityTier.P] == 36, f"P={_tier_counts[QualityTier.P]}"
assert _tier_counts[QualityTier.A] == 49, f"A={_tier_counts[QualityTier.A]}"
assert _tier_counts[QualityTier.S] == 42, f"S={_tier_counts[QualityTier.S]}"
assert _tier_counts[QualityTier.R] == 1, f"R={_tier_counts[QualityTier.R]}"
assert R3_QUALITY_TIERS["sharpness_zwicker"] is QualityTier.R
del _tier_counts
