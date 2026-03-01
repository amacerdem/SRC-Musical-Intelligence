import { useState } from 'react'
import type { R3GroupDef } from '../../data/r3'
import { R3_DIMS } from '../../data/r3'
import { R3DimensionCard } from './R3DimensionCard'
import { GlassChip } from '../glass/GlassChip'
import { ChevronDown, ChevronRight } from 'lucide-react'

const STAGE_COLORS: Record<number, string> = { 1: '#22c55e', 2: '#f59e0b' }

interface R3GroupPanelProps {
  group: R3GroupDef
  data: Float32Array | null
  defaultExpanded?: boolean
}

export function R3GroupPanel({ group, data, defaultExpanded = false }: R3GroupPanelProps) {
  const [expanded, setExpanded] = useState(defaultExpanded)

  const dims = R3_DIMS.filter((d) => d.group === group.id)

  return (
    <div className={`glass-card ${expanded ? 'ring-1 ring-white/8' : ''}`}>
      {/* Group header */}
      <div
        className="flex items-center gap-3 px-5 py-3 cursor-pointer"
        onClick={() => setExpanded((e) => !e)}
      >
        <span className="text-text-tertiary shrink-0">
          {expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
        </span>
        <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: group.color }} />
        <span className="mono text-sm font-semibold" style={{ color: group.color }}>
          {group.id}
        </span>
        <span className="text-sm text-text-primary">{group.name}</span>
        <GlassChip label={`${group.dim}D`} color={group.color} />
        <span className="mono text-[10px] text-text-tertiary">[{group.start}:{group.end})</span>
        <span className="flex-1" />
        {group.deps && (
          <span className="text-[10px] text-text-tertiary mr-2">
            dep: <span className="mono text-text-secondary">{group.deps}</span>
          </span>
        )}
        <span
          className="mono text-[10px] px-1.5 py-0.5 rounded"
          style={{
            color: STAGE_COLORS[group.stage],
            backgroundColor: `${STAGE_COLORS[group.stage]}15`,
          }}
        >
          S{group.stage}
        </span>
        <span className="text-[10px] text-text-tertiary">{group.domain}</span>
      </div>

      {/* Expanded — dimension cards */}
      {expanded && (
        <div className="border-t border-border-subtle px-4 py-3 space-y-1.5">
          {dims.map((dim) => (
            <R3DimensionCard
              key={dim.index}
              dim={dim}
              data={data}
              color={group.color}
            />
          ))}
        </div>
      )}
    </div>
  )
}
