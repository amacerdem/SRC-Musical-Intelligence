/* ── DashboardRadar — Dual-Polygon 6D Hexagonal Radar ────────────────
 *  Persona-color static polygon = user's total/aggregate 6D profile
 *  RED animated flow polygon     = morphs when music plays
 *  Adapted from LabRadar (Lab.tsx) for the Dashboard "My Mind" page.
 *  ──────────────────────────────────────────────────────────────────── */

import { useMemo, useCallback } from "react";
import { motion } from "framer-motion";
import { ALL_PSYCHOLOGY } from "@/data/dimensions";
import { FLOW_INTERVAL_MS } from "@/hooks/useDemoFlow";

const RADAR_ANGLES = Array.from(
  { length: 6 },
  (_, i) => (-90 + i * 60) * (Math.PI / 180),
);

interface Props {
  /** 6 static values [0-1] — shown in persona color */
  total: number[];
  /** 6 animated values [0-1] — shown in red when showFlow */
  flow?: number[];
  /** Persona accent color for the total polygon */
  color: string;
  /** SVG size in pixels */
  size?: number;
  /** Whether to render the animated flow polygon */
  showFlow?: boolean;
}

export function DashboardRadar({
  total,
  flow,
  color,
  size = 440,
  showFlow = false,
}: Props) {
  const cx = size / 2;
  const cy = size / 2;
  const maxR = size * 0.38;
  const labelR = maxR + 24;

  const toPath = useCallback(
    (vals: number[]) => {
      const pts = RADAR_ANGLES.map((a, i) => {
        const r = maxR * Math.max(0, Math.min(1, vals[i] ?? 0));
        return `${cx + Math.cos(a) * r} ${cy + Math.sin(a) * r}`;
      });
      return `M ${pts.join(" L ")} Z`;
    },
    [cx, cy, maxR],
  );

  const gridPath = useCallback(
    (scale: number) => {
      const pts = RADAR_ANGLES.map(
        (a) =>
          `${cx + Math.cos(a) * maxR * scale} ${cy + Math.sin(a) * maxR * scale}`,
      );
      return `M ${pts.join(" L ")} Z`;
    },
    [cx, cy, maxR],
  );

  const totalPts = useMemo(
    () =>
      RADAR_ANGLES.map((a, i) => {
        const r = maxR * Math.max(0, Math.min(1, total[i] ?? 0));
        return { x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r };
      }),
    [total, cx, cy, maxR],
  );

  const flowPts = useMemo(
    () =>
      RADAR_ANGLES.map((a, i) => {
        const r = maxR * Math.max(0, Math.min(1, (flow ?? total)[i] ?? 0));
        return { x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r };
      }),
    [flow, total, cx, cy, maxR],
  );

  const ease = [0.22, 1, 0.36, 1] as [number, number, number, number];
  // Match transition to target interval for continuous 60fps motion
  const flowDuration = FLOW_INTERVAL_MS / 1000;

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      className="overflow-visible"
    >
      {/* Grid hexagons */}
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
      {RADAR_ANGLES.map((a, i) => (
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
          r={2.5}
          fill={color}
          stroke="#0a0a0f"
          strokeWidth={0.8}
        />
      ))}

      {/* Flow data dots — animated, red */}
      {showFlow &&
        flow &&
        RADAR_ANGLES.map((_, i) => (
          <motion.circle
            key={`f${i}`}
            initial={false}
            animate={{ cx: flowPts[i].x, cy: flowPts[i].y }}
            transition={{ duration: flowDuration, ease: "easeInOut" }}
            r={3.5}
            fill="#EF4444"
            stroke="#0a0a0f"
            strokeWidth={1}
            style={{ filter: "drop-shadow(0 0 6px rgba(239,68,68,0.5))" }}
          />
        ))}

      {/* Dimension labels */}
      {ALL_PSYCHOLOGY.map((dim, i) => {
        const x = cx + Math.cos(RADAR_ANGLES[i]) * labelR;
        const y = cy + Math.sin(RADAR_ANGLES[i]) * labelR;
        return (
          <text
            key={dim.key}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="middle"
            fill={dim.color}
            fontSize={10}
            fontWeight="600"
            fontFamily="Inter"
            style={{ pointerEvents: "none" }}
          >
            {dim.name}
          </text>
        );
      })}

      {/* Percentage labels on total dots */}
      {total.map((v, i) => {
        const pct = Math.round(Math.max(0, Math.min(1, v)) * 100);
        const pctR = maxR * Math.max(0, Math.min(1, v)) - 12;
        if (pctR < 10) return null;
        const x = cx + Math.cos(RADAR_ANGLES[i]) * pctR;
        const y = cy + Math.sin(RADAR_ANGLES[i]) * pctR;
        return (
          <text
            key={`pct${i}`}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="middle"
            fill={`${color}80`}
            fontSize={7}
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
