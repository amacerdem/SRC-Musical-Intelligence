/* ── MindTypeRing — 5-segment donut showing gene distribution ──── */

import { useTranslation } from "react-i18next";
import type { MindGenes } from "@/types/m3";
import { GENE_NAMES, GENE_TO_TYPE, GENE_COLORS, getDominantGene } from "@/types/m3";
import { FAMILY_COLORS } from "@/data/persona-levels";

interface Props {
  genes: MindGenes;
  size?: number;
  showLabels?: boolean;
}

export function MindTypeRing({ genes, size = 120, showLabels = true }: Props) {
  const { t } = useTranslation();
  const safeGenes = genes ?? { entropy: 0.2, resolution: 0.2, tension: 0.2, resonance: 0.2, plasticity: 0.2 };
  const total = GENE_NAMES.reduce((s, g) => s + safeGenes[g], 0) || 1;
  const r = size / 2;
  const innerR = r * 0.6;
  const cx = r;
  const cy = r;

  let startAngle = -Math.PI / 2;
  const segments = GENE_NAMES.map((gene) => {
    const fraction = safeGenes[gene] / total;
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

    startAngle = endAngle;

    const mindType = GENE_TO_TYPE[gene];
    return {
      gene,
      mindType,
      path,
      color: GENE_COLORS[gene],
      pct: Math.round(fraction * 100),
      fraction,
    };
  });

  const dominantGene = getDominantGene(safeGenes);
  const dominantType = GENE_TO_TYPE[dominantGene];
  const dominantColor = FAMILY_COLORS[dominantType];
  const dominantPct = segments.find(s => s.gene === dominantGene)?.pct ?? 0;

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {segments.map((seg) => (
          <path
            key={seg.gene}
            d={seg.path}
            fill={seg.color}
            opacity={seg.gene === dominantGene ? 0.9 : 0.35}
            stroke="rgba(0,0,0,0.5)"
            strokeWidth={1}
          />
        ))}
        <text
          x={cx}
          y={cy - 4}
          textAnchor="middle"
          fill={dominantColor}
          fontSize={size * 0.12}
          fontFamily="var(--font-display)"
          fontWeight="600"
        >
          {dominantPct}%
        </text>
        <text
          x={cx}
          y={cy + size * 0.08}
          textAnchor="middle"
          fill="rgb(100,116,139)"
          fontSize={size * 0.065}
          fontFamily="var(--font-mono)"
        >
          {dominantType}
        </text>
      </svg>

      {showLabels && (
        <div className="flex flex-wrap justify-center gap-x-3 gap-y-1 mt-2">
          {segments.map((seg) => (
            <div key={seg.gene} className="flex items-center gap-1">
              <div
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: seg.color, opacity: seg.gene === dominantGene ? 1 : 0.5 }}
              />
              <span className="text-[9px] font-mono text-slate-500">
                {seg.pct}%
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
