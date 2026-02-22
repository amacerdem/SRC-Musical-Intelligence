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
  { key: 'A', name: 'Consonance',   range: [0, 7]   },
  { key: 'B', name: 'Energy',       range: [7, 12]  },
  { key: 'C', name: 'Timbre',       range: [12, 21] },
  { key: 'D', name: 'Change',       range: [21, 25] },
  { key: 'F', name: 'Pitch/Chroma', range: [25, 41] },
  { key: 'G', name: 'Rhythm',       range: [41, 51] },
  { key: 'H', name: 'Harmony',      range: [51, 63] },
  { key: 'J', name: 'Timbre Ext',   range: [63, 83] },
  { key: 'K', name: 'Modulation',   range: [83, 97] },
] as const;

export const FRAME_RATE = 172.27;
