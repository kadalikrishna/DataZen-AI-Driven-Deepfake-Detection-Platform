FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=10000 DATAZEN_MODEL_PATH=/home/user/app/models/model_int8.onnx DATAZEN_MODEL_CONFIG=/home/user/app/models/model_config.json
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/* && useradd -m -u 1000 user
WORKDIR /home/user/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=user:user . .
USER user
EXPOSE 10000
CMD exec gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 1 --threads 1 --timeout 300 app:application
