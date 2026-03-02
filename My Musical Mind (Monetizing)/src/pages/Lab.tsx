/* ── Lab — Scientific Analysis Studio ────────────────────────────────
 *  Full-screen layered scope: SpectralPeaks (WebGL) + FlowOverlay (Canvas 2D)
 *  stacked with PianoStrip left, WaveformNavigator bottom.
 *
 *  ┌──────────────────────────────────────────────────────────────┐
 *  │  🧪 Lab [Track▾] [Acoustic|Neuro] ▶ 0:42/3:12 [4P] [6D]   │
 *  ├─────┬────────────────────────────────────────────────────────┤
 *  │ 🎹  │  LAYERED SCOPE (flex-1)                               │
 *  │ P   │  ┌ z:0  SpectralPeaks (WebGL peaks + bloom)         ┐ │
 *  │ i   │  │ z:10 FlowOverlay (Canvas 2D neon curves)         │ │
 *  │ a   │  │ z:20 InteractionLayer (hover, seek, scroll, zoom)│ │
 *  │ n   │  │ z:30 LayerToggles (floating pills)               │ │
 *  │ o   │  └ z:40 ScopeTooltip                                ┘ │
 *  ├─────┴────────────────────────────────────────────────────────┤
 *  │  WAVEFORM NAVIGATOR (48px, entire piece)                     │
 *  └──────────────────────────────────────────────────────────────┘
 *  ──────────────────────────────────────────────────────────────────── */

import { useRef, useEffect, useMemo, useState, useCallback } from "react";
import { motion } from "framer-motion";
import {
  FlaskConical, Clock, Music2, Play, Pause,
  ChevronDown, Waves,
} from "lucide-react";

import { useLabStore } from "@/stores/useLabStore";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { pageTransition, fadeIn } from "@/design/animations";
import { miDataService } from "@/services/MIDataService";
import type { MICatalogTrack } from "@/types/mi-dataset";

import { DepthSelector } from "@/components/lab/DepthSelector";
import { LayeredScope } from "@/components/lab/LayeredScope";
import { PianoStrip } from "@/components/lab/PianoStrip";
import { WaveformNavigator } from "@/components/lab/WaveformNavigator";
import { useViewport } from "@/components/lab/useViewport";
import { extractPeaks } from "@/components/lab/peakExtractor";
import type { MelData } from "@/components/lab/peakExtractor";
import type { LabMode } from "@/components/lab/FlowOverlay";
import { LabAgent } from "@/components/lab/LabAgent";

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
    const centerFreqs = new Float32Array(buf, 16, nMels);
    const data = new Uint8Array(buf, 16 + nMels * 4);
    return { nMels, nFrames, frameRate, centerFreqs, data };
  } catch {
    return null;
  }
}

/* ── Decode audio to mono Float32Array for waveform navigator ── */
async function decodeAudioSamples(url: string): Promise<Float32Array | null> {
  try {
    const resp = await fetch(url);
    if (!resp.ok) return null;
    const buf = await resp.arrayBuffer();
    const ctx = new AudioContext();
    const decoded = await ctx.decodeAudioData(buf);
    const mono = decoded.getChannelData(0);
    // Downsample to ~4000 points for waveform drawing
    const targetLen = 4000;
    if (mono.length <= targetLen) return mono;
    const step = mono.length / targetLen;
    const out = new Float32Array(targetLen);
    for (let i = 0; i < targetLen; i++) {
      const idx = Math.floor(i * step);
      out[i] = mono[idx];
    }
    await ctx.close();
    return out;
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
  const duration = trackDetail?.duration_s ?? 0;

  /* ── Block browser zoom/scroll on the entire Lab page ── */
  const pageRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = pageRef.current;
    if (!el) return;

    // Block ctrl+wheel (browser zoom) on the whole page
    const onWheel = (e: WheelEvent) => {
      if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
      }
    };
    el.addEventListener("wheel", onWheel, { passive: false });

    // Block pinch-to-zoom gesture events
    const onGesture = (e: Event) => { e.preventDefault(); };
    el.addEventListener("gesturestart", onGesture);
    el.addEventListener("gesturechange", onGesture);
    el.addEventListener("gestureend", onGesture);

    return () => {
      el.removeEventListener("wheel", onWheel);
      el.removeEventListener("gesturestart", onGesture);
      el.removeEventListener("gesturechange", onGesture);
      el.removeEventListener("gestureend", onGesture);
    };
  }, []);

  /* ── Track catalog ─────────────────────────────── */
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
  const peakCount = 4 as const;
  const [labMode, setLabMode] = useState<LabMode>("spectral");
  const [waveformSamples, setWaveformSamples] = useState<Float32Array | null>(null);

  /* ── Shared viewport (scroll + zoom) ─────────────── */
  const viewport = useViewport(duration);

  /* ── Extracted peaks (memoized) ──────────────────── */
  const peaks = useMemo(() => {
    if (!melData) return null;
    return extractPeaks(melData);
  }, [melData]);

  // Initialize audio element + load mel data + decode waveform when track changes
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.src = "";
    }
    audioRef.current = null;
    setIsPlaying(false);
    setHasEverPlayed(false);
    setFlowIdx(0);
    setMelData(null);
    setWaveformSamples(null);

    if (!trackDetail) return;

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

      // Decode audio for waveform navigator
      decodeAudioSamples(audioUrl).then(setWaveformSamples);
    }

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
    <motion.div
      ref={pageRef}
      {...pageTransition}
      className="relative h-screen overflow-hidden"
      style={{ touchAction: "none", overscrollBehavior: "none" }}
    >

      {/* ── Ambient background ─────────────────────────────────────────── */}
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0" style={{ background: `radial-gradient(ellipse 80% 60% at 50% 20%, ${color}06 0%, transparent 60%)` }} />
        <div className="absolute inset-0" style={{ background: `radial-gradient(ellipse 40% 50% at 10% 90%, rgba(99,102,241,0.02) 0%, transparent 50%)` }} />
        <div className="absolute inset-0" style={{ background: `radial-gradient(ellipse 40% 35% at 90% 80%, rgba(168,85,247,0.02) 0%, transparent 50%)` }} />
      </div>
      <div className="cinematic-vignette z-[2]" />

      {/* ═══ MAIN ═════════════════════════════════════════════════════ */}
      <div className="relative z-10 h-full flex flex-col px-5 sm:px-8 md:px-10 pt-5 pb-4">

        {/* Click-outside overlay for track menu */}
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
            {hasAnalysis && (
              <div className="flex items-center gap-1.5 text-slate-500">
                <Clock size={11} />
                <span className="text-[10px] font-mono" style={{ color: `${color}70` }}>
                  {flowTime || "0:00"} / {totalTime}
                </span>
              </div>
            )}
          </div>

          {/* Right: Frame info */}
          <div className="flex items-center gap-3">
            {hasAnalysis && (
              <span className="text-[8px] font-mono text-slate-700">
                {temporal.source === "full" ? `${temporal.frameCount} frames` : "64 seg"}
              </span>
            )}
          </div>
        </motion.div>

        {/* ── LAYERED SCOPE + NAVIGATOR ─────────────────────────────── */}
        {hasAnalysis ? (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.6 }}
            className="flex-1 min-h-0 flex flex-col"
          >
            {/* Scope + PianoStrip */}
            <div className="flex-1 min-h-0 flex border border-white/[0.04] rounded-t-xl overflow-hidden">
              <PianoStrip />
              <LayeredScope
                melData={melData}
                temporal={temporal}
                trackDetail={trackDetail}
                depth={depth}
                accentColor={color}
                audioRef={audioRef}
                isPlaying={isPlaying}
                peakCount={peakCount}
                onSeek={handleSeek}
                viewport={viewport}
                labMode={labMode}
                peaks={peaks}
              />
            </div>

            {/* Waveform Navigator */}
            <div className="border border-t-0 border-white/[0.04] rounded-b-xl overflow-hidden">
              <WaveformNavigator
                audioRef={audioRef}
                duration={duration}
                viewport={viewport}
                accentColor={color}
                samples={waveformSamples}
              />
            </div>

            {/* Controls below waveform — orb left, mode+depth center */}
            <div className="flex items-center pt-2">
              {/* Left: M³ Agent orb */}
              <div className="flex-1 flex justify-start pl-2">
                <LabAgent accentColor={color} trackDetail={trackDetail} melData={melData} temporal={temporal} />
              </div>

              {/* Center: Mode + Depth stacked */}
              <div className="flex flex-col items-center gap-2">
                {/* Mode selector — primary, larger */}
                <div className="flex items-center rounded-2xl overflow-hidden"
                  style={{
                    border: "1px solid rgba(255,255,255,0.12)",
                    background: "rgba(0,0,0,0.35)",
                    backdropFilter: "blur(16px)",
                    boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
                  }}
                >
                  {([
                    { key: "spectral" as const, label: "Spectral", col: "#60a5fa" },
                    { key: "acoustic" as const, label: "Acoustic", col: "#FF6B35" },
                    { key: "neuro" as const, label: "NeuroAcoustic", col: color },
                  ]).map((mode, i) => {
                    const active = labMode === mode.key;
                    return (
                      <button
                        key={mode.key}
                        onClick={() => setLabMode(mode.key)}
                        className="relative px-6 py-2.5 text-[13px] font-display font-bold tracking-[0.08em] uppercase transition-all duration-300"
                        style={{
                          background: active ? `${mode.col}20` : "transparent",
                          color: active ? mode.col : "rgba(255,255,255,0.25)",
                          borderRight: i < 2 ? "1px solid rgba(255,255,255,0.06)" : "none",
                          boxShadow: active ? `inset 0 -2.5px 0 ${mode.col}, 0 0 20px ${mode.col}15` : "none",
                          textShadow: active ? `0 0 12px ${mode.col}60` : "none",
                        }}
                      >
                        {mode.label}
                      </button>
                    );
                  })}
                </div>

                {/* Depth selector — secondary, smaller */}
                <DepthSelector depth={depth} onChange={setDepth} accentColor={color} />
              </div>

              {/* Right: balance spacer */}
              <div className="flex-1" />
            </div>
          </motion.div>
        ) : (
          <div className="flex-1 min-h-0 flex items-center justify-center">
            {phase !== "idle" ? (
              /* Loading state */
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex flex-col items-center gap-4"
              >
                <div
                  className="w-12 h-12 rounded-2xl flex items-center justify-center animate-pulse"
                  style={{ background: `${color}12`, border: `1px solid ${color}20` }}
                >
                  <FlaskConical size={22} style={{ color: `${color}80` }} />
                </div>
                <span className="text-xs font-display text-slate-500 tracking-wider">Analyzing...</span>
              </motion.div>
            ) : (
              /* Welcome state */
              <motion.div
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, ease: "easeOut" }}
                className="flex flex-col items-center max-w-2xl w-full px-4"
              >
                {/* Icon */}
                <div
                  className="w-16 h-16 rounded-2xl flex items-center justify-center mb-5"
                  style={{
                    background: `linear-gradient(135deg, ${color}10, ${color}05)`,
                    border: `1px solid ${color}15`,
                    boxShadow: `0 8px 32px ${color}08`,
                  }}
                >
                  <FlaskConical size={28} style={{ color: `${color}50` }} />
                </div>

                {/* Title */}
                <h2 className="text-xl font-display font-bold text-white/85 mb-1.5 tracking-tight">
                  Welcome to your Mind Lab
                </h2>
                <p className="text-[13px] font-display text-slate-500 mb-8 text-center leading-relaxed max-w-sm">
                  Explore how your brain processes music through spectral,
                  acoustic, and neuroacoustic analysis.
                </p>

                {/* Prompt */}
                <span className="text-[9px] font-display text-slate-600 uppercase tracking-[0.15em] mb-3">
                  Choose a piece to explore
                </span>

                {/* Track cards */}
                <div
                  className="w-full max-h-[42vh] overflow-y-auto rounded-xl"
                  style={{
                    scrollbarWidth: "thin",
                    scrollbarColor: `${color}30 transparent`,
                  }}
                >
                  <div className="space-y-1.5 p-1">
                    {labTracks.map((track) => {
                      const mins = Math.floor(track.duration_s / 60);
                      const secs = Math.floor(track.duration_s % 60).toString().padStart(2, "0");
                      return (
                        <button
                          key={track.id}
                          onClick={() => handleTrackSelect(track)}
                          className="w-full flex items-center gap-3.5 px-4 py-3 rounded-xl text-left transition-all group hover:scale-[1.01]"
                          style={{
                            background: "rgba(255,255,255,0.015)",
                            border: "1px solid rgba(255,255,255,0.04)",
                          }}
                          onMouseEnter={(e) => {
                            e.currentTarget.style.background = `${color}08`;
                            e.currentTarget.style.borderColor = `${color}18`;
                          }}
                          onMouseLeave={(e) => {
                            e.currentTarget.style.background = "rgba(255,255,255,0.015)";
                            e.currentTarget.style.borderColor = "rgba(255,255,255,0.04)";
                          }}
                        >
                          {/* Album art placeholder */}
                          <div
                            className="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                            style={{ background: `${color}0A` }}
                          >
                            <Music2 size={15} style={{ color: `${color}50` }} />
                          </div>

                          {/* Info */}
                          <div className="flex-1 min-w-0">
                            <div className="text-[13px] font-display text-slate-300 group-hover:text-white truncate transition-colors">
                              {track.title}
                            </div>
                            <div className="text-[11px] text-slate-600 truncate">
                              {track.artist}
                            </div>
                          </div>

                          {/* Duration */}
                          <span className="text-[10px] font-mono text-slate-700 flex-shrink-0">
                            {mins}:{secs}
                          </span>
                        </button>
                      );
                    })}
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        )}
      </div>

    </motion.div>
  );
}
