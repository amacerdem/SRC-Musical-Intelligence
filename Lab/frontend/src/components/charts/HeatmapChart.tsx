import { useRef, useEffect } from 'react'

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

/** Max display columns */
const MAX_COLS = 600

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
  const zoomRef = useRef({ start: 0, end: 1 })
  const panRef = useRef({ active: false, startX: 0, startZoom: { start: 0, end: 1 } })
  const drawRef = useRef<() => void>(() => {})

  const draw = () => {
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

    const { start: zs, end: ze } = zoomRef.current
    const startCol = Math.floor(zs * (cols - 1))
    const endCol = Math.ceil(ze * (cols - 1))
    const viewCols = endCol - startCol + 1

    // Layout
    const labelW = rowLabels ? 60 : 0
    const legendW = 24
    const plotX = labelW
    const plotW = totalWidth - labelW - legendW - 8
    const plotH = height - 4

    // Normalize on visible range
    let min = Infinity
    let max = -Infinity
    for (let r = 0; r < rows; r++) {
      for (let c = startCol; c <= endCol; c++) {
        const v = data[r * cols + c]
        if (v < min) min = v
        if (v > max) max = v
      }
    }
    const range = max - min || 1
    const scheme = SCHEMES[colorScheme] ?? SCHEMES.viridis

    // Downsample columns
    const step = Math.max(1, Math.floor(viewCols / MAX_COLS))
    const displayCols: number[] = []
    for (let c = startCol; c <= endCol; c += step) {
      displayCols.push(c)
    }
    if (displayCols[displayCols.length - 1] !== endCol) displayCols.push(endCol)

    // Draw cells
    const cellW = plotW / displayCols.length
    const cellH = plotH / rows

    for (let r = 0; r < rows; r++) {
      for (let ci = 0; ci < displayCols.length; ci++) {
        // Average values in this bucket for better representation
        const bucketStart = displayCols[ci]
        const bucketEnd = ci < displayCols.length - 1 ? displayCols[ci + 1] : endCol + 1
        let sum = 0
        let count = 0
        for (let c = bucketStart; c < bucketEnd; c++) {
          sum += data[r * cols + c]
          count++
        }
        const v = count > 0 ? sum / count : data[r * cols + bucketStart]
        const t = (v - min) / range
        ctx.fillStyle = interpolateColor(t, scheme)
        ctx.fillRect(plotX + ci * cellW, r * cellH, cellW + 0.5, cellH + 0.5)
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

    // Playback cursor
    if (cursorFrame != null && totalFrames && totalFrames > 0) {
      const dataFrac = cursorFrame / totalFrames
      if (dataFrac >= zs && dataFrac <= ze) {
        const cx = plotX + ((dataFrac - zs) / (ze - zs)) * plotW
        ctx.beginPath()
        ctx.strokeStyle = 'rgba(255,255,255,0.7)'
        ctx.lineWidth = 1.5
        ctx.moveTo(cx, 0)
        ctx.lineTo(cx, plotH)
        ctx.stroke()
      }
    }

    // Zoom indicator
    if (ze - zs < 0.99) {
      const barY = height - 3
      ctx.fillStyle = 'rgba(255,255,255,0.06)'
      ctx.fillRect(plotX, barY, plotW, 2)
      ctx.fillStyle = 'rgba(100,180,255,0.4)'
      ctx.fillRect(plotX + zs * plotW, barY, (ze - zs) * plotW, 2)
    }
  }

  drawRef.current = draw

  useEffect(() => {
    draw()
    const observer = new ResizeObserver(() => drawRef.current())
    if (containerRef.current) observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [data, rows, cols, rowLabels, colorScheme, height, cursorFrame, totalFrames])

  // Wheel zoom
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const handleWheel = (e: WheelEvent) => {
      e.preventDefault()
      if (cols < 2) return

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
  }, [cols])

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
