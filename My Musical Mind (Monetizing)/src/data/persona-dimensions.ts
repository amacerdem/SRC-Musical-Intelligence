/* ── Persona Dimension Profiles — 24 personas × 6D radar ─────────
 *  Each persona has a canonical 6D dimension fingerprint:
 *
 *    Energy (Enerji)         — Perceived intensity/activation
 *    Valence (Duygu Tonu)    — Positive-to-negative emotional coloring
 *    Tempo (Hız)             — Perceived speed of musical events
 *    Tension (Gerilim)       — Felt strain, suspense vs. release
 *    Groove (Hareket)        — The urge to move rhythmically
 *    Complexity (Yoğunluk)   — Perceived density of events
 *
 *  Computed from each persona's 5-gene profile using multi-gene formulas,
 *  then amplified on the family's dominant dimension (+30%).
 *  Values in [0.15, 0.95].
 *
 *  Source of truth: Musical_Intelligence/brain/dimensions/tree.py
 *  ──────────────────────────────────────────────────────────────── */

import type { DimensionProfile } from "@/types/dimensions";

/**
 * Canonical 6D dimension profile for each persona ID.
 * Maps persona.id → DimensionProfile.
 */
export const PERSONA_DIMENSIONS: Record<number, DimensionProfile> = {
  // ─── ALCHEMISTS (tension gene dominant → tension dim amplified ×1.3) ──────
  1:  { energy: 0.54, valence: 0.38, tempo: 0.46, tension: 0.80, groove: 0.51, complexity: 0.39 },  // Dopamine Seeker
  6:  { energy: 0.55, valence: 0.29, tempo: 0.45, tension: 0.78, groove: 0.40, complexity: 0.52 },  // Tension Architect
  7:  { energy: 0.57, valence: 0.31, tempo: 0.52, tension: 0.75, groove: 0.46, complexity: 0.46 },  // Contrast Addict
  18: { energy: 0.48, valence: 0.44, tempo: 0.38, tension: 0.81, groove: 0.47, complexity: 0.44 },  // Dramatic Arc

  // ─── ARCHITECTS (resolution gene dominant → complexity dim amplified ×1.3) ─
  2:  { energy: 0.15, valence: 0.46, tempo: 0.15, tension: 0.20, groove: 0.23, complexity: 0.51 },  // Harmonic Purist
  4:  { energy: 0.15, valence: 0.47, tempo: 0.15, tension: 0.20, groove: 0.27, complexity: 0.40 },  // Minimal Zen
  5:  { energy: 0.25, valence: 0.42, tempo: 0.21, tension: 0.31, groove: 0.26, complexity: 0.62 },  // Resolution Junkie
  9:  { energy: 0.24, valence: 0.36, tempo: 0.25, tension: 0.22, groove: 0.22, complexity: 0.59 },  // Pattern Hunter
  20: { energy: 0.22, valence: 0.38, tempo: 0.24, tension: 0.16, groove: 0.25, complexity: 0.50 },  // Precision Mind

  // ─── EXPLORERS (entropy gene dominant → complexity dim amplified ×1.3) ─────
  3:  { energy: 0.55, valence: 0.15, tempo: 0.52, tension: 0.48, groove: 0.28, complexity: 0.70 },  // Chaos Explorer
  10: { energy: 0.52, valence: 0.20, tempo: 0.52, tension: 0.42, groove: 0.31, complexity: 0.63 },  // Sonic Nomad
  19: { energy: 0.40, valence: 0.31, tempo: 0.41, tension: 0.39, groove: 0.30, complexity: 0.59 },  // Curious Wanderer
  23: { energy: 0.54, valence: 0.15, tempo: 0.50, tension: 0.49, groove: 0.27, complexity: 0.68 },  // Edge Runner
  24: { energy: 0.51, valence: 0.46, tempo: 0.51, tension: 0.50, groove: 0.45, complexity: 0.72 },  // Renaissance Mind

  // ─── ANCHORS (resonance gene dominant → valence dim amplified ×1.3) ────────
  8:  { energy: 0.24, valence: 0.73, tempo: 0.22, tension: 0.41, groove: 0.42, complexity: 0.29 },  // Structural Romantic
  11: { energy: 0.22, valence: 0.73, tempo: 0.21, tension: 0.41, groove: 0.44, complexity: 0.21 },  // Emotional Anchor
  13: { energy: 0.15, valence: 0.63, tempo: 0.15, tension: 0.28, groove: 0.32, complexity: 0.19 },  // Tonal Dreamer
  15: { energy: 0.15, valence: 0.63, tempo: 0.15, tension: 0.28, groove: 0.31, complexity: 0.21 },  // Quiet Observer
  17: { energy: 0.15, valence: 0.62, tempo: 0.15, tension: 0.28, groove: 0.35, complexity: 0.15 },  // Ambient Flow
  22: { energy: 0.15, valence: 0.73, tempo: 0.15, tension: 0.29, groove: 0.37, complexity: 0.19 },  // Nostalgic Soul

  // ─── KINETICISTS (plasticity gene dominant → groove dim amplified ×1.3) ────
  12: { energy: 0.45, valence: 0.39, tempo: 0.54, tension: 0.26, groove: 0.68, complexity: 0.26 },  // Rhythmic Pulse
  14: { energy: 0.65, valence: 0.35, tempo: 0.68, tension: 0.47, groove: 0.72, complexity: 0.47 },  // Dynamic Storm
  16: { energy: 0.40, valence: 0.42, tempo: 0.51, tension: 0.20, groove: 0.66, complexity: 0.27 },  // Groove Mechanic
  21: { energy: 0.53, valence: 0.30, tempo: 0.59, tension: 0.35, groove: 0.64, complexity: 0.32 },  // Raw Energy
};

/**
 * Get the 6D dimension profile for a persona.
 * Falls back to a balanced profile if persona ID is unknown.
 */
export function getPersonaDimensions(personaId: number): DimensionProfile {
  return PERSONA_DIMENSIONS[personaId] ?? {
    energy: 0.5, valence: 0.5, tempo: 0.5,
    tension: 0.5, groove: 0.5, complexity: 0.5,
  };
}

/**
 * Get the dominant dimension key for a persona.
 */
export function getDominantDimension(personaId: number): keyof DimensionProfile {
  const profile = getPersonaDimensions(personaId);
  let maxKey: keyof DimensionProfile = "energy";
  let maxVal = -1;
  for (const [key, val] of Object.entries(profile) as [keyof DimensionProfile, number][]) {
    if (val > maxVal) {
      maxVal = val;
      maxKey = key;
    }
  }
  return maxKey;
}

/**
 * Family → typical dimension emphasis.
 */
export const FAMILY_DIMENSION_EMPHASIS: Record<string, keyof DimensionProfile> = {
  Alchemists:  "tension",
  Architects:  "complexity",
  Explorers:   "complexity",
  Anchors:     "valence",
  Kineticists: "groove",
};
