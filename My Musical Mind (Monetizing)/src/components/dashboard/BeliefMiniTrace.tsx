import { useRef, useEffect, useState } from "react";
import { beliefColors } from "@/design/tokens";

const beliefs = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;

interface Props {
  height?: number;
}

export function BeliefMiniTrace({ height = 120 }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef(0);
  const [width, setWidth] = useState(400);

  // Observe container width changes
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const w = Math.floor(entry.contentRect.width);
        if (w > 0) setWidth(w);
      }
    });
    ro.observe(container);
    return () => ro.disconnect();
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d")!;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + "px";
    canvas.style.height = height + "px";
    ctx.scale(dpr, dpr);

    let time = 0;

    const draw = () => {
      time += 0.015;
      ctx.clearRect(0, 0, width, height);

      beliefs.forEach((b, i) => {
        const colors = beliefColors[b];
        ctx.beginPath();
        ctx.strokeStyle = colors.primary;
        ctx.globalAlpha = 0.5;
        ctx.lineWidth = 1.2;

        const yBase = height * 0.2 + (i * height * 0.15);
        const freq = 1.5 + i * 0.4;
        const amp = 4 + i * 1.5;
        const phase = i * 1.2;

        for (let x = 0; x < width; x++) {
          const t = x / width;
          const y =
            yBase +
            Math.sin(t * freq * Math.PI * 2 + time * 2 + phase) * amp +
            Math.sin(t * freq * 1.7 * Math.PI * 2 + time * 1.3 + phase * 0.5) * amp * 0.4;

          x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.stroke();
      });

      ctx.globalAlpha = 1;
      animRef.current = requestAnimationFrame(draw);
    };

    animRef.current = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(animRef.current);
  }, [width, height]);

  return (
    <div ref={containerRef} className="w-full">
      <canvas ref={canvasRef} className="opacity-70" />
    </div>
  );
}
