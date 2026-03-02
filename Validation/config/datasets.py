"""Dataset registry — URLs, sizes, licenses, and metadata for all validation datasets."""
from __future__ import annotations

DATASETS = {
    # ── V1: Pharmacology (hardcoded from literature) ──
    "pharmacology": {
        "description": "Published effect sizes from pharmacological music studies",
        "size_mb": 0.01,
        "license": "Published data (fair use)",
        "source": "Ferreri 2019, Mallik 2017, Laeng 2021",
        "download": "hardcoded",
    },

    # ── V2: IDyOM corpora ──
    "idyom_corpora": {
        "description": "Essen Folksong Collection + other melodic corpora",
        "urls": {
            "essen": "https://github.com/apmcleod/essen-folksong-collection",
        },
        "size_mb": 10,
        "license": "Public domain / research use",
        "download": "git_clone",
    },

    # ── V3: Krumhansl (hardcoded from publication) ──
    "krumhansl": {
        "description": "Krumhansl & Kessler 1982 tonal hierarchy profiles",
        "size_mb": 0.001,
        "license": "Published data (fair use)",
        "source": "Krumhansl & Kessler 1982, Cognitive Psychology",
        "download": "hardcoded",
    },

    # ── V4: DEAM ──
    "deam": {
        "description": "1,802 songs with 2Hz continuous valence/arousal annotations",
        "urls": {
            "annotations": "https://cvml.unige.ch/databases/DEAM/DEAM_Annotations.zip",
            "audio_45s": "https://cvml.unige.ch/databases/DEAM/DEAM_audio/MEMD_audio_wav_45s.zip",
        },
        "size_gb": 15.0,
        "license": "CC BY-NC-SA 4.0",
        "source": "Aljanaki et al. 2017, MediaEval",
        "download": "http",
        "annotation_hz": 2.0,
    },

    # ── V5: NMED-T (EEG) ──
    "nmed_t": {
        "description": "20 subjects, 128-ch EEG, tempo-varied naturalistic music",
        "url": "https://purl.stanford.edu/jn859kj8079",
        "size_gb": 39.0,
        "license": "Stanford Digital Repository DUA",
        "source": "Kaneshiro et al. 2020, Stanford",
        "download": "stanford_sdr",
        "n_subjects": 20,
        "eeg_channels": 128,
        "eeg_sfreq": 125.0,
    },

    # ── V6: OpenNeuro EEG-fMRI (affective music) ──
    "ds002725": {
        "description": "21 subjects, simultaneous EEG-fMRI, affective music listening",
        "url": "https://openneuro.org/datasets/ds002725",
        "size_gb": 25.0,
        "license": "CC0",
        "source": "OpenNeuro ds002725",
        "download": "openneuro",
        "n_subjects": 21,
        "tr_seconds": 2.0,
    },

    # ── V6: OpenNeuro genre fMRI ──
    "ds003720": {
        "description": "5 subjects, 540 music pieces, 10 genres, fMRI",
        "url": "https://openneuro.org/datasets/ds003720",
        "size_gb": 40.0,
        "license": "CC0",
        "source": "OpenNeuro ds003720",
        "download": "openneuro",
        "n_subjects": 5,
        "tr_seconds": 1.5,
    },
}
