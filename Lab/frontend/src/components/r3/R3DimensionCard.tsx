import { useState, useMemo } from 'react'
import type { R3DimDef } from '../../data/r3'
import { SparkLine } from '../charts/SparkLine'
import { BeliefTrace } from '../charts/BeliefTrace'
import { extractR3Trace } from '../../stores/r3Store'
import { useAudioCursor } from '../../stores/audioStore'
import { ChevronDown, ChevronRight } from 'lucide-react'

interface R3DimensionCardProps {
  dim: R3DimDef
  data: Float32Array | null
  color?: string
}

export function R3DimensionCard({ dim, data, color }: R3DimensionCardProps) {
  const [expanded, setExpanded] = useState(false)
  const { currentFrame, totalFrames } = useAudioCursor()

  const trace = useMemo(
    () => (data ? extractR3Trace(data, dim.index) : []),
    [data, dim.index],
  )

  const hasData = trace.length > 0

  return (
    <div
      className={`glass-card cursor-pointer ${expanded ? 'ring-1 ring-white/8' : ''}`}
      onClick={() => setExpanded((e) => !e)}
    >
      {/* Collapsed view */}
      <div className="flex items-center gap-3 px-4 py-2.5">
        <span className="text-text-tertiary shrink-0">
          {expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
        </span>
        <span className="mono text-[11px] text-text-tertiary w-6 shrink-0 text-right">
          {dim.index}
        </span>
        <span className="text-sm text-text-primary truncate flex-1">
          {dim.name}
        </span>
        {hasData && (
          <SparkLine
            data={trace}
            width={80}
            height={20}
            color={color ?? 'rgba(255,255,255,0.4)'}
          />
        )}
        {!hasData && (
          <span className="text-[9px] text-text-tertiary italic">no data</span>
        )}
      </div>

      {/* Expanded view — signal trace */}
      {expanded && (
        <div className="border-t border-border-subtle px-4 py-3 space-y-2" onClick={(e) => e.stopPropagation()}>
          <div className="text-[10px] text-text-tertiary uppercase tracking-wider">
            Signal — {dim.name} [R³ idx {dim.index}]
          </div>
          {hasData ? (
            <BeliefTrace
              data={trace}
              name={dim.name}
              type="appraisal"
              color={color}
              height={120}
              cursorFrame={currentFrame}
              totalFrames={totalFrames}
            />
          ) : (
            <div className="glass-card p-6 text-center text-text-tertiary text-sm">
              Run a pipeline analysis to see R³ feature data.
            </div>
          )}
        </div>
      )}
    </div>
  )
}
