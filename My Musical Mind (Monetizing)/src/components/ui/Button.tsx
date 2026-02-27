import { motion } from "framer-motion";
import type { ButtonHTMLAttributes, ReactNode } from "react";

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "glass" | "ghost";
  size?: "sm" | "md" | "lg";
  children: ReactNode;
}

const sizeClasses = {
  sm: "px-4 py-2 text-sm",
  md: "px-6 py-3 text-sm",
  lg: "px-8 py-3.5 text-base",
};

export function Button({
  variant = "primary",
  size = "md",
  children,
  className = "",
  ...rest
}: Props) {
  const base = sizeClasses[size] + " rounded-full font-medium transition-all duration-500 " + className;

  if (variant === "primary") {
    return (
      <motion.button
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.97 }}
        className={`${base} text-white bg-accent-gradient shadow-lg shadow-purple-500/10 hover:shadow-purple-500/25`}
        {...(rest as any)}
      >
        {children}
      </motion.button>
    );
  }

  if (variant === "glass") {
    return (
      <motion.button
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.97 }}
        className={`${base} glass-hover text-slate-300 hover:text-slate-100`}
        {...(rest as any)}
      >
        {children}
      </motion.button>
    );
  }

  return (
    <motion.button
      whileHover={{ scale: 1.03 }}
      whileTap={{ scale: 0.97 }}
      className={`${base} text-slate-500 hover:text-slate-300 hover:bg-white/[0.03]`}
      {...(rest as any)}
    >
      {children}
    </motion.button>
  );
}
