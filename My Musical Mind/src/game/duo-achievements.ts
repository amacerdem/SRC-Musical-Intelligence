/* ── Duo Performance: Achievements & Tasks ────────────────────── */

export interface Achievement {
  id: string;
  name: string;
  description: string;
  xp: number;
  icon: string;      // emoji for display
  trigger: "auto";   // all auto-evaluated by game engine
}

export interface DuoTask {
  id: string;
  name: string;
  description: string;
  xp: number;
  durationSec: number;
  /** Returns 0-1 progress based on current params */
  evaluate: (emo: number[], phys: number[]) => number;
}

/* ── Achievement Definitions ──────────────────────────────────── */

export const ACHIEVEMENTS: Achievement[] = [
  {
    id: "first_resonance",
    name: "First Resonance",
    description: "Streams touched in the center",
    xp: 150,
    icon: "✦",
    trigger: "auto",
  },
  {
    id: "flow_master",
    name: "Flow Master",
    description: "15s of continuous high resonance",
    xp: 300,
    icon: "◈",
    trigger: "auto",
  },
  {
    id: "chaos_alchemist",
    name: "Chaos Alchemist",
    description: "Both pushed arousal and energy to max",
    xp: 200,
    icon: "⚡",
    trigger: "auto",
  },
  {
    id: "whisper",
    name: "Whisper",
    description: "Both minimized all parameters",
    xp: 250,
    icon: "◌",
    trigger: "auto",
  },
  {
    id: "perfect_sync",
    name: "Perfect Sync",
    description: "All 8 params within 10% of each other",
    xp: 500,
    icon: "⬡",
    trigger: "auto",
  },
  {
    id: "crescendo_rider",
    name: "Crescendo Rider",
    description: "Peak intensity at the 90s mark",
    xp: 350,
    icon: "△",
    trigger: "auto",
  },
  {
    id: "genre_bender",
    name: "Genre Bender",
    description: "Rapidly alternated between extremes",
    xp: 200,
    icon: "◇",
    trigger: "auto",
  },
  {
    id: "neural_link",
    name: "Neural Link",
    description: "30s of unbroken resonance",
    xp: 400,
    icon: "⊛",
    trigger: "auto",
  },
  {
    id: "finale",
    name: "Finale",
    description: "Completed a full 2-minute session",
    xp: 500,
    icon: "★",
    trigger: "auto",
  },
];

/* ── Task Pool ────────────────────────────────────────────────── */

export const TASK_POOL: DuoTask[] = [
  {
    id: "sync_arousal",
    name: "Sync your Arousal",
    description: "Both bring arousal/energy to similar levels",
    xp: 200,
    durationSec: 20,
    evaluate: (emo, phys) => 1 - Math.abs(emo[1] - phys[1]),
  },
  {
    id: "build_storm",
    name: "Build the Storm",
    description: "Raise all parameters above 0.7",
    xp: 250,
    durationSec: 25,
    evaluate: (emo, phys) => {
      const all = [...emo, ...phys];
      const above = all.filter(v => v > 0.7).length;
      return above / all.length;
    },
  },
  {
    id: "find_silence",
    name: "Find the Silence",
    description: "Lower all parameters below 0.3",
    xp: 250,
    durationSec: 25,
    evaluate: (emo, phys) => {
      const all = [...emo, ...phys];
      const below = all.filter(v => v < 0.3).length;
      return below / all.length;
    },
  },
  {
    id: "contrast_dance",
    name: "Contrast Dance",
    description: "One user high, the other low",
    xp: 200,
    durationSec: 20,
    evaluate: (emo, phys) => {
      const emoAvg = emo.reduce((a, b) => a + b, 0) / 4;
      const physAvg = phys.reduce((a, b) => a + b, 0) / 4;
      return Math.abs(emoAvg - physAvg);
    },
  },
  {
    id: "emotional_surge",
    name: "Emotional Surge",
    description: "Emotional user pushes all 4 to max",
    xp: 200,
    durationSec: 20,
    evaluate: (emo) => {
      return emo.reduce((a, b) => a + b, 0) / 4;
    },
  },
  {
    id: "physical_foundation",
    name: "Physical Foundation",
    description: "Physical user holds steady at 0.5",
    xp: 200,
    durationSec: 20,
    evaluate: (_emo, phys) => {
      const deviation = phys.reduce((a, b) => a + Math.abs(b - 0.5), 0) / 4;
      return 1 - deviation * 2;
    },
  },
  {
    id: "deep_dive",
    name: "Deep Dive",
    description: "Maximize depth and density together",
    xp: 200,
    durationSec: 20,
    evaluate: (emo, phys) => (emo[2] + phys[3]) / 2,
  },
  {
    id: "memory_lane",
    name: "Memory Lane",
    description: "Push nostalgia to maximum",
    xp: 150,
    durationSec: 15,
    evaluate: (emo) => emo[3],
  },
];
