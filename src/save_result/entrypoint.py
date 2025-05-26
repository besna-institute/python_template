import json
import os

from fastapi import FastAPI, Request
from fastapi.responses import Response
from google.cloud.storage import Client

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    """ヘルスチェックエンドポイント
    DBやAPIの疎通確認もここで行う。
    """
    return {"status": "ok"}


@app.post("/")
async def save_result(request: Request) -> Response:
    request_json = await request.json()
    response_data = json.dumps(request_json)

    storage_client = Client()
    bucket = storage_client.get_bucket(request_json["bucket"])
    blob = bucket.blob(request_json["object"])
    print(f"Saving result to {request_json['object']} in bucket {request_json['bucket']}.")
    blob.upload_from_string(response_data, content_type="application/json")
    print("File saved.")

    return Response(status_code=201)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", 8082)))
