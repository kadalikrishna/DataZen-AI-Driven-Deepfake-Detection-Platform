# DataZen Image and Video Deepfake Screening

DataZen performs local deepfake screening with a quantized ONNX visual model. It is designed to fit the 512 MB Render Free web-service limit.

## Supported media

- Images: JPG, JPEG, PNG and WebP, under 20 MB and 25 megapixels
- Videos: MP4, MOV, AVI and WebM, under 20 MB and 30 seconds
- Videos are represented by at most four evenly spaced frames

The service uses `dima806/deepfake_vs_real_image_detection`. Results are research screening signals, not proof, and may not generalize to new generators or heavily compressed media.

## Deploy to Render Free

1. Push this directory to a GitHub repository.
2. In Render, choose **New > Blueprint**.
3. Connect the repository and apply `render.yaml`.
4. Wait for the Docker build to download, export and quantize the model.
5. Open the generated `onrender.com` URL and test a small image first.

No environment variables, database or persistent disk are required. Free services sleep after inactivity, so the first request can take about a minute. Session history is in memory and resets after a restart.

## Docker

The multi-stage Docker build uses PyTorch only while exporting the model. The final image contains ONNX Runtime, Flask, Pillow and FFmpeg.

```powershell
docker build -t datazen .
docker run --rm -p 10000:10000 datazen
```

Open <http://127.0.0.1:10000>.

## Local development without Docker

Use 64-bit Python 3.11:

```powershell
py -3.11 -m venv .venv
./.venv/Scripts/python.exe -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
./.venv/Scripts/python.exe -m pip install -r requirements-build.txt
./.venv/Scripts/python.exe setup_models.py
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe app.py
```

## API

- `POST /api/v1/upload` - multipart form with a `file` field
- `GET /api/v1/model/status` - model, formats and limits
- `GET /api/v1/incidents` - in-memory session history
- `GET /api/v1/stats` - session verdict counts
- `POST /api/v1/clear` - clear session history
- `GET /api/v1/health` - health check

Uploaded media and extracted video frames are deleted immediately after inference.
