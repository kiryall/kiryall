FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app \
    APP_MODE=streamlit

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY configs ./configs
COPY scripts ./scripts
COPY src ./src
COPY ui ./ui
COPY models ./models
COPY output ./output

RUN pip install --upgrade pip && pip install .

EXPOSE 8501

CMD ["bash", "-lc", "if [ \"$APP_MODE\" = \"cli\" ]; then python scripts/run_pipeline.py --input-dir /data/input --output-dir /data/output; else streamlit run ui/streamlit_app.py --server.address=0.0.0.0 --server.port=8501; fi"]
