/** MI-Lab Design Tokens — Dark Glassmorphism */

export const colors = {
  bg: '#0a0a0f',
  surface: 'rgba(255, 255, 255, 0.03)',
  glass: 'rgba(255, 255, 255, 0.06)',
  glassBorder: 'rgba(255, 255, 255, 0.08)',
  glassHover: 'rgba(255, 255, 255, 0.10)',
  textPrimary: 'rgba(255, 255, 255, 0.92)',
  textSecondary: 'rgba(255, 255, 255, 0.55)',
  textMuted: 'rgba(255, 255, 255, 0.30)',

  // Pipeline stage accents
  r3: '#3b82f6',
  h3: '#8b5cf6',
  c3: '#10b981',
  reward: '#f59e0b',
  danger: '#ef4444',

  // R³ group colors
  groupA: '#60a5fa',
  groupB: '#f97316',
  groupC: '#14b8a6',
  groupD: '#eab308',
  groupF: '#22c55e',
  groupG: '#ef4444',
  groupH: '#a78bfa',
  groupJ: '#6366f1',
  groupK: '#ec4899',
} as const;

export const R3_GROUP_COLORS: Record<string, string> = {
  A: colors.groupA,
  B: colors.groupB,
  C: colors.groupC,
  D: colors.groupD,
  F: colors.groupF,
  G: colors.groupG,
  H: colors.groupH,
  J: colors.groupJ,
  K: colors.groupK,
};

export const R3_GROUPS = [
  { key: 'A', name: 'Consonance',   range: [0, 7],   detail: 'Sethares roughness, Plomp-Levelt, Helmholtz, Stumpf' },
  { key: 'B', name: 'Energy',       range: [7, 12],  detail: 'RMS amplitude, loudness, onset strength, velocity' },
  { key: 'C', name: 'Timbre',       range: [12, 21], detail: 'Warmth, sharpness, tonalness, clarity, tristimulus' },
  { key: 'D', name: 'Change',       range: [21, 25], detail: 'Spectral flux, entropy, flatness, concentration' },
  { key: 'F', name: 'Pitch/Chroma', range: [25, 41], detail: '12-bin chroma, pitch height, key clarity' },
  { key: 'G', name: 'Rhythm',       range: [41, 51], detail: 'Tempo, beat strength, pulse clarity, groove' },
  { key: 'H', name: 'Harmony',      range: [51, 63], detail: 'Key clarity, Tonnetz, voice leading, diatonicity' },
  { key: 'J', name: 'Timbre Ext',   range: [63, 83], detail: 'MFCC 1-13, spectral contrast 1-7' },
  { key: 'K', name: 'Modulation',   range: [83, 97], detail: 'Modulation spectrum, Zwicker sharpness, fluctuation' },
] as const;

export const RELAY_INFO = [
  { name: 'BCH',   unit: 'SPU', dim: 16, color: '#60a5fa', detail: 'Brainstem Consonance Hierarchy' },
  { name: 'HMCE',  unit: 'STU', dim: 18, color: '#a78bfa', detail: 'Hierarchical Musical Context Encoding' },
  { name: 'SNEM',  unit: 'ASU', dim: 12, color: '#f97316', detail: 'Sensory Novelty Expectation Model' },
  { name: 'MEAMN', unit: 'IMU', dim: 12, color: '#14b8a6', detail: 'Music-Evoked Autobiographical Memory' },
  { name: 'DAED',  unit: 'RPU', dim: 8,  color: '#eab308', detail: 'Dopamine Anticipation-Experience Dissociation' },
  { name: 'MPG',   unit: 'NDU', dim: 10, color: '#22c55e', detail: 'Melodic Pitch Gradient' },
  { name: 'SRP',   unit: 'ARU', dim: 5,  color: '#ef4444', detail: 'Subjective Reward & Pleasure' },
  { name: 'PEOM',  unit: 'MPU', dim: 3,  color: '#ec4899', detail: 'Period Entrainment Oscillation Model' },
  { name: 'HTP',   unit: 'PCU', dim: 9,  color: '#6366f1', detail: 'Hierarchical Temporal Prediction' },
] as const;

export const RAM_REGIONS = [
  'A1_HG','STG','STS','IFG','AG','TP','dlPFC','vmPFC','OFC','Insula','ACC','SMA',
  'MGB','Caudate','Putamen','NAcc','Hippocampus','Amygdala','VTA','PAG','IC',
  'AN','CN','SOC','IC_bs','PAG_bs',
];

export const NEURO_CHANNELS = [
  { name: 'Dopamine',       short: 'DA',  color: '#f59e0b' },
  { name: 'Norepinephrine', short: 'NE',  color: '#ef4444' },
  { name: 'Opioid',         short: 'OPI', color: '#a78bfa' },
  { name: 'Serotonin',      short: '5HT', color: '#10b981' },
];

export const FRAME_RATE = 172.27;

export const TRANSITION_MS = 450;
export const TRANSITION_EASING = 'cubic-bezier(0.16, 1, 0.3, 1)';
