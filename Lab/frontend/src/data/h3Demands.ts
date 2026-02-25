/**
 * H3 Temporal Demand Mapping — static data extracted from CoreBelief predict() methods.
 *
 * Each CoreBelief accesses 1-3 H3 tuples directly in predict() via h3_features.get(key).
 * This file maps belief index -> its H3 tuple references with metadata.
 */

export interface H3TupleMeta {
  r3Idx: number
  horizon: number
  morph: number
  law: number
  r3Name: string
  horizonLabel: string
  morphName: string
  lawName: 'memory' | 'forward' | 'integration'
  purpose: string
  weight: number | null
}

export interface BeliefH3Demands {
  predict: H3TupleMeta[]
  mechanismName: string
  mechanismDemandCount: number
}

const L0 = 'memory' as const
const L2 = 'integration' as const

function t(
  r3Idx: number, horizon: number, morph: number, law: 0 | 1 | 2,
  r3Name: string, horizonLabel: string, morphName: string,
  purpose: string, weight: number | null,
): H3TupleMeta {
  return {
    r3Idx, horizon, morph, law, r3Name, horizonLabel, morphName,
    lawName: law === 0 ? L0 : law === 1 ? 'forward' : L2,
    purpose, weight,
  }
}

/**
 * Maps belief index (0-130) to its H3 demands.
 * Only CoreBeliefs (36 total) have predict entries.
 */
export const BELIEF_H3_MAP: Record<number, BeliefH3Demands> = {
  // ═══════════════════════════════════════════════════
  // F1 — Sensory Processing
  // ═══════════════════════════════════════════════════
  4: {
    mechanismName: 'BCH', mechanismDemandCount: 48,
    predict: [
      t(0, 6, 18, 0, 'roughness', '200ms', 'trend', 'Roughness trend for consonance prediction', 0.05),
      t(0, 12, 1, 0, 'roughness', '525ms', 'mean', 'Roughness mean memory', 0.03),
    ],
  },
  8: {
    mechanismName: 'PSCL', mechanismDemandCount: 20,
    predict: [
      t(39, 6, 18, 0, 'pitch_salience', '200ms', 'trend', 'Pitch salience trend', 0.05),
      t(24, 6, 14, 0, 'concentration', '200ms', 'periodicity', 'Pitch concentration periodicity', 0.03),
    ],
  },
  10: {
    mechanismName: 'PCCR', mechanismDemandCount: 14,
    predict: [
      t(38, 6, 18, 0, 'PCE', '200ms', 'trend', 'Pitch class entropy trend', 0.05),
      t(14, 12, 14, 0, 'tonalness', '525ms', 'periodicity', 'Tonalness periodicity memory', 0.03),
    ],
  },
  11: {
    mechanismName: 'STAI', mechanismDemandCount: 12,
    predict: [
      t(4, 8, 18, 0, 'sensory_pleasantness', '500ms', 'trend', 'Pleasantness trend', 0.05),
      t(4, 8, 14, 0, 'sensory_pleasantness', '500ms', 'periodicity', 'Pleasantness periodicity', 0.03),
    ],
  },
  15: {
    mechanismName: 'MIAA', mechanismDemandCount: 11,
    predict: [
      t(14, 5, 1, 0, 'tonalness', '150ms', 'mean', 'Tonalness mean alpha-beta', 0.04),
      t(17, 8, 1, 0, 'spectral_auto', '500ms', 'mean', 'Spectral autocorrelation syllable mean', 0.03),
    ],
  },

  // ═══════════════════════════════════════════════════
  // F2 — Prediction
  // ═══════════════════════════════════════════════════
  20: {
    mechanismName: 'HTP', mechanismDemandCount: 18,
    predict: [
      t(13, 8, 18, 0, 'sharpness', '500ms', 'trend', 'Sharpness trend', 0.04),
      t(21, 3, 8, 0, 'spectral_flux', '100ms', 'velocity', 'Spectral flux velocity', 0.03),
    ],
  },
  21: {
    mechanismName: 'HTP', mechanismDemandCount: 18,
    predict: [
      t(60, 8, 18, 0, 'tonal_stability', '500ms', 'trend', 'Tonal stability trend', 0.05),
      t(11, 3, 14, 2, 'onset_strength', '100ms', 'periodicity', 'Onset periodicity bidirectional', 0.03),
    ],
  },
  25: {
    mechanismName: 'ICEM', mechanismDemandCount: 14,
    predict: [
      t(21, 8, 18, 0, 'spectral_flux', '500ms', 'trend', 'Spectral flux trend', 0.05),
      t(22, 3, 8, 0, 'distribution_entropy', '100ms', 'velocity', 'Entropy velocity', 0.03),
    ],
  },
  31: {
    mechanismName: 'SPH', mechanismDemandCount: 12,
    predict: [
      t(60, 8, 18, 0, 'tonal_stability', '500ms', 'trend', 'Tonal stability trend', 0.04),
      t(39, 4, 8, 0, 'pitch_salience', '125ms', 'velocity', 'Pitch salience velocity', 0.03),
    ],
  },

  // ═══════════════════════════════════════════════════
  // F3 — Attention
  // ═══════════════════════════════════════════════════
  34: {
    mechanismName: 'CSG', mechanismDemandCount: 18,
    predict: [
      t(0, 16, 18, 0, 'roughness', '1s', 'trend', 'Roughness trend 1s', 0.04),
      t(4, 3, 14, 2, 'sensory_pleasantness', '100ms', 'periodicity', 'Pleasantness periodicity', 0.03),
    ],
  },
  36: {
    mechanismName: 'IACM', mechanismDemandCount: 14,
    predict: [
      t(14, 16, 18, 0, 'tonalness', '1s', 'trend', 'Tonalness trend 1s', 0.04),
      t(16, 3, 14, 2, 'spectral_flatness', '100ms', 'periodicity', 'Spectral flatness periodicity', 0.03),
    ],
  },
  42: {
    mechanismName: 'SNEM', mechanismDemandCount: 14,
    predict: [
      t(10, 16, 18, 0, 'spectral_flux', '1s', 'trend', 'Spectral flux trend 1s', 0.04),
      t(10, 16, 14, 2, 'spectral_flux', '1s', 'periodicity', 'Spectral flux periodicity 1s', 0.05),
    ],
  },
  44: {
    mechanismName: 'SNEM', mechanismDemandCount: 14,
    predict: [
      t(25, 16, 18, 0, 'x_l0l5', '1s', 'trend', 'Cross-domain trend 1s', 0.04),
      t(25, 16, 14, 2, 'x_l0l5', '1s', 'periodicity', 'Cross-domain periodicity 1s', 0.05),
    ],
  },

  // ═══════════════════════════════════════════════════
  // F4 — Memory
  // ═══════════════════════════════════════════════════
  50: {
    mechanismName: 'MEAMN', mechanismDemandCount: 19,
    predict: [
      t(12, 20, 18, 0, 'warmth', '5s', 'trend', 'Warmth trend 5s', 0.03),
      t(14, 16, 14, 2, 'tonalness', '1s', 'periodicity', 'Tonalness periodicity 1s', 0.04),
    ],
  },
  51: {
    mechanismName: 'MEAMN', mechanismDemandCount: 19,
    predict: [
      t(0, 20, 18, 0, 'roughness', '5s', 'trend', 'Roughness trend 5s', 0.03),
      t(10, 20, 1, 0, 'loudness', '5s', 'mean', 'Loudness mean 5s', 0.04),
    ],
  },
  53: {
    mechanismName: 'MEAMN', mechanismDemandCount: 19,
    predict: [
      t(12, 20, 18, 0, 'warmth', '5s', 'trend', 'Warmth trend 5s', 0.03),
      t(12, 20, 1, 0, 'warmth', '5s', 'mean', 'Warmth mean 5s', 0.04),
    ],
  },
  59: {
    mechanismName: 'HCMC', mechanismDemandCount: 16,
    predict: [
      t(3, 20, 18, 0, 'stumpf_fusion', '5s', 'trend', 'Stumpf fusion trend 5s', 0.04),
      t(21, 16, 14, 2, 'spectral_flux', '1s', 'periodicity', 'Spectral flux periodicity 1s', 0.04),
    ],
  },

  // ═══════════════════════════════════════════════════
  // F5 — Emotion
  // ═══════════════════════════════════════════════════
  63: {
    mechanismName: 'AAC', mechanismDemandCount: 14,
    predict: [
      t(7, 16, 8, 0, 'amplitude', '1s', 'velocity', 'Amplitude velocity 1s', 0.05),
      t(11, 16, 14, 2, 'onset_strength', '1s', 'periodicity', 'Onset periodicity 1s', 0.04),
    ],
  },
  67: {
    mechanismName: 'VMM', mechanismDemandCount: 16,
    predict: [
      t(4, 20, 18, 0, 'sensory_pleasantness', '5s', 'trend', 'Pleasantness trend 5s', 0.04),
      t(14, 22, 14, 2, 'tonalness', '15s', 'periodicity', 'Tonalness periodicity 15s', 0.03),
    ],
  },
  68: {
    mechanismName: 'VMM', mechanismDemandCount: 16,
    predict: [
      t(0, 20, 18, 0, 'roughness', '5s', 'trend', 'Roughness trend 5s', 0.04),
      t(14, 22, 14, 2, 'tonalness', '15s', 'periodicity', 'Tonalness periodicity 15s', 0.03),
    ],
  },
  70: {
    mechanismName: 'NEMAC', mechanismDemandCount: 12,
    predict: [
      t(12, 20, 18, 0, 'warmth', '5s', 'trend', 'Warmth trend 5s', 0.03),
      t(14, 20, 14, 2, 'tonalness', '5s', 'periodicity', 'Tonalness periodicity 5s', 0.03),
    ],
  },

  // ═══════════════════════════════════════════════════
  // F6 — Reward
  // ═══════════════════════════════════════════════════
  81: {
    mechanismName: 'SRP', mechanismDemandCount: 31,
    predict: [
      t(7, 8, 18, 0, 'amplitude', '500ms', 'trend', 'Amplitude trend 500ms', 0.05),
    ],
  },
  83: {
    mechanismName: 'SRP', mechanismDemandCount: 31,
    predict: [
      t(7, 8, 18, 0, 'amplitude', '500ms', 'trend', 'Amplitude trend 500ms', 0.05),
    ],
  },
  84: {
    mechanismName: 'SRP', mechanismDemandCount: 31,
    predict: [
      t(21, 8, 18, 0, 'spectral_flux', '500ms', 'trend', 'Spectral flux trend 500ms', 0.05),
    ],
  },
  88: {
    mechanismName: 'SRP', mechanismDemandCount: 31,
    predict: [
      t(7, 8, 18, 0, 'amplitude', '500ms', 'trend', 'Amplitude trend 500ms', 0.05),
    ],
  },
  89: {
    mechanismName: 'SRP', mechanismDemandCount: 31,
    predict: [
      t(7, 8, 18, 0, 'amplitude', '500ms', 'trend', 'Amplitude trend 500ms', 0.05),
    ],
  },

  // ═══════════════════════════════════════════════════
  // F7 — Motor
  // ═══════════════════════════════════════════════════
  92: {
    mechanismName: 'HGSIC', mechanismDemandCount: 16,
    predict: [
      t(7, 16, 15, 0, 'velocity_A', '1s', 'smoothness', 'Amplitude smoothness 1s', 0.05),
      t(22, 11, 14, 2, 'energy', '525ms', 'periodicity', 'Energy periodicity 525ms', 0.03),
    ],
  },
  96: {
    mechanismName: 'PEOM', mechanismDemandCount: 15,
    predict: [
      t(25, 16, 14, 2, 'x_l0l5', '1s', 'periodicity', 'Cross-domain periodicity 1s', 0.05),
      t(25, 3, 14, 2, 'x_l0l5', '100ms', 'periodicity', 'Cross-domain periodicity fast', 0.03),
    ],
  },
  98: {
    mechanismName: 'PEOM', mechanismDemandCount: 15,
    predict: [
      t(10, 16, 14, 2, 'onset_strength', '1s', 'periodicity', 'Beat periodicity 1s', 0.05),
      t(11, 16, 14, 2, 'onset_strength', '1s', 'periodicity', 'Onset periodicity 1s', 0.03),
    ],
  },
  101: {
    mechanismName: 'HMCE', mechanismDemandCount: 17,
    predict: [
      t(60, 16, 18, 0, 'tonal_stability', '1s', 'trend', 'Tonal stability trend 1s', 0.05),
      t(60, 16, 1, 0, 'tonal_stability', '1s', 'mean', 'Tonal stability mean 1s', 0.03),
    ],
  },

  // ═══════════════════════════════════════════════════
  // F8 — Learning
  // ═══════════════════════════════════════════════════
  109: {
    mechanismName: 'SLEE', mechanismDemandCount: 10,
    predict: [
      t(0, 8, 18, 0, 'roughness', '500ms', 'trend', 'Roughness trend 500ms', 0.05),
      t(0, 12, 14, 0, 'roughness', '525ms', 'periodicity', 'Roughness periodicity 525ms', 0.03),
    ],
  },
  111: {
    mechanismName: 'TSCP', mechanismDemandCount: 10,
    predict: [
      t(0, 8, 18, 0, 'roughness', '500ms', 'trend', 'Roughness trend 500ms', 0.05),
      t(0, 12, 14, 0, 'roughness', '525ms', 'periodicity', 'Roughness periodicity 525ms', 0.03),
    ],
  },
  114: {
    mechanismName: 'ESME', mechanismDemandCount: 10,
    predict: [
      t(0, 8, 18, 0, 'roughness', '500ms', 'trend', 'Roughness trend 500ms', 0.05),
      t(0, 12, 14, 0, 'roughness', '525ms', 'periodicity', 'Roughness periodicity 525ms', 0.03),
    ],
  },
  119: {
    mechanismName: 'EDNR', mechanismDemandCount: 10,
    predict: [
      t(0, 8, 18, 0, 'roughness', '500ms', 'trend', 'Roughness trend 500ms', 0.05),
      t(0, 12, 14, 0, 'roughness', '525ms', 'periodicity', 'Roughness periodicity 525ms', 0.03),
    ],
  },

  // ═══════════════════════════════════════════════════
  // F9 — Social
  // ═══════════════════════════════════════════════════
  128: {
    mechanismName: 'NSCP', mechanismDemandCount: 8,
    predict: [
      t(0, 8, 18, 0, 'roughness', '500ms', 'trend', 'Roughness trend 500ms', 0.05),
      t(0, 12, 14, 0, 'roughness', '525ms', 'periodicity', 'Roughness periodicity 525ms', 0.03),
    ],
  },
  130: {
    mechanismName: 'DDSMI', mechanismDemandCount: 8,
    predict: [
      t(0, 8, 18, 0, 'roughness', '500ms', 'trend', 'Coordination trend 500ms', 0.05),
      t(0, 12, 14, 0, 'roughness', '525ms', 'periodicity', 'Coordination periodicity 525ms', 0.03),
    ],
  },
}

/** Law colors for visualization */
export const LAW_COLORS: Record<string, string> = {
  memory: '#10b981',
  forward: '#3b82f6',
  integration: '#a855f7',
}

/** Morph display names */
export const MORPH_NAMES: Record<number, string> = {
  0: 'value', 1: 'mean', 2: 'std', 8: 'velocity',
  14: 'periodicity', 15: 'smoothness', 18: 'trend',
}

/** Horizon band labels */
export const HORIZON_BANDS: Record<string, [number, number]> = {
  Micro: [0, 7],
  Meso: [8, 15],
  Macro: [16, 23],
  Ultra: [24, 31],
}

/** Mechanism → total H³ demand count (all mechanisms) */
export const MECHANISM_H3_COUNTS: Record<string, number> = {
  // F1 Sensory
  BCH: 48, PSCL: 20, PCCR: 14, STAI: 12, MIAA: 11, CSG: 18, MPG: 14, SDED: 12,
  // F2 Prediction
  HTP: 18, ICEM: 14, SPH: 12,
  // F3 Attention
  IACM: 14, AACM: 12, SNEM: 14,
  // F4 Memory
  MEAMN: 19, MMP: 16, HCMC: 16,
  // F5 Emotion
  AAC: 14, VMM: 16, NEMAC: 12,
  // F6 Reward
  SRP: 31, DAED: 18,
  // F7 Motor
  HGSIC: 16, PEOM: 15, HMCE: 17,
  // F8 Learning
  SLEE: 10, TSCP: 10, ESME: 10, EDNR: 10, ECT: 8,
  // F9 Social (belief units, no separate mechanism modules)
  NSCP: 8, SSRI: 6, DDSMI: 8,
}
