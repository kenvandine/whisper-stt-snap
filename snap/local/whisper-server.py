#!/usr/bin/env python3
"""Whisper speech-to-text HTTP server."""

import os
import tempfile
import torch
import whisper
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load configuration from environment
PORT = int(os.environ.get('WHISPER_PORT', 9000))
MODEL_NAME = os.environ.get('WHISPER_MODEL', 'base')

# Detect GPU availability
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
GPU_NAME = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None

print(f"Device: {DEVICE}" + (f" ({GPU_NAME})" if GPU_NAME else ""))

# Load model at startup
print(f"Loading Whisper model: {MODEL_NAME}")
model = whisper.load_model(MODEL_NAME, device=DEVICE)
print(f"Model loaded successfully. Server starting on port {PORT}")


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model': MODEL_NAME,
        'port': PORT,
        'device': DEVICE,
        'gpu': GPU_NAME
    })


@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Transcribe audio file to text.

    Accepts audio file as multipart form data with key 'audio'.
    Optional parameters:
        - language: Language code (e.g., 'en', 'es', 'fr')
        - task: 'transcribe' or 'translate' (translate to English)
    """
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No audio file selected'}), 400

    # Get optional parameters
    language = request.form.get('language')
    task = request.form.get('task', 'transcribe')

    if task not in ('transcribe', 'translate'):
        return jsonify({'error': 'Invalid task. Use "transcribe" or "translate"'}), 400

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        # Transcribe the audio
        options = {'task': task}
        if language:
            options['language'] = language

        result = model.transcribe(tmp_path, **options)

        return jsonify({
            'text': result['text'],
            'language': result.get('language'),
            'segments': result.get('segments', [])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.route('/models', methods=['GET'])
def list_models():
    """List available Whisper models."""
    return jsonify({
        'current': MODEL_NAME,
        'available': [
            'tiny', 'tiny.en',
            'base', 'base.en',
            'small', 'small.en',
            'medium', 'medium.en',
            'large', 'large-v1', 'large-v2', 'large-v3'
        ]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, threaded=True)
