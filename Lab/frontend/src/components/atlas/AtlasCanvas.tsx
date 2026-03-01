import { useRef, useState, useCallback, type ReactNode, type WheelEvent, type MouseEvent } from 'react'

interface Props {
  width: number
  height: number
  children: ReactNode
}

const MIN_SCALE = 0.15
const MAX_SCALE = 3
const ZOOM_SPEED = 0.001

export function AtlasCanvas({ width, height, children }: Props) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [scale, setScale] = useState(0.45)
  const [dragging, setDragging] = useState(false)
  const dragStart = useRef({ x: 0, y: 0, panX: 0, panY: 0 })

  const handleWheel = useCallback((e: WheelEvent) => {
    e.preventDefault()
    const rect = containerRef.current?.getBoundingClientRect()
    if (!rect) return

    const mx = e.clientX - rect.left
    const my = e.clientY - rect.top

    const factor = 1 - e.deltaY * ZOOM_SPEED
    const newScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, scale * factor))
    const ratio = newScale / scale

    setPan(p => ({
      x: mx - ratio * (mx - p.x),
      y: my - ratio * (my - p.y),
    }))
    setScale(newScale)
  }, [scale])

  const handleMouseDown = useCallback((e: MouseEvent) => {
    if (e.button !== 0) return
    setDragging(true)
    dragStart.current = { x: e.clientX, y: e.clientY, panX: pan.x, panY: pan.y }
  }, [pan])

  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (!dragging) return
    setPan({
      x: dragStart.current.panX + (e.clientX - dragStart.current.x),
      y: dragStart.current.panY + (e.clientY - dragStart.current.y),
    })
  }, [dragging])

  const handleMouseUp = useCallback(() => setDragging(false), [])

  const fitToView = useCallback(() => {
    const rect = containerRef.current?.getBoundingClientRect()
    if (!rect) return
    const sx = rect.width / width
    const sy = rect.height / height
    const s = Math.min(sx, sy) * 0.92
    setPan({
      x: (rect.width - width * s) / 2,
      y: (rect.height - height * s) / 2,
    })
    setScale(s)
  }, [width, height])

  return (
    <div
      ref={containerRef}
      className="relative w-full flex-1 overflow-hidden rounded-xl"
      style={{ background: 'var(--color-bg-base)', cursor: dragging ? 'grabbing' : 'grab' }}
      onWheel={handleWheel}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
      {/* Subtle grid background */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ opacity: 0.03 }}>
        <defs>
          <pattern id="atlas-grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="white" strokeWidth="0.5" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#atlas-grid)" />
      </svg>

      {/* Main SVG canvas */}
      <svg
        className="absolute inset-0 w-full h-full"
        style={{ overflow: 'visible' }}
      >
        <defs>
          <filter id="glow-sm">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
          <filter id="glow-md">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
        </defs>
        <g transform={`translate(${pan.x},${pan.y}) scale(${scale})`}>
          {children}
        </g>
      </svg>

      {/* Controls overlay */}
      <div className="absolute bottom-4 right-4 flex gap-2">
        <button
          onClick={fitToView}
          className="glass-1 px-3 py-1.5 rounded-lg text-xs text-text-secondary hover:text-text-primary transition-colors border border-white/6"
        >
          Fit
        </button>
        <button
          onClick={() => setScale(s => Math.min(MAX_SCALE, s * 1.3))}
          className="glass-1 w-8 h-8 rounded-lg text-sm text-text-secondary hover:text-text-primary transition-colors border border-white/6 flex items-center justify-center"
        >
          +
        </button>
        <button
          onClick={() => setScale(s => Math.max(MIN_SCALE, s / 1.3))}
          className="glass-1 w-8 h-8 rounded-lg text-sm text-text-secondary hover:text-text-primary transition-colors border border-white/6 flex items-center justify-center"
        >
          -
        </button>
      </div>

      {/* Scale indicator */}
      <div className="absolute bottom-4 left-4 text-[10px] mono text-text-tertiary">
        {Math.round(scale * 100)}%
      </div>
    </div>
  )
}
