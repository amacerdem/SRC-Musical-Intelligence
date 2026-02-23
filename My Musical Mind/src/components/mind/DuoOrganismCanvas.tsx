/* ── Duo Organism Canvas — React wrapper ───────────────────────── */

import { useRef, useEffect, useImperativeHandle, forwardRef } from "react";
import { DuoOrganism, type AnalysisFrame } from "@/canvas/duo-organism";
import { DuoGameEngine, type GameEvent } from "@/game/duo-game-engine";

export interface DuoOrganismHandle {
  updateParams: (emo: number[], phys: number[]) => void;
  setAnalysisFrame: (frame: AnalysisFrame) => void;
  pulseRing: () => void;
  burst: (x: number, y: number, count: number, color?: { r: number; g: number; b: number }) => void;
  flash: () => void;
  floatXP: (x: number, y: number, text: string) => void;
  getGameState: () => ReturnType<DuoGameEngine["getState"]>;
}

interface Props {
  className?: string;
  /** Called when game events fire (achievements, task complete, etc.) */
  onGameEvent?: (events: GameEvent[]) => void;
}

const RESONANCE_COLOR = { r: 251, g: 191, b: 36 };

export const DuoOrganismCanvas = forwardRef<DuoOrganismHandle, Props>(
  function DuoOrganismCanvas({ className = "", onGameEvent }, ref) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const organismRef = useRef<DuoOrganism | null>(null);
    const engineRef = useRef<DuoGameEngine | null>(null);
    const emoRef = useRef([0.5, 0.5, 0.5, 0.5]);
    const physRef = useRef([0.5, 0.5, 0.5, 0.5]);
    const tickRef = useRef(0);

    useImperativeHandle(ref, () => ({
      updateParams(emo: number[], phys: number[]) {
        emoRef.current = emo;
        physRef.current = phys;
        organismRef.current?.updateParams(emo, phys);
      },
      setAnalysisFrame(frame: AnalysisFrame) {
        organismRef.current?.setAnalysisFrame(frame);
        // Also update refs for game engine resonance calculation
        emoRef.current = [frame.beliefs.consonance, frame.beliefs.salience, frame.beliefs.familiarity, frame.relays[3]];
        physRef.current = [frame.beliefs.tempo, frame.r3[1], frame.r3[3], frame.relays[0]];
      },
      pulseRing() {
        organismRef.current?.pulseRing();
      },
      burst(x, y, count, color) {
        organismRef.current?.burst(x, y, count, color ?? RESONANCE_COLOR);
      },
      flash() {
        organismRef.current?.flash();
      },
      floatXP(x, y, text) {
        organismRef.current?.floatXP(x, y, text, RESONANCE_COLOR);
      },
      getGameState() {
        return engineRef.current?.getState() ?? {
          score: 0, combo: 1, comboTimer: 0,
          achievements: new Set(), activeTask: null,
          completedTasks: [], events: [], sessionTime: 0,
          resonanceStreak: 0, paramHistory: [],
        };
      },
    }));

    useEffect(() => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const parent = canvas.parentElement;
      if (!parent) return;

      const organism = new DuoOrganism(canvas);
      const engine = new DuoGameEngine();
      organismRef.current = organism;
      engineRef.current = engine;

      const resize = () => {
        const w = parent.clientWidth;
        const h = parent.clientHeight;
        canvas.style.width = w + "px";
        canvas.style.height = h + "px";
        organism.resize(w, h);
      };
      resize();
      organism.start();

      // Game tick — runs alongside organism animation
      const gameLoop = () => {
        if (!organismRef.current) return;
        const dt = 1 / 60; // approximate
        const resonance = organism.getResonanceStrength();
        const events = engine.tick(dt, emoRef.current, physRef.current, resonance);

        // Trigger visual effects for game events
        for (const ev of events) {
          const w = canvas.clientWidth;
          const h = canvas.clientHeight;
          switch (ev.type) {
            case "achievement":
              organism.pulseRing(RESONANCE_COLOR, 1.2);
              organism.burst(w / 2, h / 2, 60, RESONANCE_COLOR);
              organism.flash({ r: 255, g: 255, b: 255 }, 0.2);
              if (ev.xp) organism.floatXP(w / 2, h * 0.4, `+${ev.xp} XP`, RESONANCE_COLOR);
              break;
            case "task_complete":
              organism.burst(w * 0.25, h * 0.75, 40, { r: 132, g: 204, b: 22 });
              organism.pulseRing({ r: 132, g: 204, b: 22 }, 0.8);
              if (ev.xp) organism.floatXP(w * 0.25, h * 0.7, `+${ev.xp} XP`, { r: 132, g: 204, b: 22 });
              break;
            case "combo_up":
              organism.flash(RESONANCE_COLOR, 0.1);
              break;
          }
        }

        if (events.length > 0) onGameEvent?.(events);
        tickRef.current = requestAnimationFrame(gameLoop);
      };
      tickRef.current = requestAnimationFrame(gameLoop);

      const ro = new ResizeObserver(resize);
      ro.observe(parent);

      return () => {
        organism.stop();
        organismRef.current = null;
        engineRef.current = null;
        cancelAnimationFrame(tickRef.current);
        ro.disconnect();
      };
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
      <div className={`relative w-full h-full ${className}`}>
        <canvas ref={canvasRef} className="absolute inset-0" />
      </div>
    );
  }
);
