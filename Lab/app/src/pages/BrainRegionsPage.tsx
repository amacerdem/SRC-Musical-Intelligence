import React, { useMemo } from "react";
import { useStore } from "../store";
import { colors, fonts } from "../theme/tokens";
import type { RegionInfo } from "../types/experiment";

const GROUP_COLORS: Record<string, string> = {
  cortical: colors.regions.cortical,
  subcortical: colors.regions.subcortical,
  brainstem: colors.regions.brainstem,
};

const GROUP_LABELS: Record<string, string> = {
  cortical: "Cortical",
  subcortical: "Subcortical",
  brainstem: "Brainstem",
};

const SVG_W = 480;
const SVG_H = 400;
const PAD = 40;

export default function BrainRegionsPage(): React.ReactElement {
  const ramData = useStore((s) => s.ramData);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);
  const regions = useStore((s) => s.regions);

  // Project MNI coords to 2D SVG positions
  const projected = useMemo(() => {
    if (regions.length === 0) return [];
    const rawCoords = regions.map((r) => ({
      x: r.mni_coords[1],
      y: -r.mni_coords[2],
    }));
    const xs = rawCoords.map((c) => c.x);
    const ys = rawCoords.map((c) => c.y);
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);
    const rangeX = maxX - minX || 1;
    const rangeY = maxY - minY || 1;
    const plotW = SVG_W - 2 * PAD;
    const plotH = SVG_H - 2 * PAD - 40; // reserve bottom for legend

    return regions.map((r, i) => ({
      region: r,
      svgX: PAD + ((rawCoords[i]!.x - minX) / rangeX) * plotW,
      svgY: PAD + ((rawCoords[i]!.y - minY) / rangeY) * plotH,
    }));
  }, [regions]);

  // Group regions for the right-side bar list
  const groupedRegions = useMemo(() => {
    const groups: Record<string, RegionInfo[]> = {
      cortical: [],
      subcortical: [],
      brainstem: [],
    };
    for (const r of regions) {
      const list = groups[r.group];
      if (list) {
        list.push(r);
      }
    }
    return groups;
  }, [regions]);

  const frameValues = ramData?.[lodFrameIndex] ?? null;
  const noData = !ramData || regions.length === 0;

  if (noData) {
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
        Waiting for brain region data...
      </div>
    );
  }

  return (
    <div
      style={{
        height: "100%",
        display: "flex",
        background: colors.bg.primary,
        overflow: "hidden",
      }}
    >
      {/* Left half: SVG brain map */}
      <div
        style={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          borderRight: `1px solid ${colors.border}`,
          overflow: "hidden",
          padding: 8,
        }}
      >
        <svg
          viewBox={`0 0 ${SVG_W} ${SVG_H}`}
          style={{ width: "100%", height: "100%", maxWidth: SVG_W * 1.5 }}
          preserveAspectRatio="xMidYMid meet"
        >
          <rect x={0} y={0} width={SVG_W} height={SVG_H} fill={colors.bg.panel} rx={6} />

          {/* Title */}
          <text
            x={SVG_W / 2}
            y={20}
            textAnchor="middle"
            fill={colors.text.secondary}
            fontSize={11}
            fontFamily={fonts.ui}
          >
            Brain Region Activation Map (MNI projection)
          </text>

          {/* Region circles */}
          {projected.map(({ region, svgX, svgY }) => {
            const activation = frameValues
              ? Math.max(0, Math.min(1, frameValues[region.index] ?? 0))
              : 0;
            const radius = 8 + activation * 18;
            const opacity = 0.3 + activation * 0.7;
            const fillColor = GROUP_COLORS[region.group] ?? colors.text.muted;

            return (
              <g key={region.abbreviation}>
                <circle
                  cx={svgX}
                  cy={svgY}
                  r={radius}
                  fill={fillColor}
                  opacity={opacity}
                />
                <text
                  x={svgX + radius + 4}
                  y={svgY + 3}
                  fill={colors.text.secondary}
                  fontSize={8}
                  fontFamily={fonts.data}
                  opacity={0.9}
                >
                  {region.abbreviation}
                </text>
              </g>
            );
          })}

          {/* Legend */}
          {(["cortical", "subcortical", "brainstem"] as const).map(
            (group, i) => {
              const cx = 60 + i * 150;
              const cy = SVG_H - 16;
              return (
                <g key={group}>
                  <circle
                    cx={cx}
                    cy={cy}
                    r={5}
                    fill={GROUP_COLORS[group]}
                    opacity={0.8}
                  />
                  <text
                    x={cx + 10}
                    y={cy + 3}
                    fill={colors.text.secondary}
                    fontSize={9}
                    fontFamily={fonts.ui}
                  >
                    {GROUP_LABELS[group]}
                  </text>
                </g>
              );
            },
          )}
        </svg>
      </div>

      {/* Right half: activation bar list */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "8px 12px",
        }}
      >
        <div
          style={{
            fontFamily: fonts.ui,
            fontWeight: 600,
            fontSize: 13,
            color: colors.text.primary,
            marginBottom: 8,
            padding: "4px 0",
            borderBottom: `1px solid ${colors.border}`,
          }}
        >
          Region Activation &mdash; Frame {lodFrameIndex}
        </div>

        {(["cortical", "subcortical", "brainstem"] as const).map((group) => {
          const regionList = groupedRegions[group] ?? [];
          if (regionList.length === 0) return null;
          const groupColor = GROUP_COLORS[group] ?? colors.text.muted;

          return (
            <div key={group} style={{ marginBottom: 12 }}>
              {/* Section header */}
              <div
                style={{
                  fontFamily: fonts.ui,
                  fontSize: 11,
                  fontWeight: 600,
                  color: groupColor,
                  textTransform: "uppercase",
                  letterSpacing: 0.5,
                  marginBottom: 4,
                  paddingBottom: 2,
                  borderBottom: `1px solid ${groupColor}33`,
                }}
              >
                {GROUP_LABELS[group]}
              </div>

              {regionList.map((region) => {
                const val = frameValues
                  ? Math.max(0, Math.min(1, frameValues[region.index] ?? 0))
                  : 0;

                return (
                  <div
                    key={region.abbreviation}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 6,
                      padding: "3px 0",
                    }}
                  >
                    {/* Abbreviation */}
                    <span
                      style={{
                        fontFamily: fonts.data,
                        fontSize: 10,
                        fontWeight: 600,
                        color: groupColor,
                        width: 36,
                        flexShrink: 0,
                        textAlign: "right",
                      }}
                    >
                      {region.abbreviation}
                    </span>

                    {/* Full name */}
                    <span
                      style={{
                        fontFamily: fonts.ui,
                        fontSize: 10,
                        color: colors.text.secondary,
                        width: 120,
                        flexShrink: 0,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {region.name}
                    </span>

                    {/* Value */}
                    <span
                      style={{
                        fontFamily: fonts.data,
                        fontSize: 9,
                        color: colors.text.muted,
                        width: 32,
                        flexShrink: 0,
                        textAlign: "right",
                      }}
                    >
                      {val.toFixed(2)}
                    </span>

                    {/* Bar */}
                    <div
                      style={{
                        flex: 1,
                        height: 10,
                        background: colors.bg.surface,
                        borderRadius: 2,
                        overflow: "hidden",
                        position: "relative",
                      }}
                    >
                      <div
                        style={{
                          position: "absolute",
                          top: 0,
                          left: 0,
                          height: "100%",
                          width: `${val * 100}%`,
                          background: groupColor,
                          opacity: 0.7,
                          borderRadius: 2,
                          transition: "width 0.1s ease-out",
                        }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>
    </div>
  );
}
