import React, { useMemo, useState } from "react";
import { useStore } from "../store";

const BG = "#0d0d14";
const TEXT = "#c8c8d4";
const TEXT_SEC = "#8b8b9e";
const BORDER = "#252538";

const CHANNEL_COLORS: Record<string, string> = {
  DA: "#f97316",
  NE: "#06b6d4",
  OPI: "#fbbf24",
  "5HT": "#10b981",
};

const CHANNEL_NAMES = ["DA", "NE", "OPI", "5HT"];

const SVG_W = 400;
const SVG_H = 240;
const LEFT_X = 60;
const RIGHT_X = 340;
const NODE_R = 5;

/**
 * NeuroLinkEffectsPanel - Detail drawer SVG showing dims -> neurochemical channels.
 * Arrow styles by effect: produce=solid, amplify=double, inhibit=dashed.
 */
export default function NeuroLinkEffectsPanel(): React.ReactElement {
  const selectedNucleus = useStore((s) => s.selectedNucleus);
  const nucleusData = useStore((s) => s.nucleusData);
  const [hoverIdx, setHoverIdx] = useState<number | null>(null);

  const nd = selectedNucleus ? nucleusData[selectedNucleus] ?? null : null;
  const neuroLinks = nd?.neuro_links ?? [];

  // Unique dim names that have neuro links
  const uniqueDims = useMemo(() => {
    const set = new Set<string>();
    for (const l of neuroLinks) set.add(l.dim_name);
    return Array.from(set);
  }, [neuroLinks]);

  // Channels that appear
  const activeChannels = useMemo(() => {
    const set = new Set<string>();
    for (const l of neuroLinks) set.add(l.channel_name);
    return CHANNEL_NAMES.filter((c) => set.has(c));
  }, [neuroLinks]);

  const noData = !selectedNucleus || !nd || neuroLinks.length === 0;

  const dimY = (i: number) =>
    30 + (i / Math.max(1, uniqueDims.length - 1)) * (SVG_H - 60);
  const chY = (i: number) =>
    30 + (i / Math.max(1, activeChannels.length - 1)) * (SVG_H - 60);

  const dimIndexMap = new Map(uniqueDims.map((d, i) => [d, i]));
  const chIndexMap = new Map(activeChannels.map((c, i) => [c, i]));

  // Build arrowhead marker ID per channel
  const markerIds = activeChannels.map((c) => `arrow-${c.replace(/[^a-zA-Z0-9]/g, "")}`);

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
        NeuroLinks
      </div>
      <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
        {noData ? (
          <span style={{ color: TEXT_SEC, fontSize: 13, fontFamily: "Inter, sans-serif" }}>
            {!selectedNucleus
              ? "Select a nucleus"
              : neuroLinks.length === 0
                ? "No neuro links"
                : "Loading\u2026"}
          </span>
        ) : (
          <svg
            viewBox={`0 0 ${SVG_W} ${SVG_H}`}
            style={{ width: "100%", height: "100%", maxHeight: "100%" }}
            preserveAspectRatio="xMidYMid meet"
          >
            <defs>
              {activeChannels.map((c, i) => (
                <marker
                  key={c}
                  id={markerIds[i]}
                  viewBox="0 0 10 7"
                  refX={9}
                  refY={3.5}
                  markerWidth={8}
                  markerHeight={6}
                  orient="auto"
                >
                  <polygon
                    points="0 0, 10 3.5, 0 7"
                    fill={CHANNEL_COLORS[c] ?? TEXT}
                  />
                </marker>
              ))}
            </defs>

            <rect x={0} y={0} width={SVG_W} height={SVG_H} fill={BG} />

            {/* Arrow links */}
            {neuroLinks.map((l, i) => {
              const dIdx = dimIndexMap.get(l.dim_name) ?? 0;
              const cIdx = chIndexMap.get(l.channel_name) ?? 0;
              const y1 = dimY(dIdx);
              const y2 = chY(cIdx);
              const color = CHANNEL_COLORS[l.channel_name] ?? TEXT;
              const markerId = markerIds[cIdx] ?? "";

              // Stroke style by effect
              let strokeDasharray: string | undefined;
              let strokeWidth = 1.5;
              if (l.effect === "inhibit") {
                strokeDasharray = "4 3";
              } else if (l.effect === "amplify") {
                strokeWidth = 3;
              }
              // produce = solid (default)

              const isHovered = hoverIdx === i;

              return (
                <g key={i}>
                  {/* For amplify: draw a background stroke to create double-line effect */}
                  {l.effect === "amplify" && (
                    <line
                      x1={LEFT_X + NODE_R}
                      y1={y1}
                      x2={RIGHT_X - NODE_R - 10}
                      y2={y2}
                      stroke={BG}
                      strokeWidth={1.5}
                    />
                  )}
                  <line
                    x1={LEFT_X + NODE_R}
                    y1={y1}
                    x2={RIGHT_X - NODE_R - 10}
                    y2={y2}
                    stroke={color}
                    strokeWidth={strokeWidth}
                    strokeDasharray={strokeDasharray}
                    opacity={isHovered ? 1 : 0.7}
                    markerEnd={`url(#${markerId})`}
                    onMouseEnter={() => setHoverIdx(i)}
                    onMouseLeave={() => setHoverIdx(null)}
                    style={{ cursor: "pointer" }}
                  />
                  {/* Weight label on hover */}
                  {isHovered && (
                    <text
                      x={(LEFT_X + RIGHT_X) / 2}
                      y={(y1 + y2) / 2 - 6}
                      fill={color}
                      fontSize={9}
                      fontFamily="'JetBrains Mono', monospace"
                      textAnchor="middle"
                      fontWeight={600}
                    >
                      {l.weight.toFixed(3)}
                    </text>
                  )}
                </g>
              );
            })}

            {/* Dim nodes (left) */}
            {uniqueDims.map((d, i) => (
              <g key={`dim-${d}`}>
                <circle cx={LEFT_X} cy={dimY(i)} r={NODE_R} fill={TEXT} />
                <text
                  x={LEFT_X - NODE_R - 3}
                  y={dimY(i) + 3}
                  fill={TEXT}
                  fontSize={7}
                  fontFamily="'JetBrains Mono', monospace"
                  textAnchor="end"
                >
                  {d.length > 12 ? d.slice(0, 11) + "\u2026" : d}
                </text>
              </g>
            ))}

            {/* Channel nodes (right) */}
            {activeChannels.map((c, i) => {
              const color = CHANNEL_COLORS[c] ?? TEXT;
              return (
                <g key={`ch-${c}`}>
                  <circle cx={RIGHT_X} cy={chY(i)} r={NODE_R + 2} fill={color} />
                  <text
                    x={RIGHT_X + NODE_R + 6}
                    y={chY(i) + 3}
                    fill={color}
                    fontSize={10}
                    fontFamily="'JetBrains Mono', monospace"
                    fontWeight={700}
                    textAnchor="start"
                  >
                    {c}
                  </text>
                </g>
              );
            })}

            {/* Legend */}
            <g transform={`translate(${SVG_W - 120}, ${SVG_H - 50})`}>
              <line x1={0} x2={16} y1={0} y2={0} stroke={TEXT_SEC} strokeWidth={1.5} />
              <text x={20} y={3} fill={TEXT_SEC} fontSize={7} fontFamily="Inter, sans-serif">
                produce
              </text>
              <line x1={0} x2={16} y1={14} y2={14} stroke={TEXT_SEC} strokeWidth={3} />
              <text x={20} y={17} fill={TEXT_SEC} fontSize={7} fontFamily="Inter, sans-serif">
                amplify
              </text>
              <line
                x1={0} x2={16} y1={28} y2={28}
                stroke={TEXT_SEC} strokeWidth={1.5} strokeDasharray="4 3"
              />
              <text x={20} y={31} fill={TEXT_SEC} fontSize={7} fontFamily="Inter, sans-serif">
                inhibit
              </text>
            </g>
          </svg>
        )}
      </div>
    </div>
  );
}
