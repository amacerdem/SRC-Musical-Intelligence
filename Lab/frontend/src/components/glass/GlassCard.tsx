import { type ReactNode, useState } from 'react'

interface GlassCardProps {
  children: ReactNode
  className?: string
  expandable?: boolean
  expandedContent?: ReactNode
  accent?: string
  level?: 0 | 1 | 2 | 3
  onClick?: () => void
}

export function GlassCard({
  children,
  className = '',
  expandable = false,
  expandedContent,
  accent,
  level = 1,
  onClick,
}: GlassCardProps) {
  const [expanded, setExpanded] = useState(false)

  const handleClick = () => {
    if (expandable) setExpanded((e) => !e)
    onClick?.()
  }

  return (
    <div
      className={`glass-${level} border border-border-subtle rounded-[var(--radius-lg)] transition-all duration-200 ${
        expandable ? 'cursor-pointer' : ''
      } ${expanded ? 'ring-1 ring-white/8' : ''} ${className}`}
      style={accent ? { borderColor: `${accent}22` } : undefined}
      onClick={expandable ? handleClick : onClick}
    >
      {children}
      {expandable && expanded && expandedContent && (
        <div className="border-t border-border-subtle">{expandedContent}</div>
      )}
    </div>
  )
}
