import { create } from 'zustand'

export interface LayerMeta {
  code: string
  name: string
  start: number
  end: number
  scope: string
}

export interface MechanismMeta {
  fullName: string
  function: string
  unit: string
  outputDim: number
  dimensions: string[]
  layers: LayerMeta[]
}

export type MechanismMetaMap = Record<string, MechanismMeta>

interface C3State {
  beliefsData: Float32Array | null
  nBeliefs: number
  nFrames: number
  beliefsLoading: boolean
  relayCache: Record<string, { data: Float32Array; dim: number }>
  relayLoading: Record<string, boolean>
  mechanismMeta: MechanismMetaMap | null
  mechanismMetaLoading: boolean
  loadBeliefs: (experimentId: string) => Promise<void>
  loadRelay: (experimentId: string, relayName: string) => Promise<void>
  loadMechanismMeta: () => Promise<void>
  clear: () => void
}

export const useC3Store = create<C3State>((set, get) => ({
  beliefsData: null,
  nBeliefs: 131,
  nFrames: 0,
  beliefsLoading: false,
  relayCache: {},
  relayLoading: {},
  mechanismMeta: null,
  mechanismMetaLoading: false,

  loadBeliefs: async (experimentId: string) => {
    set({ beliefsLoading: true })
    try {
      const res = await fetch(`/api/c3/beliefs?experiment=${experimentId}`)
      const buf = await res.arrayBuffer()
      const data = new Float32Array(buf)
      const nBeliefs = 131
      const nFrames = data.length / nBeliefs
      set({ beliefsData: data, nBeliefs, nFrames, beliefsLoading: false })
    } catch {
      set({ beliefsLoading: false })
    }
  },

  loadRelay: async (experimentId: string, relayName: string) => {
    const { relayCache, relayLoading } = get()
    if (relayCache[relayName] || relayLoading[relayName]) return

    set({ relayLoading: { ...get().relayLoading, [relayName]: true } })
    try {
      const res = await fetch(`/api/c3/relays/${relayName}?experiment=${experimentId}`)
      const dimHeader = parseInt(res.headers.get('X-Relay-Dim') ?? '0', 10)
      const buf = await res.arrayBuffer()
      const data = new Float32Array(buf)
      const dim = dimHeader || 1
      set({
        relayCache: { ...get().relayCache, [relayName]: { data, dim } },
        relayLoading: { ...get().relayLoading, [relayName]: false },
      })
    } catch {
      set({ relayLoading: { ...get().relayLoading, [relayName]: false } })
    }
  },

  loadMechanismMeta: async () => {
    if (get().mechanismMeta || get().mechanismMetaLoading) return
    set({ mechanismMetaLoading: true })
    try {
      const res = await fetch('/api/c3/mechanism-meta')
      const data: MechanismMetaMap = await res.json()
      set({ mechanismMeta: data, mechanismMetaLoading: false })
    } catch {
      set({ mechanismMetaLoading: false })
    }
  },

  clear: () => set({
    beliefsData: null,
    nFrames: 0,
    beliefsLoading: false,
    relayCache: {},
    relayLoading: {},
  }),
}))
