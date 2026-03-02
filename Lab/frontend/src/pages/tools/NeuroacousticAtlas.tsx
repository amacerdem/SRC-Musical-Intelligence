import { useState, useCallback, useMemo } from 'react'
import { AtlasCanvas } from '../../components/atlas/AtlasCanvas'
import { AtlasTooltip } from '../../components/atlas/AtlasTooltip'
import { NeuralGraph, CANVAS_W, CANVAS_H } from '../../components/atlas/NeuralGraph'
import { ALL_DIMS } from '../../data/dimensions'
import type { AtlasNode } from '../../components/atlas/types'

type LayerKey = 'r3' | 'h3' | 'c3' | 'dims'

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

  const handleNodeClick = useCallback((nodeId: string | null) => {
    setSelected(prev => prev === nodeId ? null : nodeId)
  }, [])

  const handleBgClick = useCallback(() => {
    setSelected(null)
  }, [])

  const toggleLayer = useCallback((key: LayerKey) => {
    setLayers(prev => ({ ...prev, [key]: !prev[key] }))
  }, [])

  /** Highlight beliefs connected to selected dimension (or vice versa) */
  const highlightBeliefs = useMemo(() => {
    if (!selected) return undefined
    const set = new Set<number>()
    if (selected.startsWith('dim-')) {
      const parts = selected.split('-')
      const layer = parts[1] as 'psychology' | 'cognition' | 'neuroscience'
      const idx = parseInt(parts[2])
      const dim = ALL_DIMS.find(d => d.layer === layer && d.index === idx)
      if (dim) dim.beliefIndices.forEach(bi => set.add(bi))
    }
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

  return (
    <div className="relative flex flex-col h-full min-h-0">
      {/* Header */}
      <header className="shrink-0 px-8 pt-5 pb-2">
        <h1 className="text-xl font-semibold tracking-tight">Neuroacoustic Atlas</h1>
        <p className="mt-0.5 text-xs text-text-secondary">
          Interactive neural map — R³ → H³ → C³ → Dimensions
        </p>
      </header>

      {/* Controls */}
      <div className="shrink-0 px-8 pb-2 flex items-center gap-4">
        <input
          type="text"
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Search…"
          className="glass-1 px-3 py-1 rounded-lg text-xs text-text-primary border border-white/6 w-48 outline-none focus:border-white/15 placeholder:text-text-tertiary"
          style={{ background: 'rgba(255,255,255,0.03)' }}
        />
        <div className="flex gap-1">
          {(['r3', 'h3', 'c3', 'dims'] as LayerKey[]).map(key => (
            <button
              key={key}
              onClick={() => toggleLayer(key)}
              className={`px-2 py-0.5 rounded-md text-[11px] font-medium transition-all border ${
                layers[key]
                  ? 'bg-white/8 text-text-primary border-white/12'
                  : 'bg-transparent text-text-tertiary border-white/4'
              }`}
            >
              {key === 'r3' ? 'R³' : key === 'h3' ? 'H³' : key === 'c3' ? 'C³' : 'Dims'}
            </button>
          ))}
        </div>
        <div className="ml-auto flex items-center gap-3 text-[10px] text-text-tertiary mono">
          <span>97D</span>
          <span style={{ opacity: 0.3 }}>→</span>
          <span>H³</span>
          <span style={{ opacity: 0.3 }}>→</span>
          <span>131 beliefs</span>
          <span style={{ opacity: 0.3 }}>→</span>
          <span>42D</span>
        </div>
      </div>

      {/* Canvas */}
      <div className="flex-1 flex flex-col px-3 pb-3 min-h-0" onClick={handleBgClick}>
        <AtlasCanvas width={CANVAS_W} height={CANVAS_H}>
          <NeuralGraph
            onHover={handleHover}
            onClick={handleNodeClick}
            selected={selected}
            highlightBeliefs={highlightBeliefs}
            visibleLayers={layers}
          />
        </AtlasCanvas>
      </div>

      {/* Tooltip */}
      <AtlasTooltip node={hovered} x={mousePos.x} y={mousePos.y} />

      {/* Legend */}
      <div className="absolute bottom-6 left-8 glass-2 rounded-lg border border-white/6 px-3 py-2 pointer-events-none">
        <div className="text-[9px] text-text-tertiary uppercase tracking-wider mb-1.5 font-semibold">Legend</div>
        <div className="grid grid-cols-2 gap-x-5 gap-y-1">
          {[
            { color: '#3b82f6', label: 'Function (F1–F9)' },
            { color: '#34d399', label: 'Core Belief' },
            { color: '#60a5fa', label: 'Appraisal' },
            { color: '#fbbf24', label: 'Anticipation' },
            { color: '#22c55e', label: 'Psychology Dim' },
            { color: '#3b82f6', label: 'Cognition Dim' },
            { color: '#8b5cf6', label: 'Neuroscience Dim' },
          ].map(item => (
            <div key={item.label} className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full" style={{ background: item.color, opacity: 0.8 }} />
              <span className="text-[9px] text-text-secondary">{item.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
