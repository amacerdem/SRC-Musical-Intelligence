import type { ReactNode, ButtonHTMLAttributes } from 'react'

interface GlassButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md'
  children: ReactNode
  accent?: string
}

export function GlassButton({
  variant = 'secondary',
  size = 'md',
  children,
  accent,
  className = '',
  ...props
}: GlassButtonProps) {
  const base = 'inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all duration-150'
  const sizeClass = size === 'sm' ? 'text-xs px-3 py-1.5' : 'text-sm px-4 py-2'

  const variants = {
    primary: 'bg-white/10 text-text-primary hover:bg-white/14 border border-white/12',
    secondary: 'bg-white/5 text-text-secondary hover:text-text-primary hover:bg-white/8 border border-border-subtle',
    ghost: 'text-text-secondary hover:text-text-primary hover:bg-white/5',
  }

  return (
    <button
      className={`${base} ${sizeClass} ${variants[variant]} ${className}`}
      style={variant === 'primary' && accent ? { backgroundColor: `${accent}20`, borderColor: `${accent}33`, color: accent } : undefined}
      {...props}
    >
      {children}
    </button>
  )
}
