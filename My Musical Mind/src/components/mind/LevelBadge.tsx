import { getLevelTitle } from "@/data/levels";

interface Props {
  level: number;
  size?: "sm" | "md" | "lg";
}

export function LevelBadge({ level, size = "md" }: Props) {
  const title = getLevelTitle(level);

  const sizeStyles = {
    sm: "w-5 h-5 text-[9px]",
    md: "w-7 h-7 text-[10px]",
    lg: "w-10 h-10 text-sm",
  };

  /* Color by tier — more muted */
  const tierColor =
    level >= 46 ? "#FBBF24" :
    level >= 36 ? "#A855F7" :
    level >= 26 ? "#6366F1" :
    level >= 16 ? "#10B981" :
    level >= 6  ? "#60A5FA" :
    "#94A3B8";

  return (
    <div className="flex items-center gap-2">
      <div
        className={`${sizeStyles[size]} rounded-lg flex items-center justify-center font-display font-bold`}
        style={{
          background: `${tierColor}10`,
          border: `1px solid ${tierColor}20`,
          color: tierColor,
        }}
      >
        {level}
      </div>
      {size !== "sm" && (
        <span className="text-[10px] font-medium" style={{ color: `${tierColor}90` }}>
          {title}
        </span>
      )}
    </div>
  );
}
