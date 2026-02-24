import { NeuralFamily } from "@/types/mind";
import type { M3Temperament, M3TrackSignal } from "@/types/m3";

export interface MockTrack {
    id: string;
    name: string;
    artist: string;
    albumArt: string;
    features: {
        energy: number;              // 0-1
        valence: number;             // 0-1 (Happy/Sad)
        tempo: number;               // BPM
        danceability: number;        // 0-1
        acousticness: number;        // 0-1
        harmonicComplexity: number;  // 0-1 (M³)
        timbralBrightness: number;   // 0-1 (M³)
    };
    dominantFamily: NeuralFamily;
    genre: string;
    durationSec: number;
}

const MOCK_TRACKS: MockTrack[] = [
    {
        id: "t1", name: "Cornfield Chase", artist: "Hans Zimmer",
        albumArt: "/covers/interstellar.jpg",
        features: { energy: 0.4, valence: 0.1, tempo: 96, danceability: 0.1, acousticness: 0.8, harmonicComplexity: 0.7, timbralBrightness: 0.3 },
        dominantFamily: "Architects", genre: "Cinematic", durationSec: 302,
    },
    {
        id: "t2", name: "Bangarang", artist: "Skrillex",
        albumArt: "/covers/bangarang.jpg",
        features: { energy: 0.95, valence: 0.7, tempo: 110, danceability: 0.8, acousticness: 0.01, harmonicComplexity: 0.3, timbralBrightness: 0.9 },
        dominantFamily: "Kineticists", genre: "Electronic", durationSec: 209,
    },
    {
        id: "t3", name: "Girl with the Tattoo", artist: "Miguel",
        albumArt: "/covers/miguel.jpg",
        features: { energy: 0.6, valence: 0.4, tempo: 120, danceability: 0.6, acousticness: 0.3, harmonicComplexity: 0.5, timbralBrightness: 0.5 },
        dominantFamily: "Anchors", genre: "R&B", durationSec: 260,
    },
    {
        id: "t4", name: "Windowlicker", artist: "Aphex Twin",
        albumArt: "/covers/windowlicker.jpg",
        features: { energy: 0.8, valence: 0.5, tempo: 127, danceability: 0.7, acousticness: 0.1, harmonicComplexity: 0.8, timbralBrightness: 0.7 },
        dominantFamily: "Explorers", genre: "IDM", durationSec: 370,
    },
    {
        id: "t5", name: "On the Nature of Daylight", artist: "Max Richter",
        albumArt: "/covers/blue_notebooks.jpg",
        features: { energy: 0.2, valence: 0.05, tempo: 60, danceability: 0.1, acousticness: 0.9, harmonicComplexity: 0.6, timbralBrightness: 0.2 },
        dominantFamily: "Alchemists", genre: "Neo-Classical", durationSec: 362,
    },
    {
        id: "t6", name: "Teardrop", artist: "Massive Attack",
        albumArt: "/covers/mezzanine.jpg",
        features: { energy: 0.5, valence: 0.3, tempo: 77, danceability: 0.4, acousticness: 0.3, harmonicComplexity: 0.6, timbralBrightness: 0.4 },
        dominantFamily: "Alchemists", genre: "Trip-Hop", durationSec: 324,
    },
    {
        id: "t7", name: "Strobe", artist: "Deadmau5",
        albumArt: "/covers/strobe.jpg",
        features: { energy: 0.7, valence: 0.6, tempo: 128, danceability: 0.75, acousticness: 0.05, harmonicComplexity: 0.4, timbralBrightness: 0.6 },
        dominantFamily: "Kineticists", genre: "Progressive House", durationSec: 622,
    },
    {
        id: "t8", name: "Everything In Its Right Place", artist: "Radiohead",
        albumArt: "/covers/kid_a.jpg",
        features: { energy: 0.45, valence: 0.2, tempo: 100, danceability: 0.3, acousticness: 0.4, harmonicComplexity: 0.85, timbralBrightness: 0.35 },
        dominantFamily: "Architects", genre: "Art Rock", durationSec: 251,
    },
    {
        id: "t9", name: "Holocene", artist: "Bon Iver",
        albumArt: "/covers/holocene.jpg",
        features: { energy: 0.35, valence: 0.25, tempo: 108, danceability: 0.2, acousticness: 0.75, harmonicComplexity: 0.55, timbralBrightness: 0.3 },
        dominantFamily: "Anchors", genre: "Indie Folk", durationSec: 337,
    },
    {
        id: "t10", name: "Workinonit", artist: "J Dilla",
        albumArt: "/covers/donuts.jpg",
        features: { energy: 0.65, valence: 0.55, tempo: 86, danceability: 0.85, acousticness: 0.2, harmonicComplexity: 0.45, timbralBrightness: 0.5 },
        dominantFamily: "Kineticists", genre: "Hip-Hop", durationSec: 112,
    },
    {
        id: "t11", name: "Svefn-g-englar", artist: "Sigur Rós",
        albumArt: "/covers/agaetis.jpg",
        features: { energy: 0.3, valence: 0.15, tempo: 72, danceability: 0.1, acousticness: 0.6, harmonicComplexity: 0.75, timbralBrightness: 0.25 },
        dominantFamily: "Anchors", genre: "Post-Rock", durationSec: 600,
    },
    {
        id: "t12", name: "Acid Rain", artist: "Chance The Rapper",
        albumArt: "/covers/acid_rap.jpg",
        features: { energy: 0.55, valence: 0.45, tempo: 92, danceability: 0.5, acousticness: 0.35, harmonicComplexity: 0.5, timbralBrightness: 0.45 },
        dominantFamily: "Explorers", genre: "Hip-Hop", durationSec: 200,
    },
    {
        id: "t13", name: "Reckoner", artist: "Radiohead",
        albumArt: "/covers/in_rainbows.jpg",
        features: { energy: 0.5, valence: 0.35, tempo: 130, danceability: 0.35, acousticness: 0.55, harmonicComplexity: 0.9, timbralBrightness: 0.4 },
        dominantFamily: "Architects", genre: "Art Rock", durationSec: 290,
    },
    {
        id: "t14", name: "Untitled 07", artist: "Kendrick Lamar",
        albumArt: "/covers/untitled.jpg",
        features: { energy: 0.75, valence: 0.3, tempo: 140, danceability: 0.65, acousticness: 0.15, harmonicComplexity: 0.65, timbralBrightness: 0.6 },
        dominantFamily: "Explorers", genre: "Experimental Hip-Hop", durationSec: 480,
    },
    {
        id: "t15", name: "Flim", artist: "Aphex Twin",
        albumArt: "/covers/come_to_daddy.jpg",
        features: { energy: 0.25, valence: 0.6, tempo: 98, danceability: 0.3, acousticness: 0.2, harmonicComplexity: 0.7, timbralBrightness: 0.55 },
        dominantFamily: "Explorers", genre: "IDM", durationSec: 172,
    },
];

/** Pick a random track from the pool */
function pickRandom(): MockTrack {
    return MOCK_TRACKS[Math.floor(Math.random() * MOCK_TRACKS.length)];
}

/**
 * Determine birth temperament from a batch of tracks.
 * Analyzes genre diversity, repeat ratio, tempo variance,
 * harmonic complexity, and valence range.
 */
export function calculateTemperament(tracks: MockTrack[]): M3Temperament {
    if (tracks.length === 0) return "explorer";

    const genres = new Set(tracks.map(t => t.genre));
    const genreDiversity = genres.size / tracks.length; // 0-1

    // Repeat ratio (how many duplicates)
    const ids = tracks.map(t => t.id);
    const uniqueIds = new Set(ids);
    const repeatRatio = 1 - (uniqueIds.size / ids.length);

    // Tempo variance
    const tempos = tracks.map(t => t.features.tempo);
    const tempoMean = tempos.reduce((s, v) => s + v, 0) / tempos.length;
    const tempoVar = tempos.reduce((s, v) => s + (v - tempoMean) ** 2, 0) / tempos.length;
    const tempoStd = Math.sqrt(tempoVar);

    // Harmonic complexity mean
    const harmMean = tracks.reduce((s, t) => s + t.features.harmonicComplexity, 0) / tracks.length;

    // Valence range
    const valences = tracks.map(t => t.features.valence);
    const valRange = Math.max(...valences) - Math.min(...valences);

    // Score each temperament
    const scores: Record<M3Temperament, number> = {
        explorer: genreDiversity * 2 + (1 - repeatRatio),
        deep_diver: repeatRatio * 2 + (1 - genreDiversity),
        rhythmic: tempoStd / 30 + tracks.reduce((s, t) => s + t.features.danceability, 0) / tracks.length,
        harmonic: harmMean * 2,
        emotive: valRange * 2 + tracks.reduce((s, t) => s + Math.abs(t.features.valence - 0.5), 0) / tracks.length,
    };

    // Return highest scoring
    let best: M3Temperament = "explorer";
    let bestScore = -1;
    for (const [key, score] of Object.entries(scores)) {
        if (score > bestScore) {
            bestScore = score;
            best = key as M3Temperament;
        }
    }
    return best;
}

/**
 * Convert a MockTrack to an M3TrackSignal for feeding M³.
 */
export function trackToM3Signal(track: MockTrack, opts?: { isRepeat?: boolean; wasSkipped?: boolean }): M3TrackSignal {
    return {
        energy: track.features.energy,
        valence: track.features.valence,
        tempo: track.features.tempo,
        danceability: track.features.danceability,
        acousticness: track.features.acousticness,
        harmonicComplexity: track.features.harmonicComplexity,
        timbralBrightness: track.features.timbralBrightness,
        duration: track.durationSec,
        isRepeat: opts?.isRepeat ?? false,
        wasSkipped: opts?.wasSkipped ?? false,
    };
}

export const SpotifySimulator = {
    /** Simulates getting the currently playing track */
    getCurrentTrack: (): Promise<MockTrack> => {
        return new Promise((resolve) => {
            setTimeout(() => resolve(pickRandom()), 500);
        });
    },

    /** Simulates a stream of listening history (for populating the garden) */
    getRecentHistory: (): MockTrack[] => {
        return Array.from({ length: 5 }, () => pickRandom());
    },

    /** Simulates a full listening session (5-10 tracks with timestamps) for M³ growth */
    getListeningSession: (): { track: MockTrack; listenedAt: string; wasSkipped: boolean }[] => {
        const count = 5 + Math.floor(Math.random() * 6); // 5-10
        const now = Date.now();
        return Array.from({ length: count }, (_, i) => {
            const track = pickRandom();
            const wasSkipped = Math.random() < 0.15; // 15% skip rate
            return {
                track,
                listenedAt: new Date(now - (count - i) * 4 * 60 * 1000).toISOString(), // ~4min apart
                wasSkipped,
            };
        });
    },

    /** Get the full track pool (for temperament calculation at birth) */
    getInitialBatch: (): MockTrack[] => {
        // Simulate importing the user's first 15-20 listened tracks
        const count = 15 + Math.floor(Math.random() * 6);
        return Array.from({ length: count }, () => pickRandom());
    },
};
