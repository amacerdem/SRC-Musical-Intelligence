/**
 * NeuralGraph — Rectangular node data-flow visualization of the MI system.
 * R³ → H³ → C³ (9 Functions × 131 Beliefs) → 42 Dimensions
 */
import { useMemo } from 'react'
import { R3_GROUPS } from '../../data/r3'
import { FUNCTIONS } from '../../data/functions'
import { BELIEFS } from '../../data/beliefs'
import { RELAYS } from '../../data/relays'
import { ALL_DIMS, LAYER_COLORS, NEURO_DOMAINS } from '../../data/dimensions'
import type { AtlasNode } from './types'

interface Props {
  onHover: (node: AtlasNode | null, e: React.MouseEvent) => void
  onClick: (nodeId: string | null) => void
  selected: string | null
  highlightBeliefs?: Set<number>
  visibleLayers: { r3: boolean; h3: boolean; c3: boolean; dims: boolean }
}

export const CANVAS_W = 2600
export const CANVAS_H = 1200

// ── Colors ──
const TYPE_COLORS = { core: '#34d399', appraisal: '#60a5fa', anticipation: '#fbbf24' }

// ── Layout constants ──
const R3 = { x: 40, y: 80, w: 160, h: 38, gap: 8 }
const H3 = { x: 280, y: 160, w: 140, h: 50, gap: 16 }
const C3_X = 520
const C3_Y = 20
const FN = { w: 280, padX: 10, padY: 38, colGap: 24, rowGap: 18 }
const CHIP = { w: 56, h: 14, gx: 3, gy: 3, perRow: 5 }
const DIM_X = 1900
const DIM = { w: 150, h: 22, gap: 5 }

// ── Helpers ──
function beliefsByFunction() {
  const map = new Map<string, typeof BELIEFS>()
  for (const f of FUNCTIONS) map.set(f.id, [])
  for (const b of BELIEFS) map.get(b.functionId)?.push(b)
  return map
}

function fnBlockH(count: number) {
  const rows = Math.ceil(count / CHIP.perRow)
  return FN.padY + rows * (CHIP.h + CHIP.gy) + 12
}

function bezier(x1: number, y1: number, x2: number, y2: number): string {
  const dx = Math.abs(x2 - x1) * 0.45
  return `M${x1},${y1} C${x1 + dx},${y1} ${x2 - dx},${y2} ${x2},${y2}`
}

// ── Position computation ──
interface Rect { x: number; y: number; w: number; h: number }

function computeLayout() {
  // R³ groups
  const r3Rects: (Rect & { group: typeof R3_GROUPS[0] })[] = R3_GROUPS.map((g, i) => ({
    x: R3.x, y: R3.y + i * (R3.h + R3.gap), w: R3.w, h: R3.h, group: g,
  }))

  // H³ scales
  const h3Scales = ['Micro', 'Meso', 'Macro', 'Ultra']
  const h3Colors = ['#a78bfa', '#818cf8', '#6366f1', '#4f46e5']
  const h3Rects: (Rect & { name: string; color: string; idx: number })[] = h3Scales.map((s, i) => ({
    x: H3.x, y: H3.y + i * (H3.h + H3.gap), w: H3.w, h: H3.h, name: s, color: h3Colors[i], idx: i,
  }))

  // C³ functions — 3 columns
  const bMap = beliefsByFunction()
  const cols = 3
  const fnEntries: { fn: typeof FUNCTIONS[0]; beliefs: typeof BELIEFS; col: number; row: number; rect: Rect }[] = []
  const rowHeights: number[] = []

  FUNCTIONS.forEach((f, i) => {
    const beliefs = bMap.get(f.id) ?? []
    const col = i % cols
    const row = Math.floor(i / cols)
    const h = fnBlockH(beliefs.length)
    if (!rowHeights[row] || h > rowHeights[row]) rowHeights[row] = h
    fnEntries.push({ fn: f, beliefs, col, row, rect: { x: 0, y: 0, w: FN.w, h } })
  })

  // Compute cumulative Y
  const rowY: number[] = []
  let cumY = 0
  for (let r = 0; r < rowHeights.length; r++) {
    rowY[r] = cumY
    cumY += rowHeights[r] + FN.rowGap
  }

  // Assign positions
  for (const e of fnEntries) {
    e.rect.x = C3_X + e.col * (FN.w + FN.colGap)
    e.rect.y = C3_Y + rowY[e.row]
    e.rect.h = rowHeights[e.row]
  }

  // Belief chip positions
  const beliefRects = new Map<number, Rect & { fnId: string }>()
  for (const e of fnEntries) {
    e.beliefs.forEach((b, bi) => {
      const chipCol = bi % CHIP.perRow
      const chipRow = Math.floor(bi / CHIP.perRow)
      beliefRects.set(b.index, {
        x: e.rect.x + FN.padX + chipCol * (CHIP.w + CHIP.gx),
        y: e.rect.y + FN.padY + chipRow * (CHIP.h + CHIP.gy),
        w: CHIP.w, h: CHIP.h, fnId: e.fn.id,
      })
    })
  }

  // Dimension rects
  const dimRects: (Rect & { dim: typeof ALL_DIMS[0]; layer: string })[] = []

  // Psychology
  const psyDims = ALL_DIMS.filter(d => d.layer === 'psychology')
  psyDims.forEach((d, i) => {
    dimRects.push({
      x: DIM_X, y: 60 + i * (DIM.h + DIM.gap), w: DIM.w, h: DIM.h, dim: d, layer: 'psychology',
    })
  })

  // Cognition
  const cogDims = ALL_DIMS.filter(d => d.layer === 'cognition')
  cogDims.forEach((d, i) => {
    dimRects.push({
      x: DIM_X, y: 260 + i * (DIM.h + DIM.gap), w: DIM.w, h: DIM.h, dim: d, layer: 'cognition',
    })
  })

  // Neuroscience
  const neuroDims = ALL_DIMS.filter(d => d.layer === 'neuroscience')
  neuroDims.forEach((d, i) => {
    dimRects.push({
      x: DIM_X, y: 620 + i * (DIM.h + DIM.gap), w: DIM.w, h: DIM.h, dim: d, layer: 'neuroscience',
    })
  })

  return { r3Rects, h3Rects, fnEntries, beliefRects, dimRects }
}

// ═══════════════════════════════════════════════════════════════
// Component
// ═══════════════════════════════════════════════════════════════

export function NeuralGraph({ onHover, onClick, selected, highlightBeliefs, visibleLayers }: Props) {
  const { r3Rects, h3Rects, fnEntries, beliefRects, dimRects } = useMemo(computeLayout, [])

  // Belief→Dimension edges
  const bdEdges = useMemo(() => {
    const edges: { id: string; bIdx: number; dimId: string; bRect: Rect; dRect: Rect; color: string }[] = []
    for (const dr of dimRects) {
      for (const bi of dr.dim.beliefIndices) {
        const br = beliefRects.get(bi)
        if (!br) continue
        edges.push({
          id: `bd-${bi}-${dr.dim.layer}-${dr.dim.index}`,
          bIdx: bi, dimId: `dim-${dr.dim.layer}-${dr.dim.index}`,
          bRect: br, dRect: dr,
          color: LAYER_COLORS[dr.dim.layer as keyof typeof LAYER_COLORS],
        })
      }
    }
    return edges
  }, [beliefRects, dimRects])

  // Active edge set
  const activeEdges = useMemo(() => {
    if (!selected) return new Set<string>()
    const set = new Set<string>()
    for (const e of bdEdges) {
      if (selected === `b-${e.bIdx}` || selected === e.dimId) set.add(e.id)
    }
    return set
  }, [selected, bdEdges])

  const hoverHandlers = (tooltip: AtlasNode) => ({
    onMouseEnter: (e: React.MouseEvent) => onHover(tooltip, e),
    onMouseLeave: () => onHover(null, null!),
    onClick: (e: React.MouseEvent) => { e.stopPropagation(); onClick(tooltip.id) },
  })

  return (
    <g>
      {/* ── Defs ── */}
      <defs>
        <linearGradient id="flow-grad" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="white" stopOpacity="0.08" />
          <stop offset="50%" stopColor="white" stopOpacity="0.20" />
          <stop offset="100%" stopColor="white" stopOpacity="0.08" />
        </linearGradient>
      </defs>

      {/* ══════════ R³ → H³ edges ══════════ */}
      {visibleLayers.r3 && visibleLayers.h3 && r3Rects.map(r =>
        h3Rects.map(h => (
          <path
            key={`${r.group.id}-${h.name}`}
            d={bezier(r.x + r.w, r.y + r.h / 2, h.x, h.y + h.h / 2)}
            fill="none" stroke={r.group.color} strokeWidth={0.5} opacity={0.08}
            strokeDasharray="3 12"
            style={{ animation: 'atlas-flow 4s linear infinite' }}
          />
        ))
      )}

      {/* ══════════ H³ → C³ Function edges ══════════ */}
      {visibleLayers.h3 && visibleLayers.c3 && h3Rects.map(h =>
        fnEntries.map(({ fn, rect }) => (
          <path
            key={`${h.name}-${fn.id}`}
            d={bezier(h.x + h.w, h.y + h.h / 2, rect.x, rect.y + rect.h / 2)}
            fill="none" stroke={fn.color} strokeWidth={0.4} opacity={0.06}
            strokeDasharray="2 14"
            style={{ animation: 'atlas-flow 5s linear infinite' }}
          />
        ))
      )}

      {/* ══════════ Belief → Dimension edges ══════════ */}
      {visibleLayers.c3 && visibleLayers.dims && bdEdges.map(e => {
        const active = activeEdges.has(e.id)
        return (
          <path
            key={e.id}
            d={bezier(e.bRect.x + e.bRect.w, e.bRect.y + e.bRect.h / 2,
                       e.dRect.x, e.dRect.y + e.dRect.h / 2)}
            fill="none" stroke={e.color}
            strokeWidth={active ? 1.4 : 0.4}
            opacity={active ? 0.45 : 0.03}
            strokeDasharray={active ? '3 6' : undefined}
            style={active ? { animation: 'atlas-flow 2s linear infinite' } : { transition: 'opacity 0.3s' }}
          />
        )
      })}

      {/* ══════════ Main pipeline arrows ══════════ */}
      {visibleLayers.r3 && visibleLayers.h3 && (
        <path d={bezier(210, 320, 270, 320)} fill="none" stroke="url(#flow-grad)"
          strokeWidth={4} strokeDasharray="6 16" style={{ animation: 'atlas-flow 3s linear infinite' }} />
      )}
      {visibleLayers.h3 && visibleLayers.c3 && (
        <path d={bezier(430, 320, 510, 320)} fill="none" stroke="url(#flow-grad)"
          strokeWidth={4} strokeDasharray="6 16" style={{ animation: 'atlas-flow 3s linear infinite', animationDelay: '0.5s' }} />
      )}
      {visibleLayers.c3 && visibleLayers.dims && (
        <path d={bezier(1440, 320, 1880, 320)} fill="none" stroke="url(#flow-grad)"
          strokeWidth={4} strokeDasharray="6 16" style={{ animation: 'atlas-flow 3s linear infinite', animationDelay: '1s' }} />
      )}

      {/* ══════════ R³ LAYER ══════════ */}
      {visibleLayers.r3 && (
        <g>
          <text x={R3.x + R3.w / 2} y={R3.y - 32} textAnchor="middle"
            fill="rgba(255,255,255,0.4)" fontSize={13} fontWeight={700} letterSpacing="0.06em">
            R³ · 97D
          </text>
          <text x={R3.x + R3.w / 2} y={R3.y - 16} textAnchor="middle"
            fill="rgba(255,255,255,0.18)" fontSize={8}>PERCEPTUAL FRONT-END</text>

          {r3Rects.map(r => {
            const isSel = selected === `r3-${r.group.id}`
            return (
              <g key={r.group.id} style={{ cursor: 'pointer' }}
                {...hoverHandlers({
                  id: `r3-${r.group.id}`, type: 'r3-group',
                  label: `${r.group.id} — ${r.group.name}`, color: r.group.color,
                  description: `${r.group.domain} · ${r.group.dim}D [${r.group.start}:${r.group.end}]`,
                  features: r.group.features, dimRange: [r.group.start, r.group.end],
                })}>
                <rect x={r.x} y={r.y} width={r.w} height={r.h} rx={6}
                  fill={isSel ? `${r.group.color}20` : `${r.group.color}0a`}
                  stroke={isSel ? r.group.color : `${r.group.color}40`}
                  strokeWidth={isSel ? 1.5 : 0.7}
                  style={{ transition: 'all 0.2s' }} />
                <text x={r.x + 8} y={r.y + 15} fill={r.group.color}
                  fontSize={10} fontWeight={700} fontFamily="var(--font-mono)"
                  style={{ pointerEvents: 'none' }}>
                  {r.group.id}
                </text>
                <text x={r.x + 22} y={r.y + 15} fill="rgba(255,255,255,0.65)"
                  fontSize={9} fontWeight={500} style={{ pointerEvents: 'none' }}>
                  {r.group.name}
                </text>
                <text x={r.x + r.w - 6} y={r.y + 15} textAnchor="end"
                  fill={`${r.group.color}80`} fontSize={8} fontFamily="var(--font-mono)"
                  style={{ pointerEvents: 'none' }}>
                  {r.group.dim}D
                </text>
                {/* Dim range bar */}
                <rect x={r.x + 8} y={r.y + 24} width={r.w - 16} height={3} rx={1.5}
                  fill={`${r.group.color}15`} style={{ pointerEvents: 'none' }} />
                <rect x={r.x + 8} y={r.y + 24}
                  width={(r.w - 16) * (r.group.dim / 20)} height={3} rx={1.5}
                  fill={`${r.group.color}50`} style={{ pointerEvents: 'none' }} />
              </g>
            )
          })}
        </g>
      )}

      {/* ══════════ H³ LAYER ══════════ */}
      {visibleLayers.h3 && (
        <g>
          <text x={H3.x + H3.w / 2} y={H3.y - 32} textAnchor="middle"
            fill="rgba(255,255,255,0.4)" fontSize={13} fontWeight={700} letterSpacing="0.06em">
            H³
          </text>
          <text x={H3.x + H3.w / 2} y={H3.y - 16} textAnchor="middle"
            fill="rgba(255,255,255,0.18)" fontSize={8}>TEMPORAL MORPHOLOGY</text>

          {h3Rects.map(h => {
            const isSel = selected === `h3-${h.name.toLowerCase()}`
            return (
              <g key={h.name} style={{ cursor: 'pointer' }}
                {...hoverHandlers({
                  id: `h3-${h.name.toLowerCase()}`, type: 'h3-scale',
                  label: `${h.name} Scale`, color: h.color,
                  description: `Horizons H${h.idx * 8}–H${h.idx * 8 + 7} · 8 horizons × 24 morphs × 3 laws`,
                })}>
                <rect x={h.x} y={h.y} width={h.w} height={h.h} rx={8}
                  fill={isSel ? `${h.color}20` : `${h.color}0a`}
                  stroke={isSel ? h.color : `${h.color}35`}
                  strokeWidth={isSel ? 1.5 : 0.7}
                  style={{ transition: 'all 0.2s' }} />
                <text x={h.x + h.w / 2} y={h.y + 20} textAnchor="middle"
                  fill={h.color} fontSize={11} fontWeight={600}
                  style={{ pointerEvents: 'none' }}>
                  {h.name}
                </text>
                <text x={h.x + h.w / 2} y={h.y + 35} textAnchor="middle"
                  fill="rgba(255,255,255,0.2)" fontSize={7} fontFamily="var(--font-mono)"
                  style={{ pointerEvents: 'none' }}>
                  H{h.idx * 8}–H{h.idx * 8 + 7}
                </text>
              </g>
            )
          })}

          <text x={H3.x + H3.w / 2} y={H3.y + 4 * (H3.h + H3.gap) + 8} textAnchor="middle"
            fill="rgba(255,255,255,0.15)" fontSize={8} fontFamily="var(--font-mono)">
            32×24×3 = ~8,600 active
          </text>
        </g>
      )}

      {/* ══════════ C³ LAYER ══════════ */}
      {visibleLayers.c3 && (
        <g>
          {/* Section label */}
          <text x={C3_X + (3 * FN.w + 2 * FN.colGap) / 2} y={C3_Y - 28} textAnchor="middle"
            fill="rgba(255,255,255,0.4)" fontSize={13} fontWeight={700} letterSpacing="0.06em">
            C³ — 131 Beliefs · 96 Models
          </text>
          <text x={C3_X + (3 * FN.w + 2 * FN.colGap) / 2} y={C3_Y - 12} textAnchor="middle"
            fill="rgba(255,255,255,0.18)" fontSize={8}>COGNITIVE BRAIN · 9 FUNCTIONS</text>

          {fnEntries.map(({ fn, beliefs, rect }) => {
            const isFnSel = selected === `fn-${fn.id}`
            const relay = RELAYS.find(r => r.functionId === fn.id)

            return (
              <g key={fn.id}>
                {/* Function aura */}
                <rect x={rect.x - 3} y={rect.y - 3} width={rect.w + 6} height={rect.h + 6} rx={14}
                  fill={fn.color} opacity={0.02}
                  style={{ animation: 'atlas-halo 4s ease-in-out infinite', animationDelay: `${fn.index * 0.5}s` }} />

                {/* Function container */}
                <rect x={rect.x} y={rect.y} width={rect.w} height={rect.h} rx={10}
                  fill={isFnSel ? `${fn.color}15` : `${fn.color}08`}
                  stroke={isFnSel ? fn.color : `${fn.color}25`}
                  strokeWidth={isFnSel ? 1.5 : 0.7}
                  style={{ cursor: 'pointer', transition: 'all 0.2s' }}
                  {...hoverHandlers({
                    id: `fn-${fn.id}`, type: 'function',
                    label: `F${fn.index} — ${fn.name}`, color: fn.color,
                    description: fn.description, functionId: fn.id,
                  })} />

                {/* Function header */}
                <text x={rect.x + 10} y={rect.y + 14} fill={fn.color}
                  fontSize={10} fontWeight={700} fontFamily="var(--font-mono)"
                  style={{ pointerEvents: 'none' }}>
                  F{fn.index}
                </text>
                <text x={rect.x + 30} y={rect.y + 14} fill="rgba(255,255,255,0.7)"
                  fontSize={9} fontWeight={500} style={{ pointerEvents: 'none' }}>
                  {fn.name}
                </text>

                {/* Belief count badge */}
                <text x={rect.x + rect.w - 8} y={rect.y + 14} textAnchor="end"
                  fill="rgba(255,255,255,0.2)" fontSize={7} fontFamily="var(--font-mono)"
                  style={{ pointerEvents: 'none' }}>
                  {fn.beliefCounts.core}C+{fn.beliefCounts.appraisal}A+{fn.beliefCounts.anticipation}N
                </text>

                {/* Divider line */}
                <line x1={rect.x + 8} y1={rect.y + 22} x2={rect.x + rect.w - 8} y2={rect.y + 22}
                  stroke={`${fn.color}18`} strokeWidth={0.5} style={{ pointerEvents: 'none' }} />

                {/* Relay diamond */}
                {relay && (() => {
                  const rx = rect.x + rect.w - 20
                  const ry = rect.y + 28
                  return (
                    <g style={{ cursor: 'pointer' }}
                      {...hoverHandlers({
                        id: `relay-${relay.name}`, type: 'relay',
                        label: relay.name, color: fn.color,
                        description: `${relay.fullName} · ${relay.outputDim}D output`,
                        functionId: fn.id,
                      })}>
                      <polygon
                        points={`${rx},${ry - 6} ${rx + 6},${ry} ${rx},${ry + 6} ${rx - 6},${ry}`}
                        fill={`${fn.color}20`} stroke={fn.color} strokeWidth={0.6} />
                      <text x={rx} y={ry + 3} textAnchor="middle"
                        fill={fn.color} fontSize={4} fontWeight={700}
                        fontFamily="var(--font-mono)" style={{ pointerEvents: 'none' }}>
                        {relay.name.slice(0, 3)}
                      </text>
                    </g>
                  )
                })()}

                {/* Belief chips */}
                {beliefs.map((b, bi) => {
                  const chipCol = bi % CHIP.perRow
                  const chipRow = Math.floor(bi / CHIP.perRow)
                  const cx = rect.x + FN.padX + chipCol * (CHIP.w + CHIP.gx)
                  const cy = rect.y + FN.padY + chipRow * (CHIP.h + CHIP.gy)
                  const color = TYPE_COLORS[b.type]
                  const isHL = highlightBeliefs?.has(b.index)
                  const isBSel = selected === `b-${b.index}`
                  const dimmed = highlightBeliefs && !isHL

                  return (
                    <g key={b.index} style={{ cursor: 'pointer' }}
                      {...hoverHandlers({
                        id: `b-${b.index}`, type: 'belief',
                        label: b.name.replace(/_/g, ' '), color,
                        description: `${b.type} belief · F${fn.index} ${fn.name} · ${b.mechanism}`,
                        functionId: fn.id, beliefIndex: b.index,
                      })}>
                      <rect x={cx} y={cy} width={CHIP.w} height={CHIP.h} rx={3}
                        fill={dimmed ? `${color}08` : isHL || isBSel ? `${color}30` : `${color}15`}
                        stroke={isBSel ? 'white' : isHL ? color : `${color}30`}
                        strokeWidth={isBSel ? 1.2 : isHL ? 0.8 : 0.3}
                        opacity={dimmed ? 0.3 : 1}
                        filter={isHL ? 'url(#glow-sm)' : undefined}
                        style={{ transition: 'all 0.15s',
                          animation: !dimmed ? `atlas-pulse ${3 + (b.index % 3) * 0.5}s ease-in-out infinite` : undefined,
                          animationDelay: `${b.index * 0.06}s`,
                        }} />
                      <text x={cx + 3} y={cy + 10} fill={dimmed ? `${color}40` : color}
                        fontSize={5.5} fontFamily="var(--font-mono)" fontWeight={500}
                        style={{ pointerEvents: 'none' }}>
                        {b.name.length > 10 ? b.name.slice(0, 9) + '…' : b.name}
                      </text>
                    </g>
                  )
                })}
              </g>
            )
          })}

          {/* C³ belief type legend */}
          {(['core', 'appraisal', 'anticipation'] as const).map((t, i) => {
            const fnArea = fnEntries[fnEntries.length - 1]
            const ly = (fnArea?.rect.y ?? 0) + (fnArea?.rect.h ?? 0) + 16
            return (
              <g key={t} transform={`translate(${C3_X + i * 100}, ${ly})`}>
                <rect x={0} y={-4} width={8} height={8} rx={2} fill={TYPE_COLORS[t]} opacity={0.8} />
                <text x={12} y={4} fill="rgba(255,255,255,0.3)" fontSize={8}>
                  {t} ({t === 'core' ? 36 : t === 'appraisal' ? 65 : 30})
                </text>
              </g>
            )
          })}
        </g>
      )}

      {/* ══════════ DIMENSIONS LAYER ══════════ */}
      {visibleLayers.dims && (
        <g>
          {/* Section headers */}
          <text x={DIM_X + DIM.w / 2} y={45} textAnchor="middle"
            fill={LAYER_COLORS.psychology} fontSize={10} fontWeight={600} opacity={0.7} letterSpacing="0.05em">
            PSYCHOLOGY · 6D
          </text>
          <text x={DIM_X + DIM.w / 2} y={245} textAnchor="middle"
            fill={LAYER_COLORS.cognition} fontSize={10} fontWeight={600} opacity={0.7} letterSpacing="0.05em">
            COGNITION · 12D
          </text>
          <text x={DIM_X + DIM.w / 2} y={605} textAnchor="middle"
            fill={LAYER_COLORS.neuroscience} fontSize={10} fontWeight={600} opacity={0.7} letterSpacing="0.05em">
            NEUROSCIENCE · 24D
          </text>

          {/* Neuroscience domain labels */}
          {NEURO_DOMAINS.map((domain, di) => (
            <text key={domain.key}
              x={DIM_X - 6} y={633 + di * ((DIM.h + DIM.gap) * 4) / NEURO_DOMAINS.length * NEURO_DOMAINS.length / 6 + di * 0}
              fill="rgba(255,255,255,0.12)" fontSize={6} fontFamily="var(--font-mono)" textAnchor="end"
              style={{ pointerEvents: 'none' }}>
              {domain.name}
            </text>
          ))}

          {dimRects.map(dr => {
            const lc = LAYER_COLORS[dr.dim.layer as keyof typeof LAYER_COLORS]
            const isDimSel = selected === `dim-${dr.dim.layer}-${dr.dim.index}`

            return (
              <g key={`${dr.dim.layer}-${dr.dim.index}`} style={{ cursor: 'pointer' }}
                {...hoverHandlers({
                  id: `dim-${dr.dim.layer}-${dr.dim.index}`,
                  type: `dim-${dr.dim.layer}` as AtlasNode['type'],
                  label: dr.dim.name, color: lc,
                  description: dr.dim.description,
                  beliefIndices: dr.dim.beliefIndices,
                })}>
                <rect x={dr.x} y={dr.y} width={dr.w} height={dr.h} rx={4}
                  fill={isDimSel ? `${lc}25` : `${lc}0a`}
                  stroke={isDimSel ? lc : `${lc}30`}
                  strokeWidth={isDimSel ? 1.5 : 0.5}
                  style={{ transition: 'all 0.2s',
                    animation: `atlas-pulse ${3.5 + (dr.dim.index % 3)}s ease-in-out infinite`,
                    animationDelay: `${dr.dim.index * 0.12}s`,
                  }} />
                <text x={dr.x + 6} y={dr.y + 14} fill={lc}
                  fontSize={8} fontWeight={500} style={{ pointerEvents: 'none' }}>
                  {dr.dim.name}
                </text>
                <text x={dr.x + dr.w - 6} y={dr.y + 14} textAnchor="end"
                  fill={`${lc}50`} fontSize={6} fontFamily="var(--font-mono)"
                  style={{ pointerEvents: 'none' }}>
                  {dr.dim.beliefIndices.length}b
                </text>
              </g>
            )
          })}
        </g>
      )}
    </g>
  )
}
