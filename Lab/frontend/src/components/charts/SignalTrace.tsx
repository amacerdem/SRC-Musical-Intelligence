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
}

const DEFAULT_PALETTE = [
  '#3b82f6', '#8b5cf6', '#f97316', '#14b8a6', '#ec4899',
  '#f59e0b', '#22c55e', '#6366f1', '#06b6d4', '#ef4444',
  '#a855f7', '#10b981', '#f43f5e', '#84cc16', '#0ea5e9',
  '#d946ef',
]

export function SignalTrace({
  data,
  nChannels,
  colors,
  labels,
  height = 200,
  className = '',
  showGrid = true,
}: SignalTraceProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const draw = useCallback(() => {
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

    // Determine nFrames
    let nFrames: number
    let getValue: (t: number, ch: number) => number

    if (data instanceof Float32Array) {
      nFrames = data.length / nChannels
      getValue = (t, ch) => data[t * nChannels + ch]
    } else {
      nFrames = data.length
      getValue = (t, ch) => data[t]?.[ch] ?? 0
    }

    if (nFrames < 2) return

    // Find global min/max
    let gMin = Infinity
    let gMax = -Infinity
    for (let ch = 0; ch < nChannels; ch++) {
      for (let t = 0; t < nFrames; t++) {
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

    // Traces
    const palette = colors ?? DEFAULT_PALETTE
    for (let ch = 0; ch < nChannels; ch++) {
      ctx.beginPath()
      ctx.strokeStyle = palette[ch % palette.length]
      ctx.lineWidth = 1.2
      ctx.lineJoin = 'round'
      ctx.globalAlpha = 0.85

      for (let t = 0; t < nFrames; t++) {
        const x = pad.left + (t / (nFrames - 1)) * plotW
        const v = getValue(t, ch)
        const y = pad.top + (1 - (v - gMin) / range) * plotH
        if (t === 0) ctx.moveTo(x, y)
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
  }, [data, nChannels, colors, labels, height, showGrid])

  useEffect(() => {
    draw()
    const observer = new ResizeObserver(draw)
    if (containerRef.current) observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [draw])

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
