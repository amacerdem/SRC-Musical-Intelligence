/* ── Dimension Types — 6D + 12D + 24D Independent Tiers ─────────────
 *  Three falsifiability tiers, each computed independently from beliefs.
 *  NO tier derives from another tier's output.
 *
 *  6D:  Energy, Valence, Tempo, Tension, Groove, Density
 *  12D: Melody, Harmony, Rhythm, Timbre, Emotion, Surprise,
 *       Momentum, Story, Familiarity, Pleasure, Space, Repetition
 *  24D: 6 domains × 4 (predictive, sensorimotor, emotion, reward, memory, social)
 *
 *  Source of truth: Musical_Intelligence/brain/dimensions/tree.py
 *  ──────────────────────────────────────────────────────────────── */

/** The three user-facing dimension layers + raw research layer */
export type DimensionLayer = "psychology" | "cognition" | "neuroscience" | "research";

/** 6D radar profile — one value per psychology dimension */
export interface DimensionProfile {
  energy: number;       // 0-1 — Enerji
  valence: number;      // 0-1 — Duygu Tonu
  tempo: number;        // 0-1 — Hız
  tension: number;      // 0-1 — Gerilim
  groove: number;       // 0-1 — Hareket
  complexity: number;   // 0-1 — Yoğunluk
}

export const DIMENSION_KEYS_6D = [
  "energy", "valence", "tempo", "tension", "groove", "complexity",
] as const;

export type DimensionKey6D = (typeof DIMENSION_KEYS_6D)[number];

/** Tier → which dimension layers are visible */
export const TIER_DIMENSION_ACCESS: Record<string, DimensionLayer[]> = {
  free:     ["psychology"],
  basic:    ["psychology", "cognition"],
  premium:  ["psychology", "cognition", "neuroscience"],
  ultimate: ["psychology", "cognition", "neuroscience", "research"],
};

/** Computed dimension state at a given moment */
export interface DimensionState {
  /** 6D psychology values (always available) */
  psychology: number[];   // length 6
  /** 12D music cognition values (basic+) */
  cognition: number[];    // length 12
  /** 24D neuroscience values (premium+) */
  neuroscience: number[]; // length 24
}
