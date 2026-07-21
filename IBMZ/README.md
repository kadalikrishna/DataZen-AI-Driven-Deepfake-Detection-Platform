# DataZen - Image and Video Deepfake Screening

DataZen is a Flask web application that screens images and sampled video frames for signs of AI generation or manipulation. It runs a quantized ONNX vision model locally inside the service and does not send uploaded media to an external inference API.

> DataZen provides a research screening signal, not forensic proof. Do not use its output as the sole basis for legal, employment, financial, safety, or other consequential decisions.

## Features

- Real pretrained model inference with `dima806/deepfake_vs_real_image_detection`
- Lightweight INT8 ONNX runtime designed for a 512 MB Render Free instance
- Image screening for JPG, JPEG, PNG, and WebP
- Video screening for MP4, MOV, AVI, and WebM
- Sequential video-frame processing to keep memory usage low
- Per-sample probabilities, overall verdict, processing time, and session statistics
- Temporary-file cleanup immediately after every successful or failed request
- Responsive browser interface and versioned JSON API

## How It Works

1. The server validates the file extension and upload size.
2. Images are resized and normalized for the bundled ONNX classifier.
3. Videos are inspected with FFprobe, then FFmpeg extracts up to four evenly spaced frames.
4. Frame probabilities are averaged into one video verdict.

The model is stored at `models/model_int8.onnx`. It is already quantized and committed to the repository, so Render does not need PyTorch or model conversion during deployment.

## Supported Media and Limits

| Media | Formats | Limits | Analysis |
|---|---|---|---|
| Image | JPG, JPEG, PNG, WebP | 20 MB; maximum 25 megapixels | One normalized image |
| Video | MP4, MOV, AVI, WebM | 20 MB; maximum 30 seconds | Up to four sampled frames |

Audio files and other extensions are intentionally rejected with HTTP `415`.

## Deploy Manually on Render Free

### 1. Create the service

1. Sign in to [Render](https://dashboard.render.com) with GitHub.
2. Select **New + > Web Service**.
3. Choose **Build and deploy from a Git repository**.
4. Connect:

   ```text
   kadalikrishna/DataZen-AI-Driven-Deepfake-Detection-Platform
   ```

### 2. Use these exact settings

| Render setting | Value |
|---|---|
| Name | `datazen-deepfake-screening` |
| Branch | `main` |
| Root Directory | `IBMZ` |
| Runtime | `Docker` |
| Instance Type | `Free` |
| Health Check Path | `/api/v1/health` |
| Auto Deploy | Enabled |

Leave **Build Command**, **Start Command**, **Docker Command**, and **Pre-Deploy Command** empty. The Dockerfile supplies the complete build and start configuration.

No database, persistent disk, secret, or environment variable is required.

### 3. Deploy

Click **Create Web Service**. If the service previously failed with the old model-export build, use:

```text
Manual Deploy > Clear build cache & deploy
```

The corrected image copies the bundled ONNX model directly and does not perform memory-heavy conversion.

### 4. Verify

Open:

```text
https://YOUR-SERVICE.onrender.com/api/v1/health
```

Expected response:

```json
{"service":"DataZen","status":"ok"}
```

Then open the service root URL and test a small JPG or PNG before testing video.

### Render Free behavior

- Free services sleep after inactivity and can take about a minute to wake.
- Session history is held in memory and resets whenever the instance restarts.
- The verified container uses approximately 230–250 MiB after loading the model.
- The first Docker build is slower than later cached builds because Render installs FFmpeg and Python dependencies.

## Run with Docker

### Requirements

- Docker Desktop or Docker Engine
- Approximately 1 GB of free disk space for build layers

From the `IBMZ` directory:

```powershell
docker build -t datazen .
docker run --rm -p 10000:10000 datazen
```

Open <http://127.0.0.1:10000>.

Check container health:

```powershell
curl.exe http://127.0.0.1:10000/api/v1/health
```

## Run Locally Without Docker

Use 64-bit Python 3.11. FFmpeg and FFprobe must be installed and available on `PATH` for video analysis.

```powershell
py -3.11 -m venv .venv
./.venv/Scripts/python.exe -m pip install --upgrade pip
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe app.py
```

Open <http://127.0.0.1:5000>.

Images work without FFmpeg. If FFmpeg is missing, video requests return a readable unsupported/corrupt-video error.

## Web Interface

1. Open the application.
2. Drag a supported image or video into the upload area, or click to browse.
3. Select **Run forensic analysis**.
4. Review the verdict, fake probability, sample evidence, model name, and processing time.
5. Use **History** to view or clear results from the current server session.

Uploaded files and extracted frames are deleted after inference. Only result metadata remains in the in-memory session history.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Web interface |
| `GET` | `/api/v1/health` | Service health |
| `GET` | `/api/v1/model/status` | Model, formats, and configured limits |
| `POST` | `/api/v1/upload` | Analyze one multipart file |
| `GET` | `/api/v1/incidents` | Current in-memory history |
| `GET` | `/api/v1/stats` | Current session totals |
| `POST` | `/api/v1/clear` | Clear current session history |

### Upload an image

```powershell
curl.exe -F 'file=@C:\path\to\image.jpg' http://127.0.0.1:10000/api/v1/upload
```

### Upload a video

```powershell
curl.exe -F 'file=@C:\path\to\video.mp4' http://127.0.0.1:10000/api/v1/upload
```

Successful results include:

- `verdict`: `likely_real`, `inconclusive`, or `likely_fake`
- `fake_probability` and `real_probability`
- `evidence`: per-image or per-frame scores
- `processing_time_ms` and `total_request_time_ms`
- `detection_id`, filename, size, media type, model, and timestamp

## Project Structure

```text
IBMZ/
├── app.py                    Deployment entry point
├── backend/
│   ├── app.py                Flask routes, validation, and history
│   └── detector.py           ONNX preprocessing and image/video inference
├── models/
│   ├── model_config.json     Preprocessing and label configuration
│   └── model_int8.onnx       Quantized visual classifier
├── static/                   CSS and browser JavaScript
├── templates/index.html      Web interface
├── Dockerfile                Render and Docker runtime image
├── render.yaml               Render service defaults
└── requirements.txt          Python runtime dependencies
```

## Troubleshooting

### Render says Dockerfile not found

Set **Root Directory** to exactly `IBMZ` and keep the Dockerfile path as `./Dockerfile`.

### Render shows the previous exit `137` or model-export failure

The old deployment is using cached layers. Select **Manual Deploy > Clear build cache & deploy** and confirm Render is building the latest `main` commit.

### Service starts but health checks fail

- Set the health-check path to `/api/v1/health`.
- Do not override the Docker start command.
- Confirm the logs show Gunicorn binding to `0.0.0.0` on Render's `PORT`.

### The optimized model cannot be loaded

Confirm both files exist in the deployed commit:

```text
IBMZ/models/model_int8.onnx
IBMZ/models/model_config.json
```

### Video analysis fails locally

Run `ffmpeg -version` and `ffprobe -version`. Install FFmpeg and ensure both commands are available on `PATH`. Docker and Render install them automatically.

### GitHub warns that the ONNX file is large

The model is approximately 83 MB. It is below GitHub's 100 MB hard limit and is intentionally stored in the repository to prevent Render Free from running out of memory during model conversion.

## Limitations

- The visual model can lose accuracy on new generators, heavy compression, crops, filters, or content unlike its training data.
- Video analysis samples frames instead of inspecting every frame.
- The system does not analyze audio tracks.
- A low or high probability is not proof of authenticity or manipulation.
- In-memory history is temporary and is not suitable for audit retention.
