import { useMemo } from 'react'
import { BELIEFS, type BeliefDef, type BeliefType } from '../data/beliefs'
import { useC3Store } from '../stores/c3Store'

export interface BeliefDataResult {
  beliefs: BeliefDef[]
  data: Float32Array | null
  nFrames: number
  loading: boolean
  byType: Record<BeliefType, BeliefDef[]>
  byMechanism: Record<string, BeliefDef[]>
}

export function useBeliefData(functionId: string): BeliefDataResult {
  const { beliefsData, nFrames, beliefsLoading } = useC3Store()

  const beliefs = useMemo(
    () => BELIEFS.filter((b) => b.functionId === functionId),
    [functionId],
  )

  const byType = useMemo(() => {
    const result: Record<BeliefType, BeliefDef[]> = { core: [], appraisal: [], anticipation: [] }
    for (const b of beliefs) result[b.type].push(b)
    return result
  }, [beliefs])

  const byMechanism = useMemo(() => {
    const result: Record<string, BeliefDef[]> = {}
    for (const b of beliefs) {
      if (!result[b.mechanism]) result[b.mechanism] = []
      result[b.mechanism].push(b)
    }
    return result
  }, [beliefs])

  return {
    beliefs,
    data: beliefsData,
    nFrames,
    loading: beliefsLoading,
    byType,
    byMechanism,
  }
}

/** Extract a single belief's time series from the bulk T×131 array */
export function extractBeliefTrace(data: Float32Array, beliefIndex: number, nBeliefs: number = 131): number[] {
  const nFrames = data.length / nBeliefs
  const trace: number[] = new Array(nFrames)
  for (let t = 0; t < nFrames; t++) {
    trace[t] = data[t * nBeliefs + beliefIndex]
  }
  return trace
}
