/* ── Mock Listening History — Weekly & Monthly Data ──────────────── */

export interface ListeningDay {
  date: string;           // ISO date
  minutesListened: number;
  tracksPlayed: number;
  topGenre: string;
  dominantBelief: "consonance" | "tempo" | "salience" | "familiarity" | "reward";
  /** Belief snapshot at end of day [consonance, tempo, salience, familiarity, reward] */
  beliefSnapshot: [number, number, number, number, number];
}

export interface WeeklyStats {
  totalMinutes: number;
  totalTracks: number;
  avgMinutesPerDay: number;
  topGenres: { name: string; pct: number }[];
  topArtists: string[];
  peakListeningHour: number;
  /** Belief deltas over the week [Δconsonance, Δtempo, Δsalience, Δfamiliarity, Δreward] */
  beliefDeltas: [number, number, number, number, number];
  /** Most significant PE event */
  peakPE: { description: string; belief: string; magnitude: number };
}

export interface MonthlyEvolution {
  /** 4 weekly snapshots: belief values at each week boundary */
  weeklySnapshots: [number, number, number, number, number][];
  /** Overall drift direction */
  driftDescription: string;
  /** Which belief changed most */
  mostChangedBelief: string;
  mostChangedDelta: number;
}

/* ── Last 7 Days ─────────────────────────────────────────────────── */
export const lastWeekDays: ListeningDay[] = [
  {
    date: "2026-02-11",
    minutesListened: 142,
    tracksPlayed: 38,
    topGenre: "Post-Rock",
    dominantBelief: "salience",
    beliefSnapshot: [0.62, 0.55, 0.78, 0.41, 0.34],
  },
  {
    date: "2026-02-12",
    minutesListened: 87,
    tracksPlayed: 24,
    topGenre: "Ambient",
    dominantBelief: "familiarity",
    beliefSnapshot: [0.64, 0.52, 0.71, 0.48, 0.36],
  },
  {
    date: "2026-02-13",
    minutesListened: 203,
    tracksPlayed: 52,
    topGenre: "Electronic",
    dominantBelief: "tempo",
    beliefSnapshot: [0.58, 0.68, 0.74, 0.44, 0.42],
  },
  {
    date: "2026-02-14",
    minutesListened: 165,
    tracksPlayed: 41,
    topGenre: "Neo-Classical",
    dominantBelief: "consonance",
    beliefSnapshot: [0.72, 0.61, 0.69, 0.52, 0.48],
  },
  {
    date: "2026-02-15",
    minutesListened: 118,
    tracksPlayed: 31,
    topGenre: "Jazz",
    dominantBelief: "reward",
    beliefSnapshot: [0.68, 0.64, 0.72, 0.55, 0.53],
  },
  {
    date: "2026-02-16",
    minutesListened: 234,
    tracksPlayed: 63,
    topGenre: "Electronic",
    dominantBelief: "salience",
    beliefSnapshot: [0.65, 0.71, 0.81, 0.51, 0.49],
  },
  {
    date: "2026-02-17",
    minutesListened: 178,
    tracksPlayed: 47,
    topGenre: "Post-Rock",
    dominantBelief: "reward",
    beliefSnapshot: [0.67, 0.66, 0.76, 0.58, 0.56],
  },
];

/* ── Weekly Aggregate ────────────────────────────────────────────── */
export const weeklyStats: WeeklyStats = {
  totalMinutes: 1127,
  totalTracks: 296,
  avgMinutesPerDay: 161,
  topGenres: [
    { name: "Electronic", pct: 28 },
    { name: "Post-Rock", pct: 22 },
    { name: "Neo-Classical", pct: 18 },
    { name: "Ambient", pct: 16 },
    { name: "Jazz", pct: 12 },
  ],
  topArtists: ["Nils Frahm", "Explosions in the Sky", "Jon Hopkins", "Max Richter", "Aphex Twin"],
  peakListeningHour: 22,
  beliefDeltas: [+0.05, +0.11, -0.02, +0.17, +0.22],
  peakPE: {
    description: "Jon Hopkins — 'Luminous Beings' at 4:32 — the bass drop completely blindsided your sense of harmony while the track already felt deeply familiar. That contrast — surprise inside comfort — triggered a 3.2x pleasure spike.",
    belief: "reward",
    magnitude: 0.41,
  },
};

/* ── Monthly Evolution (4 weeks) ─────────────────────────────────── */
export const monthlyEvolution: MonthlyEvolution = {
  weeklySnapshots: [
    [0.58, 0.48, 0.65, 0.32, 0.21], // Week 1 (late Jan)
    [0.61, 0.53, 0.70, 0.38, 0.29], // Week 2
    [0.63, 0.58, 0.73, 0.45, 0.38], // Week 3
    [0.67, 0.66, 0.76, 0.58, 0.56], // Week 4 (current)
  ],
  driftDescription: "You're getting more selective about what moves you. Your sense of musical memory is growing — patterns click faster. And this week's rhythmic engagement jumped, probably from the Electronic/Post-Rock mix.",
  mostChangedBelief: "reward",
  mostChangedDelta: 0.35,
};

/* ── Recent Tracks (last 5 listened) ─────────────────────────────── */
export interface RecentTrack {
  title: string;
  artist: string;
  genre: string;
  listenedAt: string;
  peakRewardMoment: string;
  rewardIntensity: number; // 0-1
}

export const recentTracks: RecentTrack[] = [
  { title: "Luminous Beings", artist: "Jon Hopkins", genre: "Electronic", listenedAt: "2h ago", peakRewardMoment: "4:32 — bass harmonic shift", rewardIntensity: 0.89 },
  { title: "Your Hand In Mine", artist: "Explosions in the Sky", genre: "Post-Rock", listenedAt: "4h ago", peakRewardMoment: "6:15 — crescendo peak", rewardIntensity: 0.76 },
  { title: "Says", artist: "Nils Frahm", genre: "Neo-Classical", listenedAt: "6h ago", peakRewardMoment: "3:48 — overtone bloom", rewardIntensity: 0.82 },
  { title: "Avril 14th", artist: "Aphex Twin", genre: "Ambient", listenedAt: "8h ago", peakRewardMoment: "1:20 — chromatic descent", rewardIntensity: 0.71 },
  { title: "On The Nature of Daylight", artist: "Max Richter", genre: "Neo-Classical", listenedAt: "Yesterday", peakRewardMoment: "4:05 — viola entry resolves tension", rewardIntensity: 0.93 },
];
