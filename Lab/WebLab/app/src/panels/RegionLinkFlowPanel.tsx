import React, { useMemo, useState } from "react";
import { useStore } from "../store";

const BG = "#0d0d14";
const TEXT = "#c8c8d4";
const TEXT_SEC = "#8b8b9e";
const BORDER = "#252538";

const SCOPE_COLORS: Record<string, string> = {
  internal: "#3b82f6",
  external: "#22c55e",
  hybrid: "#f59e0b",
};

const REGION_GROUP_COLORS: Record<string, string> = {
  cortical: "#3b82f6",
  subcortical: "#a855f7",
  brainstem: "#ef4444",
};

const SVG_W = 400;
const SVG_H = 280;
const LEFT_X = 40;
const RIGHT_X = 360;
const NODE_R = 5;

interface HoverInfo {
  weight: number;
  citation: string;
  dimName: string;
  regionAbbr: string;
}

/**
 * RegionLinkFlowPanel - Sankey-style detail drawer showing nucleus dims -> brain regions.
 * Left column: dimension names, right column: region abbreviations.
 * Curved paths connecting them, width proportional to weight.
 */
export default function RegionLinkFlowPanel(): React.ReactElement {
  const selectedNucleus = useStore((s) => s.selectedNucleus);
  const nucleusData = useStore((s) => s.nucleusData);
  const regions = useStore((s) => s.regions);
  const [hover, setHover] = useState<HoverInfo | null>(null);

  const nd = selectedNucleus ? nucleusData[selectedNucleus] ?? null : null;
  const links = nd?.region_links ?? [];

  // Build dim -> scope map from layers
  const dimScopeMap = useMemo(() => {
    if (!nd) return new Map<string, string>();
    const m = new Map<string, string>();
    for (const layer of nd.layers) {
      for (const dn of layer.dim_names) {
        m.set(dn, layer.scope);
      }
    }
    return m;
  }, [nd]);

  // Build region abbreviation -> group map
  const regionGroupMap = useMemo(() => {
    const m = new Map<string, string>();
    for (const r of regions) {
      m.set(r.abbreviation, r.group);
    }
    return m;
  }, [regions]);

  // Unique dims and regions from links
  const { uniqueDims, uniqueRegions } = useMemo(() => {
    const dimSet = new Set<string>();
    const regSet = new Set<string>();
    for (const l of links) {
      dimSet.add(l.dim_name);
      regSet.add(l.region);
    }
    return {
      uniqueDims: Array.from(dimSet),
      uniqueRegions: Array.from(regSet),
    };
  }, [links]);

  // Compute max weight for scaling
  const maxWeight = useMemo(() => {
    if (links.length === 0) return 1;
    return Math.max(...links.map((l) => Math.abs(l.weight)), 0.01);
  }, [links]);

  const noData = !selectedNucleus || !nd || links.length === 0;

  // Layout: distribute dims and regions vertically
  const dimY = (i: number) => 24 + (i / Math.max(1, uniqueDims.length - 1)) * (SVG_H - 48);
  const regY = (i: number) => 24 + (i / Math.max(1, uniqueRegions.length - 1)) * (SVG_H - 48);

  // Index maps
  const dimIndexMap = new Map(uniqueDims.map((d, i) => [d, i]));
  const regIndexMap = new Map(uniqueRegions.map((r, i) => [r, i]));

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
        position: "relative",
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
        RegionLinks
      </div>
      <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
        {noData ? (
          <span style={{ color: TEXT_SEC, fontSize: 13, fontFamily: "Inter, sans-serif" }}>
            {!selectedNucleus
              ? "Select a nucleus"
              : links.length === 0
                ? "No region links"
                : "Loading\u2026"}
          </span>
        ) : (
          <svg
            viewBox={`0 0 ${SVG_W} ${SVG_H}`}
            style={{ width: "100%", height: "100%", maxHeight: "100%" }}
            preserveAspectRatio="xMidYMid meet"
          >
            <rect x={0} y={0} width={SVG_W} height={SVG_H} fill={BG} />

            {/* Curved link paths */}
            {links.map((l, i) => {
              const dIdx = dimIndexMap.get(l.dim_name) ?? 0;
              const rIdx = regIndexMap.get(l.region) ?? 0;
              const y1 = dimY(dIdx);
              const y2 = regY(rIdx);
              const strokeW = 1 + (Math.abs(l.weight) / maxWeight) * 5;
              const scope = dimScopeMap.get(l.dim_name) ?? "internal";
              const color = SCOPE_COLORS[scope] ?? TEXT;
              const midX = (LEFT_X + RIGHT_X) / 2;
              const d = `M${LEFT_X + NODE_R},${y1} C${midX},${y1} ${midX},${y2} ${RIGHT_X - NODE_R},${y2}`;

              return (
                <path
                  key={i}
                  d={d}
                  fill="none"
                  stroke={color}
                  strokeWidth={strokeW}
                  opacity={0.5}
                  onMouseEnter={() =>
                    setHover({
                      weight: l.weight,
                      citation: l.citation,
                      dimName: l.dim_name,
                      regionAbbr: l.region,
                    })
                  }
                  onMouseLeave={() => setHover(null)}
                  style={{ cursor: "pointer" }}
                />
              );
            })}

            {/* Dim nodes (left) */}
            {uniqueDims.map((d, i) => {
              const scope = dimScopeMap.get(d) ?? "internal";
              const color = SCOPE_COLORS[scope] ?? TEXT;
              return (
                <g key={`dim-${d}`}>
                  <circle cx={LEFT_X} cy={dimY(i)} r={NODE_R} fill={color} />
                  <text
                    x={LEFT_X - NODE_R - 3}
                    y={dimY(i) + 3}
                    fill={color}
                    fontSize={7}
                    fontFamily="'JetBrains Mono', monospace"
                    textAnchor="end"
                  >
                    {d.length > 12 ? d.slice(0, 11) + "\u2026" : d}
                  </text>
                </g>
              );
            })}

            {/* Region nodes (right) */}
            {uniqueRegions.map((r, i) => {
              const group = regionGroupMap.get(r) ?? "cortical";
              const color = REGION_GROUP_COLORS[group] ?? TEXT;
              return (
                <g key={`reg-${r}`}>
                  <circle cx={RIGHT_X} cy={regY(i)} r={NODE_R} fill={color} />
                  <text
                    x={RIGHT_X + NODE_R + 3}
                    y={regY(i) + 3}
                    fill={color}
                    fontSize={8}
                    fontFamily="'JetBrains Mono', monospace"
                    textAnchor="start"
                  >
                    {r}
                  </text>
                </g>
              );
            })}
          </svg>
        )}
      </div>

      {/* Hover tooltip */}
      {hover && (
        <div
          style={{
            position: "absolute",
            bottom: 8,
            left: 8,
            right: 8,
            background: "#1a1a24",
            border: `1px solid ${BORDER}`,
            borderRadius: 4,
            padding: "6px 8px",
            fontSize: 10,
            fontFamily: "'JetBrains Mono', monospace",
            color: TEXT,
            zIndex: 10,
          }}
        >
          <span style={{ fontWeight: 600 }}>
            {hover.dimName} &rarr; {hover.regionAbbr}
          </span>
          {" | "}
          <span>weight: {hover.weight.toFixed(3)}</span>
          {hover.citation && (
            <span style={{ color: TEXT_SEC, marginLeft: 8, fontStyle: "italic" }}>
              {hover.citation}
            </span>
          )}
        </div>
      )}
    </div>
  );
}
