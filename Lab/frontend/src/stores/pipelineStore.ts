import { create } from 'zustand'
import { useC3Store } from './c3Store'

interface AudioItem {
  name: string
  filename: string
  format: string
  duration_s: number | null
  available: boolean
}

interface ExperimentMeta {
  experiment_id: string
  audio_name: string
  duration_s: number
  n_frames: number
  fps: number
  timestamp: string
  kernel_version: string
}

interface PipelineStatus {
  status: 'running' | 'done' | 'error'
  phase: string
  progress: number
  fps: number
  audio_name?: string
  error?: string
}

interface PipelineState {
  // Audio catalog
  audioCatalog: AudioItem[]
  catalogLoading: boolean

  // Current pipeline run
  currentExperiment: string | null
  pipelineStatus: PipelineStatus | null
  runningExperiment: string | null

  // Experiment history
  experiments: ExperimentMeta[]
  experimentsLoading: boolean

  // Actions
  fetchCatalog: () => Promise<void>
  fetchExperiments: () => Promise<void>
  runPipeline: (audioName: string, excerptS?: number) => Promise<void>
  selectExperiment: (experimentId: string) => Promise<void>
}

let pollTimer: ReturnType<typeof setInterval> | null = null

export const usePipelineStore = create<PipelineState>((set, get) => ({
  audioCatalog: [],
  catalogLoading: false,
  currentExperiment: null,
  pipelineStatus: null,
  runningExperiment: null,
  experiments: [],
  experimentsLoading: false,

  fetchCatalog: async () => {
    set({ catalogLoading: true })
    try {
      const res = await fetch('/api/audio/list')
      const items: AudioItem[] = await res.json()
      set({ audioCatalog: items, catalogLoading: false })
    } catch {
      set({ catalogLoading: false })
    }
  },

  fetchExperiments: async () => {
    set({ experimentsLoading: true })
    try {
      const res = await fetch('/api/experiments/list')
      const list: ExperimentMeta[] = await res.json()
      set({ experiments: list, experimentsLoading: false })
    } catch {
      set({ experimentsLoading: false })
    }
  },

  runPipeline: async (audioName: string, excerptS?: number) => {
    const body: Record<string, unknown> = { audio_name: audioName }
    if (excerptS !== undefined) body.excerpt_s = excerptS

    try {
      const res = await fetch('/api/pipeline/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      const { experiment_id } = await res.json()
      set({
        runningExperiment: experiment_id,
        pipelineStatus: { status: 'running', phase: 'queued', progress: 0, fps: 0 },
      })

      // Start polling
      if (pollTimer) clearInterval(pollTimer)
      pollTimer = setInterval(async () => {
        try {
          const statusRes = await fetch(`/api/pipeline/status/${experiment_id}`)
          const status: PipelineStatus = await statusRes.json()
          set({ pipelineStatus: status })

          if (status.status === 'done' || status.status === 'error') {
            if (pollTimer) clearInterval(pollTimer)
            pollTimer = null
            set({ runningExperiment: null })

            if (status.status === 'done') {
              // Auto-select the completed experiment
              get().selectExperiment(experiment_id)
              get().fetchExperiments()
            }
          }
        } catch {
          // Ignore poll errors
        }
      }, 500)
    } catch {
      set({ pipelineStatus: { status: 'error', phase: 'error', progress: 0, fps: 0, error: 'Request failed' } })
    }
  },

  selectExperiment: async (experimentId: string) => {
    set({ currentExperiment: experimentId })
    // Auto-load beliefs into c3Store
    useC3Store.getState().clear()
    await useC3Store.getState().loadBeliefs(experimentId)
  },
}))
