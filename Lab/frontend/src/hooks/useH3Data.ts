import { useEffect, useMemo } from 'react'
import { BELIEF_H3_MAP, type BeliefH3Demands, type H3TupleMeta } from '../data/h3Demands'
import { useH3Store } from '../stores/h3Store'

interface H3DataResult {
  demands: BeliefH3Demands | null
  traces: Map<string, Float32Array>
  loading: boolean
}

function tupleKey(t: H3TupleMeta): string {
  return `${t.r3Idx},${t.horizon},${t.morph},${t.law}`
}

/**
 * Hook: loads H3 tuple data for a specific belief.
 * Only fetches when autoLoad is true (i.e., card is expanded).
 */
export function useH3Data(
  beliefIndex: number,
  experimentId: string | null,
  autoLoad: boolean,
): H3DataResult {
  const demands = BELIEF_H3_MAP[beliefIndex] ?? null
  const loading = useH3Store((s) => s.loading)
  const tupleCache = useH3Store((s) => s.tupleCache)
  const registry = useH3Store((s) => s.tupleRegistry)
  const loadTuples = useH3Store((s) => s.loadTuples)

  // Auto-load predict tuples when card expands
  useEffect(() => {
    if (!autoLoad || !experimentId || !demands || !registry) return
    const keys = demands.predict.map(
      (t) => [t.r3Idx, t.horizon, t.morph, t.law] as [number, number, number, number],
    )
    if (keys.length > 0) {
      loadTuples(experimentId, keys)
    }
  }, [autoLoad, experimentId, demands, registry, loadTuples])

  // Extract matching traces from cache
  const traces = useMemo(() => {
    const result = new Map<string, Float32Array>()
    if (!demands) return result
    for (const t of demands.predict) {
      const key = tupleKey(t)
      const data = tupleCache.get(key)
      if (data) result.set(key, data)
    }
    return result
  }, [demands, tupleCache])

  return { demands, traces, loading }
}
