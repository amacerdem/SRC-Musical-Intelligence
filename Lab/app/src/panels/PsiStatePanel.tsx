import React, { useMemo } from "react";
import { useStore } from "../store";

const BG = "#0d0d14";
const TEXT = "#c8c8d4";
const BORDER = "#252538";
const GRID_COLOR = "#1a1a2e";

const DOMAINS: { key: keyof import("../types/experiment").PsiData; label: string; color: string }[] = [
  { key: "affect", label: "Affect", color: "#f43f5e" },
  { key: "emotion", label: "Emotion", color: "#8b5cf6" },
  { key: "aesthetic", label: "Aesthetic", color: "#f59e0b" },
  { key: "bodily", label: "Bodily", color: "#06b6d4" },
  { key: "cognitive", label: "Cognitive", color: "#3b82f6" },
  { key: "temporal", label: "Temporal", color: "#22c55e" },
];

const CX = 160;
const CY = 140;
const MAX_R = 100;
const SVG_W = 320;
const SVG_H = 300;

function polarToXY(angle: number, radius: number): { x: number; y: number } {
  // Start from top (-PI/2), go clockwise
  const rad = angle - Math.PI / 2;
  return {
    x: CX + Math.cos(rad) * radius,
    y: CY + Math.sin(rad) * radius,
  };
}

/**
 * PsiStatePanel - Radar chart with 6 axes for Psi3 cognitive state (28D).
 * Each axis = mean of that domain's values at lodFrameIndex.
 * Hexagonal grid rings at 0.25, 0.5, 0.75, 1.0 with filled polygon.
 */
export default function PsiStatePanel(): React.ReactElement {
  const psiData = useStore((s) => s.psiData);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);

  const N = DOMAINS.length;
  const angleStep = (2 * Math.PI) / N;

  // Compute mean for each domain at current frame
  const domainValues = useMemo(() => {
    if (!psiData) return null;
    return DOMAINS.map((d) => {
      const domainFrames = psiData[d.key];
      if (!domainFrames || lodFrameIndex >= domainFrames.length) return 0;
      const row = domainFrames[lodFrameIndex];
      if (!row || row.length === 0) return 0;
      const sum = row.reduce((a, b) => a + b, 0);
      return Math.max(0, Math.min(1, sum / row.length));
    });
  }, [psiData, lodFrameIndex]);

  // Grid ring polygons
  const rings = [0.25, 0.5, 0.75, 1.0];
  const ringPaths = rings.map((r) => {
    const pts = Array.from({ length: N }, (_, i) => {
      const { x, y } = polarToXY(i * angleStep, r * MAX_R);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    });
    return pts.join(" ");
  });

  // Axis lines
  const axisLines = Array.from({ length: N }, (_, i) => {
    const { x, y } = polarToXY(i * angleStep, MAX_R);
    return { x, y };
  });

  // Value polygon
  const valuePoly = domainValues
    ? domainValues.map((v, i) => {
        const { x, y } = polarToXY(i * angleStep, v * MAX_R);
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      }).join(" ")
    : null;

  // Dominant color for fill = domain with highest value
  const dominantIdx = domainValues
    ? domainValues.reduce((best, v, i, arr) => (v > (arr[best] ?? 0) ? i : best), 0)
    : 0;
  const fillColor = DOMAINS[dominantIdx]?.color ?? TEXT;

  const noData = !psiData;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        background: BG,
        border: `1px solid ${BORDER}`,
        borderRadius: 6,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "6px 12px",
          fontSize: 12,
          fontWeight: 600,
          color: TEXT,
          borderBottom: `1px solid ${BORDER}`,
          flexShrink: 0,
        }}
      >
        &Psi;&sup3; Cognitive State (28D)
      </div>
      <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
        {noData ? (
          <span style={{ color: TEXT, fontSize: 13, fontFamily: "Inter, sans-serif" }}>
            Waiting for &Psi;&sup3; data&hellip;
          </span>
        ) : (
          <svg
            viewBox={`0 0 ${SVG_W} ${SVG_H}`}
            style={{ width: "100%", height: "100%", maxHeight: "100%" }}
            preserveAspectRatio="xMidYMid meet"
          >
            <rect x={0} y={0} width={SVG_W} height={SVG_H} fill={BG} />

            {/* Grid rings */}
            {ringPaths.map((pts, i) => (
              <polygon
                key={i}
                points={pts}
                fill="none"
                stroke={GRID_COLOR}
                strokeWidth={0.5}
              />
            ))}

            {/* Ring labels */}
            {rings.map((r) => {
              const { x, y } = polarToXY(0, r * MAX_R);
              return (
                <text
                  key={r}
                  x={x + 3}
                  y={y - 2}
                  fill={TEXT}
                  fontSize={7}
                  fontFamily="'JetBrains Mono', monospace"
                  opacity={0.4}
                >
                  {r.toFixed(2)}
                </text>
              );
            })}

            {/* Axis lines */}
            {axisLines.map((p, i) => (
              <line
                key={i}
                x1={CX}
                y1={CY}
                x2={p.x}
                y2={p.y}
                stroke={GRID_COLOR}
                strokeWidth={0.5}
              />
            ))}

            {/* Filled value polygon */}
            {valuePoly && (
              <>
                <polygon
                  points={valuePoly}
                  fill={fillColor}
                  fillOpacity={0.3}
                  stroke={fillColor}
                  strokeWidth={2}
                  strokeOpacity={0.9}
                />
              </>
            )}

            {/* Value dots and domain labels */}
            {DOMAINS.map((d, i) => {
              const v = domainValues?.[i] ?? 0;
              const labelR = MAX_R + 18;
              const labelPos = polarToXY(i * angleStep, labelR);
              const dotPos = polarToXY(i * angleStep, v * MAX_R);
              return (
                <g key={d.key}>
                  {/* Value dot */}
                  <circle
                    cx={dotPos.x}
                    cy={dotPos.y}
                    r={3}
                    fill={d.color}
                  />
                  {/* Domain label */}
                  <text
                    x={labelPos.x}
                    y={labelPos.y}
                    fill={d.color}
                    fontSize={9}
                    fontFamily="Inter, sans-serif"
                    fontWeight={600}
                    textAnchor="middle"
                    dominantBaseline="central"
                  >
                    {d.label}
                  </text>
                </g>
              );
            })}
          </svg>
        )}
      </div>
    </div>
  );
}
