/**
 * ListenPanel — Self-contained right panel for Listen mode in Dashboard.
 *
 * Encapsulates all Spotify/player state and renders NowPlayingHero,
 * queue, top tracks, and recently played in a compact layout that
 * fits the Dashboard's right panel (50% width grid cell).
 *
 * Agent integration: registers useAgentActions so the left-panel chat
 * can control playback via tool calls, and sends proactive system
 * events when the track changes.
 */

import React, { useEffect, useState, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";
import {
  ListMusic,
  Clock,
  TrendingUp,
  Loader2,
  RefreshCw,
} from "lucide-react";
import { SpotifyService } from "@/services/spotify";
import type { MockTrack } from "@/services/SpotifySimulator";
import { SpotifySimulator } from "@/services/SpotifySimulator";
import { useChatStore } from "@/stores/useChatStore";
import { useAgentActions } from "@/hooks/useAgentActions";
import { staggerChildren } from "@/design/animations";
import {
  SPOTIFY_GREEN,
  TIME_TABS,
  SpotifyLogo,
  NowPlayingHero,
  TrackRow,
  type NowPlayingProps,
  type TimeRange,
} from "@/pages/Listen";

interface Props {
  accentColor: string;
}

export function ListenPanel({ accentColor }: Props) {
  const { t, i18n } = useTranslation();
  const isTr = i18n.language === "tr";
  const color = accentColor;

  // Data state
  const [currentTrack, setCurrentTrack] = useState<MockTrack | null>(null);
  const [recentTracks, setRecentTracks] = useState<MockTrack[]>([]);
  const [topTracks, setTopTracks] = useState<MockTrack[]>([]);
  const [queueTracks, setQueueTracks] = useState<MockTrack[]>([]);
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

  // Cooldown: prevent Spotify poll from overriding agent's track choice
  const agentOverrideUntilRef = useRef(0);

  // ── Playback handlers ────────────────────────────────────────────

  const syncPlaybackState = useCallback(async () => {
    if (!isSpotifyConnected) return;
    // Skip if agent recently set a track (10s cooldown)
    if (Date.now() < agentOverrideUntilRef.current) return;
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
    try {
      const track = await SpotifyService.getCurrentlyPlaying();
      if (track) {
        setCurrentTrack(track);
        setIsPlaying(true);
        setDurationMs(track.durationSec * 1000);
      }
    } catch { /* silent */ }
  }, [isSpotifyConnected]);

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

  // ── Agent integration ─────────────────────────────────────────────

  // Wrap setCurrentTrack for agent: also sets cooldown to prevent poll override
  const setCurrentTrackFromAgent = useCallback((t: MockTrack | null) => {
    agentOverrideUntilRef.current = Date.now() + 15_000; // 15s cooldown
    setCurrentTrack(t);
  }, []);

  const { handleAction } = useAgentActions({
    isSpotifyConnected,
    setCurrentTrack: setCurrentTrackFromAgent,
    setIsPlaying,
    setProgressMs,
    setDurationMs,
    setQueueTracks,
    syncPlaybackState,
    handlePlayPause,
    handleNext,
    handlePrev,
    handleShuffle,
    handleRepeat,
    handleVolume,
    volume,
  });

  const setActionHandler = useChatStore((s) => s.setActionHandler);
  useEffect(() => {
    setActionHandler(handleAction);
    return () => setActionHandler(null);
  }, [handleAction, setActionHandler]);

  // Proactive: detect track changes
  const prevTrackKeyRef = useRef<string | null>(null);
  const sendSystemEvent = useChatStore((s) => s.sendSystemEvent);

  useEffect(() => {
    if (!currentTrack) return;
    const trackKey = `${currentTrack.id}-${currentTrack.name}`;
    if (prevTrackKeyRef.current && prevTrackKeyRef.current !== trackKey) {
      sendSystemEvent("track_changed", {
        track_name: currentTrack.name,
        artist: currentTrack.artist,
        family: currentTrack.dominantFamily,
        genre: currentTrack.genre,
      });
    }
    prevTrackKeyRef.current = trackKey;
  }, [currentTrack, sendSystemEvent]);

  // ── Data loading ──────────────────────────────────────────────────

  // Progress ticker
  useEffect(() => {
    if (progressTimerRef.current) clearInterval(progressTimerRef.current);
    if (isPlaying && currentTrack) {
      progressTimerRef.current = setInterval(() => {
        setProgressMs((p) => Math.min(p + 1000, durationMs));
      }, 1000);
    }
    return () => { if (progressTimerRef.current) clearInterval(progressTimerRef.current); };
  }, [isPlaying, currentTrack, durationMs]);

  // Initial fetch
  useEffect(() => {
    const connected = SpotifyService.isConnected();
    setIsSpotifyConnected(connected);

    async function loadDemo() {
      const current = await SpotifySimulator.getCurrentTrack();
      const history = SpotifySimulator.getRecentHistory();
      setCurrentTrack(current);
      setDurationMs(current.durationSec * 1000);
      setRecentTracks(history);
      setIsSpotifyConnected(false);
    }

    async function fetchData() {
      setLoading(true);
      try {
        if (connected) {
          const [playback, current, recent, top, q] = await Promise.all([
            SpotifyService.getPlaybackState().catch(() => null),
            SpotifyService.getCurrentlyPlaying().catch(() => null),
            SpotifyService.getRecentlyPlayed(20).catch(() => []),
            SpotifyService.getTopTracks("medium_term", 20).catch(() => []),
            SpotifyService.getQueue().catch(() => ({ currentTrack: null, queue: [] as MockTrack[] })),
          ]);
          if (playback) {
            setCurrentTrack(playback.track);
            setIsPlaying(playback.is_playing);
            setShuffleOn(playback.shuffle_state);
            setRepeatMode(playback.repeat_state);
            setProgressMs(playback.progress_ms);
            setDurationMs(playback.duration_ms);
          } else if (current) {
            setCurrentTrack(current);
            setIsPlaying(true);
            setDurationMs(current.durationSec * 1000);
            setNeedsReauth(true);
          }
          // If Spotify returned nothing useful, fall back to demo
          if (!playback && !current && (recent as MockTrack[]).length === 0) {
            await loadDemo();
          } else {
            setRecentTracks(recent as MockTrack[]);
            setTopTracks(top as MockTrack[]);
            setQueueTracks((q as { queue: MockTrack[] }).queue);
          }
        } else {
          await loadDemo();
        }
      } catch (err) {
        console.error("ListenPanel fetch error:", err);
        // Spotify completely failed — fall back to demo
        try { await loadDemo(); } catch { /* silent */ }
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  // Refetch when time range changes
  useEffect(() => {
    if (!isSpotifyConnected) return;
    SpotifyService.getTopTracks(timeRange, 20).then(setTopTracks).catch(() => {});
  }, [timeRange, isSpotifyConnected]);

  // Poll playback every 5s
  useEffect(() => {
    if (!isSpotifyConnected) return;
    const interval = setInterval(syncPlaybackState, 5_000);
    return () => clearInterval(interval);
  }, [isSpotifyConnected, syncPlaybackState]);

  // ── List tab state ─────────────────────────────────────────────────

  type ListTab = "queue" | "top" | "recent";
  const [activeTab, setActiveTab] = useState<ListTab>("queue");

  // Auto-switch to queue tab when agent builds a queue
  const prevQueueLenRef = useRef(0);
  useEffect(() => {
    if (queueTracks.length > prevQueueLenRef.current && prevQueueLenRef.current === 0) {
      setActiveTab("queue");
    }
    prevQueueLenRef.current = queueTracks.length;
  }, [queueTracks]);

  const LIST_TABS: { key: ListTab; icon: React.ElementType; labelTr: string; labelEn: string; count: () => number }[] = [
    { key: "queue",  icon: ListMusic,  labelTr: "Sıradaki",        labelEn: "Up Next",    count: () => queueTracks.length },
    { key: "top",    icon: TrendingUp, labelTr: "En Çok Dinlenen", labelEn: "Top Tracks", count: () => topTracks.length },
    { key: "recent", icon: Clock,      labelTr: "Son Dinlenen",    labelEn: "Recent",     count: () => recentTracks.length },
  ];

  // ── Render ────────────────────────────────────────────────────────

  const nowPlayingProps: NowPlayingProps = {
    track: currentTrack, accentColor: color, isPlaying, shuffleOn,
    repeatMode, progressMs, durationMs, volume,
    onPlayPause: handlePlayPause, onNext: handleNext, onPrev: handlePrev,
    onShuffle: handleShuffle, onRepeat: handleRepeat, onSeek: handleSeek, onVolume: handleVolume,
    connected: isSpotifyConnected && !needsReauth,
  };

  if (loading && !currentTrack) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 size={24} className="animate-spin" style={{ color }} />
      </div>
    );
  }

  // Active list tracks
  const activeListTracks = activeTab === "queue" ? queueTracks
    : activeTab === "top" ? topTracks
    : recentTracks;

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* ── Header: Spotify status + reconnect ──────────────── */}
      <div className="flex items-center gap-2 px-3 py-2 flex-shrink-0 border-b border-white/[0.06]">
        {isSpotifyConnected ? (
          <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-full" style={{ background: `${SPOTIFY_GREEN}10`, border: `1px solid ${SPOTIFY_GREEN}20` }}>
            <SpotifyLogo size={12} />
            <span className="text-[9px] font-display font-medium" style={{ color: SPOTIFY_GREEN }}>{t("listen.connected")}</span>
          </div>
        ) : (
          <button
            onClick={() => SpotifyService.startAuthFlow({ fromPath: "/listen" })}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-full transition-all hover:scale-105"
            style={{ background: SPOTIFY_GREEN, boxShadow: `0 0 12px ${SPOTIFY_GREEN}25` }}
          >
            <SpotifyLogo size={12} />
            <span className="text-[10px] font-display font-bold text-black">{t("listen.connectSpotify")}</span>
          </button>
        )}
        {needsReauth && (
          <button
            onClick={() => { SpotifyService.clearTokens(); SpotifyService.startAuthFlow({ fromPath: "/listen" }); }}
            className="flex items-center gap-1 px-2 py-0.5 rounded-full transition-all hover:scale-105"
            style={{ background: `${SPOTIFY_GREEN}12`, border: `1px solid ${SPOTIFY_GREEN}20` }}
          >
            <RefreshCw size={10} style={{ color: SPOTIFY_GREEN }} />
            <span className="text-[9px] font-display" style={{ color: SPOTIFY_GREEN }}>
              {isTr ? "Yeniden Bağlan" : "Reconnect"}
            </span>
          </button>
        )}
      </div>

      {/* ── Now Playing Hero ────────────────────────────────── */}
      <div className="flex-shrink-0 px-3 py-3">
        <NowPlayingHero {...nowPlayingProps} />
      </div>

      {/* ── List Tab Bar ────────────────────────────────────── */}
      <div className="flex-shrink-0 flex items-center gap-1 px-3 pb-2">
        {LIST_TABS.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.key;
          const cnt = tab.count();
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-display font-medium transition-all"
              style={{
                color: isActive ? "#fff" : "#64748B",
                background: isActive ? `${color}18` : "transparent",
                border: isActive ? `1px solid ${color}30` : "1px solid rgba(255,255,255,0.06)",
              }}
            >
              <Icon size={11} />
              <span>{isTr ? tab.labelTr : tab.labelEn}</span>
              {cnt > 0 && (
                <span className="text-[8px] font-mono" style={{ color: isActive ? color : "#475569" }}>
                  {cnt}
                </span>
              )}
            </button>
          );
        })}

        {/* Time range selector — only when Top Tracks tab is active */}
        {activeTab === "top" && isSpotifyConnected && (
          <div className="flex gap-0.5 ml-auto">
            {TIME_TABS.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setTimeRange(tab.key)}
                className="px-1.5 py-0.5 text-[8px] font-medium rounded-full transition-all"
                style={{
                  color: timeRange === tab.key ? "#fff" : "#475569",
                  background: timeRange === tab.key ? `${color}15` : "transparent",
                }}
              >
                {isTr ? tab.labelTr : tab.labelEn}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* ── Active List ─────────────────────────────────────── */}
      <div className="flex-1 min-h-0 overflow-y-auto px-3 pb-3"
        style={{ scrollbarWidth: "thin", scrollbarColor: `${color}30 transparent` }}
      >
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab + (activeTab === "top" ? `-${timeRange}` : "")}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
          >
            {activeListTracks.length > 0 ? (
              <motion.div variants={staggerChildren} initial="initial" animate="animate" className="space-y-0.5">
                {activeListTracks.slice(0, 20).map((track, i) => (
                  <TrackRow key={`${activeTab}-${track.id}-${i}`} track={track} index={i} compact />
                ))}
              </motion.div>
            ) : (
              <div className="flex flex-col items-center justify-center py-12 gap-2">
                {activeTab === "queue" && <ListMusic size={24} className="text-slate-700" />}
                {activeTab === "top" && <TrendingUp size={24} className="text-slate-700" />}
                {activeTab === "recent" && <Clock size={24} className="text-slate-700" />}
                <p className="text-[11px] text-slate-600 font-body">
                  {activeTab === "queue" ? (isTr ? "Sırada parça yok" : "No tracks in queue") :
                   activeTab === "top" ? (isTr ? "Henüz veri yok" : "No data yet") :
                   (isTr ? "Son dinlenen parça yok" : "No recent tracks")}
                </p>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
