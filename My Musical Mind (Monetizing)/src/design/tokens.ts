/* ── M³ Design Tokens — SRC⁹ DNA ──────────────────────────────── */

export const colors = {
  bg: "#000000",
  surface: "rgba(255,255,255,0.04)",
  surfaceRaised: "rgba(255,255,255,0.06)",
  surfaceHover: "rgba(255,255,255,0.09)",
  border: "rgba(255,255,255,0.08)",
  borderHover: "rgba(255,255,255,0.14)",

  accent: {
    indigo: "#6366F1",
    purple: "#A855F7",
    violet: "#8B5CF6",
    pink: "#EC4899",
    rose: "#F43F5E",
    cyan: "#06B6D4",
  },

  text: {
    primary: "#F1F5F9",
    secondary: "#94A3B8",
    muted: "#475569",
    ghost: "#1E293B",
  },

  success: "#10B981",
  warning: "#F59E0B",
  danger: "#EF4444",
} as const;

/* ── 5 Belief Domain Gradients (from SRC⁹ S³/R³/C³ system) ─── */

export const beliefColors = {
  consonance: {
    primary: "#C084FC",
    gradient: "linear-gradient(135deg, #C084FC, #F472B6, #EC4899)",
    glow: "rgba(192, 132, 252, 0.25)",
  },
  tempo: {
    primary: "#F97316",
    gradient: "linear-gradient(135deg, #EF4444, #F97316, #FDE047)",
    glow: "rgba(249, 115, 22, 0.25)",
  },
  salience: {
    primary: "#84CC16",
    gradient: "linear-gradient(135deg, #FDE047, #84CC16, #22C55E)",
    glow: "rgba(132, 204, 22, 0.25)",
  },
  familiarity: {
    primary: "#38BDF8",
    gradient: "linear-gradient(135deg, #22D3EE, #3B82F6, #6366F1)",
    glow: "rgba(56, 189, 248, 0.25)",
  },
  reward: {
    primary: "#FBBF24",
    gradient: "linear-gradient(135deg, #F59E0B, #FDE047, #FFFFFF)",
    glow: "rgba(251, 191, 36, 0.25)",
  },
  prediction: {
    primary: "#06B6D4",
    gradient: "linear-gradient(135deg, #06B6D4, #22D3EE, #67E8F9)",
    glow: "rgba(6, 182, 212, 0.25)",
  },
  emotion: {
    primary: "#F43F5E",
    gradient: "linear-gradient(135deg, #F43F5E, #EC4899, #F472B6)",
    glow: "rgba(244, 63, 94, 0.25)",
  },
} as const;

export const gradients = {
  accent: "linear-gradient(135deg, #6366F1, #A855F7, #EC4899)",
  accentH: "linear-gradient(90deg, #6366F1, #A855F7, #EC4899)",
  surface: "linear-gradient(180deg, rgba(255,255,255,0.02), transparent)",
  glow: "radial-gradient(ellipse at center, rgba(99,102,241,0.14), transparent 70%)",
  warmGlow: "radial-gradient(ellipse at center, rgba(168,85,247,0.10), transparent 60%)",
} as const;

/* ── SRC⁹ Orbital timings ─────────────────────────────────────── */

export const orbitalTimings = {
  fast: 24,    // seconds per revolution
  medium: 30,
  slow: 36,
} as const;

/* ── Compatibility labels ──────────────────────────────────────── */

export const compatibilityLabels = {
  soulmate: { min: 90, label: "Soulmate", color: "#EC4899" },
  resonant: { min: 70, label: "Resonant", color: "#A855F7" },
  complementary: { min: 50, label: "Complementary", color: "#6366F1" },
  contrasting: { min: 0, label: "Contrasting", color: "#94A3B8" },
} as const;

export function getCompatibilityLabel(score: number) {
  if (score >= 90) return compatibilityLabels.soulmate;
  if (score >= 70) return compatibilityLabels.resonant;
  if (score >= 50) return compatibilityLabels.complementary;
  return compatibilityLabels.contrasting;
}
