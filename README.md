# whisper-stt

A snap package that provides speech-to-text transcription using OpenAI's Whisper model. Runs as a daemon with a REST API for easy integration.

## Features

- **Daemon Service**: Runs automatically in the background on system startup
- **REST API**: Simple HTTP endpoints for transcription
- **GPU Acceleration**: NVIDIA CUDA support for fast inference (including Blackwell architecture)
- **Configurable**: Change model and port via `snap set` commands
- **Multiple Models**: Support for tiny, base, small, medium, and large Whisper models
- **Auto Model Download**: Models are downloaded automatically on first use

## Installation

### From Snap Store

```bash
snap install whisper-stt
```

### From Local Build

```bash
sudo snap install whisper-stt_*.snap --dangerous
```

### GPU Support

For NVIDIA GPU acceleration, connect the GPU interface:

```bash
snap connect whisper-stt:gpu-2404 mesa-2404:gpu-2404
```

## Configuration

Configure the service using `snap set`:

### Port

```bash
# Change the listening port (default: 9000)
snap set whisper-stt port=8080
```

### Model

```bash
# Change the Whisper model (default: base)
snap set whisper-stt model=small
```

Available models (listed by size/accuracy):
| Model | Parameters | Relative Speed | English-only | Multilingual |
|-------|------------|----------------|--------------|--------------|
| tiny | 39M | ~32x | tiny.en | tiny |
| base | 74M | ~16x | base.en | base |
| small | 244M | ~6x | small.en | small |
| medium | 769M | ~2x | medium.en | medium |
| large | 1550M | 1x | - | large, large-v2, large-v3 |

### View Current Configuration

```bash
snap get whisper-stt
```

## API Reference

### Health Check

Check if the service is running and view current configuration.

```bash
curl http://localhost:9000/health
```

Response:
```json
{
  "status": "healthy",
  "model": "base",
  "port": 9000,
  "device": "cuda",
  "gpu": "NVIDIA RTX 4090"
}
```

### Transcribe Audio

Transcribe an audio file to text.

```bash
curl -X POST http://localhost:9000/transcribe \
  -F "audio=@/path/to/audio.wav"
```

Optional parameters:
- `language`: Language code (e.g., "en", "es", "fr") - auto-detected if not specified
- `task`: "transcribe" (default) or "translate" (translates to English)

Example with options:
```bash
curl -X POST http://localhost:9000/transcribe \
  -F "audio=@audio.mp3" \
  -F "language=es" \
  -F "task=translate"
```

Response:
```json
{
  "text": "And so my fellow Americans, ask not what your country can do for you, ask what you can do for your country.",
  "language": "en",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 7.6,
      "text": " And so my fellow Americans ask not what your country can do for you,"
    },
    {
      "id": 1,
      "start": 7.6,
      "end": 10.6,
      "text": " ask what you can do for your country."
    }
  ]
}
```

### List Models

Get available Whisper models.

```bash
curl http://localhost:9000/models
```

Response:
```json
{
  "current": "base",
  "available": [
    "tiny", "tiny.en",
    "base", "base.en",
    "small", "small.en",
    "medium", "medium.en",
    "large", "large-v1", "large-v2", "large-v3"
  ]
}
```

## Supported Audio Formats

The service accepts any audio format supported by ffmpeg, including:
- WAV
- MP3
- FLAC
- OGG
- M4A
- WebM

## Service Management

```bash
# Check service status
snap services whisper-stt

# View logs
snap logs whisper-stt

# Restart the service
snap restart whisper-stt

# Stop the service
snap stop whisper-stt

# Start the service
snap start whisper-stt
```

## Building from Source

### Prerequisites

- snapcraft
- LXD or Multipass (for clean builds)

### Build

```bash
git clone https://github.com/kenvandine/whisper-stt.git
cd whisper-stt
snapcraft
```

### Install Local Build

```bash
sudo snap install whisper-stt_*.snap --dangerous
```

## System Requirements

### Minimum
- CPU: Any modern x86_64 processor
- RAM: 2GB (for tiny/base models)
- Storage: 2GB for snap + model storage

### Recommended (for GPU acceleration)
- NVIDIA GPU with CUDA support
- NVIDIA driver 525 or later
- 4GB+ VRAM (for small model), 8GB+ (for medium/large)

## Troubleshooting

### Service won't start

Check the logs:
```bash
snap logs whisper-stt -f
```

### GPU not detected

1. Ensure NVIDIA drivers are installed:
   ```bash
   nvidia-smi
   ```

2. Connect the GPU interface:
   ```bash
   snap connect whisper-stt:gpu-2404 mesa-2404:gpu-2404
   ```

3. Restart the service:
   ```bash
   snap restart whisper-stt
   ```

### Model download fails

Models are stored in `$SNAP_COMMON/.cache`. Ensure sufficient disk space and network connectivity.

## License

This snap packages [OpenAI Whisper](https://github.com/openai/whisper) which is released under the MIT License.
