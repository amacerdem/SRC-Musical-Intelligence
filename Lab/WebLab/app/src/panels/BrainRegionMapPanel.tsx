import React, { useMemo } from "react";
import { useStore } from "../store";

const BG = "#0d0d14";
const TEXT = "#c8c8d4";
const BORDER = "#252538";

const GROUP_COLORS: Record<string, string> = {
  cortical: "#3b82f6",
  subcortical: "#a855f7",
  brainstem: "#ef4444",
};

const SVG_W = 400;
const SVG_H = 300;
const PAD = 30;

/**
 * BrainRegionMapPanel - SVG with 26 brain region circles.
 * Positioned by MNI coords projected to 2D: x = mni_y, y = -mni_z.
 * Circle size and opacity driven by RAM activation at current frame.
 */
export default function BrainRegionMapPanel(): React.ReactElement {
  const ramData = useStore((s) => s.ramData);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);
  const regions = useStore((s) => s.regions);

  // Project MNI coords and compute scaling
  const projected = useMemo(() => {
    if (regions.length === 0) return [];
    const rawCoords = regions.map((r) => ({
      x: r.mni_coords[1], // mni_y (anterior-posterior)
      y: -r.mni_coords[2], // -mni_z (inferior-superior)
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
    const plotH = SVG_H - 2 * PAD;

    return regions.map((r, i) => ({
      region: r,
      svgX: PAD + ((rawCoords[i]!.x - minX) / rangeX) * plotW,
      svgY: PAD + ((rawCoords[i]!.y - minY) / rangeY) * plotH,
    }));
  }, [regions]);

  const frameValues = ramData?.[lodFrameIndex] ?? null;

  const noData = !ramData || regions.length === 0;

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
        Brain Regions &mdash; RAM (26D)
      </div>
      <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
        {noData ? (
          <span style={{ color: TEXT, fontSize: 13, fontFamily: "Inter, sans-serif" }}>
            Waiting for region data&hellip;
          </span>
        ) : (
          <svg
            viewBox={`0 0 ${SVG_W} ${SVG_H}`}
            style={{ width: "100%", height: "100%", maxHeight: "100%" }}
            preserveAspectRatio="xMidYMid meet"
          >
            <rect x={0} y={0} width={SVG_W} height={SVG_H} fill={BG} />
            {projected.map(({ region, svgX, svgY }, idx) => {
              const activation = frameValues
                ? Math.max(0, Math.min(1, frameValues[region.index] ?? 0))
                : 0;
              const radius = 6 + activation * 20;
              const opacity = 0.3 + activation * 0.7;
              const fillColor = GROUP_COLORS[region.group] ?? TEXT;

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
                    x={svgX + radius + 3}
                    y={svgY + 3}
                    fill={TEXT}
                    fontSize={8}
                    fontFamily="Inter, sans-serif"
                    opacity={0.8}
                  >
                    {region.abbreviation}
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
