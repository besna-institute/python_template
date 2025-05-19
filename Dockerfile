FROM python:3.12-slim

WORKDIR /app

# デフォルトのエントリーポイントを設定
ARG ENTRYPOINT=src.example.entrypoint:app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080

CMD ["uvicorn", "${ENTRYPOINT}", "--host", "0.0.0.0", "--port", "${PORT}"] 