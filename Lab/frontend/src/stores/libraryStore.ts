import { create } from 'zustand'

export interface MidiSegment {
  start: number
  end: number
  type: string
  pitches: number[]
  label: string
  detail: string
}

export interface MidiEvents {
  displayName: string
  description: string
  duration_s: number
  instrument: string
  segments: MidiSegment[]
  expectedBehavior: string
  relatedBeliefs: string[]
}

export interface AudioLibraryItem {
  name: string
  filename: string
  category: 'music' | 'midi_test'
  relay: string | null
  displayName: string
  description: string
  format: string
  duration_s: number | null
  available: boolean
  relatedBeliefs: string[]
}

interface LibraryState {
  items: AudioLibraryItem[]
  loading: boolean
  midiCache: Map<string, MidiEvents>
  fetchLibrary: () => Promise<void>
  fetchMidiEvents: (name: string) => Promise<MidiEvents | null>
  getRecommendedForBelief: (beliefName: string) => AudioLibraryItem[]
  getMusicItems: () => AudioLibraryItem[]
  getMidiItems: (relay?: string) => AudioLibraryItem[]
  getRelays: () => string[]
}

export const useLibraryStore = create<LibraryState>((set, get) => ({
  items: [],
  loading: false,
  midiCache: new Map(),

  fetchLibrary: async () => {
    set({ loading: true })
    try {
      const res = await fetch('/api/audio/list')
      const items: AudioLibraryItem[] = await res.json()
      set({ items, loading: false })
    } catch {
      set({ loading: false })
    }
  },

  fetchMidiEvents: async (name: string) => {
    const cached = get().midiCache.get(name)
    if (cached) return cached

    try {
      const res = await fetch(`/api/audio/midi-events/${name}`)
      if (!res.ok) return null
      const data: MidiEvents = await res.json()
      set((s) => {
        const next = new Map(s.midiCache)
        next.set(name, data)
        return { midiCache: next }
      })
      return data
    } catch {
      return null
    }
  },

  getRecommendedForBelief: (beliefName: string) => {
    return get().items.filter(
      (item) => item.relatedBeliefs?.includes(beliefName),
    )
  },

  getMusicItems: () => {
    return get().items.filter((item) => item.category === 'music')
  },

  getMidiItems: (relay?: string) => {
    const midi = get().items.filter((item) => item.category === 'midi_test')
    if (relay) return midi.filter((item) => item.relay === relay)
    return midi
  },

  getRelays: () => {
    const relays = new Set<string>()
    for (const item of get().items) {
      if (item.relay) relays.add(item.relay)
    }
    return Array.from(relays).sort()
  },
}))
