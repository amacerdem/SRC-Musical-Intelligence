/* -- Design Tokens -- M3 Mobile -----------------------------------------------
 *  Single source of truth for colors, spacing, typography, and family palettes.
 *  Dark-first. Glassmorphism. Neuroscience-inspired.
 *  -------------------------------------------------------------------------- */

/* -- Core Colors ------------------------------------------------------------ */

export const colors = {
  /* Surfaces */
  background: "#000000",
  surface: "rgba(255,255,255,0.03)",
  surfaceMedium: "rgba(255,255,255,0.05)",
  surfaceHigh: "rgba(255,255,255,0.08)",
  border: "rgba(255,255,255,0.06)",
  borderLight: "rgba(255,255,255,0.10)",

  /* Text */
  textPrimary: "#FFFFFF",
  textSecondary: "rgba(255,255,255,0.6)",
  textTertiary: "rgba(255,255,255,0.35)",
  textMuted: "rgba(255,255,255,0.2)",

  /* Brand — Violet core */
  violet: "#8B5CF6",
  violetLight: "#A78BFA",
  violetDark: "#6D28D9",

  /* Belief domain colors */
  consonance: "#C084FC",
  tempo: "#F97316",
  salience: "#84CC16",
  familiarity: "#38BDF8",
  reward: "#FBBF24",

  /* Semantic */
  success: "#10B981",
  danger: "#EF4444",
  warning: "#F59E0B",
  info: "#38BDF8",

  /* Gradients (start, end) */
  gradientPrimary: ["#818CF8", "#A78BFA", "#F472B6"] as const,
  gradientReward: ["#FBBF24", "#F59E0B"] as const,
  gradientConsonance: ["#C084FC", "#8B5CF6"] as const,
} as const;

/* -- Family Colors ---------------------------------------------------------- */

export const familyColors: Record<string, string> = {
  Alchemists: "#F472B6",
  Architects: "#818CF8",
  Explorers: "#22D3EE",
  Anchors: "#10B981",
  Kineticists: "#F97316",
};

/* -- Typography ------------------------------------------------------------- */

export const fonts = {
  display: "Saira_700Bold",
  heading: "Saira_600SemiBold",
  body: "Inter_400Regular",
  bodySemiBold: "Inter_600SemiBold",
  mono: "JetBrainsMono_400Regular",
  monoSemiBold: "JetBrainsMono_600SemiBold",
} as const;

/* -- Spacing ---------------------------------------------------------------- */

export const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  xxl: 32,
  xxxl: 48,
} as const;

/* -- Border Radius ---------------------------------------------------------- */

export const radii = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  full: 9999,
} as const;
