import { useNavigationStore } from '../../stores/navigationStore';
import NeuralOverview from '../../views/NeuralOverview';
import R3LayerView from '../../views/R3LayerView';
import H3LayerView from '../../views/H3LayerView';
import C3LayerView from '../../views/C3LayerView';
import OutputLayerView from '../../views/OutputLayerView';
import FeatureDetailView from '../../views/FeatureDetailView';
import RelayDetailView from '../../views/RelayDetailView';
import RewardDetailView from '../../views/RewardDetailView';
import RamDetailView from '../../views/RamDetailView';
import NeuroDetailView from '../../views/NeuroDetailView';

export default function DepthRouter() {
  const { depthPath } = useNavigationStore();
  const current = depthPath[depthPath.length - 1];

  switch (current.type) {
    case 'root':
      return <NeuralOverview />;

    // Depth 1
    case 'r3':
      return <R3LayerView />;
    case 'h3':
      return <H3LayerView />;
    case 'c3':
      return <C3LayerView />;
    case 'output':
      return <OutputLayerView />;

    // Depth 2
    case 'r3group':
      return <FeatureDetailView groupKey={current.key} groupName={current.name} />;
    case 'relay':
      return <RelayDetailView relayName={current.name} />;
    case 'reward':
      return <RewardDetailView />;
    case 'ram':
      return <RamDetailView />;
    case 'neuro':
      return <NeuroDetailView />;
    case 'beliefs':
      return <C3LayerView initialTab="beliefs" />;
    case 'feature':
      return <FeatureDetailView featureIndex={current.index} featureName={current.name} />;

    default:
      return <NeuralOverview />;
  }
}
