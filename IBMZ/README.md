---
title: DataZen Deepfake Screening
emoji: 🛡️
colorFrom: green
colorTo: gray
sdk: docker
app_port: 7860
fullWidth: true
---

# DataZen Multimodal Deepfake Screening

DataZen now performs real, local pretrained-model inference. It does not generate random scores.

## Supported media

- Images: JPG, JPEG, PNG, WebP
- Video: MP4, MOV, AVI, WebM (up to 120 seconds; 12 sampled frames)
- Speech audio: WAV, FLAC, MP3, OGG, M4A (up to 5 minutes; sampled 4-second segments)
- Maximum upload size: 50 MB

Visual media uses `dima806/deepfake_vs_real_image_detection`. Speech uses `Vansh180/deepfake-audio-wav2vec2`. Results are research screening signals, not proof, and may not generalize to new generation methods or heavily compressed media.

## Windows setup

Use 64-bit Python 3.10 or newer. From PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe setup_models.py
.\start.ps1
```

Open <http://127.0.0.1:5000>. The model setup command downloads both checkpoints once; cached models can then run offline.

## Docker deployment

The included Dockerfile is ready for a Hugging Face Docker Space and exposes port 7860. It installs CPU-only PyTorch, downloads both model checkpoints during the image build, and runs Flask through Gunicorn.

```powershell
docker build -t datazen .
docker run --rm -p 7860:7860 datazen
```

## API

- `POST /api/v1/upload` — multipart form with a `file` field
- `GET /api/v1/model/status` — models, load state, formats, and limits
- `GET /api/v1/incidents` — current in-memory session history
- `GET /api/v1/stats` — session verdict counts
- `POST /api/v1/clear` — clear session history
- `GET /api/v1/health` — service health

Uploaded media is processed through a temporary file and deleted after inference. History is held in memory and resets when the server restarts.
