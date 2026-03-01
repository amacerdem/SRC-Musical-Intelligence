/* ── Lab — Scientific Analysis Studio ────────────────────────────────
 *  Full-screen 2-panel layout: Temporal Flow (top) + Mel Spectrogram (bottom).
 *  Pure scientific instrument feel — no chat, no organism, no radar.
 *
 *  Mel spectrogram uses pre-computed data from the MI analysis pipeline
 *  (128 mel bins × T frames @ 172.27 Hz), loaded as a binary file.
 *
 *  ┌──────────────────────────────────────────────────────────────┐
 *  │  🧪 Lab   [Track ▾]  ▶ ‖  0:42/3:12   [6D|12D|24D]        │
 *  ├──────────────────────────────────────────────────────────────┤
 *  │  DimLabels │  TEMPORAL FLOW (FlowTimeline canvas)            │
 *  ├────────────┼─────────────────────────────────────────────────┤
 *  │  🎹 Piano  │  MEL SPECTROGRAM (MI Pipeline data)             │
 *  │  Roll      │  log2 freq axis, 4 peak markers                 │
 *  └────────────┴─────────────────────────────────────────────────┘
 *  ──────────────────────────────────────────────────────────────────── */

import { useRef, useEffect, useMemo, useState, useCallback } from "react";
import { motion } from "framer-motion";
import {
  FlaskConical, Clock, Music2, Activity, Play, Pause,
  ChevronDown, Waves,
} from "lucide-react";

import { useLabStore } from "@/stores/useLabStore";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { pageTransition, fadeIn } from "@/design/animations";
import { ALL_PSYCHOLOGY, ALL_COGNITION, ALL_NEUROSCIENCE } from "@/data/dimensions";
import { miDataService } from "@/services/MIDataService";
import type { MICatalogTrack } from "@/types/mi-dataset";

import { DepthSelector } from "@/components/lab/DepthSelector";
import { FlowTimeline } from "@/components/lab/FlowTimeline";
import { SpectralPeaks } from "@/components/lab/SpectralPeaks";
import type { MelData } from "@/components/lab/peakExtractor";

/* ── Track ID → audio file mapping ──────────────── */
const TRACK_AUDIO: Record<string, string> = {
  "tchaikovsky__swan_lake_suite_op20a_scene": "/music/swan-lake.wav",
  "pyotr_ilyich_tchaikovsky_berliner_philharmoniker_mstislav_rostropovich__swan_lake_suite_op_20a_i_scene_swan_theme_modera": "/music/swan-lake.wav",
};

const V4_TRACK_IDS: Record<string, string> = {
  "pyotr_ilyich_tchaikovsky_berliner_philharmoniker_mstislav_rostropovich__swan_lake_suite_op_20a_i_scene_swan_theme_modera":
    "tchaikovsky__swan_lake_suite_op20a_scene",
};

/* ── Load mel binary file ─────────────────────────── */
async function loadMelBinary(trackId: string): Promise<MelData | null> {
  const url = `/data/mi-dataset/tracks/${trackId}_mel.bin`;
  try {
    const resp = await fetch(url);
    if (!resp.ok) return null;
    const buf = await resp.arrayBuffer();
    const view = new DataView(buf);
    const nMels = view.getUint32(0, true);
    const nFrames = view.getUint32(4, true);
    const frameRate = view.getFloat32(8, true);
    // 4 reserved bytes at offset 12
    const centerFreqs = new Float32Array(buf, 16, nMels);
    const data = new Uint8Array(buf, 16 + nMels * 4);
    return { nMels, nFrames, frameRate, centerFreqs, data };
  } catch {
    return null;
  }
}

export function Lab() {
  const identity = useActiveIdentity();
  const color = identity.color;

  /* ── Lab store ──────────────────────────────────── */
  const trackDetail = useLabStore((s) => s.trackDetail);
  const depth = useLabStore((s) => s.depth);
  const setDepth = useLabStore((s) => s.setDepth);
  const temporal = useLabStore((s) => s.temporal);
  const phase = useLabStore((s) => s.phase);
  const selectTrack = useLabStore((s) => s.selectTrack);

  const hasAnalysis = phase === "done" && trackDetail && temporal;

  /* ── Track catalog for dropdown ─────────────────── */
  const labTracks = useMemo(() =>
    miDataService.getAllTracks().filter(
      (t) => t.id.includes("swan_lake") && t.duration_s > 60
    ),
  []);

  /* ── Segment data ───────────────────────────────── */
  const segments6D = useMemo(
    () => temporal?.segments.map((s) => s.psychology) ?? [],
    [temporal],
  );

  /* ── Audio playback ──────────────────────────────── */
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const segCountRef = useRef(segments6D.length);
  segCountRef.current = segments6D.length;

  const [isPlaying, setIsPlaying] = useState(false);
  const [hasEverPlayed, setHasEverPlayed] = useState(false);
  const [flowIdx, setFlowIdx] = useState(0);
  const [melData, setMelData] = useState<MelData | null>(null);
  const [peakCount, setPeakCount] = useState<4 | 8 | 16>(8);

  // Initialize audio element + load mel data when track changes
  useEffect(() => {
    // Cleanup previous
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.src = "";
    }
    audioRef.current = null;
    setIsPlaying(false);
    setHasEverPlayed(false);
    setFlowIdx(0);
    setMelData(null);

    if (!trackDetail) return;

    // Audio element setup
    const audioUrl = TRACK_AUDIO[trackDetail.id];
    let audio: HTMLAudioElement | null = null;
    if (audioUrl) {
      audio = new Audio(audioUrl);
      audio.crossOrigin = "anonymous";
      audio.preload = "auto";
      audioRef.current = audio;

      const onTimeUpdate = () => {
        if (!audio || !audio.duration || segCountRef.current <= 1) return;
        const ratio = audio.currentTime / audio.duration;
        const idx = Math.round(ratio * (segCountRef.current - 1));
        setFlowIdx(Math.max(0, Math.min(segCountRef.current - 1, idx)));
      };

      const onEnded = () => {
        setIsPlaying(false);
        setFlowIdx(0);
      };

      audio.addEventListener("timeupdate", onTimeUpdate);
      audio.addEventListener("ended", onEnded);
    }

    // Load pre-computed mel spectrogram
    loadMelBinary(trackDetail.id).then(setMelData);

    return () => {
      if (audio) {
        audio.pause();
        audio.src = "";
      }
    };
  }, [trackDetail]);

  const togglePlay = useCallback(() => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
      setIsPlaying(false);
    } else {
      setHasEverPlayed(true);
      audio.play().catch(() => { /* autoplay blocked */ });
      setIsPlaying(true);
    }
  }, [isPlaying]);

  const flowValues = segments6D[flowIdx] ?? temporal?.overall.psychology ?? [];

  /* ── Seek handler ───────────────────────────────── */
  const handleSeek = useCallback((ratio: number) => {
    const audio = audioRef.current;
    if (!audio || !audio.duration) return;
    audio.currentTime = ratio * audio.duration;
    const idx = Math.round(ratio * (segments6D.length - 1));
    setFlowIdx(Math.max(0, Math.min(segments6D.length - 1, idx)));
    if (!hasEverPlayed) setHasEverPlayed(true);
  }, [segments6D.length, hasEverPlayed]);

  /* ── Time display ───────────────────────────────── */
  const flowTime = useMemo(() => {
    if (!trackDetail || segments6D.length <= 1) return "";
    const secs = (flowIdx / Math.max(1, segments6D.length - 1)) * trackDetail.duration_s;
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  }, [flowIdx, segments6D.length, trackDetail]);

  const totalTime = useMemo(() => {
    if (!trackDetail) return "";
    const m = Math.floor(trackDetail.duration_s / 60);
    const s = Math.floor(trackDetail.duration_s % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  }, [trackDetail]);

  /* ── Track select handler ───────────────────────── */
  const handleTrackSelect = useCallback(async (track: MICatalogTrack) => {
    const resolvedId = V4_TRACK_IDS[track.id] ?? track.id;
    const detail = await miDataService.getTrackDetail(resolvedId);
    selectTrack(detail);
    setShowTrackMenu(false);
  }, [selectTrack]);

  const [showTrackMenu, setShowTrackMenu] = useState(false);

  return (
    <motion.div {...pageTransition} className="relative h-screen overflow-hidden">

      {/* ── Ambient background — scientific dark ─────────────────────── */}
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0" style={{ background: `radial-gradient(ellipse 80% 60% at 50% 20%, ${color}06 0%, transparent 60%)` }} />
        <div className="absolute inset-0" style={{ background: `radial-gradient(ellipse 40% 50% at 10% 90%, rgba(99,102,241,0.02) 0%, transparent 50%)` }} />
        <div className="absolute inset-0" style={{ background: `radial-gradient(ellipse 40% 35% at 90% 80%, rgba(168,85,247,0.02) 0%, transparent 50%)` }} />
      </div>
      <div className="cinematic-vignette z-[2]" />

      {/* ═══ MAIN ═════════════════════════════════════════════════════ */}
      <div className="relative z-10 h-full flex flex-col px-5 sm:px-8 md:px-10 pt-5 pb-20">

        {/* Click-outside overlay for track menu (must be inside z-10 context so z-50 menu is above) */}
        {showTrackMenu && (
          <div
            className="fixed inset-0 z-40"
            onClick={() => setShowTrackMenu(false)}
          />
        )}

        {/* ── Header ────────────────────────────────────────────────── */}
        <motion.div {...fadeIn} className="flex items-center justify-between pb-3 flex-shrink-0">
          {/* Left: Lab title */}
          <div className="flex items-center gap-2.5">
            <FlaskConical size={17} style={{ color }} />
            <h1 className="text-base font-display font-bold" style={{ color }}>Lab</h1>
            <span className="text-[10px] font-display text-slate-700 font-light tracking-wider uppercase">Analysis Studio</span>
          </div>

          {/* Center: Track selector + transport */}
          <div className="flex items-center gap-3">
            {/* Track dropdown */}
            <div className="relative">
              <button
                onClick={() => setShowTrackMenu(!showTrackMenu)}
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg transition-all"
                style={{
                  background: "rgba(255,255,255,0.03)",
                  border: "1px solid rgba(255,255,255,0.06)",
                }}
              >
                <Music2 size={12} className="text-slate-500" />
                <span className="text-xs font-display text-slate-300 max-w-[180px] truncate">
                  {trackDetail ? trackDetail.title : "Select track..."}
                </span>
                <ChevronDown size={12} className="text-slate-600" />
              </button>

              {showTrackMenu && (
                <motion.div
                  initial={{ opacity: 0, y: -4 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="absolute top-full mt-1 left-0 z-50 w-72 rounded-xl overflow-hidden"
                  style={{
                    background: "rgba(6,6,14,0.96)",
                    border: "1px solid rgba(255,255,255,0.08)",
                    backdropFilter: "blur(20px)",
                    boxShadow: "0 12px 40px rgba(0,0,0,0.6)",
                  }}
                >
                  <div className="max-h-64 overflow-y-auto py-1" style={{ scrollbarWidth: "thin" }}>
                    {labTracks.map((track) => (
                      <button
                        key={track.id}
                        onClick={() => handleTrackSelect(track)}
                        className="w-full flex items-center gap-2.5 px-3 py-2 text-left transition-all hover:bg-white/[0.04]"
                      >
                        <Music2 size={11} className="text-slate-600 flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <div className="text-xs font-display text-slate-300 truncate">{track.title}</div>
                          <div className="text-[10px] text-slate-600 truncate">{track.artist}</div>
                        </div>
                        <span className="text-[9px] font-mono text-slate-700">{Math.round(track.duration_s)}s</span>
                      </button>
                    ))}
                  </div>
                </motion.div>
              )}
            </div>

            {/* Play/Pause */}
            {hasAnalysis && (
              <button
                onClick={togglePlay}
                className="w-8 h-8 rounded-full flex items-center justify-center transition-all"
                style={{
                  background: isPlaying ? `${color}20` : `${color}10`,
                  border: `1.5px solid ${isPlaying ? `${color}50` : `${color}25`}`,
                  boxShadow: isPlaying ? `0 0 16px ${color}20` : "none",
                }}
              >
                {isPlaying ? (
                  <Pause size={13} style={{ color }} />
                ) : (
                  <Play size={13} style={{ color }} className="ml-0.5" />
                )}
              </button>
            )}

            {/* Time */}
            {hasAnalysis && hasEverPlayed && (
              <div className="flex items-center gap-1.5 text-slate-500">
                <Clock size={11} />
                <span className="text-[10px] font-mono" style={{ color: `${color}70` }}>
                  {flowTime} / {totalTime}
                </span>
              </div>
            )}
          </div>

          {/* Right: Peak count + Depth selector */}
          <div className="flex items-center gap-3">
            {hasAnalysis && (
              <span className="text-[8px] font-mono text-slate-700">
                {temporal.source === "full" ? `${temporal.frameCount} frames` : "64 seg"}
              </span>
            )}

            {/* Peak count selector */}
            <div className="flex items-center gap-0.5 rounded-lg overflow-hidden"
              style={{ border: "1px solid rgba(255,255,255,0.06)" }}
            >
              {([4, 8, 16] as const).map((n) => (
                <button
                  key={n}
                  onClick={() => setPeakCount(n)}
                  className="px-2 py-1 text-[9px] font-mono transition-all"
                  style={{
                    background: peakCount === n ? `${color}18` : "transparent",
                    color: peakCount === n ? color : "rgba(255,255,255,0.3)",
                    fontWeight: peakCount === n ? 700 : 400,
                  }}
                >
                  {n}P
                </button>
              ))}
            </div>

            <DepthSelector depth={depth} onChange={setDepth} accentColor={color} />
          </div>
        </motion.div>

        {/* ── 2-PANEL GRID ─────────────────────────────────────────── */}
        <div className="flex-1 min-h-0 flex flex-col gap-0">

          {/* ═ PANEL 1 — Temporal Flow (~35%) ═══════════════════════ */}
          <div
            className="min-h-0 border border-white/[0.04] rounded-t-xl overflow-hidden"
            style={{ flex: "0 0 35%" }}
          >
            {hasAnalysis ? (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2, duration: 0.6 }}
                className="h-full flex flex-col px-2 py-1"
              >
                {/* Panel header */}
                <div className="flex items-center gap-2 mb-0.5 flex-shrink-0">
                  <Activity size={10} className="text-slate-600" />
                  <span className="text-[9px] font-display font-light tracking-[0.12em] uppercase text-slate-500">
                    Temporal Flow
                  </span>
                </div>

                <div className="flex-1 min-h-0 flex">
                  {/* Dimension labels */}
                  <FlowDimLabels
                    values={
                      depth === 6 ? flowValues
                        : depth === 12 ? (temporal.segments[flowIdx]?.cognition ?? temporal.overall.cognition)
                        : (temporal.segments[flowIdx]?.neuroscience ?? temporal.overall.neuroscience)
                    }
                    dims={depth === 6 ? ALL_PSYCHOLOGY : depth === 12 ? ALL_COGNITION : ALL_NEUROSCIENCE}
                    animated={hasEverPlayed}
                  />
                  <div className="flex-1 min-h-0">
                    <FlowTimeline
                      temporal={temporal}
                      trackDetail={trackDetail}
                      depth={depth}
                      accentColor={color}
                      audioRef={audioRef}
                      isPlaying={isPlaying}
                      onSeek={handleSeek}
                    />
                  </div>
                </div>
              </motion.div>
            ) : (
              <div className="h-full flex items-center justify-center">
                <div className="flex flex-col items-center gap-3">
                  <Activity size={16} className="text-slate-800" />
                  <span className="text-[9px] font-display font-light tracking-[0.12em] uppercase text-slate-700">
                    Temporal Flow
                  </span>
                  {phase === "idle" && (
                    <p className="text-[10px] text-slate-700 font-body text-center max-w-[200px]">
                      Select a track to begin analysis
                    </p>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* ═ PANEL 2 — Mel Spectrogram (~65%) ════════════════════ */}
          <div
            className="min-h-0 border border-t-0 border-white/[0.04] rounded-b-xl overflow-hidden"
            style={{ flex: "0 0 65%" }}
          >
            {hasAnalysis ? (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.35, duration: 0.6 }}
                className="h-full flex flex-col px-2 py-1"
              >
                {/* Panel header */}
                <div className="flex items-center gap-2 mb-0.5 flex-shrink-0">
                  <Waves size={10} className="text-slate-600" />
                  <span className="text-[9px] font-display font-light tracking-[0.12em] uppercase text-slate-500">
                    Spectral Peaks
                  </span>
                  <span className="text-[7px] font-mono text-slate-700">
                    A0–C8 · log₂ · {peakCount} peaks/frame{melData ? ` · ${melData.frameRate.toFixed(0)}Hz` : ""}
                  </span>
                </div>

                <div className="flex-1 min-h-0">
                  <SpectralPeaks
                    melData={melData}
                    audioRef={audioRef}
                    isPlaying={isPlaying}
                    duration={trackDetail.duration_s}
                    accentColor={color}
                    peakCount={peakCount}
                    onSeek={handleSeek}
                  />
                </div>
              </motion.div>
            ) : (
              <div className="h-full flex items-center justify-center">
                <div className="flex flex-col items-center gap-3">
                  <Waves size={16} className="text-slate-800" />
                  <span className="text-[9px] font-display font-light tracking-[0.12em] uppercase text-slate-700">
                    Spectral Peaks
                  </span>
                </div>
              </div>
            )}
          </div>

        </div>
      </div>

    </motion.div>
  );
}


/* ═══════════════════════════════════════════════════════════════════════
 *  FlowDimLabels — Y-axis dimension labels that track curve positions
 * ═══════════════════════════════════════════════════════════════════════ */

function FlowDimLabels({ values, dims, animated }: {
  values: number[];
  dims: { key: string; name: string; color: string }[];
  animated: boolean;
}) {
  const fontSize = dims.length <= 6 ? 11 : dims.length <= 12 ? 9 : 7;
  const dotSize = dims.length <= 6 ? 7 : dims.length <= 12 ? 5 : 4;

  const sorted = useMemo(() => {
    const items = dims.map((dim, i) => ({ dim, value: values[i] ?? 0 }));
    items.sort((a, b) => b.value - a.value);
    return items;
  }, [dims, values]);

  return (
    <div
      className="flex flex-col justify-around py-2 flex-shrink-0 border-r border-white/[0.04]"
      style={{ width: dims.length <= 6 ? 90 : dims.length <= 12 ? 76 : 62 }}
    >
      {sorted.map(({ dim }) => (
        <div key={dim.key} className="flex items-center gap-1.5 px-2">
          <div
            className="flex-shrink-0 rounded-full"
            style={{
              width: dotSize,
              height: dotSize,
              background: dim.color,
              boxShadow: animated ? `0 0 5px ${dim.color}60` : "none",
            }}
          />
          <span
            className="font-display truncate leading-none font-medium"
            style={{ fontSize, color: dim.color, opacity: animated ? 0.9 : 0.7 }}
          >
            {dim.name}
          </span>
        </div>
      ))}
    </div>
  );
}
