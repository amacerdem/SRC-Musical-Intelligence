# Musical Intelligence (MI)

White-box music cognition model grounded in neuroscience literature (251 papers, 1116 empirical claims).

## Architecture

Two implementations share the same pipeline pattern:

```
audio → cochlea(128D) → R³(49D) → H³(4-tuple) → Brain(26D) → L³(104D)
```

| Layer | Role | Dimensions |
|-------|------|-----------|
| **Ear / Cochlea** | Waveform → mel spectrogram | 128D |
| **R³** | Spectral feature extraction (consonance, energy, timbre, change, interactions) | 49D |
| **H³** | Hidden representation / temporal tracking | 4-tuple per R³ feature |
| **Brain** | Unified musical cognition output | 26D |
| **L³** | Semantic language layer | 104D |

### mi/ (Production - 44 files)
Stable, unified 26D brain + 104D semantic layer. Single `MIPipeline` class.

### mi_beta/ (Research - 225 files)
Dynamic architecture with 96 models across 9 cognitive units (ARU, STU, IMU, SPU, RPU, MPU, NDU, PCU, ASU), 10 shared mechanisms, and 5 cross-unit pathways.

## Running

```bash
# Production
python -m mi audio.wav [--json out.json] [--csv out.csv] [--plot] [--no-semantics]

# Beta self-test
python -m mi_beta
```

## Testing

```bash
pytest tests/           # All tests
pytest tests/unit/      # Unit only
pytest tests/ -v        # Verbose
```

Fixtures in `tests/conftest.py`: `sine_440`, `noise_1s`, `silence_1s`, `chirp_1s`, `config`, `cochlea_output`, `mel_spectrogram`, `random_r3`, `random_h3_avg`.

## Configuration

`mi/core/config.py` — immutable `MIConfig` dataclass:
- `sample_rate=44100`, `hop_length=512`, `n_fft=2048`, `n_mels=128`
- `r3_dim=49`, `device="cpu"`
- Singleton: `MI_CONFIG`

## Tensor Shapes

| Stage | Shape |
|-------|-------|
| Audio | (B, samples) |
| Mel | (B, 128, T) |
| R³ | (B, T, 49) |
| H³ | (B, T, 72) |
| Brain | (B, T, 26) |
| L³ | (B, T, 104) |

## Dependencies

`numpy`, `torch`, `torchaudio`, `soundfile`, `matplotlib` (optional for --plot), `pytest` (dev)

## Project Structure

```
mi/              Production module
mi_beta/         Research module
tests/           Unit, integration, validation tests
Literature/      Scientific papers, summaries, extractions (C³ + R³)
Road-map/        Architecture specs and model documents
Lab/             Experiments and demo visualization
Test-Audio/      WAV/MP3 test samples
```

## Conventions

- Deferred imports in CLI entry points for fast startup
- Structured output objects: `BrainOutput`, `EarOutput`, `MIOutput`
- Config is immutable singleton
- Literature organized by framework: C³ (cognitive), R³ (spectral), H³ (harmonic), L³ (language)
- Each cognitive unit has models named `{UNIT}-{variant}-{ACRONYM}` (e.g., ARU-alpha1-SRP)
