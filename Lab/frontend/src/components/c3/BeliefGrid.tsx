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

type GroupBy = 'index' | 'type' | 'mechanism'

export function BeliefGrid({ beliefs, data, color, counts }: BeliefGridProps) {
  const [filter, setFilter] = useState<BeliefType | 'all'>('all')
  const [groupBy, setGroupBy] = useState<GroupBy>('index')

  const filtered = useMemo(
    () => filter === 'all' ? beliefs : beliefs.filter((b) => b.type === filter),
    [beliefs, filter],
  )

  const sorted = useMemo(
    () => [...filtered].sort((a, b) => a.index - b.index),
    [filtered],
  )

  const grouped = useMemo(() => {
    if (groupBy === 'index') return null
    const source = sorted
    if (groupBy === 'mechanism') {
      const groups: Record<string, BeliefDef[]> = {}
      for (const b of source) {
        if (!groups[b.mechanism]) groups[b.mechanism] = []
        groups[b.mechanism].push(b)
      }
      return groups
    }
    const groups: Record<string, BeliefDef[]> = {}
    for (const b of source) {
      if (!groups[b.type]) groups[b.type] = []
      groups[b.type].push(b)
    }
    return groups
  }, [sorted, groupBy])

  return (
    <div className="space-y-4">
      {/* Filter + Group controls */}
      <div className="flex items-center justify-between gap-4">
        <BeliefTypeFilter active={filter} onChange={setFilter} counts={counts} />
        <div className="flex gap-1 text-[11px]">
          {(['index', 'mechanism', 'type'] as GroupBy[]).map((g) => (
            <button
              key={g}
              onClick={() => setGroupBy(g)}
              className={`px-2 py-1 rounded ${groupBy === g ? 'bg-white/8 text-text-primary' : 'text-text-tertiary hover:text-text-secondary'}`}
            >
              by {g}
            </button>
          ))}
        </div>
      </div>

      {/* Belief cards */}
      {grouped ? (
        Object.entries(grouped).map(([group, groupBeliefs]) => (
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
        ))
      ) : (
        <div className="space-y-1.5">
          {sorted.map((b) => (
            <BeliefCard key={b.index} belief={b} data={data} color={color} />
          ))}
        </div>
      )}

      {sorted.length === 0 && (
        <div className="text-center text-sm text-text-tertiary py-8">No beliefs match filter</div>
      )}
    </div>
  )
}
