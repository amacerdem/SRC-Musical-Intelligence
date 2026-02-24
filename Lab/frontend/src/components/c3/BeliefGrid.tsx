import { useState, useMemo } from 'react'
import type { BeliefDef, BeliefType } from '../../data/beliefs'
import { BeliefTypeFilter } from './BeliefTypeFilter'
import { BeliefCard } from './BeliefCard'

interface BeliefGridProps {
  beliefs: BeliefDef[]
  data: Float32Array | null
  color?: string
  counts: { core: number; appraisal: number; anticipation: number; total: number }
}

type GroupBy = 'type' | 'mechanism'

export function BeliefGrid({ beliefs, data, color, counts }: BeliefGridProps) {
  const [filter, setFilter] = useState<BeliefType | 'all'>('all')
  const [groupBy, setGroupBy] = useState<GroupBy>('mechanism')

  const filtered = useMemo(
    () => filter === 'all' ? beliefs : beliefs.filter((b) => b.type === filter),
    [beliefs, filter],
  )

  const grouped = useMemo(() => {
    if (groupBy === 'mechanism') {
      const groups: Record<string, BeliefDef[]> = {}
      for (const b of filtered) {
        if (!groups[b.mechanism]) groups[b.mechanism] = []
        groups[b.mechanism].push(b)
      }
      return groups
    }
    const groups: Record<string, BeliefDef[]> = {}
    for (const b of filtered) {
      if (!groups[b.type]) groups[b.type] = []
      groups[b.type].push(b)
    }
    return groups
  }, [filtered, groupBy])

  return (
    <div className="space-y-4">
      {/* Filter + Group controls */}
      <div className="flex items-center justify-between gap-4">
        <BeliefTypeFilter active={filter} onChange={setFilter} counts={counts} />
        <div className="flex gap-1 text-[11px]">
          <button
            onClick={() => setGroupBy('mechanism')}
            className={`px-2 py-1 rounded ${groupBy === 'mechanism' ? 'bg-white/8 text-text-primary' : 'text-text-tertiary hover:text-text-secondary'}`}
          >
            by mechanism
          </button>
          <button
            onClick={() => setGroupBy('type')}
            className={`px-2 py-1 rounded ${groupBy === 'type' ? 'bg-white/8 text-text-primary' : 'text-text-tertiary hover:text-text-secondary'}`}
          >
            by type
          </button>
        </div>
      </div>

      {/* Grouped belief cards */}
      {Object.entries(grouped).map(([group, groupBeliefs]) => (
        <div key={group}>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
              {group}
            </span>
            <span className="mono text-[10px] text-text-tertiary">{groupBeliefs.length}</span>
          </div>
          <div className="space-y-1.5">
            {groupBeliefs.map((b) => (
              <BeliefCard key={b.index} belief={b} data={data} color={color} />
            ))}
          </div>
        </div>
      ))}

      {filtered.length === 0 && (
        <div className="text-center text-sm text-text-tertiary py-8">No beliefs match filter</div>
      )}
    </div>
  )
}
