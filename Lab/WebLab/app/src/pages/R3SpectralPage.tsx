import React, { useState, useMemo, useCallback } from "react";
import { useStore } from "../store";
import { colors, fonts, R3_GROUP_COLOR_MAP } from "../theme/tokens";
import { buildSmoothPath, lineColor } from "../utils/chart";

const CHART_H = 150;
const MARGIN = { top: 8, right: 6, bottom: 24, left: 48 };
const PLOT_H = CHART_H - MARGIN.top - MARGIN.bottom;
const LEGEND_W = 150;

interface GroupChartProps {
  letter: string;
  name: string;
  start: number;
  end: number;
  dim: number;
  r3Data: number[][];
  featureNames: string[];
  lodFrameIndex: number;
  groupColor: string;
}

function GroupChart({
  letter,
  name,
  start,
  end: _end,
  dim,
  r3Data,
  featureNames,
  lodFrameIndex,
  groupColor,
}: GroupChartProps): React.ReactElement {
  const T = r3Data.length;
  const plotW = 800; // viewBox internal width for the plot area
  const svgW = MARGIN.left + plotW + MARGIN.right;

  // Memoize path strings - only recompute when r3Data changes
  const paths = useMemo(() => {
    const result: { d: string; color: string; featureIdx: number }[] = [];
    for (let i = 0; i < dim; i++) {
      const featureIdx = start + i;
      result.push({
        d: buildSmoothPath(r3Data, featureIdx, plotW, PLOT_H),
        color: lineColor(i),
        featureIdx,
      });
    }
    return result;
  }, [r3Data, start, dim, plotW]);

  // Current values at playhead
  const currentValues = useMemo(() => {
    if (!r3Data[lodFrameIndex]) return [];
    return paths.map((p) => {
      const v = r3Data[lodFrameIndex]?.[p.featureIdx] ?? 0;
      return Math.max(0, Math.min(1, v));
    });
  }, [r3Data, lodFrameIndex, paths]);

  // Playhead x position
  const playheadX =
    T > 1 ? MARGIN.left + (lodFrameIndex / (T - 1)) * plotW : MARGIN.left;

  // Y axis ticks
  const yTicks = [0, 0.25, 0.5, 0.75, 1.0];

  return (
    <div style={{ marginBottom: 4 }}>
      {/* Group header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          padding: "6px 12px",
          borderLeft: `3px solid ${groupColor}`,
          background: colors.bg.surface,
        }}
      >
        <span
          style={{
            fontFamily: fonts.data,
            fontWeight: 700,
            fontSize: 13,
            color: groupColor,
          }}
        >
          {letter}
        </span>
        <span
          style={{
            fontFamily: fonts.ui,
            fontSize: 12,
            color: colors.text.primary,
          }}
        >
          {name}
        </span>
        <span
          style={{
            fontFamily: fonts.data,
            fontSize: 11,
            color: colors.text.muted,
          }}
        >
          {dim}D
        </span>
      </div>

      {/* Chart + legend row */}
      <div style={{ display: "flex", alignItems: "stretch" }}>
        {/* SVG chart */}
        <svg
          viewBox={`0 0 ${svgW} ${CHART_H}`}
          style={{ flex: 1, height: CHART_H, display: "block" }}
          preserveAspectRatio="none"
        >
          <rect x={0} y={0} width={svgW} height={CHART_H} fill={colors.bg.panel} />

          {/* Y axis grid lines and labels */}
          {yTicks.map((tick) => {
            const y = MARGIN.top + PLOT_H - tick * PLOT_H;
            return (
              <g key={tick}>
                <line
                  x1={MARGIN.left}
                  y1={y}
                  x2={MARGIN.left + plotW}
                  y2={y}
                  stroke={colors.border}
                  strokeWidth={0.5}
                />
                <text
                  x={MARGIN.left - 6}
                  y={y + 3}
                  textAnchor="end"
                  fill={colors.text.muted}
                  fontSize={8}
                  fontFamily={fonts.data}
                >
                  {tick.toFixed(2)}
                </text>
              </g>
            );
          })}

          {/* Feature line traces */}
          <g transform={`translate(${MARGIN.left},${MARGIN.top})`}>
            {paths.map((p, i) => (
              <path
                key={i}
                d={p.d}
                fill="none"
                stroke={p.color}
                strokeWidth={1.2}
                opacity={0.85}
              />
            ))}
          </g>

          {/* Playhead */}
          <line
            x1={playheadX}
            y1={MARGIN.top}
            x2={playheadX}
            y2={MARGIN.top + PLOT_H}
            stroke={colors.playhead}
            strokeWidth={1.5}
            opacity={0.9}
          />
        </svg>

        {/* HTML legend — outside SVG so text isn't distorted */}
        <div
          style={{
            width: LEGEND_W,
            flexShrink: 0,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            gap: 1,
            padding: "4px 6px",
            background: colors.bg.panel,
            overflow: "hidden",
          }}
        >
          {paths.map((p, i) => {
            const val = currentValues[i] ?? 0;
            const fname = featureNames[p.featureIdx] ?? `f${p.featureIdx}`;
            return (
              <div
                key={i}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 4,
                  lineHeight: 1.1,
                }}
              >
                <span
                  style={{
                    width: 10,
                    height: 2,
                    background: p.color,
                    flexShrink: 0,
                    borderRadius: 1,
                  }}
                />
                <span
                  style={{
                    fontSize: 9,
                    fontFamily: fonts.data,
                    color: p.color,
                    fontWeight: 600,
                    whiteSpace: "nowrap",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    flex: 1,
                    minWidth: 0,
                  }}
                >
                  {fname}
                </span>
                <span
                  style={{
                    fontSize: 9,
                    fontFamily: fonts.data,
                    color: colors.text.secondary,
                    flexShrink: 0,
                  }}
                >
                  {val.toFixed(2)}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

const DEFAULT_ENABLED = new Set(["A", "B", "C", "D"]);

export default function R3SpectralPage(): React.ReactElement {
  const r3Data = useStore((s) => s.r3Data);
  const r3Groups = useStore((s) => s.r3Groups);
  const r3FeatureNames = useStore((s) => s.r3FeatureNames);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);

  const [enabledGroups, setEnabledGroups] = useState<Set<string>>(
    () => new Set(DEFAULT_ENABLED),
  );

  const toggleGroup = useCallback((letter: string) => {
    setEnabledGroups((prev) => {
      const next = new Set(prev);
      if (next.has(letter)) {
        next.delete(letter);
      } else {
        next.add(letter);
      }
      return next;
    });
  }, []);

  if (!r3Data || r3Data.length === 0) {
    return (
      <div
        style={{
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: colors.bg.primary,
          color: colors.text.secondary,
          fontFamily: fonts.ui,
          fontSize: 14,
        }}
      >
        Waiting for R\u00b3 data\u2026
      </div>
    );
  }

  return (
    <div
      style={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        background: colors.bg.primary,
        overflow: "hidden",
      }}
    >
      {/* Title bar + group toggles */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: "8px 16px",
          borderBottom: `1px solid ${colors.border}`,
          flexShrink: 0,
        }}
      >
        <span
          style={{
            fontFamily: fonts.ui,
            fontWeight: 600,
            fontSize: 14,
            color: colors.text.primary,
            whiteSpace: "nowrap",
          }}
        >
          R\u00b3 Spectral Features &mdash; 97D
        </span>
        <div style={{ display: "flex", gap: 4, flexWrap: "wrap" }}>
          {r3Groups.map((g) => {
            const active = enabledGroups.has(g.letter);
            const gc = R3_GROUP_COLOR_MAP[g.letter] ?? colors.text.muted;
            return (
              <button
                key={g.letter}
                onClick={() => toggleGroup(g.letter)}
                title={`${g.letter}: ${g.name} (${g.dim}D)`}
                style={{
                  border: `1px solid ${active ? gc : colors.border}`,
                  background: active ? gc + "22" : "transparent",
                  color: active ? gc : colors.text.muted,
                  fontFamily: fonts.data,
                  fontSize: 11,
                  fontWeight: 600,
                  padding: "2px 8px",
                  borderRadius: 4,
                  cursor: "pointer",
                  lineHeight: "16px",
                }}
              >
                {g.letter}
              </button>
            );
          })}
        </div>
      </div>

      {/* Scrollable chart area */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          overflowX: "hidden",
          padding: "4px 8px",
        }}
      >
        {r3Groups
          .filter((g) => enabledGroups.has(g.letter))
          .map((g) => (
            <GroupChart
              key={g.letter}
              letter={g.letter}
              name={g.name}
              start={g.start}
              end={g.end}
              dim={g.dim}
              r3Data={r3Data}
              featureNames={r3FeatureNames}
              lodFrameIndex={lodFrameIndex}
              groupColor={R3_GROUP_COLOR_MAP[g.letter] ?? colors.text.muted}
            />
          ))}
      </div>
    </div>
  );
}
