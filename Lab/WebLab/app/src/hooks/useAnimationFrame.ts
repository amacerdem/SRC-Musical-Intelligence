import { useEffect, useRef } from "react";

/**
 * Calls `callback` on every animation frame while `active` is true.
 * The callback receives the current timestamp.
 */
export function useAnimationFrame(
  callback: (time: number) => void,
  active: boolean,
): void {
  const cbRef = useRef(callback);
  cbRef.current = callback;

  useEffect(() => {
    if (!active) return;
    let id = 0;
    const loop = (time: number) => {
      cbRef.current(time);
      id = requestAnimationFrame(loop);
    };
    id = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(id);
  }, [active]);
}
