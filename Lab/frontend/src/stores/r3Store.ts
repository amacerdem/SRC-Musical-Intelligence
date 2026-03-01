import { create } from 'zustand'

const R3_DIM = 97

interface R3State {
  r3Data: Float32Array | null
  nDims: number
  nFrames: number
  r3Loading: boolean
  loadR3: (experimentId: string) => Promise<void>
  clear: () => void
}

export const useR3Store = create<R3State>((set) => ({
  r3Data: null,
  nDims: R3_DIM,
  nFrames: 0,
  r3Loading: false,

  loadR3: async (experimentId: string) => {
    set({ r3Loading: true })
    try {
      const res = await fetch(`/api/pipeline/results/${experimentId}/r3`)
      const buf = await res.arrayBuffer()
      const data = new Float32Array(buf)
      const nFrames = data.length / R3_DIM
      set({ r3Data: data, nFrames, r3Loading: false })
    } catch {
      set({ r3Loading: false })
    }
  },

  clear: () => set({ r3Data: null, nFrames: 0, r3Loading: false }),
}))

/** Extract a single R³ dimension's time series from the bulk T×97 array */
export function extractR3Trace(data: Float32Array, dimIndex: number, nDims: number = R3_DIM): number[] {
  const nFrames = data.length / nDims
  const trace: number[] = new Array(nFrames)
  for (let t = 0; t < nFrames; t++) {
    trace[t] = data[t * nDims + dimIndex]
  }
  return trace
}
