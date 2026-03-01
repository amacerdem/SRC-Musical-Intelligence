/** 42-Dimension Registry — 6D Psychology + 12D Cognition + 24D Neuroscience
 *
 * Source: Musical_Intelligence/brain/dimensions/tree.py
 * Each tier is independently computed from beliefs only.
 */

export type DimLayer = 'psychology' | 'cognition' | 'neuroscience'

export interface DimensionDef {
  index: number
  key: string
  name: string
  nameTr: string
  layer: DimLayer
  parentKey?: string
  description: string
  beliefIndices: number[]
}

// ── 6D Psychology ────────────────────────────────────────────────────────────

export const PSYCHOLOGY_DIMS: DimensionDef[] = [
  { index: 0, key: 'energy', name: 'Energy', nameTr: 'Enerji', layer: 'psychology',
    description: 'Is this loud/intense or quiet/gentle?', beliefIndices: [16, 34, 35, 63] },
  { index: 1, key: 'valence', name: 'Valence', nameTr: 'Duygu Tonu', layer: 'psychology',
    description: 'Does this sound happy or sad?', beliefIndices: [4, 67, 68, 81, 89] },
  { index: 2, key: 'tempo', name: 'Tempo', nameTr: 'Hız', layer: 'psychology',
    description: 'Is this fast or slow?', beliefIndices: [42, 95, 98] },
  { index: 3, key: 'tension', name: 'Tension', nameTr: 'Gerilim', layer: 'psychology',
    description: 'Do I feel strain or release?', beliefIndices: [34, 60, 63, 80, 88] },
  { index: 4, key: 'groove', name: 'Groove', nameTr: 'Hareket', layer: 'psychology',
    description: 'Do I want to move my body?', beliefIndices: [42, 90, 92, 95, 99] },
  { index: 5, key: 'complexity', name: 'Density', nameTr: 'Yoğunluk', layer: 'psychology',
    description: 'How much stuff is going on?', beliefIndices: [16, 35, 36, 101] },
]

// ── 12D Cognition ────────────────────────────────────────────────────────────

export const COGNITION_DIMS: DimensionDef[] = [
  { index: 0, key: 'melodic_hook', name: 'Melody', nameTr: 'Melodi', layer: 'cognition',
    description: 'Is the melody catchy/memorable?', beliefIndices: [8, 10, 13, 47, 48] },
  { index: 1, key: 'harmonic_depth', name: 'Harmony', nameTr: 'Armoni', layer: 'cognition',
    description: 'Simple chords or rich/complex?', beliefIndices: [4, 5, 6, 21, 80] },
  { index: 2, key: 'rhythmic_drive', name: 'Rhythm', nameTr: 'Ritim', layer: 'cognition',
    description: 'Basic beat or layered/syncopated?', beliefIndices: [42, 44, 90, 92, 94] },
  { index: 3, key: 'timbral_color', name: 'Timbre', nameTr: 'Tını', layer: 'cognition',
    description: 'Warm/organic or cold/electronic?', beliefIndices: [11, 13, 15, 16, 111] },
  { index: 4, key: 'emotional_arc', name: 'Emotion', nameTr: 'Duygu', layer: 'cognition',
    description: 'Which specific emotion? Joy? Awe? Nostalgia?', beliefIndices: [63, 64, 67, 68, 70] },
  { index: 5, key: 'surprise', name: 'Surprise', nameTr: 'Sürpriz', layer: 'cognition',
    description: 'Did something unexpected happen?', beliefIndices: [21, 25, 75, 84] },
  { index: 6, key: 'momentum', name: 'Momentum', nameTr: 'İvme', layer: 'cognition',
    description: 'Building to somewhere or going in circles?', beliefIndices: [78, 79, 82, 88, 89] },
  { index: 7, key: 'narrative', name: 'Story', nameTr: 'Hikaye', layer: 'cognition',
    description: 'Is this a journey with chapters, or a loop?', beliefIndices: [17, 58, 101, 104, 106] },
  { index: 8, key: 'familiarity', name: 'Familiarity', nameTr: 'Tanıdıklık', layer: 'cognition',
    description: 'Do I recognize these patterns/style?', beliefIndices: [20, 31, 51, 54, 109] },
  { index: 9, key: 'pleasure', name: 'Pleasure', nameTr: 'Haz', layer: 'cognition',
    description: 'Am I enjoying this? Do I want more?', beliefIndices: [74, 75, 81, 83, 89] },
  { index: 10, key: 'space', name: 'Space', nameTr: 'Mekan', layer: 'cognition',
    description: 'Intimate whisper or cathedral vastness?', beliefIndices: [13, 16, 35, 36, 60] },
  { index: 11, key: 'repetition', name: 'Repetition', nameTr: 'Tekrar', layer: 'cognition',
    description: 'Same loop over and over, or always changing?', beliefIndices: [20, 25, 31, 85] },
]

// ── 24D Neuroscience ─────────────────────────────────────────────────────────

export const NEUROSCIENCE_DIMS: DimensionDef[] = [
  // Predictive Processing (0-3)
  { index: 0, key: 'prediction_error', name: 'Prediction Error', nameTr: 'Tahmin Hatası', layer: 'neuroscience', parentKey: 'predictive',
    description: 'Magnitude of expectation violation', beliefIndices: [25, 34, 84] },
  { index: 1, key: 'precision', name: 'Precision', nameTr: 'Hassasiyet', layer: 'neuroscience', parentKey: 'predictive',
    description: 'Confidence weighting of predictions', beliefIndices: [20, 39, 46] },
  { index: 2, key: 'information_content', name: 'Information Content', nameTr: 'Bilgi İçeriği', layer: 'neuroscience', parentKey: 'predictive',
    description: 'Surprisal / information-theoretic content', beliefIndices: [25] },
  { index: 3, key: 'model_uncertainty', name: 'Model Uncertainty', nameTr: 'Model Belirsizliği', layer: 'neuroscience', parentKey: 'predictive',
    description: 'Uncertainty in the internal model', beliefIndices: [20, 31, 46] },
  // Sensorimotor (4-7)
  { index: 4, key: 'oscillation_coupling', name: 'Beat Coupling', nameTr: 'Ritim Bağı', layer: 'neuroscience', parentKey: 'sensorimotor',
    description: 'Neural oscillation coupling to beat', beliefIndices: [42, 44] },
  { index: 5, key: 'motor_period_lock', name: 'Period Lock', nameTr: 'Periyot Kilidi', layer: 'neuroscience', parentKey: 'sensorimotor',
    description: 'Motor system period-locking strength', beliefIndices: [96, 98, 99] },
  { index: 6, key: 'auditory_motor_bind', name: 'Motor Binding', nameTr: 'Motor Bağlama', layer: 'neuroscience', parentKey: 'sensorimotor',
    description: 'Auditory-motor cortex binding', beliefIndices: [90, 92, 95, 99] },
  { index: 7, key: 'timing_precision', name: 'Timing Precision', nameTr: 'Zamanlama Hassasiyeti', layer: 'neuroscience', parentKey: 'sensorimotor',
    description: 'Temporal precision of motor timing', beliefIndices: [100] },
  // Emotion Circuitry (8-11)
  { index: 8, key: 'valence_mode', name: 'Valence Mode', nameTr: 'Duygu Modu', layer: 'neuroscience', parentKey: 'emotion',
    description: 'Current emotional valence mode', beliefIndices: [66, 67, 68] },
  { index: 9, key: 'autonomic_arousal', name: 'ANS Arousal', nameTr: 'Otonom Uyarılma', layer: 'neuroscience', parentKey: 'emotion',
    description: 'Autonomic nervous system arousal', beliefIndices: [35, 60, 63] },
  { index: 10, key: 'nostalgia_circuit', name: 'Nostalgia Circuit', nameTr: 'Nostalji Devresi', layer: 'neuroscience', parentKey: 'emotion',
    description: 'Nostalgia processing circuit activation', beliefIndices: [50, 53, 55, 70] },
  { index: 11, key: 'chills_pathway', name: 'Chills Pathway', nameTr: 'Tüylenme Yolu', layer: 'neuroscience', parentKey: 'emotion',
    description: 'Musical chills / frisson pathway', beliefIndices: [60, 61, 62, 79, 83] },
  // Reward System (12-15)
  { index: 12, key: 'da_anticipation', name: 'DA Anticipation', nameTr: 'DA Beklenti', layer: 'neuroscience', parentKey: 'reward',
    description: 'Anticipatory dopamine ramp', beliefIndices: [74, 77, 78] },
  { index: 13, key: 'da_consummation', name: 'DA Consummation', nameTr: 'DA Tüketim', layer: 'neuroscience', parentKey: 'reward',
    description: 'Consummatory dopamine release', beliefIndices: [74, 75, 83, 89] },
  { index: 14, key: 'hedonic_tone', name: 'Hedonic Tone', nameTr: 'Hedonik Ton', layer: 'neuroscience', parentKey: 'reward',
    description: 'Hedonic pleasure quality', beliefIndices: [40, 61, 81, 83] },
  { index: 15, key: 'reward_pe', name: 'Reward PE', nameTr: 'Ödül TH', layer: 'neuroscience', parentKey: 'reward',
    description: 'Reward prediction error', beliefIndices: [75, 84, 85] },
  // Memory & Learning (16-19)
  { index: 16, key: 'episodic_encoding', name: 'Episodic Encoding', nameTr: 'Epizodik Kodlama', layer: 'neuroscience', parentKey: 'memory',
    description: 'Episodic memory encoding strength', beliefIndices: [51, 57, 59] },
  { index: 17, key: 'autobiographical', name: 'Autobiographical', nameTr: 'Otobiyografik', layer: 'neuroscience', parentKey: 'memory',
    description: 'Autobiographical memory retrieval', beliefIndices: [50, 51, 55] },
  { index: 18, key: 'statistical_learning', name: 'Statistical Learning', nameTr: 'İstatistiksel Öğrenme', layer: 'neuroscience', parentKey: 'memory',
    description: 'Statistical regularity learning', beliefIndices: [20, 31, 109] },
  { index: 19, key: 'expertise_effect', name: 'Expertise Effect', nameTr: 'Uzmanlık Etkisi', layer: 'neuroscience', parentKey: 'memory',
    description: 'Musical expertise modulation', beliefIndices: [111, 114, 119, 120] },
  // Social Cognition (20-23)
  { index: 20, key: 'neural_synchrony', name: 'Neural Sync', nameTr: 'Nöral Senkron', layer: 'neuroscience', parentKey: 'social',
    description: 'Inter-brain neural synchrony', beliefIndices: [122, 128] },
  { index: 21, key: 'social_bonding', name: 'Social Bond', nameTr: 'Sosyal Bağ', layer: 'neuroscience', parentKey: 'social',
    description: 'Music-induced social bonding', beliefIndices: [55, 123, 124, 126] },
  { index: 22, key: 'social_prediction', name: 'Social Prediction', nameTr: 'Sosyal Tahmin', layer: 'neuroscience', parentKey: 'social',
    description: 'Social coordination prediction', beliefIndices: [122, 125, 130] },
  { index: 23, key: 'collective_reward', name: 'Collective Reward', nameTr: 'Kolektif Ödül', layer: 'neuroscience', parentKey: 'social',
    description: 'Collective reward experience', beliefIndices: [83, 121, 126] },
]

export const ALL_DIMS: DimensionDef[] = [...PSYCHOLOGY_DIMS, ...COGNITION_DIMS, ...NEUROSCIENCE_DIMS]

/** Tier color scheme */
export const LAYER_COLORS: Record<DimLayer, string> = {
  psychology: '#22c55e',
  cognition: '#3b82f6',
  neuroscience: '#8b5cf6',
}

/** Neuroscience domain groups */
export const NEURO_DOMAINS = [
  { key: 'predictive', name: 'Predictive Processing', indices: [0, 1, 2, 3] },
  { key: 'sensorimotor', name: 'Sensorimotor', indices: [4, 5, 6, 7] },
  { key: 'emotion', name: 'Emotion Circuitry', indices: [8, 9, 10, 11] },
  { key: 'reward', name: 'Reward System', indices: [12, 13, 14, 15] },
  { key: 'memory', name: 'Memory & Learning', indices: [16, 17, 18, 19] },
  { key: 'social', name: 'Social Cognition', indices: [20, 21, 22, 23] },
] as const
