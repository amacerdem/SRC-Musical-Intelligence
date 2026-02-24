/** Depth-based navigation state for the Neural Depth Navigator. */

import { create } from 'zustand';

export type DepthSegment =
  | { type: 'root' }
  | { type: 'r3' }
  | { type: 'h3' }
  | { type: 'c3' }
  | { type: 'output' }
  | { type: 'r3group'; key: string; name: string }
  | { type: 'h3horizon'; band: string }
  | { type: 'relay'; name: string }
  | { type: 'beliefs' }
  | { type: 'ram' }
  | { type: 'reward' }
  | { type: 'neuro' }
  | { type: 'feature'; index: number; name: string };

interface NavigationState {
  depthPath: DepthSegment[];
  currentDepth: number;
  isTransitioning: boolean;
  transitionDirection: 'in' | 'out' | 'none';

  navigateIn: (segment: DepthSegment) => void;
  navigateOut: () => void;
  navigateToRoot: () => void;
  setTransitioning: (v: boolean) => void;
}

export const useNavigationStore = create<NavigationState>((set) => ({
  depthPath: [{ type: 'root' }],
  currentDepth: 0,
  isTransitioning: false,
  transitionDirection: 'none',

  navigateIn: (segment) =>
    set((state) => {
      const newPath = [...state.depthPath, segment];
      return {
        depthPath: newPath,
        currentDepth: newPath.length - 1,
        isTransitioning: true,
        transitionDirection: 'in',
      };
    }),

  navigateOut: () =>
    set((state) => {
      if (state.depthPath.length <= 1) return state;
      const newPath = state.depthPath.slice(0, -1);
      return {
        depthPath: newPath,
        currentDepth: newPath.length - 1,
        isTransitioning: true,
        transitionDirection: 'out',
      };
    }),

  navigateToRoot: () =>
    set({
      depthPath: [{ type: 'root' }],
      currentDepth: 0,
      isTransitioning: true,
      transitionDirection: 'out',
    }),

  setTransitioning: (v) => set({ isTransitioning: v, transitionDirection: v ? undefined as any : 'none' }),
}));
