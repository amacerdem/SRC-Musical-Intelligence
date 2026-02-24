interface LayerDef {
  label: string
  dim: number
  color: string
}

interface MechanismLayerChartProps {
  layers: LayerDef[]
  totalDim: number
  className?: string
}

const DEFAULT_COLORS: Record<string, string> = {
  E: '#f97316',
  M: '#8b5cf6',
  P: '#3b82f6',
  F: '#22c55e',
  'N+C': '#ec4899',
  'T+M': '#f59e0b',
}

export function MechanismLayerChart({ layers, totalDim, className = '' }: MechanismLayerChartProps) {
  return (
    <div className={className}>
      {/* Stacked bar */}
      <div className="flex h-5 rounded-md overflow-hidden bg-white/3 border border-border-subtle">
        {layers.map((layer, i) => (
          <div
            key={i}
            className="flex items-center justify-center text-[9px] font-semibold mono text-white/80 transition-all"
            style={{
              width: `${(layer.dim / totalDim) * 100}%`,
              backgroundColor: layer.color || DEFAULT_COLORS[layer.label] || '#666',
              opacity: 0.7,
            }}
            title={`${layer.label} [${layer.dim}D]`}
          >
            {layer.dim >= 2 && layer.label}
          </div>
        ))}
      </div>
      {/* Legend */}
      <div className="flex gap-3 mt-1.5">
        {layers.map((layer, i) => (
          <span key={i} className="flex items-center gap-1 text-[10px] text-text-secondary">
            <span
              className="w-2 h-2 rounded-sm"
              style={{ backgroundColor: layer.color || DEFAULT_COLORS[layer.label] || '#666', opacity: 0.7 }}
            />
            <span className="mono">{layer.label}[{layer.dim}]</span>
          </span>
        ))}
      </div>
    </div>
  )
}
