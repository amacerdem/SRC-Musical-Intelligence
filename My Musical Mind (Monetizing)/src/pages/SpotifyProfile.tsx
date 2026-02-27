/**
 * Spotify Profile — "Your Spotify DNA"
 *
 * Displays real Spotify data (top tracks, recently played, saved tracks,
 * currently playing) in M³'s cinematic glass aesthetic.
 */
import { useEffect, useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Music2,
  Clock,
  Heart,
  Disc3,
  Headphones,
  LogOut,
  RefreshCw,
  Loader2,
  Pause,
  Play,
} from "lucide-react";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
} from "recharts";
import { SpotifyService } from "@/services/spotify";
import type { MockTrack } from "@/services/SpotifySimulator";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import {
  pageTransition,
  staggerChildren,
  slideUp,
  cinematicReveal,
  floatGentle,
} from "@/design/animations";

/* ── Constants ─────────────────────────────────────────────────── */

const SPOTIFY_GREEN = "#1DB954";

const FAMILY_COLORS: Record<string, string> = {
  Alchemists: "#A855F7",
  Architects: "#38BDF8",
  Explorers: "#84CC16",
  Anchors: "#F43F5E",
  Kineticists: "#F97316",
};

const FEATURE_COLORS: Record<string, string> = {
  energy: "#EF4444",
  valence: "#FBBF24",
  danceability: "#F97316",
  acousticness: "#38BDF8",
  harmonicComplexity: "#A855F7",
  timbralBrightness: "#84CC16",
};

const FEATURE_LABELS: Record<string, string> = {
  energy: "Energy",
  valence: "Valence",
  danceability: "Danceability",
  acousticness: "Acousticness",
  harmonicComplexity: "Harmonic",
  timbralBrightness: "Brightness",
};

type TimeRange = "short_term" | "medium_term" | "long_term";
const TIME_TABS: { key: TimeRange; label: string }[] = [
  { key: "short_term", label: "4 Weeks" },
  { key: "medium_term", label: "6 Months" },
  { key: "long_term", label: "All Time" },
];

const ease = [0.22, 1, 0.36, 1];

/* ── Helpers ───────────────────────────────────────────────────── */

function formatDuration(sec: number) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

function averageFeatures(tracks: MockTrack[]) {
  if (tracks.length === 0) return [];
  const keys = ["energy", "valence", "danceability", "acousticness", "harmonicComplexity", "timbralBrightness"] as const;
  return keys.map((k) => ({
    feature: FEATURE_LABELS[k],
    value: +(tracks.reduce((sum, t) => sum + t.features[k], 0) / tracks.length).toFixed(3),
    fullMark: 1,
    color: FEATURE_COLORS[k],
  }));
}

function familyDistribution(tracks: MockTrack[]) {
  const counts: Record<string, number> = {};
  for (const t of tracks) {
    counts[t.dominantFamily] = (counts[t.dominantFamily] || 0) + 1;
  }
  return Object.entries(counts)
    .map(([name, count]) => ({ name, count, color: FAMILY_COLORS[name] || "#6366F1" }))
    .sort((a, b) => b.count - a.count);
}

/* ── Track Row Component ───────────────────────────────────────── */

function TrackRow({ track, index, compact = false }: { track: MockTrack; index: number; compact?: boolean }) {
  const familyColor = FAMILY_COLORS[track.dominantFamily] || "#6366F1";

  return (
    <motion.div
      variants={slideUp}
      className="flex items-center gap-3 py-2 px-3 rounded-xl transition-all duration-300 hover:bg-white/[0.04] group"
    >
      <span className="w-5 text-right text-xs font-mono text-slate-600 shrink-0">
        {index + 1}
      </span>

      {!compact && track.albumArt && (
        <img
          src={track.albumArt}
          alt=""
          className="w-10 h-10 rounded-lg object-cover shrink-0"
          loading="lazy"
        />
      )}

      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-slate-200 truncate group-hover:text-white transition-colors">
          {track.name}
        </p>
        <p className="text-xs text-slate-500 truncate">{track.artist}</p>
      </div>

      <div
        className="w-2 h-2 rounded-full shrink-0"
        style={{ backgroundColor: familyColor, boxShadow: `0 0 6px ${familyColor}40` }}
        title={track.dominantFamily}
      />

      {!compact && (
        <Badge label={track.genre} color={familyColor} size="sm" />
      )}

      <span className="text-xs font-mono text-slate-600 shrink-0 w-10 text-right">
        {formatDuration(track.durationSec)}
      </span>
    </motion.div>
  );
}

/* ── Currently Playing Section ─────────────────────────────────── */

function NowPlayingSection({ track }: { track: MockTrack | null }) {
  if (!track) {
    return (
      <Card className="text-center py-8">
        <Pause size={28} className="mx-auto mb-3 text-slate-600" />
        <p className="text-sm text-slate-500 font-display">Nothing playing right now</p>
        <p className="text-xs text-slate-700 mt-1">Play something on Spotify to see it here</p>
      </Card>
    );
  }

  return (
    <motion.div
      variants={floatGentle}
      animate="animate"
      className="relative overflow-hidden rounded-2xl"
      style={{
        background: "rgba(0,0,0,0.5)",
        backdropFilter: "blur(12px)",
        border: "1px solid rgba(255,255,255,0.07)",
      }}
    >
      {/* Spotify green glow */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `radial-gradient(ellipse at 30% 50%, ${SPOTIFY_GREEN}12, transparent 60%)`,
        }}
      />

      <div className="relative flex items-center gap-5 p-5">
        {track.albumArt && (
          <motion.img
            src={track.albumArt}
            alt=""
            className="w-20 h-20 rounded-xl object-cover shadow-2xl"
            animate={{
              boxShadow: [
                `0 0 20px ${SPOTIFY_GREEN}20`,
                `0 0 40px ${SPOTIFY_GREEN}35`,
                `0 0 20px ${SPOTIFY_GREEN}20`,
              ],
            }}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
          />
        )}

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <div className="flex gap-[2px]">
              {[0, 1, 2, 3].map((i) => (
                <motion.div
                  key={i}
                  className="w-[3px] rounded-full"
                  style={{ backgroundColor: SPOTIFY_GREEN, originY: 1 }}
                  animate={{ scaleY: [0.3, 1, 0.3] }}
                  transition={{
                    duration: 0.6 + i * 0.1,
                    repeat: Infinity,
                    ease: "easeInOut",
                    delay: i * 0.15,
                  }}
                >
                  <div className="h-3" />
                </motion.div>
              ))}
            </div>
            <span className="text-[10px] uppercase tracking-[0.2em] font-medium" style={{ color: SPOTIFY_GREEN }}>
              Now Playing
            </span>
          </div>

          <p className="text-lg font-display font-bold text-white truncate">{track.name}</p>
          <p className="text-sm text-slate-400 truncate">{track.artist}</p>
        </div>

        <div className="text-right shrink-0">
          <Badge label={track.genre} color={SPOTIFY_GREEN} />
          <p className="text-xs font-mono text-slate-600 mt-2">{formatDuration(track.durationSec)}</p>
        </div>
      </div>
    </motion.div>
  );
}

/* ── Feature Bar Chart ─────────────────────────────────────────── */

function FeatureBarRow({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-[10px] text-slate-500 w-20 text-right shrink-0">{label}</span>
      <div className="flex-1 h-1.5 rounded-full bg-white/[0.04] overflow-hidden">
        <motion.div
          className="h-full rounded-full"
          style={{ backgroundColor: color }}
          initial={{ width: 0 }}
          animate={{ width: `${value * 100}%` }}
          transition={{ duration: 1, ease }}
        />
      </div>
      <span className="text-[10px] font-mono text-slate-600 w-8 shrink-0">{(value * 100).toFixed(0)}%</span>
    </div>
  );
}

/* ── Main Page ─────────────────────────────────────────────────── */

export function SpotifyProfile() {
  const [timeRange, setTimeRange] = useState<TimeRange>("medium_term");
  const [topTracks, setTopTracks] = useState<MockTrack[]>([]);
  const [recentTracks, setRecentTracks] = useState<MockTrack[]>([]);
  const [savedTracks, setSavedTracks] = useState<MockTrack[]>([]);
  const [currentTrack, setCurrentTrack] = useState<MockTrack | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  // Fetch data
  const fetchAll = async (range: TimeRange) => {
    setLoading(true);
    try {
      const [top, recent, saved, current] = await Promise.all([
        SpotifyService.getTopTracks(range, 50),
        SpotifyService.getRecentlyPlayed(20),
        SpotifyService.getSavedTracks(50),
        SpotifyService.getCurrentlyPlaying(),
      ]);
      setTopTracks(top);
      setRecentTracks(recent);
      setSavedTracks(saved);
      setCurrentTrack(current);
    } catch (err) {
      console.error("Spotify fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAll(timeRange);
  }, [timeRange]);

  // Poll currently playing every 30s
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const current = await SpotifyService.getCurrentlyPlaying();
        setCurrentTrack(current);
      } catch { /* silent */ }
    }, 30_000);
    return () => clearInterval(interval);
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchAll(timeRange);
    setRefreshing(false);
  };

  const handleDisconnect = () => {
    SpotifyService.clearTokens();
    window.location.href = "/";
  };

  // Computed data
  const radarData = useMemo(() => averageFeatures(topTracks), [topTracks]);
  const familyDist = useMemo(() => familyDistribution(topTracks), [topTracks]);
  const topGenres = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const t of topTracks) {
      if (t.genre && t.genre !== "Unknown") {
        counts[t.genre] = (counts[t.genre] || 0) + 1;
      }
    }
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([genre, count]) => ({ genre, count }));
  }, [topTracks]);

  if (loading && topTracks.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <Loader2 size={32} className="animate-spin mx-auto mb-3" style={{ color: SPOTIFY_GREEN }} />
          <p className="text-sm text-slate-500 font-display">Loading your Spotify DNA...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <motion.div {...pageTransition} className="pb-32">
      {/* ── Header ──────────────────────────────────────────────── */}
      <motion.header
        variants={cinematicReveal}
        initial="initial"
        animate="animate"
        className="flex items-center justify-between mb-8"
      >
        <div className="flex items-center gap-3">
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center"
            style={{ background: `${SPOTIFY_GREEN}15`, border: `1px solid ${SPOTIFY_GREEN}25` }}
          >
            <Headphones size={20} style={{ color: SPOTIFY_GREEN }} />
          </div>
          <div>
            <h1 className="text-xl font-display font-bold text-white">Your Spotify DNA</h1>
            <p className="text-xs text-slate-500">Powered by your listening history</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={handleRefresh} disabled={refreshing}>
            <RefreshCw size={14} className={refreshing ? "animate-spin" : ""} />
          </Button>
          <Button variant="ghost" size="sm" onClick={handleDisconnect}>
            <LogOut size={14} />
          </Button>
        </div>
      </motion.header>

      {/* ── Currently Playing ───────────────────────────────────── */}
      <motion.section variants={slideUp} initial="initial" animate="animate" className="mb-8">
        <NowPlayingSection track={currentTrack} />
      </motion.section>

      {/* ── Top Tracks ──────────────────────────────────────────── */}
      <motion.section variants={slideUp} initial="initial" animate="animate" className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Music2 size={16} className="text-slate-500" />
            <h2 className="text-sm font-display font-semibold text-slate-300 uppercase tracking-wider">
              Top Tracks
            </h2>
            <span className="text-xs font-mono text-slate-600">{topTracks.length}</span>
          </div>

          {/* Time range tabs */}
          <div className="flex gap-1 p-0.5 rounded-full" style={{ background: "rgba(255,255,255,0.04)" }}>
            {TIME_TABS.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setTimeRange(tab.key)}
                className="relative px-3 py-1 text-xs font-medium rounded-full transition-all duration-300"
                style={{
                  color: timeRange === tab.key ? "#fff" : "#64748B",
                  background: timeRange === tab.key ? `${SPOTIFY_GREEN}20` : "transparent",
                  border: timeRange === tab.key ? `1px solid ${SPOTIFY_GREEN}30` : "1px solid transparent",
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <Card>
          <AnimatePresence mode="wait">
            <motion.div
              key={timeRange}
              variants={staggerChildren}
              initial="initial"
              animate="animate"
              exit={{ opacity: 0 }}
              className="space-y-0.5"
            >
              {topTracks.slice(0, 25).map((track, i) => (
                <TrackRow key={track.id} track={track} index={i} />
              ))}
              {topTracks.length === 0 && (
                <p className="text-center text-sm text-slate-600 py-6">No top tracks found for this period</p>
              )}
            </motion.div>
          </AnimatePresence>
        </Card>
      </motion.section>

      {/* ── Two-Column: Recently Played + Saved ─────────────────── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        {/* Recently Played */}
        <motion.section variants={slideUp} initial="initial" animate="animate">
          <div className="flex items-center gap-2 mb-3">
            <Clock size={14} className="text-slate-500" />
            <h2 className="text-sm font-display font-semibold text-slate-300 uppercase tracking-wider">
              Recently Played
            </h2>
            <span className="text-xs font-mono text-slate-600">{recentTracks.length}</span>
          </div>

          <Card className="max-h-[420px] overflow-y-auto">
            <motion.div variants={staggerChildren} initial="initial" animate="animate" className="space-y-0.5">
              {recentTracks.map((track, i) => (
                <TrackRow key={`${track.id}-${i}`} track={track} index={i} compact />
              ))}
              {recentTracks.length === 0 && (
                <p className="text-center text-sm text-slate-600 py-6">No recent tracks</p>
              )}
            </motion.div>
          </Card>
        </motion.section>

        {/* Saved Tracks */}
        <motion.section variants={slideUp} initial="initial" animate="animate">
          <div className="flex items-center gap-2 mb-3">
            <Heart size={14} className="text-slate-500" />
            <h2 className="text-sm font-display font-semibold text-slate-300 uppercase tracking-wider">
              Saved Tracks
            </h2>
            <span className="text-xs font-mono text-slate-600">{savedTracks.length}</span>
          </div>

          <Card className="max-h-[420px] overflow-y-auto">
            <motion.div variants={staggerChildren} initial="initial" animate="animate" className="space-y-0.5">
              {savedTracks.map((track, i) => (
                <TrackRow key={track.id} track={track} index={i} compact />
              ))}
              {savedTracks.length === 0 && (
                <p className="text-center text-sm text-slate-600 py-6">No saved tracks</p>
              )}
            </motion.div>
          </Card>
        </motion.section>
      </div>

      {/* ── Audio DNA Section ───────────────────────────────────── */}
      <motion.section variants={slideUp} initial="initial" animate="animate" className="mb-8">
        <div className="flex items-center gap-2 mb-4">
          <Disc3 size={16} className="text-slate-500" />
          <h2 className="text-sm font-display font-semibold text-slate-300 uppercase tracking-wider">
            Audio DNA
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Radar Chart */}
          <Card className="md:col-span-1">
            <p className="hud-label mb-3">Average Features</p>
            {radarData.length > 0 ? (
              <ResponsiveContainer width="100%" height={220}>
                <RadarChart data={radarData} cx="50%" cy="50%" outerRadius="72%">
                  <PolarGrid stroke="rgba(255,255,255,0.06)" />
                  <PolarAngleAxis
                    dataKey="feature"
                    tick={{ fill: "#64748B", fontSize: 10 }}
                    tickLine={false}
                  />
                  <Radar
                    name="Audio DNA"
                    dataKey="value"
                    stroke={SPOTIFY_GREEN}
                    fill={SPOTIFY_GREEN}
                    fillOpacity={0.15}
                    strokeWidth={1.5}
                  />
                </RadarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[220px] flex items-center justify-center text-xs text-slate-600">
                No data
              </div>
            )}
          </Card>

          {/* Feature Bars */}
          <Card className="md:col-span-1">
            <p className="hud-label mb-4">Feature Breakdown</p>
            <div className="space-y-3">
              {radarData.map((d) => (
                <FeatureBarRow key={d.feature} label={d.feature} value={d.value} color={d.color} />
              ))}
            </div>
          </Card>

          {/* Neural Family Distribution + Top Genres */}
          <Card className="md:col-span-1">
            <p className="hud-label mb-4">Neural Family Mix</p>
            <div className="space-y-2 mb-6">
              {familyDist.map((f) => (
                <div key={f.name} className="flex items-center gap-2">
                  <div
                    className="w-2.5 h-2.5 rounded-full shrink-0"
                    style={{ backgroundColor: f.color, boxShadow: `0 0 8px ${f.color}40` }}
                  />
                  <span className="text-xs text-slate-400 flex-1">{f.name}</span>
                  <span className="text-xs font-mono text-slate-500">{f.count}</span>
                  <div className="w-16 h-1 rounded-full bg-white/[0.04] overflow-hidden">
                    <motion.div
                      className="h-full rounded-full"
                      style={{ backgroundColor: f.color }}
                      initial={{ width: 0 }}
                      animate={{ width: `${(f.count / topTracks.length) * 100}%` }}
                      transition={{ duration: 0.8, ease }}
                    />
                  </div>
                </div>
              ))}
            </div>

            <p className="hud-label mb-3">Top Genres</p>
            <div className="flex flex-wrap gap-1.5">
              {topGenres.map((g) => (
                <Badge key={g.genre} label={`${g.genre} (${g.count})`} color={SPOTIFY_GREEN} size="sm" />
              ))}
              {topGenres.length === 0 && (
                <span className="text-xs text-slate-600">No genre data</span>
              )}
            </div>
          </Card>
        </div>
      </motion.section>

      {/* ── Stats Summary ───────────────────────────────────────── */}
      <motion.section variants={slideUp} initial="initial" animate="animate">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { label: "Top Tracks", value: topTracks.length, icon: Music2 },
            { label: "Recent", value: recentTracks.length, icon: Clock },
            { label: "Saved", value: savedTracks.length, icon: Heart },
            {
              label: "Avg Tempo",
              value: topTracks.length > 0
                ? `${Math.round(topTracks.reduce((s, t) => s + t.features.tempo, 0) / topTracks.length)} BPM`
                : "—",
              icon: Disc3,
            },
          ].map((stat) => (
            <Card key={stat.label} className="text-center py-4">
              <stat.icon size={16} className="mx-auto mb-2 text-slate-600" />
              <p className="text-lg font-display font-bold text-white">
                {stat.value}
              </p>
              <p className="hud-label mt-1">{stat.label}</p>
            </Card>
          ))}
        </div>
      </motion.section>
    </motion.div>
  );
}
