import { create } from 'zustand'

/** MI pipeline frame rate */
const FRAME_RATE = 172.27

interface AudioState {
  /* ── Source ── */
  src: string | null
  fileName: string | null
  samples: Float32Array | null

  /* ── Playback ── */
  playing: boolean
  duration: number
  currentTime: number

  /* ── Derived ── */
  /** Current MI frame index at 172.27 Hz */
  currentFrame: number
  /** Total frames in the loaded audio */
  totalFrames: number

  /* ── Internal ── */
  _audio: HTMLAudioElement | null
  _raf: number

  /* ── Actions ── */
  loadAudio: (src: string, fileName?: string) => Promise<void>
  play: () => void
  pause: () => void
  togglePlay: () => void
  seek: (position: number) => void
  seekFrame: (frame: number) => void
  unload: () => void
}

export const useAudioStore = create<AudioState>((set, get) => ({
  src: null,
  fileName: null,
  samples: null,
  playing: false,
  duration: 0,
  currentTime: 0,
  currentFrame: 0,
  totalFrames: 0,
  _audio: null,
  _raf: 0,

  loadAudio: async (src, fileName) => {
    const prev = get()
    // Cleanup previous
    if (prev._audio) {
      prev._audio.pause()
      prev._audio.src = ''
      cancelAnimationFrame(prev._raf)
    }

    const audio = new Audio(src)
    audio.preload = 'auto'

    // Decode samples for waveform
    let samples: Float32Array | null = null
    try {
      const res = await fetch(src)
      const buf = await res.arrayBuffer()
      const actx = new AudioContext()
      const decoded = await actx.decodeAudioData(buf)
      samples = decoded.getChannelData(0)
      await actx.close()
    } catch {
      // Waveform unavailable, playback still works
    }

    const duration = await new Promise<number>((resolve) => {
      audio.addEventListener('loadedmetadata', () => resolve(audio.duration), { once: true })
      // Fallback if already loaded
      if (audio.duration) resolve(audio.duration)
    })

    audio.addEventListener('ended', () => {
      set({ playing: false })
    })

    set({
      src,
      fileName: fileName ?? src.split('/').pop() ?? 'audio',
      samples,
      _audio: audio,
      playing: false,
      duration,
      currentTime: 0,
      currentFrame: 0,
      totalFrames: Math.floor(duration * FRAME_RATE),
    })
  },

  play: () => {
    const { _audio } = get()
    if (!_audio) return
    _audio.play()
    set({ playing: true })

    // Start RAF tick
    const tick = () => {
      const audio = get()._audio
      if (audio && !audio.paused) {
        const t = audio.currentTime
        set({
          currentTime: t,
          currentFrame: Math.floor(t * FRAME_RATE),
        })
        set({ _raf: requestAnimationFrame(tick) })
      }
    }
    set({ _raf: requestAnimationFrame(tick) })
  },

  pause: () => {
    const { _audio, _raf } = get()
    if (_audio) _audio.pause()
    cancelAnimationFrame(_raf)
    set({ playing: false })
  },

  togglePlay: () => {
    const { playing, play, pause, _audio } = get()
    if (!_audio) return
    if (playing) pause()
    else play()
  },

  /** Seek by normalized position 0..1 */
  seek: (position) => {
    const { _audio, duration } = get()
    if (!_audio) return
    const t = Math.max(0, Math.min(1, position)) * duration
    _audio.currentTime = t
    set({
      currentTime: t,
      currentFrame: Math.floor(t * FRAME_RATE),
    })
  },

  /** Seek to a specific MI frame */
  seekFrame: (frame) => {
    const { _audio, totalFrames } = get()
    if (!_audio || totalFrames === 0) return
    const t = frame / FRAME_RATE
    _audio.currentTime = t
    set({
      currentTime: t,
      currentFrame: frame,
    })
  },

  unload: () => {
    const { _audio, _raf } = get()
    if (_audio) {
      _audio.pause()
      _audio.src = ''
    }
    cancelAnimationFrame(_raf)
    set({
      src: null,
      fileName: null,
      samples: null,
      playing: false,
      duration: 0,
      currentTime: 0,
      currentFrame: 0,
      totalFrames: 0,
      _audio: null,
      _raf: 0,
    })
  },
}))

/** Hook that returns just the cursor position (for re-render optimization) */
export function useAudioCursor() {
  return useAudioStore((s) => ({
    currentFrame: s.currentFrame,
    totalFrames: s.totalFrames,
    currentTime: s.currentTime,
    duration: s.duration,
    playing: s.playing,
  }))
}

/** Hook for samples only (stable reference) */
export function useAudioSamples() {
  return useAudioStore((s) => s.samples)
}
