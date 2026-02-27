import { useState, useEffect, useCallback } from 'react'

export interface DecompositionData {
  variants: string[]
  traces: Map<string, number[]>
  nFrames: number
}

/**
 * Lazy-load belief horizon decomposition data (per-band and per-law traces).
 * Only fetches when `autoLoad` is true (i.e., when the Horizons tab is active).
 */
export function useBeliefDecomposition(
  beliefName: string,
  experimentId: string | null,
  autoLoad: boolean = false,
): { data: DecompositionData | null; loading: boolean; error: string | null } {
  const [data, setData] = useState<DecompositionData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    if (!experimentId || !beliefName) return
    setLoading(true)
    setError(null)

    try {
      const res = await fetch(
        `/api/c3/beliefs/${encodeURIComponent(beliefName)}/decomposition?experiment=${experimentId}`,
      )

      if (!res.ok) {
        if (res.status === 404) {
          setData(null)
          setError('No decomposition data available')
        } else {
          setError(`Failed to load decomposition: ${res.status}`)
        }
        setLoading(false)
        return
      }

      const variantsHeader = res.headers.get('X-Decomposition-Variants') ?? ''
      const framesHeader = res.headers.get('X-Decomposition-Frames') ?? '0'
      const variants = variantsHeader.split(',').filter(Boolean)
      const nFrames = parseInt(framesHeader, 10)

      const buf = await res.arrayBuffer()
      const raw = new Float32Array(buf)
      const nVariants = variants.length

      // Data is (T × N_variants) column-major
      const traces = new Map<string, number[]>()
      for (let vi = 0; vi < nVariants; vi++) {
        const trace: number[] = new Array(nFrames)
        for (let t = 0; t < nFrames; t++) {
          trace[t] = raw[t * nVariants + vi]
        }
        traces.set(variants[vi], trace)
      }

      setData({ variants, traces, nFrames })
    } catch (err) {
      setError(`Network error: ${err}`)
    } finally {
      setLoading(false)
    }
  }, [beliefName, experimentId])

  useEffect(() => {
    if (autoLoad && experimentId) {
      load()
    }
  }, [autoLoad, experimentId, load])

  return { data, loading, error }
}
