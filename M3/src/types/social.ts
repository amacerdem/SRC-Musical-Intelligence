/* ── M³ Social Types ──────────────────────────────────────────── */

import type { MindProfile } from "./mind";

export interface UserListeningStats {
  totalHours: number;
  tracksThisWeek: number;
  minutesThisWeek: number;
  topGenres: { name: string; pct: number }[];
  topArtists: string[];
  peakHour: number;
  /** Belief snapshot at end of current week [consonance, tempo, salience, familiarity, reward] */
  beliefSnapshot: [number, number, number, number, number];
  /** Weekly belief deltas */
  beliefDeltas: [number, number, number, number, number];
}

export interface UserRecentTrack {
  title: string;
  artist: string;
  genre: string;
  listenedAt: string;
  rewardIntensity: number;
  peakMoment?: string;
}

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
  achievements: string[];
  streak: number;
  /** Short bio — how this person relates to music */
  bio?: string;
  /** Listening stats for this user */
  listening?: UserListeningStats;
  /** Recent tracks this user listened to */
  recentTracks?: UserRecentTrack[];
  /** Number of compositions created */
  compositionsCreated?: number;
  /** Number of live sessions performed */
  liveSessionsPlayed?: number;
}

export interface CompatibilityResult {
  userId: string;
  score: number;
  label: "Soulmate" | "Resonant" | "Complementary" | "Contrasting";
  strongAxes: string[];
  weakAxes: string[];
}

export interface ActivityItem {
  id: string;
  userId: string;
  userName: string;
  type: "evolution" | "creation" | "compatibility" | "achievement" | "challenge" | "performance" | "composition" | "listening";
  message: string;
  timestamp: string;
  mediaUrl?: string;
  mediaType?: "image" | "video";
}
