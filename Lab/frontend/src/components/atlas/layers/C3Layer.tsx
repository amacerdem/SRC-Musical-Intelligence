import { BELIEFS } from '../../../data/beliefs'
import { FUNCTIONS } from '../../../data/functions'
import { RELAYS } from '../../../data/relays'
import type { AtlasNode } from '../types'

interface Props {
  x: number
  y: number
  onHover: (node: AtlasNode | null, e: React.MouseEvent) => void
  selected: string | null
  dimmed: boolean
  highlightBeliefs?: Set<number>
}

const FN_W = 240
const COLS = 3
const COL_GAP = 20
const ROW_GAP = 16
const DOT_R = 4
const DOT_GAP = 4
const DOTS_PER_ROW = 12
const HEADER_H = 32
const PADDING = 10

/** Type colors matching design system */
const TYPE_COLORS = {
  core: '#34d399',
  appraisal: '#60a5fa',
  anticipation: '#fbbf24',
}

/** Map beliefs to their function blocks */
function beliefsByFunction() {
  const map = new Map<string, typeof BELIEFS>()
  for (const f of FUNCTIONS) map.set(f.id, [])
  for (const b of BELIEFS) map.get(b.functionId)?.push(b)
  return map
}

/** Get relay for function */
function relayForFunction(fId: string) {
  return RELAYS.find(r => r.functionId === fId)
}

/** Compute function block height */
function fnBlockHeight(beliefCount: number) {
  const rows = Math.ceil(beliefCount / DOTS_PER_ROW)
  return HEADER_H + rows * (DOT_R * 2 + DOT_GAP) + PADDING * 2 + 24
}

export function C3Layer({ x, y, onHover, selected, dimmed, highlightBeliefs }: Props) {
  const bMap = beliefsByFunction()
  const fnEntries = FUNCTIONS.map((f, i) => {
    const beliefs = bMap.get(f.id) ?? []
    const col = i % COLS
    const row = Math.floor(i / COLS)
    return { fn: f, beliefs, col, row }
  })

  // Compute row heights
  const rowHeights: number[] = []
  for (const entry of fnEntries) {
    const h = fnBlockHeight(entry.beliefs.length)
    if (!rowHeights[entry.row] || h > rowHeights[entry.row]) {
      rowHeights[entry.row] = h
    }
  }

  // Y offsets per row
  const rowY: number[] = []
  let cumY = 0
  for (let r = 0; r < rowHeights.length; r++) {
    rowY[r] = cumY
    cumY += rowHeights[r] + ROW_GAP
  }

  const totalW = COLS * FN_W + (COLS - 1) * COL_GAP
  const totalH = cumY - ROW_GAP

  return (
    <g opacity={dimmed ? 0.15 : 1} style={{ transition: 'opacity 0.3s' }}>
      {/* Layer label */}
      <text
        x={x + totalW / 2} y={y - 24}
        textAnchor="middle" fill="rgba(255,255,255,0.4)"
        fontSize={13} fontWeight={600} letterSpacing="0.06em"
      >
        C³ — 131 Beliefs
      </text>
      <text
        x={x + totalW / 2} y={y - 8}
        textAnchor="middle" fill="rgba(255,255,255,0.2)"
        fontSize={9} letterSpacing="0.04em"
      >
        COGNITIVE BRAIN · 9 FUNCTIONS · 96 MODELS
      </text>

      {/* Border box */}
      <rect
        x={x - 16} y={y - 16}
        width={totalW + 32} height={totalH + 32}
        rx={16} fill="none"
        stroke="rgba(255,255,255,0.06)" strokeWidth={1}
        strokeDasharray="4 4"
      />

      {fnEntries.map(({ fn, beliefs, col, row }) => {
        const fx = x + col * (FN_W + COL_GAP)
        const fy = y + rowY[row]
        const fh = rowHeights[row]
        const isFnSelected = selected === `fn-${fn.id}`
        const relay = relayForFunction(fn.id)

        return (
          <g key={fn.id}>
            {/* Function box */}
            <rect
              x={fx} y={fy}
              width={FN_W} height={fh}
              rx={10}
              fill={isFnSelected ? `${fn.color}15` : `${fn.color}08`}
              stroke={isFnSelected ? fn.color : `${fn.color}25`}
              strokeWidth={isFnSelected ? 1.5 : 0.8}
              style={{ cursor: 'pointer', transition: 'all 0.2s' }}
              onMouseEnter={e => onHover({
                id: `fn-${fn.id}`,
                type: 'function',
                label: `F${fn.index} — ${fn.name}`,
                color: fn.color,
                description: fn.description,
                functionId: fn.id,
              }, e)}
              onMouseLeave={() => onHover(null, null!)}
            />

            {/* Function header */}
            <text
              x={fx + 10} y={fy + 14}
              fill={fn.color} fontSize={10} fontWeight={700}
              fontFamily="var(--font-mono)"
              style={{ pointerEvents: 'none' }}
            >
              F{fn.index}
            </text>
            <text
              x={fx + 32} y={fy + 14}
              fill="rgba(255,255,255,0.7)" fontSize={10} fontWeight={500}
              style={{ pointerEvents: 'none' }}
            >
              {fn.name}
            </text>
            {/* Unit badge */}
            <text
              x={fx + FN_W - 10} y={fy + 14}
              textAnchor="end"
              fill={`${fn.color}80`} fontSize={9}
              fontFamily="var(--font-mono)"
              style={{ pointerEvents: 'none' }}
            >
              {fn.unit}
            </text>

            {/* Belief count */}
            <text
              x={fx + 10} y={fy + 27}
              fill="rgba(255,255,255,0.2)" fontSize={8}
              fontFamily="var(--font-mono)"
              style={{ pointerEvents: 'none' }}
            >
              {fn.beliefCounts.core}C + {fn.beliefCounts.appraisal}A + {fn.beliefCounts.anticipation}N = {fn.beliefCounts.total}
            </text>

            {/* Relay diamond */}
            {relay && (
              <g
                onMouseEnter={e => onHover({
                  id: `relay-${relay.name}`,
                  type: 'relay',
                  label: relay.name,
                  color: fn.color,
                  description: `${relay.fullName} — ${relay.outputDim}D output`,
                  functionId: fn.id,
                }, e)}
                onMouseLeave={() => onHover(null, null!)}
                style={{ cursor: 'pointer' }}
              >
                <polygon
                  points={`${fx + FN_W - 22},${fy + 22} ${fx + FN_W - 14},${fy + 30} ${fx + FN_W - 22},${fy + 38} ${fx + FN_W - 30},${fy + 30}`}
                  fill={`${fn.color}20`}
                  stroke={fn.color} strokeWidth={0.8}
                />
                <text
                  x={fx + FN_W - 22} y={fy + 33}
                  textAnchor="middle"
                  fill={fn.color} fontSize={5} fontWeight={600}
                  fontFamily="var(--font-mono)"
                  style={{ pointerEvents: 'none' }}
                >
                  {relay.name.slice(0, 3)}
                </text>
              </g>
            )}

            {/* Belief dots */}
            {beliefs.map((b, bi) => {
              const dotCol = bi % DOTS_PER_ROW
              const dotRow = Math.floor(bi / DOTS_PER_ROW)
              const dx = fx + PADDING + dotCol * (DOT_R * 2 + DOT_GAP) + DOT_R
              const dy = fy + HEADER_H + PADDING + dotRow * (DOT_R * 2 + DOT_GAP) + DOT_R
              const color = TYPE_COLORS[b.type]
              const isHighlighted = highlightBeliefs?.has(b.index)
              const isBelSelected = selected === `b-${b.index}`

              return (
                <circle
                  key={b.index}
                  cx={dx} cy={dy}
                  r={isHighlighted || isBelSelected ? DOT_R + 1.5 : DOT_R}
                  fill={isHighlighted ? color : `${color}60`}
                  stroke={isBelSelected ? 'white' : isHighlighted ? color : 'transparent'}
                  strokeWidth={isBelSelected ? 1.5 : isHighlighted ? 1 : 0}
                  filter={isHighlighted ? 'url(#glow-sm)' : undefined}
                  style={{ cursor: 'pointer', transition: 'all 0.15s' }}
                  onMouseEnter={e => onHover({
                    id: `b-${b.index}`,
                    type: 'belief',
                    label: b.name.replace(/_/g, ' '),
                    color,
                    description: `${b.type} belief in ${fn.name}`,
                    functionId: fn.id,
                    beliefIndex: b.index,
                  }, e)}
                  onMouseLeave={() => onHover(null, null!)}
                />
              )
            })}
          </g>
        )
      })}

      {/* Legend for belief types */}
      <g>
        {(['core', 'appraisal', 'anticipation'] as const).map((t, i) => (
          <g key={t} transform={`translate(${x + i * 90}, ${y + totalH + 12})`}>
            <circle cx={6} cy={0} r={4} fill={TYPE_COLORS[t]} />
            <text x={14} y={4} fill="rgba(255,255,255,0.35)" fontSize={9}>{t}</text>
          </g>
        ))}
        <text
          x={x + 280} y={y + totalH + 16}
          fill="rgba(255,255,255,0.2)" fontSize={9}
          fontFamily="var(--font-mono)"
        >
          36C + 65A + 30N = 131
        </text>
      </g>

      {/* Input port */}
      <circle
        cx={x - 16} cy={y + totalH / 2}
        r={4} fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" strokeWidth={0.8}
      />
      {/* Output port */}
      <circle
        cx={x + totalW + 16} cy={y + totalH / 2}
        r={4} fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" strokeWidth={0.8}
      />
    </g>
  )
}

export const C3_GRID_W = COLS * FN_W + (COLS - 1) * COL_GAP + 32
