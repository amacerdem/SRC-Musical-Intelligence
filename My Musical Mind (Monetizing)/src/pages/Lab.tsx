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
      <div className="relative z-10 h-full flex flex-col px-5 sm:px-8 md:px-10 pt-5 pb-20">

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
            {hasAnalysis && hasEverPlayed && (
              <div className="flex items-center gap-1.5 text-slate-500">
                <Clock size={11} />
                <span className="text-[10px] font-mono" style={{ color: `${color}70` }}>
                  {flowTime} / {totalTime}
                </span>
              </div>
            )}
          </div>

          {/* Right: Depth selector */}
          <div className="flex items-center gap-3">
            {hasAnalysis && (
              <span className="text-[8px] font-mono text-slate-700">
                {temporal.source === "full" ? `${temporal.frameCount} frames` : "64 seg"}
              </span>
            )}

            <DepthSelector depth={depth} onChange={setDepth} accentColor={color} />
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
          </motion.div>
        ) : (
          <div className="flex-1 min-h-0 flex items-center justify-center border border-white/[0.04] rounded-xl">
            <div className="flex flex-col items-center gap-3">
              <Waves size={20} className="text-slate-800" />
              <span className="text-[10px] font-display font-light tracking-[0.12em] uppercase text-slate-700">
                {phase === "idle" ? "Select a track to begin analysis" : "Loading..."}
              </span>
            </div>
          </div>
        )}
      </div>

    </motion.div>
  );
}
