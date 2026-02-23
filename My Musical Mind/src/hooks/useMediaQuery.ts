import { useState, useEffect } from "react";

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mql = window.matchMedia(query);
    setMatches(mql.matches);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mql.addEventListener("change", handler);
    return () => mql.removeEventListener("change", handler);
  }, [query]);

  return matches;
}

export const useMobile = () => useMediaQuery("(max-width: 768px)");
export const useTablet = () => useMediaQuery("(max-width: 1024px)");
export const useDesktop = () => useMediaQuery("(min-width: 1024px)");
export const useWidescreen = () => useMediaQuery("(min-width: 1536px)");
