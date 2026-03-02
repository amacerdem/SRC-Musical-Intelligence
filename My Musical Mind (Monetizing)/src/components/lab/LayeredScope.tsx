/* ── LayeredScope — Unified layered visualization container ────────────
 *  Stacks SpectralPeaks (WebGL z:0) + FlowOverlay (Canvas 2D z:10)
 *  + interaction layer (z:20) + LayerToggles (z:30) + ScopeTooltip (z:40).
 *
 *  Single source of truth for layer visibility, hover state,
 *  and wheel/click event routing.
 *  ──────────────────────────────────────────────────────────────────── */

import { useState, useCallback, useRef } from "react";
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
import { findNearestPeak } from "./peakExtractor";

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

  /* ── Wheel handler (routed to shared viewport) ─────── */
  const handleWheel = useCallback((e: React.WheelEvent<HTMLDivElement>) => {
    e.stopPropagation();
    const rect = containerRef.current?.getBoundingClientRect();
    if (!rect) return;
    const mouseXFrac = (e.clientX - rect.left) / rect.width;
    viewport.handleWheel(e, mouseXFrac);
  }, [viewport]);

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
      style={{ background: labMode === "acoustic" ? "rgba(14,8,6,1)" : "rgba(6,6,14,1)" }}
      onWheel={handleWheel}
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
        showPeaks={layers.peaks}
        showBloom={layers.bloom}
        showGrid={layers.grid}
      />

      {/* z:10 — Canvas 2D flow curves */}
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

      {/* z:20 — Interaction layer (transparent, receives pointer events) */}
      <div
        className="absolute inset-0 cursor-pointer"
        style={{ zIndex: 20 }}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        onClick={handleClick}
      />

      {/* z:30 — Layer toggles (pointer-events-auto for clicks) */}
      <div style={{ zIndex: 30 }} className="absolute top-0 right-0 pointer-events-auto">
        <LayerToggles layers={layers} onToggle={handleToggle} />
      </div>

      {/* z:40 — Tooltip */}
      <div style={{ zIndex: 40 }} className="absolute inset-x-0 bottom-0 pointer-events-none">
        <ScopeTooltip
          data={tooltipData}
          depth={depth}
          accentColor={accentColor}
          containerW={containerW}
          labMode={labMode}
        />
      </div>
    </div>
  );
}
