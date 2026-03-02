/* ── useViewport — Shared scroll + zoom state for LayeredScope ─────────
 *  Single source of truth for viewport position (scroll) and scale
 *  (windowDuration). Both WebGL (PeakScene.useFrame) and Canvas 2D
 *  (FlowOverlay rAF) read from these refs every frame.
 *
 *  PeakScene calls tick() once per frame to drive smooth lerp.
 *  ──────────────────────────────────────────────────────────────────── */

import { useRef, useCallback } from "react";

/* ── Constants ───────────────────────────────────────────────────────── */

export const MIN_WINDOW = 2;          // seconds — max zoom in
export const INITIAL_WINDOW = 12;     // seconds — default
export const PLAYHEAD_ANCHOR = 0.7;   // playhead at 70% from left
export const SCROLL_LERP = 0.12;
export const ZOOM_LERP = 0.10;
export const LEFT_STRIP_W = 54;       // piano roll width (px)

/* ── Types ───────────────────────────────────────────────────────────── */

export interface ViewportState {
  /** Current (lerped) scroll position in seconds */
  scrollRef: React.MutableRefObject<number>;
  /** Target scroll position */
  targetScrollRef: React.MutableRefObject<number>;
  /** Current (lerped) visible window duration in seconds */
  windowRef: React.MutableRefObject<number>;
  /** Target window duration */
  targetWindowRef: React.MutableRefObject<number>;

  /** Called by PeakScene.useFrame every frame to drive lerp + auto-follow */
  tick: (isPlaying: boolean, currentTime: number) => void;
  /** Wheel event: plain = pan, ctrl/meta = anchor zoom */
  handleWheel: (e: WheelEvent | React.WheelEvent, mouseXFrac: number) => void;
  /** Navigator click: jump scope center to this time fraction */
  handleNavigatorSeek: (timeFrac: number) => void;
  /** Navigator drag: set scroll directly (fraction of duration) */
  handleNavigatorDrag: (scrollFrac: number) => void;
  /** Click-to-seek on scope canvas (fraction of visible width) */
  handleScopeSeek: (xFrac: number) => number;
}

/* ── Hook ────────────────────────────────────────────────────────────── */

export function useViewport(duration: number) {
  const scrollRef = useRef(0);
  const targetScrollRef = useRef(0);
  const windowRef = useRef(INITIAL_WINDOW);
  const targetWindowRef = useRef(INITIAL_WINDOW);

  const clamp = (v: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, v));

  const maxWindow = Math.max(INITIAL_WINDOW, duration);

  /* ── tick: called every frame by PeakScene.useFrame ─────────── */
  const tick = useCallback((isPlaying: boolean, currentTime: number) => {
    // Window lerp (zoom animation)
    windowRef.current += (targetWindowRef.current - windowRef.current) * ZOOM_LERP;

    // Auto-follow playhead when playing
    if (isPlaying) {
      const anchor = PLAYHEAD_ANCHOR;
      const target = currentTime - windowRef.current * anchor;
      const maxS = Math.max(0, duration - windowRef.current);
      targetScrollRef.current = clamp(target, 0, maxS);
    }

    // Scroll lerp
    scrollRef.current += (targetScrollRef.current - scrollRef.current) * SCROLL_LERP;

    // Clamp scroll
    const maxS = Math.max(0, duration - windowRef.current);
    scrollRef.current = clamp(scrollRef.current, 0, maxS);
  }, [duration]);

  /* ── handleWheel: pan or zoom ──────────────────────────────── */
  const handleWheel = useCallback((e: WheelEvent | React.WheelEvent, mouseXFrac: number) => {
    e.preventDefault();

    if (e.ctrlKey || e.metaKey) {
      // ZOOM — anchor at mouse position
      const currentScroll = targetScrollRef.current;
      const currentWindow = targetWindowRef.current;
      const zoomAt = currentScroll + mouseXFrac * currentWindow;
      const factor = 1 + e.deltaY * 0.003;
      const newWindow = clamp(currentWindow * factor, MIN_WINDOW, maxWindow);
      targetWindowRef.current = newWindow;
      const maxS = Math.max(0, duration - newWindow);
      targetScrollRef.current = clamp(zoomAt - mouseXFrac * newWindow, 0, maxS);
    } else {
      // PAN — horizontal scroll
      const panSpeed = 0.004 * targetWindowRef.current;
      const delta = (e.deltaX || e.deltaY) * panSpeed;
      const maxS = Math.max(0, duration - targetWindowRef.current);
      targetScrollRef.current = clamp(targetScrollRef.current + delta, 0, maxS);
    }
  }, [duration, maxWindow]);

  /* ── Navigator interactions ────────────────────────────────── */
  const handleNavigatorSeek = useCallback((timeFrac: number) => {
    const time = timeFrac * duration;
    const maxS = Math.max(0, duration - targetWindowRef.current);
    targetScrollRef.current = clamp(time - targetWindowRef.current / 2, 0, maxS);
  }, [duration]);

  const handleNavigatorDrag = useCallback((scrollFrac: number) => {
    const maxS = Math.max(0, duration - targetWindowRef.current);
    targetScrollRef.current = clamp(scrollFrac * duration, 0, maxS);
  }, [duration]);

  /* ── Scope click-to-seek: returns time in seconds ──────────── */
  const handleScopeSeek = useCallback((xFrac: number): number => {
    return scrollRef.current + xFrac * windowRef.current;
  }, []);

  return {
    scrollRef,
    targetScrollRef,
    windowRef,
    targetWindowRef,
    tick,
    handleWheel,
    handleNavigatorSeek,
    handleNavigatorDrag,
    handleScopeSeek,
  } satisfies ViewportState;
}
