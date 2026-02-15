/** MI WebLab design tokens — scientific lab dark theme. */

export const colors = {
  bg: {
    primary: "#0a0a0f",
    panel: "#0d0d14",
    surface: "#111118",
    hover: "#1a1a24",
  },
  text: {
    primary: "#c8c8d4",
    secondary: "#8b8b9e",
    muted: "#5a5a6e",
    accent: "#6366f1",
  },
  grid: "#1a1a2e",
  border: "#252538",
  playhead: "#ef4444",
  accent: "#6366f1",

  r3Groups: {
    consonance: "#ef4444",
    energy: "#f97316",
    timbre: "#eab308",
    change: "#84cc16",
    interactions: "#22c55e",
    pitchChroma: "#14b8a6",
    rhythmGroove: "#06b6d4",
    harmony: "#3b82f6",
    information: "#8b5cf6",
    timbreExt: "#a855f7",
    modulation: "#ec4899",
  },

  scope: {
    internal: "#3b82f6",
    external: "#22c55e",
    hybrid: "#f59e0b",
  },

  neuro: {
    DA: "#f97316",
    NE: "#06b6d4",
    OPI: "#fbbf24",
    "5HT": "#10b981",
  },

  regions: {
    cortical: "#3b82f6",
    subcortical: "#a855f7",
    brainstem: "#ef4444",
  },

  psi: {
    affect: "#f43f5e",
    emotion: "#8b5cf6",
    aesthetic: "#f59e0b",
    bodily: "#06b6d4",
    cognitive: "#3b82f6",
    temporal: "#22c55e",
  },

  tiers: {
    alpha: "#22c55e",
    beta: "#f59e0b",
    gamma: "#ef4444",
  },

  roles: {
    relay: "#64748b",
    encoder: "#3b82f6",
    associator: "#8b5cf6",
    integrator: "#f59e0b",
    hub: "#ef4444",
  },
} as const;

export const fonts = {
  ui: "'Inter', 'Helvetica Neue', -apple-system, sans-serif",
  data: "'JetBrains Mono', 'Fira Code', 'SF Mono', monospace",
} as const;

export const sizes = {
  headerHeight: 44,
  transportHeight: 80,
  sidebarWidth: 160,
  drawerHeight: 300,
  panelGap: 6,
  panelPadding: 12,
  panelRadius: 6,
} as const;

/** Map R³ group letter (A-K) to color. */
export const R3_GROUP_COLOR_MAP: Record<string, string> = {
  A: "#ef4444",
  B: "#f97316",
  C: "#eab308",
  D: "#84cc16",
  E: "#22c55e",
  F: "#14b8a6",
  G: "#06b6d4",
  H: "#3b82f6",
  I: "#8b5cf6",
  J: "#a855f7",
  K: "#ec4899",
};
