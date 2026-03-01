import {
  PSYCHOLOGY_DIMS, COGNITION_DIMS, NEUROSCIENCE_DIMS,
  NEURO_DOMAINS, LAYER_COLORS, type DimensionDef,
} from '../../../data/dimensions'
import type { AtlasNode } from '../types'

interface Props {
  x: number
  y: number
  onHover: (node: AtlasNode | null, e: React.MouseEvent) => void
  selected: string | null
  dimmed: boolean
}

const TIER_GAP = 30
const HEX_GAP = 8

/** Draw a hexagon at (cx, cy) with radius r */
function hexPoints(cx: number, cy: number, r: number) {
  return Array.from({ length: 6 }, (_, i) => {
    const angle = (Math.PI / 3) * i - Math.PI / 2
    return `${cx + r * Math.cos(angle)},${cy + r * Math.sin(angle)}`
  }).join(' ')
}

function DimHex({
  dim, cx, cy, r, color, isSelected, onHover,
}: {
  dim: DimensionDef; cx: number; cy: number; r: number; color: string;
  isSelected: boolean; onHover: Props['onHover']
}) {
  const nodeData: AtlasNode = {
    id: `dim-${dim.layer}-${dim.index}`,
    type: `dim-${dim.layer}` as AtlasNode['type'],
    label: dim.name,
    color,
    description: dim.description,
    beliefIndices: dim.beliefIndices,
  }

  return (
    <g
      onMouseEnter={e => onHover(nodeData, e)}
      onMouseLeave={() => onHover(null, null!)}
      style={{ cursor: 'pointer' }}
    >
      <polygon
        points={hexPoints(cx, cy, isSelected ? r + 2 : r)}
        fill={isSelected ? `${color}30` : `${color}15`}
        stroke={isSelected ? color : `${color}50`}
        strokeWidth={isSelected ? 1.5 : 0.8}
        filter={isSelected ? 'url(#glow-sm)' : undefined}
        style={{ transition: 'all 0.2s' }}
      />
      <text
        x={cx} y={cy + 3}
        textAnchor="middle"
        fill="rgba(255,255,255,0.8)"
        fontSize={r > 12 ? 8 : 7}
        fontWeight={500}
        style={{ pointerEvents: 'none' }}
      >
        {dim.name.length > 10 ? dim.name.slice(0, 9) + '…' : dim.name}
      </text>
    </g>
  )
}

function TierSection({
  label, dims, color, x, y, hexR, onHover, selected,
}: {
  label: string; dims: DimensionDef[]; color: string; x: number; y: number; hexR: number;
  onHover: Props['onHover']; selected: string | null
}) {
  const perRow = Math.min(dims.length, 6)
  const rowW = perRow * (hexR * 2 + HEX_GAP)
  const startX = x + (180 - rowW) / 2 + hexR

  return (
    <g>
      <text
        x={x + 90} y={y}
        textAnchor="middle" fill={color} fontSize={10} fontWeight={600}
        letterSpacing="0.04em"
      >
        {label}
      </text>
      {dims.map((d, i) => {
        const col = i % perRow
        const row = Math.floor(i / perRow)
        const cx = startX + col * (hexR * 2 + HEX_GAP)
        const cy = y + 18 + row * (hexR * 2 + HEX_GAP) + hexR
        return (
          <DimHex
            key={d.key}
            dim={d} cx={cx} cy={cy} r={hexR}
            color={color}
            isSelected={selected === `dim-${d.layer}-${d.index}`}
            onHover={onHover}
          />
        )
      })}
    </g>
  )
}

export function DimensionLayer({ x, y, onHover, selected, dimmed }: Props) {
  // Psychology: 6 hexagons, 1 row
  const psyH = 60
  // Cognition: 12 hexagons, 2 rows
  const cogH = 80
  // Neuroscience: 24 hexagons organized by domain
  const neuroH = 280
  const totalH = psyH + TIER_GAP + cogH + TIER_GAP + neuroH

  return (
    <g opacity={dimmed ? 0.15 : 1} style={{ transition: 'opacity 0.3s' }}>
      {/* Layer label */}
      <text
        x={x + 90} y={y - 24}
        textAnchor="middle" fill="rgba(255,255,255,0.4)"
        fontSize={13} fontWeight={600} letterSpacing="0.06em"
      >
        Dimensions — 42D
      </text>
      <text
        x={x + 90} y={y - 8}
        textAnchor="middle" fill="rgba(255,255,255,0.2)"
        fontSize={9} letterSpacing="0.04em"
      >
        3-TIER FALSIFIABILITY
      </text>

      {/* Border box */}
      <rect
        x={x - 12} y={y - 12}
        width={204} height={totalH + 24}
        rx={14} fill="none"
        stroke="rgba(255,255,255,0.06)" strokeWidth={1}
        strokeDasharray="4 4"
      />

      {/* Psychology tier */}
      <TierSection
        label="Psychology · 6D" dims={PSYCHOLOGY_DIMS}
        color={LAYER_COLORS.psychology} x={x} y={y} hexR={14}
        onHover={onHover} selected={selected}
      />

      {/* Cognition tier */}
      <TierSection
        label="Cognition · 12D" dims={COGNITION_DIMS}
        color={LAYER_COLORS.cognition} x={x} y={y + psyH + TIER_GAP} hexR={12}
        onHover={onHover} selected={selected}
      />

      {/* Neuroscience tier — organized by domain */}
      <text
        x={x + 90} y={y + psyH + TIER_GAP + cogH + TIER_GAP}
        textAnchor="middle" fill={LAYER_COLORS.neuroscience} fontSize={10} fontWeight={600}
        letterSpacing="0.04em"
      >
        Neuroscience · 24D
      </text>
      {NEURO_DOMAINS.map((domain, di) => {
        const domainDims = domain.indices.map(i => NEUROSCIENCE_DIMS[i])
        const domainY = y + psyH + TIER_GAP + cogH + TIER_GAP + 18 + di * 42

        return (
          <g key={domain.key}>
            <text
              x={x + 4} y={domainY + 6}
              fill="rgba(255,255,255,0.2)" fontSize={7}
              fontFamily="var(--font-mono)"
            >
              {domain.name}
            </text>
            {domainDims.map((d, i) => {
              const cx = x + 12 + i * 42 + 16
              const cy = domainY + 24
              return (
                <DimHex
                  key={d.key}
                  dim={d} cx={cx} cy={cy} r={10}
                  color={LAYER_COLORS.neuroscience}
                  isSelected={selected === `dim-${d.layer}-${d.index}`}
                  onHover={onHover}
                />
              )
            })}
          </g>
        )
      })}

      {/* Input port */}
      <circle
        cx={x - 12} cy={y + totalH / 2}
        r={4} fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" strokeWidth={0.8}
      />
    </g>
  )
}

export const DIM_LAYER_WIDTH = 204
