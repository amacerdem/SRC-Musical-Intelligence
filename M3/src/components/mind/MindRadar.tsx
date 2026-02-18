import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";
import type { MindAxes } from "@/types/mind";

interface Props {
  axes: MindAxes;
  color?: string;
  compareAxes?: MindAxes;
  compareColor?: string;
  size?: number;
}

const axisLabels: { key: keyof MindAxes; label: string }[] = [
  { key: "entropyTolerance", label: "Entropy" },
  { key: "resolutionCraving", label: "Resolution" },
  { key: "tensionAppetite", label: "Tension" },
  { key: "salienceSensitivity", label: "Salience" },
  { key: "monotonyTolerance", label: "Monotony" },
];

export function MindRadar({
  axes,
  color = "#A855F7",
  compareAxes,
  compareColor = "#6366F1",
  size = 300,
}: Props) {
  const data = axisLabels.map(({ key, label }) => ({
    axis: label,
    value: Math.round(axes[key] * 100),
    ...(compareAxes ? { compare: Math.round(compareAxes[key] * 100) } : {}),
  }));

  return (
    <ResponsiveContainer width={size} height={size}>
      <RadarChart data={data} cx="50%" cy="50%" outerRadius="65%">
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
