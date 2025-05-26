FROM python:3.12-slim

WORKDIR /app

# デフォルトのエントリーポイントを設定
ARG ENTRYPOINT=src.example.entrypoint:app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080

CMD ["gunicorn", "--bind", ":$PORT", "--workers", "1", "--threads", "8", "--timeout", "0", "${ENTRYPOINT}"] 