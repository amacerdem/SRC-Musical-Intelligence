import { useBeliefDecomposition } from '../../hooks/useBeliefDecomposition'
import { MiniTrace } from '../charts/MiniTrace'
import {
  BELIEF_HORIZON_ATLAS,
  HORIZON_COLORS,
  HORIZON_LABELS,
  LAW_DECOMP_COLORS,
  LAW_DECOMP_LABELS,
} from '../../data/beliefHorizonAtlas'

interface HorizonDecompositionPanelProps {
  beliefIndex: number
  beliefName: string
  experimentId: string | null
  cursorFrame?: number
  totalFrames?: number
}

const LAW_KEYS = [0, 1, 2] as const

export function HorizonDecompositionPanel({
  beliefIndex,
  beliefName,
  experimentId,
  cursorFrame,
  totalFrames,
}: HorizonDecompositionPanelProps) {
  const atlas = BELIEF_HORIZON_ATLAS[beliefIndex] ?? null
  const { data, loading, error } = useBeliefDecomposition(beliefName, experimentId, true)

  if (!atlas) return null

  // Collect all unique horizons
  const allHorizons: number[] = []
  for (const b of atlas.bands) {
    for (const h of b.horizons) {
      if (!allHorizons.includes(h)) allHorizons.push(h)
    }
  }
  allHorizons.sort((a, b) => a - b)

  return (
    <div className="space-y-1">
      {/* Header */}
      <div className="flex items-center justify-between mb-1">
        <div className="text-[10px] text-text-tertiary uppercase tracking-wider">
          {allHorizons.length} Horizons
        </div>
        <div className="text-[10px] text-text-tertiary mono">
          {atlas.totalDemands} tuples
          {loading && <span className="text-blue-400 animate-pulse ml-2">loading...</span>}
        </div>
      </div>

      {error && !loading && (
        <div className="text-[10px] text-text-tertiary/60 py-1">{error}</div>
      )}

      {/* Per-horizon charts — stacked vertically */}
      {allHorizons.map((h) => {
        const traceData = data?.traces.get(`h${h}`)
        const color = HORIZON_COLORS[h] ?? '#888'
        const label = HORIZON_LABELS[h] ?? `H${h}`

        if (!traceData) {
          return (
            <div
              key={h}
              className="flex items-center h-[56px] border-b border-white/[0.03]"
            >
              <span className="text-[10px] mono ml-1" style={{ color, opacity: 0.5 }}>
                {label}
              </span>
              {!loading && (
                <span className="text-[9px] text-text-tertiary/30 ml-3">no data</span>
              )}
            </div>
          )
        }

        return (
          <div key={h} className="border-b border-white/[0.03]">
            <MiniTrace
              traceData={traceData}
              label={label}
              color={color}
              cursorFrame={cursorFrame}
              totalFrames={totalFrames}
            />
          </div>
        )
      })}

      {/* Law decomposition — also stacked */}
      <div className="flex items-center justify-between mt-2 mb-1">
        <div className="text-[10px] text-text-tertiary uppercase tracking-wider">
          Laws
        </div>
      </div>

      {LAW_KEYS.map((law) => {
        const traceData = data?.traces.get(`law_${law}`)
        const hasLaw = atlas.laws.some((l) => l.law === law)
        if (!hasLaw) return null

        const color = LAW_DECOMP_COLORS[law]
        const label = LAW_DECOMP_LABELS[law]
        const count = atlas.laws.find((l) => l.law === law)?.tupleCount ?? 0

        if (!traceData) {
          return (
            <div
              key={law}
              className="flex items-center h-[56px] border-b border-white/[0.03]"
            >
              <span className="text-[10px] mono ml-1" style={{ color, opacity: 0.5 }}>
                {label} ({count})
              </span>
            </div>
          )
        }

        return (
          <div key={law} className="border-b border-white/[0.03]">
            <MiniTrace
              traceData={traceData}
              label={`${label} (${count})`}
              color={color}
              cursorFrame={cursorFrame}
              totalFrames={totalFrames}
            />
          </div>
        )
      })}
    </div>
  )
}
