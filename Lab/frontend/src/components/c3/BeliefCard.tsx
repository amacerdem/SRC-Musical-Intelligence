import { useState, useMemo } from 'react'
import type { BeliefDef } from '../../data/beliefs'
import { GlassBadge } from '../glass/GlassBadge'
import { GlassChip } from '../glass/GlassChip'
import { SparkLine } from '../charts/SparkLine'
import { BeliefTrace } from '../charts/BeliefTrace'
import { extractBeliefTrace } from '../../hooks/useBeliefData'
import { ChevronDown, ChevronRight } from 'lucide-react'

interface BeliefCardProps {
  belief: BeliefDef
  data: Float32Array | null
  color?: string
}

export function BeliefCard({ belief, data, color }: BeliefCardProps) {
  const [expanded, setExpanded] = useState(false)

  const trace = useMemo(
    () => (data ? extractBeliefTrace(data, belief.index) : []),
    [data, belief.index],
  )

  const hasData = trace.length > 0

  return (
    <div
      className={`glass-card cursor-pointer ${expanded ? 'ring-1 ring-white/8' : ''}`}
      onClick={() => setExpanded((e) => !e)}
    >
      {/* Collapsed view */}
      <div className="flex items-center gap-3 px-4 py-3">
        <span className="text-text-tertiary shrink-0">
          {expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
        </span>
        <span className="mono text-[11px] text-text-tertiary w-6 shrink-0 text-right">
          {belief.index}
        </span>
        <GlassBadge type={belief.type} showLabel={false} />
        <span className="text-sm text-text-primary truncate flex-1">
          {belief.name}
        </span>
        <GlassChip label={belief.mechanism} color={color} />
        {hasData && (
          <SparkLine
            data={trace}
            width={60}
            height={20}
            color={color ?? 'rgba(255,255,255,0.4)'}
          />
        )}
        {belief.tau !== null && (
          <span className="mono text-[10px] text-text-tertiary">\u03c4={belief.tau}</span>
        )}
      </div>

      {/* Expanded view */}
      {expanded && (
        <div className="border-t border-border-subtle px-4 py-3 space-y-3" onClick={(e) => e.stopPropagation()}>
          {/* Full belief trace */}
          <BeliefTrace
            data={trace}
            name={belief.name}
            type={belief.type}
            color={color}
            baseline={belief.baseline}
            height={140}
          />

          {/* Core belief params */}
          {belief.type === 'core' && belief.tau !== null && (
            <div className="flex gap-4 text-xs">
              <span className="text-text-secondary">
                \u03c4 = <span className="mono text-core">{belief.tau}</span>
              </span>
              <span className="text-text-secondary">
                \u03b2\u2080 = <span className="mono text-core">{belief.baseline}</span>
              </span>
              <span className="text-text-secondary">
                type: <span className="text-core">Bayesian PE update</span>
              </span>
            </div>
          )}

          {/* Source dims */}
          <div>
            <div className="text-[10px] text-text-tertiary uppercase tracking-wider mb-1">Source Dimensions</div>
            <div className="space-y-1">
              {belief.sourceDims.map((sd, i) => (
                <div key={i} className="flex items-center gap-2">
                  <span className="mono text-xs text-text-secondary flex-1">{sd.name}</span>
                  <div className="w-24 h-1.5 rounded-full bg-white/5 overflow-hidden">
                    <div
                      className="h-full rounded-full"
                      style={{
                        width: `${sd.weight * 100}%`,
                        backgroundColor: color ?? '#60a5fa',
                        opacity: 0.6,
                      }}
                    />
                  </div>
                  <span className="mono text-[10px] text-text-tertiary w-8 text-right">
                    {sd.weight.toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
