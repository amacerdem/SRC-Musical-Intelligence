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

interface Props {
  axes: MindAxes;
  color?: string;
  compareAxes?: MindAxes;
  compareColor?: string;
  size?: number;
}

const axisKeys: { field: keyof MindAxes; tKey: string }[] = [
  { field: "entropyTolerance", tKey: "entropy" },
  { field: "resolutionCraving", tKey: "resolution" },
  { field: "tensionAppetite", tKey: "tension" },
  { field: "salienceSensitivity", tKey: "salience" },
  { field: "monotonyTolerance", tKey: "monotony" },
];

export function MindRadar({
  axes,
  color = "#A855F7",
  compareAxes,
  compareColor = "#6366F1",
  size = 300,
}: Props) {
  const { t } = useTranslation();

  const data = axisKeys.map(({ field, tKey }) => ({
    axis: t(`dashboard.axes.${tKey}`),
    value: Math.round(axes[field] * 100),
    ...(compareAxes ? { compare: Math.round(compareAxes[field] * 100) } : {}),
  }));

  return (
    <ResponsiveContainer width={size} height={size}>
      <RadarChart data={data} cx="50%" cy="50%" outerRadius="50%">
        <PolarGrid stroke="#1E1E2E" />
        <PolarAngleAxis
          dataKey="axis"
          tick={{ fill: "#94A3B8", fontSize: 12, fontFamily: "Inter" }}
        />
        <PolarRadiusAxis
          angle={90}
          domain={[0, 100]}
          tick={false}
          axisLine={false}
        />
        {compareAxes && (
          <Radar
            name="Compare"
            dataKey="compare"
            stroke={compareColor}
            fill={compareColor}
            fillOpacity={0.15}
            strokeWidth={1.5}
          />
        )}
        <Radar
          name="Mind"
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
