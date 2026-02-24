import { type ReactNode, useEffect, useRef } from 'react';
import { useNavigationStore } from '../../stores/navigationStore';

interface Props {
  children: ReactNode;
}

export default function DepthTransition({ children }: Props) {
  const { isTransitioning, transitionDirection, setTransitioning } = useNavigationStore();
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isTransitioning) {
      const timer = setTimeout(() => setTransitioning(false), 500);
      return () => clearTimeout(timer);
    }
  }, [isTransitioning, setTransitioning]);

  const getAnimClass = () => {
    if (!isTransitioning) return 'depth-idle';
    return transitionDirection === 'in' ? 'depth-zoom-in' : 'depth-zoom-out';
  };

  return (
    <div ref={containerRef} className={`depth-transition ${getAnimClass()}`}>
      {children}
    </div>
  );
}
