import { useState } from 'react'
import type { MechanismDef } from '../../data/mechanisms'
import type { BeliefDef } from '../../data/beliefs'
import { GlassBadge } from '../glass/GlassBadge'
import { GlassChip } from '../glass/GlassChip'
import { MechanismLayerChart } from '../charts/MechanismLayerChart'
import { ChevronDown, ChevronRight } from 'lucide-react'

interface MechanismCardProps {
  mechanism: MechanismDef
  linkedBeliefs: BeliefDef[]
  color?: string
}

const DEPTH_LABELS = ['Relay', 'Encoder', 'Associator', 'Integrator', 'Hub', 'Hub'] as const

export function MechanismCard({ mechanism, linkedBeliefs, color }: MechanismCardProps) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div
      className={`glass-card cursor-pointer ${expanded ? 'ring-1 ring-white/8' : ''}`}
      onClick={() => setExpanded((e) => !e)}
    >
      {/* Collapsed header */}
      <div className="flex items-center gap-3 px-4 py-3">
        <span className="text-text-tertiary shrink-0">
          {expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
        </span>
        <span
          className="mono text-sm font-semibold"
          style={{ color: color ?? '#fff' }}
        >
          {mechanism.name}
        </span>
        <GlassChip label={DEPTH_LABELS[mechanism.depth]} />
        <span className="mono text-[11px] text-text-tertiary">D{mechanism.depth}</span>
        <span className="flex-1" />
        <span className="mono text-xs text-text-secondary">{mechanism.outputDim}D</span>
        <span className="mono text-[10px] text-text-tertiary">{linkedBeliefs.length} beliefs</span>
      </div>

      {/* Expanded detail */}
      {expanded && (
        <div className="border-t border-border-subtle px-4 py-3 space-y-3" onClick={(e) => e.stopPropagation()}>
          <div className="text-xs text-text-secondary">{mechanism.fullName}</div>

          {mechanism.unit !== '\u2014' && (
            <div className="text-xs text-text-tertiary">
              Unit: <span className="mono text-text-secondary">{mechanism.unit}</span>
            </div>
          )}

          {/* Layer chart - placeholder dims based on type */}
          <MechanismLayerChart
            layers={estimateLayers(mechanism)}
            totalDim={mechanism.outputDim}
          />

          {/* Linked beliefs */}
          <div>
            <div className="text-[10px] text-text-tertiary uppercase tracking-wider mb-1.5">
              Linked Beliefs
            </div>
            <div className="flex flex-wrap gap-1.5">
              {linkedBeliefs.map((b) => (
                <span key={b.index} className="flex items-center gap-1">
                  <GlassBadge type={b.type} showLabel={false} />
                  <span className="text-[11px] text-text-secondary">{b.name}</span>
                </span>
              ))}
              {linkedBeliefs.length === 0 && (
                <span className="text-[11px] text-text-tertiary italic">no direct beliefs</span>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

/** Estimate E/M/P/F layers from mechanism type and dim */
function estimateLayers(m: MechanismDef) {
  const d = m.outputDim
  if (m.type === 'relay') {
    // Most relays follow E/M/P/F pattern with roughly equal splits
    const e = Math.ceil(d * 0.3)
    const mLayer = Math.ceil(d * 0.25)
    const p = Math.ceil(d * 0.25)
    const f = d - e - mLayer - p
    return [
      { label: 'E', dim: e, color: '' },
      { label: 'M', dim: mLayer, color: '' },
      { label: 'P', dim: p, color: '' },
      { label: 'F', dim: Math.max(f, 1), color: '' },
    ]
  }
  // Non-relay: single block
  return [{ label: m.type.charAt(0).toUpperCase(), dim: d, color: '' }]
}
