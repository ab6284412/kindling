FROM python:3.12-slim AS builder
WORKDIR /build
RUN pip install --no-cache-dir --prefix=/install fastapi uvicorn psycopg[binary]

FROM python:3.12-slim
COPY --from=builder /install /usr/local
RUN useradd -m appuser
WORKDIR /app
COPY app.py /app/
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
