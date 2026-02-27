import { useEffect, useRef } from "react";

export function useAnimationFrame(callback: (dt: number) => void) {
  const ref = useRef<number>(0);
  const prev = useRef<number>(0);

  useEffect(() => {
    const loop = (time: number) => {
      if (prev.current) {
        const dt = (time - prev.current) / 1000;
        callback(dt);
      }
      prev.current = time;
      ref.current = requestAnimationFrame(loop);
    };
    ref.current = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(ref.current);
  }, [callback]);
}
