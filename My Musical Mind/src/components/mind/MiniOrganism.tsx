import { useRef, useEffect, useState } from "react";
import { MindOrganism, type OrganismConfig } from "@/canvas/mind-organism";

interface Props {
  color: string;
  stage?: 1 | 2 | 3;
  size?: number;
  animated?: boolean; // if true, runs animation loop (default: frozen frame)
  className?: string;
}

/**
 * Card/avatar-sized organism. Renders a single frozen frame to a static image,
 * then uses CSS animation for breathing effect. Only activates canvas loop
 * when `animated` is true (e.g. on hover).
 */
export function MiniOrganism({
  color,
  stage = 1,
  size = 48,
  animated = false,
  className = "",
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const organismRef = useRef<MindOrganism | null>(null);
  const [staticFrame, setStaticFrame] = useState<string | null>(null);

  // Render frozen frame on mount
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    canvas.width = size * 2; // 2x for retina
    canvas.height = size * 2;
    canvas.style.width = size + "px";
    canvas.style.height = size + "px";

    const config: Partial<OrganismConfig> = {
      color,
      stage,
      intensity: 0.8,
      breathRate: 4,
      responsive: false,
      variant: "micro",
      frozen: true,
    };

    const organism = new MindOrganism(canvas, config);
    organismRef.current = organism;
    organism.start(); // renders single frame due to frozen: true

    // Capture as static image
    setStaticFrame(canvas.toDataURL());

    return () => {
      organism.stop();
      organismRef.current = null;
    };
  }, [color, stage, size]);

  // If animated, run canvas loop instead of static image
  useEffect(() => {
    if (!animated || !organismRef.current) return;
    organismRef.current.updateConfig({ frozen: false });
    organismRef.current.start();
    return () => {
      organismRef.current?.updateConfig({ frozen: true });
      organismRef.current?.stop();
    };
  }, [animated]);

  return (
    <div
      className={`relative ${className}`}
      style={{ width: size, height: size }}
    >
      {/* Hidden canvas for rendering */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0"
        style={{
          opacity: animated ? 1 : 0,
          pointerEvents: "none",
        }}
      />

      {/* Static frozen frame with CSS breathing */}
      {staticFrame && !animated && (
        <img
          src={staticFrame}
          alt=""
          className="absolute inset-0 w-full h-full animate-breathe"
          style={{ pointerEvents: "none" }}
        />
      )}
    </div>
  );
}
