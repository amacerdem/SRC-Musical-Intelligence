import { MiniOrganism } from "./MiniOrganism";
import { NucleusDot } from "./NucleusDot";
import { BELIEF_COLORS } from "@/canvas/mind-organism";

interface Props {
  progress?: number; // 0-100
  color: string;
  size?: number;
  className?: string;
}

const BELIEF_HEX = [
  "#C084FC", // consonance
  "#F97316", // tempo
  "#84CC16", // salience
  "#38BDF8", // familiarity
  "#FBBF24", // reward
];

/**
 * Loading indicator built from a MiniOrganism.
 * Stage progresses from 1 to 2 as progress increases.
 * Belief domain dots light up sequentially.
 */
export function OrganismLoader({
  progress = 0,
  color,
  size = 64,
  className = "",
}: Props) {
  const stage: 1 | 2 | 3 = progress > 70 ? 2 : 1;
  const activeDots = Math.floor((progress / 100) * 5);

  return (
    <div className={`flex flex-col items-center gap-3 ${className}`}>
      {/* Organism */}
      <div className="relative">
        <MiniOrganism
          color={color}
          stage={stage}
          size={size}
          animated={progress > 0}
        />

        {/* Progress text overlay */}
        {progress > 0 && (
          <div className="absolute inset-0 flex items-center justify-center">
            <span
              className="font-mono text-xs font-medium"
              style={{ color, textShadow: `0 0 8px ${color}60` }}
            >
              {Math.round(progress)}%
            </span>
          </div>
        )}
      </div>

      {/* Belief domain dots */}
      <div className="flex items-center gap-2">
        {BELIEF_HEX.map((bColor, i) => (
          <NucleusDot
            key={i}
            color={bColor}
            size={4}
            active={i < activeDots}
            pulsing={i === activeDots - 1}
            glow={i < activeDots}
          />
        ))}
      </div>
    </div>
  );
}
