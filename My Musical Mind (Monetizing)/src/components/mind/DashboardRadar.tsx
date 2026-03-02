/* ── DashboardRadar — Dual-Polygon N-D Dynamic Radar ──────────────────
 *  Persona-color static polygon = user's total/aggregate profile
 *  RED animated flow polygon     = morphs when music plays
 *  Supports 6D / 12D / 24D via dynamic `dims` prop.
 *  ──────────────────────────────────────────────────────────────────── */

import { useMemo, useCallback } from "react";
import { motion } from "framer-motion";
import { FLOW_INTERVAL_MS } from "@/hooks/useDemoFlow";

interface DimInfo {
  key: string;
  name: string;
  color: string;
}

interface Props {
  /** N static values [0-1] — shown in persona color */
  total: number[];
  /** N animated values [0-1] — shown in red when showFlow */
  flow?: number[];
  /** Dimension descriptors (key, name, color) — determines axis count */
  dims: DimInfo[];
  /** Persona accent color for the total polygon */
  color: string;
  /** SVG size in pixels */
  size?: number;
  /** Whether to render the animated flow polygon */
  showFlow?: boolean;
  /** Optional N description strings shown below each axis label */
  descs?: string[];
}

export function DashboardRadar({
  total,
  flow,
  dims,
  color,
  size = 440,
  showFlow = false,
  descs,
}: Props) {
  const n = dims.length;
  const cx = size / 2;
  const cy = size / 2;
  const maxR = size * 0.38;
  // Push labels further out — 6D/12D same distance, 24D tighter
  const labelR = maxR + (n <= 12 ? 32 : 22);

  const angles = useMemo(
    () => Array.from({ length: n }, (_, i) => (-90 + i * (360 / n)) * (Math.PI / 180)),
    [n],
  );

  const toPath = useCallback(
    (vals: number[]) => {
      const pts = angles.map((a, i) => {
        const r = maxR * Math.max(0, Math.min(1, vals[i] ?? 0));
        return `${cx + Math.cos(a) * r} ${cy + Math.sin(a) * r}`;
      });
      return `M ${pts.join(" L ")} Z`;
    },
    [angles, cx, cy, maxR],
  );

  const gridPath = useCallback(
    (scale: number) => {
      const pts = angles.map(
        (a) =>
          `${cx + Math.cos(a) * maxR * scale} ${cy + Math.sin(a) * maxR * scale}`,
      );
      return `M ${pts.join(" L ")} Z`;
    },
    [angles, cx, cy, maxR],
  );

  const totalPts = useMemo(
    () =>
      angles.map((a, i) => {
        const r = maxR * Math.max(0, Math.min(1, total[i] ?? 0));
        return { x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r };
      }),
    [angles, total, cx, cy, maxR],
  );

  const flowPts = useMemo(
    () =>
      angles.map((a, i) => {
        const r = maxR * Math.max(0, Math.min(1, (flow ?? total)[i] ?? 0));
        return { x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r };
      }),
    [angles, flow, total, cx, cy, maxR],
  );

  // Match transition to target interval for continuous 60fps motion
  const flowDuration = FLOW_INTERVAL_MS / 1000;

  // Adaptive sizing — 6D and 12D share the same label style
  const labelFontSize = n <= 12 ? 12.8 : 7;
  const labelWeight = n <= 12 ? "700" : "600";
  const descFontSize = n <= 12 ? 11 : 0; // hide descs for 24D
  const dotR = n <= 6 ? 2.5 : n <= 12 ? 2 : 1.5;
  const flowDotR = n <= 6 ? 3.5 : n <= 12 ? 2.5 : 2;
  const pctFontSize = n <= 6 ? 7 : 0; // percentages only for 6D

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      className="overflow-visible"
    >
      {/* Grid polygons */}
      {[0.25, 0.5, 0.75, 1].map((s) => (
        <path
          key={s}
          d={gridPath(s)}
          fill="none"
          stroke={
            s === 1
              ? "rgba(255,255,255,0.08)"
              : "rgba(255,255,255,0.04)"
          }
          strokeWidth={s === 1 ? 0.8 : 0.5}
        />
      ))}

      {/* Axis lines */}
      {angles.map((a, i) => (
        <line
          key={i}
          x1={cx}
          y1={cy}
          x2={cx + Math.cos(a) * maxR}
          y2={cy + Math.sin(a) * maxR}
          stroke="rgba(255,255,255,0.05)"
          strokeWidth={0.5}
        />
      ))}

      {/* Center dot */}
      <circle cx={cx} cy={cy} r={1.5} fill="rgba(255,255,255,0.1)" />

      {/* ── Total polygon — persona color ────────── */}
      <path
        d={toPath(total)}
        fill={`${color}1A`}
        stroke={color}
        strokeWidth={1.5}
        strokeLinejoin="round"
        opacity={0.85}
      />

      {/* ── Animated flow polygon — red, 60fps via Framer Motion rAF ── */}
      {showFlow && flow && (
        <motion.path
          initial={false}
          animate={{ d: toPath(flow) }}
          transition={{ duration: flowDuration, ease: "easeInOut" }}
          fill="rgba(239,68,68,0.07)"
          stroke="#EF4444"
          strokeWidth={2}
          strokeLinejoin="round"
          style={{ filter: "drop-shadow(0 0 10px rgba(239,68,68,0.25))" }}
        />
      )}

      {/* Total data dots — persona color */}
      {totalPts.map((pt, i) => (
        <circle
          key={`t${i}`}
          cx={pt.x}
          cy={pt.y}
          r={dotR}
          fill={color}
          stroke="#0a0a0f"
          strokeWidth={0.8}
        />
      ))}

      {/* Flow data dots — animated, red */}
      {showFlow &&
        flow &&
        angles.map((_, i) => (
          <motion.circle
            key={`f${i}`}
            initial={false}
            animate={{ cx: flowPts[i].x, cy: flowPts[i].y }}
            transition={{ duration: flowDuration, ease: "easeInOut" }}
            r={flowDotR}
            fill="#EF4444"
            stroke="#0a0a0f"
            strokeWidth={1}
            style={{ filter: "drop-shadow(0 0 6px rgba(239,68,68,0.5))" }}
          />
        ))}

      {/* Dimension labels */}
      {dims.map((dim, i) => {
        const x = cx + Math.cos(angles[i]) * labelR;
        const y = cy + Math.sin(angles[i]) * labelR;
        const desc = descs?.[i];
        const showDesc = desc && descFontSize > 0;
        return (
          <g key={dim.key} style={{ pointerEvents: "none" }}>
            <text
              x={x}
              y={showDesc ? y - 8 : y}
              textAnchor="middle"
              dominantBaseline="middle"
              fill={dim.color}
              fontSize={labelFontSize}
              fontWeight={labelWeight}
              fontFamily="Inter"
            >
              {dim.name}
            </text>
            {showDesc && (
              <text
                x={x}
                y={y + 10}
                textAnchor="middle"
                dominantBaseline="middle"
                fill="rgba(203,213,225,0.7)"
                fontSize={descFontSize}
                fontFamily="Inter"
                fontWeight="400"
              >
                {desc}
              </text>
            )}
          </g>
        );
      })}

      {/* Percentage labels on total dots (6D only) */}
      {pctFontSize > 0 && total.map((v, i) => {
        const pct = Math.round(Math.max(0, Math.min(1, v)) * 100);
        const pctR = maxR * Math.max(0, Math.min(1, v)) - 12;
        if (pctR < 10) return null;
        const x = cx + Math.cos(angles[i]) * pctR;
        const y = cy + Math.sin(angles[i]) * pctR;
        return (
          <text
            key={`pct${i}`}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="middle"
            fill={`${color}80`}
            fontSize={pctFontSize}
            fontFamily="monospace"
            style={{ pointerEvents: "none" }}
          >
            {pct}
          </text>
        );
      })}
    </svg>
  );
}
