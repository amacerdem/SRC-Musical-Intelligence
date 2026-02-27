/* ── MindVisualizer — React wrapper for MindVisualizerEngine ──────── */

import { useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { MindVisualizerEngine } from "@/canvas/mind-visualizer";
import { useM3AudioStore } from "@/stores/useM3AudioStore";

const ease = [0.22, 1, 0.36, 1] as const;

interface Props {
  accentColor: string;
}

export function MindVisualizer({ accentColor }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const engineRef = useRef<MindVisualizerEngine | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Initialize engine
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const engine = new MindVisualizerEngine(canvas, { accentColor });
    engineRef.current = engine;
    engine.start();

    return () => {
      engine.dispose();
      engineRef.current = null;
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Update accent color
  useEffect(() => {
    engineRef.current?.updateAccentColor(accentColor);
  }, [accentColor]);

  // Feed vizParams from store to engine every frame
  useEffect(() => {
    let running = true;
    const tick = () => {
      if (!running) return;
      const params = useM3AudioStore.getState().vizParams;
      engineRef.current?.updateParams(params);
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    return () => { running = false; };
  }, []);

  // Resize canvas to container
  useEffect(() => {
    const container = containerRef.current;
    const canvas = canvasRef.current;
    if (!container || !canvas) return;

    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        const dpr = window.devicePixelRatio || 1;
        canvas.width = width * dpr;
        canvas.height = height * dpr;
        canvas.style.width = `${width}px`;
        canvas.style.height = `${height}px`;
        const ctx = canvas.getContext("2d");
        ctx?.scale(dpr, dpr);
      }
    });
    ro.observe(container);
    return () => ro.disconnect();
  }, []);

  return (
    <motion.div
      ref={containerRef}
      initial={{ opacity: 0, scale: 0.8, filter: "blur(20px)" }}
      animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
      exit={{ opacity: 0, scale: 0.8, filter: "blur(20px)" }}
      transition={{ duration: 0.8, ease }}
      className="w-full h-full relative"
    >
      <canvas
        ref={canvasRef}
        className="w-full h-full"
      />
    </motion.div>
  );
}
