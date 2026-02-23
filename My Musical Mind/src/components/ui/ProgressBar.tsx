import { motion } from "framer-motion";

interface Props {
  value: number;    // 0-100
  color?: string;
  height?: number;
  showLabel?: boolean;
  label?: string;
}

export function ProgressBar({
  value,
  color = "#A855F7",
  height = 2,
  showLabel = false,
  label,
}: Props) {
  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between mb-1.5 text-[10px]">
          <span className="text-slate-600">{label}</span>
          <span className="font-mono text-slate-700">{Math.round(value)}%</span>
        </div>
      )}
      <div
        className="w-full rounded-full overflow-hidden"
        style={{ height, background: "rgba(255,255,255,0.03)" }}
      >
        <motion.div
          className="h-full rounded-full"
          style={{
            backgroundColor: color,
            opacity: 0.6,
            boxShadow: `0 0 8px ${color}30`,
          }}
          initial={{ width: 0 }}
          animate={{ width: `${Math.min(100, Math.max(0, value))}%` }}
          transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
        />
      </div>
    </div>
  );
}
