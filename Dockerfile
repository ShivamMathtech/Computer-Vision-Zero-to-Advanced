FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN python -m pip install --no-cache-dir ".[api]" \
    && useradd --create-home --uid 10001 learner \
    && mkdir -p /data && chown learner:learner /data
USER learner
ENV CVZERO_DB=/data/events.sqlite3
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=2)"
CMD ["uvicorn", "cvzero.platform.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
