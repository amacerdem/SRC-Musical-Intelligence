import React, { useMemo } from "react";
import { useStore } from "../store";
import type { PsiData } from "../types/experiment";

/* ── Theme ──────────────────────────────────────────────── */
const BG_PRIMARY = "#0a0a0f";
const BG_PANEL = "#0d0d14";
const BG_SURFACE = "#111118";
const TEXT_PRIMARY = "#c8c8d4";
const TEXT_SECONDARY = "#8b8b9e";
const TEXT_MUTED = "#5a5a6e";
const ACCENT = "#6366f1";
const BORDER = "#252538";
const GRID_COLOR = "#1a1a2e";
const FONT_UI = "'Inter', sans-serif";
const FONT_DATA = "'JetBrains Mono', monospace";

/* ── Domain definitions ──────────────────────────────────── */
interface DomainDef {
  key: keyof PsiData;
  label: string;
  color: string;
  dims: string[];
  regions: string[];
}

const DOMAINS: DomainDef[] = [
  {
    key: "affect",
    label: "Affect",
    color: "#f43f5e",
    dims: ["valence", "arousal", "tension", "dominance"],
    regions: ["amygdala", "insula", "vmPFC"],
  },
  {
    key: "emotion",
    label: "Emotion",
    color: "#8b5cf6",
    dims: ["joy", "sadness", "fear", "awe", "nostalgia", "tenderness", "serenity"],
    regions: ["amygdala", "ACC", "hippocampus"],
  },
  {
    key: "aesthetic",
    label: "Aesthetic",
    color: "#f59e0b",
    dims: ["beauty", "groove", "flow", "surprise", "closure"],
    regions: ["OFC", "nucleus accumbens", "dmPFC"],
  },
  {
    key: "bodily",
    label: "Bodily",
    color: "#06b6d4",
    dims: ["chills", "movement_urge", "breathing_change", "tension_release"],
    regions: ["insula", "SMA", "PAG"],
  },
  {
    key: "cognitive",
    label: "Cognitive",
    color: "#3b82f6",
    dims: ["familiarity", "absorption", "expectation", "attention_focus"],
    regions: ["dlPFC", "hippocampus", "IPS"],
  },
  {
    key: "temporal",
    label: "Temporal",
    color: "#22c55e",
    dims: ["anticipation", "resolution", "buildup", "release"],
    regions: ["SMA", "cerebellum", "basal ganglia"],
  },
];

/* ── Radar chart constants ───────────────────────────────── */
const RADAR_SIZE = 500;
const CX = RADAR_SIZE / 2;
const CY = RADAR_SIZE / 2;
const MAX_R = 180;
const N = DOMAINS.length;
const ANGLE_STEP = (2 * Math.PI) / N;

function polarToXY(index: number, radius: number): { x: number; y: number } {
  // Start from top (-PI/2), go clockwise
  const rad = index * ANGLE_STEP - Math.PI / 2;
  return {
    x: CX + Math.cos(rad) * radius,
    y: CY + Math.sin(rad) * radius,
  };
}

/* ── Radar Chart component ───────────────────────────────── */
interface RadarChartProps {
  domainMeans: number[];
}

function RadarChart({ domainMeans }: RadarChartProps): React.ReactElement {
  const rings = [0.25, 0.5, 0.75, 1.0];

  // Grid ring polygons (hexagonal)
  const ringPolygons = rings.map((r) => {
    const pts = Array.from({ length: N }, (_, i) => {
      const { x, y } = polarToXY(i, r * MAX_R);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    });
    return pts.join(" ");
  });

  // Axis lines from center to tips
  const axes = Array.from({ length: N }, (_, i) => polarToXY(i, MAX_R));

  // Value polygon
  const valuePoly = domainMeans
    .map((v, i) => {
      const { x, y } = polarToXY(i, Math.max(0, Math.min(1, v)) * MAX_R);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  // Dominant domain for fill color
  const dominantIdx = domainMeans.reduce(
    (best, v, i, arr) => (v > (arr[best] ?? 0) ? i : best),
    0,
  );
  const fillColor = DOMAINS[dominantIdx]?.color ?? TEXT_PRIMARY;

  return (
    <svg
      viewBox={`0 0 ${RADAR_SIZE} ${RADAR_SIZE}`}
      style={{ width: "100%", height: "100%", display: "block" }}
      preserveAspectRatio="xMidYMid meet"
    >
      <rect x={0} y={0} width={RADAR_SIZE} height={RADAR_SIZE} fill={BG_PRIMARY} />

      {/* Grid rings */}
      {ringPolygons.map((pts, i) => (
        <polygon
          key={i}
          points={pts}
          fill="none"
          stroke={GRID_COLOR}
          strokeWidth={i === rings.length - 1 ? 1 : 0.5}
        />
      ))}

      {/* Ring labels along first axis */}
      {rings.map((r) => {
        const { x, y } = polarToXY(0, r * MAX_R);
        return (
          <text
            key={r}
            x={x + 4}
            y={y - 4}
            fill={TEXT_MUTED}
            fontSize={10}
            fontFamily={FONT_DATA}
            opacity={0.6}
          >
            {r.toFixed(2)}
          </text>
        );
      })}

      {/* Axis lines */}
      {axes.map((p, i) => (
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
      <polygon
        points={valuePoly}
        fill={fillColor}
        fillOpacity={0.25}
        stroke={fillColor}
        strokeWidth={2}
        strokeOpacity={0.85}
      />

      {/* Value dots and domain labels */}
      {DOMAINS.map((d, i) => {
        const v = domainMeans[i] ?? 0;
        const dotPos = polarToXY(i, Math.max(0, Math.min(1, v)) * MAX_R);
        const labelPos = polarToXY(i, MAX_R + 28);
        const meanLabel = polarToXY(i, MAX_R + 44);

        return (
          <g key={d.key}>
            {/* Value dot */}
            <circle
              cx={dotPos.x}
              cy={dotPos.y}
              r={4}
              fill={d.color}
              stroke={BG_PRIMARY}
              strokeWidth={1.5}
            />

            {/* Domain label at axis tip */}
            <text
              x={labelPos.x}
              y={labelPos.y}
              fill={d.color}
              fontSize={13}
              fontFamily={FONT_UI}
              fontWeight={700}
              textAnchor="middle"
              dominantBaseline="central"
            >
              {d.label}
            </text>

            {/* Mean value under label */}
            <text
              x={meanLabel.x}
              y={meanLabel.y}
              fill={TEXT_MUTED}
              fontSize={10}
              fontFamily={FONT_DATA}
              textAnchor="middle"
              dominantBaseline="central"
            >
              {v.toFixed(3)}
            </text>
          </g>
        );
      })}

      {/* Center dot */}
      <circle cx={CX} cy={CY} r={2} fill={TEXT_MUTED} />
    </svg>
  );
}

/* ── Domain breakdown section ────────────────────────────── */
interface DomainSectionProps {
  domain: DomainDef;
  values: number[];
  allZero: boolean;
}

function DomainSection({ domain, values, allZero }: DomainSectionProps): React.ReactElement {
  return (
    <div style={{ marginBottom: 16 }}>
      {/* Header with color left border */}
      <div
        style={{
          borderLeft: `3px solid ${domain.color}`,
          paddingLeft: 10,
          paddingBottom: 4,
          marginBottom: 6,
          display: "flex",
          alignItems: "baseline",
          gap: 6,
        }}
      >
        <span
          style={{
            fontSize: 13,
            fontWeight: 700,
            color: domain.color,
            fontFamily: FONT_UI,
          }}
        >
          {domain.label}
        </span>
        <span
          style={{
            fontSize: 11,
            color: TEXT_MUTED,
            fontFamily: FONT_DATA,
          }}
        >
          ({domain.dims.length}D)
        </span>
      </div>

      {/* All-zero warning */}
      {allZero && (
        <div
          style={{
            fontSize: 10,
            color: "#f59e0b",
            fontFamily: FONT_UI,
            padding: "4px 10px 4px 13px",
            marginBottom: 4,
            background: "rgba(245, 158, 11, 0.08)",
            borderRadius: 3,
          }}
        >
          {"\u26A0"} All zero &mdash; needs more nuclei mapping to [{domain.regions.join(", ")}]
        </div>
      )}

      {/* Dimension bars */}
      <div style={{ display: "flex", flexDirection: "column", gap: 3, paddingLeft: 13 }}>
        {domain.dims.map((dimName, i) => {
          const val = values[i] ?? 0;
          const clampedVal = Math.max(0, Math.min(1, val));
          return (
            <div
              key={dimName}
              style={{ display: "flex", alignItems: "center", gap: 8 }}
            >
              {/* Dimension name */}
              <span
                style={{
                  width: 120,
                  fontSize: 10,
                  color: TEXT_SECONDARY,
                  fontFamily: FONT_UI,
                  flexShrink: 0,
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                }}
              >
                {dimName}
              </span>

              {/* Bar background */}
              <div
                style={{
                  flex: 1,
                  height: 10,
                  background: BG_SURFACE,
                  borderRadius: 2,
                  overflow: "hidden",
                  border: `1px solid ${BORDER}`,
                }}
              >
                {/* Bar fill */}
                <div
                  style={{
                    width: `${(clampedVal * 100).toFixed(1)}%`,
                    height: "100%",
                    background: domain.color,
                    opacity: 0.75,
                    borderRadius: 1,
                    transition: "width 0.1s ease-out",
                  }}
                />
              </div>

              {/* Value number */}
              <span
                style={{
                  width: 42,
                  fontSize: 10,
                  color: TEXT_PRIMARY,
                  fontFamily: FONT_DATA,
                  textAlign: "right",
                  flexShrink: 0,
                }}
              >
                {val.toFixed(3)}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ── Main page ───────────────────────────────────────────── */
export default function PsiPage(): React.ReactElement {
  const psiData = useStore((s) => s.psiData);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);

  // Compute per-domain values and means at current frame
  const { domainMeans, domainValues } = useMemo(() => {
    const means: number[] = [];
    const values: number[][] = [];

    for (const d of DOMAINS) {
      if (!psiData) {
        means.push(0);
        values.push(d.dims.map(() => 0));
        continue;
      }
      const domainFrames = psiData[d.key];
      if (!domainFrames || lodFrameIndex >= domainFrames.length) {
        means.push(0);
        values.push(d.dims.map(() => 0));
        continue;
      }
      const row = domainFrames[lodFrameIndex];
      if (!row || row.length === 0) {
        means.push(0);
        values.push(d.dims.map(() => 0));
        continue;
      }
      const vals = d.dims.map((_, i) => row[i] ?? 0);
      const sum = vals.reduce((a, b) => a + b, 0);
      const mean = vals.length > 0 ? sum / vals.length : 0;
      means.push(Math.max(0, Math.min(1, mean)));
      values.push(vals);
    }

    return { domainMeans: means, domainValues: values };
  }, [psiData, lodFrameIndex]);

  const noData = !psiData;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        background: BG_PRIMARY,
        fontFamily: FONT_UI,
      }}
    >
      {/* Page header */}
      <div
        style={{
          padding: "8px 16px",
          fontSize: 13,
          fontWeight: 700,
          color: TEXT_PRIMARY,
          borderBottom: `1px solid ${BORDER}`,
          background: BG_PANEL,
          flexShrink: 0,
          display: "flex",
          alignItems: "center",
          gap: 8,
        }}
      >
        <span style={{ color: ACCENT }}>&Psi;&sup3;</span>
        <span style={{ color: TEXT_MUTED, fontWeight: 400, fontSize: 11 }}>
          Cognitive State (28D)
        </span>
      </div>

      {noData ? (
        <div
          style={{
            flex: 1,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: TEXT_MUTED,
            fontSize: 13,
            fontFamily: FONT_UI,
          }}
        >
          Waiting for &Psi;&sup3; data&hellip;
        </div>
      ) : (
        <div
          style={{
            flex: 1,
            display: "flex",
            minHeight: 0,
            overflow: "hidden",
          }}
        >
          {/* Left half: Radar chart */}
          <div
            style={{
              flex: 1,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: 16,
              minWidth: 0,
            }}
          >
            <RadarChart domainMeans={domainMeans} />
          </div>

          {/* Divider */}
          <div style={{ width: 1, background: BORDER, flexShrink: 0 }} />

          {/* Right half: Scrollable domain breakdown */}
          <div
            style={{
              flex: 1,
              overflowY: "auto",
              padding: "12px 16px",
              minWidth: 0,
            }}
          >
            {DOMAINS.map((d, i) => {
              const vals = domainValues[i] ?? d.dims.map(() => 0);
              const allZero = vals.every((v) => v === 0);
              return (
                <DomainSection
                  key={d.key}
                  domain={d}
                  values={vals}
                  allZero={allZero}
                />
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
