# pylint: disable=duplicate-code
import json
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from src.example.solvers import SomeSolver
from src.logger import LoggingMiddleware, logger
from src.models import Input, Output

app = FastAPI()

app.add_middleware(LoggingMiddleware)


@app.get("/health")
async def health() -> dict[str, str]:
    """ヘルスチェックエンドポイント
    DBやAPIの疎通確認もここで行う。
    """
    logger.info("Health check")
    return {"status": "ok"}


@app.post("/")
async def example(request: Request) -> Response:
    """サンプル

    JSON Lines を入力とする場合
      Content-Type: application/jsonl

    JSON を入力とする場合
      Content-Type: application/json
    """
    logger.info("Received request")
    match request.headers.get("content-type", ""):
        case "application/jsonl":
            jsonl_request_body: bytes = await request.body()
            logger.info("Request Body (JSONL): %s", jsonl_request_body.decode())
            result: list[str] = []
            for json_str in jsonl_request_body.decode().splitlines():
                if not json_str:
                    continue
                request_json = json.loads(json_str)
                input_: Input = Input(api_name=request_json["api_name"], name=request_json["name"])
                output_: Output = SomeSolver().process(input=input_)
                result.append(json.dumps(output_.to_dict()))
            response_content = "\n".join(result)
            logger.info("Response Body (JSONL): %s", response_content)
            return Response(content=response_content, media_type="application/jsonl")
        case _:
            request_json = await request.json()
            logger.info("Request Body: %s", json.dumps(request_json))
            input__: Input = Input(api_name=request_json["api_name"], name=request_json["name"])
            output__: Output = SomeSolver().process(input=input__)
            response_content = output__.to_dict()
            logger.info("Response Body: %s", json.dumps(response_content))
            return JSONResponse(content=response_content)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", 8080)))
