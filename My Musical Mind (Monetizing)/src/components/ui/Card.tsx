import { motion } from "framer-motion";
import type { ReactNode } from "react";

interface Props {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  glow?: boolean;
  onClick?: () => void;
  style?: React.CSSProperties;
}

export function Card({ children, className = "", hover = false, glow = false, onClick, style }: Props) {
  const base = glow ? "glow-border p-5" : "spatial-card";
  const hoverClass = hover ? "cursor-pointer" : "";

  return (
    <motion.div
      whileHover={hover ? { scale: 1.01, y: -2 } : undefined}
      className={`${base} ${hoverClass} ${className}`}
      onClick={onClick}
      style={style}
    >
      {children}
    </motion.div>
  );
}
