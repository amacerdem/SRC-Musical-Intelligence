import { useRef, useEffect } from "react";
import { MindOrganism, type OrganismConfig } from "@/canvas/mind-organism";
import { beliefColors } from "@/design/tokens";
import { NucleusDot } from "./NucleusDot";

type BeliefDomain = "consonance" | "tempo" | "salience" | "familiarity" | "reward";

interface Props {
  value: number; // 0-100
  color?: string;
  beliefDomain?: BeliefDomain;
  height?: number;
  showDots?: boolean;
  className?: string;
}

/**
 * Progress bar with organism-derived trace waves inside.
 * Uses the trace variant canvas for the filled portion.
 */
export function OrganismProgress({
  value,
  color,
  beliefDomain,
  height = 4,
  showDots = false,
  className = "",
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const organismRef = useRef<MindOrganism | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const resolvedColor = color
    ?? (beliefDomain ? beliefColors[beliefDomain].primary : "#A855F7");
  const clampedValue = Math.max(0, Math.min(100, value));

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const w = container.clientWidth;
    const h = height * 3; // extra height for wave amplitude
    canvas.width = w;
    canvas.height = h;
    canvas.style.width = w + "px";
    canvas.style.height = h + "px";

    const config: Partial<OrganismConfig> = {
      color: resolvedColor,
      stage: 1,
      intensity: 0.8,
      breathRate: 3,
      responsive: false,
      variant: "trace",
    };

    const organism = new MindOrganism(canvas, config);
    organismRef.current = organism;
    organism.start();

    return () => {
      organism.stop();
      organismRef.current = null;
    };
  }, [resolvedColor, height]);

  return (
    <div className={`relative ${className}`} ref={containerRef}>
      {/* Track */}
      <div
        className="w-full rounded-full overflow-hidden"
        style={{
          height,
          background: "rgba(255,255,255,0.04)",
        }}
      >
        {/* Filled portion with trace canvas */}
        <div
          className="h-full rounded-full overflow-hidden transition-[width] duration-700 ease-out relative"
          style={{ width: `${clampedValue}%` }}
        >
          {/* Canvas waves */}
          <canvas
            ref={canvasRef}
            className="absolute left-0"
            style={{
              top: -(height),
              height: height * 3,
              pointerEvents: "none",
            }}
          />

          {/* Fallback gradient fill (visible immediately) */}
          <div
            className="absolute inset-0 rounded-full"
            style={{
              background: `linear-gradient(90deg, ${resolvedColor}60, ${resolvedColor})`,
            }}
          />
        </div>
      </div>

      {/* Optional milestone dots */}
      {showDots && (
        <div className="absolute inset-0 flex items-center justify-between px-1 pointer-events-none">
          {[25, 50, 75].map((milestone) => (
            <div
              key={milestone}
              className="absolute"
              style={{ left: `${milestone}%`, transform: "translateX(-50%)" }}
            >
              <NucleusDot
                color={resolvedColor}
                size={3}
                active={clampedValue >= milestone}
                pulsing={clampedValue >= milestone}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
