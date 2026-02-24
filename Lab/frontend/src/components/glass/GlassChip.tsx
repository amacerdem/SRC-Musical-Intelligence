interface GlassChipProps {
  label: string
  color?: string
  size?: 'sm' | 'md'
}

export function GlassChip({ label, color, size = 'sm' }: GlassChipProps) {
  return (
    <span
      className={`glass-chip ${size === 'md' ? 'text-xs px-3 py-1' : ''}`}
      style={color ? { borderColor: `${color}33`, color } : undefined}
    >
      {label}
    </span>
  )
}
