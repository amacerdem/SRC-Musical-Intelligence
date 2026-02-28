/* ── Persona Dimension Profiles — 24 personas × 6D radar ─────────
 *  Each persona has a canonical 6D dimension fingerprint:
 *
 *    Discovery (Keşif)    — Novelty-seeking, expectancy
 *    Intensity (Gerilim)  — Tension, arousal, sonic impact
 *    Flow (Ritim)         — Entrainment, groove, motor coupling
 *    Depth (Duygu)        — Emotional contagion, reward
 *    Trace (Hafıza)       — Memory, recognition, episodic resonance
 *    Sharing (Bağ)        — Social synchrony, bonding
 *
 *  Derived from each persona's gene profile and family alignment.
 *  Values in [0, 1].
 *  ──────────────────────────────────────────────────────────────── */

import type { DimensionProfile } from "@/types/dimensions";

/**
 * Canonical 6D dimension profile for each persona ID.
 * Maps persona.id → DimensionProfile.
 */
export const PERSONA_DIMENSIONS: Record<number, DimensionProfile> = {
  // ─── ALCHEMISTS (tension dominant → high Intensity) ──────────
  1:  { discovery: 0.65, intensity: 0.90, flow: 0.40, depth: 0.55, trace: 0.35, sharing: 0.25 },
  6:  { discovery: 0.55, intensity: 0.95, flow: 0.30, depth: 0.30, trace: 0.45, sharing: 0.25 },
  7:  { discovery: 0.60, intensity: 0.80, flow: 0.35, depth: 0.40, trace: 0.30, sharing: 0.20 },
  18: { discovery: 0.50, intensity: 0.85, flow: 0.25, depth: 0.65, trace: 0.40, sharing: 0.30 },

  // ─── ARCHITECTS (resolution dominant → high Trace) ─────
  2:  { discovery: 0.70, intensity: 0.20, flow: 0.20, depth: 0.45, trace: 0.80, sharing: 0.30 },
  4:  { discovery: 0.30, intensity: 0.15, flow: 0.25, depth: 0.55, trace: 0.60, sharing: 0.20 },
  5:  { discovery: 0.60, intensity: 0.50, flow: 0.20, depth: 0.35, trace: 0.75, sharing: 0.25 },
  9:  { discovery: 0.75, intensity: 0.25, flow: 0.25, depth: 0.25, trace: 0.85, sharing: 0.35 },
  20: { discovery: 0.65, intensity: 0.25, flow: 0.35, depth: 0.20, trace: 0.80, sharing: 0.30 },

  // ─── EXPLORERS (entropy dominant → high Discovery) ──────────
  3:  { discovery: 0.95, intensity: 0.70, flow: 0.35, depth: 0.15, trace: 0.20, sharing: 0.15 },
  10: { discovery: 0.90, intensity: 0.55, flow: 0.40, depth: 0.20, trace: 0.15, sharing: 0.20 },
  19: { discovery: 0.80, intensity: 0.40, flow: 0.35, depth: 0.35, trace: 0.30, sharing: 0.25 },
  23: { discovery: 0.90, intensity: 0.75, flow: 0.25, depth: 0.15, trace: 0.15, sharing: 0.15 },
  24: { discovery: 0.75, intensity: 0.65, flow: 0.55, depth: 0.55, trace: 0.60, sharing: 0.50 },

  // ─── ANCHORS (resonance dominant → high Depth) ──────────
  8:  { discovery: 0.40, intensity: 0.50, flow: 0.25, depth: 0.85, trace: 0.55, sharing: 0.35 },
  11: { discovery: 0.30, intensity: 0.40, flow: 0.25, depth: 0.90, trace: 0.35, sharing: 0.35 },
  13: { discovery: 0.30, intensity: 0.15, flow: 0.20, depth: 0.80, trace: 0.40, sharing: 0.20 },
  15: { discovery: 0.35, intensity: 0.20, flow: 0.20, depth: 0.75, trace: 0.45, sharing: 0.25 },
  17: { discovery: 0.25, intensity: 0.15, flow: 0.25, depth: 0.85, trace: 0.30, sharing: 0.20 },
  22: { discovery: 0.25, intensity: 0.15, flow: 0.20, depth: 0.80, trace: 0.75, sharing: 0.30 },

  // ─── KINETICISTS (plasticity dominant → high Flow) ───
  12: { discovery: 0.35, intensity: 0.50, flow: 0.90, depth: 0.30, trace: 0.25, sharing: 0.40 },
  14: { discovery: 0.60, intensity: 0.85, flow: 0.75, depth: 0.20, trace: 0.20, sharing: 0.25 },
  16: { discovery: 0.30, intensity: 0.30, flow: 0.92, depth: 0.25, trace: 0.35, sharing: 0.45 },
  21: { discovery: 0.45, intensity: 0.70, flow: 0.75, depth: 0.20, trace: 0.15, sharing: 0.20 },
};

/**
 * Get the 6D dimension profile for a persona.
 * Falls back to a balanced profile if persona ID is unknown.
 */
export function getPersonaDimensions(personaId: number): DimensionProfile {
  return PERSONA_DIMENSIONS[personaId] ?? {
    discovery: 0.5, intensity: 0.5, flow: 0.5,
    depth: 0.5, trace: 0.5, sharing: 0.5,
  };
}

/**
 * Get the dominant dimension key for a persona.
 */
export function getDominantDimension(personaId: number): keyof DimensionProfile {
  const profile = getPersonaDimensions(personaId);
  let maxKey: keyof DimensionProfile = "discovery";
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
  Alchemists:  "intensity",
  Architects:  "trace",
  Explorers:   "discovery",
  Anchors:     "depth",
  Kineticists: "flow",
};
