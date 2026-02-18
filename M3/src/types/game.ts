/* ── M³ Gamification Types ────────────────────────────────────── */

export interface Level {
  level: number;
  title: string;
  xpRequired: number;
  unlocks: string;
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;           // Lucide icon name
  condition: string;
  xpReward: number;
  rarity: "common" | "rare" | "epic" | "legendary";
}

export interface Challenge {
  id: string;
  title: string;
  description: string;
  type: "prediction" | "entropy" | "resolution" | "fusion";
  xpReward: number;
  endsAt: string;         // ISO date
  participants: number;
}

export interface XPEvent {
  action: string;
  xp: number;
  timestamp: string;
}
