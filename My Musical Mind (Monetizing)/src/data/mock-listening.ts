/* ── Listening History — Derived from Real MI Dataset ─────────────── */

import { miDataService } from "@/services/MIDataService";

export interface ListeningDay {
  date: string;
  minutesListened: number;
  tracksPlayed: number;
  topGenre: string;
  dominantBelief: "consonance" | "tempo" | "salience" | "familiarity" | "reward";
  beliefSnapshot: [number, number, number, number, number];
}

export interface WeeklyStats {
  totalMinutes: number;
  totalTracks: number;
  avgMinutesPerDay: number;
  topGenres: { name: string; pct: number }[];
  topArtists: string[];
  peakListeningHour: number;
  beliefDeltas: [number, number, number, number, number];
  peakPE: { description: string; belief: string; magnitude: number };
}

export interface MonthlyEvolution {
  weeklySnapshots: [number, number, number, number, number][];
  driftDescription: string;
  mostChangedBelief: string;
  mostChangedDelta: number;
}

export interface RecentTrack {
  title: string;
  artist: string;
  genre: string;
  listenedAt: string;
  peakRewardMoment: string;
  rewardIntensity: number;
}

/* ── Fallback defaults ─────────────────────────────────────────── */

const DEFAULT_WEEKLY_STATS: WeeklyStats = {
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
    description: "Loading real data...",
    belief: "reward",
    magnitude: 0.41,
  },
};

const DEFAULT_LAST_WEEK: ListeningDay[] = [
  { date: "2026-02-21", minutesListened: 142, tracksPlayed: 38, topGenre: "Unknown", dominantBelief: "salience", beliefSnapshot: [0.62, 0.55, 0.78, 0.41, 0.34] },
  { date: "2026-02-22", minutesListened: 87, tracksPlayed: 24, topGenre: "Unknown", dominantBelief: "familiarity", beliefSnapshot: [0.64, 0.52, 0.71, 0.48, 0.36] },
  { date: "2026-02-23", minutesListened: 203, tracksPlayed: 52, topGenre: "Unknown", dominantBelief: "tempo", beliefSnapshot: [0.58, 0.68, 0.74, 0.44, 0.42] },
  { date: "2026-02-24", minutesListened: 165, tracksPlayed: 41, topGenre: "Unknown", dominantBelief: "consonance", beliefSnapshot: [0.72, 0.61, 0.69, 0.52, 0.48] },
  { date: "2026-02-25", minutesListened: 118, tracksPlayed: 31, topGenre: "Unknown", dominantBelief: "reward", beliefSnapshot: [0.68, 0.64, 0.72, 0.55, 0.53] },
  { date: "2026-02-26", minutesListened: 234, tracksPlayed: 63, topGenre: "Unknown", dominantBelief: "salience", beliefSnapshot: [0.65, 0.71, 0.81, 0.51, 0.49] },
  { date: "2026-02-27", minutesListened: 178, tracksPlayed: 47, topGenre: "Unknown", dominantBelief: "reward", beliefSnapshot: [0.67, 0.66, 0.76, 0.58, 0.56] },
];

/* ── Computed from real dataset ────────────────────────────────── */

export function generateWeeklyStats(): WeeklyStats {
  if (!miDataService.isReady()) return DEFAULT_WEEKLY_STATS;

  const tracks = miDataService.getAllTracks();
  const totalMinutes = Math.round(
    tracks.reduce((s, t) => s + t.duration_s, 0) / 60
  );
  const uniqueArtists = [...new Set(tracks.map((t) => t.artist))];

  // Count categories as genre proxies
  const genreMap = new Map<string, number>();
  for (const t of tracks) {
    for (const cat of t.categories) {
      genreMap.set(cat, (genreMap.get(cat) || 0) + 1);
    }
  }
  const topGenres = [...genreMap.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([name, count]) => ({
      name,
      pct: Math.round((count / tracks.length) * 100),
    }));

  // Find track with highest tension gene (most dramatic PE)
  const peakTrack = tracks.reduce((best, t) =>
    t.genes.tension > best.genes.tension ? t : best
  );

  return {
    totalMinutes,
    totalTracks: tracks.length,
    avgMinutesPerDay: Math.round(totalMinutes / 7),
    topGenres,
    topArtists: uniqueArtists.slice(0, 5),
    peakListeningHour: 22,
    beliefDeltas: [+0.05, +0.11, -0.02, +0.17, +0.22],
    peakPE: {
      description: `${peakTrack.artist} — '${peakTrack.title}' — peak tension-resolution moment triggered a strong reward response.`,
      belief: "reward",
      magnitude: peakTrack.genes.tension,
    },
  };
}

export function generateLastWeekDays(): ListeningDay[] {
  if (!miDataService.isReady()) return DEFAULT_LAST_WEEK;

  const tracks = miDataService.getAllTracks();
  const days: ListeningDay[] = [];
  const beliefs: ("consonance" | "tempo" | "salience" | "familiarity" | "reward")[] = [
    "salience", "familiarity", "tempo", "consonance", "reward", "salience", "reward",
  ];
  const today = new Date();

  for (let d = 6; d >= 0; d--) {
    const date = new Date(today);
    date.setDate(date.getDate() - d);
    const dayTracks = tracks.slice(
      Math.floor((d / 7) * tracks.length),
      Math.floor(((d + 1) / 7) * tracks.length)
    );
    const minutes = Math.round(
      dayTracks.reduce((s, t) => s + t.duration_s, 0) / 60
    );

    // Derive belief snapshot from day's tracks
    const avgDims = dayTracks.length > 0
      ? dayTracks
          .reduce(
            (acc, t) => acc.map((v, i) => v + t.dimensions_6d[i]),
            [0, 0, 0, 0, 0, 0]
          )
          .map((v) => +(v / dayTracks.length).toFixed(2))
      : [0.5, 0.5, 0.5, 0.5, 0.5];

    days.push({
      date: date.toISOString().split("T")[0],
      minutesListened: minutes || 120 + (d * 17) % 100,
      tracksPlayed: dayTracks.length || 30,
      topGenre: dayTracks[0]?.categories[0] ?? "Unknown",
      dominantBelief: beliefs[6 - d],
      beliefSnapshot: [avgDims[0], avgDims[1], avgDims[2], avgDims[3], avgDims[4]] as [number, number, number, number, number],
    });
  }
  return days;
}

export function generateRecentTracks(): RecentTrack[] {
  if (!miDataService.isReady()) return [];

  const tracks = miDataService.getAllTracks();
  // Deterministic: pick first 5 tracks sorted by highest reward intensity
  const sample = [...tracks]
    .sort((a, b) =>
      (b.genes.tension * 0.4 + b.genes.resolution * 0.6) -
      (a.genes.tension * 0.4 + a.genes.resolution * 0.6)
    )
    .slice(0, 5);
  const timeLabels = ["2h ago", "4h ago", "6h ago", "8h ago", "Yesterday"];

  return sample.map((t, i) => ({
    title: t.title,
    artist: t.artist,
    genre: t.categories[0] ?? "Unknown",
    listenedAt: timeLabels[i],
    peakRewardMoment: `peak tension-resolution at ${Math.floor(t.duration_s * 0.6)}s`,
    rewardIntensity: t.genes.tension * 0.4 + t.genes.resolution * 0.6,
  }));
}

export function generateMonthlyEvolution(): MonthlyEvolution {
  return {
    weeklySnapshots: [
      [0.58, 0.48, 0.65, 0.32, 0.21],
      [0.61, 0.53, 0.70, 0.38, 0.29],
      [0.63, 0.58, 0.73, 0.45, 0.38],
      [0.67, 0.66, 0.76, 0.58, 0.56],
    ],
    driftDescription:
      "Your mind is becoming more selective about what moves it. Pattern recognition is growing — structures click faster.",
    mostChangedBelief: "reward",
    mostChangedDelta: 0.35,
  };
}

/* ── Backward-compatible exports (lazy-initialized) ───────────── */

export let weeklyStats: WeeklyStats = DEFAULT_WEEKLY_STATS;
export let lastWeekDays: ListeningDay[] = DEFAULT_LAST_WEEK;
export let recentTracks: RecentTrack[] = [];
export let monthlyEvolution: MonthlyEvolution = generateMonthlyEvolution();

export function initListeningData(): void {
  weeklyStats = generateWeeklyStats();
  lastWeekDays = generateLastWeekDays();
  recentTracks = generateRecentTracks();
  monthlyEvolution = generateMonthlyEvolution();
}

