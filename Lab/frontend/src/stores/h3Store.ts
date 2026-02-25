import { create } from 'zustand'

function tupleKey(t: [number, number, number, number]): string {
  return `${t[0]},${t[1]},${t[2]},${t[3]}`
}

interface H3State {
  /** H3 tuple registry: (N x 4) loaded once per experiment */
  tupleRegistry: Int32Array | null
  nTuples: number
  nFrames: number

  /** Cached time-series keyed by "r3,h,m,l" */
  tupleCache: Map<string, Float32Array>

  loading: boolean

  /** Load just the tuple addresses (N x 4 Int32) */
  loadRegistry: (experimentId: string) => Promise<void>

  /** Load specific tuple data by 4-tuple keys */
  loadTuples: (experimentId: string, keys: [number, number, number, number][]) => Promise<void>

  /** Find a tuple's row index in the registry */
  findTupleIndex: (key: [number, number, number, number]) => number

  /** Get cached data for a tuple */
  getTupleData: (key: [number, number, number, number]) => Float32Array | null

  clear: () => void
}

export const useH3Store = create<H3State>((set, get) => ({
  tupleRegistry: null,
  nTuples: 0,
  nFrames: 0,
  tupleCache: new Map(),
  loading: false,

  loadRegistry: async (experimentId: string) => {
    set({ loading: true })
    try {
      const res = await fetch(`/api/pipeline/results/${experimentId}/h3/registry`)
      if (!res.ok) throw new Error(`H3 registry: ${res.status}`)
      const count = parseInt(res.headers.get('X-H3-Count') ?? '0', 10)
      const buf = await res.arrayBuffer()
      set({
        tupleRegistry: new Int32Array(buf),
        nTuples: count,
        loading: false,
      })
    } catch {
      set({ tupleRegistry: null, nTuples: 0, loading: false })
    }
  },

  loadTuples: async (experimentId: string, keys: [number, number, number, number][]) => {
    const state = get()
    if (!state.tupleRegistry) return

    // Filter out already cached keys
    const needed = keys.filter((k) => !state.tupleCache.has(tupleKey(k)))
    if (needed.length === 0) return

    // Resolve 4-tuple keys to row indices
    const indices: number[] = []
    const resolvedKeys: string[] = []
    for (const key of needed) {
      const idx = state.findTupleIndex(key)
      if (idx >= 0) {
        indices.push(idx)
        resolvedKeys.push(tupleKey(key))
      }
    }
    if (indices.length === 0) return

    set({ loading: true })
    try {
      const res = await fetch(
        `/api/pipeline/results/${experimentId}/h3/select?indices=${indices.join(',')}`,
      )
      if (!res.ok) throw new Error(`H3 select: ${res.status}`)

      const nFrames = parseInt(res.headers.get('X-H3-Frames') ?? '0', 10)
      const buf = await res.arrayBuffer()
      const allData = new Float32Array(buf)

      // Split into per-tuple arrays and cache
      const newCache = new Map(state.tupleCache)
      for (let i = 0; i < resolvedKeys.length; i++) {
        const start = i * nFrames
        const tupleData = allData.slice(start, start + nFrames)
        newCache.set(resolvedKeys[i], tupleData)
      }

      set({ tupleCache: newCache, nFrames, loading: false })
    } catch {
      set({ loading: false })
    }
  },

  findTupleIndex: (key: [number, number, number, number]): number => {
    const reg = get().tupleRegistry
    if (!reg) return -1
    const n = get().nTuples
    for (let i = 0; i < n; i++) {
      const base = i * 4
      if (
        reg[base] === key[0] &&
        reg[base + 1] === key[1] &&
        reg[base + 2] === key[2] &&
        reg[base + 3] === key[3]
      ) {
        return i
      }
    }
    return -1
  },

  getTupleData: (key: [number, number, number, number]): Float32Array | null => {
    return get().tupleCache.get(tupleKey(key)) ?? null
  },

  clear: () => {
    set({
      tupleRegistry: null,
      nTuples: 0,
      nFrames: 0,
      tupleCache: new Map(),
      loading: false,
    })
  },
}))
