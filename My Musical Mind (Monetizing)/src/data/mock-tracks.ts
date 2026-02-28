/* ── Track Recommendations — Real MI Dataset + Social Data ──────── */

import { miDataService, MIDataService } from "@/services/MIDataService";
import type { MICatalogTrack } from "@/types/mi-dataset";
import { DEFAULT_GENES, type MindGenes } from "@/types/m3";

export interface Track {
  id: string;
  title: string;
  artist: string;
  genre: string;
  match?: number;
  duration: string;
  plays?: number;
  isLive?: boolean;
  creator?: string;
  peakBelief?: "consonance" | "tempo" | "salience" | "familiarity" | "reward";
  peakMoment?: string;
  peReason?: string;
  bpm?: number;
  key?: string;
}

/* ── Helpers ──────────────────────────────────────────────────── */

function formatDuration(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

const GENE_TO_BELIEF: Record<string, Track["peakBelief"]> = {
  resolution: "consonance",
  plasticity: "tempo",
  entropy: "salience",
  resonance: "familiarity",
  tension: "reward",
};

function catalogToTrack(ct: MICatalogTrack, matchPct: number): Track {
  const geneVal = ct.genes[ct.dominant_gene as keyof typeof ct.genes];
  return {
    id: ct.id,
    title: ct.title,
    artist: ct.artist,
    genre: ct.categories[0] ?? "Unknown",
    match: matchPct,
    duration: formatDuration(ct.duration_s),
    bpm: Math.round(ct.signal.tempo),
    peakBelief: GENE_TO_BELIEF[ct.dominant_gene] ?? "reward",
    peReason: `Dominant gene: ${ct.dominant_gene} (${(geneVal * 100).toFixed(0)}%)`,
  };
}

/* ── Recommended for current user (gene-based) ────────────────── */

export function getRecommendedTracks(userGenes?: MindGenes): Track[] {
  if (!miDataService.isReady()) return [];
  const recs = miDataService.getRecommendations(userGenes ?? DEFAULT_GENES, 8);
  return recs.map((ct, i) => catalogToTrack(ct, 95 - i * 3));
}

/** Static fallback for backward compat (lazy computed) */
export const recommendedTracks: Track[] = [];

export function initRecommendedTracks(userGenes?: MindGenes): void {
  recommendedTracks.length = 0;
  recommendedTracks.push(...getRecommendedTracks(userGenes));
}

/* ── Top Community Performances ─────────────────────────────── */
export const topPerformances: Track[] = [
  {
    id: "t1", title: "Neural Drift", artist: "Lena M. × Marcus W.", genre: "Live Duo",
    plays: 4200, isLive: true, duration: "12:30", bpm: 118, key: "Gm",
    peakBelief: "reward", peakMoment: "8:45 — dual mind synchronization peak",
  },
  {
    id: "t2", title: "Entropy Garden", artist: "Kai T.", genre: "Solo Performance",
    plays: 3800, duration: "8:15", bpm: 140, key: "Am",
    peakBelief: "salience", peakMoment: "6:30 — controlled noise floor eruption",
  },
  {
    id: "t3", title: "Deep State", artist: "Mia C.", genre: "Solo Performance",
    plays: 3200, duration: "6:40", bpm: 84, key: "Db",
    peakBelief: "familiarity", peakMoment: "5:15 — theme variation 3 — deepest",
  },
  {
    id: "t4", title: "Harmonic Pulse", artist: "Yuki A.", genre: "Live Solo",
    plays: 2900, isLive: true, duration: "10:05", bpm: 55, key: "Eb",
    peakBelief: "consonance", peakMoment: "7:22 — pure interval cascade",
  },
  {
    id: "t5", title: "Midnight Architecture", artist: "Marcus W.", genre: "Solo Performance",
    plays: 2400, duration: "7:22", bpm: 105, key: "Bb",
    peakBelief: "reward", peakMoment: "5:50 — structural climax resolves 3 tension threads",
  },
  {
    id: "t6", title: "Storm Protocol", artist: "Sofia R.", genre: "Live Solo",
    plays: 2100, isLive: false, duration: "9:18", bpm: 156, key: "F#m",
    peakBelief: "salience", peakMoment: "7:00 — dynamic storm peak at max density",
  },
  {
    id: "t7", title: "Memory Palace", artist: "Ava L.", genre: "Solo Performance",
    plays: 1800, duration: "5:55", bpm: 72, key: "C",
    peakBelief: "familiarity", peakMoment: "4:30 — nostalgic motif returns in minor",
  },
];

/* ── Friend Activity (matched to mock-users.ts) ────────────── */
export interface FriendActivity {
  id: string;
  userId: string;
  userName: string;
  action: "listening" | "composed" | "performing";
  trackTitle: string;
  timeAgo: string;
}

export const friendActivity: FriendActivity[] = [
  { id: "fa1", userId: "u1", userName: "Lena M.", action: "performing", trackTitle: "Neural Drift", timeAgo: "Live now" },
  { id: "fa2", userId: "u7", userName: "Marcus W.", action: "composed", trackTitle: "Midnight Architecture", timeAgo: "2h ago" },
  { id: "fa3", userId: "u2", userName: "Kai T.", action: "listening", trackTitle: "Entropy Garden", timeAgo: "4h ago" },
  { id: "fa4", userId: "u6", userName: "Yuki A.", action: "performing", trackTitle: "Harmonic Pulse", timeAgo: "Live now" },
  { id: "fa5", userId: "u5", userName: "Mia C.", action: "listening", trackTitle: "Deep State", timeAgo: "6h ago" },
  { id: "fa6", userId: "u3", userName: "Sofia R.", action: "composed", trackTitle: "Storm Protocol", timeAgo: "8h ago" },
  { id: "fa7", userId: "u9", userName: "Felix D.", action: "listening", trackTitle: "Midnight Signal", timeAgo: "12h ago" },
  { id: "fa8", userId: "u12", userName: "Zara B.", action: "composed", trackTitle: "Contrast Engine", timeAgo: "1d ago" },
];
