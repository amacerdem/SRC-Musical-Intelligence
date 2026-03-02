/* ── FlowOverlay — Canvas 2D dimension curves overlay ──────────────────
 *  Transparent Canvas 2D layer drawn over the WebGL SpectralPeaks.
 *  Reads scroll/zoom from shared ViewportState (no internal scroll).
 *  Renders neon Catmull-Rom curves, reward heatmap, neurochemical strips.
 *
 *  pointer-events: none — all interaction handled by parent LayeredScope.
 *
 *  Refactored from FlowTimeline.tsx: removed left strip, tooltip,
 *  playhead, and internal scroll state.
 *  ──────────────────────────────────────────────────────────────────── */

import { useRef, useEffect, useState, useMemo, useCallback } from "react";
import type { DepthLevel, TemporalDimensions } from "@/stores/useLabStore";
import type { MITrackDetail } from "@/types/mi-dataset";
import type { ViewportState } from "./useViewport";
import type { TooltipDim } from "./ScopeTooltip";
import {
  getLabDim,
  ALL_PSYCHOLOGY,
  ALL_COGNITION,
  ALL_NEUROSCIENCE,
  ALL_ACOUSTIC_6D,
  ALL_ACOUSTIC_12D,
  ALL_ACOUSTIC_24D,
  ACOUSTIC_R3_6D,
  ACOUSTIC_R3_12D,
  ACOUSTIC_R3_24D,
} from "@/data/dimensions";

export type LabMode = "neuro" | "acoustic";

/* ── Constants ───────────────────────────────────────────────────────── */

const NEURO_LABELS = ["DA", "NE", "OPI", "5HT"] as const;
const NEURO_COLORS = ["#22C55E", "#EF4444", "#38BDF8", "#A855F7"] as const;
const INITIAL_WINDOW = 12;

/* ── Helpers ─────────────────────────────────────────────────────────── */

function baseHex(col: string): string {
  if (col.length === 9) return col.slice(0, 7);
  return col;
}

function cr(p0: number, p1: number, p2: number, p3: number, t: number): number {
  const t2 = t * t, t3 = t2 * t;
  return 0.5 * (
    2 * p1 +
    (-p0 + p2) * t +
    (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
    (-p0 + 3 * p1 - 3 * p2 + p3) * t3
  );
}

function lerpSeg(arr: number[], time: number, duration: number): number {
  if (!arr || arr.length === 0) return 0;
  const ratio = Math.max(0, Math.min(1, time / Math.max(0.001, duration)));
  const fidx = ratio * (arr.length - 1);
  const lo = Math.floor(fidx);
  const hi = Math.min(arr.length - 1, lo + 1);
  const t = fidx - lo;
  return arr[lo] * (1 - t) + arr[hi] * t;
}

function lerpSeg2D(arr: number[][], time: number, duration: number): number[] {
  if (!arr || arr.length === 0) return [0, 0, 0, 0];
  const ratio = Math.max(0, Math.min(1, time / Math.max(0.001, duration)));
  const fidx = ratio * (arr.length - 1);
  const lo = Math.floor(fidx);
  const hi = Math.min(arr.length - 1, lo + 1);
  const t = fidx - lo;
  return arr[lo].map((v, i) => v * (1 - t) + (arr[hi]?.[i] ?? v) * t);
}

/* ── Types ───────────────────────────────────────────────────────────── */

export interface FlowHoverData {
  canvasX: number;
  time: number;
  segIdx: number;
  dims: TooltipDim[];
  reward: number;
  neuro: number[];
  timeStr: string;
}

interface Props {
  temporal: TemporalDimensions;
  trackDetail: MITrackDetail;
  depth: DepthLevel;
  accentColor: string;
  audioRef: React.RefObject<HTMLAudioElement | null>;
  isPlaying: boolean;
  viewport: ViewportState;
  labMode: LabMode;
  showCurves: boolean;
  showReward: boolean;
  showNeuro: boolean;
  /** Mouse X in container pixels, or null if not hovering */
  hoverX: number | null;
  hoverContainerW: number;
  onHoverData: (data: FlowHoverData | null) => void;
}

/* ════════════════════════════════════════════════════════════════════════
 *  FlowOverlay — Main Component
 * ════════════════════════════════════════════════════════════════════════ */

export function FlowOverlay({
  temporal, trackDetail, depth, accentColor,
  audioRef, isPlaying, viewport, labMode,
  showCurves, showReward, showNeuro,
  hoverX, hoverContainerW, onHoverData,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ w: 1200, h: 400 });
  const rafRef = useRef(0);
  const hoverRef = useRef<{ canvasX: number; time: number; segIdx: number } | null>(null);

  /* ── Derived constants ────────────────────────────────── */
  const segCount = temporal.segments.length;
  const duration = trackDetail.duration_s;
  const segDur = duration / Math.max(1, segCount - 1);
  const dpr = typeof window !== "undefined" ? Math.min(window.devicePixelRatio || 1, 2) : 1;

  const dimList = useMemo(() => {
    if (labMode === "acoustic") {
      return depth === 6 ? ALL_ACOUSTIC_6D : depth === 12 ? ALL_ACOUSTIC_12D : ALL_ACOUSTIC_24D;
    }
    return depth === 6 ? ALL_PSYCHOLOGY : depth === 12 ? ALL_COGNITION : ALL_NEUROSCIENCE;
  }, [depth, labMode]);
  const dimCount = dimList.length;

  const getDimValues = useCallback((segIdx: number): number[] => {
    if (labMode === "acoustic") {
      const r3 = temporal.r3Segments;
      if (!r3 || r3.length === 0) return new Array(dimCount).fill(0);
      const ratio = segIdx / Math.max(1, segCount - 1);
      const r3Idx = Math.min(r3.length - 1, Math.round(ratio * (r3.length - 1)));
      const r3seg = r3[r3Idx];
      if (!r3seg) return new Array(dimCount).fill(0);
      const indices = depth === 6 ? ACOUSTIC_R3_6D : depth === 12 ? ACOUSTIC_R3_12D : ACOUSTIC_R3_24D;
      return indices.map(i => r3seg[i] ?? 0);
    }
    const s = temporal.segments[segIdx];
    if (!s) return [];
    if (depth === 6) return s.psychology;
    if (depth === 12) return s.cognition;
    return s.neuroscience;
  }, [temporal, depth, labMode, dimCount, segCount]);

  const neuroArr = trackDetail.temporal_profile.neuro_per_segment;
  const rewardArr = trackDetail.temporal_profile.reward_per_segment;

  /* ── Auto-scale ────────────────────────────────────────── */
  const { dataMin, dataMax } = useMemo(() => {
    let lo = Infinity, hi = -Infinity;
    for (let s = 0; s < segCount; s++) {
      const vals = getDimValues(s);
      for (let d = 0; d < dimCount; d++) {
        const v = vals[d] ?? 0;
        if (v < lo) lo = v;
        if (v > hi) hi = v;
      }
    }
    if (!isFinite(lo) || !isFinite(hi) || lo === hi) return { dataMin: 0, dataMax: 1 };
    const pad = (hi - lo) * 0.08;
    return { dataMin: Math.max(0, lo - pad), dataMax: Math.min(1, hi + pad) };
  }, [segCount, dimCount, getDimValues]);

  /* ── ResizeObserver ───────────────────────────────────── */
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const ro = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect;
      setSize({ w: Math.round(width), h: Math.round(height) });
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  /* ── Sync canvas pixel size ──────────────────────────── */
  useEffect(() => {
    const c = canvasRef.current;
    if (!c) return;
    c.width = size.w * dpr;
    c.height = size.h * dpr;
  }, [size, dpr]);

  /* ── Draw function ───────────────────────────────────── */
  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const W = size.w, H = size.h;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    // No left strip — full width
    const MT = 10, MB = 16, ML = 0, MR = 0;
    const cW = W - ML - MR;
    const cH = H - MT - MB;

    // Read shared viewport
    const sT = viewport.scrollRef.current;
    const windowDur = viewport.windowRef.current;

    const t2x = (t: number) => ML + ((t - sT) / windowDur) * cW;
    const range = dataMax - dataMin || 1;
    const v2y = (v: number) => MT + cH * (1 - (v - dataMin) / range);

    /* ── Clear (transparent) ─────────────────────────── */
    ctx.clearRect(0, 0, W, H);

    const isAcoustic = labMode === "acoustic";

    /* ── 1. Reward heat-map (NeuroAcoustic, showReward) ── */
    if (!isAcoustic && showReward && rewardArr && rewardArr.length > 0) {
      const stripW = Math.max(2, cW / 120);
      for (let x = ML; x < ML + cW; x += stripW) {
        const t = sT + ((x - ML) / cW) * windowDur;
        const r = lerpSeg(rewardArr, t, duration);
        const a = Math.max(0, Math.min(0.03, r * 0.05));
        ctx.fillStyle = `rgba(255,200,100,${a})`;
        ctx.fillRect(x, MT, stripW + 0.5, cH);
      }
    }

    /* ── 2. Vertical time markers ────────────────────── */
    const tStep = windowDur < 10 ? 1 : windowDur < 30 ? 2 : windowDur < 120 ? 5 : 10;
    const tStart = Math.ceil(sT / tStep) * tStep;
    ctx.textAlign = "center";
    for (let t = tStart; t <= sT + windowDur + 0.01; t += tStep) {
      const x = t2x(t);
      if (x < ML - 5 || x > ML + cW + 5) continue;
      ctx.strokeStyle = "rgba(255,255,255,0.03)";
      ctx.lineWidth = 0.5;
      ctx.beginPath(); ctx.moveTo(x, MT); ctx.lineTo(x, MT + cH); ctx.stroke();
      const m = Math.floor(t / 60), s = Math.floor(t % 60);
      ctx.fillStyle = "rgba(255,255,255,0.15)";
      ctx.font = "7px 'JetBrains Mono', monospace";
      ctx.fillText(`${m}:${s.toString().padStart(2, "0")}`, x, H - 4);
    }

    /* ── 3. Neurochemical strips (NeuroAcoustic, showNeuro) ── */
    if (!isAcoustic && showNeuro && neuroArr && neuroArr.length > 0 && depth >= 12) {
      const stripH = 2;
      const baseY = MT + cH - NEURO_COLORS.length * (stripH + 1);
      for (let ni = 0; ni < NEURO_COLORS.length; ni++) {
        const y = baseY + ni * (stripH + 1);
        for (let x = ML; x < ML + cW; x += 3) {
          const t = sT + ((x - ML) / cW) * windowDur;
          const nv = lerpSeg2D(neuroArr, t, duration);
          const val = nv[ni] ?? 0;
          ctx.fillStyle = NEURO_COLORS[ni] + Math.round(val * 40 + 5).toString(16).padStart(2, "0");
          ctx.fillRect(x, y, 3, stripH);
        }
      }
    }

    /* ── 4. Dimension curves — neon glow ─────────────── */
    if (showCurves) {
      const seg0 = Math.max(0, Math.floor(sT / segDur) - 2);
      const seg1 = Math.min(segCount - 1, Math.ceil((sT + windowDur) / segDur) + 2);

      // Zoom-relative curve width
      const zoomScale = Math.sqrt(INITIAL_WINDOW / Math.max(2, windowDur));
      const coreWidth = (depth <= 6 ? 1.5 : depth <= 12 ? 1 : 0.65) * Math.max(0.4, Math.min(2, zoomScale));

      for (let d = dimCount - 1; d >= 0; d--) {
        const dim = dimList[d];
        if (!dim) continue;
        const col = baseHex(dim.color);

        const pts: { x: number; y: number; v: number }[] = [];
        for (let s = seg0; s <= seg1; s++) {
          const vals = getDimValues(s);
          const v = vals[d] ?? 0;
          pts.push({ x: t2x(s * segDur), y: v2y(v), v });
        }
        if (pts.length < 2) continue;

        // Catmull-Rom spline
        const sp: { x: number; y: number; v: number }[] = [];
        const p = [pts[0], ...pts, pts[pts.length - 1]];
        const res = 14;
        for (let i = 1; i < p.length - 2; i++) {
          for (let t = 0; t <= res; t++) {
            const tt = t / res;
            sp.push({
              x: cr(p[i - 1].x, p[i].x, p[i + 1].x, p[i + 2].x, tt),
              y: cr(p[i - 1].y, p[i].y, p[i + 1].y, p[i + 2].y, tt),
              v: cr(p[i - 1].v, p[i].v, p[i + 1].v, p[i + 2].v, tt),
            });
          }
        }
        if (sp.length < 2) continue;

        // Area fill
        const ag = ctx.createLinearGradient(0, MT, 0, MT + cH);
        ag.addColorStop(0, col + "10");
        ag.addColorStop(1, col + "01");
        ctx.beginPath();
        ctx.moveTo(sp[0].x, sp[0].y);
        for (let i = 1; i < sp.length; i++) ctx.lineTo(sp[i].x, sp[i].y);
        ctx.lineTo(sp[sp.length - 1].x, MT + cH);
        ctx.lineTo(sp[0].x, MT + cH);
        ctx.closePath();
        ctx.fillStyle = ag;
        ctx.fill();

        // Neon glow passes
        const CHUNK = 25;
        ctx.lineCap = "round";
        ctx.lineJoin = "round";

        for (let start = 0; start < sp.length - 1; start += CHUNK) {
          const end = Math.min(sp.length - 1, start + CHUNK);
          let avgV = 0;
          for (let i = start; i <= end; i++) {
            avgV += Math.max(0, Math.min(1, (sp[i].v - dataMin) / range));
          }
          avgV /= (end - start + 1);
          const glow = Math.pow(avgV, 0.7);
          if (glow < 0.08) continue;

          const outerA = Math.round(glow * 40);
          if (outerA > 2) {
            ctx.beginPath();
            ctx.moveTo(sp[start].x, sp[start].y);
            for (let i = start + 1; i <= end; i++) ctx.lineTo(sp[i].x, sp[i].y);
            ctx.shadowBlur = 6 + glow * 14;
            ctx.shadowColor = col;
            ctx.strokeStyle = col + outerA.toString(16).padStart(2, "0");
            ctx.lineWidth = (depth <= 6 ? 4 + glow * 4 : depth <= 12 ? 3 + glow * 3 : 2 + glow * 2) * zoomScale;
            ctx.stroke();
          }
        }

        ctx.shadowBlur = 0;
        ctx.shadowColor = "transparent";

        // Core line
        ctx.beginPath();
        ctx.moveTo(sp[0].x, sp[0].y);
        for (let i = 1; i < sp.length; i++) ctx.lineTo(sp[i].x, sp[i].y);
        ctx.strokeStyle = col + "D0";
        ctx.lineWidth = coreWidth;
        ctx.stroke();

        // Dim label at left edge of visible curve
        if (sp.length > 0 && d < (depth <= 6 ? 6 : depth <= 12 ? 12 : 8)) {
          const labelPt = sp[0];
          if (labelPt.x < W * 0.15) {
            ctx.font = `500 ${depth <= 6 ? 8 : 6}px 'JetBrains Mono', monospace`;
            ctx.textAlign = "left";
            ctx.textBaseline = "middle";
            ctx.fillStyle = col + "90";
            const maxChars = depth <= 6 ? 7 : 5;
            const name = dim.name.length > maxChars ? dim.name.slice(0, maxChars) : dim.name;
            ctx.fillText(name, Math.max(4, labelPt.x + 4), labelPt.y);
          }
        }
      }
    }

    /* ── 5. Hover crosshair + dots ──────────────────── */
    const hv = hoverRef.current;
    if (hv && showCurves) {
      const hx = hv.canvasX;
      ctx.beginPath();
      ctx.moveTo(hx, MT);
      ctx.lineTo(hx, MT + cH);
      ctx.strokeStyle = "rgba(255,255,255,0.12)";
      ctx.lineWidth = 0.5;
      ctx.setLineDash([4, 4]);
      ctx.stroke();
      ctx.setLineDash([]);

      const vals = getDimValues(hv.segIdx);
      const sx = t2x(hv.segIdx * segDur);
      for (let d = 0; d < Math.min(dimCount, vals.length); d++) {
        const dm = dimList[d];
        if (!dm) continue;
        const dc = baseHex(dm.color);
        const y = v2y(vals[d] ?? 0);
        ctx.beginPath();
        ctx.arc(sx, y, depth <= 6 ? 5 : 3.5, 0, Math.PI * 2);
        ctx.fillStyle = dc + "30";
        ctx.fill();
        ctx.beginPath();
        ctx.arc(sx, y, depth <= 6 ? 3 : 2, 0, Math.PI * 2);
        ctx.fillStyle = dc;
        ctx.fill();
        ctx.strokeStyle = "rgba(0,0,0,0.5)";
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }, [
    size, dpr, temporal, depth, dimCount, dimList, segCount, segDur,
    duration, accentColor, rewardArr, neuroArr, getDimValues,
    dataMin, dataMax, labMode, viewport, showCurves, showReward, showNeuro,
  ]);

  /* ── Sync hover from prop ───────────────────────────── */
  useEffect(() => {
    if (hoverX === null || hoverContainerW <= 0) {
      hoverRef.current = null;
      onHoverData(null);
      return;
    }
    const windowDur = viewport.windowRef.current;
    const sT = viewport.scrollRef.current;
    const t = sT + (hoverX / hoverContainerW) * windowDur;
    const si = Math.max(0, Math.min(segCount - 1, Math.round(t / segDur)));
    hoverRef.current = { canvasX: (hoverX / hoverContainerW) * size.w, time: t, segIdx: si };

    // Build tooltip data
    const vals = getDimValues(si);
    if (!vals || vals.length === 0) { onHoverData(null); return; }

    const dims: TooltipDim[] = vals.map((v, i) => {
      const dim = dimList[i];
      if (labMode === "acoustic") {
        return { name: dim?.name ?? `A${i}`, value: v, color: baseHex(dim?.color ?? "#FF6B35") };
      }
      const parentList = depth === 12 ? ALL_PSYCHOLOGY : depth === 24 ? ALL_COGNITION : undefined;
      const pk = dim && "parentKey" in dim ? (dim as { parentKey?: string }).parentKey : undefined;
      const parent = pk ? parentList?.find((p: { key: string }) => p.key === pk) : undefined;
      return { name: dim?.name ?? `D${i}`, value: v, color: baseHex(dim?.color ?? "#94A3B8"), parentName: parent?.name };
    });

    const m = Math.floor(t / 60), s = Math.floor(t % 60);
    const neuro = labMode === "neuro" && neuroArr ? lerpSeg2D(neuroArr, t, duration) : [0, 0, 0, 0];
    const reward = labMode === "neuro" && rewardArr ? lerpSeg(rewardArr, t, duration) : 0;

    onHoverData({
      canvasX: hoverX,
      time: t,
      segIdx: si,
      dims,
      reward,
      neuro,
      timeStr: `${m}:${s.toString().padStart(2, "0")}`,
    });
  }, [hoverX, hoverContainerW, viewport, segCount, segDur, size, getDimValues, dimList, depth, labMode, neuroArr, rewardArr, duration, onHoverData]);

  /* ── rAF Loop (reads from shared viewport, no scroll logic) ── */
  useEffect(() => {
    let running = true;
    const loop = () => {
      if (!running) return;
      draw();
      rafRef.current = requestAnimationFrame(loop);
    };
    rafRef.current = requestAnimationFrame(loop);
    return () => { running = false; cancelAnimationFrame(rafRef.current); };
  }, [draw]);

  return (
    <div
      ref={containerRef}
      className="absolute inset-0 pointer-events-none"
      style={{ zIndex: 10 }}
    >
      <canvas
        ref={canvasRef}
        style={{ width: "100%", height: "100%" }}
        />
    </div>
  );
}
