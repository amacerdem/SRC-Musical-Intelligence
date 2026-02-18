import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { FocusArtifact, RealContext, NeuralFamily } from '@/types/mind';
import { SpotifySimulator, type MockTrack } from '@/services/SpotifySimulator';
import { InstagramSimulator } from '@/services/InstagramSimulator';

interface ActiveQuest {
    id: string;
    title: string;
    description: string;
    type: 'ritual' | 'anomaly' | 'scavenger_hunt';
    status: 'active' | 'completed' | 'failed';
    progress: number; // 0-100
    targetFamily?: NeuralFamily;
    expiresAt: number;
}

interface MindGardenState {
    seedsPlanted: number;
    biodiversityScore: number; // 0-1
    dominantFamily: NeuralFamily | null;
    season: 'spring' | 'summer' | 'autumn' | 'winter';
    recentTracks: MockTrack[];
}

interface GamificationState {
    // Inventory
    artifacts: FocusArtifact[];
    resonanceCurrency: number; // Social currency
    neuralPlasticity: number;  // XP

    // Active Game State
    activeQuests: ActiveQuest[];
    mindGarden: MindGardenState;

    // Real World Context (Non-persisted)
    realContext: RealContext;

    // Actions
    addArtifact: (artifact: FocusArtifact) => void;
    updateRealContext: (ctx: Partial<RealContext>) => void;

    // Mock Integration Actions
    syncMockSpotify: () => Promise<void>;
    shareMockInstagram: (assetUrl: string) => Promise<void>;

    // Internal logic
    plantSeed: (family: NeuralFamily, track: MockTrack) => void;
    startQuest: (quest: ActiveQuest) => void;
    completeQuest: (questId: string) => void;
    addResonance: (amount: number) => void;
}

export const useGamificationStore = create<GamificationState>()(
    persist(
        (set, get) => ({
            artifacts: [],
            resonanceCurrency: 0,
            neuralPlasticity: 0,

            activeQuests: [],

            mindGarden: {
                seedsPlanted: 0,
                biodiversityScore: 0,
                dominantFamily: null,
                season: 'spring',
                recentTracks: []
            },

            realContext: {
                timeOfDay: 'day',
                weather: 'clear',
                activity: 'still',
                audioEnvironment: 'quiet'
            },

            addArtifact: (artifact) => set((state) => ({
                artifacts: [...state.artifacts, artifact]
            })),

            updateRealContext: (ctx) => set((state) => ({
                realContext: { ...state.realContext, ...ctx }
            })),

            syncMockSpotify: async () => {
                const track = await SpotifySimulator.getCurrentTrack();
                get().plantSeed(track.dominantFamily, track);
            },

            shareMockInstagram: async (assetUrl) => {
                const shareId = await InstagramSimulator.shareToStory(assetUrl);
                // Simulate waiting for engagement
                setTimeout(async () => {
                    const metrics = await InstagramSimulator.getMetrics(shareId);
                    get().addResonance(metrics.resonanceScore);
                }, 2000);
            },

            plantSeed: (family, track) => set((state) => {
                const newCount = state.mindGarden.seedsPlanted + 1;
                const seasons: MindGardenState['season'][] = ['spring', 'summer', 'autumn', 'winter'];
                const nextSeason = seasons[Math.floor((newCount / 5) % 4)]; // Faster seasons for demo

                return {
                    mindGarden: {
                        ...state.mindGarden,
                        seedsPlanted: newCount,
                        dominantFamily: family,
                        season: nextSeason,
                        recentTracks: [track, ...state.mindGarden.recentTracks].slice(0, 10)
                    },
                    neuralPlasticity: state.neuralPlasticity + 10
                };
            }),

            startQuest: (quest) => set((state) => ({
                activeQuests: [...state.activeQuests, quest]
            })),

            completeQuest: (questId) => set((state) => ({
                activeQuests: state.activeQuests.map(q =>
                    q.id === questId ? { ...q, status: 'completed', progress: 100 } : q
                ),
                neuralPlasticity: state.neuralPlasticity + 50,
                resonanceCurrency: state.resonanceCurrency + 10
            })),

            addResonance: (amount) => set((state) => ({
                resonanceCurrency: state.resonanceCurrency + amount
            })),
        }),
        {
            name: 'm3-gamification-storage',
            partialize: (state) => ({
                artifacts: state.artifacts,
                resonanceCurrency: state.resonanceCurrency,
                neuralPlasticity: state.neuralPlasticity,
                activeQuests: state.activeQuests,
                mindGarden: state.mindGarden
            }),
        }
    )
);
