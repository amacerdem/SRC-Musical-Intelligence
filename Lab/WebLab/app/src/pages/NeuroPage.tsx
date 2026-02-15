import React, { useMemo } from "react";
import { useStore } from "../store";
import type { NeuroLinkInfo } from "../types/experiment";
import { buildSmoothPath } from "../utils/chart";

/* ── Theme ──────────────────────────────────────────────── */
const BG_PRIMARY = "#0a0a0f";
const BG_PANEL = "#0d0d14";
const BG_SURFACE = "#111118";
const TEXT_PRIMARY = "#c8c8d4";
const TEXT_SECONDARY = "#8b8b9e";
const TEXT_MUTED = "#5a5a6e";
const ACCENT = "#6366f1";
const BORDER = "#252538";
const PLAYHEAD = "#ef4444";
const GRID_COLOR = "#1a1a2e";
const FONT_UI = "'Inter', sans-serif";
const FONT_DATA = "'JetBrains Mono', monospace";

/* ── Channel definitions ─────────────────────────────────── */
interface ChannelDef {
  index: number;
  abbr: string;
  name: string;
  description: string;
  color: string;
}

const CHANNELS: ChannelDef[] = [
  { index: 0, abbr: "DA", name: "Dopamine", description: "Reward prediction error", color: "#f97316" },
  { index: 1, abbr: "NE", name: "Norepinephrine", description: "Arousal / exploration balance", color: "#06b6d4" },
  { index: 2, abbr: "OPI", name: "Endorphins", description: "Hedonic evaluation", color: "#fbbf24" },
  { index: 3, abbr: "5HT", name: "Serotonin", description: "Temporal discount rate", color: "#10b981" },
];

/* ── SVG dimensions ──────────────────────────────────────── */
const SVG_W = 800;
const SVG_H = 120;
const PAD_L = 36;
const PAD_R = 16;
const PAD_T = 12;
const PAD_B = 12;
const PLOT_W = SVG_W - PAD_L - PAD_R;
const PLOT_H = SVG_H - PAD_T - PAD_B;

/* ── Effect label formatting ────────────────────────────── */
function formatEffect(effect: NeuroLinkInfo["effect"]): string {
  switch (effect) {
    case "produce":
      return "Produced by";
    case "amplify":
      return "Amplified by";
    case "inhibit":
      return "Inhibited by";
    default:
      return effect;
  }
}

/* ── Single channel strip ────────────────────────────────── */
interface ChannelStripProps {
  channel: ChannelDef;
  neuroData: number[][] | null;
  lodFrameIndex: number;
  links: NeuroLinkInfo[];
}

function ChannelStrip({ channel, neuroData, lodFrameIndex, links }: ChannelStripProps): React.ReactElement {
  const T = neuroData?.length ?? 0;

  const currentValue = neuroData?.[lodFrameIndex]?.[channel.index] ?? 0;

  // Build smoothed SVG path for this channel
  const pathD = useMemo(() => {
    if (!neuroData || neuroData.length === 0) return "";
    return buildSmoothPath(neuroData, channel.index, PLOT_W, PLOT_H);
  }, [neuroData, channel.index]);

  const playheadX = T > 1 ? PAD_L + (lodFrameIndex / (T - 1)) * PLOT_W : PAD_L;
  const gridLevels = [0.25, 0.5, 0.75];
  const noData = !neuroData || neuroData.length === 0;

  // Relevant neuro links for this channel
  const channelLinks = links.filter((l) => l.channel === channel.index);

  return (
    <div
      style={{
        flex: 1,
        display: "flex",
        minHeight: 0,
        borderBottom: `1px solid ${BORDER}`,
        background: BG_PRIMARY,
      }}
    >
      {/* Left info area */}
      <div
        style={{
          width: 200,
          flexShrink: 0,
          padding: "10px 14px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          gap: 4,
          borderRight: `1px solid ${BORDER}`,
          background: BG_PANEL,
        }}
      >
        {/* Channel name */}
        <div style={{ display: "flex", alignItems: "baseline", gap: 6 }}>
          <span
            style={{
              fontSize: 18,
              fontWeight: 700,
              color: channel.color,
              fontFamily: FONT_DATA,
            }}
          >
            {channel.abbr}
          </span>
          <span style={{ fontSize: 11, color: TEXT_SECONDARY, fontFamily: FONT_UI }}>
            ({channel.name})
          </span>
        </div>

        {/* Current value */}
        <div
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: TEXT_PRIMARY,
            fontFamily: FONT_DATA,
            lineHeight: 1,
          }}
        >
          {noData ? "---" : currentValue.toFixed(2)}
        </div>

        {/* Description */}
        <div style={{ fontSize: 10, color: TEXT_MUTED, fontFamily: FONT_UI }}>
          {channel.description}
        </div>

        {/* Neuro link info */}
        <div style={{ marginTop: 4 }}>
          {channelLinks.length === 0 ? (
            <div style={{ fontSize: 9, color: TEXT_MUTED, fontFamily: FONT_UI, fontStyle: "italic" }}>
              No active producers (baseline)
            </div>
          ) : (
            channelLinks.map((link, i) => (
              <div
                key={i}
                style={{
                  fontSize: 9,
                  color: TEXT_SECONDARY,
                  fontFamily: FONT_UI,
                  lineHeight: 1.4,
                  marginBottom: 2,
                }}
              >
                <span style={{ color: channel.color }}>{formatEffect(link.effect)}: </span>
                {link.dim_name}{" "}
                <span style={{ fontFamily: FONT_DATA, color: TEXT_MUTED }}>
                  (w={link.weight.toFixed(2)})
                </span>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Right chart area */}
      <div style={{ flex: 1, minWidth: 0, position: "relative" }}>
        {noData ? (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
              color: TEXT_MUTED,
              fontSize: 12,
              fontFamily: FONT_UI,
            }}
          >
            Waiting for data&hellip;
          </div>
        ) : (
          <svg
            viewBox={`0 0 ${SVG_W} ${SVG_H}`}
            style={{ width: "100%", height: "100%", display: "block" }}
            preserveAspectRatio="none"
          >
            <rect x={0} y={0} width={SVG_W} height={SVG_H} fill={BG_SURFACE} />

            {/* Gridlines at 0.25, 0.5, 0.75 */}
            {gridLevels.map((level) => {
              const y = PAD_T + (1 - level) * PLOT_H;
              return (
                <g key={level}>
                  <line
                    x1={PAD_L}
                    x2={SVG_W - PAD_R}
                    y1={y}
                    y2={y}
                    stroke={GRID_COLOR}
                    strokeWidth={0.5}
                  />
                  <text
                    x={PAD_L - 4}
                    y={y + 3}
                    fill={TEXT_MUTED}
                    fontSize={7}
                    fontFamily={FONT_DATA}
                    textAnchor="end"
                  >
                    {level.toFixed(2)}
                  </text>
                </g>
              );
            })}

            {/* Dashed baseline at 0.5 */}
            <line
              x1={PAD_L}
              x2={SVG_W - PAD_R}
              y1={PAD_T + 0.5 * PLOT_H}
              y2={PAD_T + 0.5 * PLOT_H}
              stroke={TEXT_SECONDARY}
              strokeWidth={0.7}
              strokeDasharray="6 4"
              opacity={0.4}
            />
            <text
              x={SVG_W - PAD_R + 2}
              y={PAD_T + 0.5 * PLOT_H + 3}
              fill={TEXT_MUTED}
              fontSize={7}
              fontFamily={FONT_DATA}
            >
              baseline
            </text>

            {/* Y-axis boundary lines */}
            <line
              x1={PAD_L}
              x2={SVG_W - PAD_R}
              y1={PAD_T + PLOT_H}
              y2={PAD_T + PLOT_H}
              stroke={GRID_COLOR}
              strokeWidth={0.3}
            />
            <line
              x1={PAD_L}
              x2={SVG_W - PAD_R}
              y1={PAD_T}
              y2={PAD_T}
              stroke={GRID_COLOR}
              strokeWidth={0.3}
            />

            {/* Channel trace */}
            <g transform={`translate(${PAD_L},${PAD_T})`}>
              <path
                d={pathD}
                fill="none"
                stroke={channel.color}
                strokeWidth={1.8}
                opacity={0.9}
              />
            </g>

            {/* Playhead */}
            <line
              x1={playheadX}
              x2={playheadX}
              y1={PAD_T}
              y2={PAD_T + PLOT_H}
              stroke={PLAYHEAD}
              strokeWidth={1.5}
            />

            {/* Current value dot on trace */}
            <circle
              cx={playheadX}
              cy={PAD_T + (1 - Math.max(0, Math.min(1, currentValue))) * PLOT_H}
              r={3}
              fill={channel.color}
              stroke={BG_PRIMARY}
              strokeWidth={1}
            />
          </svg>
        )}
      </div>
    </div>
  );
}

/* ── Main page ───────────────────────────────────────────── */
export default function NeuroPage(): React.ReactElement {
  const neuroData = useStore((s) => s.neuroData);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);
  const selectedNucleus = useStore((s) => s.selectedNucleus);
  const nucleusData = useStore((s) => s.nucleusData);

  // Get neuro links from the selected nucleus
  const links: NeuroLinkInfo[] = useMemo(() => {
    if (!selectedNucleus) return [];
    const nd = nucleusData[selectedNucleus];
    return nd?.neuro_links ?? [];
  }, [selectedNucleus, nucleusData]);

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
        <span style={{ color: ACCENT }}>NEURO</span>
        <span style={{ color: TEXT_MUTED, fontWeight: 400, fontSize: 11 }}>
          Neurochemical Channels (4D)
        </span>
        {selectedNucleus && (
          <span
            style={{
              marginLeft: "auto",
              fontSize: 10,
              fontFamily: FONT_DATA,
              color: TEXT_SECONDARY,
            }}
          >
            nucleus: {selectedNucleus}
          </span>
        )}
      </div>

      {/* 4 channel strips, each 25% height */}
      {CHANNELS.map((ch) => (
        <ChannelStrip
          key={ch.abbr}
          channel={ch}
          neuroData={neuroData}
          lodFrameIndex={lodFrameIndex}
          links={links}
        />
      ))}
    </div>
  );
}
