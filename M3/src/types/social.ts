/* ── M³ Social Types ──────────────────────────────────────────── */

import type { MindProfile } from "./mind";

export interface UserProfile {
  id: string;
  displayName: string;
  avatarUrl: string;
  country: string;
  level: number;
  xp: number;
  mind: MindProfile;
  joinedAt: string;
  tracksAnalyzed: number;
  achievements: string[];   // achievement IDs
  streak: number;
}

export interface CompatibilityResult {
  userId: string;
  score: number;            // 0-100
  label: "Soulmate" | "Resonant" | "Complementary" | "Contrasting";
  strongAxes: string[];     // which axes are most similar
  weakAxes: string[];       // most different
}

export interface ActivityItem {
  id: string;
  userId: string;
  userName: string;
  type: "evolution" | "creation" | "compatibility" | "achievement" | "challenge";
  message: string;
  timestamp: string;
  mediaUrl?: string; // [NEW] path to image/video
  mediaType?: "image" | "video"; // [NEW]
}
