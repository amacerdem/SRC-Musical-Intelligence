interface Props {
  src?: string;
  name: string;
  size?: number;
  borderColor?: string;
}

export function Avatar({ src, name, size = 40, borderColor }: Props) {
  const initials = name
    .split(" ")
    .map((w) => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <div
      className="rounded-full flex items-center justify-center font-display font-bold text-white shrink-0 overflow-hidden"
      style={{
        width: size,
        height: size,
        fontSize: size * 0.36,
        background: src ? undefined : "linear-gradient(135deg, #6366F1, #A855F7)",
        border: borderColor ? `2px solid ${borderColor}` : "2px solid #1E1E2E",
      }}
    >
      {src ? (
        <img src={src} alt={name} className="w-full h-full object-cover" />
      ) : (
        initials
      )}
    </div>
  );
}
