import React, { useMemo } from "react";
import { useStore } from "../store";
import { colors, fonts } from "../theme/tokens";
import { buildSmoothPath } from "../utils/chart";

const CHART_H = 140;
const MARGIN = { top: 8, right: 130, bottom: 20, left: 44 };
const PLOT_H = CHART_H - MARGIN.top - MARGIN.bottom;
const LEFT_PANEL_W = 120;

const SCOPE_COLORS: Record<string, string> = {
  internal: colors.scope.internal,
  external: colors.scope.external,
  hybrid: colors.scope.hybrid,
};

const SCOPE_LABELS: Record<string, string> = {
  internal: "INT",
  external: "EXT",
  hybrid: "HYB",
};

/** Lighten a hex color for multi-line shading within a layer. */
function shadeForIndex(baseHex: string, index: number, total: number): string {
  const t = total <= 1 ? 0 : (index / (total - 1)) * 0.5 - 0.25;
  const r = parseInt(baseHex.slice(1, 3), 16);
  const g = parseInt(baseHex.slice(3, 5), 16);
  const b = parseInt(baseHex.slice(5, 7), 16);
  const mix = t > 0 ? 255 : 0;
  const p = Math.abs(t);
  return `rgb(${Math.round(r + (mix - r) * p)},${Math.round(g + (mix - g) * p)},${Math.round(b + (mix - b) * p)})`;
}

interface LayerChartProps {
  layerCode: string;
  layerName: string;
  scope: "internal" | "external" | "hybrid";
  start: number;
  end: number;
  dimNames: string[];
  output: number[][];
  lodFrameIndex: number;
}

function LayerChart({
  layerCode,
  layerName,
  scope,
  start,
  end,
  dimNames,
  output,
  lodFrameIndex,
}: LayerChartProps): React.ReactElement {
  const T = output.length;
  const dimCount = end - start;
  const plotW = 700;
  const svgW = MARGIN.left + plotW + MARGIN.right;
  const scopeColor = SCOPE_COLORS[scope] ?? colors.text.muted;

  // Build paths - memoized on output data
  const paths = useMemo(() => {
    const result: { d: string; color: string; dimIdx: number }[] = [];
    for (let i = 0; i < dimCount; i++) {
      result.push({
        d: buildSmoothPath(output, start + i, plotW, PLOT_H),
        color: shadeForIndex(scopeColor, i, dimCount),
        dimIdx: start + i,
      });
    }
    return result;
  }, [output, start, dimCount, scopeColor, plotW]);

  // Current values at playhead
  const currentValues = useMemo(() => {
    if (!output[lodFrameIndex]) return [];
    return paths.map((p) => {
      const v = output[lodFrameIndex]?.[p.dimIdx] ?? 0;
      return Math.max(0, Math.min(1, v));
    });
  }, [output, lodFrameIndex, paths]);

  const playheadX =
    T > 1 ? MARGIN.left + (lodFrameIndex / (T - 1)) * plotW : MARGIN.left;

  const yTicks = [0, 0.5, 1.0];

  return (
    <div style={{ marginBottom: 4 }}>
      {/* Layer header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          padding: "4px 12px",
          background: colors.bg.surface,
          borderLeft: `3px solid ${scopeColor}`,
        }}
      >
        <span
          style={{
            fontFamily: fonts.data,
            fontWeight: 700,
            fontSize: 12,
            color: scopeColor,
          }}
        >
          {layerCode}
        </span>
        <span
          style={{
            fontFamily: fonts.ui,
            fontSize: 11,
            color: colors.text.primary,
          }}
        >
          {layerName}
        </span>
        <span
          style={{
            fontFamily: fonts.data,
            fontSize: 9,
            color: scopeColor,
            background: scopeColor + "22",
            border: `1px solid ${scopeColor}44`,
            borderRadius: 3,
            padding: "1px 5px",
          }}
        >
          {SCOPE_LABELS[scope] ?? scope}
        </span>
        <span
          style={{
            fontFamily: fonts.data,
            fontSize: 10,
            color: colors.text.muted,
          }}
        >
          {dimCount}D
        </span>
      </div>

      {/* SVG chart */}
      <svg
        viewBox={`0 0 ${svgW} ${CHART_H}`}
        style={{ width: "100%", height: CHART_H, display: "block" }}
        preserveAspectRatio="none"
      >
        <rect x={0} y={0} width={svgW} height={CHART_H} fill={colors.bg.panel} />

        {/* Y grid */}
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
                {tick.toFixed(1)}
              </text>
            </g>
          );
        })}

        {/* Traces */}
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

        {/* Right legend: fixed positions, color-matched */}
        {paths.map((p, i) => {
          const val = currentValues[i] ?? 0;
          const lineHeight = dimCount > 1 ? PLOT_H / (dimCount - 1) : 0;
          const y = MARGIN.top + i * lineHeight;
          const dname = dimNames[i] ?? `d${i}`;
          const short = dname.length > 12 ? dname.slice(0, 11) + "\u2026" : dname;
          const xBase = MARGIN.left + plotW + 6;
          return (
            <g key={i}>
              <line
                x1={xBase}
                y1={y}
                x2={xBase + 12}
                y2={y}
                stroke={p.color}
                strokeWidth={2}
                opacity={0.85}
              />
              <text
                x={xBase + 16}
                y={y + 3}
                fill={p.color}
                fontSize={7}
                fontFamily={fonts.data}
                fontWeight={600}
              >
                {short}
              </text>
              <text
                x={xBase + 16}
                y={y + 12}
                fill={colors.text.secondary}
                fontSize={7}
                fontFamily={fonts.data}
              >
                {val.toFixed(3)}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

export default function NucleusPage(): React.ReactElement {
  const experiment = useStore((s) => s.experiment);
  const selectedNucleus = useStore((s) => s.selectedNucleus);
  const nucleusData = useStore((s) => s.nucleusData);
  const selectNucleus = useStore((s) => s.selectNucleus);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);

  const nd = selectedNucleus ? nucleusData[selectedNucleus] ?? null : null;

  return (
    <div
      style={{
        height: "100%",
        display: "flex",
        background: colors.bg.primary,
        overflow: "hidden",
      }}
    >
      {/* Left panel: nucleus list */}
      <div
        style={{
          width: LEFT_PANEL_W,
          flexShrink: 0,
          borderRight: `1px solid ${colors.border}`,
          overflowY: "auto",
          background: colors.bg.panel,
        }}
      >
        <div
          style={{
            padding: "6px 8px",
            fontSize: 10,
            fontWeight: 600,
            color: colors.text.muted,
            fontFamily: fonts.ui,
            textTransform: "uppercase",
            letterSpacing: 0.5,
            borderBottom: `1px solid ${colors.border}`,
          }}
        >
          Nuclei
        </div>
        {experiment?.nuclei.map((name) => {
          const isActive = name === selectedNucleus;
          const nData = nucleusData[name];
          return (
            <div
              key={name}
              onClick={() => selectNucleus(name)}
              style={{
                padding: "5px 8px",
                cursor: "pointer",
                borderLeft: isActive
                  ? `3px solid ${colors.accent}`
                  : "3px solid transparent",
                background: isActive ? colors.bg.surface : "transparent",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                transition: "background 0.1s",
              }}
              onMouseEnter={(e) => {
                if (!isActive)
                  (e.currentTarget as HTMLDivElement).style.background =
                    colors.bg.hover;
              }}
              onMouseLeave={(e) => {
                if (!isActive)
                  (e.currentTarget as HTMLDivElement).style.background =
                    "transparent";
              }}
            >
              <span
                style={{
                  fontFamily: fonts.data,
                  fontSize: 11,
                  fontWeight: isActive ? 600 : 400,
                  color: isActive ? colors.text.primary : colors.text.secondary,
                }}
              >
                {name}
              </span>
              {nData && (
                <span
                  style={{
                    fontFamily: fonts.data,
                    fontSize: 9,
                    color: colors.text.muted,
                  }}
                >
                  {nData.output_dim}D
                </span>
              )}
            </div>
          );
        })}
      </div>

      {/* Right area: detail */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
        }}
      >
        {!selectedNucleus || !nd ? (
          <div
            style={{
              flex: 1,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: colors.text.secondary,
              fontFamily: fonts.ui,
              fontSize: 14,
            }}
          >
            Select a nucleus
          </div>
        ) : (
          <>
            {/* Header */}
            <div
              style={{
                padding: "8px 16px",
                borderBottom: `1px solid ${colors.border}`,
                flexShrink: 0,
                display: "flex",
                alignItems: "center",
                gap: 10,
                flexWrap: "wrap",
              }}
            >
              <span
                style={{
                  fontFamily: fonts.ui,
                  fontWeight: 600,
                  fontSize: 14,
                  color: colors.text.primary,
                }}
              >
                {nd.name} &mdash; {nd.full_name} ({nd.output_dim}D)
              </span>
              <Badge label={nd.unit} color={colors.text.secondary} />
              <Badge label={nd.role} color={colors.roles?.[nd.role as keyof typeof colors.roles] ?? colors.text.secondary} />
              <Badge label={`depth ${nd.depth}`} color={colors.text.muted} />
              <Badge
                label={`v${nd.metadata.version}`}
                color={colors.tiers[nd.metadata.evidence_tier] ?? colors.text.muted}
              />
            </div>

            {/* Layer charts */}
            <div
              style={{
                flex: 1,
                overflowY: "auto",
                overflowX: "hidden",
                padding: "4px 8px",
              }}
            >
              {nd.layers.map((layer) => (
                <LayerChart
                  key={layer.code}
                  layerCode={layer.code}
                  layerName={layer.name}
                  scope={layer.scope}
                  start={layer.start}
                  end={layer.end}
                  dimNames={layer.dim_names}
                  output={nd.output}
                  lodFrameIndex={lodFrameIndex}
                />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function Badge({
  label,
  color,
}: {
  label: string;
  color: string;
}): React.ReactElement {
  return (
    <span
      style={{
        fontFamily: fonts.data,
        fontSize: 9,
        color,
        border: `1px solid ${color}44`,
        background: color + "18",
        borderRadius: 3,
        padding: "1px 6px",
        whiteSpace: "nowrap",
      }}
    >
      {label}
    </span>
  );
}
