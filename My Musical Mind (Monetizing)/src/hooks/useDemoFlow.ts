/* ── useDemoFlow — Smooth 6D jitter for demo motion ──────────────────
 *  Produces periodically jittered target values around the user's
 *  static total. Targets are generated every INTERVAL ms; Framer
 *  Motion's spring/tween in the radar component handles 60fps
 *  interpolation between them (its internal rAF loop).
 *
 *  Key: transition duration in DashboardRadar must be ≈ INTERVAL
 *  so the animation is continuously in motion with no pauses.
 *  ──────────────────────────────────────────────────────────────────── */

import { useState, useEffect, useRef } from "react";

/** Target generation interval — DashboardRadar transition must match */
export const FLOW_INTERVAL_MS = 1200;

/**
 * @param total  6 static values [0-1] — user's aggregate 6D profile
 * @param active whether to animate (true when music is playing)
 * @returns 6 current target values [0-1], updated every FLOW_INTERVAL_MS
 */
export function useDemoFlow(total: number[], active: boolean): number[] {
  const [flow, setFlow] = useState(total);
  const totalRef = useRef(total);
  totalRef.current = total;

  useEffect(() => {
    if (!active) {
      setFlow(totalRef.current);
      return;
    }

    const jitter = () => {
      setFlow(
        totalRef.current.map((v) =>
          Math.max(0.05, Math.min(0.98, v + (Math.random() - 0.5) * 0.25)),
        ),
      );
    };

    jitter();
    const id = setInterval(jitter, FLOW_INTERVAL_MS);
    return () => clearInterval(id);
  }, [active]);

  return flow;
}
