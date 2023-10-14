FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*
COPY . .
ENTRYPOINT ["python", "main.py"]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