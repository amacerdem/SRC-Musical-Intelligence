import { useRef, useEffect, useImperativeHandle, forwardRef } from "react";
import { MindOrganism, type OrganismConfig, type OrganismVariant, type FamilyMorphology } from "@/canvas/mind-organism";

export interface OrganismHandle {
  highlightBelief: (index: number, strength?: number) => void;
  pulse: (strength?: number) => void;
  updateConfig: (partial: Partial<OrganismConfig>) => void;
}

interface Props {
  color?: string;
  secondaryColor?: string;
  stage?: 1 | 2 | 3;
  intensity?: number;
  breathRate?: number;
  particleCount?: number; // legacy — maps to intensity
  variant?: OrganismVariant;
  beliefWeights?: number[];
  constellations?: boolean;
  frozen?: boolean;
  className?: string;
  interactive?: boolean;
  familyMorphology?: FamilyMorphology;
  tendrilCount?: number;
  nucleiCount?: number;
}

export const MindOrganismCanvas = forwardRef<OrganismHandle, Props>(
  function MindOrganismCanvas(
    {
      color = "#A855F7",
      secondaryColor,
      stage = 1,
      intensity,
      breathRate,
      particleCount,
      variant = "hero",
      beliefWeights,
      constellations,
      frozen,
      className = "",
      interactive = true,
      familyMorphology,
      tendrilCount,
      nucleiCount,
    },
    ref
  ) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const organismRef = useRef<MindOrganism | null>(null);

    const resolvedIntensity =
      intensity ?? (particleCount ? Math.min(1, particleCount / 100) : 0.7);

    // Expose imperative handle
    useImperativeHandle(ref, () => ({
      highlightBelief(index: number, strength = 1) {
        organismRef.current?.highlightBelief(index, strength);
      },
      pulse(strength = 1) {
        organismRef.current?.pulse(strength);
      },
      updateConfig(partial: Partial<OrganismConfig>) {
        organismRef.current?.updateConfig(partial);
      },
    }));

    // Mount: create organism once
    useEffect(() => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const parent = canvas.parentElement;
      if (!parent) return;

      const resize = () => {
        const w = parent.clientWidth;
        const h = parent.clientHeight;
        canvas.style.width = w + "px";
        canvas.style.height = h + "px";
        canvas.width = w;
        canvas.height = h;
      };
      resize();

      const config: Partial<OrganismConfig> = {
        color,
        stage,
        intensity: resolvedIntensity,
        responsive: interactive,
        variant,
        constellations,
        frozen,
      };
      if (secondaryColor) config.secondaryColor = secondaryColor;
      if (breathRate) config.breathRate = breathRate;
      if (beliefWeights) config.beliefWeights = beliefWeights;
      if (familyMorphology) config.familyMorphology = familyMorphology;
      if (tendrilCount) config.tendrilCount = tendrilCount;
      if (nucleiCount) config.nucleiCount = nucleiCount;

      const organism = new MindOrganism(canvas, config);
      organismRef.current = organism;
      organism.start();

      const ro = new ResizeObserver(resize);
      ro.observe(parent);

      return () => {
        organism.stop();
        organismRef.current = null;
        ro.disconnect();
      };
      // Mount only — dynamic updates handled by next effect
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // Update: push config changes without recreating
    useEffect(() => {
      organismRef.current?.updateConfig({
        color,
        secondaryColor,
        stage,
        intensity: resolvedIntensity,
        breathRate: breathRate ?? 4,
        responsive: interactive,
        variant,
        beliefWeights,
        constellations,
        frozen,
        familyMorphology,
        tendrilCount,
        nucleiCount,
      });
    }, [
      color,
      secondaryColor,
      stage,
      resolvedIntensity,
      breathRate,
      interactive,
      variant,
      beliefWeights,
      constellations,
      frozen,
      familyMorphology,
      tendrilCount,
      nucleiCount,
    ]);

    return (
      <div className={`relative ${className}`}>
        <canvas ref={canvasRef} className="absolute inset-0" />
      </div>
    );
  }
);
