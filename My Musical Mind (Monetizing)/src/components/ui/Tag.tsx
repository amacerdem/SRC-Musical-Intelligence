interface Props {
  label: string;
  active?: boolean;
  onClick?: () => void;
}

export function Tag({ label, active = false, onClick }: Props) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ${
        active
          ? "bg-m3-accent-purple/20 text-purple-300 border border-purple-500/30"
          : "bg-m3-surface text-slate-400 border border-m3-border hover:border-m3-border-glow hover:text-slate-300"
      }`}
    >
      {label}
    </button>
  );
}
