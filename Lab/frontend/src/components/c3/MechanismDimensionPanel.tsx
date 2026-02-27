import { useRelayDimensions } from '../../hooks/useRelayDimensions'
import { MiniTrace } from '../charts/MiniTrace'
import type { SourceDim } from '../../data/beliefs'

interface MechanismDimensionPanelProps {
  mechanismName: string
  experimentId: string | null
  beliefSourceDims?: SourceDim[]
  cursorFrame?: number
  totalFrames?: number
}

const LAYER_COLORS: Record<string, string> = {
  E: '#f97316',  // orange — Extraction
  M: '#8b5cf6',  // violet — Memory
  P: '#3b82f6',  // blue   — Present
  F: '#22c55e',  // green  — Forecast
}

const SCOPE_LABELS: Record<string, string> = {
  internal: 'int',
  hybrid: 'hyb',
  external: 'ext',
}

export function MechanismDimensionPanel({
  mechanismName,
  experimentId,
  beliefSourceDims,
  cursorFrame,
  totalFrames,
}: MechanismDimensionPanelProps) {
  const { layers, loading } = useRelayDimensions(mechanismName, experimentId, true)

  // Build set of source dim names for highlighting
  const sourceDimNames = new Set(beliefSourceDims?.map((sd) => sd.name) ?? [])

  const totalDims = layers?.reduce((sum, l) => sum + l.traces.length, 0) ?? 0

  return (
    <div className="space-y-1">
      {/* Header */}
      <div className="flex items-center justify-between mb-1">
        <div className="text-[10px] text-text-tertiary uppercase tracking-wider">
          {mechanismName} Dimensions
        </div>
        <div className="text-[10px] text-text-tertiary mono">
          {totalDims > 0 ? `${totalDims}D` : ''}
          {loading && <span className="text-blue-400 animate-pulse ml-2">loading...</span>}
        </div>
      </div>

      {!layers && !loading && (
        <div className="text-[10px] text-text-tertiary/60 py-1">no data</div>
      )}

      {/* Per-layer groups */}
      {layers?.map((layer) => {
        const layerColor = LAYER_COLORS[layer.code] ?? '#888'
        const scopeLabel = SCOPE_LABELS[layer.scope] ?? layer.scope

        return (
          <div key={layer.code}>
            {/* Layer header */}
            <div className="flex items-center gap-2 mt-2 mb-0.5">
              <div
                className="w-1.5 h-1.5 rounded-full"
                style={{ backgroundColor: layerColor }}
              />
              <span className="text-[10px] text-text-tertiary uppercase tracking-wider">
                {layer.code} — {layer.name}
              </span>
              <span
                className="text-[8px] mono px-1 py-0.5 rounded"
                style={{
                  backgroundColor: layerColor + '15',
                  color: layerColor,
                }}
              >
                {scopeLabel}
              </span>
            </div>

            {/* Per-dimension traces */}
            {layer.traces.map((dim) => {
              const isSource = sourceDimNames.has(dim.name)
              const color = isSource ? layerColor : layerColor + '80'

              return (
                <div
                  key={dim.index}
                  className="border-b border-white/[0.03]"
                  style={isSource ? { borderLeftWidth: 2, borderLeftColor: layerColor } : undefined}
                >
                  <MiniTrace
                    traceData={dim.data}
                    label={dim.name}
                    color={color}
                    cursorFrame={cursorFrame}
                    totalFrames={totalFrames}
                  />
                </div>
              )
            })}
          </div>
        )
      })}
    </div>
  )
}
