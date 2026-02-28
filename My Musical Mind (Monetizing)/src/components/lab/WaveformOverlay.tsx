/* ── WaveformOverlay — SVG waveform + dimension temporal curves ──────── */

import { useMemo, useState, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { DepthLevel } from "@/stores/useLabStore";
import type { TemporalDimensions } from "@/stores/useLabStore";
import type { DimensionState } from "@/types/dimensions";
import {
  ALL_PSYCHOLOGY,
  ALL_COGNITION,
  ALL_NEUROSCIENCE,
  PSYCHOLOGY_COLORS,
  COGNITION_CHILDREN,
} from "@/data/dimensions";
import type { DimensionKey6D } from "@/types/dimensions";

/* ── Colors for 12D and 24D ─────────────────────────────── */

function getDimColor(depth: DepthLevel, index: number): string {
  if (depth === 6) {
    const key = ALL_PSYCHOLOGY[index]?.key as DimensionKey6D;
    return PSYCHOLOGY_COLORS[key] ?? "#94A3B8";
  }
  if (depth === 12) {
    const node = ALL_COGNITION[index];
    if (!node) return "#94A3B8";
    const parentKey = node.parentKey as DimensionKey6D;
    const color = PSYCHOLOGY_COLORS[parentKey] ?? "#94A3B8";
    // Alternate brightness for children of same parent
    const siblings = Object.values(COGNITION_CHILDREN).find(
      ([a, b]) => a.key === node.key || b.key === node.key
    );
    const isSecond = siblings?.[1]?.key === node.key;
    return isSecond ? `${color}B0` : color;
  }
  // 24D: inherit from 6D grandparent via modular index
  const parentIdx = Math.floor(index / 4);
  const parentKey = ALL_PSYCHOLOGY[parentIdx]?.key as DimensionKey6D;
  const base = PSYCHOLOGY_COLORS[parentKey] ?? "#94A3B8";
  const opacity = ["FF", "CC", "99", "77"][index % 4];
  return `${base}${opacity}`;
}

function getDimLabel(depth: DepthLevel, index: number): string {
  if (depth === 6) return ALL_PSYCHOLOGY[index]?.name ?? "";
  if (depth === 12) return ALL_COGNITION[index]?.name ?? "";
  return ALL_NEUROSCIENCE[index]?.name ?? "";
}

/* ── Spline interpolation (Catmull-Rom) ─────────────────── */

function catmullRomSpline(
  points: { x: number; y: number }[],
  segments: number = 20
): string {
  if (points.length < 2) return "";
  const pts = [points[0], ...points, points[points.length - 1]];
  const path: string[] = [`M ${pts[1].x} ${pts[1].y}`];

  for (let i = 1; i < pts.length - 2; i++) {
    const p0 = pts[i - 1], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2];
    for (let t = 1; t <= segments; t++) {
      const tt = t / segments;
      const t2 = tt * tt, t3 = t2 * tt;
      const x =
        0.5 * (
          2 * p1.x +
          (-p0.x + p2.x) * tt +
          (2 * p0.x - 5 * p1.x + 4 * p2.x - p3.x) * t2 +
          (-p0.x + 3 * p1.x - 3 * p2.x + p3.x) * t3
        );
      const y =
        0.5 * (
          2 * p1.y +
          (-p0.y + p2.y) * tt +
          (2 * p0.y - 5 * p1.y + 4 * p2.y - p3.y) * t2 +
          (-p0.y + 3 * p1.y - 3 * p2.y + p3.y) * t3
        );
      path.push(`L ${x} ${y}`);
    }
  }
  return path.join(" ");
}

/* ── Component ──────────────────────────────────────────── */

interface Props {
  temporal: TemporalDimensions;
  depth: DepthLevel;
  duration: number;
  accentColor: string;
}

const SVG_W = 800;
const SVG_H = 280;
const PAD_L = 0;
const PAD_R = 0;
const PAD_T = 20;
const PAD_B = 30;
const CHART_W = SVG_W - PAD_L - PAD_R;
const CHART_H = SVG_H - PAD_T - PAD_B;

export function WaveformOverlay({ temporal, depth, duration, accentColor }: Props) {
  const [hoverX, setHoverX] = useState<number | null>(null);
  const svgRef = useRef<SVGSVGElement>(null);

  const dimCount = depth;
  const segCount = temporal.segments.length;

  const getDimValues = useCallback(
    (segState: DimensionState): number[] => {
      if (depth === 6) return segState.psychology;
      if (depth === 12) return segState.cognition;
      return segState.neuroscience;
    },
    [depth]
  );

  /* ── Generate spline paths for each dimension ──────── */
  const paths = useMemo(() => {
    const result: { path: string; areaPath: string; color: string; label: string; points: { x: number; y: number }[] }[] = [];

    for (let d = 0; d < dimCount; d++) {
      const pts: { x: number; y: number }[] = [];
      for (let s = 0; s < segCount; s++) {
        const x = PAD_L + (s / (segCount - 1)) * CHART_W;
        const val = getDimValues(temporal.segments[s])[d] ?? 0;
        const y = PAD_T + CHART_H - val * CHART_H;
        pts.push({ x, y });
      }

      const linePath = catmullRomSpline(pts, 16);
      // Area path: close at bottom
      const areaPath = linePath +
        ` L ${pts[pts.length - 1].x} ${PAD_T + CHART_H}` +
        ` L ${pts[0].x} ${PAD_T + CHART_H} Z`;

      result.push({
        path: linePath,
        areaPath,
        color: getDimColor(depth, d),
        label: getDimLabel(depth, d),
        points: pts,
      });
    }
    return result;
  }, [temporal, depth, dimCount, segCount, getDimValues]);

  /* ── Hover handling ────────────────────────────────── */
  const handleMouseMove = useCallback(
    (e: React.MouseEvent<SVGSVGElement>) => {
      const svg = svgRef.current;
      if (!svg) return;
      const rect = svg.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * SVG_W;
      setHoverX(Math.max(PAD_L, Math.min(PAD_L + CHART_W, x)));
    },
    []
  );

  const hoverSegment = useMemo(() => {
    if (hoverX === null) return null;
    const ratio = (hoverX - PAD_L) / CHART_W;
    const seg = Math.round(ratio * (segCount - 1));
    return Math.max(0, Math.min(segCount - 1, seg));
  }, [hoverX, segCount]);

  const hoverValues = useMemo(() => {
    if (hoverSegment === null) return null;
    return getDimValues(temporal.segments[hoverSegment]);
  }, [hoverSegment, temporal, getDimValues]);

  const hoverTime = useMemo(() => {
    if (hoverSegment === null) return "";
    const secs = (hoverSegment / (segCount - 1)) * duration;
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  }, [hoverSegment, segCount, duration]);

  /* ── Time axis labels ──────────────────────────────── */
  const timeLabels = useMemo(() => {
    const labels: { x: number; text: string }[] = [];
    for (let s = 0; s < segCount; s++) {
      const x = PAD_L + (s / (segCount - 1)) * CHART_W;
      const secs = (s / (segCount - 1)) * duration;
      const m = Math.floor(secs / 60);
      const sec = Math.floor(secs % 60);
      labels.push({ x, text: `${m}:${sec.toString().padStart(2, "0")}` });
    }
    return labels;
  }, [segCount, duration]);

  return (
    <div className="relative w-full">
      <svg
        ref={svgRef}
        viewBox={`0 0 ${SVG_W} ${SVG_H}`}
        className="w-full"
        style={{ overflow: "visible" }}
        onMouseMove={handleMouseMove}
        onMouseLeave={() => setHoverX(null)}
      >
        {/* Background grid lines */}
        {[0.25, 0.5, 0.75].map((v) => (
          <line
            key={v}
            x1={PAD_L} y1={PAD_T + CHART_H - v * CHART_H}
            x2={PAD_L + CHART_W} y2={PAD_T + CHART_H - v * CHART_H}
            stroke="rgba(255,255,255,0.04)" strokeWidth={0.5}
          />
        ))}
        {/* Base axis */}
        <line
          x1={PAD_L} y1={PAD_T + CHART_H}
          x2={PAD_L + CHART_W} y2={PAD_T + CHART_H}
          stroke="rgba(255,255,255,0.08)" strokeWidth={0.5}
        />

        {/* Dimension area fills + lines */}
        <AnimatePresence mode="wait">
          <motion.g
            key={`depth-${depth}`}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
          >
            {paths.map(({ areaPath, path, color }, i) => (
              <g key={`${depth}-${i}`}>
                <path
                  d={areaPath}
                  fill={color}
                  fillOpacity={0.06}
                />
                <path
                  d={path}
                  fill="none"
                  stroke={color}
                  strokeWidth={depth <= 6 ? 2 : depth <= 12 ? 1.5 : 1}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  style={{ filter: `drop-shadow(0 0 4px ${color}40)` }}
                />
              </g>
            ))}
          </motion.g>
        </AnimatePresence>

        {/* Time axis labels */}
        {timeLabels.map(({ x, text }, i) => (
          <text
            key={i}
            x={x} y={SVG_H - 6}
            textAnchor="middle"
            fill="rgba(255,255,255,0.2)"
            fontSize={9}
            fontFamily="var(--font-mono)"
          >
            {text}
          </text>
        ))}

        {/* Hover crosshair */}
        {hoverX !== null && (
          <>
            <line
              x1={hoverX} y1={PAD_T}
              x2={hoverX} y2={PAD_T + CHART_H}
              stroke={accentColor}
              strokeWidth={1}
              strokeDasharray="3 3"
              opacity={0.5}
            />
            {/* Dots on each line at hover position */}
            {paths.map(({ points, color }, i) => {
              if (hoverSegment === null) return null;
              const pt = points[hoverSegment];
              if (!pt) return null;
              return (
                <circle
                  key={i}
                  cx={pt.x} cy={pt.y}
                  r={depth <= 6 ? 4 : 3}
                  fill={color}
                  stroke="black"
                  strokeWidth={1}
                  style={{ filter: `drop-shadow(0 0 6px ${color})` }}
                />
              );
            })}
          </>
        )}
      </svg>

      {/* Hover tooltip */}
      <AnimatePresence>
        {hoverX !== null && hoverValues && (
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 4 }}
            transition={{ duration: 0.15 }}
            className="absolute top-2 z-20 pointer-events-none"
            style={{ left: `${(hoverX / SVG_W) * 100}%`, transform: "translateX(-50%)" }}
          >
            <div
              className="rounded-lg px-3 py-2 min-w-[120px]"
              style={{
                background: "rgba(0,0,0,0.85)",
                backdropFilter: "blur(12px)",
                border: "1px solid rgba(255,255,255,0.08)",
                boxShadow: "0 4px 16px rgba(0,0,0,0.4)",
              }}
            >
              <div className="text-[10px] font-mono text-slate-500 mb-1.5">{hoverTime}</div>
              <div className="space-y-1">
                {hoverValues.slice(0, Math.min(dimCount, 8)).map((val, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: getDimColor(depth, i) }} />
                    <span className="text-[9px] font-display text-slate-400 flex-1 truncate">
                      {getDimLabel(depth, i)}
                    </span>
                    <span className="text-[10px] font-mono" style={{ color: getDimColor(depth, i) }}>
                      {Math.round(val * 100)}%
                    </span>
                  </div>
                ))}
                {dimCount > 8 && (
                  <div className="text-[8px] font-mono text-slate-600 text-center">
                    +{dimCount - 8} more
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Legend */}
      <div className="flex flex-wrap gap-x-3 gap-y-1 mt-2">
        {paths.slice(0, Math.min(dimCount, depth <= 12 ? dimCount : 12)).map(({ color, label }, i) => (
          <div key={i} className="flex items-center gap-1">
            <div className="w-2 h-[2px] rounded-full" style={{ background: color }} />
            <span className="text-[9px] font-display text-slate-500">{label}</span>
          </div>
        ))}
        {depth === 24 && dimCount > 12 && (
          <span className="text-[8px] font-mono text-slate-600">+{dimCount - 12} more</span>
        )}
      </div>
    </div>
  );
}
