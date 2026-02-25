import { useState } from 'react'
import { BELIEF_H3_MAP, MECHANISM_H3_COUNTS, LAW_COLORS } from '../../data/h3Demands'
import { useH3Data } from '../../hooks/useH3Data'
import { H3TupleRow } from './H3TupleRow'
import { ChevronRight, ChevronDown, Layers } from 'lucide-react'

interface H3TemporalPanelProps {
  beliefIndex: number
  mechanismName: string
  experimentId: string | null
  color?: string
  cursorFrame?: number
  totalFrames?: number
}

function tupleKey(t: { r3Idx: number; horizon: number; morph: number; law: number }): string {
  return `${t.r3Idx},${t.horizon},${t.morph},${t.law}`
}

export function H3TemporalPanel({
  beliefIndex,
  mechanismName,
  experimentId,
  color,
  cursorFrame,
  totalFrames,
}: H3TemporalPanelProps) {
  const demands = BELIEF_H3_MAP[beliefIndex] ?? null
  const [mechExpanded, setMechExpanded] = useState(false)

  // Load predict tuple data (autoLoad=true since panel is shown when card is expanded)
  const { traces, loading } = useH3Data(beliefIndex, experimentId, true)

  const predictCount = demands?.predict.length ?? 0
  const mechCount = demands?.mechanismDemandCount ?? MECHANISM_H3_COUNTS[mechanismName] ?? 0
  const mechLabel = demands?.mechanismName ?? mechanismName

  return (
    <div className="space-y-2">
      {/* Section header */}
      <div className="flex items-center justify-between">
        <div className="text-[10px] text-text-tertiary uppercase tracking-wider flex items-center gap-1.5">
          <Layers size={10} className="opacity-60" />
          H³ Temporal Inputs
        </div>
        <div className="flex items-center gap-2 text-[10px] text-text-tertiary mono">
          {predictCount > 0 && (
            <span>{predictCount} predict</span>
          )}
          {mechCount > 0 && (
            <span>{mechCount} mechanism</span>
          )}
          {loading && (
            <span className="text-blue-400 animate-pulse">loading...</span>
          )}
        </div>
      </div>

      {/* Law legend */}
      <div className="flex items-center gap-3 text-[10px]">
        {Object.entries(LAW_COLORS).map(([name, col]) => (
          <span key={name} className="flex items-center gap-1 text-text-tertiary">
            <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: col }} />
            {name}
          </span>
        ))}
      </div>

      {/* Predict tuples — visible for CoreBeliefs with predict entries */}
      {predictCount > 0 && demands && (
        <div className="space-y-1.5">
          <div className="text-[10px] text-text-secondary font-medium ml-0.5">
            Prediction References
          </div>
          {demands.predict.map((tuple) => {
            const key = tupleKey(tuple)
            return (
              <H3TupleRow
                key={key}
                meta={tuple}
                data={traces.get(key) ?? null}
                color={color}
                cursorFrame={cursorFrame}
                totalFrames={totalFrames}
              />
            )
          })}
        </div>
      )}

      {/* Mechanism demands — collapsible */}
      {mechCount > 0 && (
        <div>
          <button
            onClick={() => setMechExpanded((e) => !e)}
            className="flex items-center gap-1.5 text-[10px] text-text-tertiary hover:text-text-secondary transition-colors py-1"
          >
            {mechExpanded ? <ChevronDown size={10} /> : <ChevronRight size={10} />}
            <span className="uppercase tracking-wider">{mechLabel} Mechanism Demands</span>
            <span className="mono text-text-tertiary/60">({mechCount} tuples)</span>
          </button>
          {mechExpanded && (
            <div className="mt-1 px-2 py-2 rounded-lg bg-white/[0.02] border border-white/5 text-[10px] text-text-tertiary">
              Mechanism H³ demands are computed within the {mechLabel} pipeline.
              <span className="block mt-1 mono">
                {mechCount} tuples across memory / forward / integration laws
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
