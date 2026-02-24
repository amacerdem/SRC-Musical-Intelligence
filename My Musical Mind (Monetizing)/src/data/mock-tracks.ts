/* ── Mock Track Data — Rich, interconnected with mock-users ──── */

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
  /** Belief domain that peaks during this track */
  peakBelief?: "consonance" | "tempo" | "salience" | "familiarity" | "reward";
  /** Peak reward moment description */
  peakMoment?: string;
  /** Brief PE-based reason for the recommendation */
  peReason?: string;
  /** BPM for display */
  bpm?: number;
  /** Key signature */
  key?: string;
}

/* ── Recommended for current user (PE-optimized) ────────────── */
export const recommendedTracks: Track[] = [
  {
    id: "r1", title: "Neural Overdrive", artist: "SynthMind", genre: "Electronic",
    match: 94, duration: "3:42", bpm: 128, key: "Dm",
    peakBelief: "reward", peakMoment: "2:18 — filter sweep → harmonic lock",
    peReason: "High consonance PE at sweep resolution → DA spike predicted",
  },
  {
    id: "r2", title: "Deep Resonance", artist: "Harmonic Lab", genre: "Ambient",
    match: 91, duration: "5:18", bpm: 72, key: "Eb",
    peakBelief: "familiarity", peakMoment: "3:45 — overtone bloom deepens",
    peReason: "Low PE amplitude + high recurrence → serotonin-mediated immersion",
  },
  {
    id: "r3", title: "Entropy Garden", artist: "Kai T.", genre: "Post-Rock",
    match: 88, duration: "4:55", bpm: 140, key: "Am",
    peakBelief: "salience", peakMoment: "4:12 — crescendo breaks through noise floor",
    peReason: "Salience-gated PE → attentional capture at dynamic peak",
  },
  {
    id: "r4", title: "Cognitive Drift", artist: "Max Richter", genre: "Neo-Classical",
    match: 85, duration: "6:02", bpm: 60, key: "F",
    peakBelief: "consonance", peakMoment: "4:38 — viola resolves Neapolitan chord",
    peReason: "Deceptive cadence → high PE → resolution reward at V-I",
  },
  {
    id: "r5", title: "Tension Architecture", artist: "Nils Frahm", genre: "Minimal",
    match: 82, duration: "4:33", bpm: 96, key: "Cm",
    peakBelief: "reward", peakMoment: "3:20 — pedal tone finally releases",
    peReason: "Sustained tension appetite → accumulated DA release at resolution",
  },
  {
    id: "r6", title: "Midnight Signal", artist: "Aphex Twin", genre: "IDM",
    match: 79, duration: "3:21", bpm: 135, key: "Bb",
    peakBelief: "tempo", peakMoment: "1:48 — polyrhythm phase-locks",
    peReason: "Rhythmic entropy → NE exploration → motor cortex entrainment",
  },
  {
    id: "r7", title: "Gravity Well", artist: "Ólafur Arnalds", genre: "Neo-Classical",
    match: 76, duration: "5:44", bpm: 66, key: "Ab",
    peakBelief: "familiarity", peakMoment: "5:10 — main theme returns, transposed",
    peReason: "Recurrence + transformation → hippocampal pattern match with novelty",
  },
  {
    id: "r8", title: "Submerge", artist: "Jon Hopkins", genre: "Electronic",
    match: 73, duration: "7:15", bpm: 110, key: "Em",
    peakBelief: "salience", peakMoment: "5:42 — bass drop after 2min build",
    peReason: "Extended PE accumulation → massive prediction violation → peak reward",
  },
];

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
