/* ── FlowTimeline — Canvas-based 60fps Flow Visualization ─────────────
 *  24-second scrolling window with smooth Catmull-Rom curves,
 *  reward heat-map, glow effects, and depth-layered hover tooltips.
 *
 *  Playhead driven by requestAnimationFrame for 60fps smoothness.
 *  Scroll auto-follows playhead during playback; manual wheel/drag
 *  when paused. Seek via click.
 *
 *  Tooltip layers:
 *    6D  Psychology   — experiential labels, mini bars, 0-1 values
 *    12D Cognition    — grouped by 6D parent, + neurochemicals
 *    24D Neuroscience — compact 2-col grid, full neural detail
 *  ──────────────────────────────────────────────────────────────────── */

import { useRef, useEffect, useState, useMemo, useCallback } from "react";
import { AnimatePresence, motion } from "framer-motion";
import type { DepthLevel, TemporalDimensions } from "@/stores/useLabStore";
import type { MITrackDetail } from "@/types/mi-dataset";
import {
  getLabDim,
  ALL_PSYCHOLOGY,
  ALL_COGNITION,
  ALL_NEUROSCIENCE,
} from "@/data/dimensions";

/* ── Constants ───────────────────────────────────────────────────────── */

const WINDOW_DURATION = 24; // seconds visible at once
const NEURO_LABELS = ["DA", "NE", "OPI", "5HT"] as const;
const NEURO_COLORS = ["#22C55E", "#EF4444", "#38BDF8", "#A855F7"] as const;
const PLAYHEAD_ANCHOR = 0.3; // playhead stays at 30% from left

/* ── Types ───────────────────────────────────────────────────────────── */

interface HoverInfo {
  canvasX: number;
  time: number;
  segIdx: number;
}

interface TooltipDim {
  name: string;
  value: number;
  color: string;
  parentName?: string;
}

interface TooltipData {
  timeStr: string;
  dims: TooltipDim[];
  reward: number;
  neuro: number[];
  posX: number; // canvas-space X
}

interface Props {
  temporal: TemporalDimensions;
  trackDetail: MITrackDetail;
  depth: DepthLevel;
  accentColor: string;
  audioRef: React.RefObject<HTMLAudioElement | null>;
  isPlaying: boolean;
  onSeek: (ratio: number) => void;
}

/* ── Helpers ─────────────────────────────────────────────────────────── */

/** Catmull-Rom scalar interpolation */
function cr(p0: number, p1: number, p2: number, p3: number, t: number): number {
  const t2 = t * t, t3 = t2 * t;
  return 0.5 * (
    2 * p1 +
    (-p0 + p2) * t +
    (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
    (-p0 + 3 * p1 - 3 * p2 + p3) * t3
  );
}

/** Interpolate from N-segment array to arbitrary time */
function lerpSeg(arr: number[], time: number, duration: number): number {
  if (!arr || arr.length === 0) return 0;
  const ratio = Math.max(0, Math.min(1, time / Math.max(0.001, duration)));
  const fidx = ratio * (arr.length - 1);
  const lo = Math.floor(fidx);
  const hi = Math.min(arr.length - 1, lo + 1);
  const t = fidx - lo;
  return arr[lo] * (1 - t) + arr[hi] * t;
}

/** Interpolate 2D array (e.g. neuro_per_segment) */
function lerpSeg2D(arr: number[][], time: number, duration: number): number[] {
  if (!arr || arr.length === 0) return [0, 0, 0, 0];
  const ratio = Math.max(0, Math.min(1, time / Math.max(0.001, duration)));
  const fidx = ratio * (arr.length - 1);
  const lo = Math.floor(fidx);
  const hi = Math.min(arr.length - 1, lo + 1);
  const t = fidx - lo;
  return arr[lo].map((v, i) => v * (1 - t) + (arr[hi]?.[i] ?? v) * t);
}

/* ════════════════════════════════════════════════════════════════════════
 *  FlowTimeline — Main Component
 * ════════════════════════════════════════════════════════════════════════ */

export function FlowTimeline({
  temporal, trackDetail, depth, accentColor,
  audioRef, isPlaying, onSeek,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ w: 1200, h: 220 });
  const [tooltipData, setTooltipData] = useState<TooltipData | null>(null);

  /* ── Refs for animation (no re-renders) ───────────────── */
  const scrollRef = useRef(0);
  const targetScrollRef = useRef(0);
  const hoverRef = useRef<HoverInfo | null>(null);
  const rafRef = useRef(0);

  /* ── Derived constants ────────────────────────────────── */
  const segCount = temporal.segments.length;
  const duration = trackDetail.duration_s;
  const segDur = duration / Math.max(1, segCount - 1);
  const windowDur = Math.min(WINDOW_DURATION, duration);
  const dpr = typeof window !== "undefined" ? Math.min(window.devicePixelRatio || 1, 2) : 1;

  const dimCount = depth;
  const dimList = useMemo(() => {
    if (depth === 6) return ALL_PSYCHOLOGY;
    if (depth === 12) return ALL_COGNITION;
    return ALL_NEUROSCIENCE;
  }, [depth]);

  const getDimValues = useCallback((segIdx: number): number[] => {
    const s = temporal.segments[segIdx];
    if (!s) return [];
    if (depth === 6) return s.psychology;
    if (depth === 12) return s.cognition;
    return s.neuroscience;
  }, [temporal, depth]);

  const neuroArr = trackDetail.temporal_profile.neuro_per_segment;
  const rewardArr = trackDetail.temporal_profile.reward_per_segment;

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
  const draw = useCallback((currentTime: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const W = size.w, H = size.h;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    const MT = 10, MB = 20, ML = 0, MR = 0;
    const cW = W - ML - MR;
    const cH = H - MT - MB;
    const sT = scrollRef.current;

    const t2x = (t: number) => ML + ((t - sT) / windowDur) * cW;
    const v2y = (v: number) => MT + cH * (1 - Math.max(0, Math.min(1, v)));

    /* ── Clear ───────────────────────────────────────── */
    ctx.clearRect(0, 0, W, H);

    /* ── 1. Reward heat-map background ───────────────── */
    if (rewardArr && rewardArr.length > 0) {
      const stripW = Math.max(2, cW / 120);
      for (let x = ML; x < ML + cW; x += stripW) {
        const t = sT + ((x - ML) / cW) * windowDur;
        const r = lerpSeg(rewardArr, t, duration);
        const a = Math.max(0, Math.min(0.07, r * 0.1));
        ctx.fillStyle = `rgba(255,200,100,${a})`;
        ctx.fillRect(x, MT, stripW + 0.5, cH);
      }
    }

    /* ── 2. Grid ─────────────────────────────────────── */
    // Horizontal
    ctx.lineWidth = 0.5;
    for (const v of [0.25, 0.5, 0.75]) {
      const y = v2y(v);
      ctx.strokeStyle = "rgba(255,255,255,0.04)";
      ctx.beginPath(); ctx.moveTo(ML, y); ctx.lineTo(ML + cW, y); ctx.stroke();
    }
    // Y-axis labels
    ctx.fillStyle = "rgba(255,255,255,0.08)";
    ctx.font = "7px monospace";
    ctx.textAlign = "right";
    for (const v of [0.25, 0.5, 0.75, 1.0]) {
      ctx.fillText(v.toFixed(1), ML + cW - 3, v2y(v) + 3);
    }
    // Base axis
    ctx.strokeStyle = "rgba(255,255,255,0.06)";
    ctx.beginPath(); ctx.moveTo(ML, MT + cH); ctx.lineTo(ML + cW, MT + cH); ctx.stroke();

    // Vertical time markers
    const tStep = windowDur <= 8 ? 1 : windowDur <= 16 ? 2 : 4;
    const tStart = Math.ceil(sT / tStep) * tStep;
    ctx.textAlign = "center";
    for (let t = tStart; t <= sT + windowDur + 0.01; t += tStep) {
      const x = t2x(t);
      if (x < ML - 5 || x > ML + cW + 5) continue;
      ctx.strokeStyle = "rgba(255,255,255,0.03)";
      ctx.lineWidth = 0.5;
      ctx.beginPath(); ctx.moveTo(x, MT); ctx.lineTo(x, MT + cH); ctx.stroke();
      const m = Math.floor(t / 60), s = Math.floor(t % 60);
      ctx.fillStyle = "rgba(255,255,255,0.18)";
      ctx.font = "8px monospace";
      ctx.fillText(`${m}:${s.toString().padStart(2, "0")}`, x, H - 5);
    }

    /* ── 3. Neurochemical indicator strips (bottom) ──── */
    if (neuroArr && neuroArr.length > 0 && depth >= 12) {
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

    /* ── 4. Dimension curves ─────────────────────────── */
    const seg0 = Math.max(0, Math.floor(sT / segDur) - 2);
    const seg1 = Math.min(segCount - 1, Math.ceil((sT + windowDur) / segDur) + 2);

    for (let d = dimCount - 1; d >= 0; d--) {
      const dim = dimList[d];
      if (!dim) continue;
      const col = dim.color;

      // Data points
      const pts: { x: number; y: number }[] = [];
      for (let s = seg0; s <= seg1; s++) {
        const vals = getDimValues(s);
        pts.push({ x: t2x(s * segDur), y: v2y(vals[d] ?? 0) });
      }
      if (pts.length < 2) continue;

      // Catmull-Rom spline
      const sp: { x: number; y: number }[] = [];
      const p = [pts[0], ...pts, pts[pts.length - 1]];
      const res = 14; // sub-segments
      for (let i = 1; i < p.length - 2; i++) {
        for (let t = 0; t <= res; t++) {
          const tt = t / res;
          sp.push({
            x: cr(p[i - 1].x, p[i].x, p[i + 1].x, p[i + 2].x, tt),
            y: cr(p[i - 1].y, p[i].y, p[i + 1].y, p[i + 2].y, tt),
          });
        }
      }
      if (sp.length < 2) continue;

      // Area fill — vertical gradient
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

      // Glow stroke
      ctx.beginPath();
      ctx.moveTo(sp[0].x, sp[0].y);
      for (let i = 1; i < sp.length; i++) ctx.lineTo(sp[i].x, sp[i].y);
      ctx.strokeStyle = col + "20";
      ctx.lineWidth = depth <= 6 ? 5 : depth <= 12 ? 3.5 : 2.5;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";
      ctx.stroke();

      // Main stroke
      ctx.beginPath();
      ctx.moveTo(sp[0].x, sp[0].y);
      for (let i = 1; i < sp.length; i++) ctx.lineTo(sp[i].x, sp[i].y);
      ctx.strokeStyle = col + "CC";
      ctx.lineWidth = depth <= 6 ? 1.5 : depth <= 12 ? 1 : 0.65;
      ctx.stroke();
    }

    /* ── 5. Playhead ─────────────────────────────────── */
    const px = t2x(currentTime);
    if (px >= ML - 12 && px <= ML + cW + 12) {
      // Wide glow
      const gw = 24;
      const pg = ctx.createLinearGradient(px - gw, 0, px + gw, 0);
      pg.addColorStop(0, "transparent");
      pg.addColorStop(0.5, accentColor + "12");
      pg.addColorStop(1, "transparent");
      ctx.fillStyle = pg;
      ctx.fillRect(px - gw, MT, gw * 2, cH);

      // Core line
      ctx.beginPath();
      ctx.moveTo(px, MT - 2);
      ctx.lineTo(px, MT + cH + 2);
      ctx.strokeStyle = accentColor;
      ctx.lineWidth = 1.5;
      ctx.globalAlpha = 0.9;
      ctx.stroke();
      ctx.globalAlpha = 1;

      // Top triangle
      ctx.beginPath();
      ctx.moveTo(px - 4, MT - 6);
      ctx.lineTo(px + 4, MT - 6);
      ctx.lineTo(px, MT);
      ctx.closePath();
      ctx.fillStyle = accentColor;
      ctx.fill();
    }

    /* ── 6. Hover crosshair + dots ──────────────────── */
    const hv = hoverRef.current;
    if (hv) {
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
        const y = v2y(vals[d] ?? 0);
        // Glow
        ctx.beginPath();
        ctx.arc(sx, y, depth <= 6 ? 5 : 3.5, 0, Math.PI * 2);
        ctx.fillStyle = dm.color + "30";
        ctx.fill();
        // Dot
        ctx.beginPath();
        ctx.arc(sx, y, depth <= 6 ? 3 : 2, 0, Math.PI * 2);
        ctx.fillStyle = dm.color;
        ctx.fill();
        ctx.strokeStyle = "rgba(0,0,0,0.5)";
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }, [
    size, dpr, temporal, depth, dimCount, dimList, segCount, segDur,
    duration, windowDur, accentColor, rewardArr, neuroArr, getDimValues,
  ]);

  /* ── rAF Loop ────────────────────────────────────────── */
  useEffect(() => {
    let running = true;

    const loop = () => {
      if (!running) return;
      const audio = audioRef.current;
      const ct = audio?.currentTime ?? 0;

      // Auto-scroll when playing
      if (isPlaying && audio && !isNaN(audio.duration)) {
        const target = Math.max(0, ct - windowDur * PLAYHEAD_ANCHOR);
        const maxS = Math.max(0, duration - windowDur);
        targetScrollRef.current = Math.min(maxS, target);
      }

      // Smooth scroll
      scrollRef.current += (targetScrollRef.current - scrollRef.current) * 0.12;

      draw(ct);
      rafRef.current = requestAnimationFrame(loop);
    };

    rafRef.current = requestAnimationFrame(loop);
    return () => { running = false; cancelAnimationFrame(rafRef.current); };
  }, [isPlaying, draw, audioRef, duration, windowDur]);

  /* ── Tooltip builder ─────────────────────────────────── */
  const buildTooltip = useCallback((hv: HoverInfo): TooltipData | null => {
    const seg = temporal.segments[hv.segIdx];
    if (!seg) return null;

    const vals = depth === 6 ? seg.psychology : depth === 12 ? seg.cognition : seg.neuroscience;
    const t = hv.segIdx * segDur;
    const m = Math.floor(t / 60), s = Math.floor(t % 60);

    const dims: TooltipDim[] = vals.map((v, i) => {
      const dim = dimList[i];
      const parentList = depth === 12 ? ALL_PSYCHOLOGY : depth === 24 ? ALL_COGNITION : undefined;
      const parent = dim?.parentKey ? parentList?.find(p => p.key === dim.parentKey) : undefined;
      return { name: dim?.name ?? `D${i}`, value: v, color: dim?.color ?? "#94A3B8", parentName: parent?.name };
    });

    const neuro = neuroArr ? lerpSeg2D(neuroArr, t, duration) : [0, 0, 0, 0];
    const reward = rewardArr ? lerpSeg(rewardArr, t, duration) : 0;

    return { timeStr: `${m}:${s.toString().padStart(2, "0")}`, dims, reward, neuro, posX: hv.canvasX };
  }, [temporal, depth, dimList, segDur, duration, neuroArr, rewardArr]);

  /* ── Mouse handlers ──────────────────────────────────── */
  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const c = canvasRef.current;
    if (!c) return;
    const rect = c.getBoundingClientRect();
    const cx = ((e.clientX - rect.left) / rect.width) * size.w;
    const t = scrollRef.current + (cx / size.w) * windowDur;
    const si = Math.max(0, Math.min(segCount - 1, Math.round(t / segDur)));
    const hv: HoverInfo = { canvasX: cx, time: t, segIdx: si };
    hoverRef.current = hv;
    setTooltipData(buildTooltip(hv));
  }, [size, windowDur, segDur, segCount, buildTooltip]);

  const handleMouseLeave = useCallback(() => {
    hoverRef.current = null;
    setTooltipData(null);
  }, []);

  const handleClick = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const c = canvasRef.current;
    if (!c) return;
    const rect = c.getBoundingClientRect();
    const cx = ((e.clientX - rect.left) / rect.width) * size.w;
    const t = scrollRef.current + (cx / size.w) * windowDur;
    onSeek(Math.max(0, Math.min(1, t / duration)));
  }, [size, windowDur, duration, onSeek]);

  const handleWheel = useCallback((e: React.WheelEvent<HTMLCanvasElement>) => {
    e.stopPropagation();
    const maxS = Math.max(0, duration - windowDur);
    const delta = (e.deltaX || e.deltaY) * 0.04;
    targetScrollRef.current = Math.max(0, Math.min(maxS, targetScrollRef.current + delta));
  }, [duration, windowDur]);

  /* ── Scroll indicator ────────────────────────────────── */
  const winRatio = Math.min(1, windowDur / duration);

  return (
    <div ref={containerRef} className="relative w-full h-full">
      <canvas
        ref={canvasRef}
        style={{ width: "100%", height: "100%", cursor: "pointer" }}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        onClick={handleClick}
        onWheel={handleWheel}
      />

      {/* Scroll position indicator */}
      {duration > windowDur && (
        <div className="absolute bottom-0 left-0 right-0 h-[2px]" style={{ background: "rgba(255,255,255,0.03)" }}>
          <motion.div
            className="absolute top-0 h-full rounded-full"
            style={{ background: `${accentColor}30`, width: `${winRatio * 100}%` }}
            animate={{ left: `${(scrollRef.current / Math.max(0.01, duration - windowDur)) * (1 - winRatio) * 100}%` }}
            transition={{ duration: 0.1 }}
          />
        </div>
      )}

      {/* Tooltip overlay */}
      <AnimatePresence>
        {tooltipData && (
          <FlowTooltip
            data={tooltipData}
            depth={depth}
            accentColor={accentColor}
            containerW={size.w}
          />
        )}
      </AnimatePresence>
    </div>
  );
}


/* ════════════════════════════════════════════════════════════════════════
 *  FlowTooltip — Depth-layered hover information
 * ════════════════════════════════════════════════════════════════════════ */

function FlowTooltip({ data, depth, accentColor, containerW }: {
  data: TooltipData;
  depth: DepthLevel;
  accentColor: string;
  containerW: number;
}) {
  const tw = depth <= 6 ? 180 : depth <= 12 ? 210 : 290;
  // Edge-aware positioning
  let leftPct = (data.posX / containerW) * 100;
  const leftPx = (leftPct / 100) * containerW;
  if (leftPx < tw / 2 + 12) leftPct = ((tw / 2 + 12) / containerW) * 100;
  else if (leftPx > containerW - tw / 2 - 12) leftPct = ((containerW - tw / 2 - 12) / containerW) * 100;

  // Group dimensions by parent for 12D/24D
  const grouped = useMemo(() => {
    if (depth === 6) return null;
    const groups: { parentName: string; items: TooltipDim[] }[] = [];
    let cur = "";
    for (const d of data.dims) {
      const pn = d.parentName ?? "Other";
      if (pn !== cur) { cur = pn; groups.push({ parentName: pn, items: [] }); }
      groups[groups.length - 1].items.push(d);
    }
    return groups;
  }, [data.dims, depth]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 8 }}
      transition={{ duration: 0.1 }}
      className="absolute bottom-full mb-3 z-30 pointer-events-none"
      style={{ left: `${leftPct}%`, transform: "translateX(-50%)", width: tw }}
    >
      <div
        className="rounded-xl px-3 py-2.5"
        style={{
          background: "rgba(6,6,14,0.93)",
          backdropFilter: "blur(20px)",
          border: "1px solid rgba(255,255,255,0.07)",
          boxShadow: `0 8px 32px rgba(0,0,0,0.55), 0 0 24px ${accentColor}06`,
        }}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-2">
          <span className="text-[10px] font-mono text-slate-400">{data.timeStr}</span>
          <div className="flex items-center gap-1">
            <span className="text-[7px] font-mono text-slate-600 uppercase tracking-wider">Reward</span>
            <div className="w-10 h-[3px] rounded-full bg-white/5 overflow-hidden">
              <div className="h-full rounded-full" style={{ width: `${data.reward * 100}%`, background: accentColor, opacity: 0.65 }} />
            </div>
            <span className="text-[9px] font-mono" style={{ color: `${accentColor}90` }}>
              {data.reward.toFixed(2)}
            </span>
          </div>
        </div>

        {/* ── 6D: flat list ─────────────────────────────── */}
        {depth === 6 && (
          <div className="space-y-0.5">
            {data.dims.map((d, i) => (
              <DimRow key={i} name={d.name} value={d.value} color={d.color} />
            ))}
          </div>
        )}

        {/* ── 12D: grouped by parent ───────────────────── */}
        {depth === 12 && grouped && (
          <div className="space-y-1.5">
            {grouped.map((g, gi) => (
              <div key={gi}>
                <div className="text-[7px] font-display text-slate-600 uppercase tracking-wider mb-0.5">
                  {g.parentName}
                </div>
                {g.items.map((d, di) => (
                  <DimRow key={di} name={d.name} value={d.value} color={d.color} />
                ))}
              </div>
            ))}
          </div>
        )}

        {/* ── 24D: compact 2-column grouped ────────────── */}
        {depth === 24 && grouped && (
          <div className="space-y-1">
            {grouped.map((g, gi) => (
              <div key={gi}>
                <div className="text-[7px] font-display text-slate-600 uppercase tracking-wider mb-0.5">
                  {g.parentName}
                </div>
                <div className="grid grid-cols-2 gap-x-2 gap-y-0">
                  {g.items.map((d, di) => (
                    <DimRow key={di} name={d.name} value={d.value} color={d.color} compact />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Neurochemicals — visible at 12D+ */}
        {depth >= 12 && (
          <div className="flex items-center gap-2 mt-2 pt-1.5 border-t border-white/[0.05]">
            {NEURO_LABELS.map((label, i) => (
              <div key={label} className="flex items-center gap-0.5">
                <div className="w-1 h-1 rounded-full" style={{ background: NEURO_COLORS[i] }} />
                <span className="text-[7px] font-mono text-slate-600">{label}</span>
                <span className="text-[8px] font-mono" style={{ color: NEURO_COLORS[i] + "90" }}>
                  {data.neuro[i]?.toFixed(2) ?? "0"}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}


/* ── DimRow — single dimension bar ────────────────────────────────── */

function DimRow({ name, value, color, compact = false }: {
  name: string;
  value: number;
  color: string;
  compact?: boolean;
}) {
  return (
    <div className="flex items-center gap-1">
      <div className="w-1 h-1 rounded-full flex-shrink-0" style={{ background: color }} />
      <span
        className={`${compact ? "text-[7px]" : "text-[8px]"} font-display text-slate-400 flex-1 truncate`}
      >
        {name}
      </span>
      <div
        className={`${compact ? "w-6" : "w-10"} h-[2px] rounded-full bg-white/5 flex-shrink-0 overflow-hidden`}
      >
        <div
          className="h-full rounded-full"
          style={{ width: `${value * 100}%`, background: color, opacity: 0.65 }}
        />
      </div>
      <span
        className={`${compact ? "text-[6px]" : "text-[8px]"} font-mono flex-shrink-0`}
        style={{ color: color + "90" }}
      >
        {value.toFixed(2)}
      </span>
    </div>
  );
}
