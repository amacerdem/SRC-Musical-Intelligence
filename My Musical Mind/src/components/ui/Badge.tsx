interface Props {
  label: string;
  color?: string;
  size?: "sm" | "md";
}

export function Badge({ label, color, size = "sm" }: Props) {
  const sizeClass = size === "sm" ? "px-2.5 py-0.5 text-[10px]" : "px-3 py-1 text-xs";

  return (
    <span
      className={`${sizeClass} rounded-full font-medium inline-flex items-center tracking-wide`}
      style={{
        backgroundColor: color ? `${color}10` : "rgba(99,102,241,0.08)",
        color: color || "#A855F7",
        border: `1px solid ${color ? `${color}20` : "rgba(168,85,247,0.15)"}`,
      }}
    >
      {label}
    </span>
  );
}
