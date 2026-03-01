/**
 * Listen — Main listening hub with full Spotify integration.
 *
 * Shows persona character, currently playing with real controls,
 * queue, top tracks/artists, playlists, audio DNA, user profile.
 */
import { useEffect, useState, useMemo, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";
import {
  Music2,
  Clock,
  Heart,
  ListMusic,
  Loader2,
  Pause,
  Play,
  SkipForward,
  SkipBack,
  Shuffle,
  Repeat,
  Repeat1,
  Volume2,
  VolumeX,
  ExternalLink,
  Mic2,
  Disc3,
  TrendingUp,
  Library,
  RefreshCw,
} from "lucide-react";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
} from "recharts";
import { SpotifyService } from "@/services/spotify";
import type {
  PlaybackState,
  SpotifyUserProfile,
  SpotifyArtistInfo,
  SpotifyPlaylistInfo,
} from "@/services/spotify";
import type { MockTrack } from "@/services/SpotifySimulator";
import { SpotifySimulator } from "@/services/SpotifySimulator";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { useUserStore } from "@/stores/useUserStore";
import { useM3Store } from "@/stores/useM3Store";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { getPersona } from "@/data/personas";
import { CharacterAvatar } from "@/svg/characters/CharacterAvatar";
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
  danceability: "Dance",
  acousticness: "Acoustic",
  harmonicComplexity: "Harmonic",
  timbralBrightness: "Brightness",
};

type TimeRange = "short_term" | "medium_term" | "long_term";
const TIME_TABS: { key: TimeRange; labelEn: string; labelTr: string }[] = [
  { key: "short_term", labelEn: "4 Weeks", labelTr: "4 Hafta" },
  { key: "medium_term", labelEn: "6 Months", labelTr: "6 Ay" },
  { key: "long_term", labelEn: "All Time", labelTr: "Tüm Zamanlar" },
];

const ease = [0.22, 1, 0.36, 1] as const;

/* ── Helpers ───────────────────────────────────────────────────── */

function formatDuration(sec: number) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

function formatFollowers(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return String(n);
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
  for (const t of tracks) counts[t.dominantFamily] = (counts[t.dominantFamily] || 0) + 1;
  return Object.entries(counts)
    .map(([name, count]) => ({ name, count, color: FAMILY_COLORS[name] || "#6366F1" }))
    .sort((a, b) => b.count - a.count);
}

/* ── Spotify Logo ──────────────────────────────────────────────── */

function SpotifyLogo({ size = 20 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={SPOTIFY_GREEN}>
      <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z" />
    </svg>
  );
}

/* ── Equalizer Bars ────────────────────────────────────────────── */

function EqualizerBars({ color = SPOTIFY_GREEN, count = 5 }: { color?: string; count?: number }) {
  return (
    <div className="flex gap-[3px] items-end">
      {Array.from({ length: count }, (_, i) => (
        <motion.div
          key={i}
          className="w-[3px] rounded-full"
          style={{ backgroundColor: color, originY: 1 }}
          animate={{ scaleY: [0.2, 1, 0.3, 0.8, 0.2] }}
          transition={{ duration: 0.8 + i * 0.15, repeat: Infinity, ease: "easeInOut", delay: i * 0.1 }}
        >
          <div className="h-5" />
        </motion.div>
      ))}
    </div>
  );
}

/* ── Feature Bar Row ───────────────────────────────────────────── */

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

/* ── Now Playing Hero ──────────────────────────────────────────── */

interface NowPlayingProps {
  track: MockTrack | null;
  accentColor: string;
  isPlaying: boolean;
  shuffleOn: boolean;
  repeatMode: "off" | "track" | "context";
  progressMs: number;
  durationMs: number;
  volume: number;
  onPlayPause: () => void;
  onNext: () => void;
  onPrev: () => void;
  onShuffle: () => void;
  onRepeat: () => void;
  onSeek: (ms: number) => void;
  onVolume: (pct: number) => void;
  connected: boolean;
}

function NowPlayingHero({
  track, accentColor, isPlaying, shuffleOn, repeatMode,
  progressMs, durationMs, volume,
  onPlayPause, onNext, onPrev, onShuffle, onRepeat, onSeek, onVolume,
  connected,
}: NowPlayingProps) {
  if (!track) {
    return (
      <Card className="text-center py-12">
        <Pause size={36} className="mx-auto mb-4 text-slate-600" />
        <p className="text-base text-slate-400 font-display">Nothing playing right now</p>
        <p className="text-xs text-slate-600 mt-2">Play something on Spotify to see it here</p>
      </Card>
    );
  }

  const familyColor = FAMILY_COLORS[track.dominantFamily] || "#6366F1";
  const progressPct = durationMs > 0 ? (progressMs / durationMs) * 100 : 0;
  const RepeatIcon = repeatMode === "track" ? Repeat1 : Repeat;

  return (
    <motion.div
      variants={floatGentle}
      animate="animate"
      className="relative overflow-hidden rounded-2xl"
      style={{
        background: "rgba(0,0,0,0.5)",
        backdropFilter: "blur(16px)",
        border: "1px solid rgba(255,255,255,0.08)",
      }}
    >
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `radial-gradient(ellipse at 20% 50%, ${accentColor}15, transparent 50%), radial-gradient(ellipse at 80% 80%, ${SPOTIFY_GREEN}08, transparent 50%)`,
        }}
      />

      <div className="relative flex items-center gap-6 p-6 md:p-8">
        {track.albumArt ? (
          <motion.img
            src={track.albumArt}
            alt=""
            className="w-28 h-28 md:w-36 md:h-36 rounded-2xl object-cover shadow-2xl flex-shrink-0"
            animate={{
              boxShadow: isPlaying
                ? [`0 0 20px ${accentColor}20, 0 8px 32px rgba(0,0,0,0.5)`, `0 0 40px ${accentColor}35, 0 8px 32px rgba(0,0,0,0.5)`, `0 0 20px ${accentColor}20, 0 8px 32px rgba(0,0,0,0.5)`]
                : `0 0 12px ${accentColor}10, 0 8px 32px rgba(0,0,0,0.5)`,
            }}
            transition={{ duration: 4, repeat: isPlaying ? Infinity : 0, ease: "easeInOut" }}
          />
        ) : (
          <div className="w-28 h-28 md:w-36 md:h-36 rounded-2xl flex items-center justify-center flex-shrink-0" style={{ background: `${SPOTIFY_GREEN}15` }}>
            <Music2 size={48} className="text-slate-600" />
          </div>
        )}

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2.5 mb-3">
            {isPlaying ? <EqualizerBars color={accentColor} /> : (
              <div className="flex gap-[3px] items-end">
                {Array.from({ length: 5 }, (_, i) => (
                  <div key={i} className="w-[3px] h-2 rounded-full" style={{ backgroundColor: `${accentColor}40` }} />
                ))}
              </div>
            )}
            <span className="text-[11px] uppercase tracking-[0.2em] font-display font-medium" style={{ color: isPlaying ? SPOTIFY_GREEN : "#64748B" }}>
              {isPlaying ? "Now Playing" : "Paused"}
            </span>
          </div>

          <h2 className="text-2xl md:text-3xl font-display font-bold text-white truncate mb-1">{track.name}</h2>
          <p className="text-base text-slate-400 truncate mb-4">{track.artist}</p>

          <div className="mb-4">
            <div
              className="h-1.5 rounded-full bg-white/[0.08] overflow-hidden cursor-pointer"
              onClick={(e) => {
                if (!connected) return;
                const rect = e.currentTarget.getBoundingClientRect();
                onSeek(Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width)) * durationMs);
              }}
            >
              <div className="h-full rounded-full transition-all duration-300" style={{ width: `${progressPct}%`, background: `linear-gradient(90deg, ${accentColor}, ${SPOTIFY_GREEN})` }} />
            </div>
            <div className="flex justify-between mt-1.5">
              <span className="text-[10px] font-mono text-slate-600">{formatDuration(Math.floor(progressMs / 1000))}</span>
              <span className="text-[10px] font-mono text-slate-600">{formatDuration(Math.floor(durationMs / 1000))}</span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <button onClick={onShuffle} disabled={!connected} className={`transition-colors ${connected ? "hover:text-white" : "opacity-40 cursor-default"}`} style={{ color: shuffleOn ? accentColor : "#64748B" }}><Shuffle size={16} /></button>
            <button onClick={onPrev} disabled={!connected} className={`text-slate-400 transition-colors ${connected ? "hover:text-white active:scale-90" : "opacity-40 cursor-default"}`}><SkipBack size={18} /></button>
            <button
              onClick={onPlayPause} disabled={!connected}
              className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${connected ? "hover:scale-105 active:scale-95" : "opacity-60 cursor-default"}`}
              style={{ background: `linear-gradient(135deg, ${accentColor}, ${SPOTIFY_GREEN})`, boxShadow: isPlaying ? `0 0 20px ${accentColor}40` : `0 0 12px ${accentColor}20` }}
            >
              {isPlaying ? <Pause size={22} className="text-white" /> : <Play size={22} className="text-white ml-0.5" />}
            </button>
            <button onClick={onNext} disabled={!connected} className={`text-slate-400 transition-colors ${connected ? "hover:text-white active:scale-90" : "opacity-40 cursor-default"}`}><SkipForward size={18} /></button>
            <button onClick={onRepeat} disabled={!connected} className={`transition-colors ${connected ? "hover:text-white" : "opacity-40 cursor-default"}`} style={{ color: repeatMode !== "off" ? accentColor : "#64748B" }}><RepeatIcon size={16} /></button>
            <div className="ml-auto flex items-center gap-2">
              <button onClick={() => onVolume(volume > 0 ? 0 : 70)} disabled={!connected} className="text-slate-600 hover:text-slate-300 transition-colors">
                {volume === 0 ? <VolumeX size={14} /> : <Volume2 size={14} />}
              </button>
              <div
                className="w-20 h-1.5 rounded-full bg-white/[0.08] overflow-hidden cursor-pointer"
                onClick={(e) => { if (!connected) return; const rect = e.currentTarget.getBoundingClientRect(); onVolume(Math.max(0, Math.min(100, ((e.clientX - rect.left) / rect.width) * 100))); }}
              >
                <div className="h-full rounded-full transition-all duration-200" style={{ width: `${volume}%`, background: `${accentColor}80` }} />
              </div>
            </div>
          </div>
        </div>

        <div className="hidden md:flex flex-col items-end gap-2 self-start flex-shrink-0">
          <Badge label={track.genre} color={familyColor} />
          <Badge label={track.dominantFamily} color={familyColor} size="sm" />
          <div className="flex items-center gap-1.5 mt-2">
            <SpotifyLogo size={16} />
            <span className="text-[10px] text-slate-600 font-mono">Spotify</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

/* ── Track Row ─────────────────────────────────────────────────── */

function TrackRow({ track, index, compact = false }: { track: MockTrack; index: number; compact?: boolean }) {
  const familyColor = FAMILY_COLORS[track.dominantFamily] || "#6366F1";
  return (
    <motion.div variants={slideUp} className="flex items-center gap-3 py-2 px-3 rounded-xl transition-all duration-300 hover:bg-white/[0.04] group">
      <span className="w-5 text-right text-xs font-mono text-slate-600 shrink-0">{index + 1}</span>
      {!compact && track.albumArt && <img src={track.albumArt} alt="" className="w-10 h-10 rounded-lg object-cover shrink-0" loading="lazy" />}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-slate-200 truncate group-hover:text-white transition-colors">{track.name}</p>
        <p className="text-xs text-slate-500 truncate">{track.artist}</p>
      </div>
      <div className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: familyColor, boxShadow: `0 0 6px ${familyColor}40` }} title={track.dominantFamily} />
      {!compact && <Badge label={track.genre} color={familyColor} size="sm" />}
      <span className="text-xs font-mono text-slate-600 shrink-0 w-10 text-right">{formatDuration(track.durationSec)}</span>
    </motion.div>
  );
}

/* ── Artist Card ───────────────────────────────────────────────── */

function ArtistCard({ artist, index }: { artist: SpotifyArtistInfo; index: number }) {
  const familyColor = FAMILY_COLORS[artist.family] || "#6366F1";
  return (
    <motion.div variants={slideUp} className="flex items-center gap-3 py-2 px-3 rounded-xl transition-all duration-300 hover:bg-white/[0.04] group">
      <span className="w-5 text-right text-xs font-mono text-slate-600 shrink-0">{index + 1}</span>
      {artist.image ? (
        <img src={artist.image} alt="" className="w-10 h-10 rounded-full object-cover shrink-0" loading="lazy" />
      ) : (
        <div className="w-10 h-10 rounded-full bg-white/[0.06] flex items-center justify-center shrink-0">
          <Mic2 size={14} className="text-slate-600" />
        </div>
      )}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-slate-200 truncate group-hover:text-white transition-colors">{artist.name}</p>
        <p className="text-xs text-slate-500 truncate">{artist.genres.slice(0, 3).join(", ") || "—"}</p>
      </div>
      <Badge label={artist.family} color={familyColor} size="sm" />
      <span className="text-[10px] font-mono text-slate-600 shrink-0">{formatFollowers(artist.followers)}</span>
    </motion.div>
  );
}

/* ── Playlist Card ─────────────────────────────────────────────── */

function PlaylistCard({ playlist }: { playlist: SpotifyPlaylistInfo }) {
  return (
    <motion.div variants={slideUp} className="flex items-center gap-3 py-2 px-3 rounded-xl transition-all duration-300 hover:bg-white/[0.04] group">
      {playlist.image ? (
        <img src={playlist.image} alt="" className="w-12 h-12 rounded-lg object-cover shrink-0" loading="lazy" />
      ) : (
        <div className="w-12 h-12 rounded-lg bg-white/[0.06] flex items-center justify-center shrink-0">
          <ListMusic size={16} className="text-slate-600" />
        </div>
      )}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-slate-200 truncate group-hover:text-white transition-colors">{playlist.name}</p>
        <p className="text-xs text-slate-500 truncate">{playlist.owner} · {playlist.trackCount} tracks</p>
      </div>
      {playlist.isPublic && <Badge label="Public" color={SPOTIFY_GREEN} size="sm" />}
    </motion.div>
  );
}

/* ══════════════════════════════════════════════════════════════════
   ██  MAIN LISTEN PAGE
   ══════════════════════════════════════════════════════════════════ */

export function Listen() {
  const { t, i18n } = useTranslation();
  const isTr = i18n.language === "tr";
  const { mind } = useUserStore();
  const m3Mind = useM3Store((s) => s.mind);
  const identity = useActiveIdentity();
  const activePersonaId = m3Mind?.activePersonaId ?? mind?.personaId;
  const persona = activePersonaId ? getPersona(activePersonaId) : null;
  const personaLevel = m3Mind?.level ?? 1;
  const color = identity.color;

  // Data state
  const [currentTrack, setCurrentTrack] = useState<MockTrack | null>(null);
  const [recentTracks, setRecentTracks] = useState<MockTrack[]>([]);
  const [savedTracks, setSavedTracks] = useState<MockTrack[]>([]);
  const [topTracks, setTopTracks] = useState<MockTrack[]>([]);
  const [topArtists, setTopArtists] = useState<SpotifyArtistInfo[]>([]);
  const [playlists, setPlaylists] = useState<SpotifyPlaylistInfo[]>([]);
  const [queueTracks, setQueueTracks] = useState<MockTrack[]>([]);
  const [userProfile, setUserProfile] = useState<SpotifyUserProfile | null>(null);
  const [timeRange, setTimeRange] = useState<TimeRange>("medium_term");
  const [loading, setLoading] = useState(true);
  const [isSpotifyConnected, setIsSpotifyConnected] = useState(false);
  const [needsReauth, setNeedsReauth] = useState(false);

  // Playback state
  const [isPlaying, setIsPlaying] = useState(false);
  const [shuffleOn, setShuffleOn] = useState(false);
  const [repeatMode, setRepeatMode] = useState<"off" | "track" | "context">("off");
  const [progressMs, setProgressMs] = useState(0);
  const [durationMs, setDurationMs] = useState(0);
  const [volume, setVolume] = useState(70);
  const progressTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Local progress ticker
  useEffect(() => {
    if (progressTimerRef.current) clearInterval(progressTimerRef.current);
    if (isPlaying && currentTrack) {
      progressTimerRef.current = setInterval(() => {
        setProgressMs((p) => Math.min(p + 1000, durationMs));
      }, 1000);
    }
    return () => { if (progressTimerRef.current) clearInterval(progressTimerRef.current); };
  }, [isPlaying, currentTrack, durationMs]);

  // Sync playback state (with fallback to currently-playing endpoint)
  const syncPlaybackState = useCallback(async () => {
    if (!isSpotifyConnected) return;
    try {
      const state = await SpotifyService.getPlaybackState();
      if (state) {
        setCurrentTrack(state.track);
        setIsPlaying(state.is_playing);
        setShuffleOn(state.shuffle_state);
        setRepeatMode(state.repeat_state);
        setProgressMs(state.progress_ms);
        setDurationMs(state.duration_ms);
        return;
      }
    } catch { /* silent */ }
    // Fallback: getCurrentlyPlaying uses a different scope that may still work
    try {
      const track = await SpotifyService.getCurrentlyPlaying();
      if (track) {
        setCurrentTrack(track);
        setIsPlaying(true);
        setDurationMs(track.durationSec * 1000);
      }
    } catch { /* silent */ }
  }, [isSpotifyConnected]);

  // Initial fetch
  useEffect(() => {
    const connected = SpotifyService.isConnected();
    setIsSpotifyConnected(connected);

    async function fetchData() {
      setLoading(true);
      try {
        if (connected) {
          const [playback, current, recent, saved, top, artists, lists, q, profile] = await Promise.all([
            SpotifyService.getPlaybackState().catch(() => null),
            SpotifyService.getCurrentlyPlaying().catch(() => null),
            SpotifyService.getRecentlyPlayed(50),
            SpotifyService.getSavedTracks(50),
            SpotifyService.getTopTracks("medium_term", 50),
            SpotifyService.getTopArtists("medium_term", 20),
            SpotifyService.getUserPlaylists(20),
            SpotifyService.getQueue().catch(() => ({ currentTrack: null, queue: [] })),
            SpotifyService.getUserProfile(),
          ]);
          if (playback) {
            setCurrentTrack(playback.track);
            setIsPlaying(playback.is_playing);
            setShuffleOn(playback.shuffle_state);
            setRepeatMode(playback.repeat_state);
            setProgressMs(playback.progress_ms);
            setDurationMs(playback.duration_ms);
          } else if (current) {
            // Fallback: at least show the current track
            setCurrentTrack(current);
            setIsPlaying(true);
            setDurationMs(current.durationSec * 1000);
            // Scope mismatch: full playback state failed but basic currently-playing worked
            setNeedsReauth(true);
          }
          setRecentTracks(recent);
          setSavedTracks(saved);
          setTopTracks(top);
          setTopArtists(artists);
          setPlaylists(lists);
          setQueueTracks(q.queue);
          setUserProfile(profile);
        } else {
          const current = await SpotifySimulator.getCurrentTrack();
          const history = SpotifySimulator.getRecentHistory();
          const batch = SpotifySimulator.getInitialBatch();
          setCurrentTrack(current);
          setDurationMs(current.durationSec * 1000);
          setRecentTracks(history);
          setSavedTracks(batch.slice(0, 15));
        }
      } catch (err) {
        console.error("Listen fetch error:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  // Refetch top tracks/artists when time range changes
  useEffect(() => {
    if (!isSpotifyConnected) return;
    (async () => {
      const [top, artists] = await Promise.all([
        SpotifyService.getTopTracks(timeRange, 50),
        SpotifyService.getTopArtists(timeRange, 20),
      ]);
      setTopTracks(top);
      setTopArtists(artists);
    })();
  }, [timeRange, isSpotifyConnected]);

  // Poll playback state every 5s
  useEffect(() => {
    if (!isSpotifyConnected) return;
    const interval = setInterval(syncPlaybackState, 5_000);
    return () => clearInterval(interval);
  }, [isSpotifyConnected, syncPlaybackState]);

  // Player control handlers
  const handlePlayPause = useCallback(async () => {
    if (!isSpotifyConnected) return;
    try {
      if (isPlaying) { await SpotifyService.pause(); setIsPlaying(false); }
      else { await SpotifyService.play(); setIsPlaying(true); }
    } catch (err) { console.error("Play/Pause error:", err); }
  }, [isSpotifyConnected, isPlaying]);

  const handleNext = useCallback(async () => {
    if (!isSpotifyConnected) return;
    try { await SpotifyService.skipToNext(); setProgressMs(0); setTimeout(syncPlaybackState, 500); }
    catch (err) { console.error("Skip next error:", err); }
  }, [isSpotifyConnected, syncPlaybackState]);

  const handlePrev = useCallback(async () => {
    if (!isSpotifyConnected) return;
    try { await SpotifyService.skipToPrevious(); setProgressMs(0); setTimeout(syncPlaybackState, 500); }
    catch (err) { console.error("Skip prev error:", err); }
  }, [isSpotifyConnected, syncPlaybackState]);

  const handleShuffle = useCallback(async () => {
    if (!isSpotifyConnected) return;
    try { const s = !shuffleOn; await SpotifyService.setShuffle(s); setShuffleOn(s); }
    catch (err) { console.error("Shuffle error:", err); }
  }, [isSpotifyConnected, shuffleOn]);

  const handleRepeat = useCallback(async () => {
    if (!isSpotifyConnected) return;
    const next = repeatMode === "off" ? "context" : repeatMode === "context" ? "track" : "off";
    try { await SpotifyService.setRepeat(next); setRepeatMode(next); }
    catch (err) { console.error("Repeat error:", err); }
  }, [isSpotifyConnected, repeatMode]);

  const handleSeek = useCallback(async (ms: number) => {
    if (!isSpotifyConnected) return;
    try { await SpotifyService.seekTo(ms); setProgressMs(ms); }
    catch (err) { console.error("Seek error:", err); }
  }, [isSpotifyConnected]);

  const handleVolume = useCallback(async (pct: number) => {
    if (!isSpotifyConnected) return;
    try { await SpotifyService.setVolume(pct); setVolume(pct); }
    catch (err) { console.error("Volume error:", err); }
  }, [isSpotifyConnected]);

  // Computed
  const radarData = useMemo(() => averageFeatures(topTracks), [topTracks]);
  const familyDist = useMemo(() => familyDistribution(topTracks), [topTracks]);
  const topGenres = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const t of topTracks) if (t.genre && t.genre !== "Unknown") counts[t.genre] = (counts[t.genre] || 0) + 1;
    return Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([genre, count]) => ({ genre, count }));
  }, [topTracks]);

  if (!mind || !persona) return null;

  if (loading && recentTracks.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="text-center">
          <Loader2 size={32} className="animate-spin mx-auto mb-3" style={{ color }} />
          <p className="text-sm text-slate-500 font-display">{t("listen.loading")}</p>
        </motion.div>
      </div>
    );
  }

  return (
    <motion.div {...pageTransition} className="pb-32">

      {/* ── Persona Header + User Profile ───────────────────────────── */}
      <motion.header variants={cinematicReveal} initial="initial" animate="animate" className="flex items-center gap-5 mb-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.85 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1.2, delay: 0.05, ease }}
          className="relative flex-shrink-0"
        >
          <CharacterAvatar personaId={persona.id} color={color} family={identity.family} size={72} level={personaLevel} showAura />
        </motion.div>

        <div className="flex-1 min-w-0">
          <h1 className="text-2xl md:text-3xl font-display font-bold" style={{ color }}>
            {t(`personas.${persona.id}.name`)}
          </h1>
          <p className="text-sm text-slate-500 font-display font-light italic mt-0.5">
            "{t(`personas.${persona.id}.tagline`)}"
          </p>
          {userProfile && (
            <div className="flex items-center gap-3 mt-2">
              {userProfile.images?.[0] && (
                <img src={userProfile.images[0].url} alt="" className="w-5 h-5 rounded-full object-cover" />
              )}
              <span className="text-[11px] font-mono text-slate-500">{userProfile.display_name}</span>
              <span className="text-[10px] font-mono text-slate-600">·</span>
              <span className="text-[10px] font-mono text-slate-600">{userProfile.followers?.total ?? 0} followers</span>
              <Badge label={userProfile.product === "premium" ? "Premium" : "Free"} color={SPOTIFY_GREEN} size="sm" />
            </div>
          )}
        </div>

        <div className="flex items-center gap-2 flex-shrink-0">
          {isSpotifyConnected ? (
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full" style={{ background: `${SPOTIFY_GREEN}12`, border: `1px solid ${SPOTIFY_GREEN}25` }}>
              <SpotifyLogo size={16} />
              <span className="text-[11px] font-display font-medium" style={{ color: SPOTIFY_GREEN }}>{t("listen.connected")}</span>
            </div>
          ) : (
            <button
              onClick={() => SpotifyService.startAuthFlow({ fromPath: "/listen" })}
              className="flex items-center gap-2 px-4 py-2 rounded-full transition-all hover:scale-105"
              style={{ background: SPOTIFY_GREEN, boxShadow: `0 0 20px ${SPOTIFY_GREEN}30` }}
            >
              <SpotifyLogo size={16} />
              <span className="text-[12px] font-display font-bold text-black">{t("listen.connectSpotify")}</span>
            </button>
          )}
        </div>
      </motion.header>

      {/* ── Scope Upgrade Banner ────────────────────────────────────── */}
      {needsReauth && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 flex items-center gap-3 px-5 py-3 rounded-xl"
          style={{
            background: `linear-gradient(135deg, ${SPOTIFY_GREEN}12, rgba(255,255,255,0.03))`,
            border: `1px solid ${SPOTIFY_GREEN}25`,
          }}
        >
          <RefreshCw size={16} style={{ color: SPOTIFY_GREEN }} />
          <span className="text-xs text-slate-400 flex-1">
            {isTr
              ? "Tam kontrol için Spotify bağlantını güncelle (play/pause/skip/queue)"
              : "Update your Spotify connection for full control (play/pause/skip/queue)"}
          </span>
          <button
            onClick={() => {
              SpotifyService.clearTokens();
              SpotifyService.startAuthFlow({ fromPath: "/listen" });
            }}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-display font-bold text-black transition-all hover:scale-105"
            style={{ background: SPOTIFY_GREEN, boxShadow: `0 0 12px ${SPOTIFY_GREEN}30` }}
          >
            <SpotifyLogo size={14} />
            {isTr ? "Yeniden Bağlan" : "Reconnect"}
          </button>
        </motion.div>
      )}

      {/* ── Now Playing Hero ────────────────────────────────────────── */}
      <motion.section variants={slideUp} initial="initial" animate="animate" className="mb-8">
        <NowPlayingHero
          track={currentTrack} accentColor={color} isPlaying={isPlaying} shuffleOn={shuffleOn}
          repeatMode={repeatMode} progressMs={progressMs} durationMs={durationMs} volume={volume}
          onPlayPause={handlePlayPause} onNext={handleNext} onPrev={handlePrev}
          onShuffle={handleShuffle} onRepeat={handleRepeat} onSeek={handleSeek} onVolume={handleVolume}
          connected={isSpotifyConnected && !needsReauth}
        />
      </motion.section>

      {/* ── Queue (Up Next) ─────────────────────────────────────────── */}
      {queueTracks.length > 0 && (
        <motion.section variants={slideUp} initial="initial" animate="animate" className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <ListMusic size={15} style={{ color }} />
            <h2 className="text-sm font-display font-semibold text-slate-300 uppercase tracking-wider">{t("listen.statQueue")}</h2>
            <span className="text-xs font-mono text-slate-600">{queueTracks.length}</span>
          </div>
          <Card className="max-h-[320px] overflow-y-auto">
            <motion.div variants={staggerChildren} initial="initial" animate="animate" className="space-y-0.5">
              {queueTracks.slice(0, 15).map((track, i) => (
                <TrackRow key={`q-${track.id}-${i}`} track={track} index={i} />
              ))}
            </motion.div>
          </Card>
        </motion.section>
      )}

      {/* ── Top Tracks (with time range tabs) ──────────────────────── */}
      {isSpotifyConnected && (
        <motion.section variants={slideUp} initial="initial" animate="animate" className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <TrendingUp size={15} style={{ color }} />
              <h2 className="text-sm font-display font-semibold text-slate-300 uppercase tracking-wider">{t("listen.topTracks")}</h2>
              <span className="text-xs font-mono text-slate-600">{topTracks.length}</span>
            </div>
            <div className="flex gap-1 p-0.5 rounded-full" style={{ background: "rgba(255,255,255,0.04)" }}>
              {TIME_TABS.map((tab) => (
                <button
                  key={tab.key}
                  onClick={() => setTimeRange(tab.key)}
                  className="relative px-3 py-1 text-xs font-medium rounded-full transition-all duration-300"
                  style={{
                    color: timeRange === tab.key ? "#fff" : "#64748B",
                    background: timeRange === tab.key ? `${color}20` : "transparent",
                    border: timeRange === tab.key ? `1px solid ${color}30` : "1px solid transparent",
                  }}
                >
                  {isTr ? tab.labelTr : tab.labelEn}
                </button>
              ))}
            </div>
          </div>

          <Card className="max-h-[520px] overflow-y-auto">
            <AnimatePresence mode="wait">
              <motion.div key={timeRange} variants={staggerChildren} initial="initial" animate="animate" exit={{ opacity: 0 }} className="space-y-0.5">
                {topTracks.slice(0, 30).map((track, i) => (
                  <TrackRow key={track.id} track={track} index={i} />
                ))}
                {topTracks.length === 0 && <p className="text-center text-sm text-slate-600 py-6">{t("listen.noTopTracks")}</p>}
              </motion.div>
            </AnimatePresence>
          </Card>
        </motion.section>
      )}

      {/* ── Top Artists ─────────────────────────────────────────────── */}
      {isSpotifyConnected && topArtists.length > 0 && (
        <motion.section variants={slideUp} initial="initial" animate="animate" className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <Mic2 size={15} style={{ color }} />
            <h2 className="text-sm font-display font-semibold text-slate-300 uppercase tracking-wider">{t("listen.topArtists")}</h2>
            <span className="text-xs font-mono text-slate-600">{topArtists.length}</span>
          </div>

          <Card className="max-h-[420px] overflow-y-auto">
            <motion.div variants={staggerChildren} initial="initial" animate="animate" className="space-y-0.5">
              {topArtists.map((artist, i) => (
                <ArtistCard key={artist.id} artist={artist} index={i} />
              ))}
            </motion.div>
          </Card>
        </motion.section>
      )}

      {/* ── Two-Column: Recently Played + Saved ────────────────────── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-8">
        <motion.section variants={slideUp} initial="initial" animate="animate">
          <div className="flex items-center gap-2 mb-3">
            <Clock size={15} style={{ color }} />
            <h2 className="text-sm font-display font-semibold text-slate-300 uppercase tracking-wider">{t("listen.recentlyPlayed")}</h2>
            <span className="text-xs font-mono text-slate-600">{recentTracks.length}</span>
          </div>
          <Card className="max-h-[480px] overflow-y-auto">
            <motion.div variants={staggerChildren} initial="initial" animate="animate" className="space-y-0.5">
              {recentTracks.map((track, i) => (
                <TrackRow key={`${track.id}-${i}`} track={track} index={i} />
              ))}
              {recentTracks.length === 0 && <p className="text-center text-sm text-slate-600 py-8">{t("listen.noRecent")}</p>}
            </motion.div>
          </Card>
        </motion.section>

        <motion.section variants={slideUp} initial="initial" animate="animate">
          <div className="flex items-center gap-2 mb-3">
            <Heart size={15} style={{ color }} />
            <h2 className="text-sm font-display font-semibold text-slate-300 uppercase tracking-wider">{t("listen.savedTracks")}</h2>
            <span className="text-xs font-mono text-slate-600">{savedTracks.length}</span>
          </div>
          <Card className="max-h-[480px] overflow-y-auto">
            <motion.div variants={staggerChildren} initial="initial" animate="animate" className="space-y-0.5">
              {savedTracks.map((track, i) => (
                <TrackRow key={track.id} track={track} index={i} compact />
              ))}
              {savedTracks.length === 0 && <p className="text-center text-sm text-slate-600 py-8">{t("listen.noSaved")}</p>}
            </motion.div>
          </Card>
        </motion.section>
      </div>

      {/* ── Audio DNA (Radar + Features + Family Mix) ───────────────── */}
      {isSpotifyConnected && topTracks.length > 0 && (
        <motion.section variants={slideUp} initial="initial" animate="animate" className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Disc3 size={16} style={{ color }} />
            <h2 className="text-sm font-display font-semibold text-slate-300 uppercase tracking-wider">{t("listen.audioDna")}</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <p className="hud-label mb-3">{t("listen.avgFeatures")}</p>
              {radarData.length > 0 ? (
                <ResponsiveContainer width="100%" height={220}>
                  <RadarChart data={radarData} cx="50%" cy="50%" outerRadius="72%">
                    <PolarGrid stroke="rgba(255,255,255,0.06)" />
                    <PolarAngleAxis dataKey="feature" tick={{ fill: "#64748B", fontSize: 10 }} tickLine={false} />
                    <Radar name="Audio DNA" dataKey="value" stroke={color} fill={color} fillOpacity={0.15} strokeWidth={1.5} />
                  </RadarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-[220px] flex items-center justify-center text-xs text-slate-600">No data</div>
              )}
            </Card>

            <Card>
              <p className="hud-label mb-4">{t("listen.featureBreakdown")}</p>
              <div className="space-y-3">
                {radarData.map((d) => (
                  <FeatureBarRow key={d.feature} label={d.feature} value={d.value} color={d.color} />
                ))}
              </div>
            </Card>

            <Card>
              <p className="hud-label mb-4">{t("listen.familyMix")}</p>
              <div className="space-y-2 mb-6">
                {familyDist.map((f) => (
                  <div key={f.name} className="flex items-center gap-2">
                    <div className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: f.color, boxShadow: `0 0 8px ${f.color}40` }} />
                    <span className="text-xs text-slate-400 flex-1">{f.name}</span>
                    <span className="text-xs font-mono text-slate-500">{f.count}</span>
                    <div className="w-16 h-1 rounded-full bg-white/[0.04] overflow-hidden">
                      <motion.div className="h-full rounded-full" style={{ backgroundColor: f.color }} initial={{ width: 0 }} animate={{ width: `${(f.count / topTracks.length) * 100}%` }} transition={{ duration: 0.8, ease }} />
                    </div>
                  </div>
                ))}
              </div>
              <p className="hud-label mb-3">{t("listen.topGenres")}</p>
              <div className="flex flex-wrap gap-1.5">
                {topGenres.map((g) => (
                  <Badge key={g.genre} label={`${g.genre} (${g.count})`} color={color} size="sm" />
                ))}
                {topGenres.length === 0 && <span className="text-xs text-slate-600">—</span>}
              </div>
            </Card>
          </div>
        </motion.section>
      )}

      {/* ── Playlists ──────────────────────────────────────────────── */}
      {isSpotifyConnected && playlists.length > 0 && (
        <motion.section variants={slideUp} initial="initial" animate="animate" className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <Library size={15} style={{ color }} />
            <h2 className="text-sm font-display font-semibold text-slate-300 uppercase tracking-wider">{t("listen.playlists")}</h2>
            <span className="text-xs font-mono text-slate-600">{playlists.length}</span>
          </div>
          <Card className="max-h-[380px] overflow-y-auto">
            <motion.div variants={staggerChildren} initial="initial" animate="animate" className="space-y-0.5">
              {playlists.map((p) => (
                <PlaylistCard key={p.id} playlist={p} />
              ))}
            </motion.div>
          </Card>
        </motion.section>
      )}

      {/* ── Stats Row ──────────────────────────────────────────────── */}
      <motion.section variants={slideUp} initial="initial" animate="animate">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { label: t("listen.statNowPlaying"), value: currentTrack ? "1" : "—", icon: Music2 },
            { label: t("listen.statRecent"), value: recentTracks.length, icon: Clock },
            { label: t("listen.statSaved"), value: savedTracks.length, icon: Heart },
            { label: t("listen.statTopTracks"), value: topTracks.length, icon: TrendingUp },
          ].map((stat) => (
            <Card key={stat.label} className="text-center py-4">
              <stat.icon size={16} className="mx-auto mb-2 text-slate-600" />
              <p className="text-lg font-display font-bold text-white">{stat.value}</p>
              <p className="hud-label mt-1">{stat.label}</p>
            </Card>
          ))}
        </div>
      </motion.section>

      {/* ── Open in Spotify ─────────────────────────────────────────── */}
      {isSpotifyConnected && (
        <motion.div variants={slideUp} initial="initial" animate="animate" className="mt-6 text-center">
          <a
            href="https://open.spotify.com"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full transition-all hover:scale-105"
            style={{ background: `${SPOTIFY_GREEN}12`, border: `1px solid ${SPOTIFY_GREEN}20` }}
          >
            <SpotifyLogo size={18} />
            <span className="text-sm font-display" style={{ color: SPOTIFY_GREEN }}>{t("listen.openSpotify")}</span>
            <ExternalLink size={12} style={{ color: SPOTIFY_GREEN }} />
          </a>
        </motion.div>
      )}
    </motion.div>
  );
}
