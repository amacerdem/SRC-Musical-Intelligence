import { motion } from "framer-motion";
import { kineticContainer, kineticChar } from "@/design/animations";

interface Props {
  text: string;
  className?: string;
  delay?: number;
}

export function KineticTitle({ text, className = "", delay = 0 }: Props) {
  const chars = text.split("");

  return (
    <motion.div
      variants={kineticContainer}
      initial="initial"
      animate="animate"
      className={`inline-flex ${className}`}
      style={{ perspective: "800px" }}
    >
      {chars.map((char, i) => (
        <motion.span
          key={i}
          variants={{
            ...kineticChar,
            animate: {
              ...kineticChar.animate,
              transition: {
                ...kineticChar.animate.transition,
                delay: delay + i * 0.04,
              },
            },
          }}
          className="inline-block"
          style={{ display: char === " " ? "inline" : "inline-block" }}
        >
          {char === " " ? "\u00A0" : char}
        </motion.span>
      ))}
    </motion.div>
  );
}
