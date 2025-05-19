import json
import os
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.responses import Response
from google.cloud.storage import Client
from pydantic import BaseModel


class SaveResultRequest(BaseModel):
    result: Dict[str, Any]
    bucket: str
    object: str


app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    """ヘルスチェックエンドポイント
    DBやAPIの疎通確認もここで行うといいです。
    """
    return {"status": "ok"}


@app.post("/")
async def save_result(request: Request) -> Response:
    request_json = await request.json()

    save_request = SaveResultRequest(**request_json)
    response_data = json.dumps(save_request.result)

    storage_client = Client()
    bucket = storage_client.get_bucket(save_request.bucket)
    blob = bucket.blob(save_request.object)
    print(f"Saving result to {save_request.object} in bucket {save_request.bucket}.")
    blob.upload_from_string(response_data, content_type="application/json")
    print("File saved.")

    return Response(status_code=201)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", 8082)))
