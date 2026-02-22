import { type ReactNode, type CSSProperties } from 'react';

interface Props {
  children: ReactNode;
  className?: string;
  style?: CSSProperties;
  glow?: 'r3' | 'h3' | 'c3' | 'reward';
  small?: boolean;
  onClick?: () => void;
}

export default function GlassPanel({ children, className = '', style, glow, small, onClick }: Props) {
  const base = small ? 'glass-panel-sm' : 'glass-panel';
  const glowClass = glow ? `glow-${glow}` : '';
  return (
    <div
      className={`${base} ${glowClass} ${className}`}
      style={style}
      onClick={onClick}
    >
      {children}
    </div>
  );
}
