/* ── FamilyAffinityRing — 5-segment donut showing family distribution ── */

import { useTranslation } from "react-i18next";
import type { FamilyAffinity } from "@/types/m3";
import { FAMILY_NAMES } from "@/types/m3";
import { FAMILY_COLORS } from "@/data/persona-levels";

interface Props {
  affinity: FamilyAffinity;
  size?: number;
  showLabels?: boolean;
}

export function FamilyAffinityRing({ affinity, size = 120, showLabels = true }: Props) {
  const { t } = useTranslation();
  const total = FAMILY_NAMES.reduce((s, f) => s + affinity[f], 0) || 1;
  const r = size / 2;
  const innerR = r * 0.6;
  const cx = r;
  const cy = r;

  // Build arc segments
  let startAngle = -Math.PI / 2; // start at top
  const segments = FAMILY_NAMES.map((family) => {
    const fraction = affinity[family] / total;
    const angle = fraction * Math.PI * 2;
    const endAngle = startAngle + angle;
    const largeArc = angle > Math.PI ? 1 : 0;

    const x1o = cx + Math.cos(startAngle) * r;
    const y1o = cy + Math.sin(startAngle) * r;
    const x2o = cx + Math.cos(endAngle) * r;
    const y2o = cy + Math.sin(endAngle) * r;
    const x1i = cx + Math.cos(endAngle) * innerR;
    const y1i = cy + Math.sin(endAngle) * innerR;
    const x2i = cx + Math.cos(startAngle) * innerR;
    const y2i = cy + Math.sin(startAngle) * innerR;

    const path = [
      `M ${x1o} ${y1o}`,
      `A ${r} ${r} 0 ${largeArc} 1 ${x2o} ${y2o}`,
      `L ${x1i} ${y1i}`,
      `A ${innerR} ${innerR} 0 ${largeArc} 0 ${x2i} ${y2i}`,
      `Z`,
    ].join(" ");

    // Label position at midpoint of arc
    const midAngle = startAngle + angle / 2;
    const labelR = (r + innerR) / 2;
    const labelX = cx + Math.cos(midAngle) * labelR;
    const labelY = cy + Math.sin(midAngle) * labelR;

    startAngle = endAngle;

    return {
      family,
      path,
      color: FAMILY_COLORS[family],
      pct: Math.round(fraction * 100),
      labelX,
      labelY,
      fraction,
    };
  });

  // Find dominant
  const dominant = segments.reduce((a, b) => (a.fraction > b.fraction ? a : b));

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {segments.map((seg) => (
          <path
            key={seg.family}
            d={seg.path}
            fill={seg.color}
            opacity={seg.family === dominant.family ? 0.9 : 0.4}
            stroke="rgba(0,0,0,0.5)"
            strokeWidth={1}
          />
        ))}
        {/* Center text */}
        <text
          x={cx}
          y={cy - 4}
          textAnchor="middle"
          fill={dominant.color}
          fontSize={size * 0.12}
          fontFamily="var(--font-display)"
          fontWeight="600"
        >
          {dominant.pct}%
        </text>
        <text
          x={cx}
          y={cy + size * 0.08}
          textAnchor="middle"
          fill="rgb(100,116,139)"
          fontSize={size * 0.07}
          fontFamily="var(--font-mono)"
        >
          {dominant.family.slice(0, 4)}
        </text>
      </svg>

      {showLabels && (
        <div className="flex flex-wrap justify-center gap-x-3 gap-y-1 mt-2">
          {segments.map((seg) => (
            <div key={seg.family} className="flex items-center gap-1">
              <div className="w-2 h-2 rounded-full" style={{ backgroundColor: seg.color, opacity: seg.family === dominant.family ? 1 : 0.5 }} />
              <span className="text-[9px] font-mono text-slate-500">{seg.pct}%</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
