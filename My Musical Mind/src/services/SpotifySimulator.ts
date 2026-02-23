import { NeuralFamily } from "@/types/mind";

export interface MockTrack {
    id: string;
    name: string;
    artist: string;
    albumArt: string;
    features: {
        energy: number;   // 0-1
        valence: number;  // 0-1 (Happy/Sad)
        tempo: number;    // BPM
        danceability: number;
        acousticness: number;
    };
    dominantFamily: NeuralFamily; // Pre-calculated for demo
}

const MOCK_TRACKS: MockTrack[] = [
    {
        id: "t1",
        name: "Cornfield Chase",
        artist: "Hans Zimmer",
        albumArt: "/covers/interstellar.jpg",
        features: { energy: 0.4, valence: 0.1, tempo: 96, danceability: 0.1, acousticness: 0.8 },
        dominantFamily: "Architects"
    },
    {
        id: "t2",
        name: "Bangarang",
        artist: "Skrillex",
        albumArt: "/covers/bangarang.jpg",
        features: { energy: 0.95, valence: 0.7, tempo: 110, danceability: 0.8, acousticness: 0.01 },
        dominantFamily: "Kineticists"
    },
    {
        id: "t3",
        name: "Girl with the Tattoo",
        artist: "Miguel",
        albumArt: "/covers/miguel.jpg",
        features: { energy: 0.6, valence: 0.4, tempo: 120, danceability: 0.6, acousticness: 0.3 },
        dominantFamily: "Anchors" // Emotional connection
    },
    {
        id: "t4",
        name: "Windowlicker",
        artist: "Aphex Twin",
        albumArt: "/covers/windowlicker.jpg",
        features: { energy: 0.8, valence: 0.5, tempo: 127, danceability: 0.7, acousticness: 0.1 },
        dominantFamily: "Explorers" // Glitch/Novelty
    },
    {
        id: "t5",
        name: "On the Nature of Daylight",
        artist: "Max Richter",
        albumArt: "/covers/blue_notebooks.jpg",
        features: { energy: 0.2, valence: 0.05, tempo: 60, danceability: 0.1, acousticness: 0.9 },
        dominantFamily: "Alchemists" // Pure emotional transformation
    }
];

export const SpotifySimulator = {
    /** Simulates getting the currently playing track */
    getCurrentTrack: (): Promise<MockTrack> => {
        return new Promise((resolve) => {
            // Return a random track with a slight network delay simulation
            setTimeout(() => {
                const randomTrack = MOCK_TRACKS[Math.floor(Math.random() * MOCK_TRACKS.length)];
                resolve(randomTrack);
            }, 500);
        });
    },

    /** Simulates a stream of listening history (for populating the garden) */
    getRecentHistory: (): MockTrack[] => {
        // Return 5 random tracks
        return Array.from({ length: 5 }).map(() => MOCK_TRACKS[Math.floor(Math.random() * MOCK_TRACKS.length)]);
    }
};
