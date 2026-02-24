import { useRef, useEffect, useCallback } from 'react'

interface HeatmapChartProps {
  /** Row-major Float32Array of shape rows×cols, or null for placeholder */
  data: Float32Array | null
  rows: number
  cols: number
  /** Row labels (e.g. region names) */
  rowLabels?: string[]
  /** Color scheme: 'viridis' | 'plasma' | 'cool' */
  colorScheme?: 'viridis' | 'plasma' | 'cool'
  height?: number
  /** Current playback frame for cursor sync */
  cursorFrame?: number
  /** Total frames for cursor position */
  totalFrames?: number
  className?: string
}

// Simplified viridis-like gradient stops
const SCHEMES: Record<string, [number, number, number][]> = {
  viridis: [
    [68, 1, 84], [59, 82, 139], [33, 145, 140], [94, 201, 98], [253, 231, 37],
  ],
  plasma: [
    [13, 8, 135], [126, 3, 168], [204, 71, 120], [248, 149, 64], [240, 249, 33],
  ],
  cool: [
    [10, 20, 50], [30, 60, 120], [50, 130, 180], [100, 200, 200], [200, 240, 255],
  ],
}

function interpolateColor(t: number, scheme: [number, number, number][]): string {
  const n = scheme.length - 1
  const i = Math.min(Math.floor(t * n), n - 1)
  const f = t * n - i
  const [r1, g1, b1] = scheme[i]
  const [r2, g2, b2] = scheme[i + 1]
  const r = Math.round(r1 + (r2 - r1) * f)
  const g = Math.round(g1 + (g2 - g1) * f)
  const b = Math.round(b1 + (b2 - b1) * f)
  return `rgb(${r},${g},${b})`
}

export function HeatmapChart({
  data,
  rows,
  cols,
  rowLabels,
  colorScheme = 'viridis',
  height = 300,
  cursorFrame,
  totalFrames,
  className = '',
}: HeatmapChartProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const draw = useCallback(() => {
    const canvas = canvasRef.current
    const container = containerRef.current
    if (!canvas || !container) return

    const totalWidth = container.clientWidth
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const dpr = window.devicePixelRatio || 1
    canvas.width = totalWidth * dpr
    canvas.height = height * dpr
    ctx.scale(dpr, dpr)
    ctx.clearRect(0, 0, totalWidth, height)

    if (!data || data.length === 0) {
      ctx.fillStyle = 'rgba(255,255,255,0.04)'
      ctx.fillRect(0, 0, totalWidth, height)
      ctx.fillStyle = 'rgba(255,255,255,0.1)'
      ctx.font = '11px var(--font-mono)'
      ctx.textAlign = 'center'
      ctx.fillText('no heatmap data', totalWidth / 2, height / 2 + 4)
      return
    }

    // Layout
    const labelW = rowLabels ? 60 : 0
    const legendW = 24
    const plotX = labelW
    const plotW = totalWidth - labelW - legendW - 8
    const plotH = height - 4

    // Normalize
    let min = Infinity
    let max = -Infinity
    for (let i = 0; i < data.length; i++) {
      if (data[i] < min) min = data[i]
      if (data[i] > max) max = data[i]
    }
    const range = max - min || 1
    const scheme = SCHEMES[colorScheme] ?? SCHEMES.viridis

    // Draw cells
    const cellW = plotW / cols
    const cellH = plotH / rows

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const v = data[r * cols + c]
        const t = (v - min) / range
        ctx.fillStyle = interpolateColor(t, scheme)
        ctx.fillRect(plotX + c * cellW, r * cellH, cellW + 0.5, cellH + 0.5)
      }
    }

    // Row labels
    if (rowLabels) {
      ctx.font = '9px var(--font-mono)'
      ctx.fillStyle = 'rgba(255,255,255,0.5)'
      ctx.textAlign = 'right'
      for (let r = 0; r < Math.min(rows, rowLabels.length); r++) {
        ctx.fillText(rowLabels[r], labelW - 4, r * cellH + cellH / 2 + 3)
      }
    }

    // Color legend
    const legX = totalWidth - legendW
    const legH = Math.min(height - 20, 200)
    const legY = (height - legH) / 2
    for (let i = 0; i < legH; i++) {
      const t = 1 - i / legH
      ctx.fillStyle = interpolateColor(t, scheme)
      ctx.fillRect(legX, legY + i, 12, 1)
    }
    ctx.font = '8px var(--font-mono)'
    ctx.fillStyle = 'rgba(255,255,255,0.4)'
    ctx.textAlign = 'left'
    ctx.fillText(max.toFixed(2), legX, legY - 2)
    ctx.fillText(min.toFixed(2), legX, legY + legH + 10)
  }, [data, rows, cols, rowLabels, colorScheme, height])

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
