/* -- MindRadar -- 5-Axis Pentagon Radar Chart (SVG) -------------------------
 *  Renders a radar chart with 5 axes for the Mind Genes:
 *    Entropy (E), Resolution (R), Tension (T), Resonance (Res), Plasticity (P)
 *  Background concentric pentagons at 25%, 50%, 75%, 100%.
 *  Filled polygon based on gene values.
 *  Uses react-native-svg.
 *  ----------------------------------------------------------------------- */

import React from "react";
import { View, StyleSheet } from "react-native";
import Svg, {
  Polygon,
  Line,
  Circle,
  Text as SvgText,
  G,
} from "react-native-svg";
import type { MindGenes } from "../../types/m3";
import { colors, fonts } from "../../design/tokens";

interface MindRadarProps {
  genes: MindGenes;
  size?: number;
}

const AXES = [
  { key: "entropy" as const, label: "E", fullLabel: "Entropy" },
  { key: "resolution" as const, label: "R", fullLabel: "Resolution" },
  { key: "tension" as const, label: "T", fullLabel: "Tension" },
  { key: "resonance" as const, label: "Res", fullLabel: "Resonance" },
  { key: "plasticity" as const, label: "P", fullLabel: "Plasticity" },
];

const AXIS_COLORS = [
  colors.tempo,       // entropy — orange
  colors.familiarity,  // resolution — blue
  "#EF4444",           // tension — red
  colors.success,      // resonance — green
  colors.reward,       // plasticity — amber
];

/** Convert a value (0-1) and axis index to (x, y) on the pentagon */
function polarToCartesian(
  cx: number,
  cy: number,
  radius: number,
  value: number,
  axisIndex: number,
  totalAxes: number,
): { x: number; y: number } {
  // Start from top (- PI/2), go clockwise
  const angle = (2 * Math.PI * axisIndex) / totalAxes - Math.PI / 2;
  const r = radius * value;
  return {
    x: cx + r * Math.cos(angle),
    y: cy + r * Math.sin(angle),
  };
}

/** Build a polygon points string for a given set of values at a fixed scale */
function makePolygonPoints(
  cx: number,
  cy: number,
  radius: number,
  values: number[],
): string {
  return values
    .map((v, i) => {
      const { x, y } = polarToCartesian(cx, cy, radius, v, i, values.length);
      return `${x},${y}`;
    })
    .join(" ");
}

export function MindRadar({ genes, size = 200 }: MindRadarProps) {
  const cx = size / 2;
  const cy = size / 2;
  const maxRadius = size / 2 - 24; // leave room for labels

  const values = AXES.map((a) => genes[a.key]);

  // Background concentric pentagons
  const bgLevels = [0.25, 0.50, 0.75, 1.0];

  return (
    <View style={[styles.container, { width: size, height: size }]}>
      <Svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {/* Background pentagons */}
        {bgLevels.map((level) => (
          <Polygon
            key={`bg-${level}`}
            points={makePolygonPoints(
              cx,
              cy,
              maxRadius,
              Array(5).fill(level),
            )}
            fill="none"
            stroke="rgba(255,255,255,0.06)"
            strokeWidth={0.75}
          />
        ))}

        {/* Axis lines */}
        {AXES.map((_, i) => {
          const { x, y } = polarToCartesian(cx, cy, maxRadius, 1, i, 5);
          return (
            <Line
              key={`axis-${i}`}
              x1={cx}
              y1={cy}
              x2={x}
              y2={y}
              stroke="rgba(255,255,255,0.06)"
              strokeWidth={0.75}
            />
          );
        })}

        {/* Value polygon (filled) */}
        <Polygon
          points={makePolygonPoints(cx, cy, maxRadius, values)}
          fill="rgba(139,92,246,0.15)"
          stroke={colors.violet}
          strokeWidth={1.5}
        />

        {/* Value dots on vertices */}
        {values.map((v, i) => {
          const { x, y } = polarToCartesian(cx, cy, maxRadius, v, i, 5);
          return (
            <Circle
              key={`dot-${i}`}
              cx={x}
              cy={y}
              r={3.5}
              fill={AXIS_COLORS[i]}
              stroke={colors.background}
              strokeWidth={1}
            />
          );
        })}

        {/* Axis labels */}
        {AXES.map((axis, i) => {
          const labelOffset = maxRadius + 14;
          const { x, y } = polarToCartesian(cx, cy, labelOffset, 1, i, 5);

          // Adjust text anchor based on position
          let textAnchor: "start" | "middle" | "end" = "middle";
          if (x < cx - 10) textAnchor = "end";
          else if (x > cx + 10) textAnchor = "start";

          return (
            <SvgText
              key={`label-${i}`}
              x={x}
              y={y + 4}
              fill={AXIS_COLORS[i]}
              fontSize={10}
              fontWeight="600"
              textAnchor={textAnchor}
            >
              {axis.label}
            </SvgText>
          );
        })}
      </Svg>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    justifyContent: "center",
  },
});
