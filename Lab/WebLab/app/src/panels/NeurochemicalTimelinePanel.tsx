import React, { useMemo } from "react";
import { useStore } from "../store";

const BG = "#0d0d14";
const TEXT = "#c8c8d4";
const BORDER = "#252538";
const GRID_COLOR = "#1a1a2e";

const CHANNELS: { name: string; color: string }[] = [
  { name: "DA", color: "#f97316" },
  { name: "NE", color: "#06b6d4" },
  { name: "OPI", color: "#fbbf24" },
  { name: "5HT", color: "#10b981" },
];

const SVG_W = 600;
const SVG_H = 260;
const PAD_L = 32;
const PAD_R = 16;
const PAD_T = 16;
const PAD_B = 20;
const PLOT_W = SVG_W - PAD_L - PAD_R;
const PLOT_H = SVG_H - PAD_T - PAD_B;

function toSvgX(frame: number, total: number): number {
  if (total <= 1) return PAD_L;
  return PAD_L + (frame / (total - 1)) * PLOT_W;
}

function toSvgY(value: number): number {
  const clamped = Math.max(0, Math.min(1, value));
  return PAD_T + (1 - clamped) * PLOT_H;
}

/**
 * NeurochemicalTimelinePanel - 4-channel overlaid time-series traces (DA, NE, OPI, 5HT).
 * SVG with gridlines, baseline, playhead, legend, and current values.
 */
export default function NeurochemicalTimelinePanel(): React.ReactElement {
  const neuroData = useStore((s) => s.neuroData);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);

  const T = neuroData?.length ?? 0;

  // Build SVG path strings for each channel
  const paths = useMemo(() => {
    if (!neuroData || neuroData.length === 0) return [];
    return CHANNELS.map((ch, chIdx) => {
      const points = neuroData.map((frame, t) => {
        const x = toSvgX(t, neuroData.length);
        const y = toSvgY(frame[chIdx] ?? 0);
        return `${t === 0 ? "M" : "L"}${x.toFixed(1)},${y.toFixed(1)}`;
      });
      return { ...ch, d: points.join(" ") };
    });
  }, [neuroData]);

  // Current values at playhead
  const currentValues = neuroData?.[lodFrameIndex] ?? null;

  // Playhead x
  const playheadX = T > 0 ? toSvgX(lodFrameIndex, T) : 0;

  // Gridlines at 0, 0.25, 0.5, 0.75, 1.0
  const gridLevels = [0, 0.25, 0.5, 0.75, 1.0];

  const noData = !neuroData || neuroData.length === 0;

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
        Neurochemicals (4D)
      </div>
      <div style={{ flex: 1, position: "relative" }}>
        {noData ? (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
              color: TEXT,
              fontSize: 13,
              fontFamily: "Inter, sans-serif",
            }}
          >
            Waiting for neurochemical data&hellip;
          </div>
        ) : (
          <svg
            viewBox={`0 0 ${SVG_W} ${SVG_H}`}
            style={{ width: "100%", height: "100%", display: "block" }}
            preserveAspectRatio="xMidYMid meet"
          >
            {/* Background */}
            <rect x={0} y={0} width={SVG_W} height={SVG_H} fill={BG} />

            {/* Gridlines */}
            {gridLevels.map((level) => {
              const y = toSvgY(level);
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
                    fill={TEXT}
                    fontSize={8}
                    fontFamily="'JetBrains Mono', monospace"
                    textAnchor="end"
                    opacity={0.5}
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
              y1={toSvgY(0.5)}
              y2={toSvgY(0.5)}
              stroke={TEXT}
              strokeWidth={0.5}
              strokeDasharray="4 3"
              opacity={0.3}
            />

            {/* Channel traces */}
            {paths.map((p) => (
              <path
                key={p.name}
                d={p.d}
                fill="none"
                stroke={p.color}
                strokeWidth={1.5}
                opacity={0.9}
              />
            ))}

            {/* Playhead */}
            {T > 0 && (
              <line
                x1={playheadX}
                x2={playheadX}
                y1={PAD_T}
                y2={PAD_T + PLOT_H}
                stroke="#ef4444"
                strokeWidth={1.5}
              />
            )}

            {/* Legend in top-right corner */}
            {CHANNELS.map((ch, i) => (
              <g key={ch.name} transform={`translate(${SVG_W - PAD_R - 60}, ${PAD_T + 4 + i * 14})`}>
                <line x1={0} x2={12} y1={0} y2={0} stroke={ch.color} strokeWidth={2} />
                <text
                  x={16}
                  y={3}
                  fill={TEXT}
                  fontSize={9}
                  fontFamily="'JetBrains Mono', monospace"
                >
                  {ch.name}
                </text>
              </g>
            ))}

            {/* Current values at playhead */}
            {currentValues && (
              <g>
                {CHANNELS.map((ch, i) => {
                  const val = currentValues[i] ?? 0;
                  return (
                    <text
                      key={ch.name}
                      x={SVG_W - PAD_R - 60}
                      y={PAD_T + 4 + CHANNELS.length * 14 + 6 + i * 13}
                      fill={ch.color}
                      fontSize={9}
                      fontFamily="'JetBrains Mono', monospace"
                    >
                      {ch.name}: {val.toFixed(3)}
                    </text>
                  );
                })}
              </g>
            )}
          </svg>
        )}
      </div>
    </div>
  );
}
