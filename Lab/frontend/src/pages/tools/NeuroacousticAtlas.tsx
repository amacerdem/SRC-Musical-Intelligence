import { useState, useCallback, useMemo } from 'react'
import { AtlasCanvas } from '../../components/atlas/AtlasCanvas'
import { AtlasTooltip } from '../../components/atlas/AtlasTooltip'
import { R3Layer } from '../../components/atlas/layers/R3Layer'
import { H3Layer } from '../../components/atlas/layers/H3Layer'
import { C3Layer } from '../../components/atlas/layers/C3Layer'
import { DimensionLayer } from '../../components/atlas/layers/DimensionLayer'
import { ALL_DIMS } from '../../data/dimensions'
import { BELIEFS } from '../../data/beliefs'
import type { AtlasNode } from '../../components/atlas/types'

type LayerKey = 'r3' | 'h3' | 'c3' | 'dims'

/** Layout X positions for each layer column */
const LAYOUT = {
  r3: { x: 60, y: 80 },
  h3: { x: 280, y: 100 },
  c3: { x: 480, y: 40 },
  dims: { x: 1320, y: 80 },
  width: 1560,
  height: 700,
}

export function NeuroacousticAtlas() {
  const [hovered, setHovered] = useState<AtlasNode | null>(null)
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 })
  const [selected, setSelected] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [layers, setLayers] = useState<Record<LayerKey, boolean>>({
    r3: true, h3: true, c3: true, dims: true,
  })

  const handleHover = useCallback((node: AtlasNode | null, e: React.MouseEvent) => {
    setHovered(node)
    if (e) setMousePos({ x: e.clientX, y: e.clientY })
  }, [])

  const handleClick = useCallback(() => {
    if (hovered) {
      setSelected(prev => prev === hovered.id ? null : hovered.id)
    } else {
      setSelected(null)
    }
  }, [hovered])

  const toggleLayer = useCallback((key: LayerKey) => {
    setLayers(prev => ({ ...prev, [key]: !prev[key] }))
  }, [])

  /** Highlight beliefs connected to selected dimension */
  const highlightBeliefs = useMemo(() => {
    if (!selected) return undefined
    const set = new Set<number>()
    // If a dimension is selected, highlight its source beliefs
    if (selected.startsWith('dim-')) {
      const parts = selected.split('-')
      const layer = parts[1] as 'psychology' | 'cognition' | 'neuroscience'
      const idx = parseInt(parts[2])
      const dim = ALL_DIMS.find(d => d.layer === layer && d.index === idx)
      if (dim) dim.beliefIndices.forEach(bi => set.add(bi))
    }
    // If a belief is selected, highlight connected dimensions' beliefs too
    if (selected.startsWith('b-')) {
      const bIdx = parseInt(selected.split('-')[1])
      set.add(bIdx)
      for (const d of ALL_DIMS) {
        if (d.beliefIndices.includes(bIdx)) {
          d.beliefIndices.forEach(bi => set.add(bi))
        }
      }
    }
    return set.size > 0 ? set : undefined
  }, [selected])

  /** Flow edges between layers */
  const flowEdges = useMemo(() => {
    const edges: { x1: number; y1: number; x2: number; y2: number; color: string }[] = []
    // R3 → H3
    if (layers.r3 && layers.h3) {
      edges.push({
        x1: LAYOUT.r3.x + 152, y1: LAYOUT.r3.y + 250,
        x2: LAYOUT.h3.x - 12, y2: LAYOUT.h3.y + 100,
        color: 'rgba(255,255,255,0.08)',
      })
    }
    // H3 → C3
    if (layers.h3 && layers.c3) {
      edges.push({
        x1: LAYOUT.h3.x + 132, y1: LAYOUT.h3.y + 100,
        x2: LAYOUT.c3.x - 16, y2: LAYOUT.c3.y + 220,
        color: 'rgba(255,255,255,0.08)',
      })
    }
    // C3 → Dims
    if (layers.c3 && layers.dims) {
      edges.push({
        x1: LAYOUT.c3.x + 776, y1: LAYOUT.c3.y + 220,
        x2: LAYOUT.dims.x - 12, y2: LAYOUT.dims.y + 240,
        color: 'rgba(255,255,255,0.08)',
      })
    }
    return edges
  }, [layers])

  /** Search filtering — compute dimmed state per layer */
  const searchLower = search.toLowerCase()
  const hasSearch = searchLower.length > 1
  const searchMatchesLayer = useCallback((layerKey: LayerKey): boolean => {
    if (!hasSearch) return false
    if (layerKey === 'r3') return 'r3 perceptual'.includes(searchLower)
    if (layerKey === 'h3') return 'h3 temporal morphology'.includes(searchLower)
    if (layerKey === 'c3') {
      return BELIEFS.some(b => b.name.includes(searchLower)) ||
        'c3 cognitive brain belief'.includes(searchLower)
    }
    if (layerKey === 'dims') {
      return ALL_DIMS.some(d => d.name.toLowerCase().includes(searchLower) || d.key.includes(searchLower))
    }
    return false
  }, [hasSearch, searchLower])

  return (
    <div className="flex flex-col h-full min-h-0">
      {/* Header */}
      <header className="shrink-0 px-8 pt-6 pb-3">
        <h1 className="text-2xl font-semibold tracking-tight">Neuroacoustic Atlas</h1>
        <p className="mt-1 text-sm text-text-secondary">
          Interactive map of the full MI system — R³ → H³ → C³ → Dimensions
        </p>
      </header>

      {/* Controls bar */}
      <div className="shrink-0 px-8 pb-3 flex items-center gap-4">
        {/* Search */}
        <input
          type="text"
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Search beliefs, dimensions, functions…"
          className="glass-1 px-3 py-1.5 rounded-lg text-xs text-text-primary border border-white/6 w-64 outline-none focus:border-white/15 placeholder:text-text-tertiary"
          style={{ background: 'rgba(255,255,255,0.03)' }}
        />

        {/* Layer toggles */}
        <div className="flex gap-1.5">
          {(['r3', 'h3', 'c3', 'dims'] as LayerKey[]).map(key => (
            <button
              key={key}
              onClick={() => toggleLayer(key)}
              className={`px-2.5 py-1 rounded-md text-xs font-medium transition-all border ${
                layers[key]
                  ? 'bg-white/8 text-text-primary border-white/12'
                  : 'bg-transparent text-text-tertiary border-white/4'
              }`}
            >
              {key === 'r3' ? 'R³' : key === 'h3' ? 'H³' : key === 'c3' ? 'C³' : 'Dims'}
            </button>
          ))}
        </div>

        {/* Stats */}
        <div className="ml-auto flex items-center gap-4 text-[10px] text-text-tertiary mono">
          <span>97D R³</span>
          <span className="text-text-tertiary/40">→</span>
          <span>H³ temporal</span>
          <span className="text-text-tertiary/40">→</span>
          <span>131 beliefs</span>
          <span className="text-text-tertiary/40">→</span>
          <span>42 dimensions</span>
        </div>
      </div>

      {/* Atlas canvas */}
      <div className="flex-1 px-4 pb-4 min-h-0" onClick={handleClick}>
        <AtlasCanvas width={LAYOUT.width} height={LAYOUT.height}>
          {/* Flow edges */}
          {flowEdges.map((e, i) => (
            <path
              key={i}
              d={`M${e.x1},${e.y1} C${e.x1 + 40},${e.y1} ${e.x2 - 40},${e.y2} ${e.x2},${e.y2}`}
              fill="none"
              stroke={e.color}
              strokeWidth={2.5}
              strokeDasharray="8 4"
            />
          ))}

          {/* R³ Layer */}
          {layers.r3 && (
            <R3Layer
              x={LAYOUT.r3.x} y={LAYOUT.r3.y}
              onHover={handleHover}
              selected={selected}
              dimmed={hasSearch && !searchMatchesLayer('r3')}
            />
          )}

          {/* H³ Layer */}
          {layers.h3 && (
            <H3Layer
              x={LAYOUT.h3.x} y={LAYOUT.h3.y}
              onHover={handleHover}
              selected={selected}
              dimmed={hasSearch && !searchMatchesLayer('h3')}
            />
          )}

          {/* C³ Layer */}
          {layers.c3 && (
            <C3Layer
              x={LAYOUT.c3.x} y={LAYOUT.c3.y}
              onHover={handleHover}
              selected={selected}
              dimmed={hasSearch && !searchMatchesLayer('c3')}
              highlightBeliefs={highlightBeliefs}
            />
          )}

          {/* Dimension Layer */}
          {layers.dims && (
            <DimensionLayer
              x={LAYOUT.dims.x} y={LAYOUT.dims.y}
              onHover={handleHover}
              selected={selected}
              dimmed={hasSearch && !searchMatchesLayer('dims')}
            />
          )}
        </AtlasCanvas>
      </div>

      {/* Tooltip */}
      <AtlasTooltip node={hovered} x={mousePos.x} y={mousePos.y} />

      {/* Legend overlay */}
      <div className="absolute bottom-8 left-12 glass-2 rounded-xl border border-white/6 p-3 pointer-events-none">
        <div className="text-[10px] text-text-tertiary uppercase tracking-wider mb-2 font-semibold">Legend</div>
        <div className="grid grid-cols-2 gap-x-6 gap-y-1.5">
          {[
            { shape: 'rect', color: 'rgba(255,255,255,0.3)', label: 'R³ Group / H³ Scale' },
            { shape: 'rect', color: '#3b82f6', label: 'C³ Function (F1-F9)' },
            { shape: 'circle-core', color: '#34d399', label: 'Core Belief (36)' },
            { shape: 'circle-app', color: '#60a5fa', label: 'Appraisal (65)' },
            { shape: 'circle-ant', color: '#fbbf24', label: 'Anticipation (30)' },
            { shape: 'hex', color: '#22c55e', label: 'Dimension' },
          ].map(item => (
            <div key={item.label} className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-sm" style={{ background: `${item.color}40`, border: `1px solid ${item.color}` }} />
              <span className="text-[10px] text-text-secondary">{item.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
