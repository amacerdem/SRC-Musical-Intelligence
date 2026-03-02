/* ── LayeredScope — Unified layered visualization container ────────────
 *  Stacks SpectralPeaks (WebGL z:0) + FlowOverlay (Canvas 2D z:10)
 *  + interaction layer (z:20) + LayerToggles (z:30) + ScopeTooltip (z:40).
 *
 *  Single source of truth for layer visibility, hover state,
 *  and wheel/click event routing.
 *  ──────────────────────────────────────────────────────────────────── */

import { useState, useCallback, useRef, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { DepthLevel, TemporalDimensions } from "@/stores/useLabStore";
import type { MITrackDetail } from "@/types/mi-dataset";
import type { MelData, PeakBuffers } from "./peakExtractor";
import type { ViewportState } from "./useViewport";
import type { LabMode, FlowHoverData } from "./FlowOverlay";
import type { ScopeTooltipData, PeakInfo } from "./ScopeTooltip";

import { SpectralPeaks } from "./SpectralPeaks";
import { FlowOverlay } from "./FlowOverlay";
import { LayerToggles, DEFAULT_LAYERS } from "./LayerToggles";
import type { LayerState } from "./LayerToggles";
import { ScopeTooltip } from "./ScopeTooltip";
import { findNearestPeak, findAllPeaksAtTime } from "./peakExtractor";
import type { PeakAtTime } from "./peakExtractor";

/* ── Types ───────────────────────────────────────────────────────────── */

interface Props {
  melData: MelData | null;
  temporal: TemporalDimensions;
  trackDetail: MITrackDetail;
  depth: DepthLevel;
  accentColor: string;
  audioRef: React.RefObject<HTMLAudioElement | null>;
  isPlaying: boolean;
  peakCount: 4 | 8 | 16;
  onSeek: (ratio: number) => void;
  viewport: ViewportState;
  labMode: LabMode;
  peaks: PeakBuffers | null;
}

/* ── Component ──────────────────────────────────────────────────────── */

export function LayeredScope({
  melData, temporal, trackDetail, depth, accentColor,
  audioRef, isPlaying, peakCount, onSeek, viewport,
  labMode, peaks,
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null);

  /* ── Layer state ─────────────────────────────────────── */
  const [layers, setLayers] = useState<LayerState>(DEFAULT_LAYERS);
  const handleToggle = useCallback((key: keyof LayerState) => {
    setLayers(prev => ({ ...prev, [key]: !prev[key] }));
  }, []);

  /* ── Hover state (driven by interaction layer, consumed by FlowOverlay + Tooltip) */
  const [hoverX, setHoverX] = useState<number | null>(null);
  const [containerW, setContainerW] = useState(800);

  /* ── Tooltip state ──────────────────────────────────── */
  const [tooltipData, setTooltipData] = useState<ScopeTooltipData | null>(null);

  /* ── Spectral hover — find all peaks at cursor time ── */
  const [spectralPeaks, setSpectralPeaks] = useState<PeakAtTime[]>([]);
  const [spectralTime, setSpectralTime] = useState("");

  useEffect(() => {
    if (labMode !== "spectral" || hoverX === null || !peaks || !melData) {
      setSpectralPeaks([]);
      setSpectralTime("");
      return;
    }
    const scroll = viewport.scrollRef.current;
    const win = viewport.windowRef.current;
    const time = scroll + (hoverX / containerW) * win;
    const allP = findAllPeaksAtTime(peaks, time, melData.frameRate, peakCount);
    setSpectralPeaks(allP);
    const m = Math.floor(time / 60);
    const s = Math.floor(time % 60);
    const ms = Math.floor((time % 1) * 100);
    setSpectralTime(`${m}:${s.toString().padStart(2, "0")}.${ms.toString().padStart(2, "0")}`);
  }, [labMode, hoverX, containerW, peaks, melData, peakCount, viewport]);

  /* ── Hover data callback from FlowOverlay ───────────── */
  const handleFlowHover = useCallback((data: FlowHoverData | null) => {
    if (!data) {
      setTooltipData(null);
      return;
    }

    // Try to find nearest spectral peak for tooltip
    let peak: PeakInfo | null = null;
    if (peaks && melData) {
      const yFrac = 0.5;
      const nearest = findNearestPeak(peaks, data.time, yFrac, melData.frameRate, peakCount);
      if (nearest) {
        peak = {
          freq: nearest.freq,
          noteName: nearest.noteName,
          amplitude: nearest.amplitude,
          rank: nearest.rank,
        };
      }
    }

    setTooltipData({
      timeStr: data.timeStr,
      dims: data.dims,
      reward: data.reward,
      neuro: data.neuro,
      peak,
      posX: data.canvasX,
    });
  }, [peaks, melData, peakCount]);

  /* ── Native non-passive wheel listener (blocks browser zoom/scroll) ── */
  const viewportRef = useRef(viewport);
  viewportRef.current = viewport;

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      e.stopPropagation();
      const rect = el.getBoundingClientRect();
      const mouseXFrac = (e.clientX - rect.left) / rect.width;
      viewportRef.current.handleWheel(e, mouseXFrac);
    };

    // { passive: false } is critical — allows preventDefault on wheel
    el.addEventListener("wheel", onWheel, { passive: false });
    return () => el.removeEventListener("wheel", onWheel);
  }, []);

  /* ── Block keyboard zoom (Ctrl+Plus/Minus/Zero) ────── */
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && (e.key === "+" || e.key === "-" || e.key === "=" || e.key === "0")) {
        e.preventDefault();
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  /* ── Mouse handlers for interaction layer ──────────── */
  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    const rect = containerRef.current?.getBoundingClientRect();
    if (!rect) return;
    const x = e.clientX - rect.left;
    setHoverX(x);
    setContainerW(rect.width);
  }, []);

  const handleMouseLeave = useCallback(() => {
    setHoverX(null);
    setTooltipData(null);
  }, []);

  const handleClick = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    const rect = containerRef.current?.getBoundingClientRect();
    if (!rect) return;
    const xFrac = (e.clientX - rect.left) / rect.width;
    const time = viewport.handleScopeSeek(xFrac);
    const duration = trackDetail.duration_s;
    onSeek(Math.max(0, Math.min(1, time / duration)));
  }, [viewport, trackDetail, onSeek]);

  const duration = trackDetail.duration_s;

  return (
    <div
      ref={containerRef}
      className="relative w-full h-full overflow-hidden"
      style={{
        background: labMode === "acoustic" ? "rgba(14,8,6,1)" : "rgba(6,6,14,1)",  /* spectral + neuro share dark blue */
        touchAction: "none",
        overscrollBehavior: "none",
      }}
    >
      {/* z:0 — WebGL spectral peaks */}
      <SpectralPeaks
        melData={melData}
        audioRef={audioRef}
        isPlaying={isPlaying}
        duration={duration}
        accentColor={accentColor}
        peakCount={peakCount}
        onSeek={onSeek}
        viewport={viewport}
        showPeaks={labMode === "spectral" ? true : layers.peaks}
        showBloom={labMode === "spectral" ? true : layers.bloom}
        showGrid={labMode === "spectral" ? true : layers.grid}
      />

      {/* z:10 — Canvas 2D flow curves (hidden in spectral mode) */}
      {labMode !== "spectral" && (
        <FlowOverlay
          temporal={temporal}
          trackDetail={trackDetail}
          depth={depth}
          accentColor={accentColor}
          audioRef={audioRef}
          isPlaying={isPlaying}
          viewport={viewport}
          labMode={labMode}
          showCurves={layers.curves}
          showReward={layers.reward}
          showNeuro={layers.neuro}
          hoverX={hoverX}
          hoverContainerW={containerW}
          onHoverData={handleFlowHover}
        />
      )}

      {/* z:20 — Interaction layer (transparent, receives pointer events) */}
      <div
        className="absolute inset-0 cursor-pointer"
        style={{ zIndex: 20 }}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        onClick={handleClick}
      />

      {/* z:30 — Layer toggles (hidden in spectral mode) */}
      {labMode !== "spectral" && (
        <div style={{ zIndex: 30 }} className="absolute top-0 right-0 pointer-events-auto">
          <LayerToggles layers={layers} onToggle={handleToggle} />
        </div>
      )}

      {/* z:40 — Tooltip */}
      {labMode !== "spectral" && (
        <div style={{ zIndex: 40 }} className="absolute inset-x-0 bottom-0 pointer-events-none">
          <ScopeTooltip
            data={tooltipData}
            depth={depth}
            accentColor={accentColor}
            containerW={containerW}
            labMode={labMode}
          />
        </div>
      )}

      {/* z:40 — Spectral hover tooltip */}
      {labMode === "spectral" && hoverX !== null && (
        <div style={{ zIndex: 40 }} className="absolute inset-0 pointer-events-none">
          {/* Vertical scan line */}
          <div
            className="absolute top-0 bottom-0 w-px"
            style={{ left: hoverX, background: "rgba(255,255,255,0.15)" }}
          />

          {/* Peak info card */}
          <AnimatePresence>
            {spectralPeaks.length > 0 && (
              <motion.div
                initial={{ opacity: 0, x: 6 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 6 }}
                transition={{ duration: 0.1 }}
                className="absolute top-3"
                style={{
                  left: hoverX + 16 > containerW - 200 ? hoverX - 196 : hoverX + 16,
                }}
              >
                <div
                  className="rounded-xl px-3.5 py-3 w-[180px]"
                  style={{
                    background: "rgba(6,6,14,0.94)",
                    backdropFilter: "blur(20px)",
                    border: "1px solid rgba(255,255,255,0.08)",
                    boxShadow: "0 8px 32px rgba(0,0,0,0.6)",
                  }}
                >
                  {/* Time */}
                  <div className="text-[10px] font-mono text-slate-500 mb-2.5">
                    {spectralTime}
                  </div>

                  {/* Peak list — high to low */}
                  <div className="space-y-2">
                    {spectralPeaks.map((p, i) => {
                      const cssCol = `rgb(${Math.round(p.color[0] * 255)},${Math.round(p.color[1] * 255)},${Math.round(p.color[2] * 255)})`;
                      return (
                        <div key={i}>
                          <div className="flex items-center gap-2 mb-0.5">
                            <div
                              className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                              style={{ background: cssCol, boxShadow: `0 0 6px ${cssCol}` }}
                            />
                            <span className="text-[13px] font-mono text-white font-semibold">
                              {p.noteName}
                            </span>
                            <span className="flex-1" />
                            <span className="text-[10px] font-mono text-slate-500">
                              #{p.rank + 1}
                            </span>
                          </div>
                          <div className="flex items-center gap-2 pl-[18px]">
                            <span className="text-[10px] font-mono text-slate-400">
                              {p.freq.toFixed(1)} Hz
                            </span>
                            <span className="flex-1" />
                            <div className="w-12 h-[3px] rounded-full bg-white/5 overflow-hidden">
                              <div
                                className="h-full rounded-full"
                                style={{ width: `${p.amplitude * 100}%`, background: cssCol, opacity: 0.7 }}
                              />
                            </div>
                            <span className="text-[9px] font-mono text-slate-600 w-6 text-right">
                              {(p.amplitude * 100).toFixed(0)}
                            </span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
