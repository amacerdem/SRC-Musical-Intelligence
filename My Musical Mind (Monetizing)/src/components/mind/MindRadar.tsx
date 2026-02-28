import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";
import { useTranslation } from "react-i18next";
import type { MindAxes } from "@/types/mind";
import type { DimensionProfile } from "@/types/dimensions";
import { ALL_PSYCHOLOGY } from "@/data/dimensions";
import { DIMENSION_KEYS_6D } from "@/types/dimensions";

interface Props {
  axes?: MindAxes;
  profile?: DimensionProfile;
  color?: string;
  compareAxes?: MindAxes;
  compareProfile?: DimensionProfile;
  compareColor?: string;
  size?: number;
}

const legacyAxisKeys: { field: keyof MindAxes; tKey: string }[] = [
  { field: "entropyTolerance", tKey: "entropy" },
  { field: "resolutionCraving", tKey: "resolution" },
  { field: "tensionAppetite", tKey: "tension" },
  { field: "salienceSensitivity", tKey: "salience" },
  { field: "monotonyTolerance", tKey: "monotony" },
];

export function MindRadar({
  axes,
  profile,
  color = "#A855F7",
  compareAxes,
  compareProfile,
  compareColor = "#6366F1",
  size = 300,
}: Props) {
  const { t } = useTranslation();

  // ── 6D Dimension mode ──
  if (profile) {
    const data = ALL_PSYCHOLOGY.map((dim, i) => ({
      axis: dim.name,
      value: Math.round((profile[DIMENSION_KEYS_6D[i]] ?? 0) * 100),
      axisColor: dim.color,
      ...(compareProfile
        ? { compare: Math.round((compareProfile[DIMENSION_KEYS_6D[i]] ?? 0) * 100) }
        : {}),
    }));

    return (
      <ResponsiveContainer width={size} height={size}>
        <RadarChart data={data} cx="50%" cy="50%" outerRadius="50%">
          <PolarGrid stroke="#1E1E2E" />
          <PolarAngleAxis
            dataKey="axis"
            tick={({ x, y, payload, textAnchor }: any) => {
              const d = data.find(d => d.axis === payload.value);
              return (
                <text
                  x={x} y={y} textAnchor={textAnchor}
                  fill={d?.axisColor ?? "#94A3B8"}
                  fontSize={12} fontWeight={600} fontFamily="Inter"
                >
                  {payload.value}
                </text>
              );
            }}
          />
          <PolarRadiusAxis angle={90} domain={[0, 100]} tick={false} axisLine={false} />
          {compareProfile && (
            <Radar name="Compare" dataKey="compare" stroke={compareColor}
              fill={compareColor} fillOpacity={0.15} strokeWidth={1.5} />
          )}
          <Radar name="Mind" dataKey="value" stroke={color}
            fill={color} fillOpacity={0.25} strokeWidth={2} />
        </RadarChart>
      </ResponsiveContainer>
    );
  }

  // ── Legacy 5-axis mode ──
  if (!axes) return null;

  const data = legacyAxisKeys.map(({ field, tKey }) => ({
    axis: t(`dashboard.axes.${tKey}`),
    value: Math.round(axes[field] * 100),
    ...(compareAxes ? { compare: Math.round(compareAxes[field] * 100) } : {}),
  }));

  return (
    <ResponsiveContainer width={size} height={size}>
      <RadarChart data={data} cx="50%" cy="50%" outerRadius="50%">
        <PolarGrid stroke="#1E1E2E" />
        <PolarAngleAxis dataKey="axis"
          tick={{ fill: "#94A3B8", fontSize: 12, fontFamily: "Inter" }} />
        <PolarRadiusAxis angle={90} domain={[0, 100]} tick={false} axisLine={false} />
        {compareAxes && (
          <Radar name="Compare" dataKey="compare" stroke={compareColor}
            fill={compareColor} fillOpacity={0.15} strokeWidth={1.5} />
        )}
        <Radar name="Mind" dataKey="value" stroke={color}
          fill={color} fillOpacity={0.25} strokeWidth={2} />
      </RadarChart>
    </ResponsiveContainer>
  );
}
