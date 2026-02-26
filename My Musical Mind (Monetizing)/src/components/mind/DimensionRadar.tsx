/* ── DimensionRadar — 6D Psychology Radar Chart ──────────────────
 *  Displays the 6D dimension profile as a radar visualization.
 *  Supports comparison mode (persona canonical vs. live M³ state).
 *  Follows the same pattern as MindRadar.tsx.
 *  ──────────────────────────────────────────────────────────────── */

import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";
import { useTranslation } from "react-i18next";
import type { DimensionProfile } from "@/types/dimensions";
import { DIMENSION_KEYS_6D } from "@/types/dimensions";
import { PSYCHOLOGY_COLORS } from "@/data/dimensions";

interface Props {
  /** Primary 6D profile to display */
  profile: DimensionProfile;
  /** Color for the primary radar area */
  color?: string;
  /** Optional comparison profile (e.g., persona canonical vs live state) */
  compareProfile?: DimensionProfile;
  /** Color for comparison overlay */
  compareColor?: string;
  /** Chart size in pixels */
  size?: number;
  /** Show dimension-specific colors on each axis point */
  coloredAxes?: boolean;
}

export function DimensionRadar({
  profile,
  color = "#A855F7",
  compareProfile,
  compareColor = "#6366F1",
  size = 300,
  coloredAxes = false,
}: Props) {
  const { t, i18n } = useTranslation();
  const isTr = i18n.language === "tr";

  const data = DIMENSION_KEYS_6D.map((key) => ({
    axis: isTr ? t(`dimensions.6d.${key}`) : key.charAt(0).toUpperCase() + key.slice(1),
    key,
    value: Math.round((profile[key] ?? 0) * 100),
    ...(compareProfile ? { compare: Math.round((compareProfile[key] ?? 0) * 100) } : {}),
  }));

  const renderTick = (props: { x: number; y: number; payload: { value: string; index: number } }) => {
    const { x, y, payload } = props;
    const dimKey = DIMENSION_KEYS_6D[payload.index];
    const fillColor = coloredAxes && dimKey ? PSYCHOLOGY_COLORS[dimKey] : "#94A3B8";
    return (
      <text
        x={x}
        y={y}
        fill={fillColor}
        fontSize={11}
        fontFamily="Inter"
        textAnchor="middle"
        dominantBaseline="middle"
      >
        {payload.value}
      </text>
    );
  };

  return (
    <ResponsiveContainer width={size} height={size}>
      <RadarChart data={data} cx="50%" cy="50%" outerRadius="50%">
        <PolarGrid stroke="#1E1E2E" />
        <PolarAngleAxis
          dataKey="axis"
          tick={renderTick as unknown as React.ComponentProps<typeof PolarAngleAxis>["tick"]}
        />
        <PolarRadiusAxis
          angle={90}
          domain={[0, 100]}
          tick={false}
          axisLine={false}
        />
        {compareProfile && (
          <Radar
            name="Canonical"
            dataKey="compare"
            stroke={compareColor}
            fill={compareColor}
            fillOpacity={0.15}
            strokeWidth={1.5}
          />
        )}
        <Radar
          name="Dimensions"
          dataKey="value"
          stroke={color}
          fill={color}
          fillOpacity={0.25}
          strokeWidth={2}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}
