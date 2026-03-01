/** R³ group and dimension definitions — authoritative source: Musical_Intelligence/ear/r3/constants */

export interface R3DimDef {
  index: number
  name: string
  group: string
}

export interface R3GroupDef {
  id: string
  name: string
  start: number
  end: number
  dim: number
  stage: 1 | 2
  color: string
  domain: string
  deps?: string
  features: string[]
}

/** All 97 feature names in index order — from feature_names.py */
export const R3_FEATURE_NAMES: string[] = [
  // Group A: Consonance [0:7]
  'roughness', 'sethares_dissonance', 'helmholtz_kang', 'stumpf_fusion',
  'sensory_pleasantness', 'inharmonicity', 'harmonic_deviation',
  // Group B: Energy [7:12]
  'amplitude', 'velocity_A', 'acceleration_A', 'loudness', 'onset_strength',
  // Group C: Timbre [12:21]
  'warmth', 'sharpness', 'tonalness', 'clarity', 'spectral_smoothness',
  'spectral_autocorrelation', 'tristimulus1', 'tristimulus2', 'tristimulus3',
  // Group D: Change [21:25]
  'spectral_flux', 'distribution_entropy', 'distribution_flatness', 'distribution_concentration',
  // Group F: Pitch & Chroma [25:41]
  'chroma_C', 'chroma_Db', 'chroma_D', 'chroma_Eb', 'chroma_E', 'chroma_F',
  'chroma_Gb', 'chroma_G', 'chroma_Ab', 'chroma_A', 'chroma_Bb', 'chroma_B',
  'pitch_height', 'pitch_class_entropy', 'pitch_salience', 'inharmonicity_index',
  // Group G: Rhythm & Groove [41:51]
  'tempo_estimate', 'beat_strength', 'pulse_clarity', 'syncopation_index',
  'metricality_index', 'isochrony_nPVI', 'groove_index', 'event_density',
  'tempo_stability', 'rhythmic_regularity',
  // Group H: Harmony & Tonality [51:63]
  'key_clarity', 'tonnetz_fifth_x', 'tonnetz_fifth_y', 'tonnetz_minor_x',
  'tonnetz_minor_y', 'tonnetz_major_x', 'tonnetz_major_y',
  'voice_leading_distance', 'harmonic_change', 'tonal_stability',
  'diatonicity', 'syntactic_irregularity',
  // Group J: Timbre Extended [63:83]
  'mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5', 'mfcc_6', 'mfcc_7',
  'mfcc_8', 'mfcc_9', 'mfcc_10', 'mfcc_11', 'mfcc_12', 'mfcc_13',
  'spectral_contrast_1', 'spectral_contrast_2', 'spectral_contrast_3',
  'spectral_contrast_4', 'spectral_contrast_5', 'spectral_contrast_6', 'spectral_contrast_7',
  // Group K: Modulation & Psychoacoustic [83:97]
  'modulation_0_5Hz', 'modulation_1Hz', 'modulation_2Hz', 'modulation_4Hz',
  'modulation_8Hz', 'modulation_16Hz', 'modulation_centroid', 'modulation_bandwidth',
  'sharpness_zwicker', 'fluctuation_strength', 'loudness_a_weighted',
  'alpha_ratio', 'hammarberg_index', 'spectral_slope_0_500',
]

export const R3_GROUPS: R3GroupDef[] = [
  {
    id: 'A', name: 'Consonance', start: 0, end: 7, dim: 7, stage: 1, color: '#f97316',
    domain: 'Psychoacoustic',
    features: R3_FEATURE_NAMES.slice(0, 7),
  },
  {
    id: 'B', name: 'Energy', start: 7, end: 12, dim: 5, stage: 1, color: '#ef4444',
    domain: 'Spectral',
    features: R3_FEATURE_NAMES.slice(7, 12),
  },
  {
    id: 'C', name: 'Timbre', start: 12, end: 21, dim: 9, stage: 1, color: '#8b5cf6',
    domain: 'Spectral',
    features: R3_FEATURE_NAMES.slice(12, 21),
  },
  {
    id: 'D', name: 'Change', start: 21, end: 25, dim: 4, stage: 1, color: '#22c55e',
    domain: 'Temporal',
    features: R3_FEATURE_NAMES.slice(21, 25),
  },
  {
    id: 'F', name: 'Pitch & Chroma', start: 25, end: 41, dim: 16, stage: 1, color: '#3b82f6',
    domain: 'Tonal',
    features: R3_FEATURE_NAMES.slice(25, 41),
  },
  {
    id: 'G', name: 'Rhythm & Groove', start: 41, end: 51, dim: 10, stage: 2, color: '#f59e0b',
    domain: 'Temporal', deps: 'energy',
    features: R3_FEATURE_NAMES.slice(41, 51),
  },
  {
    id: 'H', name: 'Harmony & Tonality', start: 51, end: 63, dim: 12, stage: 2, color: '#ec4899',
    domain: 'Tonal', deps: 'pitch_chroma',
    features: R3_FEATURE_NAMES.slice(51, 63),
  },
  {
    id: 'J', name: 'Timbre Extended', start: 63, end: 83, dim: 20, stage: 1, color: '#06b6d4',
    domain: 'Spectral',
    features: R3_FEATURE_NAMES.slice(63, 83),
  },
  {
    id: 'K', name: 'Modulation & Psychoacoustic', start: 83, end: 97, dim: 14, stage: 1, color: '#a855f7',
    domain: 'Psychoacoustic',
    features: R3_FEATURE_NAMES.slice(83, 97),
  },
]

/** Flat dimension list with group assignment */
export const R3_DIMS: R3DimDef[] = R3_GROUPS.flatMap((g) =>
  g.features.map((name, i) => ({
    index: g.start + i,
    name,
    group: g.id,
  })),
)
