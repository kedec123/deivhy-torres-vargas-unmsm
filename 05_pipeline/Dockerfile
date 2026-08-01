# Build from the repository root so the canonical requirements and DVC files are included:
# docker build -f 05_pipeline/Dockerfile -t endes-anemia-pipeline .
FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /project
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["bash"]
