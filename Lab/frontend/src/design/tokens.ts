/** MI-Lab Design Tokens — Apple Liquid Glass Dark */

export const colors = {
  bg: {
    base: '#07070c',
    elevated: '#0a0a0f',
    surface: '#0d0d14',
    hover: '#111118',
  },
  border: {
    subtle: 'rgba(255, 255, 255, 0.06)',
    default: 'rgba(255, 255, 255, 0.10)',
    strong: 'rgba(255, 255, 255, 0.16)',
  },
  text: {
    primary: 'rgba(255, 255, 255, 0.92)',
    secondary: 'rgba(255, 255, 255, 0.56)',
    tertiary: 'rgba(255, 255, 255, 0.36)',
    accent: '#60a5fa',
  },
  belief: {
    core: '#34d399',
    appraisal: '#60a5fa',
    anticipation: '#fbbf24',
  },
} as const

export const glass = {
  0: { bg: 'rgba(255, 255, 255, 0.02)', blur: 'blur(8px)' },
  1: { bg: 'rgba(255, 255, 255, 0.04)', blur: 'blur(16px)' },
  2: { bg: 'rgba(255, 255, 255, 0.06)', blur: 'blur(24px) saturate(1.3)' },
  3: { bg: 'rgba(255, 255, 255, 0.10)', blur: 'blur(32px) saturate(1.5)' },
} as const

export const shadows = {
  sm: '0 1px 2px rgba(0, 0, 0, 0.4)',
  md: '0 4px 12px rgba(0, 0, 0, 0.5)',
  lg: '0 8px 24px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.04)',
  inset: 'inset 0 1px 0 rgba(255, 255, 255, 0.06)',
  glow: (color: string) => `0 0 20px ${color}33, 0 0 40px ${color}1a`,
} as const

export const radii = {
  sm: '6px',
  md: '10px',
  lg: '14px',
  xl: '20px',
} as const
