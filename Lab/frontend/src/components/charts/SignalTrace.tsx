import { useRef, useEffect, useCallback } from 'react'

interface SignalTraceProps {
  /** Flat Float32Array of shape T×D (row-major) or number[][] */
  data: Float32Array | number[][]
  nChannels: number
  colors?: string[]
  labels?: string[]
  height?: number
  className?: string
  showGrid?: boolean
  /** Current playback frame for cursor sync */
  cursorFrame?: number
  /** Total frames in the data (for cursor position calculation) */
  totalFrames?: number
}

const DEFAULT_PALETTE = [
  '#3b82f6', '#8b5cf6', '#f97316', '#14b8a6', '#ec4899',
  '#f59e0b', '#22c55e', '#6366f1', '#06b6d4', '#ef4444',
  '#a855f7', '#10b981', '#f43f5e', '#84cc16', '#0ea5e9',
  '#d946ef',
]

/** Max display points for overview */
const MAX_POINTS = 600

export function SignalTrace({
  data,
  nChannels,
  colors,
  labels,
  height = 200,
  className = '',
  showGrid = true,
  cursorFrame,
  totalFrames,
}: SignalTraceProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const zoomRef = useRef({ start: 0, end: 1 })
  const panRef = useRef({ active: false, startX: 0, startZoom: { start: 0, end: 1 } })
  const drawRef = useRef<() => void>(() => {})

  // Determine nFrames and accessor
  const nFrames = data instanceof Float32Array ? data.length / nChannels : data.length
  const getValue = useCallback((t: number, ch: number) => {
    if (data instanceof Float32Array) return data[t * nChannels + ch]
    return data[t]?.[ch] ?? 0
  }, [data, nChannels])

  // Reset zoom on data change
  useEffect(() => {
    zoomRef.current = { start: 0, end: 1 }
  }, [nFrames])

  const draw = () => {
    const canvas = canvasRef.current
    const container = containerRef.current
    if (!canvas || !container) return

    const width = container.clientWidth
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const dpr = window.devicePixelRatio || 1
    canvas.width = width * dpr
    canvas.height = height * dpr
    ctx.scale(dpr, dpr)
    ctx.clearRect(0, 0, width, height)

    if (nFrames < 2) return

    const { start: zs, end: ze } = zoomRef.current
    const startIdx = Math.floor(zs * (nFrames - 1))
    const endIdx = Math.ceil(ze * (nFrames - 1))
    const viewLen = endIdx - startIdx + 1

    // Find global min/max on visible range
    let gMin = Infinity
    let gMax = -Infinity
    for (let ch = 0; ch < nChannels; ch++) {
      for (let t = startIdx; t <= endIdx; t++) {
        const v = getValue(t, ch)
        if (v < gMin) gMin = v
        if (v > gMax) gMax = v
      }
    }
    const range = gMax - gMin || 1
    const pad = { top: 8, bottom: 24, left: 0, right: 0 }
    const plotW = width - pad.left - pad.right
    const plotH = height - pad.top - pad.bottom

    // Grid
    if (showGrid) {
      ctx.strokeStyle = 'rgba(255,255,255,0.04)'
      ctx.lineWidth = 1
      for (let i = 0; i <= 4; i++) {
        const y = pad.top + (i / 4) * plotH
        ctx.beginPath()
        ctx.moveTo(pad.left, y)
        ctx.lineTo(pad.left + plotW, y)
        ctx.stroke()
      }
    }

    // Downsample
    const step = Math.max(1, Math.floor(viewLen / MAX_POINTS))
    const indices: number[] = []
    for (let t = startIdx; t <= endIdx; t += step) {
      indices.push(t)
    }
    if (indices[indices.length - 1] !== endIdx) indices.push(endIdx)

    const toX = (arrIdx: number) => {
      const frac = (indices[arrIdx] - startIdx) / Math.max(1, endIdx - startIdx)
      return pad.left + frac * plotW
    }

    // Traces
    const palette = colors ?? DEFAULT_PALETTE
    for (let ch = 0; ch < nChannels; ch++) {
      ctx.beginPath()
      ctx.strokeStyle = palette[ch % palette.length]
      ctx.lineWidth = 1.2
      ctx.lineJoin = 'round'
      ctx.globalAlpha = 0.85

      for (let i = 0; i < indices.length; i++) {
        const x = toX(i)
        const v = getValue(indices[i], ch)
        const y = pad.top + (1 - (v - gMin) / range) * plotH
        if (i === 0) ctx.moveTo(x, y)
        else ctx.lineTo(x, y)
      }
      ctx.stroke()
      ctx.globalAlpha = 1
    }

    // Channel labels
    if (labels && labels.length > 0) {
      ctx.font = '10px var(--font-mono)'
      const labelY = height - 6
      const labelSpacing = plotW / Math.min(labels.length, 8)
      for (let i = 0; i < Math.min(labels.length, 8); i++) {
        ctx.fillStyle = palette[i % palette.length]
        ctx.globalAlpha = 0.7
        ctx.fillText(labels[i], pad.left + i * labelSpacing, labelY)
      }
      ctx.globalAlpha = 1
    }

    // Playback cursor
    if (cursorFrame != null && totalFrames && totalFrames > 0) {
      const dataFrac = cursorFrame / totalFrames
      if (dataFrac >= zs && dataFrac <= ze) {
        const cx = pad.left + ((dataFrac - zs) / (ze - zs)) * plotW
        ctx.beginPath()
        ctx.strokeStyle = 'rgba(255,255,255,0.6)'
        ctx.lineWidth = 1
        ctx.moveTo(cx, pad.top)
        ctx.lineTo(cx, pad.top + plotH)
        ctx.stroke()

        ctx.beginPath()
        ctx.arc(cx, pad.top, 2.5, 0, Math.PI * 2)
        ctx.fillStyle = 'rgba(255,255,255,0.8)'
        ctx.fill()
      }
    }

    // Zoom indicator
    if (ze - zs < 0.99) {
      const barY = height - 3
      ctx.fillStyle = 'rgba(255,255,255,0.06)'
      ctx.fillRect(pad.left, barY, plotW, 2)
      ctx.fillStyle = 'rgba(100,180,255,0.4)'
      ctx.fillRect(pad.left + zs * plotW, barY, (ze - zs) * plotW, 2)
    }
  }

  drawRef.current = draw

  // Initial draw + resize
  useEffect(() => {
    draw()
    const observer = new ResizeObserver(() => drawRef.current())
    if (containerRef.current) observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [data, nChannels, colors, labels, height, showGrid, cursorFrame, totalFrames])

  // Wheel zoom
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const handleWheel = (e: WheelEvent) => {
      e.preventDefault()
      if (nFrames < 2) return

      const rect = canvas.getBoundingClientRect()
      const mouseXFrac = (e.clientX - rect.left) / rect.width
      const { start: zs, end: ze } = zoomRef.current
      const currentRange = ze - zs
      const factor = e.deltaY > 0 ? 1.3 : 0.7
      let newRange = Math.min(1, Math.max(0.005, currentRange * factor))

      if (newRange >= 0.99) {
        zoomRef.current = { start: 0, end: 1 }
        drawRef.current()
        return
      }

      const center = zs + mouseXFrac * currentRange
      let ns = center - mouseXFrac * newRange
      let ne = ns + newRange
      if (ns < 0) { ne -= ns; ns = 0 }
      if (ne > 1) { ns -= (ne - 1); ne = 1 }

      zoomRef.current = { start: Math.max(0, ns), end: Math.min(1, ne) }
      drawRef.current()
    }

    canvas.addEventListener('wheel', handleWheel, { passive: false })
    return () => canvas.removeEventListener('wheel', handleWheel)
  }, [nFrames])

  // Drag to pan
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const handleDown = (e: MouseEvent) => {
      const z = zoomRef.current
      if (z.end - z.start >= 0.99) return
      panRef.current = { active: true, startX: e.clientX, startZoom: { ...z } }
      canvas.style.cursor = 'grabbing'
    }

    const handleMove = (e: MouseEvent) => {
      if (!panRef.current.active) return
      const rect = canvas.getBoundingClientRect()
      const dx = (e.clientX - panRef.current.startX) / rect.width
      const { start: ps, end: pe } = panRef.current.startZoom
      const range = pe - ps
      let ns = ps - dx * range
      let ne = ns + range
      if (ns < 0) { ne -= ns; ns = 0 }
      if (ne > 1) { ns -= (ne - 1); ne = 1 }
      zoomRef.current = { start: Math.max(0, ns), end: Math.min(1, ne) }
      drawRef.current()
    }

    const handleUp = () => {
      if (panRef.current.active) {
        panRef.current.active = false
        canvas.style.cursor = ''
      }
    }

    canvas.addEventListener('mousedown', handleDown)
    window.addEventListener('mousemove', handleMove)
    window.addEventListener('mouseup', handleUp)
    return () => {
      canvas.removeEventListener('mousedown', handleDown)
      window.removeEventListener('mousemove', handleMove)
      window.removeEventListener('mouseup', handleUp)
    }
  }, [])

  // Double-click to reset
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const handleDbl = () => {
      zoomRef.current = { start: 0, end: 1 }
      drawRef.current()
    }
    canvas.addEventListener('dblclick', handleDbl)
    return () => canvas.removeEventListener('dblclick', handleDbl)
  }, [])

  return (
    <div ref={containerRef} className={`w-full ${className}`}>
      <canvas
        ref={canvasRef}
        className="block w-full"
        style={{ height }}
      />
    </div>
  )
}
