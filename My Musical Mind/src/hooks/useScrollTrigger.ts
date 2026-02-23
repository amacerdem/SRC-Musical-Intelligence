import { useEffect, useRef, type RefObject } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

interface ScrollTriggerOptions {
  trigger?: RefObject<HTMLElement | null>;
  start?: string;
  end?: string;
  scrub?: boolean | number;
  pin?: boolean;
  markers?: boolean;
  onEnter?: () => void;
  onLeave?: () => void;
  onEnterBack?: () => void;
  onLeaveBack?: () => void;
}

/**
 * GSAP ScrollTrigger hook for React.
 * Returns a ref to attach to the trigger element.
 */
export function useScrollTrigger(
  animationCallback: (tl: gsap.core.Timeline, trigger: HTMLElement) => void,
  options: ScrollTriggerOptions = {},
  deps: unknown[] = []
) {
  const triggerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = options.trigger?.current ?? triggerRef.current;
    if (!el) return;

    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: el,
        start: options.start ?? "top 80%",
        end: options.end ?? "bottom 20%",
        scrub: options.scrub ?? false,
        pin: options.pin ?? false,
        markers: options.markers ?? false,
        onEnter: options.onEnter,
        onLeave: options.onLeave,
        onEnterBack: options.onEnterBack,
        onLeaveBack: options.onLeaveBack,
      },
    });

    animationCallback(tl, el);

    return () => {
      tl.scrollTrigger?.kill();
      tl.kill();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return triggerRef;
}

/**
 * Batch ScrollTrigger — staggered reveal for lists of elements.
 */
export function useScrollBatch(
  selector: string,
  containerRef: RefObject<HTMLElement | null>,
  options: { start?: string; stagger?: number } = {}
) {
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const elements = container.querySelectorAll(selector);
    if (!elements.length) return;

    gsap.set(elements, { opacity: 0, y: 40 });

    ScrollTrigger.batch(elements, {
      start: options.start ?? "top 85%",
      onEnter: (batch) =>
        gsap.to(batch, {
          opacity: 1,
          y: 0,
          duration: 0.8,
          stagger: options.stagger ?? 0.08,
          ease: "power3.out",
        }),
    });

    return () => {
      ScrollTrigger.getAll().forEach((st) => st.kill());
    };
  }, [selector, containerRef, options.start, options.stagger]);
}
